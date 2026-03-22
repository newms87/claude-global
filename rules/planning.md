# Planning Rules

## CRITICAL: Trello Card Overrides Plan Mode

**When a Trello card is assigned to the session, NEVER use EnterPlanMode.** The card IS the plan. Update the card description instead. This rule supersedes ALL triggers below (multi-file changes, architectural decisions, etc.). "make it so" from the user means implement NOW.

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

## CRITICAL: Specify Refactoring/Renaming Tools in Plans

**When a plan involves renaming or moving classes, files, or symbols across multiple references, the plan MUST specify which refactoring tool to use.** Consult `~/.claude/rules/refactoring.md` for available tools.

- **PHP class renames/moves:** Use `phpactor class:move` — updates namespace, class declaration, and all references automatically
- **TypeScript/JavaScript:** Use IDE refactoring or `ts-morph`
- **Frontend bulk string renames:** Use batch-editor agents

**Never plan a rename phase as "rename X to Y across N files" without naming the tool.** Manual find-and-replace across dozens of files is error-prone and wasteful when refactoring tools exist. The tool choice is part of the plan, not an implementation detail.

## Zero-Context Test

**Write plans as if you have amnesia.** The plan must be executable with zero memory of prior conversation.

For each task, include:
- **Exact file paths** being modified
- **Specific method/class names** (not "the scope methods")
- **What changes** in plain language
- **Why** if non-obvious

## CRITICAL: Complete ALL Planned Work or Stop

**When the user discusses a multi-part implementation strategy, EVERY part must be implemented.** Do not commit or push until all discussed items are done.

**Before starting implementation, create a checklist** of everything discussed. Track each item. Before committing, verify ALL items are checked off. If ANY item is not done:

1. **STOP immediately** — do not commit partial work
2. **Tell the user explicitly** what was NOT implemented
3. **Wait for confirmation** before proceeding

**NEVER silently drop parts of a discussed plan.** The user assumes everything discussed will be implemented. Committing partial work without disclosure is worse than not starting — it creates false confidence that the work is done.

This applies equally to:
- Performance optimizations discussed alongside architectural changes
- Data-layer changes discussed alongside orchestration changes
- Any part of a strategy the user explicitly described

**If the work is too large for one commit, say so upfront** — break it into explicit phases with the user's approval. Do not unilaterally decide which parts to defer.

## CRITICAL: Never Check Off Work That Isn't Done

**Before marking ANY checklist item complete, re-read the item text and verify the literal words are true.** "Delete X" means X is deleted from the codebase — not that you worked around it. "Eliminate pattern Y" means Y no longer exists — not that you patched its callers. If the item says to do something and you didn't do it, the item is not complete.

Marking incomplete work as complete is worse than not doing it — it hides the gap from the user and future agents. It creates false confidence that the work is done and prevents anyone from catching the omission.

**Before committing:** Re-read every acceptance criteria item you checked off. For each one, ask: "If someone grepped the codebase right now, would the literal claim in this item be true?" If not, uncheck it and either fix it or tell the user it's not done.

## Identify Shared Abstractions Explicitly

**When a plan involves multiple classes that will share logic, name the shared abstraction and its location in the plan.**

Before writing per-class tasks, add a "Shared Abstractions" section that identifies:
- What logic is shared (e.g., "field type resolution", "schema building helpers")
- Where it lives (e.g., "SchemaFieldHelper trait", "new BaseExtractionService")
- Which classes consume it

This is critical for multi-session work. Context compaction loses the "these two services share logic" insight. Making it explicit in the plan ensures every continuation session knows to use the shared location instead of reinlining.

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
3. **`/flow-quality-check`** — audit decisions, catch rationalizations
4. **`/flow-verify`** — verify tests, docs, and demos are complete (project-level gate, if available)
5. **`/flow-commit`** — stage and commit once all gates pass
6. **`/flow-self-improvement`** — process notes, update docs if warranted
7. **Mark phase complete** in the plan
8. **Immediately proceed to next phase** — repeat steps 1–8
9. **`/flow-report`** — present what was accomplished (run once after all phases complete)

### CRITICAL: The Pipeline Is Fully Automatic

**Steps 1–8 execute without stopping.** After implementing code, IMMEDIATELY invoke `/flow-code-review`, then `/flow-quality-check`, then `/flow-verify` (if the project provides it), then `/flow-commit`, then `/flow-self-improvement`. Then immediately start the next phase. Continue until ALL phases are complete. `/flow-report` runs once at the very end, after all phases finish.

The `/flow-*` skills are pipeline stages you execute via the Skill tool — they are NOT user-invoked commands you wait for. The user reviews your work via git history and the `/flow-report` output. Do NOT pause and ask "ready for code review?" or "should I proceed to the next phase?" — just execute.

**Stopping after implementation without running quality gates is a workflow violation.** "Ready for code review when you'd like" is WRONG — just run it.

**Stopping between phases to ask for approval is a workflow violation.** The plan was already approved. Execute it fully.

**User feedback during planning does NOT reset the approval.** Once the user says to start, the plan is approved. Design discussion, mid-implementation corrections, and AC changes are all part of normal execution — none of them require re-approval before running quality gates.

### When to Confirm vs. When to Proceed

- **BEFORE implementation:** If user gives non-trivial feedback that changes the plan, confirm you understand before implementing. If the feedback is a minor/obvious course correction, just proceed.
- **AFTER implementation:** Immediately run the pipeline. No pauses. No permission checks. The only thing that stops the pipeline is the user explicitly saying "stop" or "wait."

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

## Questions Are Not Decisions

**When the user asks a question about the plan, DO NOT edit the plan.** Questions are for discussion — the user is exploring options, not giving instructions.

1. Answer the question
2. Confirm what change (if any) the user wants
3. Only edit the plan after explicit agreement

Editing the plan based on your own interpretation of a question is a unilateral decision. Wait for the user to tell you what to do.

## "Review the Plan" Means ExitPlanMode

**When the user says "review the plan," call `ExitPlanMode` immediately.** That is how the user reviews, accepts, or rejects the plan — via the plan approval UI.

Never ask the user directly if they accept the plan. Never use `AskUserQuestion` for plan approval. Always use `ExitPlanMode`.

## Trust Agent Results

**Do not re-verify agent findings during planning.** Agent results are trustworthy. Write the plan directly from their output. Verification happens during implementation — if a finding turns out to be wrong, adjust then.
