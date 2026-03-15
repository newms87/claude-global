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

- **Post-implementation review (default):** Invoke `/flow-code-review`. This runs reviewer agents, creates a revisions plan in `.claude/code-review-plans/`, then fixes ALL findings following that plan before committing.
- **Full refactoring workflow:** Invoke `/code-review` when explicitly asked to refactor. This enters plan mode, runs all reviewers, creates a unified refactoring plan, and executes it.

## CRITICAL: The Primary Mission — Eliminate Legacy and Dead Code

**The #1 purpose of code review is finding and removing legacy code, backwards-compatible code, obsolete patterns, and dead code.** These findings are the highest priority — higher than style, higher than DRY, higher than missing tests. When a reviewer flags old formats, legacy fallbacks, backwards-compatibility branches, or dead code paths, that finding is automatically top priority and CANNOT be skipped for any reason.

This is what we are looking for. This is what makes code reviews worth running. A code review that discovers legacy code and doesn't remove it has failed its primary mission.

## CRITICAL: Silent Fallbacks Are the #2 Priority

**After legacy/dead code, the second highest priority is finding silent fallbacks.** Every `??`, every default value, every `isset()` guard that silently returns instead of throwing — these are bugs that mask malformed data. A fallback that hides a missing value is actively harmful code. See `core-principles.md` "Fallbacks Are Bugs" for the full rule. Reviewers must flag every fallback and the author must justify each one or replace it with an explicit error.

## What to Do with Findings

**After receiving reviewer output, create a revisions plan** (`.claude/code-review-plans/revisions-<timestamp>.md`) containing all findings and a phased implementation plan for fixes. This keeps review tracking separate from the main plan file. Fix ALL findings following the revisions plan before committing. The `/flow-code-review` skill handles the full process, and `/flow-quality-check` audits your decisions — see that skill for the full decision framework including valid skip reasons, the rationalization detector, and the 3 valid skip reasons.

## CRITICAL: Never Modify Reviewer Agents to Reduce Findings

**Reviewer agents must remain aggressive and unscoped.** They flag everything they find — pre-existing issues, issues in files you barely touched, issues unrelated to your task. This is correct behavior.

If reviewers produce too many findings, the answer is to fix all of them. Never:
- Add scoping rules to reviewer agents ("only flag things in the diff")
- Add exclusion rules ("don't flag one-liners," "don't flag heavy-mock scenarios")
- Modify reviewer prompts to reduce noise

The reviewers are intentionally ignorant of skip reasons. Skip decisions belong in `/flow-quality-check`, not in the reviewers.
