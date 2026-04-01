# Collaboration Rules

## CRITICAL: Questions Are Not Directives

When the user asks a question ("does that affect X?", "why did Y happen?", "what about Z?"), the ONLY correct response is a text explanation.

A question means:
- DO NOT modify any code
- DO NOT cancel or restart any running process
- DO NOT kill services or containers
- DO NOT start new operations
- DO NOT commit, push, or stage changes
- DO NOT take ANY action that modifies system state

A question means RESPOND WITH TEXT ONLY.

Before every tool call, ask: "Did the user ask a question or give a directive?" If the last user message contains a question mark and no action verb (fix, do, run, implement, go ahead, make it), respond with text only. When in doubt, it's a question — explain and wait.

## CRITICAL: Mistakes Are Questions, Not Instructions

When the user points out that you did something wrong — even if the fix seems obvious — STOP. Do not revert, undo, or fix anything. The user is asking you to understand what went wrong, not to scramble. Answer their question fully, then wait for explicit direction on how to proceed.

- "What does that tell you?" = explain your reasoning
- "That was wrong" = acknowledge and wait
- "Revert that" = now you can revert (using Edit, not git checkout)

## CRITICAL: Never Cancel Running Processes

Never cancel a running process (hyperopt, backtest, download, docker service) unless the user explicitly says "kill it", "stop it", "cancel it." A running process represents time investment. Killing it without permission wastes that time.

## CRITICAL: Concept Approval ≠ Implementation Approval

"Sounds good" or "yes" to an idea is NOT permission to implement it. The next step is to present the specific implementation plan — what files change, what the code looks like, what the expected impact is. Only implement after the user says "go ahead" to the specific plan.

This applies doubly when a hyperopt or backtest is running — never change strategy code during a running optimization.

## CRITICAL: Never Create Separate Strategies

When the user asks to add features to an existing strategy, edit the existing strategy file. "Incorporate X into our strategy" means add to the existing strategy, not create a new file. The existing strategy has all the tooling integration.

## All Entry Conditions Must Be Visible in UI

Every condition that affects entry (gates, suppression flags, scores) MUST be visible in the analyzer UI. If a candle shows "ENTER" in the score box but doesn't have an entry marker, the user cannot diagnose why. Hidden blockers waste hours of debugging.

Never add an invisible gate or suppression flag to entry conditions.
