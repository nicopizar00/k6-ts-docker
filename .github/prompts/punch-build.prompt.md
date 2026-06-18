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

## Optional: concise Build comms (Caveman, Build-only)

Build — and only Build — may use the
[`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md) adapter to make
**assistant prose** concise (implementation updates, sub-agent handoffs,
post-evidence debug summaries, commit drafts). It is **opt-in and off by
default**; the other lifecycle phases keep normal prose.

- Apply it **only after** the Build task is understood — never as a substitute
  for reasoning.
- Default mode **`lite`** (`/caveman lite`). Use `/caveman full` or
  `/caveman ultra` only when the user explicitly asks **and** the task is low
  risk.
- **Never** compress code, commands, paths, Python orchestration details, Docker
  Compose output, k6 output, JSON/YAML/CSV, logs, stack traces, errors, exit
  codes, test evidence (`reports/state/punch-run.json`), acceptance criteria, or
  risk notes — quote those verbatim. Caveman compresses prose **around** the
  evidence, not the evidence.
- **Priority:** Correctness > evidence > maintainability > brevity. If brevity
  harms clarity, uncertainty, or risk explanation, **stop Caveman and answer
  normally**.

Scope, modes, and stop conditions: the adapter SKILL.md and
[ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md).
