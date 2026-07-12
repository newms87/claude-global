# MCP server config — precedence + debugging (main session)

Operator main-session only. Dispatched agents use injected configs and never debug this.

## The effective config is `~/.claude.json`, NOT repo `.mcp.json`

A server added via `claude mcp add` (local scope) is stored under
`~/.claude.json` → `projects.<repo-path>.mcpServers.<name>`. That **local-scope
entry SHADOWS the repo's `.mcp.json`** for the same server name. Editing
`.mcp.json` is then a **no-op** — the values Claude actually spawns the server
with come from `~/.claude.json`.

**Before editing any MCP server config, check which file actually owns it:**

```bash
python3 -c "import json;d=json.load(open('/home/newms/.claude.json'));print(json.dumps(d['projects']['<repo-path>']['mcpServers'],indent=2))"
```

If the server is there, edit it there (back up first: `cp ~/.claude.json ~/.claude.json.bak`).
Reconnect via `/mcp` re-reads `~/.claude.json` — no full restart needed.

A working sibling project's entry is the reference shape — diff its env block
against the broken one; the missing key is usually the whole bug.

## `-32000` (or any reconnect failure) — read the real error, don't guess

`-32000` is a generic JSON-RPC server error. Running the server binary manually
WITHOUT the env Claude injects reproduces a *different* failure — do not
pattern-match that onto the live error. Confirm the real cause from:

- the spawn-with-real-env reproduction (set every env key the config sets), or
- `~/.cache/claude-cli-nodejs/<repo-path>/mcp-logs-<server>/`.

Asserting a cause before reading one of those = the documented failure mode.
