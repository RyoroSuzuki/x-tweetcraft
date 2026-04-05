---
name: x-connect-api
description: Guide the user through X (Twitter) Developer API application, authentication, and connection. Use when the user says "x-connect-apiして", "X API接続したい", "Developer API申請したい", "API繋ぎたい", "x-post使いたい", or when skills report that X API is not available and the user wants to enable it. Walks through portal application, app creation, credential retrieval, .env setup, and connection test. Enables x-post, x-refresh-brand-voice, and API-enhanced x-draft.
---

# x-connect-api

Walk the user through connecting X Developer API to x-tweetcraft, from application to working connection. This unlocks x-post (auto-posting), x-refresh-brand-voice (deep analytics), and API-enhanced x-draft.

## Workflow

### Step 1: Check current state

Ask the user where they are:
> X Developer APIの接続を始めます。現在の状況を教えてください:
>
> A) まだ何もしていない（Developer Portalアカウント未作成）
> B) Developer Portalは登録済み、App未作成
> C) App作成済み、認証情報（API Keys / Tokens）取得済み
> D) 認証情報を .env に設定済み、接続テストをしたい

### Step 2: Handle each starting point

#### A) まだ何もしていない

Guide through the application:

> **X Developer Portal 申請手順:**
>
> 1. https://developer.x.com/ にアクセス
> 2. Xアカウントでログイン（自動投稿したいアカウントでログイン）
> 3. 「Sign up for Free Account」をクリック（Freeプランで十分）
> 4. 用途説明欄に以下のテキストをコピペしてください:

Provide the application text. **Customize based on the user's actual use case** — pull relevant info from brand-voice.md / personal-info/.

Example text template:
```
I am building a personal productivity tool to semi-automate my own X posting workflow.

The tool analyzes my own past tweets to identify writing patterns and themes that resonate with my audience, then helps me generate draft posts based on my brand voice. I review and edit each draft before posting.

Specifically, I will use the API to:
1. Post my own tweets to my own account
2. Retrieve my own past tweets to analyze my writing patterns
3. Understand which topics perform well with my existing audience

This is purely a personal productivity tool — I only access my own account data. No third-party data collection, no automated mass posting. Each post is human-reviewed before publishing.

The tool is a Claude Code (Anthropic's CLI) plugin for personal use.
```

**If the user has a specific pre-drafted application text** (e.g., `ceo/x-tweetcraftmation/X_API_APPLICATION.md`), read it and present that instead.

Then tell them:
> 申請後は承認待ちです（通常1-2営業日、即時承認もあり）。
> 承認されたら「次のステップに進みたい」と声をかけてください。

Wait for user to proceed.

#### B) Developer Portal登録済み、App未作成

Guide through App creation:

> **App作成手順:**
>
> 1. Developer Portal（https://developer.x.com/en/portal/dashboard）にログイン
> 2. 「Create Project」または「Create App」をクリック
> 3. App名を入力（例: `x-tweetcraft-yourname`）
> 4. 「Keys and tokens」タブで以下を取得:
>    - API Key
>    - API Key Secret
>    - Bearer Token
>    - Access Token
>    - Access Token Secret
> 5. **User authentication settings** で以下を設定:
>    - App permissions: **Read and write**（投稿に必要）
>    - Type of App: **Web App, Automated App or Bot**
>    - Callback URI: `http://localhost:3000/callback` (ダミーでOK)
>    - Website URL: 何でもOK（`https://example.com`）
>
> 取得したら次のステップへ進みましょう。

Wait for user to confirm they have the credentials.

#### C) 認証情報取得済み

Guide through .env setup:

> **認証情報の保存:**
>
> 1. 以下の場所に `.env` ファイルを作成してください:
>    `~/.x-tweetcraft.env`
>
>    （プラグインディレクトリではなくホームに置く。git管理から外すため）
>
> 2. 以下の内容を記入:
>
> ```
> X_BEARER_TOKEN=ここにBearer Tokenを貼る
> X_API_KEY=ここにAPI Keyを貼る
> X_API_SECRET=ここにAPI Key Secretを貼る
> X_ACCESS_TOKEN=ここにAccess Tokenを貼る
> X_ACCESS_TOKEN_SECRET=ここにAccess Token Secretを貼る
> ```
>
> 3. パーミッションを制限:
>    `chmod 600 ~/.x-tweetcraft.env`
>
> ⚠️ **絶対にGitにコミットしない**でください。

Wait for user to confirm.

#### D) 接続テストをしたい

Guide through connection test:

Check if the x-tweetcraft MCP server is configured. Look for `.mcp.json` in the plugin.

If MCP server not yet configured:
> x-tweetcraft MCPサーバーがまだセットアップされていません。
> この機能はP1タスクとして別途実装が必要です。
> 現時点では、APIキーを保存しておいて、MCPサーバー実装後にテストできます。

If MCP server is configured:
> MCPサーバーの再起動が必要です。
> Claude Codeを再起動してから、以下を実行してください:
>
> ```
> 「x-connect-apiの接続テストして」
> ```
>
> → 自分のアカウント情報取得テストが走ります。

### Step 3: Confirm completion and next steps

Once the user confirms setup is complete:

> 🎉 X API接続完了です！これで以下が使えるようになります:
>
> - `x-post` — 下書きを直接投稿
> - `x-refresh-brand-voice` — 過去投稿100件以上を分析してbrand-voice深化
> - `x-draft` — API連携データ込みでより精度の高い下書き生成
>
> まず試してみるなら:
> - 「x-refresh-brand-voice」でbrand-voice.mdを深い分析で更新
> - 「今日のツイート作って」で改善版の下書きを生成

## Security Notes

Always remind the user:
- **Never commit .env to git**
- **Never share API keys in chat or code**
- **Store credentials in password manager as backup**
- **Rotate tokens if exposed**

## Edge Cases

**User's application was denied:**
- Ask for the rejection reason
- Help rewrite the use case description to address concerns
- X typically wants: clear personal use, human oversight, no spam/bot behavior

**User is confused about Project vs App:**
- Explain: A Project contains Apps. Just create a Project first, then it auto-creates an App.

**User has multiple X accounts:**
- Ensure they're logged into the account they want to automate posting FOR
- The Developer API is tied to the account that creates the App

**User wants Basic/Pro plan:**
- Free plan is enough for MVP (1,500 posts/month, 10K tweet reads/month)
- Basic ($200/month) needed for: tweet search (search_trending), high-volume reads
- Help them assess: do they actually need Basic?

**API approved but user can't find keys:**
- Guide to: Developer Portal → Projects & Apps → [App name] → Keys and tokens tab
- May need to "Regenerate" if they were shown once and not saved

## Integration with existing assets

**If `ceo/x-tweetcraftmation/X_API_APPLICATION.md` exists** (VITAL Z convention):
- Read it and use the pre-drafted application text
- Mention that this saves time

**After successful connection:**
- Suggest running `x-refresh-brand-voice` immediately to see the quality improvement
- Update the user's `brand-voice.md` 更新履歴 section with "API connected: YYYY-MM-DD"
