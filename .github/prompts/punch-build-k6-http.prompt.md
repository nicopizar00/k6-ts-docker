---
agent: agent
description: Phase 4 — Build (k6 HTTP). Implement ONE approved k6 HTTP performance test task within scope.
---

# Punch — Build (k6 HTTP)

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the Plan)
**Owner skill:** [`punch-k6-performance`](../skills/punch-k6-performance/SKILL.md)
**Agent:** [`punch-builder-scoped`](../agents/punch-builder-scoped.agent.md)

## Pre-conditions

- An approved Plan task with **Build prompt: `punch-build-k6-http`**.
- A named task ID (e.g. `K-01`).
- A human has confirmed the Plan.

If any of these is missing, **stop** and return to Plan.

## Typical scope

```
Allowed:
  src/tests/*.ts                  (HTTP tests only — NOT browser-*)
  src/tests/support/**            (only if the shared helper genuinely changes,
                                   and the Plan said so)

Read-only:
  docker-compose.yml
  src/services/**
  docker/k6.Dockerfile

Forbidden:
  src/punch/**                    (orchestrator is a different domain)
  docker/**                       (image changes are a different domain — replan)
  src/tests/browser-*.ts*         (Browser is a different prompt)
  docker-compose.yml              (compose changes are a different domain)
```

The Plan may **narrow** these lists. The Plan may not widen them beyond
the Forbidden set without re-planning.

## When to use

You have an approved Plan task for a k6 HTTP test (smoke, gate, or
journey) and want to execute it. One task per invocation.

## Inputs

- The approved Plan task.
- The task ID.

## What to do

1. Re-state the task's allowed / read-only / forbidden paths.
2. Read the existing `src/tests/*.ts` to match conventions.
3. Read [`thresholds.md`](../skills/punch-k6-performance/thresholds.md)
   and confirm the test category (smoke / gate / journey) and its
   threshold profile.
4. Implement the change in the allowed paths.
5. Keep thresholds at the top of the file. Configurable
   `__ENV.TARGET_BASE_URL` with an in-network default.
6. Use `SharedArray` for fixtures. Deterministic IDs (`prod-001`, …).
7. Export `handleSummary` writing `/reports/<test>.html` (via
   `support/report.ts`) and `/reports/<test>.json`.
8. If the change requires editing something outside scope (e.g. a new
   compose service for a new test), **stop** and return to Plan.

## Expected output

A focused diff under `src/tests/`. Plus:

- The task ID.
- Every file changed.
- The thresholds declared in the new/changed test.
- Confirmation that `handleSummary` writes the contracted artifacts.
- One sentence on the next step.

## Validation gate

Verify (`./bin/punch run <test>`). Do not claim success here.

## Scope expansion rule

Same as orchestrator. Stop on out-of-scope edits; return to Plan.
