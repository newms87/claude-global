# Claude Global Config

All discipline rules + skills now ship as Claude Code plugins from the `newms-plugins` marketplace at `~/web/claude-plugins/`. The plugin system handles auto-invocation; this file is a lean pointer.

## Plugins

Source of truth: `~/web/claude-plugins/` (separate git repo, single user-authored marketplace).

| Plugin | Purpose |
|---|---|
| `base` | Universal discipline. Install on every claude instance. |
| `investigate` | Read-only diagnostic methodology. No fix-writing. |
| `dev` | Code-writing: TDD, debugging-with-fix, code quality, git safety. |
| `pipeline` | Human-in-loop dev: flow-* skills, plan mode, collaboration. |
| `issues` | Issue card workflow + tracker contract. |
| `danxbot` | Danxbot orchestrator domain knowledge. |
| `issue-worker` | Autonomous issue-worker skills (danx-*). Workspace-only. |

## Install matrix

| Env | base | investigate | dev | pipeline | issues | danxbot | issue-worker |
|---|---|---|---|---|---|---|---|
| Global default (this file) | ✓ | | | | | | |
| Repo dev session | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| issue-worker workspace | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ |
| slack-worker workspace | ✓ | ✓ | | | ✓ | ✓ | |
| system-test workspace | ✓ | | | | | ✓ | |

Project-level `<repo>/.claude/settings.json` declares `enabledPlugins` per-repo. Workspace-level `.claude/settings.json` (committed in danxbot's `src/poller/inject/workspaces/<name>/`) declares per-workspace plugin set. Container worker `/home/danxbot/.claude/settings.json` is baked in danxbot Dockerfile and registers the marketplace at `/opt/claude-plugins`.

## Adding a new rule or skill

Edit the source plugin in `~/web/claude-plugins/<plugin>/skills/<name>/SKILL.md`. Run `/reload-plugins` in any active session. Container workers pick up changes on next image build (`make build` in danxbot rsyncs the monorepo into the docker context).

## Local marketplace

Already registered in this `settings.json` as `newms-plugins` → `directory:/home/newms/web/claude-plugins`. Adding new plugins to the marketplace.json catalog makes them installable immediately via `claude plugin install <name>@newms-plugins`.

## Backups

Pre-migration content moved to:
- `/tmp/claude-dev-backup-*` — old `~/.claude/dev/`
- `/tmp/claude-rules-skills-backup-*` — old `~/.claude/{rules,skills}/`

Once confident migration is stable (workspace dispatches succeed in container), these can be deleted.
