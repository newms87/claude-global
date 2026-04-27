# Environment Rules

## Always cd First

Before running git, build tools, or any project command, ALWAYS cd into the expected directory first. Working directory state is unreliable — always be explicit: `cd /path/to/project && git status`.

## Relative Paths Only

Absolute paths are forbidden in all bash commands. They require manual approval and break autonomous operation. Always use relative paths (`./vendor/bin/sail test`, `yarn build`). If a command fails, check `pwd` first — never switch to absolute paths as a fix.

## "Locally" means the LOCAL dev stack, not "from my terminal"

When the user says "locally", "local", "on my machine", or "the local X" (worker, poller, dashboard, API, container), they mean the development stack running on THIS HOST — `docker ps`, `docker logs`, `make logs`, `localhost:<port>`. They do NOT mean "from my terminal running commands against production." Default to local every time. Check `docker ps` first to see what's running locally. Only touch production when the user explicitly says "prod", "production", "deployed", or names the deployment target (e.g. "on gpt", "on the EC2 instance"). This rule exists because SSHing into prod feels equivalent to an agent ("it's still my terminal") but is categorically different from the user's mental model — they meant the stack, you defaulted to the shell.

## Everything Is Immediate (HMR)

This is a local dev environment. PHP/Laravel changes apply instantly. Vue/TypeScript uses Vite HMR. CSS/Tailwind updates instantly. Only run production builds when explicitly requested for final validation.

## Never Ask About Environment

The user's environment is identical to yours. HMR means every saved file is live instantly. Never ask "which commit?", "which environment?", or "can you confirm your setup?" — investigate the code instead.

## Long-Running Commands: Background Only

Commands matching these patterns MUST use `run_in_background: true` with NO timeout: `make backtest`, `make hyperopt`, `make monthly-opt`, `make adaptive-*`, `make analyze`, `make signal-stability`, `make gate-analysis`, `make sweep-thresholds`, `make feature-importance`, `docker compose run.*freqtrade`. Check if a previous instance is running before launching (`docker top` for containerized commands). Wait for the background completion notification — do NOT poll or launch duplicates. If the first attempt appears stuck, verify with `docker top` before launching another — competing CPU-bound processes make each one 3x slower.

## One Environment — Files Exist Everywhere or Nowhere

Docker containers are volume-mounted to the host. Host files = container files. There is no "host version" vs "container version." If you write a file, it exists everywhere. If "file not found," your path is wrong — that is the answer 99.99% of the time. Run `pwd`, fix the path. Never search the filesystem for a file you already know the path to, try container paths when host paths fail, or hypothesize about partial clones.

## Docker Containers: Just Start Them

A stopped container is not broken infrastructure. `docker compose up -d` and continue. Never install dependencies on the host, run project scripts on the host, or try alternatives that bypass the container.

## Async Commands Require ScheduleWakeup

When you run an async command (agent dispatch, background job, any process that returns immediately while work continues), you MUST call `ScheduleWakeup` to check on it later. You have no ability to spontaneously act — without a timer, the process sits unobserved indefinitely. "I'll check back in N minutes" without a `ScheduleWakeup` call is a lie. The pattern is: dispatch → confirm launched → `ScheduleWakeup` → verify on wake → next step.

## Never Edit node_modules

Reading `node_modules/` is OK for understanding dependencies. Editing is NEVER OK.
