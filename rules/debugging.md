# Debugging

**Full debugging discipline lives in `debugging` skill, not here.** Invoke via Skill tool at any trigger below. No exceptions, no minimum bug size, no "explanation mode" exemption.

## Triggers

**Bug / error / unexpected state.** Failing test, error, unexpected value, user report, "that's odd" thought, stack trace, stuck job, silent failure. Classic debugging surface.

**Investigation.** User says "investigate," "look into," "find out," "dig into," "figure out," "trace," "audit," "check on," "look at." User asks "why is X happening?", "how does Y work?", "what's going on with Z?", "is the agent running?", "did it dispatch?", or any question requiring reading + synthesizing evidence to answer.

**Factual assertion about local system behavior.** About to state:
- Timing / latency / performance ("takes Xms," "is slow," "fine on healthy system")
- What code does in paraphrase (not direct quotation)
- Causality ("failed because X," "root cause is Y," "this happens when Z")
- Why local design choice exists, when answer requires more than quoting docstring
- What config value, timeout, env var, threshold means in practice
- Whether process running / job ran / service responsive
- Comparison of runtime behavior under different conditions (cold/warm, healthy/loaded, before/after)

Reaching for "probably," "typically," "usually," "on the order of," "a matter of," "cold start," "warm system," or any hedge about local behavior — STOP. Hedge = tell. Invoke skill, measure, report numbers.

## What Is NOT a Trigger

Direct file reads where answer = quotation or literal value ("function X takes three args: a, b, c", "the const is set to 2000") — normal lookups covered by `Verify, never guess` rule. Line: **answer contains any claim not directly quotable from code, docs, or tool result captured in this conversation → making assertion + skill required.**

## Why No Methodology Lives Here

File intentionally contains no phases, no checklist, no forbidden patterns. Duplicating content would let me read this file + skip skill — defeats point. Skill creates TodoWrite checklist that IS workflow.

Need debugging guidance → need skill. Call it.