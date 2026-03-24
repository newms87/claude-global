# Core Engineering Principles

`SOLID / DRY / Zero-Debt / One-Way / Read-First / 100%-Tests / Flawless`

## CRITICAL: The Mission Is 100% Perfect Quality Code

**Cost and time are NOT factors.** The mission is 100% perfect quality code — every file, every method, every test, every docblock. There is no budget. There is no deadline. There is no "good enough." There is only correct and incorrect.

This means:
- **Never skip work because it's hard.** Hard work is still required work.
- **Never skip work because it's time-consuming.** Time is not a constraint.
- **Never skip work because "it was already broken."** You own the entire codebase. Fix it.
- **Never construct reasons to avoid work.** If you catch yourself building an argument for why something doesn't need to be done, that is proof it needs to be done. The effort you spend rationalizing is effort you should spend implementing.
- **Never modify reviewer agents, quality gates, or process rules to reduce findings.** Reducing the signal is the opposite of fixing the problem. If reviewers flag too many things, the answer is to fix all of them — not to make the reviewers stop looking.

## The Principles

| Principle | Description |
|-----------|-------------|
| **Zero Tech Debt** | No legacy code, no backwards compatibility, no dead code. NEVER add compatibility layers. |
| **SOLID** | Single responsibility, small files, small methods. |
| **DRY** | Refactor duplication immediately. Never copy-paste code. |
| **One Way** | ONE correct pattern for everything. Fix at source, not caller. |
| **Read First** | Always read existing implementations before writing new code. |
| **100% Tests** | All features and bug fixes require comprehensive tests. |
| **Flawless** | Every component perfectly documented, typed, and styled. Library-grade quality. |

## Zero Backwards Compatibility

**NEVER introduce backwards compatibility code. This is a CRITICAL violation.**

### Why: Legacy Code Is Net Negative

Legacy code, backwards compatibility, fallbacks, deprecated paths, and duplicated patterns are not "low value" — they are **actively harmful**. They make the system worse than if nothing had been written. Every compatibility layer is a bug waiting to happen, a misleading path for the next developer, and wasted effort maintaining something that should not exist. A broken system that fails loudly is **better** than a "working" system with two paths doing the same thing.

**Broken is preferred over backwards-compatible.** When migrating in phases, each phase removes the old pattern completely. If unmigrated code breaks, that is correct — it fails loudly, telling the next phase exactly what to fix. Never build a bridge between old and new patterns "until migration is complete." The bridge IS the corruption. A clear RuntimeException saying "this operation has no Workers/ class yet" is infinitely better than a fallback path that silently runs the old code.

### Forbidden Patterns

- Supporting multiple parameter names (`$param = $params['old_name'] ?? $params['new_name'] ?? null;`)
- Comments containing "backwards compatibility", "legacy support", "deprecated"
- Code that handles "old format" or "new format" simultaneously
- Fallback logic for old parameter names, data structures, or APIs
- Two resolution paths for the same concept (e.g., "try new, fall back to old")
- "Temporary" compatibility code that "will be removed in a later phase"
- Scanner anchors, stub classes, or shims that exist solely to keep old paths working

### The Rule

ONE correct way to do everything. If something uses the wrong name, fix it at the source. Never add compatibility layers. If a phased migration leaves some code broken, that is the correct state — the break is the signal, not a problem to be papered over.

## CRITICAL: Refactor First — Never Build on a Bad Foundation

**If you see a DRY or SOLID violation, refactor it IMMEDIATELY. Do not build on top of it.**

Building on code that needs refactoring is wasted effort — you're throwing away tokens, time, and money. The new code will need to be rewritten when the foundation is eventually fixed. Refactor until you are 100% certain no further refactoring is required, THEN build.

**Do it right the first time. Always.** Even if doing it right takes significantly longer. Never defer correctness — the cost of doing it wrong and fixing later is always higher than doing it right now.

## CRITICAL: Extract Shared Abstractions Before Building Consumers

**When 2+ classes will need the same logic, extract it to a shared location FIRST — before writing either consumer.**

Before building a new service or class:
1. Read ALL related services in the same domain
2. Identify logic that will be shared (type resolution, schema building, data formatting, etc.)
3. Extract shared logic to a trait, base class, or shared service BEFORE implementing consumers
4. Then build consumers using the shared abstraction

**This applies especially across context windows.** When a plan involves multiple services that operate on the same data structures, the plan must explicitly name the shared abstraction and where it lives. Every continuation session needs to know: "shared logic is in X trait/service — use it, don't reinline it."

**The test:** If you're about to write a method and a similar method already exists in another class in the same domain, STOP. Extract to shared location first.

## CRITICAL: Use Instance State — Never Thread Parameters

**When a class method chain shares the same data, store it as instance state.** Passing `$taskRun`, `$plan`, or any shared context through 3+ method signatures is a procedural anti-pattern in OOP. It increases cognitive load, inflates method signatures, creates redundant null checks, and makes refactoring fragile — every parameter pass is a potential bug site during future changes.

**The rule:** If 3+ methods in a class receive the same parameter, it belongs on `$this`. Set it once at the entry point, read it from `$this` in every method.

