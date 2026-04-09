---
name: flow-self-improvement
description: Final pipeline step. Process agent-notes.md, create Trello cards for meaningful improvements, clean up.
---

# Self-Improvement

Final step in every pipeline run. Reflect on the session, process any notes, and create Trello cards for improvements that warrant human review. This is NOT about logging — it's about identifying concrete actions that will make the next session better.

---

## Steps

1. **Read `agent-notes.md`** in the project root. If the file doesn't exist or is empty, output "No self-improvement needed" and stop.

2. **Filter for real problems.** For each note, ask:
   - Did this waste meaningful time or effort (>10 min lost)?
   - Was the human frustrated or did they have to correct the same mistake twice?
   - Is there a concrete fix (rule change, new tool, better docs, code refactor)?
   - If YES to at least one: proceed. Otherwise: discard — not everything needs a card.

3. **Apply immediate rule fixes directly.** If the fix is a small rule addition/clarification (1-10 lines) to `~/.claude/rules/` or project rules, just make the edit now. No card needed for obvious rule gaps.

4. **Create Trello cards for bigger improvements.** For anything that needs human approval — new tools, skill changes, code refactors, documentation overhauls — create a card in the **Review** list:
   - Title: `[Self-Improvement] Short description of what went wrong`
   - Description: What happened, why it wasted time, proposed fix with specific files/changes
   - Label: Feature or Bug as appropriate
   - Position: top

   Categories that warrant cards:
   - **New tool/skill** — a manual workflow that should be automated
   - **Skill improvement** — an existing skill missed a case
   - **Code refactor** — misleading code sent the agent down the wrong path
   - **Better error messages** — a script failed silently or unhelpfully
   - **Prompt/documentation gap** — missing context that a fresh agent needs

5. **Delete processed notes** from `agent-notes.md`. Only delete notes you recognize as yours (by task name). Leave other agents' notes untouched.

6. **If rule files were changed**, commit them separately:
   - Message format: `[Self-Improvement] Brief description of rule added`
   - Stage only the changed rule files
   - Do NOT commit agent-notes.md (gitignored) or Trello card creation

## Rules

- **Sparingly.** Most sessions produce zero cards. Only create cards when something actually went wrong.
- **Never create cards for:** one-off typos, minor style preferences, hypothetical optimizations, or things that are already obvious from the code.
- **NEVER write files to `~/.claude/`** except rule files in `~/.claude/rules/`. No logs, no notes, no artifacts.
- **If no notes or no warranted changes:** Output "No self-improvement needed" and stop. Do not force an update.
- **Cards go to Review list** — the human decides what to act on.
