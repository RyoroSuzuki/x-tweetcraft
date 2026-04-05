---
name: x-interview
description: Deepen the user's brand voice by conducting an interactive personal interview. Supports pause/resume across sessions — users can do one round today, another next week. Use when the user says "brand-voiceを深めたい", "もっとパーソナライズしたい", "インタビューして", "x-interviewで深めたい", "インタビュー続きから", "自分の原体験を入れたい", or when tweet drafts feel shallow. Saves session logs to personal-info/interview-logs/ and resumes from the last completed round. Accepts document attachments (resumes, career sheets, vision docs) to enrich the interview.
---

# x-interview

Conduct a deep personal interview across 6 rounds to surface the user's unique story, values, and voice. Supports **pause/resume** — users don't need to finish in one session. Each session's log is saved and subsequent sessions continue from where they left off.

## Workflow

### Step 1: Check prior session history

Look for existing interview logs at:
- `ceo/x-automation/personal-info/interview-logs/` (VITAL Z convention)
- `./personal-info/interview-logs/` (other users)
- `./interview-logs/` (fallback)

**If logs exist:**
Read the most recent log file to identify:
- Which rounds are completed
- Which rounds are incomplete or not started
- Key material already gathered

Summarize to the user:
> 前回のインタビュー記録を見つけました:
> - 完了: [Round X, Y]
> - 未完了: [Round Z]
> - 未着手: [Round W, ...]
>
> どこから再開しますか？
> A) 前回の続きから（推奨）
> B) 特定のRoundを指定
> C) 新しく別の視点から深める

**If no logs exist:**
This is a first-time interview. Proceed to Step 2.

### Step 2: Explain purpose and set expectations

Tell the user:
> brand-voice を深めるためのインタビューを始めます。
>
> 過去ツイートだけだと表層的になりがちなので、あなたの**原体験・価値観・転機**を聞いていきます。
> これらが入ると、あなたにしか書けない投稿を生成できるようになります。
>
> **全部で6 Round・20-30分くらい。一気にやらなくてOKです。**
> 途中で「今日はここまで」と言えば、次回続きから再開できます。
> 気が乗らない質問もスキップOK。
>
> もし **職歴書・スキルシート・ビジョンドキュメント** などがあれば、
> ファイルパスを教えていただくか内容をコピペしてください。インタビュー時間が短縮できます。

Wait for confirmation.

### Step 3: Conduct the interview (one question at a time)

Ask questions **one at a time**. Wait for each answer. Follow up when answers are short or surface-level.

**Important:** One question per message. Do not batch questions.

#### Round 1: キャリアの軌跡
1. これまでの職歴を教えてください。新卒から今まで、業界・職種の変遷を
2. その中で一番長くいた/思い入れのある会社・プロジェクトは？なぜ？
3. 途中で大きく方向転換した瞬間はありましたか？何がきっかけで？
4. 今の事業（会社・プロダクト）を始めた直接的なきっかけは？
5. その前後で「自分の見方」が変わったことはありますか？

#### Round 2: 転機・挫折
1. キャリアで一番しんどかった時期は？何があった？
2. あの時の自分と同じ状態で苦しんでる人を今見かけたら、何を伝えたいですか？
3. 失敗したり、撤退した経験は？そこから学んだことは？
4. 「あの時の選択が全てを変えた」という分岐点はありますか？
5. （任意）話せる範囲で、個人的に一番重い経験は？

#### Round 3: 価値観・信念
1. 仕事で絶対に譲れないことは？
2. 逆に、周りの多くが大事にしてるけど自分はそう思わないことは？
3. 「これは自分が正しいと思う」という逆張り意見は？
4. 尊敬する人・ロールモデルは誰？何が尊敬ポイント？
5. 10年後、どうありたい？

#### Round 4: 届けたい人
1. 今のフォロワーはどういう人が多そう？
2. 本当に届けたい「理想のフォロワー像」は？その人のどんな悩みに刺さりたい？
3. その人に「自分だから言える」と思うメッセージは？

#### Round 5: 自分だからこそ語れる話
1. 業界的に「あるある」だけど外からは見えにくいこと、知ってますか？
2. あなたが当たり前だと思ってるけど周りからは驚かれる習慣・思考・スキルは？
3. 過去の経験で「今なら笑い話にできる」エピソードは？
4. 持ちネタ・武勇伝・黒歴史、どれか一つ教えて

