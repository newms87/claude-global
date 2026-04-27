# Killing Processes

Workspace shared. Every running process may belong to user, another agent, unrelated program. Destroying any irreversible → can delete hours unsaved work. Treat `kill`, `pkill`, `kill -9`, `taskkill`, `SIGTERM`, `SIGKILL`, every other signal delivery same way: **production action, no undo**.

## The Iron Rule

May only kill process when **100% of following true**:

1. **Spawned it THIS session** (not prior session, not another agent, not user).
2. **Captured PID at spawn time** into variable in own code or notes — spawn command visible in conversation.
3. **Captured PID still exact PID about to signal** (no `ps` lookup, no pattern match, no inference from time/TTY/CPU/cwd).

Even one not satisfied → don't kill. Ask user instead. Describe what want kill + why, wait explicit action verb ("kill it," "stop it," "cancel it," "SIGTERM <pid>").

Correlation ≠ proof. Matching start time, TTY, CPU, "claude" string in command line — none evidence of ownership. Only evidence of ownership = PID personally captured at moment spawned process.

## Capture the PID at Spawn Time — Always, For Anything That Might Run >30s

Even remote chance process spawn lives >~30s → capture PID at exact moment of spawning. Examples:

- Node `child_process.spawn()` → save `child.pid` immediately
- Shell `background_cmd &` → save `$!` immediately
- Python `subprocess.Popen()` → save `proc.pid` immediately
- `wt.exe` / `wsl.exe` wrapper scripts → script write `$$` to PID file before `exec`

Lose PID → lost right to kill. Ask user. Do not reconstruct ownership from `ps`.

## Forbidden Tools

- **`pkill -f <pattern>`** — FORBIDDEN. Pattern-matching across all processes = unbounded blast radius. Never use for any reason.
- **`killall <name>`** — FORBIDDEN. Same reason.
- **`kill $(pgrep …)`** — FORBIDDEN. Same reason.
- Any shell construct killing by name, pattern, inferred ownership from `ps` — FORBIDDEN.

Only ever send signals to single PID captured yourself at spawn.

## Before Any Signal: Proof Block

Before calling `kill`/`pkill`/etc., conversation must contain Proof Block user can audit:

```
Target: PID <N>
Spawned by me at: <tool-call reference or line of code>
Captured as: <variable/note where I stored the PID>
Command I expect it to run: <exact args>
```

Cannot fill all four lines from memory of current session → don't kill. Ask.

## "It's Just Cleanup"

No such thing as "administrative" kill, "quick cleanup" kill, "obviously-mine" kill, "no one else could have that" kill, "just tidying up orphans" kill. Every signal to process not fully verified = potential destruction of someone else's work. Housekeeping not lower category of action — exactly as dangerous as production work.

When in doubt, process stays alive. Stale orphan ∞ cheaper than destroyed session.

## Correcting This File's Existence

Rule exists because agent killed user's unrelated Claude Code session by guessing ownership from `ps` columns. Cost = hours of lost context. Future agent about to reach for `kill` without Proof Block → about to repeat this incident. Stop. Ask.