# Tabbed tracker artifact — template

A self-contained "living tracker" Artifact: tabs (Open / Plan / Decided / Runs) with live
counts, a search box filtering every field, light/dark theme, and card layouts built around
one rule — **actionable content is never hidden behind a click.**

## When to use this

Any time you're about to publish a multi-item status/decision page instead of a one-off
report — a session handoff, an open-questions tracker, a build log the operator checks back
on. If the content is a single narrative or a single deliverable, this is the wrong shape;
just write a normal artifact. Load the `artifact-design` skill first regardless — this
template is a starting point for the HTML, not a replacement for that skill's judgment on
whether an artifact is warranted at all and how much design investment it's worth.

## The one rule that matters: card anatomy

A card has two zones, and mixing them up is the single most common mistake:

- **Top of the card, always visible, no click required:** a numbered `needs` list (concrete
  steps the human should take) and/or `solutions` (named options, each with a pros/cons
  breakdown collapsed *within* itself — that inner collapse is fine, it's a side-by-side
  comparison table, not the ask). For a `DECIDED` card, `resolution` (what actually happened)
  goes here too.
- **Bottom of the card, collapsed under "Background":** `context` — the problem statement,
  history, why this came up. Pure background. If a reader must act on it or decide something
  because of it, it does not belong here — move it into `needs` or `solutions`.

The failure mode this prevents: burying a numbered list of asks for the human inside a
collapsed "Problem + example" toggle, where it reads as optional detail instead of the point
of the card. If you catch yourself writing "here's what I need from you" as a paragraph
inside `context`, stop and move it to `needs` instead.

## Usage

1. Copy `build.py` into the current repo's scratch/tools location (not this template — edit
   your copy, not the global one, unless you're improving the template itself).
2. Fill in `OUT` (a real path — the session scratchpad dir is fine), `NOW`, and `PROJECT`
   (`name`, `sub`, `logo` — logo is 1-2 characters).
3. Replace the `EXAMPLE-*` entries in `OPEN` / `PLAN` / `DECIDED` / `RUNS` with real data,
   following the field comments already in the file.
4. `python3 build.py` to render the HTML, then publish it with the `Artifact` tool
   (`favicon` required — pick one emoji and keep it stable across redeploys of the same
   tracker).
5. **Update it after every action or new finding, not in batches at the end.** If it isn't on
   the page, it isn't recorded. Re-run `build.py` and republish to the same artifact URL each
   time (pass `url:` on the `Artifact` call once you have it, so it updates in place instead
   of creating a new artifact).

## Field reference

| Field | Where it renders | Notes |
|---|---|---|
| `ref` | chip, top-left | Stable id (`BUILD-CACHE`, `RUN-14`). **Never renumber** once assigned — readers refer back to these across sessions. |
| `ts` | chip, top-right | `YYYY-MM-DD HH:MM TZ`, real clock time, updated whenever the entry is touched. |
| `title` | h3/h4 | One line. |
| `status` (Open/Plan only) | badge | `"mine"` \| `"needs_input"` (default) \| `"backlog"`. |
| `verdict` (Decided only) | badge | `"accepted"` \| `"rejected"` \| `"caveat"`. |
| `needs` | top of card, visible | Array of short strings, each a standalone action item. Optional `needsLabel` overrides the heading (default "What I need from you"). |
| `solutions` | top of card, visible | Array of `{title, pros[], cons[], recommended?}`. Put "(RECOMMENDED)" in the title of the recommended one and set `recommended: true` — both are needed (the flag drives the highlight, the text survives search/copy). |
| `resolution` (Decided only) | top of card, visible | What was actually decided/found, with the evidence. |
| `context` | collapsed "Background" | Problem statement and history ONLY. Never an action item. |
| Run rows (`RUNS`) | compact row, not a full card | `what`, `config`, `result` (`pass`\|`fail`\|`stopped`\|`pending`), `score`, `timing`, `spend`, `notes`. Sorted newest-first at build time. |

## What's generic vs. what you customize

Everything from the `<style>` block through the closing `</script>` in `build.py` is the
generic rendering engine (search, tabs, theme toggle, card renderers) — you should not need
to touch it for a normal tracker. Only the data section at the top (`OUT`, `NOW`, `PROJECT`,
`OPEN`/`PLAN`/`DECIDED`/`RUNS`) is meant to be edited per use.

If you do need to change the engine (a new field, a layout tweak), consider syncing the fix
back to this template (`~/.claude/templates/tracker-artifact/build.py`) so the next repo
inherits it too, the same way the needs-list-at-top-level fix that created this template got
folded back in after being found in one repo's tracker.

## Theming

Follows the `artifact-design` skill's dark-mode contract in full: the complete light palette
sits on bare `:root`; the same dark values are defined twice — once under
`@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])` (so a
reader with no explicit preference gets dark automatically when their OS is dark), and again
under `:root[data-theme="dark"]` (so the in-page Light/Dark toggle button pair can force
either mode regardless of OS). Every color a card uses — including badge tints
(`--badge-good-bg`/`-fg`, `--badge-bad-bg`/`-fg`, `--badge-warn-bg`/`-fg`) and the search
highlight (`--mark-bg`) — is a token defined in all three places, never a bare hex value
inside a component rule; if you add a new color, add it as a token in all three blocks the
same way, or it will silently ignore both the toggle and the OS preference. A small init
script also syncs the toggle buttons' visual `.on` state to whichever theme actually applied
on load, without stamping `data-theme` itself — so a reader who never clicks the toggle keeps
following live OS theme changes instead of getting frozen onto whatever was true at load.
