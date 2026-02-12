---
name: low-context
description: Emergency context preservation. Stops all work and updates the plan with everything the next agent needs to continue.
---

# Low Context Emergency Handoff

**STOP ALL CODE WRITING IMMEDIATELY.** Context window is running low.

## Step 1: Enter Plan Mode

Use `EnterPlanMode` tool now. All context must be captured in the plan file.

## Step 2: Update Plan with Handoff Context

Add a new section at the TOP of the plan file:

```markdown
## Context Window Handoff

**Status:** Work in progress - context window exhausted

### What Was Being Done
[Describe the current task/phase in 2-3 sentences]

### Files Being Modified
- `path/to/file1` - [brief description of changes]
- `path/to/file2` - [brief description of changes]

### Work Completed This Session
- [Completed item 1]
- [Completed item 2]

### Work Remaining
- [ ] [Next step 1]
- [ ] [Next step 2]

### Critical Context
[Any non-obvious decisions, gotchas, or context that would be lost]

### For Next Agent
You are resuming work with an empty context window. Before continuing:
1. Run `git diff` to see all uncommitted changes
2. Read the modified files listed above
3. Review the "Work Remaining" checklist
4. Continue from where the previous agent stopped
```

## Step 3: Capture Everything Important

Include in your handoff:
- Decisions made and why
- Problems encountered and solutions found
- Any test failures or errors being debugged
- Relationships between files being modified
- What was about to be done next

## Step 4: Exit Plan Mode

Use `ExitPlanMode` to save the plan. The next agent (or you with cleared context) will use this plan to continue seamlessly.

## Rules

- **Don't try to finish** - Stop immediately
- **Be specific** - Include exact file paths and line numbers
- **Preserve decisions** - Document why, not just what
- **Include gotchas** - What would trip up the next agent?
