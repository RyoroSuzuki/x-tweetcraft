# x-tweetcraft

自分のブランドボイスを保ったまま、X（Twitter）の投稿を半自動化するClaude Codeプラグイン。

「自動化しても、自分の声を失わない」がコンセプト。

## できること

- **パーソナライズされた下書き生成** — あなたのトーン・テーマ・型に沿ったツイート案を5-10件
- **2層構造のブランドボイス** — 公開用（Public）と内部参照用（Private）を分離
- **分割可能なインタビュー** — 複数セッションに分けてブランドボイスを育てられる
- **段階的な機能拡張** — X API未接続でも動作。接続後に自動投稿・分析が使える

## 同梱スキル

| スキル | 役割 |
|--------|------|
| `x-setup` | 初回オンボーディング。Xアカウントとツイートからブランドボイスを生成 |
| `x-interview` | 6ラウンドの対話型インタビュー（途中停止・再開OK） |
| `x-draft` | 下書き5-10案を生成。仮説と根拠付き |
| `x-connect-api` | X Developer API申請・認証設定をガイド |

**P1（X API接続後に追加予定）:**
- `x-post` — 下書きを直接投稿
- `x-refresh-brand-voice` — 過去投稿100件以上を分析してブランドボイスを深化
- `x-reflect` — 採用/却下された下書きから自律学習

## インストール

### 前提: 相性のいいCompanion Skills（推奨）

x-tweetcraftと併用すると便利なClaude Code公式スキル：

- **`document-skills@anthropic-agent-skills`** — PDF/Word/Excel/PowerPointを読み込める（職歴書・ブランド資料の分析に便利）
- **`superpowers@claude-plugins-official`** — ブレスト・計画・TDD等の汎用ワークフロー（コンテンツ戦略に活用）

インストールコマンド:
```bash
claude plugin install document-skills@anthropic-agent-skills
claude plugin install superpowers@claude-plugins-official
```

### x-tweetcraft本体

**方法A: ローカル開発用（推奨・今のところ）**
```bash
git clone https://github.com/RyoroSuzuki/x-tweetcraft.git ~/develop/x-tweetcraft
claude --plugin-dir ~/develop/x-tweetcraft
```

**方法B: マーケットプレース経由（公開後）**
```bash
claude plugin install x-tweetcraft@<marketplace-name>
```

## 使い方

### 初回セットアップ

```
「x-tweetcraftをセットアップして」
```

x-setupスキルが起動して、以下を案内します:
1. 推奨Companion Skillsのチェック
2. あなたのXアカウント情報のヒアリング
3. ツイートサンプルの収集（コピペ または Claudeブラウザ拡張）
4. ブランドボイス雛形の生成
5. x-interviewへの連続オファー（深掘り希望の場合）

### 日常の下書き生成

```
「今日のツイート作って」
```

ブランドボイスを元に下書き5-10案を生成。仮説・根拠・推奨パターン付き。

### ブランドボイスを深める

```
「x-interviewで深めたい」
```

6ラウンドの対話型インタビューを実行。1日1ラウンドでも、まとめてでも、自由なペースで。前回の続きから再開できます。

### X APIを接続する

```
「x-connect-apiして」
```

X Developer Portal申請、App作成、認証情報設定、接続テストまでガイドします。

## ブランドボイスの構造

セットアップ後、あなたの作業ディレクトリに以下が作成されます:

```
brand-voice.md                    # 目次 + クイックサマリ + コマンド案内
personal-info/
├── public-voice.md               # 公的: トーン・テーマ・型・NG事項
├── values-and-origin.md          # 私的: 価値観・原体験・キャリア
├── audience-and-messages.md      # 私的: 届けたい人・コアメッセージ
└── interview-logs/               # x-interviewセッション記録
```

### 2層設計の意図

- **Public（公的レイヤー）** — ツイートに直接反映してOKな要素（トーン、テーマ、型）
- **Private（私的レイヤー）** — 視点・動機の「源」。x-draftが内部参照するが直接ツイート化はしない

原体験・価値観転換ストーリー等を「公開する前の準備段階」として保管でき、成功や節目が来た時に取り出せる設計です。

## 思想

> 「同じ道を迷いながら歩く同志」
>
> 上から目線の師匠でもなく、コーチでもなく、ただ同じ道を歩いている人。隣から気づきを置いていくくらいの距離感。

x-tweetcraftは、**盛らず・カッコつけず・等身大**で発信を続けたい人のためのツールです。バズりを狙うのではなく、**自分の声を失わずに発信を継続する**ことに価値を置きます。

## PCへの負荷について

**現時点: ゼロです。**

このプラグインは **Markdown形式のスキル集** であり、Claude Codeが必要な時に読むだけです。サーバーもバックグラウンドプロセスも立ち上がりません。

将来、X API接続用のMCPサーバーを追加した場合でも、それはClaude Codeセッション中にのみ動く軽量なプロセスです（常駐しません）。

## 開発状況

- ✅ **MVP**: ブランドボイス生成、下書き生成、インタビュー、API接続ガイド
- ⏳ **P1**: X API統合（MCPサーバー、自動投稿、分析）
- 🔜 **P2**: 学習ループ（x-reflect）

## ライセンス

MIT

## 作者

鈴木遼郎（[株式会社VITAL Z](https://www.vital-z.co.jp/)）
