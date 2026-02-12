---
name: commit
description: Stage and commit changes. Use "/commit now" for instant commit, or "/commit" to see summary while commit runs.
---

# Commit Workflow

This skill supports two modes based on arguments.

---

## Mode 1: Instant Commit (`/commit now`)

When the user includes "now" in the command, perform everything in a single response:

1. Run `git status` and `git diff --name-only` to identify changed files
2. Output the **Summary Table** and **Overview** (see format below)
3. Immediately run a single chained command: `git add <file1> <file2> ... && git commit -m "..."`
4. Show commit result

**No stopping, no confirmation - one continuous response.**

---

## Mode 2: Standard Commit (`/commit`)

### Step 1: Stage and Summarize (parallel)

Run these in parallel:
- **Bash:** `git add <file1> <file2> ...` (stage only YOUR session's files)
- **Output:** Summary Table + Overview (see format below)

### Step 2: Commit Immediately

After `git add` succeeds, immediately run the commit. NEVER ask "Ready to commit?" — `/commit` IS the confirmation.

```bash
git commit -m "$(cat <<'EOF'
Brief summary in imperative mood

- Key change 1
- Key change 2

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

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
