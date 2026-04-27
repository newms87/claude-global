# Trello Card Workflow

Project-specific board IDs, list IDs, labels live in each project's `.claude/rules/trello-config.md`.

## Card Titles

`[Project > Domain] verb phrase` for features, `Fix:` prefix for bugs. Phase cards: `Epic Title > Phase N: Description`. Keep under ~80 chars.

## Card Descriptions

Must pass **zero-context test** — fresh agent with no conversation history can implement from description alone. No code blocks — prose only.

**Feature:** Context (what exists, why change) -> Solution (high-level approach) -> Key files.

**Bug:** Problem (what's broken) -> Root Cause (why, or "TBD") -> Solution (what to change) -> Key files.

Every description must include: exact file paths, known gotchas, how to verify. Update with investigation findings when picking up card.

## Checklists

Three checklists max. Names exact:

**Acceptance Criteria** (required): Specific, verifiable items starting with verb. "Returns 422 when email missing" not "Handle validation."

**Implementation Phases** (only if multi-phase): One item per phase.

**Progress** (required): Planning, Tests Written, Implementation, Tests Pass, Code Review, Committed.

`update_checklist_item` requires `checkItemId` (unique ID), not name. Save IDs from `add_checklist_item` or fetch via `get_checklist_items`.

## Reading a Card

Always read full context before starting: description, ALL comments (`get_card_comments`), acceptance criteria (`get_acceptance_criteria`), other checklists, labels. Never work from title alone.

## Creating a Card != Implementing It

**Create card → DONE.** Don't implement, pick up, start work. Card hands work to different agent in different session. After `add_card_to_list`, only actions: tell user card created (show URL), continue previous work, or stop.

## CRITICAL: Never Check Off an Unverified AC Item

Before marking any Acceptance Criteria item complete, must have direct evidence: passing test, command output, verified runtime result. "By construction" + "obviously correct" not evidence. Cannot verify AC item in current environment → leave unchecked + say so — never check off with excuse for why verification skipped.

## Card Lifecycle

**Pick up:** Move to In Progress (top) -> apply labels -> create Progress checklist -> read full context -> plan work (complex: use writing-plans skill; simple: start immediately).

**During:** Post review results as comments. Add comments for significant discoveries. Checklist items + card moves handled by `/flow-commit`.

**Complete:** All completion actions (check off items, retro comment, move to Done) happen via `/flow-commit`. Don't perform manually.

## Phases vs Epics

**Phases on one card:** Most multi-step work stays on single card with Implementation Phases checklist. Phases split work into sequential steps — each phase = commit boundary, not separate card. No Epic label needed.

**Epic = work split across multiple cards.** Only use Epic label when individual phases large enough to warrant own card (own description, own AC, own progress tracking). Epic card = overview — stays In Progress while phase cards worked individually.

**When to split into epic:** Each phase looks like substantial unit of work (multiple files, own tests, could take full session). Phases smaller related tasks → keep as checklist items on one card.

**Epic mechanics:** Add Epic label to parent, then IMMEDIATELY create all phase cards (`Epic Title > Phase N: Description`), each with own description/AC/Progress/label. Planning agent has full context — capture into phase cards NOW, not later. Deferring phase-card creation to "when work starts" wrong: next agent has less context than planner, recreating design from scratch wastes planner's understanding.

**Where phase cards go:** Same list as parent epic at time of creation. Epic in Review awaiting human approval → phase cards also Review. Epic already In Progress when split → phase cards In Progress. Phase cards move with epic through lifecycle — human approves epic (moves to ToDo or In Progress) → approves whole epic including phases.

**After completing each phase card:** Move phase card to Done (position: "top") immediately after phase commit. Don't wait until epic complete — each phase card has own lifecycle. Then update epic — see `/flow-commit` for full phase completion checklist (AC items, handoff comment, epic review). Then look for next phase card (check In Progress first, then ToDo). ALL phase cards Done → move epic to Done with retro comment summarizing all phases.

**CRITICAL: Update next phase card before ending session.** Next phase picked up by fresh agent with zero context from this session. After completing phase, post "Notes from Phase N" comment on next phase card with anything that could cause next agent to waste time or make mistakes: discovered constraints, timing gotchas, reusable helpers + paths, cost/budget observations, dependencies between phases, corrections to card description. Assume next agent reads ONLY card description + comments — not epic handoff, not conversation history, not git log.

## Comment Formats

**Retro** (every card): What went well, What went wrong, Action items, Commits.

**Bug Diagnosis** (bug cards): Problem, Root Cause, Solution.

**Review:** Summary of findings + fixes.

## The Card IS the Plan

Trello card assigned: never use EnterPlanMode, never invoke writing-plans or executing-plans skills. Card description + checklists ARE plan. Re-read card after context compaction, when unsure what's left, before marking Done. Always fetch via `get_card` using card ID or shortLink.

## CRITICAL: Always Move to Top Position

Every `move_card` call MUST include `position: "top"`. No exceptions. New cards via `add_card_to_list` MUST include `position: "top"`. Cards created now likely worked on soon — sort later, not at creation time.

## Board Setup — List Creation Order

Setting up new Trello board → create lists in exact order (each with `pos=top`, so create in reverse display order):

1. Cancelled
2. Done
3. Needs Help
4. In Progress
5. ToDo
6. Action Items
7. Review

Produces correct left-to-right display: Review | Action Items | ToDo | In Progress | Needs Help | Done | Cancelled.

Required labels (assign to existing unnamed color labels or create new): Bug (red), Feature (green), Epic (purple), Needs Help (orange), Triaged (sky).

## General Rules

- One card at a time
- Don't block on Trello API failures — log + continue
- Always pass `boardId` to `move_card` (prevents cross-board moves)
- Labels required on every card (Bug or Feature minimum)
- Comments = markdown with `##` headers
- Acceptance criteria in checklists, not descriptions
- Connected repo cards reference connected repo architecture (not danxbot's paths)