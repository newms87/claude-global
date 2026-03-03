# Trello Card Workflow

Universal patterns for working with Trello cards. Project-specific board IDs, list IDs, and labels live in each project's `.claude/rules/trello.md`.

## Reading a Card

**Always read the full card context before starting work:**

1. **Description** — The problem statement or feature request
2. **ALL comments** — Essential context from users and prior investigation
3. **Acceptance Criteria checklist** — Defines "done" (fetch via `get_acceptance_criteria`)
4. **Other checklists** — Progress tracking, phase lists, etc.
5. **Labels** — Bug, Feature, Epic, etc.

Never start work based on the card title alone. Comments often contain critical context not in the description.

## Card Lifecycle

### Picking Up a Card

1. Move card to In Progress (`position: "top"`)
2. Ensure card has a label (Bug or Feature at minimum)
3. Create a **Progress** checklist with tracking items (e.g., Planning, Implementation, Tests, Code Review, Committed)
4. Read full card context (see above)

### During Work

- **Check off Progress items** as milestones are reached
- **Check off Acceptance Criteria** as each criterion is verified (use `update_checklist_item` with `state: "complete"`)
- **Post review results as comments** (formatted as markdown with `##` headers)
- **Add comments for significant discoveries** or plan changes

### Completing a Card

1. Verify ALL acceptance criteria are checked off
2. Add a **retro comment** (see format below)
3. Move card to Done (`position: "top"`)
4. Auto-complete any remaining Progress checklist items

## Epic Splitting

When a card requires 3+ phases or spans different domains:

1. Add `Epic` label to the parent card
2. Create a **Phases** checklist on the parent listing each phase
3. Create individual phase cards in In Progress: `Epic Name > Phase N: Description`
4. Each phase card gets its own description, acceptance criteria, and label
5. Add a comment to the epic listing all phase cards
6. Move the epic to Done (phases track the real work)
7. Pick up the first phase card

After completing a phase card, look for the next phase card in In Progress.

## Comment Formats

### Retro Comment (on completion)

```markdown
## Retro

**What went well:** [1-2 sentences]

**What went wrong:** [1-2 sentences or "Nothing"]

**Action items:** [improvements or "Nothing"]

**Commits:** [commit sha(s)]
```

### Bug Diagnosis Comment (bug cards only)

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

## Plan File Integration

When a Trello card is assigned via `/trello`, add a reference at the top of the plan file:

```
**Trello Card:** [Card Name](card-url) | Card ID: `card-id`
```

This links the plan to the card across sessions. When resuming work, use the card ID from the plan to fetch current card state. If the card ID returns 404, use `get_card` with the shortLink from the URL (e.g., `0uEn8qf8` from `trello.com/c/0uEn8qf8`) — shortLinks work as card IDs in all MCP calls.

## Sync Points

### After Plan Approval

1. Update card description with a brief summary (3-5 lines max)
2. Create **Implementation Phases** checklist with one item per phase
3. Add comment with the plan file path

### After Phase Completion

1. Check off the corresponding checklist item
2. Keep working — no pause needed

### After Significant Plan Changes

1. Add a comment explaining what changed and why
2. Only for meaningful changes, not every minor edit

## General Rules

- **One card at a time.** Finish or pause before starting another.
- **Plan is source of truth.** If plan and card conflict, plan wins.
- **Don't block on Trello failures.** If a Trello API call fails, log it and continue. Sync can be retried later.
- **Keep card descriptions brief.** Details live in the plan file.
- **Always specify position.** Use `"top"` when moving cards so recent work appears first. Use `"bottom"` for newly generated cards (e.g., ideation).
- **Labels are required.** Every card must have at least one label (Bug or Feature). Apply when picking up or creating cards.
- **Comments are markdown.** Use `##` headers, bullet lists, and proper formatting.
- **Acceptance criteria live in checklists, not descriptions.** Use the "Acceptance Criteria" checklist via `create_checklist` + `add_checklist_item`.
