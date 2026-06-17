---
agent: punch-builder-compose
description: Phase 4 — Build (compose). Implement ONE approved Docker/Docker Compose task within scope.
---

# Punch — Build (Compose)

**Lifecycle phase:** Build
**Mode:** Agent (edits permitted, scoped to the Plan)
**Owner skill:** [`incremental-implementation`](../skills/incremental-implementation/SKILL.md) (the method) + [`punch-docker-compose`](../skills/punch-docker-compose/SKILL.md)
**Agent:** [`punch-builder-compose`](../agents/punch-builder-compose.agent.md)

## Pre-conditions

- An approved Plan task with **Build prompt: `punch-build-compose`**.
- A named task ID (e.g. `C-01`).
- A human has confirmed the Plan.

If any of these is missing, **stop** and return to Plan.

## Typical scope

```
Allowed:
  docker-compose.yml
  docker/**
  .env.example                    (if/when added)
  docs/docker/**                  (if/when a docker-docs subtree is added)

Read-only:
  src/punch/**
  src/tests/**
  src/services/**

Forbidden:
  src/punch/**                    (orchestrator is a different domain)
  src/tests/**                    (k6 is a different domain)
  src/services/**                 (service code is a different domain)
  .github/workflows/**            (CI is external to Punch)
```

The Plan may **narrow** these lists. The Plan may not widen them beyond
the Forbidden set without re-planning.

## When to use

You have an approved Plan task for Docker Compose or a Dockerfile and
want to execute it. One task per invocation.

## Inputs

- The approved Plan task.
- The task ID being executed.

## What to do

1. Re-state the task's allowed / read-only / forbidden paths.
2. Read [`compose-contract.md`](../skills/punch-docker-compose/compose-contract.md)
   and confirm the change either adds a service following the contract
   or modifies a service within its contract.
3. If the change renames a service or changes a port:
   - Grep for the old name/port across `src/tests/**`, `src/punch/**`,
     and docs.
   - The Plan must already cover the dependents; if it does not, **stop**
     and return to Plan.
4. Edit only files in the allowed list.
5. Preserve healthchecks; preserve the no-CMD rule for the k6 image;
   pin image tags.
6. If a change requires editing something outside scope, **stop** and
   return to Plan.

## Expected output

A focused diff under `docker-compose.yml` and/or `docker/`. Plus:

- The task ID.
- Every file changed.
- New/changed/removed services with their contract fields.
- Confirmation that no out-of-scope file was edited.
- One sentence on the next step.

## Validation gate

Verify (`./bin/punch doctor`, then the smoke + relevant tests). Do not
claim success here.

## Scope expansion rule

Same as orchestrator. Stop on out-of-scope edits; return to Plan.
