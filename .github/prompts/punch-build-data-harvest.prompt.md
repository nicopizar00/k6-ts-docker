---
agent: agent
description: Phase 4 — Build (data harvest / reporting). Implement ONE approved artifact, log, or reporting task within scope.
---

# Punch — Build (Data Harvest)

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the Plan)
**Owner skill:** [`punch-data-harvest`](../skills/punch-data-harvest/SKILL.md)
**Agent:** [`punch-builder-scoped`](../agents/punch-builder-scoped.agent.md)

## Pre-conditions

- An approved Plan task with **Build prompt: `punch-build-data-harvest`**.
- A named task ID (e.g. `D-01`).
- A human has confirmed the Plan.
- The Plan filled in an **artifact contract entry** for every new or
  changed artifact (see
  [`artifact-contract.md`](../skills/punch-data-harvest/artifact-contract.md)).

If any of these is missing, **stop** and return to Plan.

## Typical scope

```
Allowed:
  src/tests/support/**            (HTML/JSON report builder)
  src/punch/**                    (ONLY the reporting/state-writing parts;
                                   the Plan must name the functions)
  docs/validation/**              (artifact documentation)
  docs/ai/maintenance-matrix.md   (when a path or schema moves)

Read-only:
  src/tests/*.ts
  docker-compose.yml
  src/services/**

Forbidden:
  docker/**
  src/services/**
  .github/workflows/**            (CI changes are out of scope)
```

The Plan may **narrow** these lists. The Plan may not widen them beyond
the Forbidden set without re-planning.

## When to use

You have an approved Plan task for an artifact, log, or report — adding
one, changing its schema, moving its path, or changing the
terminal-vs-file noise split. One task per invocation.

## Inputs

- The approved Plan task.
- The task ID.
- The artifact contract entry/entries (see precondition).

## What to do

1. Re-state the task's allowed / read-only / forbidden paths.
2. Re-read the artifact contract entries for every artifact affected.
3. Implement the producer-side change in the allowed paths.
4. Preserve the principle of **low-noise terminal output / complete file
   logs**. New verbose output goes to a file, not stdout, unless the
   Plan explicitly authorizes terminal exposure.
5. Preserve **stable artifact paths**. A rename or schema change is a
   contract change — the Plan must already cover the cascade.
6. Update `docs/ai/maintenance-matrix.md` in the same diff if a path or
   schema is moving.
7. If a change requires editing something outside scope, **stop** and
   return to Plan.

## Expected output

A focused diff under `src/tests/support/` and/or `src/punch/`. Plus:

- The task ID.
- Every file changed.
- The artifact contract entries added or modified.
- Confirmation that downstream consumers (CI validation job, this
  skill, the matrix) still resolve.
- One sentence on the next step.

## Validation gate

Verify (`./bin/punch run smoke` or the relevant test). Confirm the
new/changed artifact appears under `reports/` with the expected path
and schema.

## Scope expansion rule

Same as orchestrator. Stop on out-of-scope edits; return to Plan.
