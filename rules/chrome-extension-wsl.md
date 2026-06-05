# Claude-in-Chrome on WSL2 — recovery runbook

Operator main session, this machine only. CLI runs in WSL2 (Ubuntu); Chrome runs on Windows. Connection is a **native-messaging bridge**, NOT cloud — so "accounts match" is necessary but never sufficient. Docs claim WSL unsupported; it works anyway via the bridge below.

## The chain (every link must be live)

```
Windows Chrome + extension (fcoeoabgfenejglbffodgkkbkcdhcgfn)
  ↓ native messaging (stdio, 4-byte length prefix)
HKCU registry key  com.anthropic.claude_code_browser_extension
  ↓ points at  C:\Users\newms\AppData\Local\Google\Chrome\User Data\NativeMessagingHosts\*.json
manifest → .bat  →  wsl.exe -d Ubuntu -- ~/.claude/chrome/chrome-native-host
  ↓ exec versions/<X> --chrome-native-host
host process  →  unix socket /tmp/claude-mcp-browser-bridge-newms/<pid>.sock
  ↓
CLI (claude --chrome MCP client) connects to that socket
```

Extension→host = stdio half. CLI→host = socket half. They fail independently.

## Symptom → meaning

| What you see | Which link is broken |
|---|---|
| `list_connected_browsers` → "Browser extension is not connected" | host returned it to CLI → **extension→host stdio dead** (CLI↔host fine) |
| `/chrome` → `JSON Parse error: Unexpected identifier "Browser"` | **version mismatch** CLI vs host — host printed plaintext error, CLI tried `JSON.parse` |
| no `chrome-native-host` process running at all | extension isn't dialing Code's host (likely bound Claude **Desktop**'s host instead) |
| `/chrome` shows "Extension: Installed" | detection fine — that's the symlink, not the live connection |

## Diagnose (read-only, fast)

```bash
# host running? socket present?
ps aux | grep chrome-native-host | grep -v grep
ls /tmp/claude-mcp-browser-bridge-newms/

# wrapper pinned to CURRENT cli version?
cat ~/.claude/chrome/chrome-native-host          # exec path must match `claude --version`
ls ~/.local/share/claude/versions/

# all native hosts claiming the extension (the conflict surface)
/mnt/c/Windows/System32/reg.exe query "HKCU\Software\Google\Chrome\NativeMessagingHosts" /s

# Desktop's host manifest — does allowed_origins list fcoeoab…? (= conflict)
cat "/mnt/c/Users/newms/AppData/Roaming/Claude/ChromeNativeHost/com.anthropic.claude_browser_extension.json"

# manual chain test — should print "Socket server listening"
timeout 8 /mnt/c/Windows/System32/cmd.exe /c "C:\Users\newms\AppData\Local\Google\Chrome\User Data\NativeMessagingHosts\com.anthropic.claude_code_browser_extension.bat" </dev/null 2>&1 | head
```

## Two root causes seen (2026-06-05)

### 1. Version mismatch (CLI updated, wrapper stale)
CLI auto-updates; `~/.claude/chrome/chrome-native-host` regenerates to the new `versions/<X>` — but old host processes from before the update keep running on the old version. Chrome respawns them stale.
**Fix:** confirm wrapper exec path == `claude --version`. Kill leftover old-version `chrome-native-host` procs. Toggle extension.

### 2. Claude Desktop steals the extension (the real one — "what changed")
ONE extension ID is claimed by TWO native hosts:
- Desktop: `com.anthropic.claude_browser_extension` (its `allowed_origins` lists `fcoeoab…`)
- Code: `com.anthropic.claude_code_browser_extension`

Extension binds whichever registered first → Desktop wins → Code's host never spawns. GitHub anthropics/claude-code#24539. Triggered by an **extension auto-update** (1.0.75, 2026-06-04) changing bind order.

**Fix — disable Desktop's host so the extension falls through to Code's:**
```bash
cd "/mnt/c/Users/newms/AppData/Roaming/Claude/ChromeNativeHost"
mv com.anthropic.claude_browser_extension.json com.anthropic.claude_browser_extension.json.bak
```
Then in Chrome: `chrome://extensions` → Claude extension → toggle **OFF → ON**.

Verify: `ps aux | grep chrome-native-host` shows a host on the current version + a fresh `.sock`; `list_connected_browsers` returns a browser.

**Trade-off:** kills Claude **Desktop's** own in-Chrome sidebar while renamed. Can't run both at once. Keep the `.bak` to keep Code-chrome working. **Desktop relaunch may regenerate the manifest** → conflict returns → re-rename + toggle.

## Standard recovery order

1. `claude --version` == wrapper exec path? If not, the wrapper regen on next CLI start fixes it.
2. Kill stale-version `chrome-native-host` procs (get explicit confirm before kill — shared machine).
3. Desktop manifest renamed to `.bak`?
4. Toggle extension OFF→ON in `chrome://extensions` (NOT just close the window — service worker only dials on startup).
5. Re-probe `list_connected_browsers`.
