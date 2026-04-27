# Debugging

**The full debugging discipline lives in the `debugging` skill, not here.** Invoke it via the Skill tool at any of the following triggers. No exceptions, no minimum bug size, no "explanation mode" exemption.

## Triggers

**Bug / error / unexpected state.** Failing test, error, unexpected value, user report, "that's odd" thought, stack trace, stuck job, silent failure. The classic debugging surface.

**Investigation.** User says "investigate," "look into," "find out," "dig into," "figure out," "trace," "audit," "check on," "look at." User asks "why is X happening?", "how does Y work?", "what's going on with Z?", "is the agent running?", "did it dispatch?", or any question that requires reading and synthesizing evidence to answer.

**Factual assertion about local system behavior.** You are about to state:
- Timing / latency / performance ("takes Xms," "is slow," "fine on a healthy system")
- What code does in paraphrase (not direct quotation)
- Causality ("failed because X," "root cause is Y," "this happens when Z")
- Why a local design choice exists, when the answer requires more than quoting a docstring
- What a config value, timeout, env var, or threshold means in practice
- Whether a process is running / a job ran / a service is responsive
- Comparison of runtime behavior under different conditions (cold/warm, healthy/loaded, before/after)

If you find yourself reaching for "probably," "typically," "usually," "on the order of," "a matter of," "cold start," "warm system," or any hedge about local behavior — STOP. That hedge is the tell. Invoke the skill, measure, report numbers.

## What Is NOT a Trigger

Direct file reads where the answer is a quotation or literal value ("function X takes three args: a, b, c", "the const is set to 2000") — those are normal lookups covered by the `Verify, never guess` rule. The line: **if your answer contains any claim not directly quotable from code, docs, or a tool result captured in this conversation, you are making an assertion and the skill is required.**

## Why No Methodology Lives Here

This file intentionally contains no phases, no checklist, no forbidden patterns. Duplicating that content would let me read this file and skip the skill — defeating the point. The skill creates the TodoWrite checklist that IS the workflow.

If you need debugging guidance, you need the skill. Call it.
