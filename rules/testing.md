# Testing Rules

## 100% Test Coverage Required

All features and bug fixes MUST have comprehensive tests. No exceptions.

## Test Philosophy: Quality Over Quantity

- Focus on behavior and outcomes, not implementation details
- Every test must verify functionality that could actually break
- Use descriptive test names that explain the scenario

## TDD for Bug Fixes

When fixing bugs, ALWAYS use TDD:

1. **Write failing test** - Create test that fails due to the bug
2. **Run test** - Verify it fails for the right reason
3. **Fix the bug** - Minimal change to make test pass
4. **Verify** - Run test, confirm it passes
5. **Check for regressions** - Run related tests

## Features Get Tests After Implementation

After implementing a feature (or completing a phase):
1. Write unit tests for all new code
2. Write integration/feature tests for endpoints or user flows
3. Test happy paths AND error cases
4. Verify all tests pass
5. **Run test-reviewer agent** — this is MANDATORY, not optional. Address all gaps it identifies before proceeding.

**Write tests as part of implementation, before running `/flow-code-review`.** The test-reviewer agent runs inside `/flow-code-review` alongside the code-reviewer and architecture-reviewer — it will flag any gaps you missed. For related phases in the same domain, tests can be written after all related phases complete (see code-reviews.md for grouping rules).

## Good Tests (Write These)

- Critical business logic with complex conditions
- State transitions and workflow correctness
- Security and authorization checks
- Edge cases that could cause data corruption
- Error handling and exception scenarios
- Custom logic with date/filter calculations

## Bad Tests (Never Write These)

- Factory creates model (tests the factory, not your code)
- Framework features work (relationships, casts, routing — trust the framework)
- Database constraints (unique, cascade delete — trust migrations)
- Getters/setters (testing basic property access)
- Mocking database instead of using real database
- Testing implementation details instead of behavior

**Before writing a test, ask: "Would this test fail if MY code has a bug, or only if the framework has a bug?" If the answer is the framework, don't write it.**

## Zero Vue Warnings in Tests

**Vue warnings in test output are bugs, not noise.** Common causes:

- Composable with lifecycle hooks (`onUnmounted`, `onMounted`) called outside component setup — wrap in `mount(defineComponent({ setup() { ... } }))`
- `defineComponent()` result passed as a prop — wrap with `markRaw()`
- Required prop omitted — always provide all required props
- Empty object `{}` used as component stub — use `defineComponent({ template: "<span />" })`

## Test Ownership

**YOU ARE RESPONSIBLE FOR ALL CHANGES.** If a test fails in your domain:

- **NEVER assume it was "pre-existing"** — You are the only one making changes
- **ALWAYS fix failing tests** — Either fix implementation, update the test, or remove if obsolete
- Tests must be 100% passing at all times before completing work

## CRITICAL: Never Run Tests in Parallel

**Always run test commands sequentially, one at a time.** Tests share a database and resources protected by a lock system. Parallel test processes block each other, waiting for locks to release — guaranteed slower than sequential due to lock polling overhead.

## CRITICAL: Full Test Suite — Run Once, Extract Everything

**The full test suite is expensive (minutes of heavy CPU).** Treat it as a one-shot operation:

1. **Run at most ONCE per work session** — only when all changes are complete and you're confident they're correct
2. **Run targeted tests first** (`--filter=TestName`) to catch issues cheaply before ever running the full suite
3. **Extract ALL information in a single command** — never re-run to get different output

**Save output to a file** so you never need to re-run for missing information:

```bash
<test-command> > /tmp/test-output.txt 2>&1
```

Then grep the file for failures and read the file for stack traces. The exact grep pattern depends on the test runner — learn the output format for each project.

**Re-running the full suite to "find" failures is FORBIDDEN.** If you missed information, read from the saved output. The only reason to re-run is after making code changes to fix failures — and even then, prefer targeted tests for the specific failing test first.

## CRITICAL: Never Let Subagents Run Tests

**When spawning batch-editor or other subagents, explicitly tell them NOT to run tests.** Test validation belongs in the main pipeline — not inside subagents.

Multiple subagents running `yarn test:run` simultaneously spawns parallel Vitest processes, each with heavy CPU/RAM overhead (jsdom environments, TypeScript transforms, full import graphs). Three concurrent test runs can consume 16GB+ RAM and 100% CPU, causing system thrashing.

**Rule:** Subagents edit files only. The parent agent runs tests once after all subagents complete.

**Concurrency limit:** Never run more than 2 batch-editor agents at a time. More than 2 concurrent agents causes resource contention, incomplete edits, and unreliable results. If work requires more than 2 batches, wait for the first pair to finish before launching the next.

## Vitest Mock Isolation: Never Use vi.restoreAllMocks() in afterEach

**Use `vi.clearAllMocks()` in `beforeEach` and explicitly reset mock return values.** Never rely on `vi.restoreAllMocks()` in `afterEach` to undo `mockReturnValue()` — it does not reliably clear return values set by previous tests, causing mock state to leak between tests in hard-to-debug ways. Instead, explicitly call `mockFn.mockReturnValue(defaultValue)` in `beforeEach` for any mock that tests override.

## Test Review Process

Before completing any phase with tests, call the `test-reviewer` agent to audit your work. Address its findings before marking complete.
