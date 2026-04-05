---
name: x-connect-api
description: Guide the user through X (Twitter) Developer API application, authentication, and connection. Use when the user says "x-connect-apiして", "X API接続したい", "Developer API申請したい", "API繋ぎたい", "x-post使いたい", "API料金知りたい", or when skills report that X API is not available and the user wants to enable it. Walks through portal application, app creation, credential retrieval, .env setup, and connection test with detailed cost expectations upfront. Most suitable for non-developer users (business owners, content creators).
---

# x-connect-api

Walk the user through connecting X Developer API. x-tweetcraft's real power (L2分析, L3トレンド, 週次戦略, 自動投稿) requires this connection. Without it, only L1 (draft generation) works.

**Target user:** Non-developers. Assume zero familiarity with APIs, tokens, or Developer portals.

## Workflow

### Step 1: Explain value and cost upfront (重要)

Before starting the application, set accurate expectations. Tell the user:

> X API接続は **x-tweetcraftの真価を発揮するため必須** です。ただし料金がかかります。
>
> **料金の概算:**
> - **Free プラン ($0)**: 自動投稿のみ。分析・トレンド機能は実質使えない
> - **Basic プラン ($200/月 ≈ 30,000円)**: すべての機能が動く。**本格運用ならこちら**
>
> **なぜお金が必要？**
> X社が2023年以降、APIを有料化しました。無料枠は月100投稿の取得しかできず、分析や検索には使えません。
>
> 詳細はここに: `${CLAUDE_PLUGIN_ROOT}/skills/x-connect-api/references/api-plans-and-costs.md`
> （あなたの運用ケース別コスト目安も書いてます）
>
> **最初のおすすめ:** まず Free で申請して動作確認 → 必要を感じたら Basic にアップグレード
>
> 続けますか？

**If user wants more cost info:** Read `references/api-plans-and-costs.md` and present relevant sections.

**If user hesitates:** Remind them x-tweetcraft still works without API (L1生成のみ)。急がなくてOK。

### Step 2: Check current state

Ask the user where they are:
> 現在の状況を教えてください:
>
> A) まだ何もしていない（Developer Portalアカウント未作成）
> B) Developer Portalは登録済み、App未作成
> C) App作成済み、認証情報取得済み
> D) 認証情報を .env に設定済み、接続テストをしたい

### Step 3: Guide based on starting point

**For detailed step-by-step walkthrough**, read `references/detailed-setup-guide.md` and follow the relevant sections:
- A → Start from Step 1 of the guide
- B → Jump to Step 3 of the guide
- C → Jump to Step 5 of the guide
- D → Jump to Step 6 of the guide

The detailed guide covers:
- Exact portal navigation
- Application text template (English)
- App permissions configuration (Read and write)
- ⚠️ Access Token regeneration after permission changes
- Secure credential storage (~/.x-tweetcraft.env)
- Common errors and fixes

**When reading references**, adapt the content to user's specific situation. Don't dump the whole file into chat — guide conversationally.

### Step 4: Application text (if at Step A)

**If the user has a pre-drafted application text** (e.g., `ceo/x-automation/X_API_APPLICATION.md` for VITAL Z users), read it and offer to use that.

**Otherwise**, provide the generic template from the detailed guide and customize with the user's specifics (use case, target audience from brand-voice.md if available).

### Step 5: Security reminder

Always remind before credential handling:

> ⚠️ **絶対にやってはいけないこと:**
> - APIキーをGitリポジトリにコミットしない
> - APIキーをチャット（ChatGPT/Claude.ai等）に貼らない
> - APIキーをSlackや公開チャンネルに書かない
> - スクリーンショットを撮らない
>
> 保存先: `~/.x-tweetcraft.env`（ホーム直下、リポジトリ外）
> バックアップ: パスワードマネージャー推奨

---

## Phase B: 環境セットアップ代行（非エンジニア最優先）

**Claudeがbashコマンドを実際に実行**してユーザーを詰まらせない。ユーザーは Y/N で答えるだけ。

**全bash実行前に必ずユーザー確認を取る:**
> これから以下を実行します。よろしいですか？
> `<コマンド>`
> （Y/N）

### B1: Python環境チェック

Run:
```bash
python3 --version
```

- **3.9以上が表示:** B2に進む
- **出ない or 3.8以下:** ユーザーのOSを聞いて、`references/python-env-setup.md` のOS別導入手順を参照して案内する

### B2: pip利用可否チェック

Run:
```bash
python3 -m pip --version
```

- **正常:** B3に進む
- **"No module named pip":** `python3 -m ensurepip --upgrade` を案内

### B3: 依存ライブラリインストール

プラグインのインストール場所を特定：
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

その値を使ってrequirements.txtをインストール（`--user` フラグでシステムPython汚染回避）：
```bash
python3 -m pip install --user -r "${CLAUDE_PLUGIN_ROOT}/mcp-server/requirements.txt"
```

**エラー時の分岐:**
- `externally-managed-environment` (macOS Homebrew Python 3.11+): venvモードを案内
- `Permission denied`: `--user` フラグが抜けていないか確認
- その他: `references/python-env-setup.md` のトラブルシュートを参照

import確認：
```bash
python3 -c "import tweepy; import fastmcp; import dotenv; print('All OK')"
```

### B4: .env ファイル雛形作成

