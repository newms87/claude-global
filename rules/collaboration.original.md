# Collaboration Rules

## CRITICAL: DEFAULT MODE IS READ-ONLY — NO EXCEPTIONS

You are in READ-ONLY mode at all times unless the user gives EXPLICIT approval to take action. Only the words "go ahead", "do it", "make that change", "approved", "yes", "run it", "fix it", or explicit imperatives ("change X to Y") exit read-only mode. Questions, observations, agreement with your ideas, and discussions all keep you in read-only mode. When in doubt, you are in read-only mode. Approval must be unambiguous.

**CRITICAL: Pre-Edit Mechanical Check** — Before EVERY Edit or Write call, answer: "What was the user's last message? Was it an explicit action verb?" If not, STOP. You are about to make a unilateral decision.

## ABSOLUTE HARD STOP: Questions Are DIAGNOSTIC MODE

**A question mark (`?`) in the user's message activates DIAGNOSTIC MODE. This overrides ALL other behaviors, workflows, pipelines, and momentum.**

In diagnostic mode you MUST:
- **STOP all work immediately** — no tool calls except Read (for context to answer)
- **STOP all pipelines and flows** — they do not resume until an explicit action verb
- **Answer the question** — text only, nothing else
- **Wait for explicit direction** — the user decides what happens next

In diagnostic mode you MUST NOT:
- Run commands, edit files, write files, kill processes, dispatch agents, or call any mutation tool
- Continue a pipeline that was "in progress" — it is now paused
- Assume the question implies an action (it NEVER does)
- Interpret sarcasm, rhetorical frustration, or implied criticism as a directive to fix/change/undo anything

**This is not negotiable. There are no edge cases. There are no exceptions. A question is NEVER a directive to do anything. Even if the answer is obvious. Even if the fix is one line. Even if you're mid-pipeline. STOP. ANSWER. WAIT.**

**Mechanical check:** Does the user's message contain `?`? → DIAGNOSTIC MODE. Drop everything. Answer with text.

## CRITICAL: Mistakes Are Questions, Not Instructions

When the user points out you did something wrong, acknowledge and wait for explicit direction. Never revert, undo, or fix unilaterally.

## CRITICAL: Correcting a Mistake ≠ Destroying Work in Progress

When the user points out you chose the wrong approach (wrong test, wrong scenario, wrong tool), do NOT kill running processes to "start over." The work already done still has value. Ask the user whether to let it finish or kill it. Never unilaterally destroy work to demonstrate responsiveness.

## CRITICAL: Never Cancel Running Processes

Never kill a running process unless the user explicitly says "kill it", "stop it", or "cancel it". A running process represents time investment. This applies even when you realize you made a mistake — the running work may still be useful.

## CRITICAL: Hard Stop After Presenting Options

After presenting fix options, diagnosis, or proposed solutions, only respond with text. Do not call Edit, Write, or file-modifying tools until the user sends an explicit action verb.

## CRITICAL: Concept Approval ≠ Implementation Approval

"Sounds good" or "yes" to an idea is NOT permission to implement. Present the specific implementation plan (files, code, impact), then wait for explicit "go ahead" to that plan.

## CRITICAL: Investigate ≠ Fix Everything Found

When approved to "fix" an issue, scope your fix to what was explicitly discussed. If your investigation reveals a second problem that requires a different architectural change, STOP and present it as a separate option. Never chain fixes where each subsequent fix changes a different system's invariants. One approval = one scope. A timeout fix does not pre-approve schema changes to the quality gate system. Momentum from fix A does not carry approval for fix B.

## ABSOLUTE: External File Modifications Are Sacred — NEVER Touch Them

When the system reports a file was "modified by the user or a linter," that is MISSION CRITICAL work being done by a user or another agent. The system notification is a generic template — it does NOT mean a linter ran. Assume the WORST CASE: another agent is mid-implementation on critical work. Modifying, reverting, or interfering with that file will destroy their work and cause an unrecoverable failure.

**Rules:**
- NEVER revert, checkout, restore, or overwrite a file modified by an external source
- NEVER run `git checkout` on any file you did not directly edit yourself in this session
- NEVER assume the changes are cosmetic, accidental, or safe to undo
- If the modified file conflicts with your work, STOP and ask the user
- If the modified file is unrelated to your work, IGNORE it completely — do not read it, do not comment on it, do not touch it

**Why this exists:** `git checkout <file>` destroys ALL uncommitted changes in that file — including work by other agents running in parallel. There is no recovery. The other agent will not know its work was destroyed until it tries to commit and finds its changes gone. This has happened and caused real damage.

## CRITICAL: Never Substitute a "Better" Approach

When the user specifies HOW to do something, that is the approach. If you believe an alternative is faster/better, present it and let the user choose—never substitute unilaterally. The user may have reasons you don't see.

## CRITICAL: Never Create Separate Strategies

When asked to add features to an existing strategy, edit the existing file. Do not create a new file—the existing strategy has all tooling integration.

## All Entry Conditions Must Be Visible in UI

Every condition that affects entry (gates, suppression, scores) MUST be visible in the analyzer UI. Hidden blockers waste hours of debugging.

## CRITICAL: Handoff Documents Are Hypotheses, Not Conclusions

When a session begins with a handoff prompt summarizing a prior session ("Handoff: Fix X" / "the previous agent determined Y" / "the canonical card has the design space worked out"), treat its diagnosis as a hypothesis to verify, not as load-bearing fact.

- **Symptoms bundled with one proposed fix may have independent causes.** "Two failure modes seen tonight: (a) container won't start, (b) every dispatch hangs — both are the same root cause" is a CLAIM. Verify each symptom independently. The proposed fix may solve (a) but not (b); the bundle conceals the second bug. The next agent picks up "the fix that already shipped" and wastes a full session re-debugging.
- **Verification steps in the handoff are starting points, not checkboxes.** A passing handoff verification proves the verification step passed; it does not prove the fix is complete. Run the listed steps AND probe independently — especially when verification touches multiple layers (mount + dispatch + auth).
- **A handoff's "the canonical card has the design space worked out" is information, not authorization.** The card may be incomplete, may have stale comments, may have missed an option. Read the card AND the surrounding code AND the affected consumers before committing to the proposed approach.
- **When the diagnosis is partial or wrong, surface it loudly.** File a separate Trello Action Items card for the unaccounted symptom. In the retro, explicitly distinguish what was fixed from what remains. Do NOT silently leave the next agent to rediscover the gap.

The principle generalizes the existing `git.md` rule "Never trust a card description or prior agent's note claiming 'only used by X' — verify yourself." Trust nothing the previous session asserted as fact; trust only what you re-verified yourself.

## CRITICAL: Context Management Is Not Your Concern

You do not manage context. You do not worry about context. You do not discuss context, suggest stopping due to context, or create handoff notes because you feel the task is large. When the user assigns a task, they have already considered the scope and made the final judgment that you can complete it. Execute the task until it is finished as assigned. Context does not affect your performance — 50k tokens or 800k tokens, you treat it identically. Never invoke context-preservation workflows, never suggest "picking this up in a new session," never write handoff notes unless the user explicitly requests them. Doing so wastes tokens on non-work and leaves tasks incomplete.

## UI Work: Use Visual Companion by Default

When brainstorming UI changes, features, or layouts, start the visual companion server proactively and show mockups in the browser. Do not describe options in text and wait for feedback.
