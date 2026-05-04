# Issue Workflow

Universal workflow rules for issue cards tracked as YAML files at `<repo>/.danxbot/issues/{open,closed}/<id>.yml` and synced to a backend tracker (Trello, Memory) by the danxbot worker.

**Agent path is YAML + `mcp__danx-issue__*` MCP tools only.** The agent never calls a backend tracker SDK directly. The danxbot worker is the sole writer to the backend on its ~60s poll cycle.

## YAML Schema

Authoritative source: `/home/newms/web/danxbot/src/issue-tracker/interface.ts` (the `Issue` type).

Quick reference:

| Field | Type | Notes |
|---|---|---|
| `schema_version` | `3` | Never change. |
| `tracker` | string | Don't change. Implementation-managed. |
| `id` | string (`ISS-N`) | Internal primary key. Filename is `<id>.yml`. Don't change. |
| `external_id` | string | Tracker-native id. Sync-layer only — never expose, never edit. |
| `parent_id` | `string \| null` | Phase card → epic's `id`. Reverse linkage to `children[]`. |
| `children` | `string[]` (ids) | Epics list their phase children. Maintained by `danx-epic-link` skill. |
| `dispatch_id` | `string \| null` | Poller-managed. Don't touch. |
| `status` | `Review` \| `ToDo` \| `In Progress` \| `Needs Help` \| `Done` \| `Cancelled` | Editing this field IS how you "move" the card. |
| `type` | `Bug` \| `Feature` \| `Epic` | Required. |
| `title` | string | Card name (no `#ISS-N:` prefix — worker prefixes when pushing). |
| `description` | string | Full markdown body. |
| `triaged` | `{timestamp, status, explain}` | Triage agent owns this. Leave alone. |
| `ac` | `[{check_item_id, title, checked}]` | Acceptance Criteria. New items: `check_item_id: ""` (worker assigns). |
| `phases` | `[{check_item_id, title, status, notes}]` | `status`: `Pending` \| `Complete` \| `Blocked`. |
| `comments` | `[{id?, author, timestamp, text}]` | Append `{author, timestamp, text}` (no `id`) — worker pushes. |
| `retro` | `{good, bad, action_items[], commits[]}` | Fill on Done / Cancelled / Needs Help only. Worker auto-renders ONE `## Retro` comment AND spawns one fresh issue per `action_items[]` string on terminal save. |
| `blocked` | `null` OR `{reason, timestamp, by[]}` | `null` when nothing blocks the card. Set to a record when the card is **waiting on other in-flight work** (a phase sibling, an Action Items card, a separately-scoped task) and DOES NOT need a human. `reason` is a non-empty sentence; `timestamp` is ISO 8601; `by[]` is a non-empty list of `ISS-N` ids that must reach Done / Cancelled before the card unblocks. If no card describes the unblock work, **create one** (`danx_issue_create`) and reference it. The worker forces `status: ToDo` whenever `blocked` is non-null; the poller auto-clears the record and dispatches the card once every blocker is terminal. **Blocked is NOT Needs Help** — see "Needs Help vs Blocked" below. |

## MCP Tool Surface

All under prefix `mcp__danx-issue__*` (note hyphen). Error shape: `{<verb>: false, errors: ["msg", ...]}`.

| Tool | Args | Purpose |
|---|---|---|
| `danx_issue_save` | `{id}` | Validate the YAML at `<repo>/.danxbot/issues/{open,closed}/<id>.yml` and reconcile with the tracker (or call `tracker.createCard()` for orphans with empty `external_id`). Returns `{saved: true, ...}` or `{saved: false, errors[]}`. Call after every meaningful Edit. |
| `danx_issue_create` | `{type, title, description, parent_id?, children?, status?, ac?, phases?, comments?}` | Allocate next `ISS-N`, build canonical YAML, push via `tracker.createCard`, write to `<repo>/.danxbot/issues/open/<id>.yml`. Returns `{created: true, id, path, external_id}` or `{created: false, errors[]}`. One call — no draft YAML required. |
| `danx_issue_get` | `{id}` | Read the YAML for a given `ISS-N` and return parsed object. Use to inspect parents, siblings, etc. without re-parsing manually. |
| `danx_issue_list` | `{status?, type?, parent_id?}` | Enumerate open issues filtered by status / type / parent. Avoid reading every YAML by hand. |
| `danx_issue_close` | `{id}` | Explicit terminal close (sets `status: Cancelled` if not already terminal, fills retro, moves file `open/` → `closed/`). |