## CRITICAL: No Wrapper Functions — Composables Directly

**NEVER create wrapper functions around composable calls. Call composables directly from where the data is interacted with.**

A function whose body is a single composable call with slightly different arguments is dead weight. It adds indirection, obscures intent, and violates DRY. Inline it.

**Forbidden:**
```
function onLabelUpdate(label) { actions.edit(directive, { label }); }
function onNameUpdate(name) { actions.edit(directive, { name }); }
```
Call `actions.edit()` directly from the template or from the watcher that has the data.

**The only exception:** Generic/reusable components (SelectField, DanxButton, etc.) that cannot import domain composables because they don't know their context. These use emits and props because they must.

## CRITICAL: Props and Emits Are a Last Resort

**Emits exist only for generic components that cannot know their domain context.** If a component can import a composable, it should call the composable directly — not emit an event asking a parent to call it.

**Props are kept to a minimum.** >4 props on a component is suspicious — the data likely belongs in a composable or typed config object. When extracting code into a new component, design the interface from zero — never mechanically copy the existing prop/event surface.

### Interface Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Props | >4 | Consolidate into config object or read from composable |
| Emits on specialized component | >2 | Component should call composable directly |
| Emits passing through unchanged | Any | Emit chain — break it, call composable at source |

## CRITICAL: Scalar Values Live on the Parent — Never Make API Calls for Single Values

**Never make an API call to fetch a scalar value (count, status, flag, name) that should already be available on a loaded model.** Minimizing unnecessary API calls is always a top priority. If the UI needs a value, that value belongs on the parent model as a field — loaded with the parent, not fetched separately.

**This applies to counts, statuses, booleans, names, and any single value.** If a field doesn't exist on the parent yet, add one (relation counter, computed column, cached attribute, or resource field) — don't invent a fetching mechanism.

**The pattern for counts and related data:**
1. Parent model maintains the count (via relation counter, computed column, or resource field)
2. Resource exposes the count as an eager field and the full list as a lazy field
3. UI reads the count for badges/indicators and loads the list on demand when clicked

## CRITICAL: Build It Right — Never Take Shortcuts

**Every line of code is permanent. Treat it as a long-term solution that the team will maintain and build upon.**

Never optimize for speed of implementation. The "quick and easy" approach creates tech debt, inconsistency, and rework. The correct approach is:

1. **Search first** — Before building anything, search the codebase for existing solutions. Utilities, components, helpers, patterns — someone likely solved this already.
2. **Follow established patterns** — If the codebase does something a specific way, do it that way. Consistency matters more than your preference.
3. **Build for the team** — Write code as if someone else will maintain it tomorrow. Because they will.

**The fast way and the right way are never the same.** If you catch yourself thinking "this is simpler" or "this is good enough," stop — you're about to take a shortcut. Look up the right way and do that instead.

## CRITICAL: You Own the Entire Codebase

**You are 100% responsible for 100% of the code in this repo 100% of the time.** It does not matter who wrote it, when it was written, or whether you touched it in your current diff. If a problem exists, it is your problem. If a reviewer flags it, you fix it.

There are zero valid excuses based on:
- "I didn't write this code"
- "This was pre-existing"
- "This isn't related to my changes"
- "I only made small edits to this file"
- "This would take too long to fix"
- "This needs too many mocks"
- "This is a separate effort"

None of these are reasons. They are rationalizations. The default action for every finding is: **fix it immediately.**

## CRITICAL: Never Guess — Verify Everything

**Do NOT be lazy. ALWAYS do things the right way. NEVER guess. Be 100% sure of what you're doing before you do it.**

This is a blocking rule that applies to ALL work:

- **Before using a prop value** — read the source to confirm it's valid (icon names, types, enums)
- **Before using a component** — read its source to understand its props, slots, and behavior
- **Before writing code** — read the existing implementation to understand patterns and conventions
- **Before making assumptions** — verify with the actual codebase, not your memory or general knowledge
- **If you're not sure** — STOP and look it up. Reading a file takes seconds. Fixing a wrong guess wastes minutes.

Guessing leads to broken code, wasted time, and lost trust. Every time you guess instead of checking, you create work that has to be undone. There is no scenario where guessing is faster than verifying.

## CRITICAL: Domain Guides Are Mandatory Reading

**Before fixing tests, writing code, or explaining behavior in any domain, READ the relevant domain guide first.** Check the project's CLAUDE.md for a "Domain Guides" section — if a guide exists for the domain you're working in, read it before touching anything.

- **Do not infer data models from implementation code.** The guide describes the intended design. Implementation code shows what IS; the guide shows what SHOULD BE. When they disagree, the guide wins.
- **Do not fabricate data structures.** If you don't know what `schema_data` contains, what an artifact's structure looks like, or how objects relate — READ the guide. Never construct a plausible-sounding answer from partial code reads.
- **Do not skip the guide to "save time."** Skipping the guide guarantees wasted time from wrong assumptions. Every minute spent reading saves ten minutes of wrong fixes.

This is a mechanical check: "Am I about to work in a domain that has a guide? Have I read it?" If the answer is no, stop and read it before proceeding.

