# Planning Rules

## NEVER Create Plan Files Directly

**Plan files are ONLY created by the system when you use `EnterPlanMode`.** This is a blocking rule.

**FORBIDDEN — no exceptions:**
- `mkdir .claude/plans/`
- `Write` to any `.claude/plans/` path
- Creating plan files via any tool (Bash, Write, Edit on a new file)
- Creating plan-like documents anywhere else in the project

**If you need a plan:** Use `EnterPlanMode`. The system creates the file. You edit it in plan mode. That is the ONE way.

## Plan File is Sacred - NEVER Overwrite

**The plan file is a persistent document spanning multiple sessions. NEVER erase it.**

### Editing the Plan File

In plan mode, you edit the plan file using the `Edit` tool. **NEVER use `Write` tool** - it replaces the entire file and destroys all existing content.

### Code Reviews Go IN the Current Phase

When doing a code review for a phase:
- Find the current phase section in the plan
- Add findings **at the end of that phase**, before the next phase
- Do NOT create a separate "Code Review" document
- Do NOT replace the entire plan with review findings

## Plans Are Prose - NEVER Code

**CRITICAL: Plan files must contain ZERO code blocks.** This is a blocking rule.

### What Is Forbidden

- Vue/React templates
- TypeScript/JavaScript (including interfaces)
- PHP, Python, or any programming language
- CSS/SCSS
- Config files
- "Example" snippets to "help clarify"

### Why This Rule Exists

- **Code in plans is never executed** - it's pure waste
- **Users scan plans quickly** - code blocks slow reading and hide the actual plan
- **Premature implementation** - writing code locks in details before the user approves the approach
- **Forces clear thinking** - if you can't describe it in prose, you don't understand it yet

### What To Write Instead

Describe behavior in plain language:
- "The component accepts width and height props. Numbers become viewport units, strings pass through as-is."
- "The dialog exposes open() and close() methods for parent components to call."
- "Clicking the confirm button emits a confirm event and shows a loading spinner when isSaving is true."

## Zero-Context Test

**Write plans as if you have amnesia.** The plan must be executable with zero memory of prior conversation.

For each task, include:
- **Exact file paths** being modified
- **Specific method/class names** (not "the scope methods")
- **What changes** in plain language
- **Why** if non-obvious

## Phase-by-Phase Development (Default Mode)

**All multi-step features MUST use phase-by-phase development:**

1. **Create a plan** with numbered phases (Phase 0, Phase 1, etc.)
2. **Complete one phase at a time** - implement, test, validate
3. **STOP and report results** - present what was accomplished to the user
4. **Wait for user validation and commit** - NEVER proceed without explicit approval
5. **Mark phase complete** with brief summary of what was accomplished
6. **Plan the next phase** before starting implementation
7. **Move to next phase** only after steps 3-6 are complete

**CRITICAL: NEVER autonomously move to the next phase.** Even if the next phase is a single line of code, you MUST stop after completing the current phase, commit, and plan before starting the next one.

**Phase completion format:**
```markdown
## Phase N: Name ✅ COMPLETE

**Accomplished:** One sentence summary.

**Files:** Comma-separated list of key files created/modified.
```

## Trust Agent Results

**Do not re-verify agent findings during planning.** Agent results are trustworthy. Write the plan directly from their output. Verification happens during implementation — if a finding turns out to be wrong, adjust then.
