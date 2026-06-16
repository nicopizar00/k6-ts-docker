---
mode: ask
description: Phase 1 — Define. Read broadly to translate a request into a clean problem statement.
---

# Punch — Define

**Lifecycle phase:** Define
**Mode:** Ask (read-only — no edits permitted)
**Owner skill:** [`punch-context`](../skills/punch-context/SKILL.md) +
the relevant domain skill picked at the end
**Agent:** [`punch-architect-readonly`](../agents/punch-architect-readonly.agent.md)

## When to use

You have a request, issue, or symptom and you need a clean problem
statement before anyone writes a spec. Examples:

- "Smoke runs but gate sometimes fails on CI — why?"
- "We want a `--quiet` flag for `./bin/punch run`. What would that touch?"
- "The HTML report shows the wrong p95 — where does it come from?"

## Inputs

- The request, issue, or symptom (one paragraph max).
- (Optional) a failing log, artifact path, branch name, or PR URL.

## What to do

1. Load [`punch-context`](../skills/punch-context/SKILL.md) — read
   `CLAUDE.md`, `docs/architecture/punch-boundaries.md`, and
   `docs/ai/operating-model.md`.
2. Trace the execution chain (source → bundle → image → run → reports)
   as it relates to the request.
3. Identify which architectural layer the change touches. If more than
   one, call out the integration explicitly.
4. Surface assumptions, hidden coupling, and any rule in `CLAUDE.md` or
   `.github/instructions/` that constrains the area.
5. Identify the smallest unknown that would unblock Spec.

## Expected output

A Define note containing:

- **Problem summary** — one paragraph naming the actual problem (not the
  request).
- **Relevant repository areas** — file paths.
- **Current behavior** — what the code does today, with file:line refs.
- **Desired behavior** — what the change wants, in one sentence.
- **Architectural boundaries involved** — which layer(s) own this.
- **Risks** — what could go wrong if implemented carelessly.
- **Open questions** — the smallest set Spec must answer.
- **Suggested next step** — usually `punch-spec`.

## Validation gate

None — no edits to verify. Spec is the next phase.
