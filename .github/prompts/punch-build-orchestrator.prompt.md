---
mode: agent
description: Phase 4 — Build (orchestrator). Implement ONE approved Python orchestration task within scope.
---

# Punch — Build (Orchestrator)

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the Plan)
**Owner skill:** [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md)
**Agent:** [`punch-builder-scoped`](../agents/punch-builder-scoped.agent.md)

## Pre-conditions

- An approved Plan task with **Build prompt: `punch-build-orchestrator`**.
- A named task ID (e.g. `O-01`).
- A human has confirmed the Plan.

If any of these is missing, **stop** and return to Plan.

## Typical scope

```
Allowed:
  src/punch/**/*.py
  bin/punch                       (only if the wrapper contract changes)
  tests/**/orchestrator/**        (if/when a test directory is added)

Read-only:
  docker-compose.yml
  docker/**
  src/tests/**

Forbidden:
  src/services/**
  src/tests/**                   (test code is k6's domain — replan if it must change)
  docker-compose.yml             (no compose edits in an orchestrator task)
  docker/**                      (no image edits in an orchestrator task)
  .github/workflows/**           (CI is external to Punch)
```

The Plan may **narrow** these lists. The Plan may not widen them beyond
the Forbidden set without re-planning.

## When to use

You have an approved Plan task for the Python orchestrator and want to
execute it. One task per invocation — do not bundle tasks.

## Inputs

- The approved Plan task (link or paste).
- The task ID being executed.

## What to do

1. Re-state the task's allowed / read-only / forbidden paths at the
   start of the work.
2. Read the relevant files in `src/punch/` to ground in the current
   control flow.
3. Confirm the change stays stdlib-only.
4. Edit **only** files in the task's allowed list.
5. Match the existing streaming-subprocess pattern (see
   [`examples/streaming-subprocess.md`](../skills/punch-python-orchestration/examples/streaming-subprocess.md)).
6. Preserve exit-code propagation and the
   `reports/state/punch-run.json` evidence contract.
7. If the change requires editing something outside scope, **stop**.
   Report the new fact and return to Plan.

## Expected output

A focused diff in `src/punch/**` (and `bin/punch` if explicitly
allowed). Plus:

- The task ID.
- Every file changed.
- Confirmation that no out-of-scope file was edited.
- One sentence on the next step (Verify, or "blocked — return to Plan").

## Validation gate

Verify is the next phase. Do not claim success here; Build only produces
candidate changes.

## Scope expansion rule

If, mid-Build, you discover the task cannot be completed within the
allowed paths, **stop**. Do not edit a forbidden file as a "small fix".
Capture the new fact, return to Plan, get a revised task, then resume.
