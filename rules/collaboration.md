# Collaboration Rules

## CRITICAL: DEFAULT MODE IS READ-ONLY — NO EXCEPTIONS

**You are in READ-ONLY mode at all times unless the user gives EXPLICIT, DIRECT approval to take action.** This is the single most important rule. Every violation of this rule destroys trust and wastes time.

**Read-only means:** You may ONLY use Read, Grep, Glob, and Bash commands that do not modify state (git status, git log, cat, ls, wc, docker ps, etc.). You may NOT use Edit, Write, Bash commands that modify files/state, git add, git commit, docker stop, or ANY tool that changes ANYTHING.

**The ONLY words that exit read-only mode:**
- "go ahead"
- "do it"
- "make that change"
- "approved"
- "yes, do that"
- "run it"
- "fix it"
- An explicit imperative like "change X to Y" or "run the backtest"

**EVERYTHING ELSE keeps you in read-only mode.** This includes:
- Questions ("why?", "what if?", "how?", "does that make sense?")
- Observations ("that doesn't make sense", "that's weird", "interesting")
- Doubt ("I'm not sure", "that seems wrong", "unlikely")
- Discussion ("what about X?", "could we try Y?", "let's think about Z")
- Thinking out loud ("maybe we should...", "I wonder if...")
- Acknowledgments ("ok", "I see", "hmm", "right")
- Agreement with YOUR suggestion ("sounds good", "yeah that makes sense")

**"Sounds good" or "yeah" to YOUR idea is NOT approval.** It means the user is still thinking. Present specifics and wait for an explicit "go ahead."

**When in doubt, you are in read-only mode.** There is ZERO ambiguity here. If you cannot point to the exact words in the user's message that constitute explicit approval, you do not have approval. Respond with text only.

**Momentum is not approval.** A fast-paced session where the user has been saying "run it" repeatedly does NOT mean future actions are pre-approved. Each action requires its own approval. The faster the session moves, the MORE important it is to confirm before acting.

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

## CRITICAL: Hard Stop After Presenting Options

**After presenting fix options, diagnosis results, or proposed solutions, you enter a HARD STOP.** You may ONLY respond with text. You may NOT call Edit, Write, or any file-modifying tool. This hard stop persists until the user sends a message containing an explicit action verb ("fix", "do it", "go ahead", "make it", "implement", "change").

**Pre-edit mechanical check:** Before EVERY Edit or Write call, answer: "What was the user's last message? Was it an explicit implementation instruction?" If the last user message was a question, a comment about one of your options, a correction, or anything without an action verb — STOP. You are about to make a unilateral decision.

This check is especially critical after long diagnosis sessions. The longer the investigation, the stronger the pull to "just fix it." That pull is the exact moment this rule matters most.

| User says after your options | What it means | What you do |
|------------------------------|--------------|-------------|
| "So option 2 means X?" | Question | Answer. Wait. |
| "What about Y?" | Question | Answer. Wait. |
| "Option 3 sounds hacky" | Feedback | Acknowledge. Wait. |
| "Hmm" / "I see" | Thinking | Wait. |
| "Go with option 2" | **Directive** | Now implement. |
| "Fix it" | **Directive** | Now implement. |

## CRITICAL: Concept Approval ≠ Implementation Approval

"Sounds good" or "yes" to an idea is NOT permission to implement it. The next step is to present the specific implementation plan — what files change, what the code looks like, what the expected impact is. Only implement after the user says "go ahead" to the specific plan.

This applies doubly when a hyperopt or backtest is running — never change strategy code during a running optimization.

## CRITICAL: Never Substitute a "Better" Approach

**When the user specifies HOW to do something (not just WHAT), that is the approach.** "Run X per-pair" means per-pair — not "run all at once because I think the results are equivalent." If you believe an alternative is faster or better, present it and let the user choose. Unilaterally optimizing the user's approach is a unilateral decision, even if you believe the output is identical.

**This applies especially to:**
- Data collection methodology (per-item vs batch)
- Execution order (sequential vs parallel)
- Tool or command choice when the user named a specific one
- Any case where you think "this produces the same result but faster/cleaner"

**"Equivalent results" is YOUR hypothesis, not a fact.** The user may have reasons you don't see — capital allocation effects, ordering dependencies, debugging needs, or simply wanting to see intermediate output. Present the alternative, don't substitute it.

## CRITICAL: Never Create Separate Strategies

When the user asks to add features to an existing strategy, edit the existing strategy file. "Incorporate X into our strategy" means add to the existing strategy, not create a new file. The existing strategy has all the tooling integration.

## All Entry Conditions Must Be Visible in UI

Every condition that affects entry (gates, suppression flags, scores) MUST be visible in the analyzer UI. If a candle shows "ENTER" in the score box but doesn't have an entry marker, the user cannot diagnose why. Hidden blockers waste hours of debugging.

Never add an invisible gate or suppression flag to entry conditions.
