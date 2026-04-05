# Agent Self-Improvement

## Real-Time Notes

Context gets compacted — write notes immediately when you make a wasteful mistake. File: `agent-notes.md` in project root (git-ignored, ephemeral).

**When to write:** As soon as you perform a wasteful action (re-ran expensive command, wrong path, avoidable mistake). Write immediately, not later.

**Format:**
```markdown
## [Task Name] Short description

**What happened:** 1-2 sentences.
**What should have happened:** 1-2 sentences.
**Potential rule:** Draft rule or "N/A - one-off mistake".
```

**Processing:** `/flow-self-improvement` reads the file at end of pipeline, decides what warrants doc updates, makes changes, cleans up.

## When to Self-Improve

**Only when ALL true:** Wasted meaningful effort, a short rule (1-10 lines) would prevent it, and it's not a one-off edge case.

**Do NOT** self-improve for minor inconveniences, hypothetical improvements, or verbose explanations.

## /docs and /explain Always Produce a Change

"The rules already cover this" is NEVER acceptable. If an error happened despite existing rules, those rules failed — make them more prominent, more specific, or placed where the agent reads them. `/docs` -> rule/doc update. `/explain` -> concrete prevention proposal (not "I'll be more careful").

## Where to Add Rules

All projects: `~/.claude/rules/` (global). This project only: project `.claude/rules/` or CLAUDE.md. Ask: "Would this help an agent in ANY codebase?" If yes, global.

## Rules, Not Memory

Behavioral corrections go in rules files, NEVER in memory. Memory = contextual, soft, disposable. Rules = universal, durable, authoritative. When the user corrects behavior, that's a rule.

## Self-Improvement Log

Every change MUST be logged: global rules -> `~/.claude/agent-self-improvement.md`, project rules -> `/tmp/claude-agent-notes/<project>/agent-self-improvement.md`.

```markdown
## YYYY-MM-DD: Short title
**File:** path. **Change:** 1 sentence. **Why:** 1 sentence.
```

## Guardrails

Sparingly (most sessions don't trigger this). Small additions only (max 10 lines). Never remove existing rules. Never restructure docs. Log every change. `agent-notes.md` must be git-ignored.
