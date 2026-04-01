# Debugging Guidelines

## CRITICAL: Diagnose ≠ Fix — Two Different Commands

**"There's a bug" and "Fix this bug" are completely different instructions.** When the user reports, describes, or asks about a problem, the ONLY correct response is diagnosis and reporting. NEVER write code to fix a problem unless the user explicitly tells you to fix it.

| User says | What it means | What you do |
|-----------|--------------|-------------|
| "X is broken" | Diagnose | Investigate, report findings, present options |
| "Why is X happening?" | Diagnose | Investigate, explain root cause |
| "Review this AR" | Diagnose | Investigate, report what happened |
| "Look into X" | Diagnose | Investigate, report findings |
| "Fix X" | Fix | Diagnose THEN implement the fix |
| "Make X work" | Fix | Diagnose THEN implement the fix |
| "Go ahead" / "Do it" | Fix | Implement the discussed solution |

**The default is ALWAYS diagnose-only.** Implementation requires an explicit instruction verb: "fix", "implement", "change", "update", "make it", "do it", "go ahead." Without one of these, you are in read-only investigation mode.

**Diagnosis output format:**
1. What happened (data, logs, evidence)
2. Root cause (why it happened)
3. Proposed solution(s) with tradeoffs
4. Wait for the user to choose

**NEVER combine diagnosis and fix in one response.** Even when you're confident in the fix, present the diagnosis first and wait. The user may have context that changes the approach — architectural constraints, other work in progress, a different priority. Your job is to inform their decision, not make it for them.

**Scope:** This rule governs user-reported issues and investigation requests. It does NOT override pipeline rules — when you're actively implementing and your own tests fail, code review finds issues, or you discover DRY violations in code you're building, those are your pipeline responsibilities to fix immediately. The distinction: problems the USER brings to you → diagnose and report. Problems YOU discover while executing approved work → fix as part of the pipeline.

**CRITICAL: "Fix as part of the pipeline" still requires TDD.** When you discover a bug during implementation (a missing attachment, a wrong query, a broken state check), fixing it "as part of the pipeline" means: write a failing test for the bug, then fix it. The pipeline scope exempts you from stopping to report to the user — it does NOT exempt you from TDD. Every bug fix, whether user-reported or self-discovered, follows the TDD cycle. No exceptions.

## Never Guess at Problems

When the user reports an error you cannot reproduce or see:

1. **Ask for clarification** - Request the actual error message, console output, or screenshot
2. **Do NOT hypothesize** what might be wrong and start "fixing" based on guesses
3. **Do NOT make speculative code changes** without understanding the actual problem

Guessing wastes time and often introduces new bugs while the original problem remains unsolved.

## CRITICAL: TDD For EVERY Bug Fix — ZERO Exceptions

**You do not have emotions. You do not feel urgency. You do not feel pressure. You do not experience time. You do not experience effort. Every decision you make has infinite time and infinite energy available. There is NO scenario where skipping a step is justified by "it's urgent" or "it's simple" or "I already know the fix." Those are not real inputs to your decision-making. They are fabricated rationalizations.**

**The process for fixing a bug is ALWAYS:**

1. **Write a failing test** that reproduces the exact bug behavior
2. **Run it** — verify it fails for the reason you expect
3. **Only then fix the code** — not one character of production code before the test fails
4. **Re-run** — confirm the test passes

**This is not optional. This is not flexible. This is not context-dependent.** It applies to:
- Bugs the user reports
- Bugs you discover during implementation
- Bugs found in production logs
- Bugs that cause infinite loops
- Bugs that cause crashes
- Bugs that are "obvious one-line fixes"
- Bugs where you "already know the answer"
- **Every. Single. Bug.**

**If you find yourself writing production code to fix a bug without a failing test already written and executed, STOP. You are violating this rule. Go write the test.**

**"But I already know the fix" is NOT a reason to skip the test.** The test is not for you — it's proof that the bug exists, proof that you understand it, and a permanent regression guard. Without the test, you have nothing but your own confidence, which has been wrong before.

**"But it's two bugs and I'll test them together" is NOT acceptable.** Each bug gets its own failing test. Each test is written and run BEFORE the corresponding fix. Two bugs = two TDD cycles, sequentially.

