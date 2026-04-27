# Planning Rules

## Trello Card Overrides Plan Mode

Trello card assigned → NEVER use EnterPlanMode. Card IS plan. Update card description directly if plan changes.

## Plan Files

**Location:** `~/.claude/plans/` only. Create ONLY via `EnterPlanMode`. Never write plan files manually.

**Editing:** Use Edit (preserves content). Never use Write (overwrites everything).

**Content:** Prose only — zero code blocks. Code locks in details before approval.

**Zero-context test:** Write as if amnesic. Include exact file paths, specific method names, clear reasoning.

## CRITICAL: Card Instructions Are Not Suggestions

Card specifies technical approach (endpoint to call, component to reuse, data to display) → requirement, not suggestion replaceable with simpler alternative. Specified approach has genuine technical blocker → STOP, report blocker to user with proposed alternative. Never silently substitute placeholder + mark work complete. "Too complex" + "too coupled" not blockers — engineering problems to solve.

## Implementation Checklist

Before starting, create checklist of all discussed items. Track each. ANY item incomplete at commit time → STOP immediately + tell user what wasn't implemented. Never commit partial work.

Before checking off any item, verify literal claim true (via grep/test/code read).

## Shared Abstractions

2+ classes share logic → explicitly name abstraction + where lives. Continuation sessions need know: "use X trait/service, don't reinline."

## Phases

Use multiple phases only when scope exceeds single pipeline run. Each phase = complete pipeline run. Phases never justify backwards compat — broken code signals next phase to fix.

**CRITICAL: One Phase = One Commit = One Card Lifecycle.** Each phase card gets own commit. After each phase commit: check off all AC + Progress items on phase card, move phase card to Done, check off phase on epic's Implementation Phases checklist. Do NOT batch multiple phases into single commit — makes structurally impossible maintain accurate card state. Commit boundary IS phase boundary.

## Refactoring Tools

Renaming/moving symbols across files → specify tool in plan: `phpactor class:move` (PHP), `ts-morph`/`gopls rename`/`rope` (other languages). Never plan manual find-and-replace.

## Code Review Priorities

Code review = running reviewer agents via Task tool, NOT you reading code.

**Run when:** Multi-file, >10 lines, new feature, phase completion.

**Priority order:**
1. Legacy code, backwards compatibility, dead code
2. Silent fallbacks (`??`, defaults, implicit infers)
3. Everything else (style, DRY, tests)

Never modify reviewer agents to reduce findings. Reviewers intentionally aggressive — fix all findings.

## The Pipeline (Automatic)

1. Implement (write code, tests)
2. `/flow-code-review` (fix findings)
3. `/flow-quality-check` (audit decisions)
4. `/flow-commit` (stage and commit)
5. `/flow-report` (present results)
6. Mark phase complete
7. Repeat for next phase
8. `/flow-finish` (at session end — Action Items + knowledge dump)

**CRITICAL:** Pipeline automatic. User approval of plan = pre-approval for entire pipeline. NEVER pause between steps. NEVER ask "ready for code review?" Just execute. Do NOT skip quality gates.

Quality gates run after each phase (independent domains) or once after all related phases (same domain). Never skip.

**CRITICAL: Phase with no code change still runs pipeline.** Verification-only phases, plan-only phases, research phases NOT exempt. Still run `/flow-report` at phase end + `/flow-finish` at session end. Code-oriented steps (`/flow-code-review`, `/flow-quality-check`, `/flow-commit`) = no-ops on empty diff — still invoke + exit cleanly with "nothing to review / nothing to commit." Pipeline not conditional on code being changed; structure for phase + session closure.

**`/flow-finish` NEVER optional.** Regardless whether session produced commits, plans, or only investigation, every session ends with `/flow-finish`. Captures unwritten knowledge + formalizes Action Items otherwise lost when context window destroyed. Skipping `/flow-finish` because "already filed action items manually" or "no code change" = classic end-of-session shortcut. Do not take.

**Rationalization to watch for:** "No code change, so no pipeline." Wrong. Pipeline = structure, not work — ensures closure happens. Skipping steps because phase light → STOP + run anyway.

## Questions Are Not Decisions

User asks question → answer + wait explicit agreement ("go ahead", "do it", "yes") before editing plan.

## "Review the Plan"

Call `ExitPlanMode` immediately. That = how user approves plans.