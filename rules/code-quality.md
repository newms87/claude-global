# Code Quality

`SOLID / DRY / Zero-Debt / One-Way / Read-First / 100%-Tests / Flawless`

## CRITICAL: The Mission Is 100% Perfect Quality Code

Cost and time are not factors. Every file, every method, every test must be correct—there is no budget, deadline, or "good enough". Never skip work because it's hard, time-consuming, or pre-existing. Never construct reasons to avoid work. Never modify reviewer agents or quality gates to reduce findings.

## CRITICAL: Zero Backwards Compatibility

**NEVER introduce backwards compatibility code.** Legacy code hides bugs permanently and lets corrupted state propagate silently. Breaking is better—a clear error tells you exactly what to fix.

**Forbidden patterns:**
- Supporting multiple parameter names or handling "old format" alongside "new format"
- Fallback logic for old names, data structures, or APIs
- Two resolution paths for the same concept
- "Temporary" compatibility code or migration paths that keep old code working
- Shims, scanner anchors, or stubs that exist solely to keep old paths working

**The rule:** ONE correct way to do everything. Fix at source, never add compatibility layers.

## CRITICAL: Legacy Imports ≠ Legacy Module — Default Is Update, Not Delete

**When a module imports a symbol that is being deleted, that is a migration signal, not a deletion signal.** Surface-level coupling to legacy code (imports, docstring examples, string fixtures, shaped-for-legacy data flow) does NOT justify deleting the module. It justifies **updating** the module to use the new system. **~90% of the time the right answer is rewrite, not delete.**

Before removing any file because it "uses legacy code," answer these three questions IN WRITING, as part of the plan, not as post-hoc retro:

1. **What capability does this module provide?** One sentence. If you can't describe the capability without referencing the legacy implementation, you haven't separated the two — keep thinking. Example: "gate_analysis computes per-gate bin-edge predictiveness" is the capability; "gate_analysis reads SHORT_ENTRY_CONDITIONS from a LadderReversion-shaped strategy" is the implementation.
2. **Does that capability apply to the new system?** If yes → **REWRITE** (capability kept, implementation migrates). If no → **DELETE** is justified.
3. **Is deletion a scope decision I'm making unilaterally?** If the capability is used by a UI page, a Makefile target the user uses, a test the user depends on, or any surface outside the immediate legacy blast radius → **surface it to the user before acting.** A "delete legacy" directive from the user is NOT blanket authorization to delete capabilities; it is authorization to remove the LEGACY IMPLEMENTATION of those capabilities.

**Surface signals that indicate UPDATE, not DELETE:**
- The module has a consumer that's still wanted (a UI view, nav link, Makefile target the user references, documented workflow step)
- The capability has an equivalent in the new system (new APIs produce the same class of data the module consumes)
- The module's docstring describes a generic function, even if the current implementation is shaped around a legacy strategy
- The capability appears in user-facing config (gates columns, signals config, analysis pipeline documentation)

**Deletion requires that the CAPABILITY ITSELF is obsolete, not just that the current implementation is.** "It imports a deleted function" is a migration task. "The feature it provides is no longer wanted" is a deletion.

**Inconsistency is the tell.** If you find yourself making opposite decisions (delete vs keep) on two modules that have the same underlying technical problem (e.g. both built on a flat oracle when the system now produces a tier-mode oracle), you are pattern-matching on surface signals — docstring tone, file name — instead of capability. Stop, name the underlying technical problem, and apply the same decision to both.

## CRITICAL: Refactor First — Never Build on Bad Foundation

If you see a DRY or SOLID violation, refactor IMMEDIATELY before building on top of it. Building on code that needs refactoring wastes effort—the new code will need rewriting when the foundation is eventually fixed. Do it right the first time, always, even if significantly longer.

## CRITICAL: Extract Shared Abstractions Before Building Consumers

When 2+ classes will need the same logic, extract it to a shared location FIRST before writing either consumer. Read all related classes in the domain, identify shared patterns, extract to trait/base class/service, then build consumers. For cross-session work, name the shared abstraction explicitly in planning so continuation sessions use it instead of reinlining.

## CRITICAL: Use Instance State — Never Thread Parameters

When a class method chain shares the same data, store it as instance state. Passing the same context through 3+ method signatures is a procedural anti-pattern that inflates signatures, creates null checks, and makes refactoring fragile. If 3+ methods receive the same parameter, it belongs on `$this`.

## CRITICAL: No Wrapper Functions — Composables Directly

Never create wrapper functions around composable calls. Call composables directly from where the data is interacted with. A function whose body is a single composable call is dead weight that adds indirection and violates DRY.

**Exception:** Generic/reusable components (SelectField, DanxButton) that cannot import domain composables because they don't know their context. These must use emits and props.

## CRITICAL: Props and Emits Are a Last Resort

Emits exist only for generic components that cannot know their domain context. If a component can import a composable, it should call it directly—not emit an event asking a parent to call it. Props are kept to a minimum: >4 props is suspicious (consolidate into config object or read from composable), >2 emits on specialized components is suspicious (component should call composable directly), and emits passing through unchanged should be broken and called at source.

## CRITICAL: Scalar Values Live on Parent — Never API Call for Single Values