**確認後に実行:**
```bash
# 既存チェック
ls -la ~/.x-tweetcraft.env 2>/dev/null
```

- **既存で値入り:** B5をスキップしてB6へ
- **既存で空 or 未作成:** 以下を実行

```bash
cat > ~/.x-tweetcraft.env << 'EOF'
# X Developer API credentials for x-tweetcraft
# Get these from https://developer.x.com/en/portal/dashboard

X_BEARER_TOKEN=
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
EOF

chmod 600 ~/.x-tweetcraft.env
```

### B5: 認証情報入力（セキュリティ最優先）

ユーザーに2つの方式を提示：

> 認証情報をどう入力しますか？
>
> **A) エディタで直接貼り付け（簡単・macOS推奨）**
> → ファイルをテキストエディタで開いて、値を貼り付けて保存
>
> **B) 対話スクリプトで入力（よりセキュア）**
> → 画面に表示されない方式で1つずつ入力。チャット履歴にも残らない
>
> どちらにしますか？

**方式A選択時:**
```bash
open -t ~/.x-tweetcraft.env   # macOS
# または
xdg-open ~/.x-tweetcraft.env  # Linux
# または
notepad "$env:USERPROFILE\.x-tweetcraft.env"  # Windows
```

ユーザーに伝える：
> エディタが開きました。5つの `=` の右側に各値を貼り付けて、保存してください。
> **ダブルクォート（"）で囲まない**でください。保存したら教えてください。

**方式B選択時:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/mcp-server/setup-credentials.py"
```

対話形式でgetpass経由入力（画面非表示）。

**Claudeがやってはいけないこと:**
- `cat ~/.x-tweetcraft.env` を実行しない（値が見えてしまう）
- 値をチャットに表示しない
- 値をコピーして別の場所に書き出さない

### B6: 動作確認（認証情報をログに出さない）

空欄チェックのみ（値は読まない）：
```bash
grep -c "^X_[A-Z_]*=$" ~/.x-tweetcraft.env
```

`0` と出れば全入力完了。他の数字が出たらユーザーに未入力の項目があることを伝える（どの項目かは言わない、プライバシーのため「○項目未入力です」だけ）。

ファイル権限確認：
```bash
ls -la ~/.x-tweetcraft.env
```

`-rw-------` であることを確認。違う場合は `chmod 600 ~/.x-tweetcraft.env` を実行。

**詳細参照:**
- Python環境: `references/python-env-setup.md`
- 認証情報入力: `references/credential-input-guide.md`

---

## Phase C: 接続テスト

### Step 6: MCPサーバーを再起動して接続確認

MCPサーバーは `.mcp.json` 経由で起動する。認証情報を設定した後は **Claude Codeセッションを再起動** するとMCPサーバーが新しい `.env` を読み込む。

ユーザーに伝える：
> 認証情報のセットアップが完了しました。
>
> 新しい認証情報を読み込むため、Claude Codeを一度終了して再起動してください：
> ```
> /exit（またはCtrl+D）→ claude --plugin-dir <plugin-path> で再起動
> ```
>
> 再起動後、「X APIの接続テストして」と言えば、軽いAPI呼び出しで動作確認します。

### Step 7: Next steps guidance

Once setup is complete:

> 🎉 X API接続準備完了です！これで以下が使えるようになります:
>
> **今すぐ使えるもの（API依存スキル）:**
> - `x-analyze-posts` — 過去投稿の深い傾向分析
> - `x-research-trends` — 市場トレンド研究
> - `x-content-strategist` — 週次戦略レビュー（agent）
> - `x-draft` — API連携データ込みでより精度の高い下書き生成
>
> **計画中（P1実装予定）:**
> - `x-post` — 下書きを直接投稿
> - `x-refresh-brand-voice` — 過去投稿100件以上を分析してbrand-voice深化
>
> まず試すなら:
> - 「自分の投稿分析して」で `x-analyze-posts` を実行
> - 「今伸びてるツイート調べて」で `x-research-trends` を実行

## References

- **Detailed setup guide** (non-developer-friendly): `references/detailed-setup-guide.md`
- **API plans & costs** (pricing analysis): `references/api-plans-and-costs.md`

## Principles

- **Expect zero technical knowledge** — User is likely a business owner/creator, not a developer
- **Surface costs upfront** — Don't let users discover $200/month pricing after the setup
- **Emphasize Free→Basic path** — Most users should start Free to validate
- **Walk through conversationally** — Don't dump reference file contents; guide step-by-step

## Edge Cases

**User's application gets rejected:**
- Common reasons: vague use case, commercial data mining language, bot-like behavior wording
- Fix: rewrite with "personal use", "human-reviewed", "own account only"

**User is confused about Project vs App:**
- Clarify: Project contains Apps. Create a Project → App auto-generated inside.

**User has multiple X accounts:**
- API is tied to the account that creates the App. Log in with the posting target account.

**User hesitates due to cost:**
- Affirm: x-tweetcraft works without API for L1 (draft generation). No pressure to pay.

**Access Token was generated BEFORE setting Read+Write permissions:**
- Must regenerate Token. This is the most common pitfall. Explicitly warn.

## Integration

- **Triggered by:** User asking about API, or skills reporting "API unavailable"
- **Writes:** `~/.x-tweetcraft.env` (user's home, NOT in repo)
- **Enables:** All L2/L3 skills and agents that depend on X API
