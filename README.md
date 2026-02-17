# Claude Global Config

Shared [Claude Code](https://docs.anthropic.com/en/docs/claude-code) configuration across all projects. Contains rules, skills, agents, and settings that apply globally.

## Setup

Clone into `~/.claude/`:

```bash
git clone git@github.com:newms87/claude-global.git ~/.claude
```

## What's Here

| Directory | Purpose |
|-----------|---------|
| `rules/` | Global coding standards and workflow rules |
| `skills/` | Invocable skills (`/flow-commit`, `/flow-code-review`, `/trello`, etc.) |
| `agents/` | Shared agents available in all projects |
| `settings.json` | Hooks (sound effects on events) |

## What's NOT Here

These are gitignored and stay local:

- `.credentials.json` — Auth tokens
- `plans/`, `projects/`, `tasks/` — Session-specific data
- `cache/`, `debug/`, `telemetry/` — Ephemeral data
- MCP server config — Lives in `~/.claude.json` (separate file)