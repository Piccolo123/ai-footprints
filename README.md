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

## DeepSeek Harness (dsh)

DeepSeek Harness natively supports both skill files and MCP servers — URL Manager plugs in either way.

### Option A — Skill (recommended, zero extra deps)

Clone into any skill discovery root, or add this repo's root as a custom skill dir:

```bash
# User-level (any workspace):
mkdir -p ~/.dsh/skills
git clone --depth 1 https://github.com/Piccolo123/url-manager.git ~/.dsh/skills/url-manager

# Or project-level (one workspace):
mkdir -p .dsh/skills && cp -r SKILL.md scripts .dsh/skills/url-manager/
```

Restart the session — `url-manager` appears in `<available_skills>`, and the model loads it on demand via the `skill` tool.

### Option B — MCP server (full 21-tool API surface)

Add to your profile's `cordis.patch.yml` (e.g. `~/.dsh/profiles/headless/cordis.patch.yml` or the `web` profile):

```yaml
- insert:
    - id: mcp-url-manager
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: url_manager
        transport: stdio
        command: uvx
        args: ['url-manager-mcp']
        env:
          FOOTPRINTS_ENDPOINT: 'https://ai.ocean94.com'
```

All 21 tools appear as `mcp__url_manager__*` (add_footprint, search_footprints, list_categories, agent_magic_link, …). The model auto-registers on first use — no API key needed.

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
