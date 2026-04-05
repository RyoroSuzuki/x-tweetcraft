---
name: x-analyze-posts
description: Deeply analyze the user's past X posts to surface engagement patterns, winning topics, voice evolution, and actionable insights. Use when the user says "自分の投稿分析して", "過去の投稿傾向を見たい", "どのツイートが伸びた？", "analyze my X posts", "performance review", or wants standalone deep analysis beyond what x-draft does inline. Requires X API connection (via x-tweetcraft MCP server). Falls back to manual tweet paste mode if API not connected.
---

# x-analyze-posts

Conduct deep, standalone analysis of the user's X posts. This is the L2 (分析・学習) skill in x-tweetcraft's 3-layer architecture. Unlike `x-draft` which does light-touch analysis inline, this skill produces a thorough report and actionable insights.

## Workflow

### Step 1: Check X API availability

Look for MCP tools from the x-tweetcraft MCP server: `mcp__x_tweetcraft__get_my_tweets`, `mcp__x_tweetcraft__get_tweet_metrics`.

**If available:** Proceed to Step 2 (API mode).

**If NOT available:** Tell the user:
> X Developer APIが接続されていないため、直接分析できません。以下から選んでください:
>
> A) **コピペ分析モード** — 直近20-50件のツイートをコピペ（Claudeブラウザ拡張を使うと早い）
> B) **APIを接続してから再実行** — `x-connect-api` でセットアップ
>
> どちらにしますか？

If user chooses A, guide them through paste mode (similar to x-setup's Claude browser extension flow). If B, invoke x-connect-api.

### Step 2: Determine analysis scope

Ask the user:
> 分析したい範囲を教えてください:
>
> A) **最近30件** — 短期の傾向・直近の当たり外れ
> B) **最近100件** — 中期トレンド・型の発見
> C) **全期間** — 長期進化・テーマの変遷
>
> また、特に気になることはありますか？（例: 「最近伸びない」「特定のテーマの反応」など）

### Step 3: Gather posts

**API mode:**
- Call `mcp__x_tweetcraft__get_my_tweets` with the determined count
- For each tweet, fetch metrics via `mcp__x_tweetcraft__get_tweet_metrics` if available
- Data collected per tweet: text, posted_at, likes, retweets, bookmarks, impressions, reply_count

**Paste mode:**
- Accept user-pasted data (similar to x-setup flow)
- Ask for metrics if not included

### Step 4: Analyze systematically

Perform analysis across these dimensions. **Do not invent numbers** — if data is missing, say so explicitly.

#### A. Engagement distribution
- Calculate: avg likes, avg RTs, avg impressions, engagement rate (interactions / impressions)
- Identify: top 10% performers, bottom 30% underperformers
- Note: median vs average (to catch outliers)

#### B. Topic analysis
- Cluster tweets by topic (leverage brand-voice.md テーマ section)
- Measure: engagement per topic
- Identify: which themes resonate most with this user's audience

#### C. Format/Pattern analysis
- Cross-reference with `personal-info/public-voice.md` のよく使う型
- Categorize each tweet by pattern (数字→気づき / 問いかけ / 葛藤吐露 / 自嘲オチ etc.)
- Measure: engagement per pattern
- Identify: winning patterns, patterns to try more

#### D. Temporal analysis
- Time-of-day: which hours get most engagement
- Day-of-week: weekend vs weekday
- Note: sample size per bucket (don't over-interpret small samples)

#### E. Length analysis
- Short (<100 chars) vs medium (100-200) vs long (200-280)
- Correlation with engagement

#### F. Voice evolution (if長期分析の場合)
- Has tone shifted over time?
- Has theme focus narrowed/broadened?
- Has engagement trend improved/declined?

### Step 5: Produce the report

Output format:

```markdown
# 投稿分析レポート — YYYY-MM-DD

## サンプル
- 分析対象: [N]件のツイート
- 期間: YYYY-MM-DD 〜 YYYY-MM-DD

## エンゲージメント全体像
- 平均: ○いいね / ○RT / ○インプ / エンゲージ率 ○%
- 上位10%の特徴: [何が違うか3点]
- 下位30%の共通点: [何が効かなかったか3点]

## 🏆 伸びた投稿 トップ5
1. [ツイート全文]
   - 指標: [数字]
   - なぜ伸びた: [仮説]
   - パターン: [型]

## 📉 伸びなかった投稿の傾向
- [共通要素]

## テーマ別の手応え
| テーマ | サンプル数 | 平均インプ | 平均エンゲ率 |
|--------|---------|---------|-----------|
...

## 型別の勝ちパターン
| 型 | サンプル数 | 平均エンゲ率 |
|----|---------|-----------|
...

## 時間帯・曜日傾向
- [気づき]

## 🎯 次のアクション提案
1. [強化すべきこと]
2. [やめるべきこと]
3. [試したいこと]

## brand-voiceへの反映提案
以下を `personal-info/public-voice.md` に追加するとよさそう:
- [具体的な追記提案]
```

### Step 6: Offer follow-up

> レポート出しました。以下どうしますか？
>
> A) brand-voiceに反映する（提案を public-voice.md に追記）
> B) 伸びた投稿の型でもっと下書き作る（x-draftに引き継ぎ）
> C) この分析をファイル保存する（`personal-info/analysis-YYYY-MM-DD.md`）
> D) もう少し掘り下げたい点を指定

## Analysis Principles

- **Evidence-based**: Only claim what the data shows. Use "このサンプルでは" prefix for tentative claims.
- **Small samples warning**: If a bucket has <5 samples, explicitly flag it as "参考値"
- **Avoid generic advice**: Don't say things like "エンゲージメントを上げるには..." — say what THIS user specifically should try
- **Connect to brand-voice**: Every insight should relate back to the user's established voice
- **Don't interpret private signals as public**: If the user has a private rant tweet that got high engagement, don't recommend "be more controversial" — consider the brand fit

## Edge Cases

**User has very few posts (<20):**
Tell them: "サンプル数が少ないので統計的な傾向は取りにくいです。質的な観察ベースでコメントします。"

**Engagement is universally low:**
Focus on relative comparison (top vs bottom) rather than absolute numbers. Check if discovery/timing is the issue vs content.

**User's best posts conflict with brand direction:**
Note the tension: "これは伸びたけど brand-voice の方向とはズレる気がする。どう扱いますか？"
Don't automatically recommend doubling down on off-brand virality.

**API rate limits hit mid-analysis:**
Save partial results, tell the user to retry later for full dataset.

## Integration with other components

- **Reads**: `brand-voice.md`, `personal-info/public-voice.md` (for pattern/theme references)
- **Can write to**: `personal-info/public-voice.md` (if user approves suggestions), `personal-info/analysis-logs/` (if saving reports)
- **Feeds into**: `x-content-strategist` agent (agent aggregates this analysis + x-research-trends)
