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

Always:

- [`punch-incremental-implementation`](../skills/punch-incremental-implementation/SKILL.md) — one verifiable slice at a time.
- [`punch-test-driven-development`](../skills/punch-test-driven-development/SKILL.md) — RED → GREEN → REFACTOR for behavior changes.
- [`punch-source-driven-development`](../skills/punch-source-driven-development/SKILL.md) — verify against actual source / runtime behavior, never assumptions.
- [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md) — load repo / cross-file context before editing.

When the task needs it:

- [`punch-planning-and-task-breakdown`](../skills/punch-planning-and-task-breakdown/SKILL.md) — only on `/build auto` with no task list, to derive ordered tasks.
- [`punch-debugging-and-error-recovery`](../skills/punch-debugging-and-error-recovery/SKILL.md) — when a test or build fails.
- [`punch-doubt-driven-development`](../skills/punch-doubt-driven-development/SKILL.md) — high-risk or ambiguous decisions.
- [`punch-using-agent-skills`](../skills/punch-using-agent-skills/SKILL.md) — the *agents* canon: how `punch-builder` delegates to engineers.
- [`graphify`](../skills/graphify/SKILL.md) — when a repo dependency map helps locate the change surface (native, explicit-only; never invoked automatically).

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
