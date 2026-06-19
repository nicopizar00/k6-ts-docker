---
agent: punch-planner
description: Phase 3 — Plan. Convert a Spec into scoped tasks with explicit allowed/read-only/forbidden paths.
---
# Punch — Plan

**Lifecycle phase:** Plan
**Mode:** Plan discipline — output is plan, no product edits (enforced by agent definition)
**Owner skill:** [`planning-and-task-breakdown`](../skills/planning-and-task-breakdown/SKILL.md) (method)
+ [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md) + matching domain skill(s);
on `.github/` changes, [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
**Agent:** [`punch-planner`](../agents/punch-planner.agent.md)
**Operating comms:** Caveman **`full`** (per-phase canon). Plan docs persistent — no Wenyan; task contracts/paths/validation commands verbatim. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Have approved Spec, need partition into tasks Build executes one at a time. Plan = contract Build bound to — every Build prompt refuses edit files outside task's allowed paths.

## Inputs

- Approved Spec.
- Constraint set: relevant files in `CLAUDE.md`, applicable path instructions, execution chain, maintenance matrix ([`docs/ai/maintenance-matrix.md`](../../docs/ai/maintenance-matrix.md)).

## What to do

1. Decompose Spec into smallest task set that together meet acceptance criteria.
2. Tag each task by Build domain: orchestrator (O), compose (C), k6-http (K), k6-browser (B), data-harvest (D).
3. Per task, fill **task contract**:

   - **Task ID** (e.g. `O-01`, `C-01`, `K-01`).
   - **Goal** — one sentence.
   - **Allowed edit paths** — globs.
   - **Read-only context paths** — globs.
   - **Forbidden paths** — globs (must include every layer task does not own).
   - **Expected diff size** — rough line count.
   - **Validation commands** — official Punch commands Verify runs.
   - **Rollback notes** — how to undo if Verify fails.
   - **Human checkpoint** — "human approval required before Build".
   - **Build prompt** — which of 5 build-* prompts handles it.

4. Task crosses layers naturally → flag as **integration task**, split into per-layer sub-tasks with fixed execution order.
5. List risks and rollback path for whole change.
6. Reference any cascade required by maintenance matrix (e.g. CI workflow update if service name changes).

## Expected output

Plan document (in chat, or written to `docs/` if requested) with every task contract plus top-level summary:

- **Goal** (from Spec).
- **Tasks** — full per-task contract.
- **Order of execution** — typically k6 → compose → orchestrator for integration changes.
- **Cross-cutting risks** — single section for risks spanning tasks.
- **Rollback plan** — for whole change.

## Validation gate

Plan approved when human confirms. Build prompts refuse to run without approved Plan task ID.

## Edits permitted

Only plan doc itself, when user explicitly asks to persist. This prompt produces prose by default.
