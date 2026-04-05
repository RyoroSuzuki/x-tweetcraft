# X Developer API 接続 完全ガイド（非エンジニア向け）

**所要時間:** 30分〜1時間
**難易度:** ★★☆☆☆（画面の手順通りにやれば完了）
**前提:** X（Twitter）アカウントを持っている、パソコンが使える

---

## 事前に決めること

### どのアカウントで申請する？

発信したいメインアカウントで申請してください。**申請したアカウントからしか投稿できません。**

### 電話番号認証

X Developer Portal の申請には電話番号認証が必要です。まだXアカウントに電話番号を登録していない場合は、先にX本体で電話番号を登録してください。

---

## ステップ1: Developer Portalに入る

### 1-1. ブラウザでアクセス

以下のURLを開いてください:
https://developer.x.com/

### 1-2. サインイン

右上の「Sign in」をクリック。発信用のXアカウントでログインします。

### 1-3. Developer Portalダッシュボードへ

ログイン後、「Developer Portal」または「Dashboard」ボタンをクリック。

---

## ステップ2: Free プランに申請

### 2-1. Free Accountを選ぶ

ダッシュボードで「Sign up for Free Account」または「Apply for Free」をクリック。

### 2-2. 利用目的の記入

**英語のみ受付です。** 以下のテンプレートをコピペしてください（250文字以上必要）：

```
I am building a personal productivity tool to semi-automate my own X posting workflow.

The tool analyzes my own past tweets to identify writing patterns and themes that resonate with my audience, then helps me generate draft posts based on my brand voice. I review and edit each draft before posting.

Specifically, I will use the API to:
1. Post my own tweets to my own account
2. Retrieve my own past tweets to analyze my writing patterns
3. Understand which topics perform well with my existing audience

This is purely a personal productivity tool — I only access my own account data. No third-party data collection, no automated mass posting. Each post is human-reviewed before publishing.

The tool is a Claude Code plugin for personal use.
```

### 2-3. 承認待ち

送信ボタンを押して完了。通常は数分〜数時間で承認されます（即時承認もあり）。
承認されるとメールが届きます。

**却下されたら:** 上記文面を少し編集（「individual use」「not for commercial data collection」等を強調）して再申請。

---

## ステップ3: プロジェクトとアプリを作る

### 3-1. プロジェクト作成

Developer Portalで「Projects & Apps」→「Create Project」をクリック。

- **Project name:** `x-tweetcraft-personal` など分かりやすい名前
- **Use case:** 「Personal use」または「Making a bot」
- **Project description:** 英語で1文（例: "Personal tweet drafting tool"）

### 3-2. アプリ作成

プロジェクト作成後、自動的にアプリ作成画面に進みます。
- **App name:** `x-tweetcraft-yourname` など（グローバルにユニークな名前が必要）

### 3-3. User Authentication Settings（重要）

アプリ作成後、「User authentication settings」の「Set up」をクリック。以下のように設定:

| 項目 | 設定 |
|------|------|
| **App permissions** | **Read and write**（これが投稿に必須！） |
| **Type of App** | Web App, Automated App or Bot |
| **Callback URI / Redirect URL** | `http://localhost:3000/callback`（ダミーでOK） |
| **Website URL** | `https://example.com`（何でもOK） |

「Save」をクリック。

### 3-4. ⚠️ 重要: App permissionsを変更したら Access Token を再生成する

もし**最初に「Read only」で作成してから「Read and write」に変更した場合**、既存のAccess Tokenは古い権限のまま。
→ 次のステップで必ず「Regenerate」をクリックして新しいTokenを生成してください。

---

## ステップ4: 認証情報（APIキー）を取得

### 4-1. Keys and tokensタブへ

アプリページの「Keys and tokens」タブを開きます。

### 4-2. 5つの情報を取得

以下5つの情報を生成・取得します。**取得時に1度しか表示されないものがあるので、必ずメモしてください。**

| 情報 | どこで取得 | 使い道 |
|------|----------|------|
| **API Key** (Consumer Key) | API Key and Secret → "Regenerate" | 認証 |
| **API Key Secret** (Consumer Secret) | 同上、ペアで表示 | 認証 |
| **Bearer Token** | Bearer Token → "Generate" | 読み取り用 |
| **Access Token** | Access Token and Secret → "Generate" | 投稿・読み取り |
| **Access Token Secret** | 同上、ペアで表示 | 投稿・読み取り |

### 4-3. ⚠️ 超重要: 絶対にやってはいけないこと

- ❌ Gitリポジトリにコミットしない
- ❌ ChatGPT/Claudeのチャットに貼り付けない（一部は公開ログに残る）
- ❌ Slackや公開チャンネルに書かない
- ❌ スクリーンショットを撮らない

取得した情報は **パスワードマネージャー**（1Password、Bitwarden等）に保存してください。

---

## ステップ5: 認証情報をPC上に保存

### 5-1. 認証情報ファイルを作る

ターミナルを開いて以下を実行:

```bash
touch ~/.x-tweetcraft.env
chmod 600 ~/.x-tweetcraft.env
```

### 5-2. 中身を記入

テキストエディタで `~/.x-tweetcraft.env` を開き、以下を貼り付けて実際の値を入れます:

```bash
X_BEARER_TOKEN=ここにBearer Tokenを貼る
X_API_KEY=ここにAPI Keyを貼る
X_API_SECRET=ここにAPI Key Secretを貼る
X_ACCESS_TOKEN=ここにAccess Tokenを貼る
X_ACCESS_TOKEN_SECRET=ここにAccess Token Secretを貼る
```

**注意:** 値は**ダブルクォートで囲まない**でください（そのまま貼り付け）。

### 5-3. なぜホーム直下に置くの？

- `~/.x-tweetcraft.env` → ホームディレクトリ（プロジェクト外）
- プロジェクトディレクトリに置くと、うっかりGitにコミットしてしまうリスクがある
- ホーム直下なら確実に独立している

---

## ステップ6: 接続テスト（オプション）

Claude Codeでx-tweetcraftプラグインを読み込んだ状態で：

```
X APIの接続テストして
```

→ x-connect-apiが簡単な疎通確認を行います（例: 自分のプロフィール取得）。

成功すれば完了です。🎉

---

## トラブルシューティング

### 「403 Forbidden」エラー
→ App permissionsが「Read only」になってる可能性。「Read and write」に変更してAccess Tokenを**再生成**。

### 「401 Unauthorized」エラー
→ .envファイルの値が間違っている、または空白・改行が混入している可能性。

### 「Rate limit exceeded」エラー
→ Freeプランのリミットに達した可能性。プラン詳細は `api-plans-and-costs.md` を参照。

### 申請が却下された
→ 用途説明を「personal use」「no data collection」「human-reviewed」を強調して再申請。

---

## 次のステップ

接続完了したら：

1. **「自分の投稿分析して」** → x-analyze-posts 起動
2. **「今日のツイート作って」** → x-draft が API連携モードで動く
3. **「x-scheduleして」** → 自動化セットアップ

無料プランで始めて、必要を感じたら Basic（$200/月）にアップグレードする流れがおすすめです。

---

## サポート

Issues: https://github.com/RyoroSuzuki/x-tweetcraft/issues
