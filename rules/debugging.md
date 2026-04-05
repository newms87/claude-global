# Debugging Guidelines

## CRITICAL: Diagnose ≠ Fix — Two Different Commands

| User says | What it means | What you do |
|-----------|--------------|------------|
| "X is broken" / "Why is X?" / "Look into X" | Diagnose | Investigate, report findings, present options |
| "Fix X" / "Make X work" / "Go ahead" / "Do it" | Fix | Implement the fix |

**Default is ALWAYS diagnose-only.** Only explicit action verbs (fix, implement, change, do it, go ahead) authorize fixes. After presenting options, you are in a HARD STOP — text only until you get an action verb.

**Scope:** This rule applies to user-reported issues. Pipeline discovery (test fails, DRY violation) is a pipeline responsibility to fix immediately — but still requires TDD. User-reported bugs always follow diagnose-and-report regardless of card status.

## CRITICAL: TDD For EVERY Bug Fix — ZERO Exceptions

**Failing test → run → fix → verify. Non-negotiable for every bug.**

1. **Write failing test** that reproduces the bug
2. **Run it** — verify it fails for the reason you expect
3. **Fix code** — minimal change
4. **Verify** — test passes, run related tests

**Multiple bugs = multiple TDD cycles, sequentially.** If unable to reproduce in a test, you don't understand the bug yet — go back to investigation.

## Never Guess — Verify Everything

Before using a value, component, or prop: read the source. Do NOT assume names exist or guess behavior. **If unsure, STOP and look it up.** Reading takes seconds; fixing a wrong guess wastes minutes.

## Assumptions Are Not Evidence

Every link in a causal chain must be verified independently. "A could cause B" does NOT mean "A is causing B." Verify: is it the same file? Was that code actually running? Does the metric mean what I think? If you cannot verify all links, REPORT your hypothesis — do NOT act on it.

## Never Silence an Error — Investigate Why It Fires

When validation fails, the error is telling you something is wrong upstream. NEVER bypass with `try/catch`, flags, or `orUpdate: true`. The bug is in whatever failed to find the existing record before the create. **Trace back and fix the source, not the error.**

## Never Deflect Bugs as "Pre-existing"

You own the entire codebase. When the user encounters a bug, diagnose root cause and options. Never defer unless the user raises scope concerns first.

## When You Don't Know — STOP

If unsure how to solve a problem: stop immediately, explain what you understand and don't, list theories, ask for guidance. Do NOT continue with trial-and-error.

## Pipeline Monitoring Is Not Testing

When a running pipeline fails, each failure is a bug requiring TDD: failing test → fix → verify. Do NOT fix inline and rerun the pipeline. The pipeline rerun validates integration; the unit test validates your fix. Both required, test comes first.

## Never Bypass a Component — Fix It

When a UI component doesn't render correctly, read its source to understand how it works. Before swapping components: (1) read the source, (2) check working examples in the codebase, (3) fix the usage. The problem is almost always in how it's being called, not the component itself.

## Agent Findings Are Hypotheses, Not Proof

When a subagent reports "X is never set" or "Y doesn't exist," verify with empirical data before acting. Run a database query. Check actual runtime values. Code analysis tells you what the code SAYS; only data tells you what it DOES. When they disagree, data wins.
