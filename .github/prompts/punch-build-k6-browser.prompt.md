---
mode: agent
description: Phase 4 — Build (k6 Browser). Implement ONE approved k6 Browser task within scope. CURRENTLY DEFERRED.
---

# Punch — Build (k6 Browser)

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the Plan)
**Owner skill:** [`punch-k6-performance`](../skills/punch-k6-performance/SKILL.md)
**Agent:** [`punch-builder-scoped`](../agents/punch-builder-scoped.agent.md)

> **Status: deferred.** The reference k6 image does not ship Chromium and
> the project has not approved the image-size / build-time / CI-cost
> trade. Any task using this prompt must first be authorized by a Plan
> that explicitly accepts the trade and includes a paired
> `punch-build-compose` task to introduce the Browser image.

## Pre-conditions

- An approved Plan task with **Build prompt: `punch-build-k6-browser`**.
- A named task ID (e.g. `B-01`).
- A human has confirmed the Plan **and** the cost trade.

If any of these is missing, **stop** and return to Plan.

## Typical scope

```
Allowed:
  src/tests/browser-*.ts
  src/tests/browser-*.ts.example
  docker/k6-browser.Dockerfile    (only when explicitly planned as part
                                   of enabling Browser execution)

Read-only:
  docker-compose.yml
  src/services/**
  docker/k6.Dockerfile

Forbidden:
  src/punch/**                    (orchestrator is a different domain)
  src/tests/*.ts                  (non-browser tests are a different prompt)
  docker/k6.Dockerfile            (HTTP k6 image — separate from Browser)
  docker-compose.yml              (compose changes are a different domain)
```

The Plan may **narrow** these lists. The Plan may not widen them beyond
the Forbidden set without re-planning.

## When to use

You have an approved Plan task for a k6 Browser test. Today this almost
always means *enabling* Browser execution for the first time — which
also requires a paired `punch-build-compose` task.

## Inputs

- The approved Plan task.
- The task ID.

## What to do

1. Re-state the task's allowed / read-only / forbidden paths.
2. Read `src/tests/browser-smoke.ts.example` for the intended shape.
3. Implement the change in the allowed paths.
4. Browser thresholds replace HTTP thresholds (`browser_web_vital_lcp`,
   `browser_web_vital_cls`, `browser_web_vital_fid`, `checks`).
5. Reuse the `handleSummary` evidence contract — Browser tests write
   their HTML/JSON to `/reports/` exactly like HTTP tests.
6. If the task implies a Dockerfile change but no paired
   `punch-build-compose` task exists, **stop** and return to Plan.

## Expected output

A focused diff under `src/tests/browser-*` and possibly
`docker/k6-browser.Dockerfile`. Plus:

- The task ID.
- Every file changed.
- The Browser thresholds declared.
- Confirmation that the paired compose task (if any) is also planned.
- One sentence on the next step.

## Validation gate

Verify (a Browser-specific Punch command, defined by the Plan that
enabled Browser; today no such command exists by default).

## Scope expansion rule

Same as orchestrator. Stop on out-of-scope edits; return to Plan.
