---
name: trello
description: Assign a Trello card to the current session. Usage: /trello <card name or URL>
argument-hint: <card name or URL>
---

# Trello Card Assignment

Assign a Trello card to this working session. Requires Trello MCP and board configuration in project-level `.claude/rules/trello.md`.

## Step 1: Find the Card

The user provides a card name (partial match) or Trello card URL.

**If URL:** Extract the card ID from the URL and fetch with `get_card`.

**If name:** Fetch cards from each list until a match is found. Search In Progress first, then ToDo, then other lists. Match case-insensitively against the card name. If multiple matches, show them and ask the user to pick one.

**Board ID and list IDs** come from the project's `.claude/rules/trello.md` file. If that file doesn't exist, tell the user this project isn't configured for Trello.

## Step 2: Show Card Details

Display a summary of the card:

| Field | Value |
|-------|-------|
| **Name** | Card name |
| **List** | Current list name |
| **Labels** | Label names |
| **URL** | Card short URL |

Show the card description if it has one.

If the card has checklists or acceptance criteria, show those too.

## Step 3: Move to In Progress

If the card is not already in the In Progress list, move it there using `move_card` with the list ID from the project's trello.md rule file (position: `"top"`).

If already In Progress, skip this step and note it.

## Step 4: Pick Up the Card

Follow the "Picking Up a Card" workflow from `~/.claude/rules/trello.md`:

1. Create a **Progress** checklist (Planning, Tests Written, Implementation, Tests Pass, Code Review, Committed)
2. Read full card context (description, ALL comments, acceptance criteria, labels)

## Step 5: Investigate and Plan on the Card

**Do NOT use EnterPlanMode. The Trello card IS the plan.**

1. **Investigate the codebase** — Use agents or direct reads to understand the problem, trace the code, and identify what needs to change. Be thorough — this is the planning phase.

2. **Update the card description** following the appropriate template from `~/.claude/rules/trello.md` (Feature or Bug format). Must pass the zero-context test.

3. **Create an Acceptance Criteria checklist** — each item specific, verifiable, starts with a verb.

4. **Create an Implementation Phases checklist** if the work requires multiple phases (skip for single-phase work).

5. **Present the plan to the user** — Show what you wrote to the card and ask for approval before implementing. Do NOT start coding yet.

**The card is the source of truth.** Re-read it after context compaction, session clearing, or whenever you need to confirm what's left to do. Never rely on conversation memory for the plan — always fetch the card.