**Save semantics:** Edit the YAML with `Edit` (never `Write` over an existing file — preserves other agents' uncommitted edits), then call `danx_issue_save({id})`. Validation runs synchronously; tracker push happens on the next worker poll (~60s). On `saved: false`, fix the validation errors in `errors[]` and re-call.

**Status terminal moves:** when you set `status: Done`, `status: Cancelled`, or `status: Needs Help` and save, the worker moves the file `open/` → `closed/` (Done / Cancelled) on its next poll. Never move the file yourself.

## Needs Help vs Blocked

Two different states for "this card cannot proceed right now":

- **Needs Help** (`status: "Needs Help"`): the card cannot complete without **a human acting**. Credentials, deploy, secrets rotation, ambiguous spec needing a human design call, architectural decision that changes the goal of the card, write-only repo. The card sits in Needs Help until the human acts.
- **Blocked** (`blocked: {...}`): the card is waiting on **other in-flight work** that does NOT need a human — phase siblings shipping first, an Action Items card landing, a separately-scoped task. The poller auto-unblocks and dispatches the card once every blocker reaches Done / Cancelled. Status remains `ToDo` (worker enforces). NEVER set `status: "Needs Help"` for a "waiting on another card" card; that's Blocked.

When the unblock work needs a human, the right shape is: keep this card Blocked, and put the human task in a NEW Needs Help card referenced from `blocked.by[]`. The original card unblocks the moment the human-task card moves to Done / Cancelled.

## Card Titles

`[Project > Domain] verb phrase` for features. `Fix:` prefix for bugs. Phase cards: `Epic Title > Phase N: Description`. Keep under ~80 chars.

## Card Descriptions (`description` field)

Must pass **zero-context test** — fresh agent with no conversation history can implement from description alone. No code blocks — prose only.

**Feature:** Context (what exists, why change) → Solution (high-level approach) → Key files.

**Bug:** Problem (what's broken) → Root Cause (why, or "TBD") → Solution (what to change) → Key files.

Every description must include: exact file paths, known gotchas, how to verify. Update with investigation findings when picking up a card (Edit the YAML's `description` field, then `danx_issue_save`).

## Checklists

Two YAML arrays, both authoritative:

**`ac[]` (Acceptance Criteria, required):** Specific, verifiable items starting with a verb. "Returns 422 when email missing" not "Handle validation."

**`phases[]` (Implementation Phases, only if multi-phase):** One item per phase. `status` field tracks `Pending` / `Complete` / `Blocked`.

There is no separate "Progress" checklist on the YAML schema — progress lives in the agent's pipeline (TDD test pass, code review pass, commit) and is reflected in `phases[i].status: Complete` plus `retro.commits[]` on terminal save.

`update_checklist_item` analogue: edit `ac[i].checked: true` (match by exact `title` text — `check_item_id` may be empty for new items the worker hasn't synced yet) or `phases[i].status: Complete`, then `danx_issue_save`.

## Reading a Card

Always read full context before starting:
- `description`
- ALL `comments[]` (every entry, oldest first)
- `ac[]` (with verification status)
- `phases[]`
- `triaged` (if non-empty)

`mcp__danx-issue__danx_issue_get({id})` returns the full parsed object. Never work from title alone.

## Creating a Card != Implementing It

**Spawn → DONE.** Don't implement, don't pick up, don't start work. The card hands work to a different agent in a different session. After `danx_issue_create`, only valid actions: tell user the card was created (show `ISS-N`), continue previous work, or stop.

## CRITICAL: Never Check Off an Unverified AC Item

Before setting `ac[i].checked: true`, must have direct evidence: passing test, command output, verified runtime result. "By construction" / "obviously correct" are NOT evidence. Cannot verify an AC item in current environment → leave `checked: false` and say so — never check off with an excuse for why verification was skipped.

## Card Lifecycle

**Pick up:** Edit YAML → set `status: In Progress`. Save. Read full context (description, all comments, all AC, phases, labels-equivalent via `type`). Plan work (complex: use writing-plans skill; simple: start immediately).

**During:** Append review results / discoveries to `comments[]`, save. Status moves + checklist edits handled by `flow-commit` skill.

**Complete:** All completion actions (check off ACs, fill retro, set `status: Done`) happen via `flow-commit`. Don't perform manually outside the pipeline.

## Phases vs Epics

**Phases on one card:** Most multi-step work stays on a single YAML with `phases[]` populated. Each phase = commit boundary, not a separate card. No `type: Epic` needed.

**Epic = work split across multiple YAMLs.** Use `type: Epic` only when individual phases warrant their own card (own `description`, own `ac[]`, own progress). Epic stays In Progress while phase cards are worked individually.

**When to split into epic:** Each phase looks like substantial work (multiple files, own tests, full session). Smaller related tasks → keep as `phases[]` items on one card.

**Epic mechanics:** Set epic's `type: Epic`, then IMMEDIATELY spawn all phase YAMLs (`Epic Title > Phase N: Description`), each with its own description / `ac[]` / `phases[]` / `type`. Set each phase's `parent_id` to the epic's `id`. Append each phase's `id` to the epic's `children[]`. Planning agent has full context — capture into phase cards NOW, not later.

**Where phase cards go:** Same `status` as parent epic at creation time. Epic in Review → phase cards Review. Epic In Progress → phase cards In Progress. Phase cards move with the epic through lifecycle.

**After completing each phase card:** Set its `status: Done`, fill retro, save. The worker handles the file move + retro comment + action-item spawn on its next poll. Then update the epic via `flow-commit`'s phase handoff (see `~/.claude/skills/flow-commit/SKILL.md`). All phase cards Done → epic also moves to Done with a retro comment summarizing all phases.

**CRITICAL: Update next phase card before ending session.** Append a "Notes from Phase N" entry to the next phase card's `comments[]` and save. Capture: discovered constraints, timing gotchas, reusable helpers + paths, cost/budget observations, dependencies between phases, corrections to the description. Assume the next agent reads ONLY `description` + `comments[]` — not epic handoff, not conversation history, not git log.

## Comment Formats

All comments append to `comments[]` as `{author, timestamp, text}` (no `id` — worker assigns).

**Retro** (filled in `retro.{good, bad, action_items, commits}` fields, NOT as a manual comment): worker renders ONE `## Retro` comment automatically on terminal save (Done / Cancelled / Needs Help). Re-saving with edited retro fields → worker edits the same comment in place.

**Bug Diagnosis** (bug cards): Problem, Root Cause, Solution. Either prepend to `description` or append as a `comments[]` entry titled `## Bug Diagnosis`.

**Review:** Summary of findings + fixes. Append as a `comments[]` entry titled `## Code Review` / `## Test Review` / `## Review Fixes`.

## The Card IS the Plan

Issue card assigned (`ISS-N`): never use `EnterPlanMode`, never invoke `writing-plans` or `executing-plans` skills. The YAML's `description` + `ac[]` + `phases[]` + `comments[]` ARE the plan. Re-fetch via `mcp__danx-issue__danx_issue_get({id})` after context compaction, when unsure what's left, before marking Done.

## Backend Tracker

Backend tracker (Trello today; could be others later) is owned by the danxbot worker. Backend-specific config (board IDs, list IDs, label IDs) lives in:

- `<repo>/.danxbot/config/trello-backend.md` (project-specific) — consumed only by the worker.

Agents do NOT read backend config and NEVER call `mcp__trello__*` tools. If a user pastes a Trello URL or short link, look up the matching local YAML by `external_id` field via `mcp__danx-issue__danx_issue_list({})`, then proceed by `id` (`ISS-N`).

## General Rules

- One card at a time
- Don't block on tracker sync failures — the worker retries on next poll; the YAML is canonical
- `type: Bug` or `type: Feature` minimum (or `Epic`) — required
- Comments = markdown with `##` headers
- AC + phases live in `ac[]` / `phases[]` — never inline in `description`
- `retro.action_items[]` strings cannot contain `→` (rejected by the tracker)
- Connected repo cards reference the connected repo's architecture (not danxbot's paths)
- NEVER call `mcp__trello__*` from agent path
- NEVER manually move YAML files between `open/` and `closed/` — terminal `status` triggers the worker move
