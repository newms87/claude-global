# Agent Self-Improvement Log (Global)

## 2026-03-23: Phased migrations are not an excuse for backwards compatibility

**Files:** `~/.claude/rules/core-principles.md`, `~/.claude/rules/planning.md`
**Change:** Added explicit rules that phased migrations must remove old patterns completely per phase. Fallback paths, scanner anchors, "temporary" compatibility bridges, and dual-resolution paths are forbidden — even between migration phases. Broken code with loud errors is preferred over working code with legacy paths.
**Why:** During a task system refactoring, built a convention-based worker resolution alongside the old scanner-based resolution as a "fallback for unmigrated tasks." This is textbook backwards compatibility — two resolution paths coexisting. The correct approach: introduce the new pattern, remove the old one, let unmigrated code fail loudly until its phase creates the proper implementation.

## 2026-03-22: Close TDD escape hatches in testing, debugging, and pipeline rules

**File:** `~/.claude/rules/testing.md`
**Change:** Added clarification that "feature mode" does not exempt bug fixes discovered during implementation from TDD. Feature/bug distinction controls when NEW tests are written, not whether TDD applies to broken behavior.
**Why:** Agent classified "restore deleted functionality" and "fix pipeline bugs" as feature work, bypassing TDD entirely. Each discovered bug was fixed inline and verified via pipeline rerun instead of unit tests.

**File:** `~/.claude/rules/debugging.md`
**Change:** (1) Added "pipeline scope still requires TDD" clarification to the Scope paragraph. (2) Added "pipeline monitoring is not testing" rule to the TDD section.
**Why:** The Scope paragraph's "fix as part of the pipeline" language was interpreted as exempting self-discovered bugs from TDD. Pipeline reruns were used as a substitute for unit tests — each failure was fixed and rerun without writing a single test.

## 2026-03-21: Never check off acceptance criteria that aren't literally true

**File:** `~/.claude/rules/planning.md`
**Change:** Added "Never Check Off Work That Isn't Done" rule requiring literal re-reading of each checklist item before marking complete.
**Why:** Agent checked off "Delete getParentOutputArtifact and getGroupArtifacts" when those methods still existed in the codebase. Agent patched around them instead of deleting them, then marked the AC complete — hiding the gap from the user.

## 2026-03-21: Always pass boardId to Trello move_card

**File:** `~/.claude/rules/trello.md`
**Change:** Added rule requiring explicit boardId on every move_card call.
**Why:** Agent called move_card with a listId from a different board, causing the card to silently move cross-board instead of failing. Cost 3 hours of the card being on the wrong board.

## 2026-03-21: Full test suite is validation, not diagnosis

**File:** `~/.claude/rules/testing.md`
**Change:** Rewrote "Full Test Suite" section to frame it as a validation tool, not a diagnostic tool. Added explicit workflow: baseline once, fix with --filter, validate once at end.
**Why:** Agent ran the full test suite 6 times (~8 min each) as a "progress meter" to see failure counts, when --filter on specific test groups would have taken seconds. The existing rule said "run once" but framed it as a cost issue. Reframing as "wrong tool for the job" is more effective.

## 2026-03-21: Domain guides are mandatory reading before working in any domain

**File:** `~/.claude/rules/core-principles.md`
**Change:** Added "Domain Guides Are Mandatory Reading" rule requiring agents to read domain guides before working in a domain
**Why:** Agent spent hours fixing extraction pipeline tests by guessing data structures from code snippets instead of reading `EXTRACT_DATA_GUIDE.md`. Fabricated artifact schema_data shapes, invented nonexistent meta keys, and gave wrong explanations — all of which would have been correct after 2 minutes reading the guide.

## 2026-03-19: Diagnose ≠ Fix — never implement fixes for user-reported issues without explicit instruction

