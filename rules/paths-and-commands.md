# Paths and Commands

## CRITICAL: Always cd First

**Before running git, build tools, or any project command, ALWAYS cd into the expected directory first.**

Working directory state is unreliable. Previous commands may have changed it. Always be explicit:

```bash
cd /path/to/project && git status
cd /path/to/project && yarn build
```

Never assume you're in the right directory. Never run project commands without the `cd &&` prefix.

## CRITICAL: RELATIVE PATHS ONLY - NO EXCEPTIONS

**ABSOLUTE PATHS ARE FORBIDDEN IN ALL BASH COMMANDS**

This is a blocking requirement - absolute paths require manual approval and break autonomous operation.

### ALWAYS use relative paths:
- `./vendor/bin/sail test`
- `yarn build`
- `yarn test`

### NEVER use absolute paths:
- `/home/user/project/...`
- Any path starting with `/home/`, `/Users/`, `/var/`, etc.

### If your command fails due to wrong directory:
1. First, verify you're in the project root
2. Use `pwd` to check current directory
3. NEVER switch to absolute paths as a "fix"

## Development Environment: Everything Is Immediate

**This is a local dev environment. NEVER think about production builds.**

All code changes are reflected immediately:
- **PHP/Laravel**: Interpreted — changes apply instantly
- **Vue/TypeScript**: Vite HMR — changes apply instantly
- **CSS**: Tailwind + Vite — instant updates

Only run production builds (`yarn build`) for final validation before committing, and only when requested.

## NEVER Ask About Environment or Commit State

**The user's environment is identical to yours.** HMR means every saved file is live instantly. There is no separate deployment, no other server, no other branch.

- NEVER ask "which commit are you on?" — your files ARE their files
- NEVER ask "which environment?" — there is only one: local dev with HMR
- NEVER ask "can you confirm your setup?" — you can read every file they see
- If something doesn't work, **investigate the code**, don't question the environment

## NEVER Edit node_modules

**`node_modules/`**: Reading is OK for understanding dependencies. Editing is NEVER OK.
