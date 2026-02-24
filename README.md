# Claude Global Config

Shared [Claude Code](https://docs.anthropic.com/en/docs/claude-code) configuration across all projects. Contains rules, skills, agents, and settings that apply globally.

## Setup

Clone into `~/.claude/`:

```bash
git clone git@github.com:newms87/claude-global.git ~/.claude
```

Then install `clad` to your PATH:

```bash
~/.claude/bin/install.sh
```

## clad — Claude with Automatic credential Detection

`clad` manages multiple Claude Max accounts, checks rate limit usage across all of them, and launches Claude Code with the best available credential.

### Quick Start

```bash
# Add your first account
clad --add=personal

# Add another account
clad --add=work

# Launch Claude — clad picks the best credential automatically
clad
```

### How It Works

1. Discovers all credential files (`~/.claude/.credentials-*.json`)
2. Syncs any tokens that Claude refreshed back to the named files
3. Refreshes expired tokens via OAuth (prompts login if refresh fails)
4. Checks rate limit usage for each credential (5h + 7d utilization windows)
5. Selects the best key and copies it to `.credentials.json`
6. Launches `claude --dangerously-skip-permissions`

### Per-Project Preferences

Link a project directory to prefer a specific account:

```bash
cd ~/my-project
clad --link=work
echo ".claude-credentials.json" >> .gitignore
```

When `clad` runs from that directory, it prefers the linked credential (as long as it's under 99% usage). The symlink should be gitignored since it's machine-specific.

### Selection Algorithm

- Check the preferred key first (project symlink or current default)
- If preferred key is under 99% used, keep it
- If over 99%, cycle through remaining keys
- First key found with under 90% usage wins
- If all keys are over 90%, use the one with the lowest usage

### Commands

| Command | Description |
|---------|-------------|
| `clad` | Launch Claude with best credential |
| `clad --add=NAME` | Add a new credential account |
| `clad --login=NAME` | Re-login to fix a corrupted credential |
| `clad --link=NAME` | Link current directory to prefer NAME |
| `clad --help` | Show help with full usage details |

Extra arguments pass through to Claude: `clad --resume ID`, `clad -p "prompt"`, etc.

## What's Here

| Directory | Purpose |
|-----------|---------|
| `bin/` | CLI tools (`clad`) |
| `rules/` | Global coding standards and workflow rules |
| `skills/` | Invocable skills (`/flow-commit`, `/flow-code-review`, `/trello`, etc.) |
| `agents/` | Shared agents available in all projects |
| `settings.json` | Hooks (sound effects on events) |

## What's NOT Here

These are gitignored and stay local:

- `.credentials*.json` — Auth tokens (managed by `clad`)
- `plans/`, `projects/`, `tasks/` — Session-specific data
- `cache/`, `debug/`, `telemetry/` — Ephemeral data
- MCP server config — Lives in `~/.claude.json` (separate file)
