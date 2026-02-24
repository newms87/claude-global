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

### Forbidden Patterns

- Supporting multiple parameter names (`$param = $params['old_name'] ?? $params['new_name'] ?? null;`)
- Comments containing "backwards compatibility", "legacy support", "deprecated"
- Code that handles "old format" or "new format" simultaneously
- Fallback logic for old parameter names, data structures, or APIs

### The Rule

ONE correct way to do everything. If something uses the wrong name, fix it at the source. Never add compatibility layers.

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

## CRITICAL: NEVER Edit JS/Vue Dependency Packages Without Explicit Permission

**danx-ui and quasar-ui-danx are OFF LIMITS unless the user explicitly grants permission.**

Before making ANY change to these packages: tell the user what and why, wait for explicit approval. No exceptions.

**Note:** The danx Laravel package (`/home/newms/web/danx/`) is a direct working directory — edit it yourself, never spawn child agents for it.

## Observation is not Instruction

When the user describes a behavior or limitation, DO NOT immediately start "fixing" it. Ask what they want to do about it. Present options. Wait for direction. Only act when explicitly asked.

**Never modify user-authored content without explicit request.** Demo code, documentation, example strings, and similar authored content reflects deliberate choices. Do not delete, reformat, or restructure it based on your own judgment.
