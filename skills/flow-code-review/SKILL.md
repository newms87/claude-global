---
name: flow-code-review
description: Lightweight post-implementation review. Runs reviewer agents in parallel, fixes findings inline.
---

# Post-Implementation Code Review

Lightweight review step in the development pipeline. This is NOT the full `/code-review` refactoring workflow — it's a quick quality check after implementation.

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

## Step 3: Fix Findings Inline

For each finding from the agents:

- **Typical findings** (naming, small refactors, missing tests, DRY violations): Fix immediately. No plan mode needed.
- **Pre-existing issues** outside your scope: Flag to the user, do not fix.
- **Do not dismiss findings** — if an agent flags something, address it or explain why it doesn't apply.

## Step 4: Write Pattern-Worthy Findings to Notes

If any finding reveals a pattern that could prevent future mistakes, write it to `agent-notes.md` in the project root using the standard note format. These get processed later by `/flow-self-improvement`.

## Escalation: When to Enter Plan Mode

Use your judgment. Enter plan mode if findings are **extensive** — meaning they:
- Touch many files across multiple domains
- Require investigation to understand the right approach
- Amount to a significant refactor

When escalating: add findings under the CURRENT phase in the existing plan file. Never overwrite or create a new plan.

---

## Rules

- **You are the author — agents are the reviewers.** Never skip this step because you're confident in your code.
- **Fix before committing.** All findings must be addressed before `/flow-commit`.
- **Keep it fast.** This is a quality gate, not a refactoring session. Fix what's broken, note what's interesting, move on.
