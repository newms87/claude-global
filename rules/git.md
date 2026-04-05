# Git Operations

## CRITICAL: Never Delete a Repository

NEVER run `rm -r`, `rm -rf`, or ANY deletion command on a repo directory. Repos contain irreplaceable local state: `.env` files with credentials, uncommitted work, local config. Deleting is permanent — re-cloning doesn't recover gitignored files or session work.

If a hook blocks `rm -rf`, the hook is correct. Never bypass it with alternative commands. Ask the user instead.

## Never Create Branches

Commit directly to main. Other agents share the working tree. Branches disrupt their work and are pointless overhead when committing to main.

## Commit Message Format

```
[Task Name] Phase N: Short title

Body explaining what changed and why.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Omit "Phase N" for non-phased work.

## Always Use /flow-commit

Never manually run `git add` + `git commit`. Always invoke `/flow-commit` via Skill tool (except amending a previous commit to fix a hook failure). `/flow-commit` handles staging, committing, Trello lifecycle, and summary output. Manual commits bypass all of this.

## Check for Other Agents' Staged Work

Before committing, run `git status` to check for already-staged files you didn't create. If found, another agent may be mid-commit. Poll every 5 seconds, up to 30 seconds. If staged files persist, ask the user.

Never commit on top of another agent's staged work. Never unstage their files.

## Never Reset or Remove Other Changes

NEVER use `git reset`. When committing, stage ONLY your changes (`git add <specific-files>`). Never reset the staging area. Never unstage already-staged files.

## Never Use git stash

Forbidden. No exceptions. To understand a failure, investigate the code itself. Stashing destroys uncommitted work and can corrupt multi-agent sessions.

## Never Use git checkout, git restore, or git revert

NEVER use these to undo changes. This includes `cp` from clean source, `git show HEAD:file > file`, or Write tool with original content — any mechanism that overwrites a file wholesale. Files may contain user changes mixed with yours; wholesale replacement destroys user work.

Instead: Run `git diff`, identify YOUR specific changes, use Edit to remove only those. Preserve all user and other agent changes. If unsure what's yours, ask the user.

## Git Operations Allowed

**Read-only:** `git status`, `git diff`, `git log` (anytime)

**Via pipeline:** `git add` + `git commit` when executing `/flow-commit` (automatically allowed)

**Otherwise:** Not allowed without explicit user request
