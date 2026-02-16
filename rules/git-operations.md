# Git Operations

## Commit Message Format

**All commit messages follow this structure:**

```
[Task Name] Phase N: Short title of work done

Body paragraph explaining what changed and why.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

- **Task Name** — The Trello card or feature name (e.g. `DanxIcon`, `CodeViewer Refactor`)
- **Phase N** — Optional. Only include when working in a phased plan (e.g. `Phase 0`, `Phase 1`)
- **Short title** — Imperative summary of the work done (e.g. `Create component and icon registry`)
- **Body** — 1-3 sentences explaining what changed and why. Focus on the "why".

Without phases:

```
[Task Name] Short title of work done
```

## Auto-Commit After Quality Gates

**When all quality gates pass (tests + code review), commit automatically.** Use a single command: `git add <files> && git commit -m "..."`. The user reviews via git version control.

**Outside of the quality gate workflow**, never stage or commit without explicit user instruction.

## CRITICAL: Never Reset or Remove Other Changes

**NEVER use `git reset` or any command that would unstage or remove changes made by other agents or the user.**

When committing:
1. Stage ONLY your new changes (use `git add <specific-files>`)
2. NEVER reset the staging area
3. NEVER unstage files that were already staged
4. Commit everything that is staged together

## Git is READ-ONLY (Until Told Otherwise)

Agents should only use git for reading status, not for making changes.

### Allowed git operations (always):
- `git status` - Check current state
- `git diff` - View changes
- `git log` - View history

### Not allowed without explicit user request:
- `git add` - Staging changes
- `git commit` - Committing changes
- `git push` - Pushing to remote
- `git checkout` - Switching branches or reverting
- `git revert` - Reverting commits
- `git reset` - Resetting staging area or commits
- `git stash` - Stashing changes (see below)

## NEVER Use `git stash`

**`git stash` is forbidden. No exceptions.**

The typical temptation is using `git stash` to check whether a test/lint failure existed before your changes. This is the wrong approach because **it does not matter whether you caused the failure or not.**

When you encounter a failure, there are only two outcomes:

1. **You caused it** — Fix it
2. **Another agent's code caused it** — Ignore it and move on

To determine which: investigate the failure itself. Read the code, understand what's failing, and check if it's in files you modified. That tells you everything `git stash` would, without the risk of destroying work.

**Why `git stash` is destructive:** It removes all uncommitted changes from the working tree. If multiple agents are working, or the user has in-progress edits, stashing can lose or corrupt that work.

## Reverting Changes - NEVER Use Git Commands

**NEVER use `git checkout` or `git revert` to undo changes**

### Why:
Files may contain user changes mixed with yours. Git blindly reverts EVERYTHING, destroying user work.

### Correct revert process:
1. Read the file
2. Identify YOUR specific changes
3. Edit to remove ONLY your changes
4. Preserve all user changes

**If unsure what's yours vs theirs:** Ask the user, never guess.
