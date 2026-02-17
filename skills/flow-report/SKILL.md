---
name: flow-report
description: Present results to the user after a commit. Concise summary of what was done.
---

# Report Results

Present a concise summary of what was accomplished after committing. The user reviews details via git — this is just the high-level overview.

---

## Steps

1. Run `git show --stat HEAD` to get the files changed in the most recent commit
2. Output the report (see format below)

## Report Format

**Keep it to 5-10 lines max.** Include:

- **What was accomplished** — 1-2 sentence summary of the feature/fix/refactor
- **Files changed** — From `git show --stat`, formatted as a compact list
- **Test results** — If tests were run, mention pass/fail status and count
- **Next step** — What comes next (next phase name, or "Done" if all phases complete)

## Rules

- **Be concise.** This is a status update, not documentation.
- **Never repeat the full commit message.** Summarize in your own words.
- **Always state the next step.** The user needs to know if there's more work or if they should review and approve.
- **If working in phases**, reference the phase number and name for both completed and upcoming work.
