# Monitor & Poll-Loop Intervals

Polling has cost. Each iteration of a `Monitor` or `until` loop spawns a process, opens DB/network connections, and emits a chat notification that consumes user attention and context window. Cheap per-tick locally feels free; on backend jobs it isn't. This rule sets hard floors so the cost matches the signal.

## The Iron Rule

**Floor for poll intervals when waiting on backend jobs (artisan, queue worker, LLM call, agent dispatch, schema/template builder, octane, horizon, dispatch round-trip): 60 seconds. Period.**

15s and 30s are forbidden for these. Each iteration:
- Cold-boots an interpreter (`./vendor/bin/sail artisan` ≈ 1–3s of PHP boot)
- Opens DB connections (already proven fragile — `too many clients already` is a known failure mode in this stack)
- Emits a chat notification that costs context tokens AND user focus
- Adds load to the exact system you're waiting on

A multi-minute job polled every 15s = ~10x the useful signal rate. Pure noise.

## Decision Tree — Run This BEFORE Arming Any Monitor

Answer the question literally before you reach for the Monitor tool:

1. **"Tell me ONCE when X finishes"** → use `Bash` with `run_in_background: true` and an `until <terminal-state>; do sleep <interval>; done` one-shot. NEVER use `Monitor` for this. You get one notification at completion, zero spam.

2. **"Tell me on STATE CHANGES only"** → `Monitor` with a `prev`/`cur` diff. Emit only when `cur != prev`. The poll still runs at the floor interval, but emissions are bounded by real transitions.

3. **"Tell me every line of a stream"** (log tail, build output, console errors) → `Monitor` with `tail -f <file> | grep --line-buffered <pattern>`. The pattern alternation MUST cover every terminal state you'd act on, not just the happy path (see `Coverage` below).

4. **"I want progress feedback"** → that's narration, not signal. It is not a real requirement. Use Option 1.

If the answer to "what do I need" is "Option 1," you must NOT use `Monitor`. Reaching for `Monitor` when `Bash run_in_background` is correct is the failure mode this rule exists to prevent.

## Interval Floor Table

| What you're polling | Minimum interval |
|---|---|
| Local trivial check (file exists, port open, lock file present) | 1–5s |
| Local process state (`docker ps`, `pgrep`, `ps`) | 10–15s |
| Local file content (small file, no boot, no DB) | 5–10s |
| Backend job state (`artisan`, queue length, DB query, container exec) | **60s** |
| LLM job / agent dispatch / multi-stage orchestrator | **60–120s** |
| Remote API (`gh`, Slack, OpenAI, Trello) | 30–60s (rate limits) |

Pick from this table. Do NOT invent your own number "because this one's different."

## The Load-Failure Override

**If you have already seen the system you're polling fail under load in this session, the floor doubles.** A `too many clients already` from PG, a queue worker exhaustion, a Horizon supervisor death, a 429 from a remote API — any of these means the system is fragile right now. Polling it is adding load to a sick system. 60s becomes 120s. 30s becomes 60s. If in doubt, stop polling and check on demand.

This is the rule that catches "but I already saw the DB die five minutes ago and I'm still going to hammer it every 15 seconds" — exactly the failure that produced this rule.

## Coverage — Silence Is Not Success

If your `Monitor` filter only matches the happy path, a crash looks identical to "still running" and you wait until timeout for nothing. Every Monitor command must, in one alternation, cover:

- Forward progress signal (the line you'd celebrate)
- Every terminal failure signature you'd act on (`Traceback`, `Error`, `FAILED`, `Killed`, `OOM`, `assert`, language-specific panic markers)
- Process death (use `; echo "EXITED: $?"` after a `tail -f` if relevant)

When in doubt, broaden the alternation. Some extra noise beats missing a crashloop.

## Notification Cost Is Real

Every `echo` line in a `Monitor` script becomes a chat message. Chat messages:
- Eat the user's input tokens permanently for the rest of the session
- Eat the user's attention (they read each one)
- Risk hitting the "too many events → monitor auto-stopped" guardrail

Emit ONLY lines the user would act on. `tick: Running` repeated 30 times is not an action signal — it's narration. Cut it.

## Why This Rule Exists

In a session debugging a hung extraction, the agent:
1. Triggered a worker storm by hitting `--rerun` on a 21-process orchestrator
2. Saw `too many clients already` from Postgres seconds later
3. Set up a `Monitor` polling that exact same DB every 15 seconds via `artisan` (Laravel cold-boot + DB connection per tick)
4. Emitted `tick: Running` notifications until the user manually interrupted

Every individual decision felt locally rational ("I want to know when it finishes," "15s feels responsive"). The aggregate was: hammering a sick DB while flooding chat with noise the user explicitly didn't want. The rule above mechanically blocks that pattern by forcing a 60s floor for backend jobs and pushing single-shot waits to `Bash run_in_background` instead of `Monitor`.

## Mechanical Pre-Arm Check

Before EVERY `Monitor` call, answer in writing (in your reasoning, in the description, somewhere visible):

1. **Need:** "Tell me once" / "tell me on changes" / "tell me every line"?
2. **Tool:** Did the decision tree above route me to `Bash run_in_background`? If yes, I am NOT using `Monitor`.
3. **Interval:** What table row am I in? What's my floor?
4. **Load override:** Have I seen this system fail under load this session? If yes, doubled?
5. **Coverage:** Does my filter emit on terminal failure modes, not just success?

Skipping this check is how the original failure happened. The check IS the prevention.
