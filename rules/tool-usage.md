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

### CRITICAL: Import Order — Usage First, Import Second

**Linters run after EVERY Edit/Write call.** They delete unused imports instantly. This creates a strict ordering constraint:

1. **First Edit:** Add the method/code that REFERENCES the new class or module
2. **Second Edit:** Add the `use`/`import` statement at the top of the file

**NEVER add imports before the usage code exists in the file.** The linter will delete the import before your next edit runs, and subsequent code will resolve to the wrong namespace (e.g., `Model` resolves to `App\Repositories\Model` instead of `Illuminate\Database\Eloquent\Model`, causing a fatal error).

This applies to ALL languages — PHP (Pint), TypeScript (ESLint), Vue, Python, etc. When adding a new class to an `applyAction` override, an `import { Foo }`, or any cross-file reference: write the body first, imports second. No exceptions.

## CRITICAL: Read MCP Tool Schemas Before Calling

**Never guess MCP tool parameters. Always verify required parameters from the schema returned by ToolSearch.**

MCP tools from the same service often have inconsistent interfaces — one tool may identify resources by name, another by ID. Pattern-matching from similar tools causes silent failures. Read the schema every time.

**Trello checklist updates:** `update_checklist_item` requires `checkItemId` (the ID returned when the item was created). It does NOT accept name-based lookup like `add_checklist_item`. Save creation IDs and reference them for updates.

## Browser Automation: Use Claude in Chrome

**Always use `mcp__claude-in-chrome__*` tools for browser automation. Never use `mcp__playwright__*` tools.**

Start with `tabs_context_mcp` to get available tabs, then create a new tab with `tabs_create_mcp`. Use `navigate` to load pages, `computer` with `action: "screenshot"` to see the page, `read_page` for accessibility tree, and `computer` with click/type actions to interact. Use `read_console_messages` with a `pattern` filter for debugging.

## NEVER Read or Edit dist/ Directories

**Pretend `dist/` directories do not exist. NEVER read, search, or edit files in `dist/`.**

We are always editing locally with HMR. `dist/` is a stale build artifact that has no effect on what we see in the browser. If you find something in `dist/`, ignore it — the answer is always in `src/`.

**`node_modules/`**: Reading is OK for understanding dependencies. Editing is NEVER OK.
