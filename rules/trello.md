# Trello Card Workflow

Universal patterns for working with Trello cards. Project-specific board IDs, list IDs, and labels live in each project's `.claude/rules/trello.md`.

## Card Titles

Titles are short, scannable, and type-appropriate:

| Card Type | Format | Example |
|-----------|--------|---------|
| Feature | `[Project > Domain]` verb phrase | "[Danxbot > Auth] Add SSO login" |
| Bug | `[Project > Domain] Fix:` prefix | "[Million > Trading] Fix: signal error" |
| Epic | Same as Feature/Bug | "[Danxbot > Dashboard] Redesign events" |
| Phase | `Epic Title > Phase N: Desc` | "… Dashboard] … > Phase 1: API" |

**Project prefix:** Use the project name the card targets. For Danxbot itself, use `Danxbot`. For a connected repo, use the repo name (e.g., `Million`).

Keep titles under ~80 characters. Use `[Project > Domain]` prefixes to categorize cards by project and area of the codebase.

## Card Descriptions

The description is the plan document. It must pass the **zero-context test** — a fresh agent with no conversation history should be able to implement from the description alone.

**No code blocks in descriptions.** Same rule as plan files — describe behavior in prose.

### Feature Card Description

```
**Context:** What exists today and why it needs to change. (2-3 sentences)

**Solution:** What to build or change. High-level approach, not implementation details. (1 paragraph)

**Key files:** List of files and methods affected.
```

### Bug Card Description

```
**Problem:** What the user sees or what's broken. (1-2 sentences)

**Root Cause:** Why it happens. Reference specific code paths. (1-2 sentences, or "TBD — needs investigation" if unknown when card is created)

**Solution:** What to change and why. (1-2 sentences)

**Key files:** List of files and methods affected.
```

### Description After Investigation

When picking up a card, update the description with investigation findings. The description should grow more specific — replace "TBD" root causes with actual findings, add discovered key files, refine the solution approach.

### Handoff Assumption

**Assume a different agent will implement every card.** That agent has zero conversation history and only the card to work from. They can explore the codebase themselves, but the card must eliminate ambiguity about *what* needs to change.

Every card description must include:
- **Exact file paths** of every file to create, modify, or fix
- **Known gotchas and edge cases** discovered during investigation
- **How to verify** the implementation works (test commands, expected behavior)

The agent picking up the card can read the codebase to understand how things work — you don't need to document the entire system. But they should never have to guess *what* you intended. If you investigated something and the finding affects the implementation, it belongs in the card.

## Checklists

Every card has up to 3 checklists. Names are exact — do not vary them.

### Acceptance Criteria (required on every card)

Defines "done." Created via `create_checklist` + `add_checklist_item`.

**Each item must be:**
- **Specific** — names the exact behavior, file, or output
- **Verifiable** — can be confirmed by running a test, checking output, or reading code
- **Starts with a verb** — "Returns error when...", "Displays count on...", "Removes legacy fallback from..."

| Good | Bad |
|------|-----|
| "Returns 422 when email is missing" | "Handle validation" |
| "FragmentSelectorService provides all traversal methods" | "Centralize logic" |
| "All existing tests pass" | "Tests work" |

### Implementation Phases (only if multi-phase)

One item per phase: `Phase N: Description`. Only create this checklist when the work requires 2+ distinct implementation phases. Single-phase cards skip this entirely.

Check off each phase as it completes.

### Progress (required on every card)

Tracks pipeline milestones. Always these 6 items in this order:

1. Planning
2. Tests Written
3. Implementation
4. Tests Pass
5. Code Review
6. Committed

Check off each item as the milestone is reached.

### Updating Checklist Items

`update_checklist_item` requires `checkItemId` (the unique ID), NOT checklist name + text. Either save the IDs returned by `add_checklist_item` when creating items, or fetch them first via `get_checklist_items`.

## Reading a Card

**Always read the full card context before starting work:**

1. **Description** — The plan document
2. **ALL comments** — `get_card_comments(cardId)`. Comments contain essential context from users and prior investigation
3. **Acceptance Criteria** — `get_acceptance_criteria(cardId)`. Defines "done"
4. **Other checklists** — Progress tracking, phase lists
5. **Labels** — Bug, Feature, Epic, etc.

Never start work based on the card title alone.

## CRITICAL: Creating a Card ≠ Implementing a Card

**When you create a Trello card, you are DONE. Do not implement it. Do not pick it up. Do not start work on it. STOP.**

The entire purpose of creating a Trello card is to **hand the work off to a different agent in a different session.** You are writing instructions for someone else. That someone else is NOT you. The card exists so the user can:

