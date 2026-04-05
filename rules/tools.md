# Tool Usage Rules

## File Operations

**ALWAYS use Write and Edit tools. NEVER use bash commands for file ops.**

| Operation | Tool | Never Use |
|-----------|------|-----------|
| Create file | Write | `echo >`, `cat <<EOF`, `printf` |
| Edit file | Edit | `sed`, `awk`, `perl -i` |
| Read file | Read | `cat`, `head`, `tail` |
| Search files | Glob | `find`, `ls` |
| Search content | Grep | `grep`, `rg` |

**Workflow:** Read first (required before Edit) → Edit → hooks lint automatically.

## Edit Failures

If Edit match fails, reduce `old_string` to 2-5 lines (smaller strings have fewer whitespace mismatches).

**If Edit/Write fails repeatedly: STOP.** Do NOT rewrite entire file with Write, use Bash as fallback, or invent workarounds. Either the file cannot be edited (system issue) or you're not supposed to edit it. Report the failure and proceed without that edit if possible.

## Import Order

Linters delete unused imports after EVERY Edit/Write. Strict ordering: **Usage first, imports second.** Add code that REFERENCES a new class, then add the import statement. Never add imports before the usage exists — the linter will delete it and subsequent code resolves to wrong namespace.

## Lint

Hooks run automatically after Write/Edit. Never run lint manually — it's redundant.

## MCP Tools

Never guess parameters. Always read the schema from ToolSearch before calling. MCP tools have inconsistent interfaces — one tool identifies by name, another by ID. Trello example: `update_checklist_item` requires `checkItemId` (not name), so save creation IDs.

## Browser Automation

Use `mcp__claude-in-chrome__*` tools only, never Playwright. Start with `tabs_context_mcp`, then `tabs_create_mcp`, `navigate`, `computer` (screenshot/click/type), `read_page` (accessibility tree), `read_console_messages` (with pattern filter).

## dist/ and node_modules/

Never read, search, or edit `dist/` — it's a stale build artifact. HMR makes `src/` the source of truth.

Reading `node_modules/` is OK for understanding dependencies. Editing is NEVER OK.

## Refactoring Tools

Use language-specific refactoring tools for cross-file renames/moves — they update all references automatically. Manual find-and-replace is error-prone.

- **PHP:** `phpactor class:move src/Old/Path/Class.php src/New/Path/Class.php`
- **TypeScript/JavaScript:** `ts-morph` or IDE refactoring
- **Go:** `gorename`, `gopls rename`
- **Python:** `rope`, `jedi`

Use for: renaming classes/functions across files, moving to different namespaces, any cross-file reference updates.

## Markdown Tables in Output

Keep total row width under ~140 characters in CLI output. Use abbreviations + icons (e.g., `✏️ M` not "Modified"). Prefer more rows over wider rows.
