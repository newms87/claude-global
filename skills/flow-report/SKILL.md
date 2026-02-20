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

**Keep it concise.** Include:

- **Accomplished** — Bulleted list: 1-2 bullet summary of the feature/fix/refactor
- **Files changed** — Table with columns: File, Type (✏️ M / ➕ A / 🗑️ D), Description
- **Test results** — Table with columns: Suite, Passed, Failed, Status (✅/❌). Only include if tests were run.
- **Pre-existing issues** — Bulleted list of issues flagged by reviewers that are outside your scope. Omit section if none.
- **Next step** — Bulleted list: what comes next (next phase name, or "Done" if all phases complete)

## Rules

- **Be concise.** This is a status update, not documentation.
- **Never repeat the full commit message.** Summarize in your own words.
- **Always state the next step.** The user needs to know if there's more work or if they should review and approve.
- **If working in phases**, reference the phase number and name for both completed and upcoming work.
