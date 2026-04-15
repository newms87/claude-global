# Trello Card Workflow

Project-specific board IDs, list IDs, and labels live in each project's `.claude/rules/trello-config.md`.

## Card Titles

`[Project > Domain] verb phrase` for features, `Fix:` prefix for bugs. Phase cards: `Epic Title > Phase N: Description`. Keep under ~80 chars.

## Card Descriptions

Must pass the **zero-context test** — a fresh agent with no conversation history can implement from the description alone. No code blocks — prose only.

**Feature:** Context (what exists, why change) -> Solution (high-level approach) -> Key files.

**Bug:** Problem (what's broken) -> Root Cause (why, or "TBD") -> Solution (what to change) -> Key files.

Every description must include: exact file paths, known gotchas, how to verify. Update with investigation findings when picking up a card.

## Checklists

Three checklists max. Names are exact:

**Acceptance Criteria** (required): Specific, verifiable items starting with a verb. "Returns 422 when email missing" not "Handle validation."

**Implementation Phases** (only if multi-phase): One item per phase.

**Progress** (required): Planning, Tests Written, Implementation, Tests Pass, Code Review, Committed.

`update_checklist_item` requires `checkItemId` (unique ID), not name. Save IDs from `add_checklist_item` or fetch via `get_checklist_items`.

## Reading a Card

Always read full context before starting: description, ALL comments (`get_card_comments`), acceptance criteria (`get_acceptance_criteria`), other checklists, labels. Never work from title alone.

## Creating a Card != Implementing It

**When you create a card, you are DONE.** Do not implement, pick up, or start work on it. The card hands work to a different agent in a different session. After `add_card_to_list`, your only actions: tell the user the card was created (show URL), continue previous work, or stop.

## CRITICAL: Never Check Off an Unverified AC Item

Before marking any Acceptance Criteria item complete, you must have direct evidence: a passing test, a command output, or a verified runtime result. "By construction" and "obviously correct" are not evidence. If you cannot verify an AC item in the current environment, leave it unchecked and say so — never check it off with an excuse for why verification was skipped.

## Card Lifecycle

**Pick up:** Move to In Progress (top) -> apply labels -> create Progress checklist -> read full context -> plan work (complex: use writing-plans skill; simple: start immediately).

**During:** Post review results as comments. Add comments for significant discoveries. Checklist items and card moves handled by `/flow-commit`.

**Complete:** All completion actions (check off items, retro comment, move to Done) happen via `/flow-commit`. Do not perform manually.

## Phases vs Epics

**Phases on one card:** Most multi-step work stays on a single card with an Implementation Phases checklist. Phases split up work into sequential steps — each phase is a commit boundary, not a separate card. No Epic label needed.

**Epic = work split across multiple cards.** Only use the Epic label when individual phases are large enough to warrant their own card (own description, own AC, own progress tracking). The epic card is the overview — it stays In Progress while phase cards are worked individually.

**When to split into an epic:** Each phase looks like a substantial unit of work (multiple files, own tests, could take a full session). If phases are smaller related tasks, keep them as checklist items on one card.

**Epic mechanics:** Add Epic label to parent, create phase cards in In Progress (`Epic Title > Phase N: Description`), each with own description/AC/Progress/label.

**After completing each phase card:** Move the phase card to Done (position: "top") immediately after the phase commit. Do not wait until the epic is complete — each phase card has its own lifecycle. Then check off that phase on the epic's Implementation Phases checklist, and look for the next phase card in In Progress (not ToDo — phase cards are created in In Progress). When ALL phase cards are Done, move the epic to Done with a retro comment summarizing all phases.

## Comment Formats

**Retro** (every card): What went well, What went wrong, Action items, Commits.

**Bug Diagnosis** (bug cards): Problem, Root Cause, Solution.

**Review:** Summary of findings and fixes.

## The Card IS the Plan

When a Trello card is assigned: never use EnterPlanMode, never invoke writing-plans or executing-plans skills. Card description + checklists ARE the plan. Re-read the card after context compaction, when unsure what's left, and before marking Done. Always fetch via `get_card` using card ID or shortLink.

## CRITICAL: Always Move to Top Position

Every `move_card` call MUST include `position: "top"`. No exceptions. New cards via `add_card_to_list` MUST include `position: "top"`. Cards created now are likely to be worked on soon — sort later, not at creation time.

## Board Setup — List Creation Order

When setting up a new Trello board, create lists in this exact order (each with `pos=top`, so create in reverse display order):

1. Cancelled
2. Done
3. Needs Help
4. In Progress
5. ToDo
6. Action Items
7. Review

This produces the correct left-to-right display: Review | Action Items | ToDo | In Progress | Needs Help | Done | Cancelled.

Required labels (assign to existing unnamed color labels or create new): Bug (red), Feature (green), Epic (purple), Needs Help (orange).

## General Rules

- One card at a time
- Don't block on Trello API failures — log and continue
- Always pass `boardId` to `move_card` (prevents cross-board moves)
- Labels required on every card (Bug or Feature minimum)
- Comments are markdown with `##` headers
- Acceptance criteria in checklists, not descriptions
- Connected repo cards reference connected repo architecture (not danxbot's paths)
