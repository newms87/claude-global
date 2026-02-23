---
name: flow-code-review
description: Post-implementation review. Runs reviewer agents in parallel, fixes ALL findings before committing.
---

# Post-Implementation Code Review

Post-implementation review step in the development pipeline. Runs reviewer agents and fixes ALL findings before committing. The primary goal is that every file you touched is in perfect shape — feature delivery is secondary to code quality.

---

## Step 1: Determine Scope

Review code from **your current session's work**:

1. Recall which files you worked on during this session
2. Use `git diff --name-only` as a **refresher** to confirm changed files
3. Filter to ONLY files you are aware of working on (other agents may have committed unrelated changes)

## Step 2: Run Reviewer Agents in Parallel

Launch available review agents simultaneously in a SINGLE message with multiple Task tool calls:

All three agents are MANDATORY. They have distinct, non-overlapping roles — do not skip any.

1. **test-reviewer** — Test coverage and quality (tests only)
2. **code-reviewer** — Per-file quality: size limits, per-file DRY, dead code, documentation, per-file anti-patterns
3. **architecture-reviewer** — Cross-file patterns: component interfaces (>4 props, emit chains, prop threading), composable-first enforcement, cross-file DRY, domain placement

## Step 3: Fix ALL Findings

**Every finding from every reviewer MUST be fixed. No exceptions.**

For each finding from the agents:

- **Typical findings** (naming, small refactors, missing tests, DRY violations): Fix immediately. No plan mode needed.
- **Larger findings** (size violations, emit chains, composable extractions): Fix them. If extensive, use the escalation process below to enter plan mode — but still fix them. Never skip.

## Step 4: Write Pattern-Worthy Findings to Notes

If any finding reveals a pattern that could prevent future mistakes, write it to `agent-notes.md` in the project root using the standard note format. These get processed later by `/flow-self-improvement`.

## Step 5: Run `/flow-quality-check`

**After fixing all findings, invoke `/flow-quality-check` before proceeding to `/flow-commit`.** This audits your decisions — verifying that every finding was addressed and no rationalizations slipped through. It is a mandatory pipeline step.

## Escalation: When to Enter Plan Mode

Use your judgment. Enter plan mode if findings are **extensive** — meaning they:
- Touch many files across multiple domains
- Require investigation to understand the right approach
- Amount to a significant refactor

When escalating: add findings under the CURRENT phase in the existing plan file. Never overwrite or create a new plan.

---

## Rules

- **You are the author — agents are the reviewers.** Never skip this step because you're confident in your code.
- **Fix before committing.** ALL findings must be fixed before `/flow-commit`. No deferring, no "flagging for later."
- **Always run `/flow-quality-check` after fixing.** This is what catches rationalizations and skipped findings.
- **Escalate large findings, don't skip them.** If findings require significant refactoring, enter plan mode. But they still get fixed in this pipeline run.
