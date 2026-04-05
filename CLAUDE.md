# CLAUDE.md - x-tweetcraft

このファイルは x-tweetcraft プラグイン内の Claude Code 用指示書。プラグインを利用する際、またはプラグイン自体の拡張・保守を行う際に Claude が参照する。

## プラグインの目的

**「自動化しても、自分の声を失わない」** をコンセプトにしたX（Twitter）投稿支援プラグイン。

ユーザーのブランドボイス（トーン・テーマ・型・価値観）を元に、ツイートの下書きを生成し、半自動で運用できる状態を作る。

## 全体アーキテクチャ

### 3レイヤー設計

```
L1: 生成
  └ brand-voice.md → 下書き5-10案
L2: 分析・学習
  └ 過去投稿の実績データ → 伸びる型の分析 → 仮説
L3: 市場調査
  └ トレンド検索 → 勝ちパターンの取り込み
```

この3レイヤーを統合して「○○の訴求 × ○○の型が伸びそう」という仮説を立て、下書きに反映する。

### プログレッシブ・エンハンスメント方式

X API未接続でも動作するが、接続すると段階的に機能が拡張される：

| 機能 | API未接続 | API接続後 |
|------|----------|----------|
| 下書き生成 (L1) | ✅ brand-voice.mdベース | ✅ + 実績+トレンド |
| 過去投稿分析 (L2) | ❌ | ✅ 深い分析 |
| トレンド分析 (L3) | ❌ | ✅ Basic推奨 |
| 自動投稿 | ❌ クリップボード | ✅ 直接投稿 |
| 週次戦略 | ❌ | ✅ agent起動可 |

## ディレクトリ構造

```
x-tweetcraft/
├── .claude-plugin/
│   └── plugin.json                    # プラグイン定義
├── .mcp.json                           # MCPサーバー登録
├── CLAUDE.md                           # このファイル（Claude向け指示書）
├── README.md                           # 人間向けドキュメント
├── data/                               # 共通データ・テンプレート
│   ├── brand-voice-template.md         # ブランドボイステンプレート
│   └── browser-extraction-prompts.md   # 共通ブラウザ拡張プロンプト集
├── skills/                             # Claudeが読む手順書（8スキル）
│   ├── x-setup/SKILL.md
│   ├── x-interview/
│   │   ├── SKILL.md
│   │   └── references/interview-questions.md
│   ├── x-draft/SKILL.md
│   ├── x-reflect/SKILL.md
│   ├── x-schedule/
│   │   ├── SKILL.md
│   │   └── references/schedule-templates.md
│   ├── x-connect-api/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── api-plans-and-costs.md
│   │       ├── detailed-setup-guide.md
│   │       ├── python-env-setup.md
│   │       └── credential-input-guide.md
│   ├── x-analyze-posts/SKILL.md
│   └── x-research-trends/SKILL.md
├── agents/                             # 独立起動するサブエージェント
│   └── x-content-strategist.md
└── mcp-server/                         # 自作MCPサーバー（X API v2ラッパー）
    ├── server.py                       # FastMCP + tweepy、~150行
    ├── requirements.txt
    ├── setup-credentials.py            # 対話型認証情報入力スクリプト
    └── .env.example
```

## Skills（手順書）

各skillは特定のタスクを実行するためのClaude向け手順書。ユーザーの発話がdescriptionにマッチすると起動する。

| Skill | 起動タイミング | 役割 | APIレイヤー |
|-------|-------------|------|------------|
| `x-setup` | 初回オンボーディング | brand-voice構造を生成 | L1のみ |
| `x-interview` | brand-voice深化希望 | 6Round対話型インタビュー（再開可） | 不要 |
| `x-draft` | 「今日のツイート作って」 | 下書き5-10案生成（統合型）、draft-logs/に自動保存 | L1+L2+L3軽量 |
| `x-improve` | 「精度を上げたい」「下書きが浅い」 | ズレを診断→最適な改善手段へルーティング | 不要 |
| `x-reflect` | x-draft後のフィードバック時 | 採用/却下/編集から学習してlearnings.mdに蓄積 | 不要 |
| `x-schedule` | 自動化セットアップ | 朝の下書き準備・週次レビュー等をcron登録 | 設定 |
| `x-connect-api` | X API接続希望 | Developer Portal申請ガイド | 設定 |
| `x-analyze-posts` | 自分の投稿分析希望 | L2単独・深い分析 | L2 |
| `x-research-trends` | 市場調査希望 | L3単独・トレンド研究 | L3 |

## Agents（サブエージェント）

agentsはClaudeが必要に応じて起動するサブエージェント。長時間の分析や独立した文脈が必要なタスクを担当。

| Agent | 起動タイミング | 役割 |
|-------|-------------|------|
| `x-content-strategist` | 週次レビュー・戦略相談 | L2+L3+brand-voiceを統合して戦略提案 |

## MCP Server（自作・X API v2ラッパー）

`mcp-server/server.py` は自作のMCPサーバー。X API v2を呼ぶためのPythonツール群を提供。

### 設計原則

- **最小スコープ** — x-tweetcraftが必要とする4関数のみ（~150行）
- **監査可能性** — コード量を抑えてユーザーが読める状態に
- **セキュリティ優先** — コミュニティMCPへの依存リスクを避けて自作
- **公式ドキュメント準拠** — tweepy + X API v2 公式リファレンスに沿って実装

### 提供ツール