Never make an API call to fetch a scalar value (count, status, flag, name) that should already be on a loaded model. If the UI needs a value, it belongs on the parent model as a field—loaded with the parent, not fetched separately. If a field doesn't exist yet, add one (relation counter, computed column, cached attribute, or resource field) instead of inventing a fetching mechanism.

## CRITICAL: Build It Right — Never Take Shortcuts

Every line of code is permanent—treat it as a long-term solution. Search first for existing solutions before building anything. Follow established patterns (consistency matters more than preference). Build for the team—write code as if someone else will maintain it tomorrow. The fast way and the right way are never the same; when tempted by "this is simpler," look up the right way instead.

## CRITICAL: You Own the Entire Codebase

You are 100% responsible for 100% of the code 100% of the time, regardless of who wrote it or when. If a problem exists, it's your problem. No valid excuses: not your code, pre-existing, unrelated to changes, would take too long, needs too many mocks, separate effort. Cross-session ownership applies: you ARE every previous Claude session. Investigate, explain, and own untracked files and stale artifacts.

## CRITICAL: Never Guess — Verify Everything

Before using a prop value, component, or writing code, read the source to verify (icon names, types, enums, props, slots, behavior). Before making assumptions, verify with the actual codebase. Reading a file takes seconds; fixing a wrong guess wastes minutes. Guessing leads to broken code, wasted time, and lost trust.

## CRITICAL: Read Comments On Methods and Classes Before Editing or Investigating

Comments on a class, method, or function are authoritative context from whoever last understood the code. They exist specifically to save the next reader (you) from repeating a mistake, missing a constraint, or misreading behavior. **Read them before editing the code and before asserting what the code does.**

Mechanical check — before any Edit to a method/class OR any factual claim about its behavior:

1. **Open the file and read the comment block(s) above the symbol** — docstring, JSDoc, PHPDoc, Python docstring, C#/Rust `///`, Go doc comment, `/** */`, or plain `// comment` lines immediately preceding the declaration.
2. **Read inline comments inside the body** that mark non-obvious logic, invariants, workarounds, or "do not X because Y" warnings.
3. **Read header / file-top comments** on the file containing the symbol — they often describe module-level invariants that bind every method inside.
4. **Read comments on callers and on any overridden parent** — if the method overrides an interface or base class, its contract lives on the parent's comment. A comment on the caller may state a precondition you're about to violate.

**Do not skip comments because:**
- "The name is obvious" — names lie; comments don't.
- "I can infer from the body" — the body shows mechanism; the comment shows intent and constraint.
- "It's just a one-line change" — one-line changes break invariants documented one line above them.
- "The comment is probably stale" — assume it's current until you've proven otherwise. If you suspect it's stale, verify against behavior, then update the comment in the same edit.

If your edit or assertion contradicts an existing comment, STOP. Either the comment is stale (update it as part of your change) or your understanding is wrong (revise the plan). Silent contradiction — changing the code so the comment becomes a lie — is a zero-tech-debt violation.

This rule applies equally during investigation: when reading code to answer "how does X work" or "why does Y happen," the comments are primary evidence, not decoration.

## CRITICAL: Domain Guides Are Mandatory Reading

Before fixing tests, writing code, or explaining behavior in any domain, read the relevant domain guide first. Do not infer data models from implementation code (guide describes intended design; code shows what IS). Do not fabricate data structures. Skipping the guide guarantees wasted time. Mechanical check: "Am I about to work in a domain with a guide? Have I read it?" If no, stop and read it first.

## CRITICAL: Fallbacks Are Bugs — Fail Loud, Never Fail Silent

A fallback is a silent bug—the system appears to work while producing wrong results. Failing is good; throwing an error tells you exactly what's wrong and where. Fallbacks hide problems and let corrupted state propagate until debugging is 10x harder.

**Decision order:** Throw an error (DEFAULT—missing values almost always indicate caller bugs), ask the user (if you cannot determine correctness), use a fallback (ONLY when 100% certain the default is intended AND the value is truly optional, which is rare).

**Where fallbacks are ALWAYS bugs:** Discriminator fields (`type`, `status`, `kind`), configuration keys, structural validation, constructor parameters, type inference (guessing structure from shape).

## CRITICAL: NEVER Edit danx-ui Without Explicit Permission

danx-ui is OFF LIMITS unless the user explicitly grants permission. Before any change: tell the user what and why, wait for explicit approval.

## CRITICAL: Production Jobs Must Be Incremental by Default

Before writing code that processes production data, answer: "What happens when this runs the second time?" If it redoes all the work, the design is wrong. Any recurring job, sync, migration, or pipeline touching production must be incremental: identify delta mechanism (`updated_at`, auto-increment, sync cursor), store high-water mark after each run, only process new/changed rows, never truncate-and-reload. Test: state expected cost/time of the 10th run, not just the first. If identical, redesign.

## CRITICAL: Observation Is Not Instruction

When the user describes a problem, reports a bug, or asks about unexpected behavior, your only job is to investigate and report. Do NOT write code or implement fixes. Present findings and wait for explicit direction. This applies even when the fix is obvious. See `debugging.md` for full decision rules. Design proposals are not implementation instructions—confirm the approach and wait for explicit "go ahead" before coding. Never modify user-authored content without explicit request. Production errors are observations: report findings and options, wait for user direction.
