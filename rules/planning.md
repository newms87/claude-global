# Planning Rules

## NEVER Create Plan Files Directly

**Plan files are ONLY created by the system when you use `EnterPlanMode`.** This is a blocking rule.

**FORBIDDEN — no exceptions:**
- `mkdir .claude/plans/`
- `Write` to any `.claude/plans/` path
- Creating plan files via any tool (Bash, Write, Edit on a new file)
- Creating plan-like documents anywhere else in the project

**If you need a plan:** Use `EnterPlanMode`. The system creates the file. You edit it in plan mode. That is the ONE way.

## Plan Files Live in ~/.claude/plans/

**Plan files are in the user's home directory (`~/.claude/plans/`), NOT in the project's `.claude/plans/`.** Never glob or search for plan files — their absolute path is always provided by the system in plan mode context. Use that path directly.

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

## When to Use Phases

**Only break work into phases when the scope exceeds a single pipeline run.** Small-to-medium tasks (single domain, a few files) should be one phase. Use multiple phases when:

- Work spans distinct domains that benefit from separate commits
- The scope is large enough that reviewing everything at once would be unwieldy
- There are natural checkpoints where the codebase should be in a working state

**Do NOT create phases for the sake of granularity.** If the work can be implemented, reviewed, and committed as one unit, it should be.

## The Pipeline (Per Phase)

**Every phase runs the FULL pipeline automatically. No pauses, no waiting.**

1. **Implement** — write the code
2. **`/flow-code-review`** — run reviewer agents, fix findings
3. **`/flow-commit`** — stage and commit once quality gates pass
4. **`/flow-report`** — present what was accomplished
5. **`/flow-self-improvement`** — process notes, update docs if warranted
6. **Mark phase complete** in the plan
7. **Immediately proceed to next phase** — repeat steps 1–6

### CRITICAL: The Pipeline Is Fully Automatic

**Steps 1–7 execute without stopping.** After implementing code, IMMEDIATELY invoke `/flow-code-review`, then `/flow-commit`, then `/flow-report`, then `/flow-self-improvement`. Then immediately start the next phase. Continue until ALL phases are complete.

The `/flow-*` skills are pipeline stages you execute via the Skill tool — they are NOT user-invoked commands you wait for. The user reviews your work via git history and the `/flow-report` output. Do NOT pause and ask "ready for code review?" or "should I proceed to the next phase?" — just execute.

**Stopping after implementation without running quality gates is a workflow violation.** "Ready for code review when you'd like" is WRONG — just run it.

**Stopping between phases to ask for approval is a workflow violation.** The plan was already approved. Execute it fully.

### Quality Gate Timing

- **Independent phases** (different domains, separate concerns): Run the full pipeline after each phase.
- **Related phases** (same domain, building on each other): Implement all related phases first, then run the pipeline once on the combined work.

Use judgment. If phases 1-3 all modify the same component tree, writing tests after each phase wastes effort since later phases may change the code. Group them and test the final result.

**CRITICAL: Quality gates are NOT optional.** Test coverage and code review MUST run before committing. Skipping them — even "planning to do them later" — is a workflow violation. Grouping related phases doesn't mean skipping — it means running quality gates on the group.

**Phase completion format:**
```markdown
## Phase N: Name ✅ COMPLETE

**Accomplished:** One sentence summary.

**Files:** Comma-separated list of key files created/modified.
```

## Trust Agent Results

**Do not re-verify agent findings during planning.** Agent results are trustworthy. Write the plan directly from their output. Verification happens during implementation — if a finding turns out to be wrong, adjust then.
