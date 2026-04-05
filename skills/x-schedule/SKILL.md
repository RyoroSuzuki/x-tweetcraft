---
name: x-schedule
description: Set up automated recurring x-tweetcraft workflows using Claude Code's scheduling system. Use when the user says "スケジュール設定して", "朝までに下書き作っておいて", "自動化したい", "毎朝ツイート準備", "毎週月曜に振り返り", "x-schedule", "cron設定", or wants to run x-draft/x-analyze-posts/x-content-strategist automatically. Presents pre-built schedule templates (morning draft prep, weekly strategy review, monthly brand refresh) and lets users customize frequency/time/content.
---

# x-schedule

Set up recurring automated executions of x-tweetcraft workflows. Users wake up to fresh drafts, weekly strategy reports, and brand voice refreshes — no manual triggering needed.

## Workflow

### Step 1: Check scheduling infrastructure

Verify Claude Code scheduling is available:
- Look for `CronCreate`, `CronList`, `CronDelete` tools
- Or `schedule` skill (claude-code-scheduler)
- Or system-level cron (fallback)

If none available, tell the user:
> この環境にはClaude Codeのスケジューリング機能が見つかりません。
> `schedule` skill を `claude plugin install` で追加するか、macOS/Linuxのcrontabを使う方法を案内できます。

### Step 2: Present schedule templates

Ask the user which automation to set up. Show templates from `references/schedule-templates.md`:

> 以下のテンプレートから選んでください（複数選択可）:
>
> **A) 朝の下書き準備（毎朝）**
> 起床前に自動で最新トレンド・自分の投稿分析・下書き10案を生成。朝起きたらすぐ選んで投稿するだけ。
>
> **B) 週次戦略レビュー（月曜朝）**
> 先週の振り返り＋今週の方向性を x-content-strategist が提案。
>
> **C) 月次ブランドリフレッシュ**
> x-refresh-brand-voice で過去100件以上を深く分析してbrand-voiceをアップデート。
>
> **D) 即興：カスタム**
> 独自のスケジュールを設定。

Read `references/schedule-templates.md` for the full specs of each template.

### Step 3: Customize the chosen template

For each selected template, ask:
- **時刻**: 実行タイミング（デフォルトから変更するか）
- **頻度**: 毎日 / 平日のみ / 週次 等
- **通知**: 完了時にSlack等へ通知するか（任意）
- **API依存**: 未接続機能を含む場合は警告し、どう動作させるか選択

### Step 4: Generate the schedule command

For each customized schedule, construct the Claude Code prompt that will run at the scheduled time.

Before generating the cron command, **determine the user's data directory**:
- Ask the user: "x-tweetcraftのインストールフォルダを教えてください（例: `~/x-tweetcraft`、`~/Documents/x-tweetcraft`）"
- Record as `PLUGIN_DIR` variable
- This is both the plugin directory AND where user data lives (unified model)

Example prompt for morning draft prep (with `PLUGIN_DIR=~/x-tweetcraft`):
```
cd ~/x-tweetcraft && claude --plugin-dir . -p "brand-voice.md を読んで、x-analyze-posts と x-research-trends を軽量実行してから x-draft を起動。下書き10案を personal-info/draft-logs/$(date +%Y-%m-%d_%H%M).md に保存して終了。"
```

### Step 5: Create the schedule

Use the available scheduling tool to register the cron:

**If `CronCreate` tool available:** Call it directly with the schedule expression and prompt.

**If `schedule` skill available:** Invoke the skill with the schedule config.

**If falling back to crontab:** Generate a crontab entry and show the user with install instructions.

### Step 6: Save schedule metadata

Write to `personal-info/schedules.md` (VITAL Z path priority same as brand-voice.md):

```markdown
# Active Schedules

## [Schedule name]
- 頻度: [cron expression + human-readable]
- 実行内容: [what runs]
- 登録日: YYYY-MM-DD
- 状態: active / paused
- 最終実行: (updated by job)
```

This file gives the user visibility into what's running.

### Step 7: Guide next steps

Tell the user:
> スケジュール登録しました。
>
> - 一覧確認: 「スケジュール一覧見せて」
> - 一時停止: 「[名前] を止めて」
> - 削除: 「[名前] を削除」
> - 変更: 「[名前] の時刻を変えたい」
>
> 実行結果は `personal-info/draft-logs/` や各種logsディレクトリに自動保存されます。

## Template Details

See `references/schedule-templates.md` for full specifications of each pre-built template, including:
- Exact cron expressions
- Full command prompts for each schedule
- Expected runtime duration
- API dependencies and fallbacks
- Output locations

## Managing existing schedules

**List all:**
Call `CronList` or equivalent, and cross-reference with `personal-info/schedules.md`.

**Pause/resume:**
Update state in scheduling system and schedules.md.

**Delete:**
Call `CronDelete` and update schedules.md.

## Principles

- **User consent per schedule**: Never create multiple schedules in one go without explicit user selection
- **Fail-safe defaults**: If API dependency fails mid-execution, save partial output with error log rather than deleting work
- **No silent actions**: Each scheduled run produces a log file in `draft-logs/` or equivalent
- **Timezone clarity**: Always confirm timezone when setting schedules (default to user's system timezone)
- **Budget-aware**: Warn user if running x-analyze-posts/x-research-trends daily could hit API rate limits

## Edge Cases

**User's machine is off at scheduled time:**
Tell them: "このスケジュールはあなたのPCで動くので、PCが起動していない時はスキップされます。クラウドで動かす場合はGitHub Actions等の追加設定が必要です。"

**User requests extremely frequent schedule (e.g., every 10 min):**
Warn about API rate limits and cost. Suggest minimum 1h interval for most workflows.

**Schedule conflicts with X API free plan limits:**
Explain the monthly quota and suggest a frequency that stays safe.

**User wants to run while traveling/different timezone:**
Ask which timezone they want to anchor to.

## Integration

- **Depends on**: Claude Code scheduling tools (CronCreate/schedule skill)
- **Reads**: `brand-voice.md` (to customize prompts with user's context)
- **Writes**: `personal-info/schedules.md` (active schedules log)
- **Invokes at scheduled times**: `x-draft`, `x-analyze-posts`, `x-research-trends`, `x-content-strategist`, `x-refresh-brand-voice` (P1)
