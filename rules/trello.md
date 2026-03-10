# Trello Card Workflow

Universal patterns for working with Trello cards. Project-specific board IDs, list IDs, and labels live in each project's `.claude/rules/trello.md`.

## Card Titles

Titles are short, scannable, and type-appropriate:

| Card Type | Format | Example |
|-----------|--------|---------|
| Feature | `[Domain]` + imperative verb phrase | "[Auth] Add SSO login support" |
| Bug | `[Domain] Fix:` prefix | "[Extract Data] Fix: group artifacts polluted" |
| Epic | Same as Feature/Bug | "[Extract Data] Redesign extraction pipeline" |
| Phase | `Epic Title > Phase N: Description` | "[Extract Data] Redesign pipeline > Phase 1: Extract traits" |

Keep titles under ~80 characters. Use domain prefixes in brackets (e.g., `[Extract Data]`, `[Auth]`) to categorize cards by area of the codebase.

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
- **Labels are required.** Every card must have at least one label (Bug or Feature).
- **Comments are markdown.** Use `##` headers, bullet lists, and proper formatting.
- **Acceptance criteria live in checklists, not descriptions.** Use the "Acceptance Criteria" checklist via `create_checklist` + `add_checklist_item`.
