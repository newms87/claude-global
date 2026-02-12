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

If the card is not already in the In Progress list, move it there using `move_card` with the list ID from the project's trello.md rule file.

If already In Progress, skip this step and note it.

## Step 4: Prompt for Planning

Tell the user the card is assigned and suggest entering plan mode to create an implementation plan. The plan file will be linked to this card via the rules in `.claude/rules/trello.md`.
