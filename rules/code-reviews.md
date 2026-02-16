# Code Reviews

## CRITICAL: Code Review Is Not You Reading Code

A "code review" means running the project's **reviewer agents** via the Task tool. It does NOT mean you reading files and writing commentary. You are the author — you cannot review your own work.

## When to Run Code Reviews

**MANDATORY** — run a code review on your work when ANY of these apply:

- Changes span multiple files
- More than ~10 lines of code changed
- New feature or component added
- Completing a phase in a phased plan

Skip code reviews only for trivial changes (typo fix, single-line change, config tweak).

## Timing: Per-Phase vs. Grouped

**The workflow is: implement → test coverage → code review → report to user → commit.**

When to run the quality gates depends on how related the phases are:

- **Independent phases** (different domains, separate concerns): Run test coverage + code review after each phase before moving on.
- **Related phases** (same domain, building on each other): Group them and run test coverage + code review once after all related phases are complete.

Use judgment. The goal is to catch issues before presenting to the user, not to create busywork. If phases 1-3 all modify the same files and build incrementally, reviewing after phase 3 is more efficient than reviewing three times.

## How to Run Code Reviews

Use the `/code-review` skill for full refactoring workflows. For lighter post-implementation reviews, launch the project's reviewer agents directly via the Task tool.

Each project defines its own reviewer agents and review process. Check the project's `.claude/rules/` or `.claude/agents/` for available reviewers and how to use them.

## What to Do with Findings

- **Fix issues** before committing or marking a phase complete
- **Flag pre-existing issues** to the user — do not fix code outside your scope
- **Do not dismiss findings** — if an agent flags something, address it or explain why it doesn't apply
