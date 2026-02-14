---
name: next-phase
description: Complete the current phase and advance to the next one. Syncs Trello, commits, and condenses the plan.
---

# Next Phase Workflow

Complete the current plan phase and prepare for the next one. Performs three steps in order.

**CRITICAL: Steps 1 and 2 happen BEFORE entering plan mode.** Commit and sync first, then enter plan mode to condense. If you are already in plan mode when `/next-phase` is invoked, you can still run Trello sync and git commit — plan mode does not prevent these operations. Do them first, then proceed to Step 3.

## Step 1: Trello Sync (if card present)

Read the plan file for a `**Trello Card:**` reference line with a Card ID.

**If a card ID exists:**
1. Fetch the card's "Implementation Phases" checklist using `get_checklist_by_name` with the card ID
2. **If the checklist doesn't exist yet**, create it using `create_checklist` with name "Implementation Phases" and the card ID, then add one item per phase from the plan using `add_checklist_item`
3. Find the checklist item matching the current phase name
4. Mark it complete using `update_checklist_item` with `state: "complete"`
5. If any Trello call fails, note it and continue — never block on Trello

**If no card reference:** Skip this step silently.

## Step 2: Commit

Run `git status` and `git diff --name-only` to identify changed files. Then commit in a single chained command:

```
git add <file1> <file2> ... && git commit -m "$(cat <<'EOF'
Phase N: Brief description of what was accomplished

- Key change 1
- Key change 2

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**Rules:**
- **NEVER use `git add .` or `git add -A`** — stage specific files only
- Use the phase number and name in the commit message subject
- Use HEREDOC for the commit message

## Step 3: Condense Plan

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

After all three steps, display:

1. Trello sync result (if applicable)
2. Commit hash and message
3. Brief statement of what the next phase is and whether you found any ambiguities that need discussion before starting
