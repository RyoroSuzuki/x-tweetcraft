# Browser Extension Extraction Prompts

Shared prompts for Claude browser extension usage across x-tweetcraft skills. When the user has Claude's browser extension installed and needs to extract data from X (Twitter), present the relevant prompt below.

---

## Prompt 1: 自分のツイート抽出（x-setup用）

**Use case:** User needs to extract their own recent tweets to build initial brand-voice.

**Instructions:** User opens their X profile page, then pastes this prompt into Claude browser extension:

```
【背景】
私は自分のXアカウントの投稿を半自動化するツールを構築中で、
そのために「自分のブランドボイス（文体・トーン・テーマ・型）」を
定義するドキュメントを作成しています。
このページから抽出したツイートは、そのドキュメント作成の元データになります。

【抽出してほしい情報】
- 自分のオリジナル投稿のみ（リポスト・引用RP・返信は除く）
- 最大20件、新しい順
- 各ツイートの本文 + 反応数（いいね、RP、ブックマーク、インプ）

【出力フォーマット】
各ツイートをMarkdownで以下の形式で：

---
### ツイート1
**本文:** [ツイート本文を改行・絵文字・ハッシュタグ・URL含めてそのまま]
**投稿日時:** [表示されている日時]
**いいね:** [数字] / **RP:** [数字] / **ブックマーク:** [数字] / **インプ:** [数字]
---

【注意事項】
- 本文は絶対に要約・加工しないでください（文体分析のため原文が必要）
- 数字が見えないものは「-」と記入
- スレッドの場合は各ツイートを別々に扱う
- ツイートの内容自体に対する感想や分析は不要、抽出のみ

以上です。よろしくお願いします。
```

---

## Prompt 2: トレンド・市場調査ツイート抽出（x-research-trends用）

**Use case:** User needs to extract trending tweets from X search results or a specific topic/account.

**Instructions:** User opens X search results or topic page, then pastes this prompt:

```
【背景】
私は自分のXでの発信の戦略を立てるために、最近伸びている関連ツイートの「型」や
「フォーマット」をリサーチしています。
誰かの投稿をコピーするのではなく、勝ちパターンを抽象化して自分のbrand-voiceに
翻訳するのが目的です。

【抽出してほしい情報】
このページから、エンゲージメントの高そうなツイート（目安: いいね100以上 または
リプライ10以上）を10-20件抽出してください。

【出力フォーマット】
---
### ツイート1
**本文:** [原文そのまま]
**投稿者:** [@ハンドル]
**いいね/RP/リプライ:** [数字]
**投稿日時:** [表示されている日時]
---

【注意事項】
- 本文は絶対に要約せず原文のまま（型の分析に必要）
- プロモーション・広告ツイートは除く
- スパムっぽいバズ狙いアカウント（インプレゾンビ）も除く
- ツイート本文への感想・分析は不要、抽出のみ

以上です。よろしくお願いします。
```

---

## Prompt 3: 特定アカウントの型リサーチ（x-research-trends用）

**Use case:** User wants to analyze a specific account's posting patterns as a role model reference.

**Instructions:** User opens target account's profile page:

```
【背景】
私は自分のX発信の参考にしたいアカウントの投稿パターンを分析しています。
文体・型・テーマの傾向を抽象化して、自分のbrand-voiceに翻訳します。

【抽出してほしい情報】
このアカウントの最近の投稿から、反応が特に良いものを10件程度抽出してください。

【出力フォーマット】
---
### ツイート1
**本文:** [原文そのまま]
**いいね/RP/リプライ:** [数字]
**型（推定）:** [数字→気づき / 問いかけ / 体験談 / 逆張り等]
---

【注意事項】
- 本文は要約せず原文のまま
- パターンが共通しているものを優先（1つだけ極端に伸びたものより、安定して伸びるもの）
- リポスト・引用RPは除く

以上です。よろしくお願いします。
```

---

## 使い方

各スキルのSKILL.mdから、適切なpromptセクションを参照してユーザーに提示します。

- x-setup → Prompt 1
- x-research-trends → Prompt 2 or 3（ケースに応じて）
- x-analyze-posts → Prompt 1を流用（自分のツイート抽出）

プロンプトが大量のテキストなので、スキル本体には埋め込まず、このファイルから必要箇所だけピックアップしてください。
