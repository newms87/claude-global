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

1. **Is the file in my diff?** If yes → fix it. "Pre-existing" is not a valid skip reason. **Never use `git stash` or `git checkout` to check if a failure is pre-existing** — other agents and the user are actively modifying files in this repo, and stash/checkout will destroy their uncommitted work. The proof is also irrelevant: pre-existing or not, you own it. Investigate the code, not the history.
2. **Did a reviewer flag it?** If yes → fix it. Reviewers don't flag things for fun.
3. **Am I calling it "out of scope"?** That's not a valid category. There is no scope boundary.
4. **Am I saying "it would take too long"?** Your effort estimates are systematically wrong — divide by 10.
5. **Am I saying "it needs its own card/ticket"?** No. If the reviewer flagged it now, fix it now.
6. **Am I saying "it's a separate refactoring effort"?** No. It's THIS effort.
7. **Am I saying "I'll flag it for later"?** There is no later. Later means never.
8. **Am I saying "it's a coverage improvement, not a bug"?** Test gaps are mandatory. Not a bug ≠ not required.
9. **Am I saying "the migration only touched N lines"?** Irrelevant. File is in diff + reviewer flagged it = fix it.

### Every Finding Is Your Responsibility

It does not matter:
- Whether the issue is "pre-existing" or newly introduced
- Whether you caused it or someone else did months ago
- Whether it relates to your current task or not
- Whether fixing it requires significant additional work
- Whether the file was only "lightly touched" in your diff

**If a reviewer flagged it, you own it. Period.** Do not rationalize, argue, qualify, or logic your way out of it. Do not add caveats like "but only for targeted edits" or "but the size was pre-existing." The default action is: **IMMEDIATELY implement the correction.**

### The Only 3 Valid Skip Reasons

To skip a finding, you MUST choose exactly one of these reasons and explain it in ONE sentence. **All other reasons are invalid — implement the fix immediately.**

| # | Reason | Required Proof | NOT Valid |
|---|--------|---------------|-----------|
| 1 | **Another agent is actively working on it** | Show which untracked/staged files prove another agent is mid-edit in that domain | "Someone else should do this" |
| 2 | **Adds zero value to codebase quality** | The change would not improve readability, maintainability, correctness, OR test coverage — not even slightly | "It's a one-liner," "it tests framework behavior," "it would only test mock wiring" |
| 3 | **The correction would be wrong** | Applying the fix would introduce a bug or break behavior | "Splitting would scatter logic," "the file is cohesive," "I prefer the current architecture" |

**Tightened definitions:**
- **"Zero value" means LITERALLY zero.** If the change improves ANY aspect of quality — even marginally — it has value. "Low value" is not "zero value." A test for a one-liner still verifies it doesn't break. A docblock on a small method still helps the next reader.
- **"Would be wrong" means introduces a defect.** Architectural preferences, cohesion arguments, and "I don't think splitting helps" are not defects. If the code would still work correctly after the fix, the fix is not wrong. **"Would be wrong" does NOT mean "would be hard," "would be large," or "would be risky."** If the fix is just big, that's an effort complaint — not a correctness concern.
- **Cost and time are NEVER factors.** "Too many mocks," "would take too long," "significant refactor" are effort complaints, not skip reasons. The mission is 100% perfect quality code. There is no budget. There is no deadline.

**If your skip reason is longer than one sentence, you are rationalizing.** Go fix it.

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

- **All findings addressed, all skips justified by the 3 valid reasons above** → Proceed to `/flow-commit`
- **Any finding skipped for an invalid reason** → Go back and fix it before proceeding

---

## Rules

- **This step is NOT optional.** Skipping it is a pipeline violation.
- **Be honest with yourself.** The whole point is catching your own rationalizations.
- **The table in Step 1 is required output.** Show it so the user can see your decision-making.
- **Speed is not a factor.** Taking 2 extra minutes to fix a finding is always cheaper than shipping a skip.
