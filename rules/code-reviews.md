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

**The workflow is: implement → `/flow-code-review` → `/flow-commit` → `/flow-report` → `/flow-self-improvement` → next phase.**

**This entire pipeline — including advancing to the next phase — runs automatically.** Invoke `/flow-code-review` via the Skill tool immediately after code is written. Do not stop and wait for the user to trigger any step. The pipeline executes as one continuous unit across all phases until the work is complete.

When to run the quality gates depends on how related the phases are:

- **Independent phases** (different domains, separate concerns): Run the full pipeline after each phase.
- **Related phases** (same domain, building on each other): Group them and run the pipeline once after all related phases are complete.

Use judgment. The goal is to catch issues before committing, not to create busywork. If phases 1-3 all modify the same files and build incrementally, reviewing after phase 3 is more efficient than reviewing three times.

## How to Run Code Reviews

- **Post-implementation review (default):** Invoke `/flow-code-review`. This runs reviewer agents, fixes findings inline, and is the standard quality gate in the development pipeline.
- **Full refactoring workflow:** Invoke `/code-review` when explicitly asked to refactor. This enters plan mode, runs all reviewers, creates a unified refactoring plan, and executes it.

## CRITICAL: Implement ALL Reviewer Recommendations

**Every recommendation from a code reviewer or test reviewer MUST be implemented. No exceptions.**

Do not skip, defer, or dismiss recommendations because they seem unrelated to your current work. The reviewer flagged it for a reason. Just do it.

- Missing test? Write it.
- Code quality issue? Fix it.
- Coverage gap? Fill it.
- Refactor suggestion? Apply it.

The only valid reason to skip a recommendation is if it's factually wrong (e.g., the reviewer misread the code). In that case, explain why in a comment. Otherwise, implement it before committing.

## What to Do with Findings

- **Fix issues** before committing or marking a phase complete
- **Flag pre-existing issues** to the user — do not fix code outside your scope
- **Do not dismiss findings** — if an agent flags something, address it or explain why it doesn't apply
