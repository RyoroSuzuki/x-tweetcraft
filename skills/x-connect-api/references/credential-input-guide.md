# 認証情報入力ガイド（セキュリティ最優先）

X API の5つの認証情報を `~/.x-tweetcraft.env` に安全に保存するためのガイド。

## 2つの入力方式

| 方式 | 難易度 | セキュリティ | 推奨ユーザー |
|------|-------|-----------|-----------|
| **A. エディタ貼り付け方式** | ★☆☆ | ★★☆ | 初心者（macOS） |
| **B. 対話スクリプト方式** | ★★☆ | ★★★ | セキュリティ重視 |

## 共通の準備（Claudeが代行）

### 1. .envファイル作成

Claude がユーザーに確認してから以下を実行：

```bash
# 存在確認（既にあれば上書きしない）
ls -la ~/.x-tweetcraft.env 2>/dev/null && echo "既存" || echo "新規作成"

# 新規作成の場合
touch ~/.x-tweetcraft.env
chmod 600 ~/.x-tweetcraft.env

# プレースホルダ付きテンプレートを書き込み
cat > ~/.x-tweetcraft.env << 'EOF'
# X Developer API credentials for x-tweetcraft
# Get these from https://developer.x.com/en/portal/dashboard

X_BEARER_TOKEN=
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
EOF
```

### 2. 権限確認

```bash
ls -la ~/.x-tweetcraft.env
```

`-rw-------` と出れば正しい（所有者のみ読み書き可能）。

---

## 方式A: エディタ貼り付け方式

**Claudeはこの流れでユーザーをサポート:**

### A1: エディタでファイルを開く（Claude実行）

**macOS:**
```bash
open -t ~/.x-tweetcraft.env
```
→ デフォルトのテキストエディタ（TextEditなど）が開く

**Linux:**
```bash
xdg-open ~/.x-tweetcraft.env
# または: nano ~/.x-tweetcraft.env
```

**Windows:**
```powershell
notepad $env:USERPROFILE\.x-tweetcraft.env
```

### A2: ユーザーが値を貼り付け

Claudeはユーザーにこう伝える:

> エディタが開きました。X Developer Portal の「Keys and tokens」タブで取得した5つの値を、
> 各 `=` の右側に貼り付けてください：
>
> - `X_BEARER_TOKEN=` の右側に Bearer Token
> - `X_API_KEY=` の右側に API Key
> - `X_API_SECRET=` の右側に API Key Secret
> - `X_ACCESS_TOKEN=` の右側に Access Token
> - `X_ACCESS_TOKEN_SECRET=` の右側に Access Token Secret
>
> **値をダブルクォート（"）で囲まないでください。**
> 貼り付けたら保存（Cmd+S / Ctrl+S）してエディタを閉じてください。

### A3: 入力確認（Claude実行）

**Claudeは中身を見ない。** 代わりに、プレースホルダが残っていないかだけチェック：

```bash
# 値が空のキーがあるか確認（Claudeは値は読まず、空欄だけ確認）
grep -c "^X_[A-Z_]*=$" ~/.x-tweetcraft.env
```

`0` と出れば全項目が入力済み。

**注意:** `cat ~/.x-tweetcraft.env` は絶対に実行しない（Claudeが値を見てしまう）。

---

## 方式B: 対話スクリプト方式（よりセキュア）

`mcp-server/setup-credentials.py` を実行。`getpass` モジュールで入力が画面に表示されない。

### B1: スクリプト実行（Claudeがユーザーに案内）

```bash
python3 <plugin-root>/mcp-server/setup-credentials.py
```

### B2: プロンプトに応じて入力

スクリプトは各値を順番に聞いてくる（入力は画面に出ない）：

```
X_BEARER_TOKEN を入力（Ctrl+Vでペースト可、画面には出ません）: ************
X_API_KEY を入力: ************
...
```

### B3: スクリプトが自動で.envに書き込み

- ファイルを `~/.x-tweetcraft.env` に作成
- `chmod 600` を自動適用
- 完了メッセージ表示

**メリット:**
- チャット履歴に認証情報が残らない
- ターミナル履歴にも残らない（getpass使用）
- ファイル権限も自動設定

---

## セキュリティ原則

### 絶対にやってはいけないこと

- ❌ Claudeのチャット欄に認証情報を貼る（ログに残る）
- ❌ `.env` ファイルをGitリポジトリにコミットする
- ❌ スクリーンショットを撮る
- ❌ Slack/Discord等の公開チャンネルに送る
- ❌ 別のAIチャット（ChatGPT等）に貼る

### 推奨する扱い

- ✅ パスワードマネージャー（1Password, Bitwarden等）に保管
- ✅ `~/.x-tweetcraft.env` はホーム直下（リポジトリ外）で管理
- ✅ 権限は常に `chmod 600`
- ✅ 使わなくなった認証情報は Developer Portal で Revoke

### キーが漏洩したら

1. X Developer Portal で即座に Revoke/Regenerate
2. 新しい認証情報で `.env` を更新
3. 漏洩経路を特定（Gitコミット、画面共有、等）

---

## Claudeが代行する際の確認フロー

各bash実行前に必ず：

> これから以下を実行します。よろしいですか？
>
> `<コマンド>`
>
> （Y/N）

ユーザーがYを返してから実行。エラーが出たらそのまま進めず、対処を案内する。
