# Claude Global Config

This is the shared Claude Code configuration repo, cloned to `~/.claude/`. It contains global rules, skills, agents, settings, and the `clad` CLI tool. Everything here applies across all projects.

## Repo Structure

| Path | Purpose |
|------|---------|
| `bin/clad` | Multi-account credential manager + launcher |
| `bin/install.sh` | Copies clad to `~/.local/bin/` |
| `rules/` | Global rule files loaded by Claude Code |
| `skills/` | Invocable skills (each has `SKILL.md`) |
| `agents/` | Shared agent definitions |
| `settings.json` | Hooks and global settings |
| `README.md` | User-facing repo documentation |

**Git tracked**: `bin/`, `rules/`, `skills/`, `agents/`, `settings.json`, `README.md`, `CLAUDE.md`, `.gitignore`

**Gitignored**: credentials, plans, projects, tasks, cache, debug, telemetry, session data

## clad CLI (`bin/clad`)

Manages multiple Claude Max accounts, checks rate limits, picks the best credential, and launches Claude Code.

### Flow

1. Discover `~/.claude/.credentials-*.json` files
2. Sync refreshed tokens from `.credentials.json` back to the last-active named file
3. Refresh expired OAuth tokens (prompt interactive login if refresh fails)
4. Check rate limit usage via minimal haiku API call (reads `anthropic-ratelimit-unified-*` headers)
5. Select best credential based on usage
6. Copy selected to `.credentials.json`, record in `.credentials-active`
7. Launch `claude` with appropriate flags

### Selection Algorithm

- Preferred key (project-linked or current default) with <99% usage: use it
- Otherwise, first key with <90% usage wins
- If all >=90%, use lowest usage

### Commands

| Command | What it does |
|---------|--------------|
| `clad` | Launch with best credential |
| `--add=NAME` | Create new credential |
| `--login=NAME` | Re-login existing credential |
| `--link=NAME` | Set project preference |
| `--trust` / `--no-trust` | Toggle dangerous mode per directory |
| `--verbose` / `--quiet` | Toggle startup verbosity |
| Extra args | Passed through to `claude` |

### Config Files

| File | Scope |
|------|-------|
| `~/.claude/.clad-config.json` | Global (verbose setting) |
| `.claude/clad.json` (in project) | Per-project (trust, credential) |
| `~/.claude/.credentials-active` | Last-activated credential path |

### Rate Limit Check

Uses a 1-token haiku API call. Reads unified rate limit headers (`5h-utilization`, `7d-utilization`, `representative-claim`). Uses the binding window's utilization. 429 = 100%. Auth failure = -1 (skip).

## Rules (`rules/`)

| File | Key Points |
|------|------------|
| `tool-usage.md` | Use Read/Edit/Write tools, never bash for file ops |
| `paths-and-commands.md` | Always `cd` first. Relative paths only. Local dev + HMR |
| `git-operations.md` | Commit format: `[Task] Phase N: Title`. Atomic stage+commit |
| `planning.md` | Plans via EnterPlanMode only. No code in plans. Full pipeline per phase |
| `core-principles.md` | SOLID/DRY/Zero-Debt. No backwards compat. Refactor first |
| `code-reviews.md` | Run reviewer agents via Task tool. Fix ALL findings |
| `testing.md` | 100% coverage. TDD for bugs. Never parallel tests |
| `debugging.md` | Prove bug before fixing. Never guess prop values |
| `self-improvement.md` | Real-time `agent-notes.md`. Process via `/flow-self-improvement` |
| `markdown-formatting.md` | Table rows under ~140 chars |

## Skills (`skills/`)

### Pipeline Skills (run automatically per phase)

| Skill | Purpose |
|-------|---------|
| `flow-commit` | Stage and commit with summary table |
| `flow-code-review` | Run reviewer agents, fix ALL findings |
| `flow-quality-check` | Post-review audit, catch rationalizations |
| `flow-report` | Present results after commit |
| `flow-self-improvement` | Process notes, update docs if warranted |

### Utility Skills

| Skill | Purpose |
|-------|---------|
| `trello` | Assign a Trello card to session |
| `next-phase` | Complete phase, sync Trello, commit, condense plan |
| `docs` | Update documentation based on what went wrong |
| `explain` | Diagnostic — analyze behavior, no code changes |
| `low-context` | Emergency context preservation |
| `code-review` | Full refactoring workflow with plan mode |

## Platform

WSL2 Linux. Hooks in `settings.json` use `powershell.exe` for Windows sound effects (chimes on question, tada on stop, notify on notification).
