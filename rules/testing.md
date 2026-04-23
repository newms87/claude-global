# Testing

**The full testing discipline lives in the `testing` skill, not here.** Invoke it via the Skill tool the FIRST time you run, write, fix, inspect, or reason about any test in a session. No exceptions, no minimum size, no "just one test" exemption, no "I already know what I'm doing" escape hatch.

## Triggers

**Run triggers.** About to invoke `vitest`, `pytest`, `jest`, `rspec`, `go test`, `cargo test`, `phpunit`, `./vendor/bin/sail test`, `make test*`, `npm test`, `yarn test`, or any project-specific test wrapper — filtered or full, single test or entire suite.

**Write triggers.** About to create a new test file, add a test case, write a failing test for a bug fix (TDD), extend a mock helper, or modify a fixture/factory/conftest.

**Fix triggers.** A test is failing. A suite reports non-zero exit. About to mark a test `skip`/`xfail`/`it.skip`/`@pytest.mark.skip`. About to delete a test. About to change assertions to match "what the code does" instead of "what the code should do."

**Reason triggers.** Answering "is this tested?" / "what's the coverage?" / "which tests cover X?". About to claim "tests pass" or "all green." About to run a reviewer agent that will ask about tests.

## What Is NOT a Trigger

Reading a test file to learn what the code-under-test does (as a documentation source, not to run or modify it) — that's a normal file read. The line: **if you're about to run, write, fix, or assert about the state of any test, the skill is required.**

## Why No Methodology Lives Here

Duplicating the methodology would let me read this file and skip the skill — exactly the failure mode that justifies the skill's existence. The skill creates the TodoWrite checklist that IS the workflow. If you need testing guidance of any kind, call the skill.
