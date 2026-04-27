# Action Items — Trello Cards for Improvements

## Purpose

When something goes wrong or you discover something that needs attention, create a Trello card in **Action Items** immediately. Don't defer, don't write notes to files, don't wait for session end. Trello cards are persistent, visible to all agents and humans, and actionable.

## When to Create Cards

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

## Card Requirements

Every card must pass the zero-context test — a fresh agent or human with no conversation history can understand the problem and decide what to do.

Cards go in **Action Items** list. The human decides whether to act on them.

**Card format:**
- Title: Short description of what went wrong or what needs fixing
- Description: What happened, why it wasted time, proposed fix (specific files/changes)
- Label: Feature (for new tools/skills) or Bug (for broken behavior/docs)

Categories:
- **Prompt/rules fix** — a rule was missing, ambiguous, or wrong and caused a mistake
- **New tool/skill** — a manual workflow that should be automated
- **Skill improvement** — an existing skill that missed a case or could be tightened
- **Documentation** — code comments, CLAUDE.md updates that would have saved time
- **Code refactor** — misleading code that sent the agent down the wrong path
- **Better error messages** — a script failed silently or unhelpfully

## /docs and /explain Always Produce a Change

"The rules already cover this" is NEVER acceptable. If an error happened despite existing rules, those rules failed — make them more prominent, more specific, or placed where the agent reads them. `/docs` -> rule/doc update. `/explain` -> concrete prevention proposal (not "I'll be more careful").

## Where to Add Rules

All projects: `~/.claude/rules/` (global). This project only: project `.claude/rules/` or CLAUDE.md. Ask: "Would this help an agent in ANY codebase?" If yes, global.

## Rules, Not Memory

Behavioral corrections go in rules files, NEVER in memory. Memory = contextual, soft, disposable. Rules = universal, durable, authoritative. When the user corrects behavior, that's a rule.

## CRITICAL: Never Write Agent Files to ~/.claude/

`~/.claude/` is the user's configuration directory. NEVER write log files, notes, or agent artifacts there. Improvements are Trello cards, not files on disk.
