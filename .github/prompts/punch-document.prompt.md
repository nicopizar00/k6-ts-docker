---
agent: punch-ai-governance
description: Documentate — own and reconcile ALL of docs/ (+ .github config, AGENTS.md, CLAUDE.md, README.md) in waves. Maintain lean, AI-First, minimal-human-readable docs (emojis / ASCII emoticons allowed). Map with the Global Graphify repository track, then keep / merge / rewrite / archive / delete / promote.
---

# Punch — Documentate

**Lifecycle phase:** Documentate (recurring maintenance; orthogonal to Spec → Ship)
**Mode:** Ask / Agent — reconciliation edits via `punch-ai-governance`
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(the decision authority) + [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(the Graphify gate) + [`documentation-and-adrs`](../skills/documentation-and-adrs/SKILL.md)
(the writing method). The structural map is delegated to the existing `/graphify` skill.
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (Documentation mode)
**Operating comms:** Caveman **`lite`** for persistent documentation; **`ultra` only for a terminal/status summary**. **Wenyan is forbidden** in docs, ADRs, context maps, skills, prompts, registries, and handoffs — these are source-of-truth artifacts. The `/graphify` map fork (1-deep) returns a `wenyan`-compatible report; its evidence is consumed, never written verbatim into docs. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Periodically, or after a feature lands and docs drifted, to retire documentation
debt — duplicated, stale, partial, or orphaned knowledge — across **all of `docs/`**
and the config/doc surface this prompt owns. Run **one wave at a time**; defer the rest.

## Scope — resolves all `docs/`

This prompt (via `punch-ai-governance`, which holds complete admin over `.github/`
and `docs/`) owns and reconciles the **entire** documentation surface:

- **All human docs** — `README.md`, `docs/**` (incl. `docs/architecture/**`,
  `docs/workflows/**`, `docs/validation/**`, top-level `docs/*.md`), ADRs.
- **All AI-facing docs** — `AGENTS.md`, `CLAUDE.md`, `docs/ai/**`, and the
  `.github/` instructions / prompts / skills / agents + registries.

Frozen/upstream zones (`docs/ai/history/**`, `.ai-upstream/**`, adopted-upstream
skills) follow the convention in the agent's *Handle with care* scope: refresh /
append, don't rewrite.

## Documentation style — AI-First, minimal human-readable

Every doc this phase writes or rewrites is:

- **Lean** — say it once, link don't restate; single source of truth per fact.
- **AI-First** — self-describing names, explicit structure, machine-scannable
  (front-loaded summaries, tables, stable headings) so agents resolve it fast.
- **Minimal human-readable** — short, skimmable prose for humans; no filler.
- **Emojis / ASCII emoticons allowed** — when they aid scannability or signal
  status (✅ ⚠️ ❌ `:)`); this is an explicit carve-out from Caveman's no-decorative-
  emoji rule, for **persisted docs only**. Evidence stays verbatim regardless.

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

- **Wave scope** — a slice of the full surface above: AI-config (`.github/` +
  `docs/ai/`) · human docs (`README.md`, `docs/**`) · a single subsystem. The
  *ownership* is all of `docs/`; the *wave* is the slice worked this pass.
- The **Global Graphify repository track** (see below) — an existing
  `graphify-out/` if present, else the Map step builds it.

## Graphify — Global repository track

Maintain **one repo-wide ("global") Graphify graph** as the standing map of the
whole project, and **track** it across waves:

- **Build once, global:** `/graphify .` over the repository root — the whole tree,
  not per-wave slices — so cross-doc duplication/orphan/stale signals are visible
  project-wide.
- **Track incrementally:** between waves, keep it current with
  `/graphify . --update` (re-extract only new/changed files); after doc-writing
  waves, run a manual `--update` so authored docs re-enter the graph.
- Still **evidence, never canonical** — `graphify-out/` is gitignored and never
  promoted without a governance decision ([ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)).

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
