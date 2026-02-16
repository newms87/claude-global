# Agent Self-Improvement Log (Global)

## 2026-02-16: Full test suite run efficiency rules

**File:** `~/.claude/rules/testing.md`
**Change:** Added "Full Test Suite — Run Once, Extract Everything" section requiring single-pass runs with file-based output capture.
**Why:** Agent ran the full test suite 3+ times in a single session trying to grep different failure info, wasting ~15 minutes of heavy CPU.

## 2026-02-16: Self-improvement workflow step

**File:** `~/.claude/rules/self-improvement.md` (new), `~/.claude/rules/planning.md`
**Change:** Created self-improvement rules file and added it as step 8 in the phase-by-phase workflow.
**Why:** Establishing the self-improvement workflow as a standard practice.
