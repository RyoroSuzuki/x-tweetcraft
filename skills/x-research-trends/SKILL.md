---
name: x-research-trends
description: Research current high-performing tweet patterns and formats in the user's themes/domains on X (Twitter). Use when the user says "今伸びてるツイート調べて", "トレンド分析して", "勝ちパターン見つけて", "research trending tweets", "what's working on X now", or wants standalone market research beyond what x-draft does inline. Ideally uses X API search (Basic plan or above). Falls back to WebSearch/WebFetch and user-provided examples if API limited.
---

# x-research-trends

Research market trends in tweets relevant to the user's themes, identify winning formats, and translate them into the user's voice. This is the L3 (市場調査) skill in x-tweetcraft's 3-layer architecture.

**⚠️ MCP server status:** x-tweetcraft MCP server is planned (P1) but not yet implemented. When MCP is unavailable, this skill falls back to Claude browser extension / WebSearch / user-provided tweet samples. See Step 2 for method selection.

## Workflow

### Step 1: Determine research targets

Read the user's brand-voice to identify target domains. Search for `brand-voice.md` in this order (unified across all x-tweetcraft skills):
1. `./brand-voice.md` (current working directory)
2. `./ceo/x-automation/brand-voice.md` (VITAL Z convention)
3. `~/brand-voice.md` (user home)

Then read the referenced personal-info files:
- `personal-info/public-voice.md` (テーマセクション)
- `personal-info/audience-and-messages.md` (届けたい人)

Ask the user:
> トレンドリサーチ、どの切り口で進めますか？（複数選択可）
>
> A) **あなたのテーマ領域** — [読み取ったテーマをリスト] の最近伸びてる投稿
> B) **届けたい人の関心領域** — [ターゲットセグメント] にウケてる投稿
> C) **特定のキーワード** — あなたが調べたい言葉を指定
> D) **特定アカウントの型** — ロールモデルのツイートパターンを分析

### Step 2: Check research method availability

Evaluate what tools are available:

| 方法 | 条件 | 得られるもの |
|------|------|-----------|
| **X API search** | Basic plan以上 ($200/月) | 完全な検索・メトリクス |
| **Claudeブラウザ拡張** | ユーザーのブラウザに拡張あり | 良質な手動リサーチ |
| **WebSearch + 公開情報** | 常時可 | 記事・まとめページ経由の情報 |
| **ユーザー提供のツイート** | ユーザーが手動でコピペ | 確実だが時間コスト |

**Prefer order:** X API > Claude browser extension > User paste > WebSearch

### Step 3: Gather samples

**API mode (X API Basic+):**
- Use `mcp__x_tweetcraft__search_trending` with user's keywords
- Fetch 30-50 high-engagement tweets per topic cluster
- Filter: recent (last 7-14 days), meaningful engagement

**Browser extension mode:**
- Give user a prompt to paste into Claude browser extension
- Prompt template:
  ```
  【背景】
  私は自分のX発信の戦略を立てるために、最近伸びている関連ツイートの型をリサーチしています。

  【抽出してほしい情報】
  この検索結果ページから、エンゲージメントの高そうなツイート（いいね100以上 or リプライ10以上）を
  10-20件抽出してください。

  【出力フォーマット】
  ---
  ### ツイート1
  **本文:** [そのまま]
  **投稿者:** [@ハンドル]
  **いいね/RP/リプライ:** [数字]
  ---

  【注意事項】
  - 本文は要約せず原文そのまま
  - 広告ツイートは除く
  ```

**WebSearch mode:**
- Search for: "Twitter Xバズったツイート [user's theme] [year/month]"
- Collect examples from blog posts, まとめサイト

### Step 4: Analyze the samples

For each gathered tweet, extract:

#### A. Hook type
- 問いかけ / 数字提示 / 逆張り / 自己開示 / 断言 / メタファー など

#### B. Structure
- 1文即終わり / 短文改行型 / リスト型 / 物語型 / Before/After型

#### C. Emotional trigger
- 共感 / 驚き / 納得 / 笑い / 憤り / 希望

#### D. Content angle
- 体験ベース / 洞察 / ハック / 予言 / 観察

#### E. Specific language patterns
- 頻出する言い回し、接続詞、文末表現

### Step 5: Synthesize winning patterns

Distill 3-5 clear patterns that are working RIGHT NOW. For each:

```markdown
## 勝ちパターンN: [名前]

**型の説明:** [何をどう書く型か]

**実例:**
> [該当ツイート例]
> → いいね XXX

**なぜ効くか:** [仮説]

**あなたの brand-voice への翻訳:**
[この型をユーザーのトーン・テーマに翻訳した具体案]

**NG化のリスク:** [もしこの型が brand-voice のNG事項に触れそうなら警告]
```

### Step 6: Produce report

```markdown
# トレンド分析レポート — YYYY-MM-DD

## リサーチ対象
- 領域: [テーマ]
- サンプル: [N]件
- 期間: 直近[X]日

## 今効いている5つの勝ちパターン
[パターン1-5の詳細、上記フォーマット]

## あなたのbrand-voiceとの適合度
| パターン | 適合度 | 備考 |
|---------|------|------|
...

## 試したい下書き案（brand-voice翻訳済み）
[勝ちパターンを使った下書き3-5案]

## やらない方がいい型
[あなたのNG事項に触れる型があれば列挙]
```

### Step 7: Offer follow-up

> 分析レポート出しました。次はどうしますか？
>
> A) **勝ちパターンで下書き作る** → x-draftに引き継ぎ（パターン指定あり版）
> B) **brand-voiceに反映** → 使える型を `public-voice.md` の「よく使う型」に追加
> C) **レポート保存** → `personal-info/trend-reports/YYYY-MM-DD.md`
> D) **特定パターンをもっと深掘り** → そのパターンのサンプルを追加調査

## Analysis Principles

- **Don't chase virality blindly**: If a winning pattern clashes with user's brand NG items, flag it. Better to miss virality than break brand.
- **Evidence-based attribution**: Don't claim "this went viral because of X" without basis. Say "この投稿が伸びた要因の仮説は..."
- **Time-sensitivity**: Mark all findings with a date. Twitter trends shift weekly.
- **Translate, don't copy**: Every pattern should be converted to user's voice. Never recommend verbatim copying.
- **Small sample warning**: If <10 samples per pattern, mark as 参考程度.

## Edge Cases

**User's niche is too narrow for bulk search:**
Broaden slightly or search for adjacent topics. Explain: "このテーマだと直接ヒットが少ないので、[隣接テーマ] も含めて見ました"

**Search returns mostly ads/spam:**
Filter them out manually. Explain "広告・プロモ系は除外しました"

**Winning pattern conflicts with brand direction:**
Flag it explicitly:
> この型は伸びてるけど、あなたのbrand-voiceの「[NG事項]」に触れる気がします。採用しない方が良さそうです。

**API rate limits hit:**
Pause, save partial results, tell user when to retry.

## Integration with other components

- **Reads**: `brand-voice.md`, `personal-info/public-voice.md` (テーマ、NG事項), `personal-info/audience-and-messages.md`
- **Can write to**: `personal-info/public-voice.md` (new patterns), `personal-info/trend-reports/` (if saving)
- **Feeds into**: `x-content-strategist` agent (L3インプット), `x-draft` (can reference recent trend report)
