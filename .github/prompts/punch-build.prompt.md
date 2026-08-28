---
agent: punch-builder
description: Build — execute ONE approved Plan task. Invokes punch-builder, which classifies the task by subsystem and implements it within scope.
---
# Punch — Build

**Lifecycle phase:** Build
**Agent:** [`punch-builder`](../agents/punch-builder.agent.md)

## Pre-conditions

- Approved Plan task (from `punch-plan`) with a named task ID.
- Human confirmed the Plan.

Missing either → **stop**, return to Plan.

## What this prompt does

1. Declares the **Build** phase.
2. Invokes [`punch-builder`](../agents/punch-builder.agent.md).
3. Hands it the approved Plan task: goal, allowed/read-only/forbidden paths, task ID.

## Agent Skills (workflow canon — drive the build)

Always (the one default Build method, no trigger needed):

- [`punch-incremental-implementation`](../skills/punch-incremental-implementation/SKILL.md) — one verifiable slice at a time.

Trigger-only — load only when the named condition is actually present, not by default:

- [`punch-test-driven-development`](../skills/punch-test-driven-development/SKILL.md) — only for a
  behavioral change or a bug-reproduction proof (RED → GREEN → REFACTOR); not for pure docs/config edits.
- [`punch-source-driven-development`](../skills/punch-source-driven-development/SKILL.md) — only for
  version-sensitive k6/Docker/Postgres API work; not every Build.
- [`punch-planning-and-task-breakdown`](../skills/punch-planning-and-task-breakdown/SKILL.md) — only on `/build auto` with no task list, to derive ordered tasks.
- [`punch-debugging-and-error-recovery`](../skills/punch-debugging-and-error-recovery/SKILL.md) — only after a test or build actually fails.
- [`punch-doubt-driven-development`](../skills/punch-doubt-driven-development/SKILL.md) — only for a high-risk or ambiguous decision.

## Modes

- `/build` — implement the next pending task, verify it, then **stop**.
- `/build auto` — after explicit human approval, implement all pending tasks in
  dependency order; uses `punch-planning-and-task-breakdown` if no task list exists.

## Rules

- No free agent or skill selection. `punch-builder` is the only Build entry point.
- `punch-builder` classifies the task into a subsystem (runtime or
  performance-test — see [`punch-builder.agent.md`](../agents/punch-builder.agent.md))
  and implements it directly within that subsystem's scope.
- The change must be minimal, verifiable, and aligned with Punch architecture.
- Any edit outside the task's allowed paths → **stop**, return to Plan.

## Scope

`punch-builder` does not delegate the build — it is the implementer for
whichever subsystem the task classifies into.

Out of scope regardless of subsystem: product direction, architecture, the
`/test` verdict, the `/review` verdict, `/ship` readiness, or
destructive/irreversible operations. Builder may run tests during build but
never replaces the final `/test` or `/ship` verdict.

## Validation gate

Change is done only when `reports/state/punch-run.json` records `passed: true`
(`./bin/punch run <test>`). No success claim without runtime evidence.

## Required final report

- **Result** — DONE | BLOCKED, + task ID/title
- **Subsystem** — runtime or performance-test
- **Agent Skills used** — which skills the build invoked
- **Files changed** — and why
- **Evidence run** — each command → pass/fail + output, or omitted with the
  reason; build/typecheck/lint + `./bin/punch run <test>`
- **Commits** — hash/message if created
- **Remaining risks**
- **Handoff** — ready for `/test`? ready for `/review`? blockers/follow-ups; +
  next recommended Punch prompt
