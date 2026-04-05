---
name: x-setup
description: Onboard a user to x-tweetcraft by generating their initial brand-voice.md from their X (Twitter) account and sample tweets. Use when the user asks to "set up x-tweetcraft", "configure x-tweetcraft", "start using x-tweetcraft", "create my brand voice", or when no brand-voice.md exists yet. Adapts to X API availability — uses copy-pasted tweets or Playwright MCP if API not connected.
---

# x-setup

Generate a personalized `brand-voice.md` file that captures the user's X (Twitter) voice, themes, and style. This file becomes the foundation for all draft generation in `x-draft`.

## Workflow

### Step 0: Check companion skills (recommended)

Before starting setup, briefly check whether useful companion skills are available. These aren't required, but they make x-tweetcraft more powerful.

Look at the available skills list in the current session and identify which are NOT present:

**Strongly recommended:**
- `document-skills` (pdf, docx, xlsx, pptx readers) — for reading vision docs, brand guidelines, career sheets when building brand-voice
- `superpowers` (brainstorming, writing-plans, TDD etc.) — for deeper content planning and campaign design

If both are installed, say:
> ✅ おすすめのCompanion Skillsはすでに揃っています。セットアップを始めます。

If some are missing, tell the user:
> x-tweetcraftと相性のいい **おすすめCompanion Skills** を紹介します。必須ではないですが、入れておくと便利です:
>
> **[未インストールのみ列挙]**
> - `document-skills` → PDF/Word/Excel/PowerPointを読み込めるようになります（職歴書・ブランド資料の分析に便利）
> - `superpowers` → ブレスト・計画・TDD等の汎用ワークフロー（コンテンツ戦略に活用できます）
>
> インストール方法:
> ```
> claude plugin install document-skills@anthropic-agent-skills
> claude plugin install superpowers@claude-plugins-official
> ```
>
> または `npx skills add <skill-name>` でも追加できます。
>
> 今すぐ入れなくても x-tweetcraft のセットアップは進められます。このまま続けますか？

Wait for user confirmation, then proceed to Step 1.

### Step 1: Ask for the user's X account

Ask: "あなたのXアカウントを教えてください（URLまたは@ハンドル）"

Wait for the user's response. Accept any of: full URL, @handle, or just the handle.

### Step 2: Check X API availability and explain constraints

Before gathering tweet samples, check whether the X API MCP server is available (look for tools like `mcp__x_auto__get_my_tweets` or similar).

**If X API is NOT available:**

Explain to the user:
> X Developer APIをまだ接続していないため、現時点ではXに直接アクセスできません。以下の方法で進められます：
>
> **A. ツイートを手動コピペ**（確実）
>    最近の投稿から「これは自分らしい」と思うものを5-10件コピペしてください
>
> **B. Claudeブラウザ拡張で抽出**（推奨・早い）
>    Xにログイン済みのブラウザでClaude拡張を使って抽出する。専用プロンプトを提示します
>
> **C. Playwright MCPで公開プロフィールの浅い分析**（MCPが入っていれば）
>    bio・フォロワー数などの公開情報のみ取得。ツイート本文は取れない場合が多い
>
> あとでX APIを申請・接続した後に、`x-refresh-brand-voice` コマンドを使えば、
> 過去の投稿実績を深く分析してbrand-voice.mdをアップデートできます。
>
> どの方法で進めますか？

**If the user chooses Option B (Claude browser extension):**

First, check if they already have the Claude browser extension. Ask:
> Claudeのブラウザ拡張はすでにインストールされていますか？

**If NOT installed**, guide them:
> Claudeブラウザ拡張のインストール手順：
>
> 1. Chromeまたは対応ブラウザで https://claude.ai/download を開く
> 2. 「Browser Extension」セクションから拡張機能をインストール
> 3. Claudeアカウントでログイン
> 4. XのプロフィールページでアイコンをクリックしてClaudeを起動
>
> インストールできたら教えてください。

**Once extension is ready**, present the prompt:

