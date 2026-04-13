# Claude Global Rules

**Read-only by default.** Do not modify anything without explicit approval ("go ahead," "do it," "fix it," or a direct imperative). Questions, observations, and "sounds good" are NOT approval. After presenting options, enter a hard stop — text only until an action verb.

**QUESTIONS = FULL STOP.** If the user's message contains a question mark, you are in DIAGNOSTIC MODE. Stop ALL work, ALL pipelines, ALL flows. Answer the question with text only. Do not run commands, edit files, kill processes, or take any action. Do not resume work until the user gives an explicit action verb. No exceptions. No "but I'm mid-pipeline." No "the fix is obvious." STOP. ANSWER. WAIT.

**Verify, never guess.** Read the source before using any prop, component, API, or value. Read existing code before writing new code. A wrong guess always costs more than reading a file.

**No backwards compatibility. No legacy code. No silent fallbacks.** ONE correct pattern for everything. Throw errors by default — fallbacks hide bugs permanently. Broken code that fails loudly is better than "working" code with two paths.

**TDD for EVERY change — no exceptions, no category exemptions.** Failing test first, then fix/implement, then verify. Infrastructure, config, cross-process behavior, agent dispatch restrictions — ALL require a test. "This can't be unit tested" means you don't understand the problem yet. Never claim something works without test evidence.

**Own the entire codebase.** "Pre-existing" and "out of scope" are not valid reasons to skip work.

---

## Rule Index

Every rule below has full context in the referenced rules file. These are loaded automatically.

**Collaboration** — Read-only default. **Questions = FULL STOP (diagnostic mode, no actions).** Hard stop after presenting options. Concept approval != implementation approval. Never cancel running processes. Correcting a mistake ≠ destroying work in progress. Never substitute your "better" approach. Visual companion for UI brainstorming.

**Code Quality** — SOLID/DRY/Zero-Debt. Refactor before building. Extract shared abstractions first. Instance state over parameter threading. Props/emits are last resort. Scalar values on parent model. Production jobs must be incremental. Never edit danx-ui without permission.

**Debugging** — Diagnose != Fix. TDD for every change (not just bugs). Never deflect as "pre-existing." Never silence errors — investigate why they fire. When unsure, STOP and explain. Assumptions are not evidence. Never claim verified without test proof.

**Testing** — 100% coverage. Dump output to file. Never parallel, never background. Full suite rare (end-only). Good tests verify behavior, bad tests verify framework. Test protected methods. Never let subagents run tests.

**Planning** — Trello card overrides plan mode. Plans are prose (never code). Complete ALL planned work. Never check off incomplete work. Zero-context test for plans. Pipeline is automatic: implement -> /flow-code-review -> /flow-quality-check -> /flow-commit -> /flow-report (per phase) -> /flow-finish (session end).

**Git** — Never delete repos. Always use /flow-commit. Never stash, never reset other changes. Revert via Edit, never git checkout. Check for other agents' staged work before committing.

**Tools** — Use Read/Edit/Write/Glob/Grep, never bash equivalents. Lint runs via hooks automatically. Import order: usage first, import second. Read MCP schemas before calling. Never read/edit dist/ or node_modules.

**Environment** — Always cd first. Relative paths only. HMR means changes are immediate. File not found = wrong path. Docker containers: just start them. Long-running commands: background only.

**Self-Improvement** — Write notes to agent-notes.md immediately when mistakes happen. /docs and /explain always produce a change. Rules, not memory, for behavioral corrections.

---

## Invoke `/wow` Before Every Implementation Phase

The `/wow` skill reloads critical rules into recency position. Invoke it before writing code in every phase — `/next-phase` and the orchestrator do this automatically.
