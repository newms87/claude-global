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
5. Show commit result
6. **Update Trello card** (if one is assigned to the session) — see Trello Sync below

**Everything happens in one continuous response. Stage and commit are always a single command.**

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
   - All phases done, all acceptance criteria met → move to **Done** with retro comment
   - Never move to Done prematurely — only when ALL work is complete

**Do NOT move to Done just because a commit happened.** The card moves to Done only when every acceptance criteria item and every progress item is checked off.

---

## Rules

- **NEVER use `git add .` or `git add -A`** - Always stage specific files by name
- **NEVER include unrelated files** - Only stage files from your session work
- **NEVER skip the summary table** - Users need to see what's being committed
- **NEVER push to remote** unless explicitly asked
- **NEVER use `--amend`** unless explicitly asked
- **NEVER skip pre-commit hooks**
- **ALWAYS use HEREDOC** for commit messages to preserve formatting
- **Use imperative mood**: "Add feature" not "Added feature"
- **Keep summary under 70 characters**
