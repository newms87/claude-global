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

## Phase-by-Phase Development (Default Mode)

**All multi-step features MUST use phase-by-phase development:**

1. **Create a plan** with numbered phases (Phase 0, Phase 1, etc.)
2. **Implement the phase** — write the code
3. **Quality gates** — test coverage + code review (see timing below)
4. **Auto-commit** — once quality gates pass, commit immediately (`git add ... && git commit` in one command). User reviews via git.
5. **STOP and report results** — present what was accomplished to the user
6. **Wait for user approval** — NEVER proceed to next phase without explicit approval
7. **Mark phase complete** with brief summary of what was accomplished
8. **Self-improvement** — reflect on the session and update docs if an obvious efficiency win was missed (see `self-improvement.md`)
9. **Move to next phase** only after steps 2-8 are complete

### Quality Gate Timing

- **Independent phases** (different domains, separate concerns): Run test coverage + code review after each phase.
- **Related phases** (same domain, building on each other): Implement all related phases first, then run test coverage + code review once on the combined work.

Use judgment. If phases 1-3 all modify the same component tree, writing tests after each phase wastes effort since later phases may change the code. Group them and test the final result.

**CRITICAL: NEVER autonomously move to the next phase.** Even if the next phase is a single line of code, you MUST stop after completing the current phase, commit, and plan before starting the next one.

**CRITICAL: Quality gates are NOT optional.** Test coverage and code review MUST run before presenting results to the user. Skipping them — even "planning to do them later" — is a workflow violation. Grouping related phases doesn't mean skipping — it means running quality gates on the group.

**Phase completion format:**
```markdown
## Phase N: Name ✅ COMPLETE

**Accomplished:** One sentence summary.

**Files:** Comma-separated list of key files created/modified.
```

## Trust Agent Results

**Do not re-verify agent findings during planning.** Agent results are trustworthy. Write the plan directly from their output. Verification happens during implementation — if a finding turns out to be wrong, adjust then.
