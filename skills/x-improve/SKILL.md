---
name: x-improve
description: Diagnose what's off with generated tweet drafts and route the user to the right improvement path (interview, X API connection, or reference tweets). Use when the user says "精度を上げたい", "下書きが浅い", "自分らしくない", "もっとあなたのことを知って精度を上げたい", "下書きがしっくりこない", "ブランドボイスが薄い", "AI感がある", "もっと自分らしく", or when drafts feel generic/shallow but the user doesn't know which improvement tool to pick. This skill asks a short diagnostic question then routes to x-interview, x-connect-api, or reference-tweet addition.
---

# x-improve

A lightweight diagnostic router. When users feel their drafts aren't good enough but don't know what to fix, this skill asks a short question to diagnose the issue and routes them to the right tool.

## Workflow

### Step 1: Acknowledge and diagnose

Tell the user:
> 下書きの質を上げたいんですね。何がズレてるか、少し聞かせてください。
>
> 以下のどれに一番近いですか？
>
> **A)** 文体や語尾、言い回しが「自分のじゃない」感じがする
> **B)** テーマや視点が浅い、自分の核心に触れてない気がする
> **C)** 今のXで伸びてる型と違う気がする／バズらない
> **D)** 実際に伸びた過去投稿のパターンと違う気がする
> **E)** 具体的には言えないけど、直感的にしっくりこない
> **F)** どれにも当てはまらない / 複合的

### Step 2: Route based on diagnosis

Based on the user's answer, propose the specific improvement path:

**A (文体・語尾・言い回しのズレ):**
→ 対話インタビューが効きます。
`x-interview` を起動して、あなたの言葉遣いや発信スタンスをもっと深く聞き出します。
「インタビュー始めていいですか？」と確認して、OKなら x-interview に遷移。

**B (テーマ・視点の浅さ):**
→ 対話インタビューで原体験・価値観を深掘りします。
`x-interview` で Round 2-3（転機・挫折・価値観）を重点的にやるのが効きます。
「ここを深掘りするインタビューをやりますか？」と確認して、OKなら x-interview に遷移。

**C (市場・トレンドとのズレ):**
→ X API連携で市場トレンドを分析に混ぜられます。
`x-connect-api` でX Developer APIに接続し、`x-research-trends` で今伸びてる型をリサーチします。
「X APIの接続案内を始めましょうか？」と確認して、OKなら x-connect-api に遷移。

**D (自分の実績データとのズレ):**
→ X API連携で過去投稿の実績データを分析に反映できます。
`x-connect-api` で接続し、`x-analyze-posts` で自分の過去投稿の伸びた型を自動把握します。
「X API接続の案内を始めましょうか？」と確認して、OKなら x-connect-api に遷移。

**E (直感的にしっくりこない):**
→ 参考ツイートを追加するのが早いです。
> あなたが「こういう投稿になりたい」「この人の投稿が理想」と思うツイートを3-5件教えてください。
> `personal-info/public-voice.md` の「参考ツイート」セクションに追加して、分身の方向性を調整します。

ユーザーがツイート提供したら、内容を `personal-info/public-voice.md` の参考ツイートセクションに追記。

**F (複合的・不明):**
→ まず対話インタビューで現状を整理するのが早道です。
> 複数の要素が絡んでそうですね。まずは対話インタビューで「どういう発信をしたいか」を改めて言語化してみるのが一番早いです。
> `x-interview` を起動して、Round 4（届けたい人）と Round 6（発信スタンス）から始めてみましょうか？

OKなら x-interview に遷移。

### Step 3: After routing

After the user completes the routed improvement:
- Suggest running `x-draft` again to see if quality improved
- Reassure: 「改善は1度で完璧にならないです。分身は使うほど育ちます」

## Principles

- **Short diagnostic** — Don't make the user fill out a survey. 1 question, 6 options.
- **Don't pathologize** — The user's drafts aren't "bad"; they're "still evolving"
- **Route confidently** — Pick the best single path, don't overwhelm with all options
- **Respect skip** — If the user says "どれでもない、やっぱりいいや", let them go

## Edge Cases

**User can't answer the diagnostic:**
If the user says "分からない" or skips, default to option F → x-interview.

**User wants multiple paths simultaneously:**
Say: 「順番にやりましょう。まずは○○から」と最優先を1つ選んで案内。

**User mentions a specific past draft:**
Ask: 「その下書きをもう一度見せてください。どの部分が気になりますか？」
その具体的な問題を起点に診断する。

**API未接続で C/D を選んだ:**
x-connect-api 案内に進むが、「接続には$0〜月数ドルのコストがかかる可能性があります」と伝える。
コスト感を気にするようなら、先にBを試す（インタビュー深掘り）ことを提案。

## Integration

- **Reads**: brand-voice.md で現在のボイス状況を把握
- **Routes to**: `x-interview`, `x-connect-api`, or updates `personal-info/public-voice.md` directly
- **Triggers downstream**: ルーティング先のskillを実行