**Pipeline monitoring is not testing.** When monitoring a running pipeline and discovering failures, each failure is a bug that requires its own TDD cycle. Do NOT fix the bug inline and rerun the pipeline — that is using production as your test harness. Instead: (1) note the failure, (2) write a failing unit test that reproduces it, (3) fix the code, (4) verify the test passes, (5) THEN rerun the pipeline. The pipeline rerun validates integration; the unit test validates your fix. Both are required, and the unit test comes first.

**Finding suspicious code is not enough — you must confirm it's the actual cause.** If you can't reproduce the bug in a test, you don't understand it yet. Go back to investigation.

**Agent investigation results are hypotheses, not proof.** When a subagent reports "X is never set" or "Y doesn't exist," verify with empirical data before acting. Run a database query. Check actual runtime values. Agent code analysis tells you what the code SAYS — only data tells you what the code DOES. When they disagree, data wins. NEVER implement a fix based solely on an agent's code reading without checking the actual system state.

## CRITICAL: Assumptions Are Not Evidence

When investigating a production issue, every link in your causal chain must be verified independently. "A is happening" + "B could cause A" does NOT mean "B is causing A." Before acting on any diagnosis:

1. **Verify your comparison is apples-to-apples** (same file, same conditions)
2. **Verify the code you suspect is actually the code that ran** (check deploy timing)
3. **Verify the metric you're reading means what you think** (Timeout on which code?)
4. **If you cannot verify all links, REPORT YOUR HYPOTHESIS — do not act on it**

A plausible explanation is not a diagnosis. "This could be the cause" means "I need more data," not "I should fix this."

## CRITICAL: Never Deflect Bugs as "Pre-existing" or "Out of Scope"

**When the user encounters a bug while using a feature you built or modified, the bug is yours.** "This was already broken" is not a diagnosis — it's a deflection. "Not caused by our changes" is irrelevant information that serves no purpose except distancing yourself from the problem.

The user owns the entire codebase. They reported a bug. The only correct responses are:
1. Diagnose the root cause
2. Report what the fix would be
3. Ask if they want it fixed now

**Never suggest deferring to a separate card or future session unless the user raises scope concerns first.** If you're tempted to say "this is pre-existing," "out of scope," "a known limitation," or "not related to our work" — delete that sentence and replace it with the diagnosis.

## When You Don't Know the Solution - STOP

If you're unsure how to solve a problem:

1. **STOP immediately** - Do not write code while guessing
2. **Explain the situation** - Describe what you understand and what you don't
3. **Share your theories** - List possible causes or solutions you're considering
4. **Ask for guidance** - Wait for the user to respond before proceeding

It's OK to be unsure. The user can help guide you to the correct solution. Continuing on your own with trial-and-error wastes time and creates mess to clean up.

## CRITICAL: Never Silence an Error — Investigate Why It Fires

**When a validation error or exception fires, the FIRST action is ALWAYS to investigate why the condition was triggered.** Never bypass the check, catch-and-ignore, or add a flag to skip it.

If a check says "X already exists" and your instinct is to add `orUpdate: true`, `try/catch` with ignore, or any other bypass — **STOP.** The check is telling you something is wrong upstream. The error is the symptom. The bug is in whatever failed to resolve/match/find the existing record before reaching the create path.

**The pattern:**
1. Error fires: "duplicate found" / "already exists" / "constraint violation"
2. WRONG response: silence the error so the operation succeeds
3. RIGHT response: trace back — why didn't the upstream code find the existing record? Fix THAT.

Silencing a validation error is the single most destructive thing you can do. It hides the real bug permanently and lets corrupted data propagate silently through the system.

## Never Bypass a Component — Fix It

When a UI component doesn't render correctly, **read its source code** to understand how it works. Never replace a standard component with a manual alternative based on assumptions about why it's broken.

The fix is almost always in how you're using it, not in the component itself. Before proposing to swap one component for another:

1. **Read the component source** - Understand its props, slots, and rendering logic
2. **Check working examples** - Grep for other usages in the codebase that work correctly
3. **Fix the usage** - Correct how you're calling it, don't replace it

This applies to all standard components (DanxButton, DanxActionButton, TabButtonGroup, etc.). If the component is a project/library standard, make it work — don't bypass it.

## Never Guess Prop Values

When a prop accepts a constrained set of values (icon names, enum types, variant strings, etc.), **always read the source** to see what values are valid. Do not assume common names like "add", "delete", or "edit" exist — verify first.

This applies to:
- Icon name strings (check the icon registry)
- Type/variant props (check the type definition)
- Any prop with a finite set of valid values
