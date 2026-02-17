---
name: flow-self-improvement
description: Process agent-notes.md and update docs if warranted. Auto-commits doc changes separately.
---

# Self-Improvement

Process notes from the current session and decide if any warrant permanent documentation updates. Notes come from two sources: real-time inefficiency notes written during implementation, and code review findings written by `/flow-code-review`.

---

## Steps

1. **Read `agent-notes.md`** in the project root. If the file doesn't exist or is empty, output "No self-improvement needed" and stop.

2. **Process notes matching your current task.** For each note:
   - Does it describe a problem that wasted meaningful effort?
   - Would a short, clear rule (1-10 lines) have prevented it?
   - Is it generalizable, not a one-off edge case?
   - If ALL three are true: proceed to update docs. Otherwise: discard.

3. **Make the doc update.** Add the rule to the most relevant existing file:
   - Global rules (`~/.claude/rules/`): If the rule applies to ANY codebase
   - Project rules (`.claude/rules/` or project docs): If project/framework-specific
   - **Never remove existing rules.** Only add or clarify.
   - **Never restructure docs.** Add to the most relevant existing file.
   - **Keep additions small** — 1-10 lines max.

4. **Log the change.** Record every update in the improvement log:
   - Global changes: `~/.claude/agent-self-improvement.md`
   - Project changes: `<project-root>/.claude/agent-self-improvement.md`
   - Format: date, file changed, what was added, why

5. **Delete processed notes** from `agent-notes.md`. Only delete notes you recognize as yours (by task name). Leave other agents' notes untouched.

6. **Auto-commit doc changes** as a separate commit (not bundled with feature work):
   - Message format: `[Self-Improvement] Brief description of rule added`
   - Stage only the doc files and improvement log
   - Use the standard commit rules (HEREDOC, specific files, no push)

## Rules

- **Sparingly.** Most sessions produce no self-improvement. Only obvious wins.
- **Never self-improve for:** one-off edge cases, things already documented, hypothetical improvements, verbose explanations.
- **If no notes or no warranted changes:** Output "No self-improvement needed" and stop. Do not force an update.
- **Doc changes get their own commit.** Never mix self-improvement commits with feature commits.
