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

After implementing a feature:
1. Write unit tests for all new code
2. Write integration/feature tests for endpoints or user flows
3. Test happy paths AND error cases
4. Verify all tests pass
5. **Run test-reviewer agent** as final step before marking tests complete

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

## Test Ownership

**YOU ARE RESPONSIBLE FOR ALL CHANGES.** If a test fails in your domain:

- **NEVER assume it was "pre-existing"** — You are the only one making changes
- **ALWAYS fix failing tests** — Either fix implementation, update the test, or remove if obsolete
- Tests must be 100% passing at all times before completing work

## Test Review Process

Before completing any phase with tests, call the `test-reviewer` agent to audit your work. Address its findings before marking complete.