| ツール | 用途 | APIプラン要件 |
|--------|------|-------------|
| `post_tweet(text)` | ツイート投稿 | Free以上 |
| `get_my_tweets(count=30)` | 自分の投稿取得 | Free（制限大）／Basic推奨 |
| `get_tweet_metrics(tweet_id)` | メトリクス取得 | Free（一部のみ）／Basic推奨 |
| `search_trending(query, count=20)` | 検索 | **Basic必須** |

### セキュリティ

- 認証情報は `~/.x-tweetcraft.env`（ホーム直下、リポジトリ外）
- `chmod 600` で所有者のみ読み取り可能
- 各tweepy関数呼び出しにX API公式ドキュメントのURLをコメント記載
- APIキーをログに出さない（エラー時も）

### 動作確認ステータス

⚠️ 実X APIキーでのエンドツーエンドテストは **未完了**。コードはドキュメント通り実装されているが、実際の挙動は使用者が自己責任で検証する必要がある。

## Brand Voice の2層設計

**ユーザーの作業ディレクトリに生成される構造:**

```
brand-voice.md                    # 目次 + クイックサマリ + コマンド案内
personal-info/
├── public-voice.md               # 公的: トーン・テーマ・型・NG事項
├── values-and-origin.md          # 私的: 価値観・原体験・キャリア
├── audience-and-messages.md      # 私的: 届けたい人・コアメッセージ
├── learnings.md                  # x-reflectが蓄積するユーザーの好み学習
├── schedules.md                  # x-scheduleが登録した自動実行の一覧
├── interview-logs/               # x-interviewセッション記録
├── draft-logs/                   # x-draftの全出力履歴（自動保存）
├── analysis-logs/                # x-analyze-posts レポート
├── strategy-reports/             # x-content-strategist レポート
└── trend-reports/                # x-research-trends レポート
```

### 設計思想

- **Public（公的レイヤー）** → ツイートに直接反映してOK（トーン、テーマ、型、NG事項）
- **Private（私的レイヤー）** → 視点・動機の「源」として内部参照。**直接ツイート化しない**

なぜこの設計か：
- 原体験・価値観転換ストーリー等は「成功してから語れる」という心理がある
- ユーザーが「まだ何者でもない」段階でも、私的レイヤーを育てられる
- 節目で「取り出して公開」する選択肢を残す

**重要:** x-draft などのskillは両レイヤーを読むが、Privateレイヤーの内容を**直接引用してツイートを生成してはいけない**。Privateレイヤーは「視点の持ち方」の参考情報。

## ユーザー導線

### 初回セットアップ

```
ユーザー「x-tweetcraftセットアップして」
  ↓
x-setup起動
  ↓ (Companion Skills確認 → X アカウント → ツイートサンプル → brand-voice雛形)
「Round 1 だけインタビューする？」
  ↓
x-interview（任意）
  ↓
完了。「今日のツイート作って」で x-draft が使える状態
```

### 日常運用

```
「今日のツイート作って」 → x-draft → 下書き5-10案
  ↓
ユーザーが選択・編集
  ↓
API接続済: x-post で投稿 / 未接続: クリップボードコピー
```

### 深掘り・分析

```
「もっとbrand-voice深めたい」→ x-interview （分割OK、再開可）
「自分の投稿分析して」     → x-analyze-posts （API必要）
「今何がウケてるか調べて」  → x-research-trends （API必要）
「今週の戦略立てたい」     → x-content-strategist agent （API推奨）
```

## 拡張ガイドライン

### 新しいskillを追加するとき

1. `skills/<name>/SKILL.md` を作成
2. frontmatter の `name` と `description` を明確に（トリガー判定に使われる）
3. 既存skillのパターンを踏襲（Workflow、Edge Cases、Red Flagsセクション）
4. Public/Privateレイヤーの使い分けを守る
5. API未接続時のフォールバック動作を明記

### 新しいagentを追加するとき

1. `agents/<name>.md` を作成
2. frontmatter の `description` に「いつ使うか」を明記（複数example入り）
3. `plugin.json` の `agents` フィールドに追加
4. 独立文脈で動くことを前提に設計（パラメータを明示的に受け取る）

### skill vs agent の判断基準

- **skill**: 対話型・1回完結・Claudeと人間がやりとりしながら進める
- **agent**: 長時間実行・独立処理・複数データソース統合・定期実行を想定

## API接続関連

### 必要な認証情報

ユーザーの `~/.x-tweetcraft.env` に保存（Gitコミットしない）：

```
X_BEARER_TOKEN=...
X_API_KEY=...
X_API_SECRET=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
```

### X API プランと制限

| 機能 | Free | Basic ($200/月) |
|------|------|---------------|
| 投稿 | 1,500/月 | 3,000/月 |
| 自分の投稿取得 | 10,000/月 | 50,000/月 |
| ツイート検索 | ❌ | ✅ |
| メトリクス | 制限あり | 詳細取得 |

**MVP運用はFreeで可。L3（トレンド分析）を本格運用するならBasic必要。**

## 思想・トーン

- **同じ道を迷いながら歩く同志**（上から目線の師匠ではない）
- **盛らず・カッコつけず・等身大**で発信を支援する
- **バズりより継続性**を重視

このトーンはgenerateされるすべてのツイートに適用される。ユーザーのbrand-voice.mdがさらにこれを個別化する。

## メンテナンス

- 新機能追加時: このCLAUDE.mdを更新
- skill追加時: Skills表を更新
- agent追加時: Agents表 + `plugin.json` を更新
- API仕様変更時: API接続関連セクションを更新