1. **Review it** — verify the task was understood correctly
2. **Prioritize it** — decide when and whether to do it
3. **Assign it** — choose which session picks it up via `/trello`

**Any work you do on a card you just created is 100% wasted effort.** The user will revert it immediately. You wrote the card description — you already have context bias. A fresh agent reading the card tests whether the description actually works as a standalone plan (the zero-context test). If you implement your own card, that test never happens.

**This is a BLOCKING rule.** After `add_card_to_list` returns, your only allowed actions are:
- Tell the user the card was created (show the URL)
- Continue with whatever you were doing BEFORE the card creation request
- If there's nothing else to do, stop

**NEVER:** move the card to In Progress, create checklists on it, read it back and start planning, or write any code related to it. The card is a message in a bottle — you throw it and walk away.

## Card Lifecycle

### Picking Up a Card

1. Move card to In Progress (`position: "top"`)
2. **Apply labels immediately** — Use `update_card_details` with label IDs from the project's `.claude/rules/trello.md` to set appropriate labels. Every card needs at least one label (Bug, Feature, etc.). If the card already has labels, verify they're appropriate for the work.
3. Create a **Progress** checklist (6 items above)
4. Read full card context (description, comments, acceptance criteria)

### During Work

- **Post review results as comments** (formatted as markdown with `##` headers)
- **Add comments for significant discoveries** or plan changes
- Checklist items and card moves are handled by `/flow-commit` — do not update them manually

### Completing a Card

All completion actions (checking off items, retro comment, move to Done) happen automatically via `/flow-commit` when it detects all work is finished. Do not perform these manually.

## Epic Splitting

When a card requires 3+ phases or spans different domains:

1. Add `Epic` label to the parent card
2. Create an **Implementation Phases** checklist on the parent listing each phase
3. Create individual phase cards in In Progress: `Epic Title > Phase N: Description`
4. Each phase card gets its own description, acceptance criteria, Progress checklist, and label (Bug or Feature)
5. Add a comment to the epic listing all phase cards
6. Move the epic to Done (phases track the real work)
7. Pick up the first phase card

After completing a phase card, look for the next phase card in In Progress.

## Comment Formats

### Retro Comment (on every completed card)

```markdown
## Retro

**What went well:** [1-2 sentences]

**What went wrong:** [1-2 sentences or "Nothing"]

**Action items:** [improvements or "Nothing"]

**Commits:** [commit sha(s)]
```

### Bug Diagnosis Comment (bug cards only)

Post after fixing, before the retro:

```markdown
## Bug Diagnosis

**Problem:** What the user saw
**Root Cause:** Why it happened
**Solution:** What changed and why
```

### Review Results Comment

```markdown
## Code Review

[summary of findings and fixes]
```

## The Card IS the Plan

**Do NOT use EnterPlanMode when a Trello card is assigned.** The card description and checklists ARE the plan. No separate plan file.

### Re-reading the Card

**The card is the source of truth.** Re-read it:
- After context compaction or session clearing
- When unsure what's left to do
- Before marking the card Done (verify all acceptance criteria are checked)

Never rely on conversation memory for the plan. Always fetch the card via `get_card` using the card ID or shortLink (e.g., `0uEn8qf8` from `trello.com/c/0uEn8qf8`). ShortLinks work as card IDs in all MCP calls.

### After Significant Plan Changes

1. Update the card description directly
2. Add a comment explaining what changed and why (only for meaningful changes)

## General Rules

- **One card at a time.** Finish or pause before starting another.
- **Card is source of truth.** No separate plan file when a Trello card is assigned.
- **Don't block on Trello failures.** If a Trello API call fails, log it and continue.
- **Always specify position.** `"top"` when moving cards, `"bottom"` for newly generated cards (e.g., ideation).
- **Always pass boardId to move_card.** The `move_card` MCP call moves cards cross-board if the target listId is on a different board. Always pass the project's `boardId` explicitly to prevent accidental board moves.
- **Labels are required.** Every card must have at least one label (Bug or Feature).
- **Comments are markdown.** Use `##` headers, bullet lists, and proper formatting.
- **Acceptance criteria live in checklists, not descriptions.** Use the "Acceptance Criteria" checklist via `create_checklist` + `add_checklist_item`.
- **Connected repo cards reference connected repo architecture.** When creating a card that targets the connected repo, all file paths, API patterns, framework references, and architecture descriptions MUST come from the connected repo's docs (`repo-overview.md`, `repo-config.md`), NOT from danxbot's rules. Before writing a card description, re-read the repo overview to confirm paths. Danxbot's `dashboard/` and `src/dashboard/` are NOT the connected repo's frontend/backend.
