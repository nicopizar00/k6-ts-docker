---
agent: punch-builder
description: Build — execute ONE approved Plan task. Invokes punch-builder, which delegates to a registered engineer within scope.
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
- [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md) — only at the start of a
  new session, a task switch, or when the task needs cross-file/repository reasoning; not re-loaded
  mid-task once oriented.
- [`punch-planning-and-task-breakdown`](../skills/punch-planning-and-task-breakdown/SKILL.md) — only on `/build auto` with no task list, to derive ordered tasks.
- [`punch-debugging-and-error-recovery`](../skills/punch-debugging-and-error-recovery/SKILL.md) — only after a test or build actually fails.
- [`punch-doubt-driven-development`](../skills/punch-doubt-driven-development/SKILL.md) — only for a high-risk or ambiguous decision.

## Modes

- `/build` — implement the next pending task, verify it, then **stop**.
- `/build auto` — after explicit human approval, implement all pending tasks in
  dependency order; uses `punch-planning-and-task-breakdown` if no task list exists.

## Rules

- No free agent or skill selection. `punch-builder` is the only Build entry point.
- `punch-builder` never builds itself. It delegates the complete build to one
  registered engineer agent:
  [`punch-runtime-engineer`](../agents/punch-runtime-engineer.agent.md) or
  [`punch-performance-test-engineer`](../agents/punch-performance-test-engineer.agent.md).
- The change must be minimal, verifiable, and aligned with Punch architecture.
- Any edit outside the task's allowed paths → **stop**, return to Plan.

## Delegation

`punch-builder` is the command-owned coordinator for this `/build` phase — not a
lifecycle router. It delegates the complete build to exactly one engineer agent.

Do **not** delegate: product direction, architecture, the `/test` verdict, the
`/review` verdict, `/ship` readiness, or destructive/irreversible operations.
Builder may run tests during build but never replaces the final `/test` or
`/ship` verdict.

## Validation gate

Change is done only when `reports/state/punch-run.json` records `passed: true`
(`./bin/punch run <test>`). No success claim without runtime evidence.

## Required final report

- **Result** — DONE | BLOCKED, + task ID/title
- **Agent used** — the engineer that executed the build
- **Agent Skills used** — which skills the build invoked
- **Files changed** — and why
- **Evidence run** — each command → pass/fail + output, or omitted with the
  reason; build/typecheck/lint + `./bin/punch run <test>`
- **Commits** — hash/message if created
- **Remaining risks**
- **Handoff** — ready for `/test`? ready for `/review`? blockers/follow-ups; +
  next recommended Punch prompt