#### Round 6: 発信スタンス
1. 自分の投稿で「これは自分らしい」と思うものは？
2. 逆に「これは盛った/寄せた」と感じたものは？
3. これから発信で意識していきたいトーンは？
4. 届けたい人に対してどんな立ち位置でいたい？（先輩/同志/観察者など）

### Step 4: Handle pause requests

If the user says "今日はここまで" / "続きは後で" / "一旦終了":

1. Save current progress to a session log (see Step 6)
2. Tell the user:
   > お疲れ様でした。ここまでの内容を保存しました。
   >
   > 次回再開するときは:
   > - 「x-interview続きから」
   > - または「brand-voiceをもっとパーソナライズしたい」
   >
   > と声をかけてください。前回の続きから再開します。

### Step 5: After each round completes

Between rounds, check in:
> [Round N] が完了しました。
> 次のRoundに進みますか？ それとも一旦休憩しますか？

This gives users natural pause points.

### Step 6: Save session log

At the end of each session (complete or partial), save a log file using the same path resolution order as Step 1:
1. `ceo/x-automation/personal-info/interview-logs/` (VITAL Z convention)
2. `./personal-info/interview-logs/` (other users)
3. `./interview-logs/` (fallback)

File name format: `YYYY-MM-DD_round{N}-{M}.md`

Log format:
```markdown
# インタビュー記録: YYYY-MM-DD（Round N-M）

## 実施情報
- 日付: YYYY-MM-DD
- 実施スキル: x-interview
- 状態: [完了 / 未完了]
- カバー範囲: Round N-M

## 次回再開ポイント
- [ ] 残りのRound

## 取得した素材
### Round N: [タイトル]
- 質問への回答を要約
- 本人の直接引用（重要な言葉はそのまま）

## 観察・所感
- インタビュアーとしての気づき
- 掘り下げた方がいい領域の仮説
```

### Step 7: Update personal-info/ files

Based on gathered material, update or create these files:
- `personal-info/public-voice.md` — 公的トーン・スタイル・テーマ
- `personal-info/values-and-origin.md` — 価値観・原体験・キャリア（Private）
- `personal-info/audience-and-messages.md` — 届けたい人・コアメッセージ（Private）

**Do not overwrite**. Merge new insights with existing content.

### Step 8: Update brand-voice.md index

If this was a significant update, update the クイックサマリ section and 更新履歴 in `brand-voice.md`.

### Step 9: Final handoff

If all 6 rounds complete:
> 全Round完了しました。brand-voice.mdを大幅にアップデートしました。
>
> これで `x-draft` がより深い下書きを生成できます。試してみませんか？

If partial:
> [Round N] まで完了しました。次回続きをやりましょう。

## Interview Principles

- **One question at a time** — batch questions dilute depth
- **Follow up on short answers** — "もう少し詳しく" "例えばどういう時？"
- **Resist the urge to summarize mid-interview** — just listen
- **Don't judge or interpret** during the interview — save it for later
- **Respect skips and pauses** — if they say "次でいい" / "今日はここまで", don't push
- **Watch for gold** — when they say something unusual, pause and dig
- **Accept document attachments** — if the user provides a file path or pastes content, read/use it to enrich context

## Red Flags to Avoid

- Don't ask leading questions ("これは大変でしたよね？")
- Don't project your own interpretations back
- Don't fabricate experiences — only capture what the user actually says
- Don't make brand-voice sound like a resume — it should feel alive
- Don't force continuation when the user wants to pause

## Edge Cases

**User gives very short answers:**
Gently probe: "もう少し聞かせてください" "具体的にどういう場面？"

**User says they have nothing interesting:**
Reframe: "それが当たり前に思えてるだけかも。周りの人に『それ面白い』って言われたこと、ないですか？"

**User wants to stop midway:**
Save progress, offer to resume later with clear instructions.

**User's answers contradict past tweets:**
Note it but don't judge. Ask: "過去ツイートだとこういう傾向があるけど、それは意図してた？それとも流れで？"

**User says "まだ何者でもないから上から目線は嫌":**
Take this seriously. Adjust the Public/Private split — put more material in Private (internal context) and keep Public tone as "同志" rather than "先輩".

**User provides documents (resumes, vision docs):**
Read them via appropriate tools. Extract relevant info. Ask follow-up questions to verify interpretation.
