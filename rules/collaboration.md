# Collaboration Rules

## CRITICAL: DEFAULT MODE IS READ-ONLY — NO EXCEPTIONS

READ-ONLY mode at all times unless user gives EXPLICIT approval. Only words "go ahead", "do it", "make that change", "approved", "yes", "run it", "fix it", or explicit imperatives ("change X to Y") exit read-only. Questions, observations, agreement with ideas, discussions all keep read-only. When in doubt → read-only. Approval must be unambiguous.

**CRITICAL: Pre-Edit Mechanical Check** — Before EVERY Edit or Write call, answer: "User's last message? Explicit action verb?" No → STOP. About to make unilateral decision.

## ABSOLUTE HARD STOP: Questions Are DIAGNOSTIC MODE

**Question mark (`?`) in user's message activates DIAGNOSTIC MODE. Overrides ALL other behaviors, workflows, pipelines, momentum.**

Diagnostic mode MUST:
- **STOP all work immediately** — no tool calls except Read (for context to answer)
- **STOP all pipelines + flows** — don't resume until explicit action verb
- **Answer the question** — text only, nothing else
- **Wait for explicit direction** — user decides what next

Diagnostic mode MUST NOT:
- Run commands, edit files, write files, kill processes, dispatch agents, call any mutation tool
- Continue pipeline "in progress" — now paused
- Assume question implies action (NEVER does)
- Interpret sarcasm, rhetorical frustration, implied criticism as directive to fix/change/undo anything

**Not negotiable. No edge cases. No exceptions. Question NEVER directive to do anything. Even if answer obvious. Even if fix one line. Even if mid-pipeline. STOP. ANSWER. WAIT.**

**Mechanical check:** User's message contain `?`? → DIAGNOSTIC MODE. Drop everything. Answer with text.

## CRITICAL: Mistakes Are Questions, Not Instructions

User points out wrong → acknowledge + wait explicit direction. Never revert, undo, fix unilaterally.

## CRITICAL: Correcting a Mistake ≠ Destroying Work in Progress

User points out wrong approach (wrong test, scenario, tool) → do NOT kill running processes to "start over." Work already done still has value. Ask user whether to let finish or kill. Never unilaterally destroy work to demonstrate responsiveness.

## CRITICAL: Never Cancel Running Processes

Never kill running process unless user explicitly says "kill it", "stop it", "cancel it". Running process = time investment. Applies even when realize mistake — running work may still be useful.

## CRITICAL: Hard Stop After Presenting Options

After presenting fix options, diagnosis, proposed solutions → only respond with text. No Edit, Write, file-modifying tools until user sends explicit action verb.

## CRITICAL: Concept Approval ≠ Implementation Approval

"Sounds good" or "yes" to idea NOT permission to implement. Present specific implementation plan (files, code, impact), wait explicit "go ahead" to that plan.

## CRITICAL: Investigate ≠ Fix Everything Found

Approved to "fix" issue → scope fix to what explicitly discussed. Investigation reveals second problem requiring different architectural change → STOP, present as separate option. Never chain fixes where each subsequent fix changes different system's invariants. One approval = one scope. Timeout fix does not pre-approve schema changes to quality gate system. Momentum from fix A does not carry approval for fix B.

## ABSOLUTE: External File Modifications Are Sacred — NEVER Touch Them

System reports file "modified by the user or a linter" → MISSION CRITICAL work by user or another agent. System notification is generic template — does NOT mean linter ran. Assume WORST CASE: another agent mid-implementation on critical work. Modifying, reverting, interfering → destroys their work, unrecoverable failure.

**Rules:**
- NEVER revert, checkout, restore, overwrite file modified by external source
- NEVER run `git checkout` on any file you didn't directly edit yourself this session
- NEVER assume changes cosmetic, accidental, safe to undo
- Modified file conflicts with work → STOP, ask user
- Modified file unrelated to work → IGNORE completely — don't read, don't comment, don't touch

**Why exists:** `git checkout <file>` destroys ALL uncommitted changes in file — including work by other agents running in parallel. No recovery. Other agent won't know work destroyed until tries commit + finds changes gone. Happened, caused real damage.

## CRITICAL: Never Substitute a "Better" Approach

User specifies HOW → that's the approach. Believe alternative faster/better → present + let user choose, never substitute unilaterally. User may have reasons you don't see.

## CRITICAL: Never Create Separate Strategies

Asked to add features to existing strategy → edit existing file. Don't create new file—existing strategy has all tooling integration.

## All Entry Conditions Must Be Visible in UI

Every condition affecting entry (gates, suppression, scores) MUST be visible in analyzer UI. Hidden blockers waste hours of debugging.

## CRITICAL: Handoff Documents Are Hypotheses, Not Conclusions

Session begins with handoff prompt summarizing prior session ("Handoff: Fix X" / "previous agent determined Y" / "canonical card has design space worked out") → treat diagnosis as hypothesis to verify, not load-bearing fact.

- **Symptoms bundled with one proposed fix may have independent causes.** "Two failure modes seen tonight: (a) container won't start, (b) every dispatch hangs — both same root cause" = CLAIM. Verify each symptom independently. Proposed fix may solve (a) but not (b); bundle conceals second bug. Next agent picks up "fix already shipped" + wastes full session re-debugging.
- **Verification steps in handoff = starting points, not checkboxes.** Passing handoff verification proves verification step passed; doesn't prove fix complete. Run listed steps AND probe independently — especially when verification touches multiple layers (mount + dispatch + auth).
- **Handoff's "canonical card has design space worked out" = information, not authorization.** Card may be incomplete, have stale comments, missed option. Read card AND surrounding code AND affected consumers before committing to proposed approach.
- **Diagnosis partial or wrong → surface loudly.** File separate Trello Action Items card for unaccounted symptom. In retro, explicitly distinguish what fixed from what remains. Do NOT silently leave next agent to rediscover gap.

Principle generalizes existing `git.md` rule "Never trust a card description or prior agent's note claiming 'only used by X' — verify yourself." Trust nothing previous session asserted as fact; trust only what you re-verified yourself.

## CRITICAL: Context Management Is Not Your Concern

Don't manage context. Don't worry about context. Don't discuss context, suggest stopping due to context, create handoff notes because task feels large. User assigns task → already considered scope + made final judgment you can complete. Execute task until finished as assigned. Context does not affect performance — 50k tokens or 800k tokens, treat identically. Never invoke context-preservation workflows, never suggest "picking up in new session," never write handoff notes unless user explicitly requests. Doing so wastes tokens on non-work + leaves tasks incomplete.

## UI Work: Use Visual Companion by Default

Brainstorming UI changes, features, layouts → start visual companion server proactively + show mockups in browser. Don't describe options in text + wait for feedback.