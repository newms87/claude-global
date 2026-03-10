---
name: next-phase
description: Complete the current phase and advance to the next one. Commits via /flow-commit and condenses the plan.
---

# Next Phase Workflow

Complete the current plan phase and prepare for the next one. Performs two steps in order.

**CRITICAL: Step 1 happens BEFORE entering plan mode.** Commit first, then enter plan mode to condense. If you are already in plan mode when `/next-phase` is invoked, you can still run `/flow-commit` — plan mode does not prevent this. Do it first, then proceed to Step 2.

## Step 1: Commit

Invoke `/flow-commit`. This handles staging, committing, and Trello sync (checking off items, posting commit comment, moving card if all work is done).

## Step 2: Condense Plan

**Now enter plan mode** using `EnterPlanMode`. Plan mode provides the plan file path and the correct tools for reading/writing it. Never search for or create plan files manually.

Edit the plan file to shift focus from completed work to upcoming work:

**For the just-completed phase:**
- Replace the detailed task list with a brief completion summary (2-3 lines max)
- Format: `## Phase N: Name ✅ COMPLETE\n\n**Accomplished:** One sentence summary.\n\n**Files:** Comma-separated list of key files created/modified.`
- Remove all detailed sub-steps, bullet points, and file tables — they're in git history now

**For the next phase:**
- Read any files referenced in the next phase that you haven't read yet
- If any instructions are ambiguous or reference code patterns you need to verify, add brief clarifying notes inline
- Do NOT expand the phase into full implementation detail — just ensure there are no ambiguities that would cause you to stop and ask questions mid-implementation

**Leave all future phases (beyond the next one) untouched.**

## Output

After both steps, display:

1. Commit hash and message (from `/flow-commit` output)
2. Brief statement of what the next phase is and whether you found any ambiguities that need discussion before starting
