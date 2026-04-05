---
name: x-interview
description: Deepen the user's brand-voice.md by conducting an interactive interview that surfaces their career history, turning points, values, and original stories. Use after x-setup when brand-voice feels generic or shallow, when the user says "brand-voiceを深めたい", "もっとパーソナライズしたい", "インタビューして", "自分の原体験を入れたい", or when tweet drafts feel surface-level. The output is a richer brand-voice.md with persona depth, origin stories, values, and "only-I-can-tell" angles.
---

# x-interview

Conduct a deep personal interview to surface the user's unique story and inject it into brand-voice.md. Past tweets alone produce shallow brand voices — lived experience makes them distinctive.

## Workflow

### Step 1: Explain the purpose and set the stage

Tell the user:
> brand-voice.md を深めるためのインタビューを始めます。
>
> 過去ツイートだけだと表層的になりがちなので、あなたの**原体験・価値観・転機**を聞いていきます。
> これらが入ると、あなたにしか書けない投稿を生成できるようになります。
>
> 全部で20-30分くらい。気が乗らない質問はスキップOKです。
> 途中で「ちょっと今日はここまで」でも大丈夫。続きは後日できます。

Confirm readiness: "始めてOKですか？"

### Step 2: Conduct the interview in 6 rounds

Ask questions **one at a time**. Wait for each answer before moving to the next. Follow up when answers are short or surface-level.

**Do not batch questions.** One question per message, deep engagement.

#### Round 1: キャリアの軌跡（5問）
1. これまでの職歴を教えてください。新卒から今まで、業界・職種の変遷を
2. その中で一番長くいた/思い入れのある会社・プロジェクトは？なぜ？
3. 途中で大きく方向転換した瞬間はありましたか？何がきっかけで？
4. 今の事業（会社・プロダクト）を始めた直接的なきっかけは？
5. その前後で「自分の見方」が変わったことはありますか？

#### Round 2: 転機・挫折（3-4問）
1. キャリアで一番しんどかった時期は？何があった？
2. 失敗したり、撤退した経験は？そこから学んだことは？
3. 「あの時の選択が全てを変えた」という分岐点はありますか？
4. （任意）話せる範囲で、個人的に一番重い経験は？

#### Round 3: 価値観・信念（4-5問）
1. 仕事で絶対に譲れないことは？
2. 逆に、周りの多くが大事にしてるけど自分はそう思わないことは？
3. 「これは自分が正しいと思う」という逆張り意見は？
4. 尊敬する人・ロールモデルは誰？何が尊敬ポイント？
5. 10年後、どうありたい？

#### Round 4: 発信したい届けたい人（3問）
1. 今のXフォロワーはどういう人が多そう？
2. 本当に届けたい「理想のフォロワー像」は？その人のどんな悩みに刺さりたい？
3. その人に「自分だから言える」と思うメッセージは？

#### Round 5: 自分だからこそ語れる話（3-4問）
1. 業界的に「あるある」だけど外からは見えにくいこと、知ってますか？
2. あなたが当たり前だと思ってるけど周りからは驚かれる習慣・思考・スキルは？
3. 過去の経験で「今なら笑い話にできる」エピソードは？
4. 持ちネタ・武勇伝・黒歴史、どれか一つ教えて

#### Round 6: 発信スタンス（2-3問）
1. 自分の投稿で「これは自分らしい」と思うものは？
2. 逆に「これは盛った/寄せた」と感じたものは？
3. これから発信で意識していきたいトーンは？

### Step 3: Verify and clarify

After all 6 rounds, summarize what you learned:
> ありがとうございます。聞いた内容を整理します。[3-5行のサマリ]
>
> この理解で合ってますか？補足や訂正ありますか？

### Step 4: Draft the enhanced brand-voice.md

Update (or create) brand-voice.md by **merging** new interview data with existing content (do not erase the old).

**New sections to add:**

```markdown
## 原体験・キャリアストーリー
（Round 1-2の内容を物語として）

## 価値観・信念
（Round 3の内容）
- 譲れないこと: ...
- 違和感があること: ...
- 逆張り意見: ...
- ロールモデル: ...
- ありたい姿: ...

## 自分だからこそ語れる領域
（Round 5の内容）
- ドメイン知識: ...
- 独自視点: ...
- 持ちネタエピソード: ...

## 届けたい人
（Round 4の内容）
- 理想のフォロワー像: ...
- その人の悩み: ...
- 自分だから言えるメッセージ: ...
```

### Step 5: Present and iterate

Show the updated brand-voice.md and ask:
> 大幅にアップデートしました。読んでいただいて、違和感・追記したい部分ありますか？

Iterate until the user is satisfied.

### Step 6: Save and close

Confirm save location and write the file.

Tell the user:
> brand-voice.md v2、保存しました。
>
> これで `x-draft` を実行すると、今までより「あなたらしい」下書きが出るはずです。
> 試してみませんか？

## Interview Principles

- **One question at a time** — batch questions dilute depth
- **Follow up on short answers** — "もう少し詳しく" "例えばどういう時？"
- **Resist the urge to summarize mid-interview** — just listen
- **Don't judge or interpret** during the interview — save it for Step 3-4
- **Respect skips** — if they say "次でいい", don't push
- **Watch for gold** — when they say something unusual, pause and dig

## Red Flags to Avoid

- Don't ask leading questions ("これは大変でしたよね？")
- Don't project your own interpretations back
- Don't fabricate experiences — only capture what the user actually says
- Don't make brand-voice.md sound like a resume — it should feel alive

## Edge Cases

**User gives very short answers:**
Gently probe: "もう少し聞かせてください" "具体的にどういう場面？"

**User says they have nothing interesting:**
Reframe: "それが当たり前に思えてるだけかも。周りの人に『それ面白い』って言われたこと、ないですか？"

**User wants to stop midway:**
Save progress to brand-voice.md with a note "（インタビュー途中保存）", offer to resume later.

**User's answers contradict past tweets:**
Note it but don't judge. Ask: "過去ツイートだとこういう傾向があるけど、それは意図してた？それとも流れで？"
