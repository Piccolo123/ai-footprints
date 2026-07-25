# URL Manager — Agent-first URL collection & knowledge management

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

**Deliver results as beautiful cards, not raw link dumps.** An [agentskills.io](https://agentskills.io)-compatible skill that lets AI agents save, organize, search, and share web resources on behalf of human users. Agents auto-register on first use — zero manual setup.

> 📖 **Agent instructions** → [SKILL.md](./SKILL.md)
>
> 🇨🇳 **中文版** → [SKILL.zh-CN.md](./SKILL.zh-CN.md)

## What This Tool Gives Humans

The content human users want to save is everywhere — a YouTube workout video, an Amazon gear link, a Substack training plan — scattered across platforms with no connection. **URL Manager fixes this.** Paste any link from any platform. AI auto-identifies the content and suggests a category — confirm and it's a footprint. All saves flow into one platform-agnostic library, organized and always findable. Then share in one click.

## Install

```bash
hermes skills tap add Piccolo123/url-manager
```

Works across Hermes, Claude Code, Cursor, Codex, and any agentskills.io-compatible agent.

## How Agents Use It

```
1. Agent auto-registers on first call — no human credential setup
2. Agent collects links during research sessions
3. Agent categorizes, tags, and organizes into structured collections
4. Agent delivers results via magic link — user clicks to see card-based interface
```

## Features

- **Agent-first auto-registration** — zero human setup
- **Save anything** — web links (URL auto-fetched) or plain-text notes
- **Full-text search** — across titles, descriptions, and AI summaries
- **Categories, tags, category sets** — hierarchical organization
- **Shared categories** — team collaboration with cocreate (co-editing) and subscribe (read-only) modes
- **Batch operations** — reorganize up to 50 items at once
- **Magic link delivery** — send organized collections as a polished card interface
- **Cross-platform** — Hermes, Claude Code, Cursor, Codex, OpenClaw

## Privacy

This skill connects to a hosted backend at **ai.ocean94.com**. On first use, the agent auto-creates an account. All collected URLs and data are stored on this backend.

- Users can delete their data at any time via the web interface
- Collected data is accessible only to the account owner
- [Terms of Service](https://ai.ocean94.com/terms.html) · [Privacy Policy](https://ai.ocean94.com/privacy.html)

## License

MIT — see [LICENSE](./LICENSE).
