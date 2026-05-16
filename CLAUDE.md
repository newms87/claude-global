# Claude Global Config

Discipline rules + skills live in plugins. Source: `~/web/claude-plugins/`. Marketplace: `newms-plugins` → `github:newms87/claude-plugins`. Per-instance plugin set in `<repo>/.claude/settings.json`. Container worker baseline at `/home/danxbot/.claude/settings.json` (baked in danxbot Dockerfile, auto-updates via `autoUpdate: true`).

**Edit flow:** rule/skill source in plugin → commit (do NOT push by hand) → `cd ~/web/claude-plugins && ./scripts/publish.sh patch <plugin>` (bumps `.claude-plugin/plugin.json` version, commits the bump, pushes) → `/reload-plugins` in active sessions.

**Plain `git push` of a plugin edit is a NO-OP for consumers.** The marketplace loader compares `version` fields, not commit shas. Pushing source-tree changes without bumping `.claude-plugin/plugin.json` means every consumer keeps whatever version they cached on first install. The dead-code state is silent — your edit looks shipped on GitHub, ships nowhere. Verify per-plugin docs at `~/web/claude-plugins/scripts/publish.sh` if memory disagrees. **Mechanical pre-action check before declaring a plugin edit "done": did `./scripts/publish.sh <bump-type> <plugin>` run + push?** If not, the edit is unshipped — period; no rationalization, no "I'll bump later", no "the consumer will pick it up anyway". Bump or it never landed.

## MANDATORY pre-edit check — discipline rules + skills

Before creating/editing ANY rule or skill file (`.claude/rules/*.md`, `.claude/skills/**/SKILL.md`, `CLAUDE.md` rows referencing them), STOP and answer:

> "Is the source-of-truth for this rule/skill the plugin under `~/web/claude-plugins/<plugin>/`?"

Yes → edit plugin source, commit + push, `/reload-plugins`. That is the only flow for danxbot rules + skills now (was previously dual-housed in the poller inject pipeline; epic DX-269 retired the inject side). When in doubt, plugin wins.

**Pre-write scope gate — answer BEFORE editing `~/.claude/CLAUDE.md` or anything under `~/.claude/rules/` / `~/.claude/skills/`. Mechanical, no rationalization allowed:**

1. Does the rule TEXT name any of: a specific repo (`danxbot`, `gpt-manager`, etc.), a specific app / package (`@thehammer/*`, etc.), a specific plugin (`base`, `dev`, `pipeline`, `investigate`, `danxbot`, `human-collaboration`, `issues`, `issue-worker`), OR ANY plugin skill in `<plugin>:<skill>` form (`dev:debugging`, `investigate:investigate`, `pipeline:explain`, etc.)? → **STOP. Wrong file.** No exemption — "universal because it applies in every session" is FALSE: plugins also load in every session, so the universal-everywhere argument routes to the plugin, NOT here. Project-scoped rule → edit `~/web/<repo>/CLAUDE.md` or `~/web/<repo>/.claude/rules/<file>.md`. Plugin-scoped rule → edit `~/web/claude-plugins/<plugin>/skills/<skill>/SKILL.md` or sibling rule file, commit + push, `/reload-plugins`.
2. Is the rule a self-trigger / load-discipline gate FOR a plugin skill (e.g. "always invoke X before Y")? → **STOP. The skill's own description IS the trigger surface.** Edit the skill description / SKILL.md body in the plugin so the trigger fires from the plugin's own load path — global self-reminders here are second-class and get ignored when the skills list is long.
3. Only after BOTH answer "no": the rule is genuinely universal (applies to every project AND no plugin owns its subject) → edit here.

The "make sure I see it next time" / "I want it loaded everywhere" instinct is the rationalization that causes this exact failure. Plugins ARE the everywhere-loaded surface; if the rule belongs everywhere AND a plugin already owns the subject, the rule belongs IN that plugin.

## `@thehammer/*` npm publish — invoke `thehammer-publish` skill

Editing any `@thehammer/*` source OR about to `npm publish` against `@thehammer/*` OR about to defer with "operator must publish" → invoke `thehammer-publish` skill (lives at `~/.claude/skills/thehammer-publish/` — newms-personal, not in any plugin). Owner-repo make-target table + standing autonomous-publish authorization + pre-publish `grep "^publish" Makefile` check live there.

## Rule placement — plugin as default

Discipline rules + skills that any session needs (operator's main session OR danxbot dispatched agents) → plugin skill in `~/web/claude-plugins/danxbot/skills/<skill>/`. The `newms-plugins` marketplace mirrors the plugin into every consumer's settings with `autoUpdate: true`, so the same source loads everywhere automatically — main session, host-mode dispatched workers, and container workers (whose baseline `/home/danxbot/.claude/settings.json` enables the plugin) all read the same body.

Per-repo or per-workspace rules that vary by `RepoContext` (`danx-repo-config.md`, `danx-repo-overview.md`, `danx-repo-workflow.md`, `danx-tools.md`) → poller's inject pipeline at `~/web/danxbot/src/poller/inject/workspaces/<workspace>/.claude/`. These files are templated and regenerated each tick from the connected repo's `.danxbot/config/`; never edit them by hand. The inject pipeline no longer ships static rules or skills — epic DX-269 retired that surface in favor of single-sourced plugin content.

Default when adding a new rule: plugin.

## Monitoring loops — wait ≠ task

Watching a target reach a state is the GOAL, not the action. After flagging a blocker once: investigate root cause + try the next safe action you have authorization for (root-cause fix, retry, restart). Re-pinging "no change" each tick = failure to do the job. Re-read prior-turn restrictions per tick — "do not auto-clear" applies to the FIRST observation, not every observation across hours.

**Idle-queue mechanical check (danxbot poller / any periodic dispatcher).** Before saying "wait one more tick" compute: `seconds_since_last_dispatch_completion / tick_interval`. If quotient ≥ 2 AND queue depth > 0 AND worker reports healthy → that is a BUG, not cadence. The next-tick excuse is only valid when quotient < 1. Don't anchor on "I personally haven't observed a full tick" — anchor on the system's own elapsed-since-completion clock.