## CRITICAL: Fallbacks Are Bugs — Fail Loud, Never Fail Silent

**A fallback is the worst kind of bug: a silent one.** The system appears to work while producing wrong results. Every `??`, every default value, every implicit type inference is a potential silent failure that masks malformed data, missing configuration, or caller bugs.

**Failing is GOOD.** Throwing an error when data is missing or malformed is the correct behavior. An exception tells you exactly what's wrong and where. A fallback hides the problem and lets corrupted state propagate through the system until it causes a failure somewhere completely unrelated — where debugging is 10x harder.

**The rule: treat every `??` and default value as suspicious until proven correct.**

**Decision order:**
1. **Throw an error** — this is the DEFAULT. When in doubt, throw. A missing value almost always indicates a caller bug or a misconfigured system. Failing early with a clear error message is infinitely better than silently producing wrong output.
2. **Ask the user** — if you genuinely cannot determine whether a fallback or an error is correct.
3. **Use a fallback** — ONLY when you are 100% certain the default is the intended behavior AND the value is truly optional (e.g., pagination page defaults to 1, optional UI label falls back to name). This is rare. Most values that seem optional are actually required but nobody noticed because the fallback masked the bug.

**Where fallbacks are ALWAYS bugs:**
- Discriminator fields (`type`, `status`, `kind`, `category`, `mode`) — these determine behavioral class. A silent default creates records with unintended behavior.
- Configuration keys — if a config key is missing, the system is misconfigured. Throw, don't guess.
- Structural validation — if a data structure is missing a required field, it's malformed. Throw, don't patch.
- Constructor parameters — if a class needs a value to function, require it explicitly. No defaults that hide missing callers.
- Type inference (`is_array` instead of reading a `state` key) — guessing the structure from the shape of the data is fragile and hides malformed input.

**Code review priority:** Finding and removing silent fallbacks is one of the highest-priority review findings — higher than style, naming, or DRY. A fallback that masks a bug is actively harmful code that must be removed.

## CRITICAL: NEVER Edit JS/Vue Dependency Packages Without Explicit Permission

**danx-ui and quasar-ui-danx are OFF LIMITS unless the user explicitly grants permission.**

Before making ANY change to these packages: tell the user what and why, wait for explicit approval. No exceptions.

**Note:** The danx Laravel package (`/home/newms/web/danx/`) is a direct working directory — edit it yourself, never spawn child agents for it.

## CRITICAL: Production Jobs Must Be Incremental by Default

**Before writing any code that processes data in production, answer: "What happens when this runs the second time?"** If the answer is "it redoes all the work from the first time," the design is wrong.

Any recurring job, sync, migration, or data pipeline that touches production data must be designed for incremental operation from the start:

1. **Identify the delta mechanism** — `updated_at` timestamp, auto-increment ID, sync cursor, changelog. Every table has one.
2. **Store the high-water mark** — after each run, record what was processed so the next run starts where the last one left off.
3. **Only process new/changed rows** — `WHERE updated_at > last_sync_at`, not `SELECT *`.
4. **Never truncate and reload** unless explicitly requested for a one-time migration.

**Why:** A full-table sync that costs $0.01 on day one costs $3.65/year. A full-table sync of 13M rows costs real money every single run — in compute, in BigQuery ingestion fees, in SSH tunnel bandwidth, in MySQL read load. The "simple" approach is the expensive approach. Incremental is the default.

**The test:** Before implementing, state the expected cost/time of the *10th run*, not just the first. If the 10th run does the same work as the 1st, redesign.

## CRITICAL: Observation is not Instruction — Diagnose, Report, Wait

**When the user describes a problem, reports a bug, or asks about unexpected behavior, your ONLY job is to investigate and report.** Do NOT write code. Do NOT implement fixes. Present findings and wait for explicit direction.

See `~/.claude/rules/debugging.md` "Diagnose ≠ Fix" for the full decision table. The short version: unless the user says "fix", "implement", "change", "make it", "do it", or "go ahead," you are in **read-only investigation mode**.

**This applies even when the fix is obvious.** Especially when the fix is obvious — obvious fixes are the most tempting to apply unilaterally, which is exactly why this rule exists. The user's decision authority is not a function of fix complexity.

**Design proposals are not implementation instructions.** When the user says "we need X" or "it should work like Y" during an analysis or planning conversation, they are proposing a direction — not authorizing implementation. Continue the design discussion: confirm the approach, surface edge cases, and wait for an explicit "go ahead" or "make it so" before writing code. The more specific a proposal sounds, the more tempting it is to skip confirmation — resist that temptation.

**Never modify user-authored content without explicit request.** Demo code, documentation, example strings, and similar authored content reflects deliberate choices. Do not delete, reformat, or restructure it based on your own judgment.

**Production errors are observations, not instructions.** When monitoring production and you discover a failure (timeout, exception, crash), your job is to REPORT the finding with data. Never fix production issues autonomously — present the diagnosis and options, then wait. The urgency of a production issue makes it MORE important to confirm with the user, not less. "I saw it failing so I fixed it" is never acceptable — the user may have context you don't (architectural constraints, deployment schedules, other workarounds in progress).
