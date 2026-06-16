---
mode: ask
description: Phase 3 — Plan. Convert a Spec into scoped tasks with explicit allowed/read-only/forbidden paths.
---

# Punch — Plan

**Lifecycle phase:** Plan
**Mode:** Ask (Plan discipline — output is a plan, not edits)
**Owner skill:** [`punch-context`](../skills/punch-context/SKILL.md) +
the matching domain skill(s); on `.github/` changes,
[`punch-governance-review`](../skills/punch-governance-review/SKILL.md)
**Agent:** [`punch-planner`](../agents/punch-planner.agent.md)

## When to use

You have an approved Spec and need to partition it into tasks that Build
can execute one at a time. The Plan is the contract that Build is
literally bound to — every Build prompt refuses to edit files outside
its task's allowed paths.

## Inputs

- The approved Spec.
- The constraint set: relevant files in `CLAUDE.md`, applicable path
  instructions, the execution chain, and the maintenance matrix
  ([`docs/ai/maintenance-matrix.md`](../../docs/ai/maintenance-matrix.md)).

## What to do

1. Decompose the Spec into the smallest set of tasks that, together,
   meet the acceptance criteria.
2. Tag each task by Build domain: orchestrator (O), compose (C),
   k6-http (K), k6-browser (B), data-harvest (D).
3. For each task, fill in the **task contract**:

   - **Task ID** (e.g. `O-01`, `C-01`, `K-01`).
   - **Goal** — one sentence.
   - **Allowed edit paths** — globs.
   - **Read-only context paths** — globs.
   - **Forbidden paths** — globs (must include every layer the task
     does not own).
   - **Expected diff size** — rough line count.
   - **Validation commands** — the official Punch commands Verify will
     run.
   - **Rollback notes** — how to undo if Verify fails.
   - **Human checkpoint** — "human approval required before Build".
   - **Build prompt** — which of the 5 build-* prompts handles it.

4. If a task naturally crosses layers, flag it as an **integration
   task** and split it into per-layer sub-tasks with a fixed execution
   order.
5. List risks and a rollback path for the whole change.
6. Reference any cascade required by the maintenance matrix (e.g. CI
   workflow update if a service name changes).

## Expected output

A plan document (in chat, or written to `docs/` if requested) containing
every task contract plus a top-level summary:

- **Goal** (from Spec).
- **Tasks** — full per-task contract.
- **Order of execution** — typically k6 → compose → orchestrator for
  integration changes.
- **Cross-cutting risks** — single section for risks that span tasks.
- **Rollback plan** — for the whole change.

## Validation gate

Plan is approved when a human confirms it. Build prompts refuse to run
without an approved Plan task ID.

## Edits permitted

Only the plan doc itself, when the user explicitly asks to persist it.
This prompt produces prose by default.
