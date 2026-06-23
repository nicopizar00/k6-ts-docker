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

- [`incremental-implementation`](../skills/incremental-implementation/SKILL.md) — one verifiable slice at a time.
- [`test-driven-development`](../skills/test-driven-development/SKILL.md) — RED → GREEN → REFACTOR for behavior changes.

When the task needs it:

- [`planning-and-task-breakdown`](../skills/planning-and-task-breakdown/SKILL.md) — only on `/build auto` with no task list, to derive ordered tasks.
- [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md) — when repo / cross-file context is needed before editing.
- [`punch-debugging-and-error-recovery`](../skills/punch-debugging-and-error-recovery/SKILL.md) — when a test or build fails.
- [`doubt-driven-development`](../skills/doubt-driven-development/SKILL.md) — high-risk or ambiguous decisions.

cavecrew (vendor) is the **execution/delegation optimization** layer, not a
replacement for these skills.

## Modes

- `/build` — implement the next pending task, verify it, then **stop**.
- `/build auto` — after explicit human approval, implement all pending tasks in
  dependency order; uses `planning-and-task-breakdown` if no task list exists.

## Rules

- No free agent or skill selection. `punch-builder` is the only Build entry point.
- `punch-builder` never builds itself. It delegates the complete build to one
  registered engineer agent:
  [`punch-runtime-engineer`](../agents/punch-runtime-engineer.agent.md) or
  [`punch-performance-test-engineer`](../agents/punch-performance-test-engineer.agent.md).
- The change must be minimal, verifiable, and aligned with Punch architecture.
- Any edit outside the task's allowed paths → **stop**, return to Plan.

## Delegation (bounded workers only)

`punch-builder` is the command-owned coordinator for this `/build` phase — not a
lifecycle router. It delegates the complete build to one engineer, and may hand
**bounded, independently verifiable** packets to vendor cavecrew leaf workers:

- [`cavecrew-investigator`](../agents/cavecrew-investigator.agent.md) — read-only
  locate / call-site map. Not for architecture recommendations.
- [`cavecrew-builder`](../agents/cavecrew-builder.agent.md) — known-location 1-2
  file edit. Not for 3+ files or cross-cutting refactors.
- [`cavecrew-reviewer`](../agents/cavecrew-reviewer.agent.md) — compact in-build
  diff review. **Not** the `/review` gate.

Do **not** delegate: product direction, architecture, the `/test` verdict, the
`/review` verdict, `/ship` readiness, or destructive/irreversible operations.
Workers are one level deep — they do not spawn further sub-agents. Builder may run
tests during build but never replaces the final `/test` or `/ship` verdict. cavecrew's
terse style must not strip required verification evidence.

## Comms

Builder speaks caveman **`full`** to humans; it briefs the engineer in
**`wenyan-lite`**. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## Validation gate

Change is done only when `reports/state/punch-run.json` records `passed: true`
(`./bin/punch run <test>`). No success claim without runtime evidence.

## Required final report

- **Result** — DONE | BLOCKED, + task ID/title
- **Agent used** — engineer + any cavecrew worker → packet → result
- **Agent Skills used** — which skills the build invoked
- **Files changed** — and why
- **Evidence run** — each command → pass/fail + output, or omitted with the
  reason; build/typecheck/lint + `./bin/punch run <test>`
- **Commits** — hash/message if created
- **Remaining risks**
- **Handoff** — ready for `/test`? ready for `/review`? blockers/follow-ups; +
  next recommended Punch prompt
