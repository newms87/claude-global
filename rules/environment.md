# Environment Rules

## Always cd First

Before running git, build tools, or any project command, ALWAYS cd into the expected directory first. Working directory state is unreliable — always be explicit: `cd /path/to/project && git status`.

## Relative Paths Only

Absolute paths are forbidden in all bash commands. They require manual approval and break autonomous operation. Always use relative paths (`./vendor/bin/sail test`, `yarn build`). If a command fails, check `pwd` first — never switch to absolute paths as a fix.

## Everything Is Immediate (HMR)

This is a local dev environment. PHP/Laravel changes apply instantly. Vue/TypeScript uses Vite HMR. CSS/Tailwind updates instantly. Only run production builds when explicitly requested for final validation.

## Never Ask About Environment

The user's environment is identical to yours. HMR means every saved file is live instantly. Never ask "which commit?", "which environment?", or "can you confirm your setup?" — investigate the code instead.

## Long-Running Commands: Background Only

Commands matching these patterns MUST use `run_in_background: true` with NO timeout: `make backtest`, `make hyperopt`, `make monthly-opt`, `make adaptive-*`, `docker compose run.*freqtrade`. Check if a previous instance is running before launching. Wait for the background completion notification — do NOT poll or launch duplicates.

## One Environment — Files Exist Everywhere or Nowhere

Docker containers are volume-mounted to the host. Host files = container files. There is no "host version" vs "container version." If you write a file, it exists everywhere. If "file not found," your path is wrong — that is the answer 99.99% of the time. Run `pwd`, fix the path. Never search the filesystem for a file you already know the path to, try container paths when host paths fail, or hypothesize about partial clones.

## Docker Containers: Just Start Them

A stopped container is not broken infrastructure. `docker compose up -d` and continue. Never install dependencies on the host, run project scripts on the host, or try alternatives that bypass the container.

## Never Edit node_modules

Reading `node_modules/` is OK for understanding dependencies. Editing is NEVER OK.
