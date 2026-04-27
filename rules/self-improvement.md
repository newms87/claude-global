# Action Items — Trello Cards for Improvements

## Purpose

Something goes wrong or discover something needing attention → create Trello card in **Action Items** immediately. Don't defer, don't write notes to files, don't wait session end. Trello cards persistent, visible to all agents + humans, actionable.

## When to Create Cards

**Only when something actually went wrong.** Wasted meaningful time/effort, or human visibly frustrated with result. Not hypothetical improvements, not minor inconveniences, not "nice to haves."

Signs card warranted:
- Spent >10 min on something should have taken 2 (missing tool, missing context, bad docs)
- Human had to correct you on same class of mistake twice
- Script/tool failed in way better error messages or docs would have caught instantly
- Went down wrong path because code misleading or poorly documented
- Manual multi-step process could be automated with Makefile target or skill

Signs card NOT warranted:
- One-off typo or wrong path (fix + move on)
- Minor style preference
- Hypothetical future optimization nothing triggered
- "We should document X" when X already obvious from code

## Card Requirements

Every card must pass zero-context test — fresh agent or human with no conversation history can understand problem + decide what to do.

Cards go in **Action Items** list. Human decides whether to act on them.

**Card format:**
- Title: Short description of what went wrong or what needs fixing
- Description: What happened, why wasted time, proposed fix (specific files/changes)
- Label: Feature (new tools/skills) or Bug (broken behavior/docs)

Categories:
- **Prompt/rules fix** — rule missing, ambiguous, or wrong → caused mistake
- **New tool/skill** — manual workflow should be automated
- **Skill improvement** — existing skill missed case or could be tightened
- **Documentation** — code comments, CLAUDE.md updates that would have saved time
- **Code refactor** — misleading code sent agent down wrong path
- **Better error messages** — script failed silently or unhelpfully

## /docs and /explain Always Produce a Change

"Rules already cover this" NEVER acceptable. Error happened despite existing rules → rules failed — make more prominent, more specific, or placed where agent reads them. `/docs` -> rule/doc update. `/explain` -> concrete prevention proposal (not "I'll be more careful").

## Where to Add Rules

All projects: `~/.claude/rules/` (global). This project only: project `.claude/rules/` or CLAUDE.md. Ask: "Would this help agent in ANY codebase?" Yes → global.

## Rules, Not Memory

Behavioral corrections go in rules files, NEVER in memory. Memory = contextual, soft, disposable. Rules = universal, durable, authoritative. User corrects behavior → that's a rule.

## CRITICAL: Never Write Agent Files to ~/.claude/

`~/.claude/` = user's configuration directory. NEVER write log files, notes, agent artifacts there. Improvements = Trello cards, not files on disk.