---
name: x-draft
description: Generate 5-10 personalized tweet drafts for X (Twitter) based on the user's brand-voice.md. Use when the user says "今日のツイート作って", "ツイート下書いて", "draft a tweet", "ツイートのネタ出して", or similar. Integrates brand voice, past post analysis (via X API when available), and market trends (when API connected) to form hypotheses and produce drafts with rationale. Progressively enhances output as X API features become available.
---

# x-draft

Generate multiple personalized tweet drafts grounded in the user's brand voice, with hypotheses about what will resonate. Each draft comes with rationale so the user can pick wisely.

## Workflow

### Step 1: Locate and load brand-voice.md

Search for `brand-voice.md` in the following locations (in order):
1. Current working directory root: `./brand-voice.md`
2. VITAL Z convention: `./ceo/x-automation/brand-voice.md`
3. User's home: `~/brand-voice.md`

**If not found:** Tell the user "brand-voice.md が見つかりません。`x-setup` を実行して作成しましょうか？" and stop.

Read the file and internalize the persona, tone, themes, patterns, and NG items.

### Step 2: Check X API availability

Look for MCP tools from the x-auto MCP server: `mcp__x_auto__get_my_tweets`, `mcp__x_auto__search_trending`, etc.

Track which are available:
- `get_my_tweets` → Layer 2 (own post analysis)
- `get_tweet_metrics` → Layer 2 (engagement data)
- `search_trending` → Layer 3 (market trends)

### Step 3: Gather enhancement data (if API available)

**Layer 2 — Own post analysis:**
If `get_my_tweets` is available, fetch the most recent 30-50 tweets. Identify:
- Which posts got the most engagement
- Common characteristics of high-performing posts (topic, hook, length, time of day)
- Themes that resonated vs. fell flat

**Layer 3 — Market trends:**
If `search_trending` is available, search for trending tweets in the user's theme areas. Identify:
- Current hot angles and formats
- Patterns worth adapting to the user's voice

**Fallback (no API):**
Skip these steps. Note in the output that API connection would improve results.

### Step 4: Form a hypothesis

Combine brand-voice.md + gathered data into a hypothesis of the form:

> "○○（訴求）× ○○（型）× ○○（時間帯） が伸びそう"

Example: "起業の失敗談 × 数字→学びの型 × 朝7時 が伸びそう"

Base the hypothesis on:
- Brand voice themes and patterns
- What's working (from Layer 2) if available
- What's trending (from Layer 3) if available
- If no API data, state the hypothesis is based on brand-voice.md alone

### Step 5: Ask user for direction (optional)

If the user didn't specify a topic, ask:
> 今日のトピックや方向性は何か決まっていますか？（任意。指定なければ仮説から自動で生成します）

Otherwise proceed with the hypothesis.

### Step 6: Generate 5-10 drafts

Generate drafts personalized to the user's voice. Each draft should:
- Match the tone and style from brand-voice.md
- Use one of the user's "よく使う型" (patterns)
- Avoid all NG items
- Be within 280 characters (X limit)

**Output format for each draft:**

```
### Draft N
[Tweet text]

**根拠:** [Why this draft — which theme, which pattern, connection to hypothesis]
**型:** [Pattern used, e.g., 失敗談→学び]
**推奨時間帯:** [Time, only if API data supports it]
```

### Step 7: Add summary and feedback

At the top of the output, show:
- The hypothesis used
- Which data sources were available (brand-voice.md / Layer 2 / Layer 3)

At the bottom, if API not connected, add:
> **💡 X APIを接続するとこう改善されます:**
> - 過去投稿の実績データから「実際に伸びた型」を分析
> - 今のトレンドから「勝ちパターン」を取り込み
> - より具体的な「○時台が伸びやすい」推奨時間
> - `post_tweet` ツールで下書きを直接投稿可能

### Step 8: Invite iteration

End with:
> 気に入った案はありますか？修正したい部分があれば「3番をもっとカジュアルに」のように指示してください。投稿するなら `x-post` スキルが使えます。

## Quality Checklist

Before presenting drafts, self-check:

- [ ] Each draft is under 280 characters
- [ ] All drafts match the user's tone from brand-voice.md
- [ ] No NG items appear
- [ ] At least 2 different patterns are used across drafts (not all the same type)
- [ ] Rationale is concrete, not generic
- [ ] Drafts feel distinct from each other (don't all say the same thing in slightly different words)

## Heuristics

**Variety:** Mix short (100 chars) and longer (250 chars) drafts. Mix patterns (失敗談→学び, 逆張り, 質問→答え, 数字→気づき).

**Specificity beats generics:** "売上が3ヶ月で2倍" is better than "売上が伸びた". Draw concrete details from brand-voice.md examples if possible.

**Avoid AI giveaways:**
- Don't use corporate buzzwords ("〜の重要性", "〜することで")
- Don't use generic phrases that the user never uses
- Don't force emojis if the user doesn't use them
- Match the user's Japanese/English mix proportion

**Hypothesis discipline:** If no data supports a hypothesis element, don't invent it. Say "これはbrand-voice.mdからの推定です".
