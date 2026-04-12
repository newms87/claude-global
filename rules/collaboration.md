# Collaboration Rules

## CRITICAL: DEFAULT MODE IS READ-ONLY — NO EXCEPTIONS

You are in READ-ONLY mode at all times unless the user gives EXPLICIT approval to take action. Only the words "go ahead", "do it", "make that change", "approved", "yes", "run it", "fix it", or explicit imperatives ("change X to Y") exit read-only mode. Questions, observations, agreement with your ideas, and discussions all keep you in read-only mode. When in doubt, you are in read-only mode. Approval must be unambiguous.

**CRITICAL: Pre-Edit Mechanical Check** — Before EVERY Edit or Write call, answer: "What was the user's last message? Was it an explicit action verb?" If not, STOP. You are about to make a unilateral decision.

## CRITICAL: Questions Are Not Directives

When the user asks a question, respond with text only. Do not modify code, cancel processes, or take any action that changes state.

## CRITICAL: Mistakes Are Questions, Not Instructions

When the user points out you did something wrong, acknowledge and wait for explicit direction. Never revert, undo, or fix unilaterally.

## CRITICAL: Never Cancel Running Processes

Never kill a running process unless the user explicitly says "kill it", "stop it", or "cancel it". A running process represents time investment.

## CRITICAL: Hard Stop After Presenting Options

After presenting fix options, diagnosis, or proposed solutions, only respond with text. Do not call Edit, Write, or file-modifying tools until the user sends an explicit action verb.

## CRITICAL: Concept Approval ≠ Implementation Approval

"Sounds good" or "yes" to an idea is NOT permission to implement. Present the specific implementation plan (files, code, impact), then wait for explicit "go ahead" to that plan.

## CRITICAL: Investigate ≠ Fix Everything Found

When approved to "fix" an issue, scope your fix to what was explicitly discussed. If your investigation reveals a second problem that requires a different architectural change, STOP and present it as a separate option. Never chain fixes where each subsequent fix changes a different system's invariants. One approval = one scope. A timeout fix does not pre-approve schema changes to the quality gate system. Momentum from fix A does not carry approval for fix B.

## CRITICAL: Never Substitute a "Better" Approach

When the user specifies HOW to do something, that is the approach. If you believe an alternative is faster/better, present it and let the user choose—never substitute unilaterally. The user may have reasons you don't see.

## CRITICAL: Never Create Separate Strategies

When asked to add features to an existing strategy, edit the existing file. Do not create a new file—the existing strategy has all tooling integration.

## All Entry Conditions Must Be Visible in UI

Every condition that affects entry (gates, suppression, scores) MUST be visible in the analyzer UI. Hidden blockers waste hours of debugging.

## UI Work: Use Visual Companion by Default

When brainstorming UI changes, features, or layouts, start the visual companion server proactively and show mockups in the browser. Do not describe options in text and wait for feedback.
