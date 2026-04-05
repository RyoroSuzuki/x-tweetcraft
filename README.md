# x-tweetcraft

Claude Code plugin for crafting personalized X (Twitter) posts. Generates tweet drafts grounded in your own brand voice, then (optionally) automates posting — without losing the voice that makes you *you*.

## Features

- **Personalized draft generation** — Tweet drafts grounded in your own voice, themes, and patterns
- **Progressive enhancement** — Works without X API; richer when connected
- **2-layer brand voice** — Public (tweet-ready) + Private (voice source, not publicly shared)
- **Pausable interview** — Deepen your brand voice over multiple sessions
- **Onboarding flow** — From zero to working brand voice in minutes

## Skills Included

| Skill | Purpose |
|-------|---------|
| `x-setup` | Initial onboarding: generates brand-voice structure from X account + sample tweets |
| `x-interview` | Deep personal interview (6 rounds, pausable) to enrich brand voice |
| `x-draft` | Generates 5-10 personalized tweet drafts with hypothesis and rationale |
| `x-connect-api` | Guides X Developer API application, authentication, and connection |

**Planned (P1, after X API connection):**
- `x-post` — Post drafts directly to X
- `x-refresh-brand-voice` — Update brand voice from 100+ historical posts
- `x-reflect` — Weekly learning from chosen/rejected drafts

## Install

### Prerequisites

This plugin works best with these Claude Code companion skills installed:

**Strongly recommended:**
- `document-skills@anthropic-agent-skills` — PDF/DOCX/XLSX/PPTX readers (useful for importing vision docs, career sheets, brand guidelines)
- `superpowers@claude-plugins-official` — brainstorming, writing-plans, TDD workflows (useful for content planning)

Install companion skills:
```bash
claude plugin install document-skills@anthropic-agent-skills
claude plugin install superpowers@claude-plugins-official
```

### Install x-tweetcraft

**Option A: Local (for development/testing):**
```bash
git clone https://github.com/RyoroSuzuki/x-tweetcraft.git ~/develop/x-tweetcraft
claude --plugin-dir ~/develop/x-tweetcraft
```

**Option B: Via marketplace (when published):**
```bash
claude plugin install x-tweetcraft@<marketplace-name>
```

## Usage

### Quick start

```
# In Claude Code
「x-setupして」
```

This walks you through:
1. Companion skills check
2. Your X account info
3. Tweet sample gathering (copy-paste or Claude browser extension)
4. Brand voice generation
5. Offer to chain to x-interview for depth

### Daily workflow

```
「今日のツイート作って」
```

Generates 5-10 drafts from your brand voice. Pick, edit, post.

### Deepening your brand voice

```
「x-interviewで深めたい」
```

Runs a 6-round interview. Pausable — do 1 round today, continue tomorrow.

### Connecting X API

```
「x-connect-apiして」
```

Walks through X Developer Portal application and setup.

## Brand Voice Structure

After setup, you'll have this structure (in your working directory):

```
brand-voice.md                    # Index + quick summary + command guide
personal-info/
├── public-voice.md               # Public layer: tone, themes, patterns
├── values-and-origin.md          # Private layer: values, origin, career
├── audience-and-messages.md      # Private layer: target, core messages
└── interview-logs/               # x-interview session records
```

The **2-layer design** separates:
- **Public** (tweet-ready) — tone, themes, patterns you'll use in tweets
- **Private** (voice source) — origin stories and values that inform your perspective but aren't directly published

This lets you build a rich brand voice without having to publicly share personal stories before you're ready.

## Philosophy

> "Same road, walking alongside." Not a mentor, not a coach — just someone walking the same path who leaves observations for others following.

x-tweetcraft is designed to help you show up consistently as yourself, without performance or posturing. The goal isn't virality — it's authentic presence that finds your people.

## Development Status

- ✅ MVP: Core generation flow (no API required)
- ⏳ P1: X API integration (MCP server, auto-post, analytics)
- 🔜 P2: Reflection/learning loop

## License

MIT

## Author

Ryoro Suzuki ([VITAL Z Inc.](https://www.vital-z.co.jp/))
