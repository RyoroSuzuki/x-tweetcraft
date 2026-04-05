# Schedule Templates

Pre-built recurring schedules for x-tweetcraft. Each template is a complete specification that x-schedule can adapt to user preferences.

## `$PLUGIN_DIR` について

各テンプレート内の `$PLUGIN_DIR` は、**ユーザーがx-tweetcraftをcloneした場所**に置換します。
- 例: `~/x-tweetcraft`、`~/Documents/x-tweetcraft`
- 統合モデル（推奨）では、ここがプラグイン兼ユーザーデータのディレクトリ
- cronタスク登録時に x-schedule スキルが絶対パスに展開する

---

## Template A: 朝の下書き準備

**目的**: 起床前に最新トレンド・自分の投稿分析・下書き10案を準備。朝起きたらすぐ選んで投稿するだけの状態にする。

**デフォルトcron**: `0 6 * * *`（毎朝6時）
**実行時間**: 約3-5分
**API依存**: x-analyze-posts（軽量） + x-research-trends（軽量） + x-draft

**実行プロンプト:**
```
cd $PLUGIN_DIR && claude -p "brand-voice.mdを読み込んで、まずx-analyze-postsを軽量モードで実行（直近10件の傾向把握のみ）、次にx-research-trendsを軽量モードで実行（1-2件のトレンド把握のみ）、最後にx-draftを起動して下書き10案を生成。結果を personal-info/draft-logs/$(date +%Y-%m-%d)_morning.md に保存。API未接続時はL2/L3をスキップしてbrand-voice.md単独で生成。"
```

**出力先**: `personal-info/draft-logs/YYYY-MM-DD_morning.md`

**API未接続時のフォールバック**: brand-voice.mdとlearnings.mdのみで下書き生成

**カスタマイズ可能な項目**:
- 時刻（デフォルト6時）
- 平日のみ / 毎日
- 下書き案数（10 → 5-15）
- 軽量モード vs 完全モード

---

## Template B: 週次戦略レビュー

**目的**: 先週の振り返り＋今週の方向性を `x-content-strategist` エージェントが提案。

**デフォルトcron**: `0 8 * * 1`（毎週月曜8時）
**実行時間**: 約5-10分
**API依存**: x-content-strategist（L2+L3 full）

**実行プロンプト:**
```
cd $PLUGIN_DIR && claude -p "x-content-strategistエージェントを起動。先週7日間の投稿実績分析＋市場トレンド調査＋brand-voiceとのギャップ分析をして、今週の戦略レポートを personal-info/strategy-reports/$(date +%Y-%m-%d)_weekly.md に保存。"
```

**出力先**: `personal-info/strategy-reports/YYYY-MM-DD_weekly.md`

**API未接続時のフォールバック**: brand-voice.mdと直近draft-logsから質的な振り返りのみ実施

**カスタマイズ可能な項目**:
- 曜日（デフォルト月曜）
- 時刻（デフォルト8時）
- 分析対象期間（7日 / 14日）

---

## Template C: 月次ブランドリフレッシュ

**目的**: `x-refresh-brand-voice` で過去100件以上の投稿を深く分析し、brand-voiceを実績ベースでアップデート。

**デフォルトcron**: `0 9 1 * *`（毎月1日9時）
**実行時間**: 約10-15分
**API依存**: ⚠️ P1実装予定のため現時点では動作しない

**実行プロンプト:**
```
cd $PLUGIN_DIR && claude -p "x-refresh-brand-voiceスキルを起動。過去100件の投稿とメトリクスを分析して、personal-info/public-voice.md のパターン・型セクションをアップデート提案。ユーザー不在実行のため、変更提案は personal-info/analysis-logs/$(date +%Y-%m-%d)_brand-refresh-proposal.md に保存（自動適用はしない）。"
```

**出力先**: `personal-info/analysis-logs/YYYY-MM-DD_brand-refresh-proposal.md`

**重要**: 自動適用せず「提案ファイル」として保存。ユーザーが後で確認して手動反映。

**カスタマイズ可能な項目**:
- 月の何日に実行するか
- 分析対象件数（100 / 200 / 全件）

---

## Template D: カスタム

**目的**: ユーザーが独自のスケジュールを定義。

**設定フロー:**
1. cron expression入力（または「毎日夜9時」等の自然言語）
2. 実行したいスキル/エージェント名
3. 引き継ぎたいコンテキスト（ある場合）
4. 出力先ファイルパス

**実行プロンプト生成**:
```
cd $PLUGIN_DIR && claude -p "[user-defined prompt]"
```

---

## 組み合わせ推奨パターン

### 最小セット（推奨・API未接続でも動く）
- Template A（朝の下書き準備）のみ
- 1日1回、確実に下書きができた状態で朝を迎える

### 標準セット（API接続後・バランス型）
- Template A（毎日）
- Template B（週次）
- この2つで日常運用＋戦略が回る

### フルセット（API接続後・本格運用）
- Template A, B, C すべて
- 月次のブランドリフレッシュまで含めた全自動運用

---

## cron expression ちょいガイド

| 表現 | 意味 |
|------|------|
| `0 6 * * *` | 毎日6時 |
| `0 6 * * 1-5` | 平日6時（月〜金） |
| `0 8 * * 1` | 毎週月曜8時 |
| `0 9 1 * *` | 毎月1日9時 |
| `*/30 * * * *` | 30分ごと（使用非推奨） |

## セキュリティ注意

- スケジュールコマンドに `X_API_KEY` 等の認証情報をベタ書きしない
- `.env` ファイル参照にとどめる
- スケジュールログにAPIキーが漏れないか確認
