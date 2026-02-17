---
name: code-review
description: Full refactoring workflow. Runs reviewer agents in parallel, creates a unified plan, then executes.
disable-model-invocation: true
argument-hint: [file-or-directory]
---

# Refactoring Workflow

Follow this workflow to refactor `$ARGUMENTS`:

## Default Scope (No Arguments)

If no target is specified, refactor code related to **your current session's work**:

1. Recall which files you worked on during this session
2. Use `git show --stat HEAD` as a **refresher** to confirm recent changes
3. Filter to ONLY files you are aware of working on (other agents may have committed unrelated changes)
4. Expand scope to include related files in that domain (services, tests, models, etc.)
5. Proceed with the refactoring workflow for that scope

**Important:** The refactor pertains to YOUR session work, not all recent git activity. Use git as a memory aid, not the source of truth for scope.

## Step 1: Enter Plan Mode

Use `EnterPlanMode` tool FIRST. Refactoring requires a consolidated plan before execution.

## Step 2: Run Review Agents in Parallel

Launch ALL available review agents simultaneously in a SINGLE message with multiple Task tool calls:

1. **test-reviewer** - Audit test coverage for the code in scope
2. **code-reviewer** - Analyze code quality (file size, SOLID, DRY, anti-patterns)
3. **architecture-reviewer** (if available) - Analyze domain placement and cross-boundary concerns

## Step 3: Consolidate into Single Plan

After all agents report back, create ONE unified plan file. **Include the test-reviewer's inventory table AS-IS** - tables provide clear, scannable status at a glance.

Organize the plan as:

**Part 1: Test Coverage** (from test-reviewer) - Test inventory table, tests to write, tests to fix

**Part 2: Architecture** (from architecture-reviewer, if run) - Domain placement issues, cross-boundary duplication

**Part 3: Code Quality** (from code-reviewer) - File splitting, SOLID/DRY violations, anti-patterns

**Execution order:** Tests first, then architecture fixes, then code quality improvements.

## Step 4: Get Approval and Execute

1. Exit plan mode to get user approval
2. Execute Part 1 (tests) - verify they pass
3. Execute Part 2 (refactoring) - run tests after each significant change

---

## What Refactoring Means

| Refactoring IS | Refactoring is NOT |
|----------------|---------------------|
| Breaking large files into focused ones | Removing console.logs and calling it done |
| Ensuring EVERY file meets SOLID | Marking violations as "future work" |
| Fixing ALL DRY violations immediately | Listing issues without fixing them |
| Removing ALL dead code, tech debt | A partial cleanup pass |

## Priority Order

1. **Test coverage** - Must exist before refactoring
2. **Domain placement** - Move misplaced code to correct domains
3. **Cross-domain dedup** - Consolidate duplicate code
4. **Large file splitting** - Files exceeding size limits
5. **Large method splitting** - Methods >30 lines
6. **SOLID violations** - Single responsibility issues
7. **DRY violations** - Local duplicated code
8. **Dead/debug code** - Unused code and debug statements
