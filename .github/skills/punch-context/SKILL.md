---
name: punch-context
description: Project-wide context primer for any AI assistant working in Punch — architecture, runtime, lifecycle, and scope discipline in one place.
applies-to: project-wide primer; any agent, any phase; not path-scoped
---

# Skill: punch-context

## Responsibility

This skill is the **first read** for any agent that has not seen this
repository before. It loads the minimum mental model needed to avoid
asking the wrong question.

It owns:

- A pointer-list to the canonical docs (no duplication of their content).
- The current lifecycle (Spec → Plan → Build → Verify → Review → Ship, where
  Spec absorbs the former Define clarify step) and where each phase's prompt lives.
- The ownership boundaries and the "scope discipline" principle.

It does **not** own:

- The architecture itself (lives in `CLAUDE.md` and
  `docs/architecture/punch-boundaries.md`).
- Domain rules (those live in the per-domain skills below).
- Governance enforcement (lives in `punch-governance-review`).

## When to use

- An agent is invoked on this repo and has no prior context.
- A prompt explicitly says "load `punch-context` first".
- A reviewer wants to point a new contributor at one map.

## Inputs expected

None. This skill is a primer, not a tool.

## Procedure

1. Read [`CLAUDE.md`](../../../CLAUDE.md) — the constitution.
2. Read [`docs/architecture/punch-boundaries.md`](../../../docs/architecture/punch-boundaries.md)
   — the ownership map.
3. Read [`docs/ai/operating-model.md`](../../../docs/ai/operating-model.md)
   — the lifecycle and asset taxonomy.
4. Read [`docs/ai/workflow.md`](../../../docs/ai/workflow.md) — the
   walkthrough with a worked example.
5. Identify which layer the current task touches; that picks the matching
   domain skill (orchestration, compose, k6 performance, data harvest) and
   the matching Build prompt.
6. Honor scope discipline: read broadly, edit narrowly, return to Plan on
   scope expansion.

## Output

A short mental summary the agent can keep front-of-context:

- The 7 phases and which one this task is in.
- Which architectural layer this task owns.
- Which domain skill is authoritative for this work.
- Which Build prompt to invoke (if currently in Build).
- The artifact the task must produce to advance phases.

## Safety / boundary rules

- This skill never edits files.
- It never restates content from the docs it points to — drift is the
  enemy.
- If a pointed-at file disappears, the skill fails loudly (the maintenance
  matrix update was missed).

## References

- `CLAUDE.md`
- `docs/architecture/punch-boundaries.md`
- `docs/ai/operating-model.md`
- `docs/ai/workflow.md`
- `docs/ai/scoped-build-policy.md`
- The five domain skills below this one in the registry.
