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

The full pipeline (implement → `/flow-code-review` → `/flow-quality-check` → `/flow-commit` → `/flow-report` → `/flow-self-improvement`) runs automatically after each phase. For related phases in the same domain, group them and run the pipeline once on the combined work. See `planning.md` for full pipeline details.

## How to Run Code Reviews

- **Post-implementation review (default):** Invoke `/flow-code-review`. This runs reviewer agents, then you fix findings inline, then run `/flow-quality-check` to audit your decisions before committing.
- **Full refactoring workflow:** Invoke `/code-review` when explicitly asked to refactor. This enters plan mode, runs all reviewers, creates a unified refactoring plan, and executes it.

## What to Do with Findings

Fix ALL findings before committing. The `/flow-code-review` skill handles the fixing process, and `/flow-quality-check` audits your decisions — see that skill for the full decision framework including valid skip reasons, the rationalization detector, and the 3 valid skip reasons.

## CRITICAL: Never Modify Reviewer Agents to Reduce Findings

**Reviewer agents must remain aggressive and unscoped.** They flag everything they find — pre-existing issues, issues in files you barely touched, issues unrelated to your task. This is correct behavior.

If reviewers produce too many findings, the answer is to fix all of them. Never:
- Add scoping rules to reviewer agents ("only flag things in the diff")
- Add exclusion rules ("don't flag one-liners," "don't flag heavy-mock scenarios")
- Modify reviewer prompts to reduce noise

The reviewers are intentionally ignorant of skip reasons. Skip decisions belong in `/flow-quality-check`, not in the reviewers.
