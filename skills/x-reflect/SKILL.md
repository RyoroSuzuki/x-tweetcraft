---
name: x-reflect
description: Capture learnings from each x-draft session automatically — which drafts were picked, which were rejected, how they were edited, and what patterns emerge. Updates learnings.md which x-draft reads on next run. Use when the user selects drafts from x-draft output (invoke after picking), when the user says "この選択を記録して", "学習しておいて", "x-reflect", "フィードバック記録", or periodically to review accumulated learnings. This is the autonomous learning loop of x-tweetcraft — your digital twin gets smarter every session.
---

# x-reflect

Close the learning loop. Every time the user picks, edits, or rejects drafts from x-draft, this skill captures that signal into `learnings.md`. x-draft reads this on the next run, so your digital twin gradually learns what you actually want vs what you don't.

## When this fires

**Automatic triggers (in x-draft workflow):**
- User picks 1+ drafts from x-draft output
- User edits a draft
- User says "この3番で行く"、"5番だけ投稿する"、"全部微妙"

**Manual triggers:**
- "x-reflect" / "フィードバック記録" / "学習しておいて"
- Weekly/periodic invoking: "今週の学習振り返って"

## Workflow

### Step 1: Gather the signal

From the current conversation or user input, identify:

**The 10 drafts** that were generated (from the previous x-draft output).

**User actions per draft:**
- 🟢 **Picked and posted as-is** (strongest positive signal)
- 🟡 **Picked but edited** (positive + specific correction signal)
- 🔵 **Picked for later/scheduled** (positive signal, delayed)
- ⚪ **Not picked, not rejected** (neutral)
- 🔴 **Explicitly rejected** ("これは違う" "これはナシ")
- 🟠 **Edited into something new** (strongest correction signal)

**Meta comments:**
- User's free-form feedback ("3番は〜な感じでお願い")
- Themes/patterns the user complained about or praised

Ask the user if information is missing:
> 今日の下書き10案から、どれを選びましたか？編集箇所や採用理由があれば教えてください。
> （スキップする場合は「スキップ」と言ってください）

### Step 2: Locate learnings.md

Search for `learnings.md` in this order:
1. `ceo/x-automation/personal-info/learnings.md` (VITAL Z convention)
2. `./personal-info/learnings.md` (other users)
3. `./learnings.md` (fallback)

**If not found:** Create a new file at the most appropriate location (matching where brand-voice.md is).

### Step 3: Extract learnings

For each piece of signal, derive a learning. Be specific, not generic.

**From picked-as-is:**
- "○○の型は今日の文脈で響く"
- "○○のトピックは今の鈴木さんの気分に合っている"

**From edited:**
- "○○の表現は使わない方が自分らしい" （user removed word）
- "○○を足すと自分らしくなる" （user added phrase）
- "文末は○○より○○の方がしっくりくる"

**From rejected:**
- "○○のトピックは今避けたい"
- "○○の型は自分には合わない"

**From meta feedback:**
- Direct quote and interpretation

**Red line:** Do not invent learnings. If the signal is too weak (user just said "OK"), skip it.

### Step 4: Update learnings.md

Append to learnings.md with timestamp. Do NOT overwrite.

Format:

```markdown
## YYYY-MM-DD のセッション

### 採用した型
- [pattern name]: [count]回
- [pattern name]: [count]回

### 却下されたパターン
- [pattern]: [回数] / 理由: [user's stated or inferred reason]

### 編集で見えた修正癖
- [original] → [edited]: [learning]

### ユーザー直接フィードバック
> [exact quote]
- 解釈: [what this means for future drafts]

### 今日の気づき（次回x-draftで反映すべきこと）
1. [concrete actionable insight]
2. ...
```

### Step 5: Deduplication / pattern aggregation

When learnings.md grows past 10 sessions, aggregate repeated patterns into a "確定した癖" section at the top:

```markdown
## 確定した癖（10+セッション分のパターン）

### 強い好み（5回以上採用された型）
- [pattern]: 採用[N]回
- [pattern]: 採用[N]回

### 強い拒否（5回以上却下された型）
- [pattern]: 却下[N]回

### 編集で一貫して直される表現
- "○○" → "△△"（[N]回の修正履歴）
```

This aggregation prevents learnings.md from becoming an unreadable journal.

### Step 6: Tell the user

> 今日の学習を記録しました。次回x-draftを実行するときに反映されます。
> [1-2個の具体的なlearnings要約]

## learnings.md をx-draftが参照する仕組み

x-draft は Step 1 で brand-voice.md を読む際、同じディレクトリの `learnings.md` も読み込みます。

- 強い好みパターン → 優先的に生成される
- 強い拒否パターン → 避けられる
- 修正癖 → 生成時に初めから反映される

これにより「使うほど賢くなる分身」が実現します。

## Principles

- **Evidence-based**: 1セッションだけの signal では「仮説」にとどめる。3+回繰り返されたら「確定」に昇格
- **Preserve user's exact words**: インタビューログと同じく、ユーザーの直接引用を大事にする
- **Aggregate, don't delete**: 古いセッションログは残しつつ、トップにサマリを足す
- **Don't guess**: ユーザーが何も言わなかったら learning 化しない
- **Brand-voice over learnings**: brand-voiceのNG事項とlearningsが矛盾したら、brand-voice優先

## Edge Cases

**Signal が曖昧（ユーザーが明示的にピックしなかった）:**
Ask: "今日の10案、しっくりきたのありましたか？"

**学習ファイルが肥大化（100+セッション）:**
Aggregateして古いセッションログを `learnings-archive/` に移動。

**brand-voice.mdとの矛盾が出た:**
Flag explicitly: "learningsでは○○だけど、brand-voice.mdでは△△と書いてあります。brand-voice.mdを更新しますか？"

**ユーザーが「全部却下」:**
Don't over-interpret. Ask: "何がハマらなかったですか？" — 空振りの理由を聞く。

## Integration

- **Reads**: `brand-voice.md`, `personal-info/learnings.md`, 直前のx-draft出力
- **Writes**: `personal-info/learnings.md`（追記・集約）
- **Consumed by**: `x-draft`（次回生成時に参照）、`x-content-strategist`（長期学習傾向の把握）

## Philosophy

分身を育てるのは、あなた自身の選択の積み重ね。

ピックする・却下する・編集する — その全てがシグナル。x-reflectはそれを言語化して記録し、分身が「次はもっとあなたらしく書けるように」していきます。
