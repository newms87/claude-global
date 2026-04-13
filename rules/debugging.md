# Debugging Guidelines

## CRITICAL: Diagnose ≠ Fix — Two Different Commands

| User says | What it means | What you do |
|-----------|--------------|------------|
| "X is broken" / "Why is X?" / "Look into X" | Diagnose | Investigate, report findings, present options |
| "Fix X" / "Make X work" / "Go ahead" / "Do it" | Fix | Implement the fix |

**Default is ALWAYS diagnose-only.** Only explicit action verbs (fix, implement, change, do it, go ahead) authorize fixes. After presenting options, you are in a HARD STOP — text only until you get an action verb.

**Scope:** This rule applies to user-reported issues. Pipeline discovery (test fails, DRY violation) is a pipeline responsibility to fix immediately — but still requires TDD. User-reported bugs always follow diagnose-and-report regardless of card status.

## CRITICAL: TDD For EVERY Change — ZERO Exceptions

**Failing test → run → fix → verify. Non-negotiable for every bug AND every feature.**

1. **Write failing test** that reproduces the bug or proves the feature doesn't work yet
2. **Run it** — verify it fails for the reason you expect
3. **Fix/implement code** — minimal change
4. **Verify** — test passes, run related tests

**Multiple bugs = multiple TDD cycles, sequentially.** If unable to reproduce in a test, you don't understand the bug yet — go back to investigation.

**No category is exempt.** Infrastructure changes, config changes, cross-process behavior, agent dispatch restrictions — ALL require a test that fails before the fix and passes after. "This is config, not code" and "this can't be unit tested" are rationalizations. If you can't write a test, you don't understand the problem well enough to fix it.

**Never claim something works without test evidence.** Running the system and observing output is not verification — it's anecdote. A passing test is verification. If you report "working correctly" to the user, you must have a test that proves it.

## Never Guess — Verify Everything

Before using a value, component, or prop: read the source. Do NOT assume names exist or guess behavior. **If unsure, STOP and look it up.** Reading takes seconds; fixing a wrong guess wastes minutes.

## ABSOLUTE: NEVER Write Solution Code Without Proven Understanding

Before implementing ANY fix or change to behavior, you must have 100% confidence in what the problem is and why your solution solves it. 100% confidence comes ONLY from runtime evidence: logs, test output, reproduction, or a controlled experiment. If you are 99% or less confident, STOP. Either run an experiment to prove your theory, or ask the human. "I'm pretty sure this is the issue" is not confidence — it's a guess. Guesses get published to npm and waste 30 minutes. Proof takes 60 seconds.

This applies to EVERYTHING — application bugs, infrastructure, Node.js internals, OS-level operations, timing issues. "I know how setTimeout works" is not evidence. Prove it works in your specific context before shipping it.

## CRITICAL: Code Is Not Evidence — Reproduce or Find Runtime Proof

Before concluding what happened AND ESPECIALLY before deciding on a fix, you MUST have direct evidence from one of these sources:

1. **Runtime logs/traces** — session JSONL, audit logs, event history, database state
2. **Reproduction** — trigger the same failure in a controlled way
3. **Failing test** — write a test that proves the problem causes a failure (TDD — always preferred when feasible)

Reading code tells you what COULD happen. Only runtime data tells you what DID happen. Code reading is useful for orientation — knowing where to look — but it is NEVER sufficient for drawing conclusions. A theory constructed from code alone is a guess, and a fix based on a guess is reckless.

**Mechanical check before proposing any fix:** "What is my direct evidence that this is what happened? Can I point to a specific log line, event, timestamp, or failing test?" If the answer is "I read the code and it looks like..." — STOP. Go find the runtime evidence first.

## Assumptions Are Not Evidence

Every link in a causal chain must be verified independently. "A could cause B" does NOT mean "A is causing B." Verify: is it the same file? Was that code actually running? Does the metric mean what I think? If you cannot verify all links, REPORT your hypothesis — do NOT act on it.

## Never Fabricate Justifications for Existing Code

When explaining WHY code exists, read the producing side before answering. If explaining a response handler, read the endpoint. If explaining a fallback, read what produces the data. If explaining a compatibility layer, verify both formats actually exist.

"The code handles two shapes, so there must be two shapes" is BACKWARDS REASONING. Code is often wrong, speculative, or copy-pasted. The code's existence is not evidence that it's correct. Read the source of truth (the producer, the schema, the actual data) before explaining why consumer code does what it does.

**Mechanical check:** "Am I about to explain why code exists? Have I read the other side?" If no, read it first — or say "I haven't verified this" and stop.

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
