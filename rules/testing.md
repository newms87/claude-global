# Testing

**Full testing discipline lives in `testing` skill, not here.** Invoke via Skill tool FIRST time you run, write, fix, inspect, or reason about any test in session. No exceptions, no minimum size, no "just one test" exemption, no "I already know what I'm doing" escape hatch.

## Triggers

**Run triggers.** About to invoke `vitest`, `pytest`, `jest`, `rspec`, `go test`, `cargo test`, `phpunit`, `./vendor/bin/sail test`, `make test*`, `npm test`, `yarn test`, or any project-specific test wrapper — filtered or full, single test or entire suite.

**Write triggers.** About to create new test file, add test case, write failing test for bug fix (TDD), extend mock helper, modify fixture/factory/conftest.

**Fix triggers.** Test failing. Suite reports non-zero exit. About to mark test `skip`/`xfail`/`it.skip`/`@pytest.mark.skip`. About to delete test. About to change assertions to match "what code does" instead of "what code should do."

**Reason triggers.** Answering "is this tested?" / "what's the coverage?" / "which tests cover X?". About to claim "tests pass" or "all green." About to run reviewer agent that will ask about tests.

## What Is NOT a Trigger

Reading test file to learn what code-under-test does (as documentation source, not to run or modify) — normal file read. Line: **about to run, write, fix, or assert about state of any test → skill required.**

## Why No Methodology Lives Here

Duplicating methodology would let me read this file + skip skill — exact failure mode justifying skill's existence. Skill creates TodoWrite checklist that IS workflow. Need testing guidance of any kind → call skill.