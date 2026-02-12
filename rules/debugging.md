# Debugging Guidelines

## Never Guess at Problems

When the user reports an error you cannot reproduce or see:

1. **Ask for clarification** - Request the actual error message, console output, or screenshot
2. **Do NOT hypothesize** what might be wrong and start "fixing" based on guesses
3. **Do NOT make speculative code changes** without understanding the actual problem

Guessing wastes time and often introduces new bugs while the original problem remains unsolved.

## When You Don't Know the Solution - STOP

If you're unsure how to solve a problem:

1. **STOP immediately** - Do not write code while guessing
2. **Explain the situation** - Describe what you understand and what you don't
3. **Share your theories** - List possible causes or solutions you're considering
4. **Ask for guidance** - Wait for the user to respond before proceeding

It's OK to be unsure. The user can help guide you to the correct solution. Continuing on your own with trial-and-error wastes time and creates mess to clean up.

## Never Bypass a Component — Fix It

When a UI component doesn't render correctly, **read its source code** to understand how it works. Never replace a standard component with a manual alternative based on assumptions about why it's broken.

The fix is almost always in how you're using it, not in the component itself. Before proposing to swap one component for another:

1. **Read the component source** - Understand its props, slots, and rendering logic
2. **Check working examples** - Grep for other usages in the codebase that work correctly
3. **Fix the usage** - Correct how you're calling it, don't replace it

This applies to all standard components (DanxButton, DanxActionButton, TabButtonGroup, etc.). If the component is a project/library standard, make it work — don't bypass it.