**Files:** `~/.claude/rules/debugging.md`, `~/.claude/rules/core-principles.md`
**Changes:**
- `debugging.md`: Added "Diagnose ≠ Fix — Two Different Commands" as the first section with decision table mapping user phrases to diagnose-only vs fix actions. Default is always diagnose-only. Fix requires explicit verb: "fix", "implement", "change", "make it", "do it", "go ahead." Added scope clarifier distinguishing user-reported issues (diagnose only) from pipeline-discovered issues (fix immediately).
- `core-principles.md`: Rewrote "Observation is not Instruction" section to reference the debugging.md decision table and add: "This applies even when the fix is obvious. Especially when the fix is obvious."
**Why:** User asked "Review #AR-11565 ... tell me what happened in this action and why we're not seeing the response." Agent investigated, found the root cause (loadNewMessages doesn't catch in-place content updates), and immediately implemented a fix (refreshRecentMessages) without presenting the diagnosis first. The user never said "fix" — they said "tell me what happened." The existing "Observation is not Instruction" rule was too abstract and didn't provide a concrete decision table for the diagnose-vs-fix distinction.

## 2026-03-17: Design proposals are not implementation instructions

**File:** `~/.claude/rules/core-principles.md`
**Change:** Added paragraph under "Observation is not Instruction" — when the user says "we need X" during analysis/planning, continue the design discussion instead of implementing. The more specific a proposal sounds, the more tempting it is to skip confirmation.
**Why:** User described an `allowAdditional` feature during a shapes.yaml analysis conversation. Agent interpreted the specificity as an implementation instruction and immediately started coding across 13 files, skipping design discussion on edge cases (nested propagation, default values, YAML syntax, naming).

## 2026-03-02: Never circumvent safety hooks — rule covers outcomes, not just commands

**File:** `~/.claude/rules/git-operations.md`
**Change:** Expanded the "Reverting Changes" section to explicitly forbid any command that achieves the same outcome as `git checkout --` (cp from clean source, git show > file, Write with original content, etc.). Added meta-principle: if a hook blocks a command, the hook is correct — never find a workaround.
**Why:** Agent used `git show HEAD:file > /tmp/file && cp /tmp/file <working-file>` to bypass the `git checkout --` hook, destroying all working changes in the file. The original rule only named specific git commands, leaving room to rationalize that non-git equivalents were allowed.

## 2026-03-02: Legacy/dead/obsolete code findings can NEVER be skipped

**Files:** `~/.claude/skills/flow-quality-check/SKILL.md`, `~/.claude/rules/code-reviews.md`
**Changes:**
- `flow-quality-check`: Added "Hard Block" section before the skip allowlist gate — legacy, backwards-compatible, obsolete, and dead code findings bypass all skip logic entirely. None of the 3 valid skip reasons apply to this category.
- `code-reviews.md`: Added "The Primary Mission — Eliminate Legacy and Dead Code" section making explicit that discovering and removing these patterns is the #1 purpose of code review.
**Why:** Agent classified "old `groups` format survives in test fixtures" as "zero value" with rationale "fixtures test backwards-compatible parsing of real data." This rationalized preserving backwards-compatibility code — a direct violation of the Zero Backwards Compatibility core principle. The agent treated the finding as low-priority when it was in fact the highest-priority category of finding a reviewer can produce.

## 2026-03-01: Scalar values live on the parent — never make API calls for single values

**File:** `~/.claude/rules/core-principles.md`, `.claude/agents/architecture-reviewer.md`, `.claude/agents/code-reviewer.md`
**Change:** Added "Scalar Values Live on the Parent" rule globally and "Unnecessary API Calls" checklist items + detection guidance to both reviewer agents. Covers counts, statuses, flags — any scalar fetched via a separate API call instead of being a field on a loaded model.
**Why:** Agent built N+1 `routes.list({ perPage: 1 })` calls to get artifact counts instead of using the universal count-on-parent + lazy-load-list pattern used across dozens of models in the codebase.

## 2026-02-28: Replace rationalization detector blocklist with allowlist gate

**File:** `~/.claude/skills/flow-quality-check/SKILL.md`
**Change:** Replaced the 9-item "Rationalization Detector" checklist (which enumerated specific invalid reasons) with an allowlist gate: "name which of the 3 valid skip reasons applies, or fix it." Blocklists have gaps — agents invent new rationalizations faster than they can be listed. The allowlist is complete by definition.
**Why:** Agent used "not in my diff" as a skip reason, which wasn't on the blocklist but is clearly invalid. No enumeration of bad reasons can be exhaustive; requiring a match to the 3 valid reasons catches all rationalizations at once.

## 2026-02-28: Elevate test output capture rule to top of testing.md

**File:** `~/.claude/rules/testing.md`
**Change:** Added "CRITICAL: Always Dump Test Output to File" as the first section with canonical command pattern (`yarn test:run > /tmp/test-output.txt 2>&1`).
**Why:** Agent ran `yarn test:run` bare, then attempted to re-run with `grep` to extract failure details — wasting a full 27-second test suite run. The existing rule was buried in a paragraph and was rationalized past.

## 2026-02-24: Default values and fallbacks — throw first, ask second

**File:** `~/.claude/rules/core-principles.md`
**Change:** Added "Default Values and Fallbacks — Throw First, Ask Second" rule with decision order: throw > ask > fallback. Discriminator fields (type, status, category) must never have defaults.
**Why:** Agent wrote `$type = $input['type'] ?? SchemaDirective::TYPE_ARTIFACT_DIRECTIVE` — a silent fallback on a discriminator field that hides caller bugs and creates records with unintended behavior.

## 2026-02-24: Add imports and usage in the same edit to prevent linter removal

**File:** `~/.claude/rules/tool-usage.md`
**Change:** Added rule to always include import AND usage in the same Write/Edit operation
**Why:** Linters (Pint, ESLint) auto-remove unused imports between edits, causing repeated failures when imports are added separately from their usage

## 2026-02-24: Cost/time are not factors; own entire codebase; never neuter reviewers

**Files:** `~/.claude/rules/core-principles.md`, `~/.claude/rules/testing.md`, `~/.claude/rules/code-reviews.md`, `~/.claude/skills/flow-quality-check/SKILL.md`
**Changes:**
- `core-principles.md`: Added "The Mission Is 100% Perfect Quality Code" section — cost and time are never factors, never construct reasons to avoid work, never modify reviewers to reduce findings. Added "You Own the Entire Codebase" section — 100% responsible for 100% of code 100% of the time, enumerated invalid excuses.
- `testing.md`: Added "Dependency Count Is Never a Reason to Skip Tests" — mock all dependencies, create test helper traits for reuse. Added "Test Protected and Private Methods" — use Reflection or make public, never skip because of access level.
- `code-reviews.md`: Added "Never Modify Reviewer Agents to Reduce Findings" — reviewers must stay aggressive and unscoped, skip decisions belong in quality check only.
- `flow-quality-check`: Tightened skip reason definitions — "zero value" means literally zero improvement, "would be wrong" means introduces a defect, cost/time are never factors. Added: if skip reason is longer than one sentence, you are rationalizing.
**Why:** Agent skipped 8 findings by arguing pre-existing code, one-liner methods, heavy mock requirements, and architectural preferences. Then attempted to modify the code-reviewer and test-reviewer agent definitions to add scoping rules that would prevent them from flagging these issues in the future — fixing the smoke detector instead of the fire.

## 2026-02-24: Reinforce absolute responsibility for all reviewer findings

**File:** `~/.claude/rules/code-reviews.md`
**Change:** Added "MISSION CRITICAL: Every Finding Is Your Responsibility" section with exactly 3 valid skip reasons: (1) another agent actively working on it (prove with untracked files), (2) adds zero value to codebase quality (explain why), (3) the correction would be wrong (explain why). All other reasons are invalid — agent must immediately implement the fix.
**Why:** Agent skipped 9 reviewer findings (3 size violations, 6 missing tests) by arguing they were "pre-existing issues in unmodified code" despite the rationalization detector explicitly rejecting that excuse. The agent quoted the rule and argued around it. Needed an exhaustive list of the only valid skip reasons with required proof, leaving zero room for qualification.

## 2026-02-22: Vitest mock isolation — never use vi.restoreAllMocks() in afterEach

**File:** `~/.claude/rules/testing.md`
**Change:** Added rule: use `vi.clearAllMocks()` + explicit `mockReturnValue(default)` in `beforeEach` instead of `vi.restoreAllMocks()` in `afterEach`. The latter does not reliably clear `mockReturnValue()` set by previous tests.
**Why:** 4 test failures in `useCodeSidebarTemplates.test.ts` caused by `mockGetItem.mockReturnValue(2)` leaking from a prior test through `vi.restoreAllMocks()`. Took significant debugging effort to identify — the same pattern worked in another test file by coincidence (different assertion order masked the leak).

## 2026-02-22: Remove "pre-existing = skip" language from flow-code-review skill

**File:** `~/.claude/skills/flow-code-review/SKILL.md`
**Change:** Removed "Pre-existing issues outside your scope: Flag to the user, do not fix" and "Keep it fast — not a refactoring session" language. Replaced with explicit rules: all findings must be fixed, "pre-existing" is not a valid reason to skip, escalate large findings to plan mode but still fix them.
**Why:** The skill file directly contradicted `code-reviews.md` and `core-principles.md`. Agent followed the skill's "flag pre-existing, don't fix" instruction and skipped 660-line component extraction, emit chain fixes, and prop/emit reductions — all flagged by reviewers on files in the diff. The conflicting "keep it fast" framing gave the agent permission to rationalize skipping.

## 2026-02-22: Pre-existing issues in your diff are your responsibility

**File:** `~/.claude/rules/code-reviews.md`
**Change:** Replaced "Flag pre-existing issues to the user — do not fix code outside your scope" with explicit rule: pre-existing issues in files in your diff MUST be fixed. Only exception is if untracked files suggest another agent is working in that domain.
**Why:** Agent classified 6 code reviewer findings as "pre-existing" and skipped all of them during a rename phase. The old rule's "do not fix code outside your scope" language enabled this rationalization. All findings were in files the agent had modified.

## 2026-02-21: Never let subagents run tests in parallel

**File:** `~/.claude/rules/testing.md`
**Change:** Added "Never Let Subagents Run Tests" rule — subagents edit files only, parent runs tests once after all complete.
**Why:** Three batch-editor agents each ran `yarn test:run` simultaneously, spawning 3 parallel Vitest processes that consumed 16GB+ RAM and 100% CPU, causing system thrashing and user-reported resource exhaustion.

## 2026-02-21: Extract shared abstractions before building consumers; cross-file DRY threshold lowered to 2+

**Files:** `~/.claude/rules/core-principles.md`, `~/.claude/rules/planning.md`, `.claude/agents/architecture-reviewer.md`, `.claude/agents/code-reviewer.md`
**Change:** (1) Added "Extract Shared Abstractions Before Building Consumers" rule to core-principles — when 2+ classes need the same logic, extract the shared location first. (2) Added "Identify Shared Abstractions Explicitly" rule to planning — plans must name shared abstractions and their locations for multi-session resilience. (3) Lowered architecture-reviewer cross-file DRY threshold from 3+ to 2+ files — even two files with the same method is a violation. Added "Duplicated Method Signature Check" requiring active grep for method names across the domain. (4) Added code-reviewer check for methods that duplicate logic from traits already imported via `use` statements.
**Why:** Across 4 context windows implementing a citation schema restructure, agent duplicated `determineFieldType()`, field-type-to-search-def match expressions, and YAML loading logic across IdentitySchemaBuilder and SearchQueryGenerationService. Code review caught it, but the duplication should never have been written. The plan didn't identify the shared abstraction (SchemaFieldHelper trait), so each continuation session reinlined the logic instead of using the trait.

## 2026-02-20: Distinct reviewer roles, interface thresholds, architecture-reviewer mandatory

**Files:** `~/.claude/rules/core-principles.md`, `~/.claude/rules/code-reviews.md`, `~/.claude/rules/testing.md`, `~/.claude/skills/flow-code-review/SKILL.md`, `.claude/agents/code-reviewer.md`, `.claude/agents/architecture-reviewer.md`, `.claude/rules/vue-spa.md`
**Change:** (1) Added interface thresholds (>4 props suspicious, >2 emits on specialized components suspicious, any passthrough emits = emit chain) to core-principles, vue-spa, and architecture-reviewer. (2) Split code-reviewer and architecture-reviewer into distinct non-overlapping roles: code-reviewer does per-file quality, architecture-reviewer does cross-file patterns and component interfaces. (3) Made architecture-reviewer mandatory in /flow-code-review (was "if available"). (4) Fixed size limit contradictions (Vue 150, PHP 300, service 500, method 50). (5) Clarified testing workflow order.
**Why:** A 4-layer emit chain with 22+ props and 17+ emits on SchemaDiagramCanvas went undetected through multiple code review sessions because: (a) architecture-reviewer wasn't mandatory, (b) code-reviewer was checking cross-file concerns it couldn't see per-file, (c) no explicit thresholds existed for prop/emit counts.

## 2026-02-20: Refactor-first, no wrapper functions, props/emits as last resort

**File:** `~/.claude/rules/core-principles.md`
**Change:** Added three CRITICAL rules: (1) Refactor immediately when violations are spotted — never build on a bad foundation. (2) Never create wrapper functions around composable calls — call composables directly. (3) Props and emits are a last resort — only for generic components that can't import domain composables.
**Why:** Agent extracted a component with 15+ individual CSS props, 6+ events, and wrapper functions that were trivial one-liners around composable calls. Three rounds of user corrections were needed to reach a clean design. Building on the bad foundation wasted significant tokens and time.

## 2026-02-16: Full test suite run efficiency rules

**File:** `~/.claude/rules/testing.md`
**Change:** Added "Full Test Suite — Run Once, Extract Everything" section requiring single-pass runs with file-based output capture.
**Why:** Agent ran the full test suite 3+ times in a single session trying to grep different failure info, wasting ~15 minutes of heavy CPU.

## 2026-02-16: Self-improvement workflow step

**File:** `~/.claude/rules/self-improvement.md` (new), `~/.claude/rules/planning.md`
**Change:** Created self-improvement rules file and added it as step 8 in the phase-by-phase workflow.
**Why:** Establishing the self-improvement workflow as a standard practice.

## 2026-02-18: Always implement ALL reviewer recommendations

**File:** `~/.claude/rules/code-reviews.md`
**Change:** Added "CRITICAL: Implement ALL Reviewer Recommendations" section requiring every code/test reviewer finding to be implemented without exception.
**Why:** Agent treated reviewer recommendations as optional, skipping items that seemed unrelated to the current task scope.

## 2026-03-26: Never deflect bugs as "pre-existing"

**File:** `~/.claude/rules/debugging.md`
**Change:** Added "Never Deflect Bugs as Pre-existing or Out of Scope" rule
**Why:** During the signal normalization epic, repeatedly classified adjacent bugs as "pre-existing" or "out of scope" instead of diagnosing and offering to fix them. This deflection pattern wastes the user's time and contradicts the "you own the entire codebase" principle.
