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

Never manually run `git add` + `git commit`. Always invoke `/flow-commit` via Skill tool (except amending a previous commit to fix a hook failure). `/flow-commit` handles staging, committing, pushing, Trello lifecycle, and summary output. Manual commits bypass all of this.

## Always Push After Commit

Every commit is followed by `git push` in the same flow. Push is not optional and is not gated on a separate user request — `/flow-commit` runs it automatically. The only exceptions are:

- **Push fails** (rejected, no upstream, network) — report the failure and stop. Never force-push to recover.
- **User explicitly says "don't push"** for this commit.

Force-push (`--force`, `--force-with-lease`) still requires explicit user authorization — see Git Operations Allowed below.

## Check for Other Agents' Staged Work

Before committing, run `git status` to check for already-staged files you didn't create. If found, another agent may be mid-commit. Poll every 5 seconds, up to 30 seconds. If staged files persist, ask the user.

Never commit on top of another agent's staged work. Never unstage their files.

## Never Reset or Remove Other Changes

NEVER use `git reset`. When committing, stage ONLY your changes (`git add <specific-files>`). Never reset the staging area. Never unstage already-staged files.

## Never Use git stash

Forbidden. No exceptions. To understand a failure, investigate the code itself. Stashing destroys uncommitted work and can corrupt multi-agent sessions.

## Before Deleting Any File: Grep for Consumers First

Before running `rm`, Edit-to-empty, Write-empty-string, or any file removal: **grep the entire source tree** for imports, requires, includes, and textual references to the file. If ANY consumer exists, STOP — either the delete is wrong, or the consumers must be migrated first.

**Never trust a card description or prior agent's note claiming "only used by X" — verify yourself.** A parenthetical "(verify with grep first)" on a delete card is load-bearing, not optional. Skipping the grep and then fixing the broken compile with `git checkout` is the exact failure mode the next section prevents.

Cost of the grep: a few seconds. Cost of an unverified delete that breaks a consumer: either a forbidden `git checkout` recovery (which silently destroys whatever else touched that file between your delete and your recovery) or a broken tree that the user has to clean up.

## ABSOLUTE: Never Use git checkout, git restore, or git revert

NEVER use these to undo changes. This includes `cp` from clean source, `git show HEAD:file > file`, or Write tool with original content — any mechanism that overwrites a file wholesale. Files may contain user changes mixed with yours; wholesale replacement destroys user work.

**This is the single most destructive action you can take.** Other agents and users are actively working on files in this repo. `git checkout <file>` silently destroys ALL their uncommitted work in that file with ZERO recovery. The other agent will not know its work was destroyed. This has caused real damage in production sessions.

**When system notifications say a file was "modified by the user or a linter":** That is another agent or the user doing intentional work. NEVER touch that file. NEVER revert it. NEVER investigate whether the changes are "correct." Assume it is mission-critical work that must not be interrupted.

Instead: Run `git diff`, identify YOUR specific changes, use Edit to remove only those. Preserve all user and other agent changes. If unsure what's yours, ask the user.

### If you deleted a file and now need it back

**This is the most common rationalization path into the forbidden `git checkout`.** The reasoning goes: "I just deleted the file, nothing else could have touched it, restoring from HEAD is harmless." The reasoning is wrong:

1. In a multi-agent working tree you **cannot prove** nothing else touched the file between your delete and your recovery. Another agent may have created a new version of it, or renamed it into place, in the window between `rm` and your `git checkout`.
2. Even if nothing else touched it, taking the shortcut trains the habit. The next time you reach for `git checkout` to recover, the situation will be less benign and you'll take the same shortcut.
3. `git restore` and `git checkout -- <path>` and `git show HEAD:<path>` piped to a file are ALL the same action from this rule's perspective — wholesale overwrite. The rule is not about the command name; it is about the overwrite.

**The only safe recovery is:** stop, tell the user what you deleted and why you now need it back, wait for explicit direction. Do not run any recovery command without the user's action verb.

## CRITICAL: All Code Is Your Code

You wrote 100% of everything in every repo — committed, uncommitted, tracked, untracked. You are the sum of all Claude sessions past and present. There is no "not my change," "pre-existing," "someone else did this," or "out of scope." Every line of code is your responsibility even if you don't have context from the session that wrote it.

**Exception for uncommitted changes:** Another agent (another version of you) may be actively working on uncommitted changes outside your session context. Only commit changes from YOUR current session. When you see uncommitted changes not from this session: acknowledge them, explain what they are, and ask the user what to do — never ignore them, never deflect, and never commit them without explicit instruction.

## Git Operations Allowed

**Read-only:** `git status`, `git diff`, `git log` (anytime)

**Via pipeline:** `git add` + `git commit` + `git push` when executing `/flow-commit` (automatically allowed)

**Force-push, amend, rebase, reset, checkout/restore/revert:** Not allowed without explicit user request

**Otherwise:** Not allowed without explicit user request
