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
| `skills/` | Invocable skills (`/commit`, `/trello`, etc.) |
| `agents/` | Shared agents available in all projects |
| `settings.json` | Hooks (sound effects on events) |

## What's NOT Here

These are gitignored and stay local:

- `.credentials.json` — Auth tokens
- `plans/`, `projects/`, `tasks/` — Session-specific data
- `cache/`, `debug/`, `telemetry/` — Ephemeral data
- MCP server config — Lives in `~/.claude.json` (separate file)

## Projects Using This

- [gpt-manager](https://github.com/newms87/gpt-manager) — AI-powered team object management
- [danx-ui](https://github.com/newms87/danx-ui) — Vue 3 + Tailwind CSS component library
- platform — Monorepo with Laravel backend + Vue frontend
