# Tool Usage Rules

## CRITICAL: File Editing Tools

**ALWAYS use the Write and Edit tools for file operations. NEVER use bash commands.**

### Required Tool Usage

| Operation | Tool | NEVER Use |
|-----------|------|-----------|
| Create new file | Write | `echo >`, `cat <<EOF`, `printf` |
| Edit existing file | Edit | `sed`, `awk`, `perl -i` |
| Read file | Read | `cat`, `head`, `tail` |
| Search files | Glob | `find`, `ls` |
| Search content | Grep | `grep`, `rg` |
| Output text | Direct output | `echo`, `printf` |

### Why This Matters

- **Write/Edit tools are linted automatically** via Claude Code hooks
- **Bash edits bypass linting** and can introduce formatting errors
- **Read tool preserves context** for the Edit tool

### Workflow

1. **Read** the file first (required before Edit)
2. **Edit** with precise old_string/new_string replacement
3. **Linting runs automatically** via PostToolUse hook — NEVER run lint manually

### Edit Failures: Reduce Match Size, Then STOP

If an Edit match fails, **reduce the old_string to fewer lines** (2-5 lines is usually enough). Smaller strings have fewer invisible whitespace mismatches.

**If Edit/Write fails after multiple attempts: STOP ALL OPERATIONS.**

This is a **CRITICAL SYSTEM FAILURE**.

- **DO NOT** rewrite the entire file with Write to bypass a failed Edit
- **DO NOT** use Bash (`sed`, `echo >`, `cat <<EOF`) as a fallback
- **DO NOT** invent any creative workaround to write to files

Either you are not supposed to be editing that file, or there is a critical system error. If you can continue your task without that edit, proceed. Otherwise, stop immediately and report the failure to the user.

### NEVER Run Lint Manually

The PostToolUse hook runs lint on every file after Write/Edit. Running lint as a separate Bash command is redundant. Trust the hooks.

### Add Imports and Usage in the Same Edit

Linters remove unused imports automatically after each Write/Edit. If you add an import in one edit, the linter runs and deletes it before you add the code that uses it.

**Always write the code that USES the import first, then add the import.** Never add imports before the usage exists in the file. This applies to all languages — PHP (Pint), TypeScript (ESLint), Vue, Python, etc.

## NEVER Read or Edit dist/ Directories

**Pretend `dist/` directories do not exist. NEVER read, search, or edit files in `dist/`.**

We are always editing locally with HMR. `dist/` is a stale build artifact that has no effect on what we see in the browser. If you find something in `dist/`, ignore it — the answer is always in `src/`.

**`node_modules/`**: Reading is OK for understanding dependencies. Editing is NEVER OK.
