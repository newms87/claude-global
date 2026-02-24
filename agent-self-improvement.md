# Agent Self-Improvement Log (Global)

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
