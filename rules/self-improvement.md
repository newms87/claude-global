# Agent Self-Improvement

## The Rule

After completing work (post-commit), reflect on the session. If you encountered an inefficiency that wasted significant effort or expensive resources — and a small documentation addition would have prevented it — update the docs.

**This is a workflow step, not optional reflection:**

```
Plan → Implement → Test Coverage → Code Review → Fixes → Commit → Self-Improvement
```

## Real-Time Notes: Capture Problems As They Happen

Context gets compacted. By the time you reach the self-improvement step, you may not remember what went wrong. **Write notes immediately when you make an inefficient mistake.**

**File:** `agent-notes.md` in the project root (git-ignored, ephemeral).

**When to write:** As soon as you perform a wasteful action — re-run an expensive command, go down a wrong path, make an avoidable mistake. Write the note IMMEDIATELY, not later.

**Format:** Each note must identify the task context and the problem clearly enough that a future agent (or yourself after context compaction) can understand it:

```markdown
## [Task Name] Short description of inefficiency

**What happened:** 1-2 sentences describing the wasteful action you took.
**What should have happened:** 1-2 sentences describing the correct approach.
**Potential rule:** Draft the rule that would prevent this (or "N/A - one-off mistake").
```

**During the self-improvement step:**
1. Read `agent-notes.md`
2. For each note YOU wrote (match by task name): decide if it warrants a doc update
3. If yes: add the rule to the appropriate docs file and log it in the improvement log
4. If no: discard it — it was a one-off
5. **Delete your notes** from the file after processing. Do not let this file grow.

**IMPORTANT:** Other agents may have notes in this file too. Only process and delete notes you recognize as yours (by task name). Leave other agents' notes untouched.

## When to Self-Improve

**Only when ALL of these are true:**

- You wasted meaningful effort (re-ran expensive operations, went down a wrong path, made avoidable mistakes)
- A short, clear rule would have prevented it
- The rule is small (1-10 lines) — not a paragraph of explanation

**Do NOT self-improve for:**

- Minor inconveniences or one-off edge cases
- Things that are already documented but you missed
- Hypothetical improvements ("this might help someday")
- Adding verbose explanations to existing rules

## Where to Add Rules

| Scope | Location |
|-------|----------|
| **All projects, all languages** | `~/.claude/rules/` (global) |
| **This project only** | Project `.claude/rules/` or project docs |

Ask: "Would this rule help an agent working in ANY codebase?" If yes, global. If it's project/framework-specific, keep it local.

## Self-Improvement Log

**Every self-improvement MUST be recorded** in a changelog file so the user can review what agents are changing:

| Scope | Log file |
|-------|----------|
| **Global rules** | `~/.claude/agent-self-improvement.md` |
| **Project rules** | `<project-root>/.claude/agent-self-improvement.md` |

If the log file doesn't exist, create it. Each entry records what changed and why:

```markdown
## YYYY-MM-DD: Short title

**File:** `path/to/rule-file.md`
**Change:** What was added/modified (1 sentence)
**Why:** What went wrong that this prevents (1 sentence)
```

## Guardrails

- **Sparingly.** Most sessions should NOT trigger self-improvement. Only obvious wins.
- **Small additions only.** If the rule needs more than 10 lines, it's too complex — simplify or skip.
- **Never remove existing rules.** Only add or clarify.
- **Never restructure docs.** Add your rule to the most relevant existing file.
- **Log every change.** No silent doc edits.
- **`agent-notes.md` must be git-ignored.** Add it to `.gitignore` in any new project.
