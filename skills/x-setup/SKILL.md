---
name: x-setup
description: Onboard a user to x-auto by generating their initial brand-voice.md from their X (Twitter) account and sample tweets. Use when the user asks to "set up x-auto", "configure x-auto", "start using x-auto", "create my brand voice", or when no brand-voice.md exists yet. Adapts to X API availability — uses copy-pasted tweets or Playwright MCP if API not connected.
---

# x-setup

Generate a personalized `brand-voice.md` file that captures the user's X (Twitter) voice, themes, and style. This file becomes the foundation for all draft generation in `x-draft`.

## Workflow

### Step 1: Ask for the user's X account

Ask: "あなたのXアカウントを教えてください（URLまたは@ハンドル）"

Wait for the user's response. Accept any of: full URL, @handle, or just the handle.

### Step 2: Check X API availability and explain constraints

Before gathering tweet samples, check whether the X API MCP server is available (look for tools like `mcp__x_auto__get_my_tweets` or similar).

**If X API is NOT available:**

Explain to the user:
> X Developer APIをまだ接続していないため、現時点ではXに直接アクセスできません。以下の2つの方法で進められます：
>
> **A. ツイートをコピペしていただく**（推奨・確実）
>    最近の投稿から「これは自分らしい」と思うものを5-10件コピペしてください
>
> **B. Playwright MCPで公開プロフィールの浅い分析**
>    bio・フォロワー数などの公開情報のみ取得できますが、ツイート本文は取れません
>
> あとでX APIを申請・接続した後に、`x-refresh-brand-voice` コマンドを使えば、
> 過去の投稿実績を深く分析してbrand-voice.mdをアップデートできます。
>
> どちらの方法で進めますか？

**If X API IS available:**

Use the MCP tools directly:
- `get_my_tweets` to fetch recent 20-50 tweets
- Analyze engagement metrics if available

### Step 3: Gather tweet samples

Based on the user's choice, gather their tweet samples.

**For Option A (copy-paste):**
Ask: "最近の投稿で、あなたらしいと感じる・お気に入りのツイートを5-10件、このチャットにコピペしてください。1件ずつでも、まとめてでもOKです。"

Wait for the user to paste tweets. Accept them and move on when they say they're done or have pasted 5+ tweets.

**For Option B (Playwright MCP):**
Use Playwright MCP to fetch the public X profile page. Extract bio, follower count, following count, and any visible recent tweets. Note: Playwright may get blocked by X's login wall — if it fails, fall back to Option A.

**For X API available:**
Call `get_my_tweets` to retrieve recent tweets programmatically.

### Step 3.5: Ask for additional context materials

Before analyzing, ask the user if they have any other materials about their X operation direction:

> ツイート以外に、X運用の方向性・戦略をまとめたメモや資料はありますか？
> 例えば：
> - 発信テーマのメモ
> - ターゲット読者の定義
> - 投稿カレンダー・企画書
> - ブランディング資料
> - ペルソナ設定資料
>
> ファイルパスを教えていただくか、内容をコピペしていただければ、brand-voice.mdに反映します。
> （なければスキップでOK）

If the user provides file paths, read them. If they paste content, use it. If they skip, proceed with tweets only.

These materials often contain intentional direction that may not be visible in past tweets — the user's "こう発信したい" vs. past "こう発信した". Prioritize intentional direction when conflicts exist.

### Step 4: Analyze the samples

From the gathered tweets, extract:

1. **Persona clues**: What does the user present themselves as? (occupation, role, identity)
2. **Tone and style**: Casual/formal, length, humor, emotion
3. **Recurring themes**: What topics come up most often? (aim for 2-4 themes)
4. **Patterns/formulas**: What structures do they repeat? (e.g., story→lesson, question→answer, contrarian opinion + reasons)
5. **NG items** (things they avoid): What tones/topics seem to be missing? (e.g., no provocative posts, no personal attacks)

Keep analysis concise. Do not over-analyze or invent characteristics not visible in the samples.

### Step 5: Generate brand-voice.md draft

Create a draft based on the template at `${CLAUDE_PLUGIN_ROOT}/data/brand-voice-template.md` but filled in with the user's actual content from analysis.

**Storage location:**
- Default: Save to the current working directory as `brand-voice.md`
- If the user specifies a different path, use that
- For VITAL Z users, the convention is `ceo/x-automation/brand-voice.md`

Ask the user before writing: "brand-voice.md の保存先はどこにしますか？（デフォルト: `./brand-voice.md`）"

### Step 6: Present draft for user review

Show the generated draft to the user and ask:
> この内容であなたらしさを表せてますか？修正したい部分があれば教えてください。

Iterate based on feedback. Common adjustments:
- Tone descriptions too formal/casual
- Missing themes
- Wrong interpretation of style
- Add specific NG items

### Step 7: Save the final version

Write the confirmed version to the chosen path. Confirm with the user that it was saved.

### Step 8: Guide the user to next steps

Tell the user:
> brand-voice.md を保存しました。これで準備完了です。
>
> 次のステップ:
> - 「今日のツイート作って」と言うと `x-draft` スキルが起動して下書きを5-10案生成します
> - X Developer APIを申請・接続すると、過去投稿の自動分析・トレンド分析・自動投稿ができるようになります
> - API接続後は `x-refresh-brand-voice` でより深い分析に更新できます

## Analysis Heuristics

When analyzing tweets, use these heuristics to avoid shallow or generic brand voices.

**Tone detection signals:**
- Sentence-end particles (「だ」「です」「よね」「ね」) → formality level
- Use of exclamation marks, emojis → emotional expression
- Hedge words (「たぶん」「思う」) vs. assertions → confidence style

**Theme extraction:**
- Look for repeating nouns/topics across tweets
- Group semantically (e.g., "起業" "経営" "資金調達" → 起業・経営テーマ)
- If fewer than 2 clear themes emerge, ask the user what they *want* to post about

**Pattern recognition:**
- Does the user start with a hook? Question? Claim?
- Single-line vs. multi-line tweets?
- Numbers, specifics, anecdotes?

Be honest about limitations: if only 5 tweets are provided, explicitly say "これはサンプル5件からの推定です。もっと書いていくうちに調整が必要です。"

## Edge Cases

**User provides fewer than 5 tweets:**
Proceed but warn them: "サンプルが少ないので推定精度は低めです。運用しながら調整しましょう"

**User's tweets are all about one topic:**
That's fine — a focused brand is strong. Don't artificially add themes.

**User doesn't have an X account yet:**
Ask what they *want* to post about and build the brand voice aspirationally. Mark in the file that this is aspirational, not descriptive.

**Tweets are in multiple languages:**
Default the brand-voice.md language to the user's dominant tweet language. Note mixed language use if relevant.
