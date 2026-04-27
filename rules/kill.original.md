# Killing Processes

The workspace is shared. Every running process may belong to the user, another agent, or an unrelated program. Destroying any of them is irreversible and can delete hours of unsaved work. Treat `kill`, `pkill`, `kill -9`, `taskkill`, `SIGTERM`, `SIGKILL`, and every other signal delivery the same way: **a production action with no undo**.

## The Iron Rule

You may only kill a process when **100% of the following are true**:

1. **You spawned it in THIS session** (not in a prior session, not by another agent, not by the user).
2. **You captured its PID at spawn time** into a variable in your own code or notes — with the spawn command visible in the conversation.
3. **That captured PID is still the exact PID you are about to signal** (no `ps` lookup, no pattern match, no inference from time/TTY/CPU/cwd).

If even one of those three is not satisfied, you do not kill. Ask the user instead. Describe what you want to kill and why, and wait for an explicit action verb ("kill it," "stop it," "cancel it," "SIGTERM <pid>").

Correlation is not proof. Matching start time, matching TTY, matching CPU, matching the string "claude" in the command line — none of these are evidence of ownership. The only evidence of ownership is a PID you personally captured at the moment you spawned the process.

## Capture the PID at Spawn Time — Always, For Anything That Might Run >30s

If there is even a remote chance a process you spawn will live longer than ~30 seconds, capture its PID at the exact moment of spawning. Examples:

- Node `child_process.spawn()` → save `child.pid` immediately
- Shell `background_cmd &` → save `$!` immediately
- Python `subprocess.Popen()` → save `proc.pid` immediately
- `wt.exe` / `wsl.exe` wrapper scripts → have the script write `$$` to a PID file before `exec`

If you lose the PID, you have lost the right to kill. Ask the user. Do not reconstruct ownership from `ps`.

## Forbidden Tools

- **`pkill -f <pattern>`** — FORBIDDEN. Pattern-matching across all processes has unbounded blast radius. Never use it for any reason.
- **`killall <name>`** — FORBIDDEN. Same reason.
- **`kill $(pgrep …)`** — FORBIDDEN. Same reason.
- Any shell construct that kills by name, pattern, or inferred ownership from `ps` — FORBIDDEN.

Only ever send signals to a single PID that you captured yourself at spawn.

## Before Any Signal: Proof Block

Before calling `kill`/`pkill`/etc., the conversation must contain a Proof Block the user can audit:

```
Target: PID <N>
Spawned by me at: <tool-call reference or line of code>
Captured as: <variable/note where I stored the PID>
Command I expect it to run: <exact args>
```

If you cannot fill in all four lines from memory of the current session, you do not kill. Ask.

## "It's Just Cleanup"

There is no such thing as an "administrative" kill, a "quick cleanup" kill, an "obviously-mine" kill, a "no one else could have that" kill, or a "just tidying up orphans" kill. Every signal to a process you did not fully verify is a potential destruction of someone else's work. Housekeeping is not a lower category of action — it is exactly as dangerous as production work.

When in doubt, the process stays alive. A stale orphan is infinitely cheaper than a destroyed session.

## Correcting This File's Existence

This rule exists because an agent killed the user's unrelated Claude Code session by guessing ownership from `ps` columns. The cost was hours of lost context. If a future agent finds themselves about to reach for `kill` without a Proof Block, that agent is about to repeat this incident. Stop. Ask.
