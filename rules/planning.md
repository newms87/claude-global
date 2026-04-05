# Planning Rules

## Trello Card Overrides Plan Mode

When a Trello card is assigned, NEVER use EnterPlanMode. The card IS the plan. Update the card description directly if the plan changes.

## Plan Files

**Location:** `~/.claude/plans/` only. Create them ONLY via `EnterPlanMode`. Never write plan files manually.

**Editing:** Use Edit (preserves content). Never use Write (overwrites everything).

**Content:** Prose only — zero code blocks. Code locks in details before approval.

**Zero-context test:** Write as if you have amnesia. Include exact file paths, specific method names, and clear reasoning.

## Implementation Checklist

Before starting, create a checklist of all discussed items. Track each one. If ANY item is incomplete at commit time, STOP immediately and tell the user what wasn't implemented. Never commit partial work.

Before checking off any item, verify the literal claim is true (via grep/test/code read).

## Shared Abstractions

When 2+ classes share logic, explicitly name the abstraction and where it lives. Continuation sessions need to know: "use X trait/service, don't reinline."

## Phases

Use multiple phases only when scope exceeds a single pipeline run. Each phase is a complete pipeline run. Phases never justify backwards compatibility — broken code signals the next phase to fix it.

## Refactoring Tools

When renaming/moving symbols across files, specify the tool in the plan: `phpactor class:move` (PHP), `ts-morph`/`gopls rename`/`rope` (other languages). Never plan manual find-and-replace.

## Code Review Priorities

Code review = running reviewer agents via Task tool, NOT you reading code.

**Run when:** Multi-file, >10 lines, new feature, phase completion.

**Priority order:**
1. Legacy code, backwards compatibility, dead code
2. Silent fallbacks (`??`, defaults, implicit infers)
3. Everything else (style, DRY, tests)

Never modify reviewer agents to reduce findings. Reviewers are intentionally aggressive — fix all findings.

## The Pipeline (Automatic)

1. Implement (write code, tests)
2. `/flow-code-review` (fix findings)
3. `/flow-quality-check` (audit decisions)
4. `/flow-commit` (stage and commit)
5. `/flow-self-improvement` (process notes)
6. Mark phase complete
7. Repeat for next phase
8. `/flow-report` (after ALL phases complete)

**CRITICAL:** Pipeline is automatic. User approval of plan = pre-approval for entire pipeline. NEVER pause between steps. NEVER ask "ready for code review?" Just execute. Do NOT skip quality gates.

Quality gates run after each phase (independent domains) or once after all related phases (same domain). Never skip them.

## Questions Are Not Decisions

When the user asks a question, answer and wait for explicit agreement ("go ahead", "do it", "yes") before editing the plan.

## "Review the Plan"

Call `ExitPlanMode` immediately. That is how the user approves plans.
