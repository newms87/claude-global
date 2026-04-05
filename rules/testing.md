# Testing Rules

## 100% Test Coverage Required

All features and bug fixes MUST have comprehensive tests. No exceptions.

## CRITICAL: TDD For Bug Fixes

See `debugging.md` — every bug fix requires: failing test → run → fix → verify.

## Features Get Tests After Implementation

After implementing a feature:
1. Write unit tests for all new code
2. Write integration/feature tests for endpoints or user flows
3. Test happy paths AND error cases
4. Verify all tests pass
5. **Run test-reviewer agent** — this is MANDATORY. Address all gaps before proceeding.

Write tests before running `/flow-code-review`. For related phases in the same domain, tests can be written after all related phases complete.

## CRITICAL: Passing Existing Tests ≠ Tested

Running `--filter` and seeing green confirms you didn't break anything. It does NOT confirm your new code is tested. After every implementation, ask: "What new public methods did I add, and where are their tests?" If not answered, you're not done.

## Good Tests vs Bad Tests

**Write these:**
- Critical business logic with complex conditions
- State transitions and workflow correctness
- Security and authorization checks
- Edge cases that could cause data corruption
- Error handling and exception scenarios

**Never write these:**
- Factory creates model (tests the factory)
- Framework features work (relationships, casts, routing — trust the framework)
- Database constraints (unique, cascade delete — trust migrations)
- Getters/setters (basic property access)
- Mocking database instead of using real database
- Testing implementation details instead of behavior

**Test rule:** Would this test fail if MY code has a bug, or only if the framework has a bug? If the framework, don't write it.

## Zero Vue Warnings in Tests

Vue warnings are bugs, not noise. Common causes:
- Composable with lifecycle hooks (`onMounted`, `onUnmounted`) called outside component setup — wrap in `mount(defineComponent({ setup() { ... } }))`
- `defineComponent()` result passed as a prop — wrap with `markRaw()`
- Required prop omitted — always provide all required props
- Empty object `{}` used as component stub — use `defineComponent({ template: "<span />" })`

## Test Ownership

**YOU OWN ALL CODE.** Not just your changes — the entire codebase.
- NEVER assume it was "pre-existing" — you own it
- ALWAYS fix failing tests
- Tests must be 100% passing before completing work
- If a reviewer flags a missing test, write it. No exceptions.

## Never Skip Tests Due to Dependency Count

If a service has 5, 10, or 100 dependencies — mock them all and write the test. Extract common mock setups into a test helper trait so multiple tests reuse the setup. "Too many mocks" is a rationalization, not a technical limitation.

## Test Protected and Private Methods

Protected/private methods contain logic that needs tests. Either: (1) make the method public and test directly, or (2) use Reflection to test in place. Never skip a test because the method is protected.

## CRITICAL: Never Run Tests in Parallel or Background

Tests share a database and resources. Parallel processes block waiting for locks — guaranteed slower than sequential. **NEVER use `run_in_background: true`.** Tests are resource-intensive. While tests run, do NOT edit code, read files, run commands, launch agents, or make decisions. Wait for results, then proceed.

## Full Test Suite — Rare, End-Only

**ALWAYS use `--filter` for testing.** Full suite is a rare event. `--filter` takes seconds; full suite takes 5-25 minutes.

**Run full suite ONLY when ALL are true:**
- Implementation 100% complete (not mid-work)
- All filtered tests pass
- Changes span multiple domains or touch shared infrastructure
- You believe changes could break something outside your domain

**If running full suite:** (1) run ONCE at the end, (2) save output to file: `<test-command> > /tmp/test-output.txt 2>&1`, (3) fix failures with `--filter`, (4) try full suite one more time, (5) read the saved file — never re-run just for output.

## CRITICAL: Never Let Subagents Run Tests

Subagents must edit files only. Parent agent runs tests once after all subagents complete. Multiple concurrent test runs cause system thrashing (16GB+ RAM, 100% CPU). **Max 2 batch-editor agents at a time.** If work requires more batches, wait for the first pair to finish.

## Vitest Mock Isolation

Use `vi.clearAllMocks()` in `beforeEach` and explicitly reset mock return values. Do NOT use `vi.restoreAllMocks()` in `afterEach` — it does not reliably clear return values, causing mock state to leak between tests.

## Always Dump Test Output to File

Never run test suites bare. Always capture: `yarn test:run > /tmp/test-output.txt 2>&1`. Then grep the file for failures. Re-running to get different output is FORBIDDEN.

## Test Review Process

Before completing any phase with tests, call the `test-reviewer` agent to audit coverage. Address all findings before marking complete.
