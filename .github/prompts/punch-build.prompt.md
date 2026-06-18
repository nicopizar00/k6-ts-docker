---
agent: punch-builder
description: Build — execute ONE approved Plan task. The punch-builder dispatcher classifies it and delegates to the runtime or performance-test engineer within scope.
---

# Punch — Build

**Lifecycle phase:** Build
**Mode:** Agent (scoped, via dispatch)
**Owner skill:** [`incremental-implementation`](../skills/incremental-implementation/SKILL.md) + [`test-driven-development`](../skills/test-driven-development/SKILL.md) + the task's domain skill
**Agent:** [`punch-builder`](../agents/punch-builder.agent.md) → delegates to one engineer

## Pre-conditions

- An approved Plan task (from `punch-plan`) with a named task ID.
- A human has confirmed the Plan.

If any is missing, **stop** and return to Plan.

## Inputs

- The approved Plan task: goal, allowed/read-only/forbidden paths, task ID.

## What to do

1. Classify the task into **one** domain and select the engineer + domain skill:
   - orchestrator / `bin/punch` / Compose / service images / data harvest →
     [`punch-runtime-engineer`](../agents/punch-runtime-engineer.agent.md)
     (`punch-python-orchestration` / `punch-compose-runtime` / `punch-data-harvest`).
   - k6 HTTP/Browser / thresholds / `package.json` / TS bundle / lint →
     [`punch-performance-test-engineer`](../agents/punch-performance-test-engineer.agent.md)
     (`punch-k6-testing`).
2. Hand the engineer the goal, scope, constraints, expected output, and required
   evidence (depth-1 — the engineer delegates to no one).
3. On return, consolidate the result, changed files, evidence, and next step.

## Expected output

Per the `punch-builder` evidence contract: **Result · Changed Files · Evidence ·
Unresolved Assumptions · Recommended Next Step**.

## Validation gate

Verify (`./bin/punch run <test>`) — do not claim success here. A change is done
when `reports/state/punch-run.json` records `passed: true`.

## Scope expansion rule

Any edit outside the task's allowed paths → **stop**, return to Plan.
