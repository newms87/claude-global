# Git Operations

## CRITICAL: NEVER Delete a Repository — ZERO EXCEPTIONS

**NEVER run `rm -r`, `rm -rf`, or ANY deletion command on a repository directory. Not a clone, not a symlink target, not a "temporary" copy. NEVER. There is NO scenario where this is acceptable.**

A repository is not "just code from GitHub." It contains:
- **`.env` files** with database credentials, API keys, passwords — GONE FOREVER if deleted
- **Uncommitted work** — hours of local changes that exist NOWHERE else
- **Local configuration** — IDE settings, auth tokens, cached data
- **Files you created this session** — if you wrote files into a repo and didn't commit them, deleting the repo destroys YOUR OWN WORK

**"I'll just re-clone it" is NOT a recovery plan.** Re-cloning gets you the committed code. It does NOT get back `.env` files, uncommitted changes, local config, or anything in `.gitignore`. Those are gone permanently. There is no undo.

**"It's just a fresh clone" is a LIE you tell yourself.** You may have written files into it 5 minutes ago. You may have forgotten. The `.env` was there before you started. You do not have perfect memory of every file in every directory. Assume every repository contains irreplaceable local state, because it almost certainly does.

**If a hook blocks `rm -rf`, that is the hook SAVING YOU from a catastrophic mistake.** Do NOT try `rm -r` instead. Do NOT try `find -delete`. Do NOT try any alternative that achieves the same outcome. The hook blocked it because it is DANGEROUS. Stop. Think. Ask the user.

**If you need to replace a directory with a symlink:** Ask the user to do it. You do not have the judgment to decide what is safe to delete.

## CRITICAL: Never Create Branches

**Commit directly to main. Never run `git checkout -b` or `git branch`.** Other agents share the same working tree. Switching branches disrupts their in-progress work. Creating a branch just to immediately merge it back is pointless overhead — commit straight to main.

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

## CRITICAL: Always Use /flow-commit

**Never manually run `git add` + `git commit`. Always invoke `/flow-commit` via the Skill tool.** The only exception is amending a previous commit (e.g., fixing a hook failure).

`/flow-commit` handles staging, committing, Trello card lifecycle (Progress checklist updates, retro comments, move to Done), and summary output. Manual commits bypass all of this.

**Outside of the pipeline workflow**, never stage or commit without explicit user instruction.

## CRITICAL: Check for Other Agents' Staged Work

**Before committing, check `git status` for already-staged files that are NOT yours.**

If you see staged changes you didn't make, another agent is likely mid-commit:

1. Poll `git status` every 5 seconds, up to 30 seconds
2. If the staged files clear (the other agent committed), proceed with your commit
3. If they persist after 30 seconds, ask the user

**NEVER commit on top of another agent's staged work.** NEVER unstage their files.

## CRITICAL: Never Reset or Remove Other Changes

**NEVER use `git reset` or any command that would unstage or remove changes made by other agents or the user.**

When committing:
1. Stage ONLY your new changes (use `git add <specific-files>`)
2. NEVER reset the staging area
3. NEVER unstage files that were already staged
4. Commit everything that is staged together

## Git Write Operations

### Always allowed (read-only):
- `git status` - Check current state
- `git diff` - View changes
- `git log` - View history

### Allowed automatically via pipeline:
- `git add` + `git commit` — When executing `/flow-commit` as part of the development pipeline (see "Auto-Commit After Quality Gates" above). The pipeline auto-commits after quality gates pass.

### Not allowed without explicit user request:
- `git add` + `git commit` — Outside the pipeline workflow
- `git push` - Pushing to remote
- `git checkout` - Switching branches or reverting
- `git revert` - Reverting commits
- `git reset` - Resetting staging area or commits
- `git stash` - Stashing changes (see below)

## NEVER Use `git stash`

**`git stash` is forbidden. No exceptions.**

The typical temptation is using `git stash` to check whether a test/lint failure existed before your changes. This is the wrong approach because **it does not matter whether you caused the failure or not.**

When you encounter a failure, there is only one outcome: **fix it.** You own the entire codebase. It does not matter who caused the failure.

To understand the failure: investigate the code itself. Read it, understand what's failing, and trace the cause. That tells you everything `git stash` would, without the risk of destroying work.

**Why `git stash` is destructive:** It removes all uncommitted changes from the working tree. If multiple agents are working, or the user has in-progress edits, stashing can lose or corrupt that work.

## CRITICAL: Reverting Changes - NEVER Use Git Commands

**NEVER use `git checkout`, `git restore`, or `git revert` to undo changes. No exceptions — not even when asked to "undo" or "revert" quickly.**

**This includes ANY command that achieves the same result:** `cp` from a clean source, `git show HEAD:file > file`, Write tool with original content, bash redirection, or any other mechanism that overwrites the working file wholesale. The rule is about the **outcome** (replacing a file's contents entirely), not the specific command. If a dozen different commands can destroy work, all dozen are forbidden.

**If a hook blocks a command, the hook is correct.** Follow the safe alternative below. NEVER find a different command that bypasses the hook to achieve the same blocked outcome. Circumventing a safety hook is a critical violation — worse than the original mistake, because it proves you understood the danger and proceeded anyway.

### Why:
Files may contain user changes mixed with yours. Any wholesale replacement blindly reverts EVERYTHING, destroying user work. Time pressure is not an excuse — this is when the rule matters most.

### Correct revert process:
1. Run `git diff` on each file to see exactly what changed
2. Identify YOUR specific changes
3. Use Edit to remove ONLY your changes
4. Preserve all user and other agent changes

**If unsure what's yours vs theirs:** Ask the user, never guess.
