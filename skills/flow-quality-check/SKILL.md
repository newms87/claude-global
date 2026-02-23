---
name: flow-quality-check
description: Post-review decision audit. Validates that all findings are addressed and no rationalizations slipped through.
---

# Quality Check — Decision Audit

**Run this AFTER `/flow-code-review` and BEFORE `/flow-commit`.** This is a mandatory pipeline step that audits your decisions about reviewer findings. Its purpose is to catch rationalizations and skipped findings before they get committed.

---

## Step 1: List Every Finding

Go through each reviewer agent's output (test-reviewer, code-reviewer, architecture-reviewer) and list every finding with its disposition:

| # | Reviewer | Finding | Action | Rationale |
|---|----------|---------|--------|-----------|
| 1 | code | Duplicate createObject() | Fixed | Extracted to trait |
| 2 | arch | Interface naming | **SKIPPED** | "Out of scope" |
| 3 | test | Missing edge case test | Fixed | Added test |

**Every finding must appear in this table.** If a finding isn't listed, it wasn't considered.

## Step 2: Challenge Every Skip

For each finding marked SKIPPED, DEFERRED, or NOT FIXED, run it through this checklist:

### The Rationalization Detector

Ask yourself each question. If ANY answer is "yes", the finding MUST be fixed:

1. **Is the file in my diff?** If yes → fix it. "Pre-existing" is not a valid skip reason.
2. **Did a reviewer flag it?** If yes → fix it. Reviewers don't flag things for fun.
3. **Am I calling it "out of scope"?** That's not a valid category. There is no scope boundary.
4. **Am I saying "it would take too long"?** Your effort estimates are systematically wrong — divide by 10.
5. **Am I saying "it needs its own card/ticket"?** No. If the reviewer flagged it now, fix it now.
6. **Am I saying "it's a separate refactoring effort"?** No. It's THIS effort.
7. **Am I saying "I'll flag it for later"?** There is no later. Later means never.
8. **Am I saying "it's a coverage improvement, not a bug"?** Test gaps are mandatory. Not a bug ≠ not required.
9. **Am I saying "the migration only touched N lines"?** Irrelevant. File is in diff + reviewer flagged it = fix it.

### The Only Valid Skips

A finding can ONLY be skipped if:

1. **Another agent is actively working on the file.** Check: `git status` shows untracked files in the same domain. No untracked files = no exception.
2. **The reviewer is factually wrong.** The reviewer misread the code — explain specifically what they got wrong.

Nothing else qualifies. If your reason doesn't match one of these two, go back and fix the finding.

## Step 3: Challenge Test Coverage

Before committing, verify these test coverage questions:

1. **Did I write tests for every new public method?** If not, why not?
2. **Did I test error/edge cases, not just happy paths?** Validation errors, empty inputs, null values?
3. **Did the test-reviewer flag missing tests?** If yes, did I write ALL of them?
4. **Do my tests verify behavior, not implementation?** Would they still pass after a refactor?
5. **Did I run the relevant test suites and confirm 0 failures?**

## Step 4: Final Gut Check

Before proceeding to `/flow-commit`, answer honestly:

- **Is there any finding I'm hoping the user won't notice I skipped?** If yes, go fix it.
- **Would I be comfortable if the user asked me to explain why I skipped each skipped finding?** If not, go fix it.
- **If I re-ran the reviewers right now, would they find the same issues?** If yes, I haven't finished.

## Step 5: Proceed or Go Back

- **All findings addressed, all skips justified by the two valid reasons above** → Proceed to `/flow-commit`
- **Any finding skipped for an invalid reason** → Go back and fix it before proceeding

---

## Rules

- **This step is NOT optional.** Skipping it is a pipeline violation.
- **Be honest with yourself.** The whole point is catching your own rationalizations.
- **The table in Step 1 is required output.** Show it so the user can see your decision-making.
- **Speed is not a factor.** Taking 2 extra minutes to fix a finding is always cheaper than shipping a skip.
