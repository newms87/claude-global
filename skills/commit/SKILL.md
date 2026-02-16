---
name: commit
description: Stage and commit changes with a summary table.
---

# Commit Workflow

`/commit` IS the confirmation. Never ask "Ready to commit?" — just do it.

---

## Steps

1. Run `git status` and `git diff --name-only` in parallel to identify changed files
2. **Check for other agents' staged work** — if `git status` shows staged files that are NOT yours, another agent may be mid-commit. Poll `git status` every 5 seconds up to 30 seconds. If the staged files clear (committed by the other agent), proceed. If they persist after 30 seconds, ask the user.
3. Output the **Summary Table** and **Overview** (see format below)
4. Run a single chained command: `git add <file1> <file2> ... && git commit -m "..."`
5. Show commit result

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
