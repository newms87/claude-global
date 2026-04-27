---
name: flow-commit
description: Stage and commit changes with a summary table.
---

# Commit Workflow

`/flow-commit` IS the confirmation. Never ask "Ready to commit?" — just do it.

---

## Steps

1. Run `git status` and `git diff --name-only` in parallel to identify changed files
2. **Check for other agents' staged work** — if `git status` shows staged files that are NOT yours, another agent may be mid-commit. Poll `git status` every 5 seconds up to 30 seconds. If the staged files clear (committed by the other agent), proceed. If they persist after 30 seconds, ask the user.
3. Output the **Summary Table** and **Overview** (see format below)
4. Run a single chained command: `git add <file1> <file2> ... && git commit -m "..."`
5. **Push to remote** — run `git push` immediately after the commit succeeds. Push is part of every commit, not an optional follow-up. If push fails (rejected, no upstream, network), report the failure and stop — do NOT force-push, do NOT retry blindly, do NOT amend.
6. Show commit and push result
7. **Update Trello card** (if one is assigned to the session) — see Trello Sync below

**Everything happens in one continuous response. Stage, commit, and push are always a single sequence.**

---

## Summary Table Format

**Output as actual markdown (not in a code block):**

| File | Type | Description |
|------|------|-------------|
| `path/to/file.php` | ✏️ M | Brief description |
| `path/to/new.ts` | ➕ A | Brief description |
| `path/to/old.vue` | 🗑️ D | Why removed |

## Overview Format

2-3 sentences covering:
- What feature/fix/refactor was implemented
- Why these changes were made

---

## Trello Sync

**Only runs if a Trello card is assigned to the session.** If no card, skip this entirely.

After every commit:

1. **Check off completed items** — Mark any Acceptance Criteria, Implementation Phases, and Progress checklist items that this commit satisfies
2. **Post a commit comment** linking the commit SHA to what was completed:
   ```
   ## Phase N Commit

   **Commit:** <sha>
   **Completed:** [list of checklist items checked off]
   ```
3. **Move the card to the correct column** based on current state:
   - Still has remaining phases → keep in **In Progress**
   - All phases done, all acceptance criteria met → move to **Done** (position: `"top"`) with retro comment
   - Never move to Done prematurely — only when ALL work is complete

**Do NOT move to Done just because a commit happened.** The card moves to Done only when every acceptance criteria item and every progress item is checked off.

4. **Update parent epic** (phase cards only) — If the card name contains `>` (phase card pattern like `Epic > Phase N`), fetch the parent epic card linked in the description and perform the full phase handoff:

   **a. Check off epic items:** Mark the completed phase on the Implementation Phases checklist. Also check off any epic-level Acceptance Criteria items that this phase satisfies — epic AC items map to specific phases and must be marked complete as the work is verified, not deferred until the epic is fully done.

   **b. Post a Phase Handoff comment** on the epic card. This is the bridge between agents — it ensures no knowledge is lost when context is destroyed. Include:
   - What was built and committed (commit SHA)
   - Discoveries that affect remaining phases (bugs found, assumptions invalidated, new constraints)
   - Corrections to the epic description or remaining phase cards if anything is wrong or outdated
   - Technical context the next agent will need (e.g., timing constraints, reusable helpers, gotchas)

   **c. Re-read the epic description and remaining phase cards.** If anything is wrong, outdated, or missing context from what you learned during this phase, update the card descriptions now. The epic must always be zero-context ready for the next agent.

   **d. Update the next phase card.** Find the next incomplete phase card in In Progress. Post a "Notes from Phase N" comment with anything that could cause the next agent to waste time or make mistakes: discovered constraints, timing gotchas, reusable helpers and their paths, cost/budget observations, dependencies between phases. The next agent has ZERO context — it reads only the card description and comments.

   **e. Check if epic is complete.** If ALL phase items on the epic's checklist are done, move the epic to Done (position: `"top"`) with a retro comment summarizing all phases and their commits. Do not leave the epic in In Progress or ToDo when all phases are Done.

---

## Continue the Pipeline

**After Trello sync, immediately invoke `/flow-report`.** The pipeline is automatic — do not pause, do not wait for user input, do not treat the commit as the end of the workflow. The commit is step 4 of 5. `/flow-report` is step 5.

---

## Rules

- **NEVER use `git add .` or `git add -A`** - Always stage specific files by name
- **NEVER include unrelated files** - Only stage files from your session work
- **NEVER skip the summary table** - Users need to see what's being committed
- **ALWAYS push to remote** after every successful commit — this is the default, not an exception
- **NEVER force-push** (`--force`, `--force-with-lease`) unless explicitly asked
- **NEVER use `--amend`** unless explicitly asked
- **NEVER skip pre-commit hooks**
- **ALWAYS use HEREDOC** for commit messages to preserve formatting
- **Use imperative mood**: "Add feature" not "Added feature"
- **Keep summary under 70 characters**
