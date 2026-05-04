# Claude Global Rules

## Skill Priority (Canonical Workflow Doctrine)

**flow-* IS canonical.** Pipeline: implement -> `flow-code-review` -> `flow-quality-check` -> `flow-commit` -> `flow-report` (per phase) -> `flow-finish` (session end). `next-phase` advances. `wow` reloads rules before each impl phase. Automatic — never pause between steps.

**Plan source priority:**
1. Trello card assigned (or `danx-issue` after Phase 2 epic) → card IS the plan. Never use EnterPlanMode.
2. No card + multi-step → `EnterPlanMode` → `~/.claude/plans/` (prose only).
3. No card + investigation → `debugging` skill.

**Superpowers skills — DEPRECATED for this user (do NOT invoke):**
- `requesting-code-review` → use `flow-code-review` instead
- `receiving-code-review` → use `flow-code-review` (fix all findings) instead
- `finishing-a-development-branch` → use `flow-commit` + `flow-finish` instead (no feature-branch model — commit directly to main)
- `systematic-debugging` → use `debugging` skill instead
- `test-driven-development` → use `testing` skill instead
- `verification-before-completion` → use `flow-quality-check` instead

**Superpowers skills — RETAINED (use when needed):**
- `dispatching-parallel-agents` → 2+ independent tasks, no shared state
- `using-git-worktrees` → isolated worktree for parallel feature work
- `subagent-driven-development` → executing plan via independent subagent tasks in current session
- `writing-skills` → creating or editing skill files

Plan files live in `~/.claude/plans/` only. Superpowers `docs/superpowers/specs/` + `docs/superpowers/plans/` paths NOT used here.

---

**Read-only default.** No modify without explicit approval ("go ahead," "do it," "fix it," direct imperative). Questions, observations, "sounds good" = NOT approval. After presenting options, hard stop — text only until action verb.

**QUESTIONS = FULL STOP.** Question mark in user message → DIAGNOSTIC MODE. Stop ALL work, pipelines, flows. Answer text only. No commands, edits, kills, actions. No resume until explicit action verb. No exceptions. No "but mid-pipeline." No "fix obvious." STOP. ANSWER. WAIT.

**Verify, never guess.** Read source before using any prop, component, API, value. Read existing code before writing new. Wrong guess > cost of reading file.

**No backwards compat. No legacy code. No silent fallbacks.** ONE correct pattern. Throw errors default — fallbacks hide bugs forever. Loud break > "working" code with two paths.

**TDD EVERY change — no exceptions, no category exemptions.** Failing test first → fix/implement → verify. Infrastructure, config, cross-process, agent dispatch — ALL need test. "Can't be unit tested" = don't understand problem yet. Never claim works without test evidence. **Full procedure + testing rules in `testing` skill — see MANDATORY rule below.**

**MANDATORY: Invoke `testing` skill FIRST time you run, write, fix, inspect, reason about ANY test in session — unit, integration, system, validation, snapshot, E2E, single test, full suite, filtered, bug-repro, "just one quick run." No exceptions. No minimum size. No "I know what I'm doing" escape hatch.** Call via Skill tool BEFORE first test-related tool call — not after. "Quick sanity check," "just filter one test," "see if it passes," "5-second run" = EXACTLY where rule gets skipped + re-run cycle begins. Skill = TodoWrite checklist preventing lost output, re-running-to-change-stdout, symptom-suppressing assertion edits, "pre-existing failure" excuses.

**MANDATORY: Invoke `debugging` skill on ANY bug, error, unexpected value, failing test, user report, "that's odd" thought, INVESTIGATION (user says "investigate," "look into," "find out," "why is X," "how does Y work"), OR any time about to ASSERT factually about local system state, timing, behavior, causality, "why X works this way" — no minimum size, no exceptions, no "explanation mode" escape hatch.** Call via Skill tool BEFORE commands, code analysis reads, drafting answer with claims about system. Skill = workflow. "Quick fix" + "I know what it is" = exactly where shortcuts produce wrong fixes. If planned answer contains "probably," "typically," "usually," "on the order of," "a matter of," "cold start," "warm system" about local behavior → failure mode this rule prevents. Stop, invoke skill, measure.

**Own entire codebase.** "Pre-existing" + "out of scope" = NOT valid reasons to skip work.

---

## Rule Index

Every rule below has full context in referenced rules file. Loaded automatically.

**Collaboration** — Read-only default. **Questions = FULL STOP (diagnostic mode, no actions).** Hard stop after presenting options. Concept approval != implementation approval. Never cancel running processes. Correcting mistake ≠ destroying work in progress. Never substitute "better" approach. Visual companion for UI brainstorming.

**Code Quality** — SOLID/DRY/Zero-Debt. Refactor before building. Extract shared abstractions first. Instance state over param threading. Props/emits last resort. Scalar values on parent model. Production jobs must be incremental. Never edit danx-ui without permission. **Read method/class comments before editing or asserting behavior** — docstrings, JSDoc, file-top comments, inline invariant notes = authoritative. Change contradicts comment → either comment updates same edit or plan wrong.

**Debugging** — Invoke `debugging` skill immediately on: bugs/errors/unexpected values, "that's odd" thoughts, **investigations** ("investigate," "look into," "why is X," "how does Y work"), **any factual assertion about local system state, timing, behavior, causality**. Explanation mode not exempt. Skill = discipline; never investigate or assert without it.

**Testing** — Invoke `testing` skill FIRST before any test-related action (run/write/fix/skip/delete — even one filtered test). Skill = TodoWrite checklist; rules file = pointer. Triggers + anti-patterns in `testing.md`; full procedure in skill.

**Planning** — Trello card overrides plan mode. Plans = prose (never code). Complete ALL planned work. Never check off incomplete work. Zero-context test for plans. Pipeline automatic: implement -> /flow-code-review -> /flow-quality-check -> /flow-commit -> /flow-report (per phase) -> /flow-finish (session end).

**Git** — Never delete repos. Always use /flow-commit. Never stash, never reset other changes. Revert via Edit, never git checkout. Check for other agents' staged work before committing.

**Tools** — Use Read/Edit/Write/Glob/Grep, never bash equivalents. Lint runs via hooks auto. Import order: usage first, import second. Read MCP schemas before calling. Never read/edit dist/ or node_modules.

**Kill** — Invoke `process-kill` skill BEFORE every `kill`/`pkill`/signal call. NEVER kill without 100% ownership proof (PID captured at spawn THIS session). No `pkill -f`, no `killall`, no pattern matches, no `ps` inference. Correlation NOT proof. Lose PID or any doubt → ASK, never kill. Skill = Iron Rule + Proof Block checklist.

**Environment** — Always cd first. Relative paths only. HMR → changes immediate. File not found = wrong path. Docker containers: just start them. Long-running commands: background only.

**Monitor / Polling** — Invoke `monitor-polling` skill BEFORE every `Monitor` call or `until <cond>; sleep N` poll loop. Floor 60s for backend jobs (artisan, queue, LLM, agent dispatch). 15s/30s forbidden. "Tell me once when X done" = `Bash run_in_background` with `until`-loop, NOT `Monitor`. Skill = decision tree + interval floor table + load-failure override.

**Action Items** — Create Trello cards in Action Items immediately when mistakes or issues found. /docs + /explain always produce change. Rules, not memory, for behavioral corrections.

---

## Invoke `/wow` Before Every Implementation Phase

`/wow` skill reloads critical rules into recency position. Invoke before writing code every phase — `/next-phase` + orchestrator do this auto.