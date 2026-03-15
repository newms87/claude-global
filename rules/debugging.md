# Debugging Guidelines

## Never Guess at Problems

When the user reports an error you cannot reproduce or see:

1. **Ask for clarification** - Request the actual error message, console output, or screenshot
2. **Do NOT hypothesize** what might be wrong and start "fixing" based on guesses
3. **Do NOT make speculative code changes** without understanding the actual problem

Guessing wastes time and often introduces new bugs while the original problem remains unsolved.

## Prove the Bug Before Fixing It

**NEVER fix a suspected bug without proving it first.** Finding suspicious code is not enough — you must confirm it's the actual cause.

1. **Write a failing test** that reproduces the exact bug behavior, OR set up a minimal experiment that demonstrates the failure
2. **Run it** — verify it fails for the reason you expect
3. **Only then fix the code**
4. **Re-run** — confirm the test passes / experiment succeeds

If you can't reproduce the bug, you don't understand it yet. Go back to investigation. Fixing code that "looks wrong" without proof leads to unnecessary changes that don't solve the real problem and may introduce new ones.

**Agent investigation results are hypotheses, not proof.** When a subagent reports "X is never set" or "Y doesn't exist," verify with empirical data before acting. Run a database query. Check actual runtime values. Agent code analysis tells you what the code SAYS — only data tells you what the code DOES. When they disagree, data wins. NEVER implement a fix based solely on an agent's code reading without checking the actual system state.

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
