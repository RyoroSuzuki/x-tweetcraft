---
name: x-draft
description: Generate 5-10 personalized tweet drafts for X (Twitter) based on the user's brand-voice.md. Use when the user says "今日のツイート作って", "ツイート下書いて", "draft a tweet", "ツイートのネタ出して", or similar. Integrates brand voice, past post analysis (via X API when available), and market trends (when API connected) to form hypotheses and produce drafts with rationale. Progressively enhances output as X API features become available.
---

# x-draft

Generate multiple personalized tweet drafts grounded in the user's brand voice, with hypotheses about what will resonate. Each draft comes with rationale so the user can pick wisely.

## Workflow

### Step 1: Locate and load brand-voice structure

Search for `brand-voice.md` in the following locations (in order):
1. Current working directory root: `./brand-voice.md`
2. VITAL Z convention: `./ceo/x-automation/brand-voice.md`
3. User's home: `~/brand-voice.md`

**If not found:** Tell the user "brand-voice.md が見つかりません。`x-setup` を実行して作成しましょうか？" and stop.

Read `brand-voice.md` (the index file). It contains the quick summary and references to:
- `personal-info/public-voice.md` — 公的トーン・スタイル・テーマ・型・NG事項
- `personal-info/values-and-origin.md` — 価値観・原体験・キャリア（Private）
- `personal-info/audience-and-messages.md` — 届けたい人・コアメッセージ（Private）

**Also check for `personal-info/learnings.md`** — if it exists, read it to incorporate prior x-reflect sessions' learnings:
- 強い好みパターン → 優先的に生成に反映
- 強い拒否パターン → 避ける
- 修正癖 → 生成時に初めから反映

**Read ALL referenced files** (not just brand-voice.md index). The public files guide output style; the private files inform voice, perspective, and motivation — but their content MUST NOT be directly quoted in tweets.

Internalize:
- Public: tone, themes, patterns, NG items, 3-step structure
- Private: values, origin story, target audience, core messages (as internal context only)
- Learnings: accumulated user preferences from prior sessions (strong signal)

### Step 2: Check X API availability

Look for MCP tools from the x-tweetcraft MCP server: `mcp__x_tweetcraft__get_my_tweets`, `mcp__x_tweetcraft__search_trending`, etc.

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

Generate drafts personalized to the user's voice. For each draft:
- Match the tone and style from brand-voice.md
- Use one of the user's "よく使う型" (patterns)
- Avoid all NG items
- Stay within 280 characters (X limit) — **Japanese characters count as 2 each on X, so keep Japanese tweets within ~140 Japanese characters to be safe**

**Output format for each draft:**

```
### Draft N
[Tweet text]

**根拠:** [Why this draft — which theme, which pattern, connection to hypothesis]
**型:** [Pattern used, e.g., 失敗談→学び]
**推奨時間帯:** [Time, only if API data supports it]
```

### Step 7: Save draft log

**Always save the generated drafts to a log file**, regardless of whether the user picks anything. This preserves history and feeds future analysis/learning.

Save to (same path priority as brand-voice.md):
1. `ceo/x-automation/personal-info/draft-logs/YYYY-MM-DD_HHMM.md` (VITAL Z convention)
2. `./personal-info/draft-logs/YYYY-MM-DD_HHMM.md` (other users)
3. `./draft-logs/YYYY-MM-DD_HHMM.md` (fallback)

Create the directory if it doesn't exist.

File format:
```markdown
# Draft Log - YYYY-MM-DD HH:MM

## Context
- brand-voice version: [hash or updated date]
- learnings.md: [exists / not exists]
- API status: [connected/disconnected], layers used: [L1/L2/L3]
- Topic requested: [user-specified topic or "自動"]

## Hypothesis
[The hypothesis used]

## Drafts
[All N drafts with their rationale]

## User response
[To be filled by x-reflect if user provides feedback]
- Picked: (will be updated)
- Rejected: (will be updated)
- Edits: (will be updated)
```

The "User response" section is initially empty. x-reflect fills it in when the user gives feedback.

### Step 8: Add summary and feedback

At the top of the output, show:
- The hypothesis used
- Which data sources were available (brand-voice.md + personal-info/ / Layer 2 / Layer 3)
- Tell the user: "下書きは `personal-info/draft-logs/` に保存しました"

At the bottom, if API not connected, add:
> **💡 X APIを接続するとこう改善されます:**
> - 過去投稿の実績データから「実際に伸びた型」を分析
> - 今のトレンドから「勝ちパターン」を取り込み
> - より具体的な「○時台が伸びやすい」推奨時間
> - `post_tweet` ツールで下書きを直接投稿可能
> - API接続は `x-connect-api` スキルで設定できます

### Step 9: Invite iteration and deepening

End with:
> 気に入った案はありますか？修正したい部分があれば「3番をもっとカジュアルに」のように指示してください。投稿するなら `x-post` スキル（計画中・API接続後に実装予定）が使えます。
>
> 💡 **選んだ後にフィードバック教えてもらえると、次回もっとあなたらしく書けるようになります。**
> （例: 「3番を採用。ただし○○の部分を△△に変えた」「7番は好き、ただ文末を柔らかくしたい」）
> これをもとに `x-reflect` が自動でlearningsに記録して、分身が賢くなります。
>
> 💎 **精度をさらに上げたい時:**
> - 「x-interviewで深めたい」 → brand-voiceをもっとパーソナライズ
> - 「自分の投稿分析して」 → `x-analyze-posts` で深い傾向分析（API接続後）
> - 「今伸びてるツイート調べて」 → `x-research-trends` で市場研究（API推奨）
> - 「今週の戦略立てて」 → `x-content-strategist` agent で週次戦略レビュー

### Step 10: Trigger x-reflect on user response

After presenting drafts, when the user responds with their picks/edits/rejections:
- Invoke the `x-reflect` skill workflow to capture the learnings
- If the user said "スキップ" or gave no feedback, skip x-reflect invocation

## Quality Checklist

Self-check before presenting drafts:

- [ ] Confirm each draft is under 280 characters
- [ ] Confirm all drafts match the user's tone from brand-voice.md
- [ ] Confirm no NG items appear
- [ ] Confirm at least 3 different patterns appear across 10 drafts (not all the same type)
- [ ] Confirm rationale is concrete, not generic
- [ ] Confirm drafts feel distinct from each other (not the same idea in different wording)

## Heuristics

**Variety:** Mix short (100 chars) and longer (250 chars) drafts. Mix patterns (失敗談→学び, 逆張り, 質問→答え, 数字→気づき).

**Specificity beats generics:** "売上が3ヶ月で2倍" is better than "売上が伸びた". Draw concrete details from brand-voice.md examples if possible.

**Avoid AI giveaways:**
- Don't use corporate buzzwords ("〜の重要性", "〜することで")
- Don't use generic phrases that the user never uses
- Don't force emojis if the user doesn't use them
- Match the user's Japanese/English mix proportion

**Hypothesis discipline:** If no data supports a hypothesis element, don't invent it. Say "これはbrand-voice.mdからの推定です".
