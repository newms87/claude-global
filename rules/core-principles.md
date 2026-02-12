# Core Engineering Principles

`SOLID / DRY / Zero-Debt / One-Way / Read-First / 100%-Tests / Flawless`

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

## Observation is not Instruction

When the user describes a behavior or limitation, DO NOT immediately start "fixing" it. Ask what they want to do about it. Present options. Wait for direction. Only act when explicitly asked.

**Never modify user-authored content without explicit request.** Demo code, documentation, example strings, and similar authored content reflects deliberate choices. Do not delete, reformat, or restructure it based on your own judgment.
