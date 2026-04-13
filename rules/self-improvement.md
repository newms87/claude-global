# Agent Self-Improvement

## Purpose

The final pipeline step. After every commit, reflect on the session and identify meaningful improvements. The goal: make the next agent session faster, smoother, and less frustrating for the human.

## CRITICAL: Trello Cards Immediately — Never agent-notes.md

When you make a wasteful mistake or discover something that needs attention, create a Trello card in **Action Items** immediately. Do NOT write to `agent-notes.md` — that file is ephemeral and gets lost when sessions end abruptly or context compacts. Trello cards are persistent, visible to all agents and humans, and actionable.

**When to create:** As soon as you identify a mistake, a missing tool, a documentation gap, or an observation the user should know about. Don't defer to session end.

**Card requirements:** Every card must pass the zero-context test — a fresh agent or human with no conversation history can understand the problem and decide what to do. Include: what happened, why it matters, proposed fix with specific files/changes.

## When to Create Self-Improvement Cards

**Only when something actually went wrong.** Something wasted meaningful time or effort, or the human was visibly frustrated with the result. Not hypothetical improvements, not minor inconveniences, not "nice to haves."

Signs that a card is warranted:
- You spent >10 minutes on something that should have taken 2 (missing tool, missing context, bad docs)
- The human had to correct you on the same class of mistake twice
- A script/tool failed in a way that better error messages or docs would have caught instantly
- You went down a wrong path because the code was misleading or poorly documented
- A manual multi-step process could be automated with a Makefile target or skill

Signs that a card is NOT warranted:
- One-off typo or wrong path (just fix it and move on)
- Minor style preference
- Hypothetical future optimization that nothing triggered
- "We should document X" when X is already obvious from the code

## What Goes on the Card

Cards go in the best-fit list (priority: **Action Items** if available, then **Review**, then whichever list makes sense). The human decides whether to act on them.

Categories of improvements:
- **Prompt/rules fix** — a rule was missing, ambiguous, or wrong and caused a mistake
- **New tool/skill** — a manual workflow that should be automated (new Makefile target, new skill, new script)
- **Skill improvement** — an existing skill that missed a case or could be tightened
- **Documentation** — code comments, CLAUDE.md updates, CONFIG.md updates that would have saved time
- **Code refactor** — misleading variable names, confusing control flow, or unnecessary complexity that sent the agent down the wrong path
- **Better error messages** — a script failed silently or with an unhelpful error, wasting investigation time

**Card format:**
- Title: `[Self-Improvement] Short description of what went wrong`
- Description: What happened, why it wasted time, proposed fix (specific files/changes)
- Label: Feature (for new tools/skills) or Bug (for broken behavior/docs)

## /docs and /explain Always Produce a Change

"The rules already cover this" is NEVER acceptable. If an error happened despite existing rules, those rules failed — make them more prominent, more specific, or placed where the agent reads them. `/docs` -> rule/doc update. `/explain` -> concrete prevention proposal (not "I'll be more careful").

## Where to Add Rules

All projects: `~/.claude/rules/` (global). This project only: project `.claude/rules/` or CLAUDE.md. Ask: "Would this help an agent in ANY codebase?" If yes, global.

## Rules, Not Memory

Behavioral corrections go in rules files, NEVER in memory. Memory = contextual, soft, disposable. Rules = universal, durable, authoritative. When the user corrects behavior, that's a rule.

## CRITICAL: Never Write Agent Files to ~/.claude/

`~/.claude/` is the user's configuration directory. NEVER write log files, notes, or agent artifacts there. Self-improvement actions are Trello cards in Action Items, not files on disk. Do NOT write `agent-notes.md` — use Trello cards instead.
