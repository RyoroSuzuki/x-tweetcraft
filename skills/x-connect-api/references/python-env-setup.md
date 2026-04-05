# Python環境セットアップ ガイド（非エンジニア向け）

x-tweetcraft MCPサーバーを動かすためにPython環境が必要。この文書は x-connect-api スキルがClaudeに指示する際の参照資料。

**ターゲットユーザー:** プログラミング経験ゼロの経営者・一般ユーザー

## なぜPythonが必要？

x-tweetcraft がX APIを叩くために、mcp-server/server.py（Python製）を起動する必要がある。Python自体はMacならデフォルトで入っていることが多い。

## OS別: Python確認と導入

### macOS

**確認:**
```bash
python3 --version
```

**3.9以上が表示されたら:** 次のステップへ

**出なかった or 3.8以下:**
1. Homebrew経由（推奨）
   ```bash
   # Homebrewが入っているか確認
   brew --version

   # Homebrewが無ければインストール（Claudeが一緒に進める）
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Python 3 インストール
   brew install python@3.11
   ```

2. 公式サイト経由
   - https://www.python.org/downloads/macos/ から最新版のmacOS installerをダウンロード
   - pkgファイルをダブルクリックでインストール

### Linux (Ubuntu/Debian)

```bash
python3 --version

# なければ
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Windows

- 公式サイト: https://www.python.org/downloads/windows/
- インストール時「Add Python to PATH」に**必ずチェック**を入れる
- 確認: PowerShellで `python --version`

## 依存ライブラリのインストール

Pythonが入っていたら、x-tweetcraftが使うライブラリを入れる。

### 推奨: `--user` フラグでシステムPython汚染を回避

```bash
# x-tweetcraft ディレクトリに移動
cd <plugin-root>/mcp-server

# 必要なライブラリをユーザーディレクトリにインストール
python3 -m pip install --user -r requirements.txt
```

インストールされるもの:
- `fastmcp` — MCPサーバー構築用
- `tweepy` — X API公式Pythonクライアント
- `python-dotenv` — `.env` 読み込み用

### 上級者向け: venv使用

環境を完全に隔離したい場合:

```bash
cd <plugin-root>/mcp-server

# 仮想環境作成
python3 -m venv .venv

# アクティベート
source .venv/bin/activate   # macOS/Linux
# または
.venv\Scripts\activate      # Windows

# ライブラリインストール
pip install -r requirements.txt
```

**注意:** venvを使う場合、`.mcp.json` の `python` を `.venv/bin/python` に変更する必要がある。

## トラブルシューティング

### `pip: command not found`

```bash
python3 -m ensurepip --upgrade
```

### `ModuleNotFoundError: No module named 'tweepy'`

インストールが完了していない、または違うPythonを使っている:

```bash
# どのpythonが使われるか確認
which python3

# そのPythonで直接インストール
$(which python3) -m pip install --user -r requirements.txt
```

### `Permission denied`（macOS）

`--user` フラグが抜けている可能性：

```bash
python3 -m pip install --user -r requirements.txt
```

### `externally-managed-environment`（macOS、Python 3.11+）

HomebrewのPythonで発生。venvを使うか、`--break-system-packages` 追加（非推奨）：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## import確認

ライブラリが正しく入ったかチェック:

```bash
python3 -c "import tweepy; import fastmcp; import dotenv; print('All OK')"
```

`All OK` と出れば成功。

## 完了後の次ステップ

Python環境が整ったら、認証情報のセットアップへ進む。
→ `credential-input-guide.md` を参照
