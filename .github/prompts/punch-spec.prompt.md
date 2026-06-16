---
mode: ask
description: Phase 2 — Spec. Convert a Define note into goals, non-goals, constraints, and acceptance criteria.
---

# Punch — Spec

**Lifecycle phase:** Spec
**Mode:** Ask (read-only — output is a spec doc, not edits)
**Owner skill:** [`punch-context`](../skills/punch-context/SKILL.md) +
the matching domain skill (orchestration / compose / k6 / data-harvest)
**Agent:** [`punch-architect-readonly`](../agents/punch-architect-readonly.agent.md)

## When to use

You have a clear Define note and need to crystallize it into a spec
before Plan begins partitioning work. Spec is the contract that Plan
will be evaluated against.

## Inputs

- The Define note (link or paste).
- (Optional) the issue, ticket, or PR description that prompted the
  request.

## What to do

1. Re-state the goal in one sentence — concrete, testable.
2. Enumerate non-goals — what this work explicitly will not do.
3. Capture functional requirements — observable behavior the change
   delivers.
4. Capture technical constraints — what the implementation may not do
   (no host deps, stdlib only, no Compose service renames, etc.).
5. Identify affected architectural layers (refer to
   [`punch-boundaries.md`](../../docs/architecture/punch-boundaries.md)).
6. Call out artifact / log / reporting implications. Will any artifact
   path or schema change? Will terminal noise change? Update the
   reporting contract if so.
7. Define acceptance criteria — the conditions Verify will check.

## Expected output

A spec doc (in chat, or written to `docs/` if the user requests
persistence). It contains:

- **Goal** — one sentence.
- **Non-goals** — bullet list.
- **Functional requirements** — what the change delivers.
- **Technical constraints** — what implementation must respect.
- **Affected layers** — which boundary(ies) own this.
- **Artifact / log / reporting implications** — explicit, even if "none".
- **Acceptance criteria** — what Verify will assert.

## Validation gate

Spec is approved when the goal, non-goals, and acceptance criteria are
agreed. Plan is the next phase.

## Edits permitted

Only the spec doc itself, when the user explicitly asks to persist it
(e.g. under `docs/architecture/specs/<topic>.md`). Otherwise this prompt
produces prose only.
