---
agent: punch-architect-readonly
description: Spec — clarify and refine the request, then convert it into goals, non-goals, constraints, and acceptance criteria. Absorbs the former Define step.
---

# Punch — Spec

**Lifecycle phase:** Spec (the entry phase — it absorbs the former Define clarify step)
**Mode:** Code read-only; may write the spec doc when persisted (per agent definition)
**Owner skill:** [`spec-driven-development`](../skills/spec-driven-development/SKILL.md) (the method)
+ [`punch-context`](../skills/punch-context/SKILL.md)
+ [`idea-refine`](../skills/idea-refine/SKILL.md) (clarify step, when the idea is vague)
+ the matching domain skill (orchestration / compose / k6 / data-harvest)
**Agent:** [`punch-architect-readonly`](../agents/punch-architect-readonly.agent.md)

## When to use

You have a request, issue, or symptom and need to turn it into a spec
before Plan begins partitioning work. Spec is the entry phase: it first
clarifies/refines the request (the former Define work), then crystallizes
it into the contract Plan will be evaluated against.

## Inputs

- The request, issue, or symptom (one paragraph).
- (Optional) a failing log, artifact path, branch name, or PR URL.

## What to do

**Clarify first (the former Define step).** Trace the execution chain
(source → bundle → image → run → reports) for the request. If the idea is
still vague, run the [`idea-refine`](../skills/idea-refine/SKILL.md) skill to
sharpen it into a clean problem statement. Then specify:

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