> Xのあなたのプロフィールページを開いた状態で、Claude拡張に以下のプロンプトを貼ってください：
>
> ```
> 【背景】
> 私は自分のXアカウントの投稿を半自動化するツールを構築中で、
> そのために「自分のブランドボイス（文体・トーン・テーマ・型）」を
> 定義するドキュメントを作成しています。
> このページから抽出したツイートは、そのドキュメント作成の元データになります。
>
> 【抽出してほしい情報】
> - 自分のオリジナル投稿のみ（リポスト・引用RP・返信は除く）
> - 最大20件、新しい順
> - 各ツイートの本文 + 反応数（いいね、RP、ブックマーク、インプ）
>
> 【出力フォーマット】
> 各ツイートをMarkdownで以下の形式で：
>
> ---
> ### ツイート1
> **本文:** [ツイート本文を改行・絵文字・ハッシュタグ・URL含めてそのまま]
> **投稿日時:** [表示されている日時]
> **いいね:** [数字] / **RP:** [数字] / **ブックマーク:** [数字] / **インプ:** [数字]
> ---
>
> 【注意事項】
> - 本文は絶対に要約・加工しないでください（文体分析のため原文が必要）
> - 数字が見えないものは「-」と記入
> - スレッドの場合は各ツイートを別々に扱う
> - ツイートの内容自体に対する感想や分析は不要、抽出のみ
>
> 以上です。よろしくお願いします。
> ```
>
> 出力結果をこのチャットに貼っていただければ分析します。

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

### Step 5: Generate brand-voice structure

Create a **2-layer structure** based on the analysis:

**File structure to generate:**
```
brand-voice.md                           # Index + quick summary
personal-info/
├── public-voice.md                      # Public: tone, themes, patterns, NG items
├── values-and-origin.md                 # Private: values, story, career
├── audience-and-messages.md             # Private: target, core messages
└── interview-logs/                      # For x-interview sessions
```

**brand-voice.md** is the index containing:
- Quick summary (name, tone, themes)
- References to personal-info/ files
- Command guide (x-draft, x-interview etc.)

**personal-info/public-voice.md** (from template at `${CLAUDE_PLUGIN_ROOT}/data/brand-voice-template.md`):
- Persona, tone, themes, patterns, NG items
- Filled with user's actual content from analysis

**personal-info/values-and-origin.md** (initial stub):
- Empty scaffolding for x-interview to fill later
- Note: "Run `x-interview` to deepen this section"

**personal-info/audience-and-messages.md** (initial stub):
- Basic target audience from tweet analysis
- Note: "Run `x-interview` to deepen this section"

**Storage location:**
- Default: Save to the current working directory
- For VITAL Z users: `ceo/x-automation/`
- Ask the user: "brand-voice の保存先はどこにしますか？（デフォルト: `./`）"

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

### Step 8: Offer chaining to x-interview

Tell the user:
> brand-voice 構造を保存しました。基本セットアップ完了です。
>
> ただ、ツイートだけから作ったbrand-voiceはどうしても表層的になりがちです。
> あなたの**原体験・価値観・転機**を入れると、あなたにしか書けない投稿を生成できるようになります。
>
> **今すぐ `x-interview` で1 Round（5分程度）だけやってみませんか？**
> 全部で6 Roundありますが、今日は1つだけでもOK。続きは後日でも大丈夫です。
>
> A) はい、Round 1 だけやる（推奨）
> B) 今日はここまで、後でやる
> C) 最後まで一気にやる（20-30分）

**If user chooses A or C:** Immediately transition to the `x-interview` skill workflow. Skip x-interview Step 1 (prior session check — none exists yet) and start from Step 2 (explain purpose) through Step 9 as if it were the current skill.

**If user chooses B:** Tell the user:
> OK、いつでも「x-interviewで深めたい」と声をかけてください。

### Step 9: Final guidance (if x-interview was done or skipped)

Tell the user:
> 次のステップ:
> - **今すぐ使う**: 「今日のツイート作って」で `x-draft` 起動 → 下書き5-10案生成
> - **brand-voiceを育てる**: 「x-interviewで深めたい」（いつでも）
> - **分析・自動化まで本気でやりたい**: 「x-connect-apiして」で X Developer API接続（Basic $200/月が必要。詳細は接続スキルで案内）
> - **自動化セットアップ**: 「朝までに下書き作っておいて」で x-schedule が走る
>
> 💡 **API接続について:** 下書き生成だけなら不要。投稿分析・トレンド分析・自動化が欲しい時に検討してください。

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
