---
name: trello
description: DEPRECATED — superseded by danx-issue. Do not invoke. Pickup of work cards now happens through the YAML issue tracker; the backend Trello sync is owned by the danxbot worker, not the agent.
---

# DEPRECATED — Use `danx-issue` Instead

This skill has been retired as part of the workflow migration epic (Phase 4). The agent path no longer interacts with Trello directly.

## What replaced it

| Old action | New action |
|---|---|
| `/trello <card name or URL>` to assign work | `/danx-issue ISS-N` (or `<repo>/.danxbot/issues/open/ISS-N.yml` path) |
| `mcp__trello__*` tool calls from agent | YAML edits + `mcp__danx-issue__*` MCP tools |
| Trello card IS the plan | Issue YAML IS the plan (`description` + `ac[]` + `phases[]` + `comments[]`) |
| Workflow rules in `~/.claude/rules/trello.md` | Workflow rules in `~/.claude/rules/issues.md` |

## Where Trello still exists

The danxbot **worker** (background poller, not part of the agent dispatch) is the sole writer to the Trello backend. It picks up YAML changes from `<repo>/.danxbot/issues/open/<id>.yml` on its ~60s tick and pushes them to Trello via the `IssueTracker` interface. Backend tracker config (board IDs, list IDs, label IDs) lives at `<repo>/.danxbot/config/trello-backend.md` and is consumed only by the worker.

## If a user types `/trello <something>`

Treat it as a `/danx-issue` invocation:

- If they pasted a Trello URL or short link, look up the matching local YAML by `external_id` field. `mcp__danx-issue__danx_issue_list({})` returns the open issues; grep for the `external_id`. Use the corresponding `id` (`ISS-N`).
- If they named a card by partial title, list open issues and match against `title` field.
- Then invoke the `danx-issue` skill with the resolved `ISS-N`.

Do not call any `mcp__trello__*` tool from this skill or any pickup flow.

## Cross-references

- `~/.claude/skills/danx-issue/SKILL.md` (now lives at the project level: `<repo>/.claude/skills/danx-issue/SKILL.md`)
- `~/.claude/rules/issues.md` — universal issue workflow patterns
