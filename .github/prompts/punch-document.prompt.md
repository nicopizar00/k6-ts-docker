---
agent: punch-ai-governance
description: Documentate — reconcile documentation debt in waves. Map docs + AI-config with /graphify, then keep / merge / rewrite / archive / delete / promote.
---

# Punch — Documentate

**Lifecycle phase:** Documentate (recurring maintenance; orthogonal to Spec → Ship)
**Mode:** Ask / Agent — reconciliation edits via `punch-ai-governance`
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(the decision authority) + [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(the Graphify gate) + [`documentation-and-adrs`](../skills/documentation-and-adrs/SKILL.md)
(the writing method). The structural map is delegated to the existing `/graphify` skill.
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (Documentation mode)

## When to use

Periodically, or after a feature lands and docs drifted, to retire documentation
debt — duplicated, stale, partial, or orphaned knowledge — across human docs
(`README.md`, `docs/`, ADRs) and AI-facing docs (`AGENTS.md`,
`.github/` instructions / prompts / skills / agents, `docs/ai/`, registries).
Run **one wave at a time**; defer the rest.

## Pre-conditions

- Host `graphify` installed (`uv tool install graphifyy`; scoped Rule-1
  exception — [ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)). If
  the CLI is absent, the `punch-context-engineering` gate shows the **Graphify
  Team Setup** message and the wave proceeds with non-graph evidence.
- The map runs **in the IDE session** — the active model does semantic extraction,
  **no API key**. The headless `graphify extract --backend` path is not used in-IDE.

## How it works (boundary)

**Graphify provides the map; `punch-ai-governance` makes every decision.** The
graph is *evidence* for reconciliation, never the canonical source. Nothing under
`graphify-out/` is promoted to canonical without a governance decision, and it is
never committed (it is gitignored — [ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)).

## Inputs

- **Wave scope** — one of: AI-config (`.github/` + `docs/ai/`) · human docs
  (`README.md`, `docs/`, `docs/architecture/`) · a single subsystem.
- An existing `graphify-out/` if present (else the Map step builds it).

## What to do

1. **Map & gather (via Context Engineering).** Follow `punch-context-engineering`'s
   Graphify gate to build, query, or update the graph for this wave's scope —
   reconciliation is a broad/governance task, so an `update` is usually warranted.
   Delegate to the existing `/graphify` skill (1-deep, inheriting the IDE session
   model — no key); never re-implement extraction. Consume native outputs (`graphify-out/graph.json`, `GRAPH_REPORT.md`)
   and targeted `query|path|explain|affected` as duplication / orphan / stale
   signals.
2. **Classify** each finding: duplicate · stale · partial · orphaned ·
   canonical-candidate.
3. **Reconcile** in ≤3-file steps — keep / merge / rewrite / archive / delete /
   promote. Update the matching registry row in the same step. Surface each
   intended change and wait for approval before writing.
4. **Record** the wave outcome: findings closed, and what is queued for the next
   wave.

## Expected output

- A per-wave reconciliation report: findings (with `source_location` citations),
  the decision per finding, and applied edits.
- Updated docs / registries for the reconciled scope.
- A queue line for the next wave (or "documentation debt closed for this scope").

## Validation gate

Wave recorded and `punch-ai-governance` audit clean for the touched files →
the scope is reconciled. Remaining debt advances to the next wave.
