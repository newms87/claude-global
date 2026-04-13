---
name: flow-finish
description: Use when ending a session or completing all work — processes self-improvement notes, surfaces unwritten session knowledge, and ensures nothing is lost when context is destroyed.
---

# Finish Session

Final skill invoked when a session is ending. Two jobs: process self-improvement notes, and dump any session knowledge that hasn't been captured anywhere. Context is about to be destroyed — anything not written down is lost forever.

---

## Part 1: Self-Improvement

1. **Read `agent-notes.md`** in the project root. If empty or missing, skip to Part 2.

2. **Filter for real problems.** For each note:
   - Did this waste meaningful time or effort (>10 min lost)?
   - Was the human frustrated or had to correct the same mistake twice?
   - Is there a concrete fix (rule change, new tool, better docs)?
   - If YES to at least one: proceed. Otherwise: discard.

3. **Apply immediate rule fixes directly.** Small rule additions (1-10 lines) to `~/.claude/rules/` or project rules — just make the edit. No card needed.

4. **Create Trello cards for bigger improvements** in the best-fit list (priority: **Action Items** if it exists, then **Review**, then whichever list makes the most sense for the board):
   - Title: `[Self-Improvement] Short description of what went wrong`
   - Description: What happened, why it wasted time, proposed fix with specific files/changes
   - Label: Feature or Bug
   - Position: top

5. **Delete processed notes** from `agent-notes.md`. Leave other agents' notes.

6. **Commit rule changes separately** if any were made:
   - Message: `[Self-Improvement] Brief description`
   - Stage only rule files

---

## Part 2: Session Knowledge Dump

**This is the critical addition.** Before the session ends, review everything you know and surface anything that hasn't been captured.

### What to check

Walk through each category and ask: "Is there anything I learned or observed that isn't written down anywhere?"

1. **Trello cards** — Are all cards up to date? Any status changes, blockers, or discoveries that should be commented on a card?

2. **Code comments / docblocks** — Did I encounter confusing code during investigation that I now understand but didn't document? Any "gotchas" I discovered that the next agent will hit?

3. **Rules / CLAUDE.md** — Did I learn a project convention or pattern that isn't in the rules? Did a rule confuse me or need clarification?

4. **Outstanding work** — Is there anything I said I'd do but didn't? Any loose ends from the conversation? Anything the user mentioned wanting that we didn't get to?

5. **Observations for the user** — Anything I noticed during investigation that the user should know about but wasn't part of the task? Stale data, broken tests, degraded infrastructure, security concerns?

### What to output

Present findings as a concise list grouped by category. Only include categories that have something to say. Skip empty categories.

```
## Session Notes

### Outstanding
- [things not yet done, blockers, next steps]

### Observations
- [things noticed but not addressed — stale data, broken tests, etc.]

### Undocumented Knowledge
- [things learned that aren't captured in rules/docs/comments/cards]
```

If the session was clean and everything is captured: output "Session complete. Nothing outstanding."

### What NOT to do

- Don't repeat what's already on Trello cards, in commit messages, or in flow-report output
- Don't fabricate observations to look thorough — silence is fine
- Don't create cards for observations (those are for the user to decide)
- Don't write files for this — just output to the conversation

---

## Part 3: Recommended Next Actions

**End every session with a numbered action list.** The user should be able to glance at this and know exactly what to do next, in priority order. This is the last thing the user sees before closing the session.

### How to build the list

Walk through these sources in order. Each produces zero or more actions:

1. **Incomplete phases on the active Trello card** — if a card is assigned and has unchecked Implementation Phases, the next unchecked phase is the top action
2. **Cards created during this session** — epic phase cards, self-improvement cards, bug cards — link them
3. **Blockers requiring user action** — things only the human can do (restart a service, approve a publish, test in browser, make a business decision)
4. **Documentation/rule updates** — if observations revealed undocumented patterns or stale rules
5. **New cards to create** — problems observed that warrant a card but weren't created (because the agent doesn't create cards for observations — the user decides)

### Output format

```
## Recommended Next Actions

1. **[Action verb] [specific thing]** — [why, with link/path if relevant]
2. **[Action verb] [specific thing]** — [context]
3. ...
```

### Rules for the list

- **Actionable and specific.** "Fix the bug" is useless. "Run `artisan test:template-builder --scenario=2 --dispatch` and verify 10/10" is actionable.
- **Ordered by priority.** Most impactful or blocking action first.
- **Include commands/URLs/card links** where relevant so the user can act immediately.
- **Max 7 items.** If more than 7, group related items or defer low-priority ones.
- **Skip if truly nothing.** If the session completed all work with no loose ends, say "No actions needed — all work complete."

---

## Rules

- **Sparingly on self-improvement.** Most sessions produce zero cards.
- **Thorough on knowledge dump.** Actually think about what you know. The session is about to be destroyed.
- **NEVER write files to `~/.claude/`** except rule files in `~/.claude/rules/`.
- **Cards go to Review list** — the human decides what to act on.
- **Knowledge dump is conversation output only** — no files, no commits, just tell the user.
