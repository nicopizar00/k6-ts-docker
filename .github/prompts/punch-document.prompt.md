---
agent: punch-ai-governance
description: Documentate — own and reconcile ALL of docs/ (+ .github config, AGENTS.md, CLAUDE.md, README.md) in waves. Maintain lean, AI-First, minimal-human-readable docs (emojis / ASCII emoticons allowed). Map with the Global Graphify repository track, then keep / merge / rewrite / archive / delete / promote.
---
# Punch — Documentate

**Lifecycle phase:** Documentate (recurring maintenance; orthogonal to Spec → Ship)
**Mode:** Ask / Agent — reconciliation edits via `punch-ai-governance`
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(decision authority) + [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(Graphify gate) + [`punch-documentation-and-adrs`](../skills/punch-documentation-and-adrs/SKILL.md)
(writing method). Structural map delegated to existing `/graphify` skill.
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (Documentation mode)
**Operating comms:** Caveman **`lite`** for persistent docs; **`ultra` only for terminal/status summary**. **Wenyan forbidden** in docs, ADRs, context maps, skills, prompts, registries, handoffs — these source-of-truth artifacts. `/graphify` map fork (1-deep) returns `wenyan`-compatible report; evidence consumed, never written verbatim into docs. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Periodically, or after feature lands and docs drift, to retire documentation
debt — duplicated, stale, partial, orphaned knowledge — across **all of `docs/`**
and config/doc surface this prompt owns. Run **one wave at a time**; defer rest.

## Scope — resolves all `docs/`

This prompt (via `punch-ai-governance`, holds complete admin over `.github/`
and `docs/`) owns and reconciles **entire** documentation surface:

- **All human docs** — `README.md`, `docs/**` (incl. `docs/architecture/**`,
  `docs/workflows/**`, `docs/validation/**`, top-level `docs/*.md`), ADRs.
- **All AI-facing docs** — `AGENTS.md`, `CLAUDE.md`, `docs/ai/**`, and
  `.github/` instructions / prompts / skills / agents + registries.

Frozen/upstream zones (`docs/ai/history/**`, `.ai-upstream/**`, adopted-upstream
skills) follow convention in agent's *Handle with care* scope: refresh /
append, don't rewrite.

## Documentation style — AI-First, minimal human-readable

Every doc this phase writes or rewrites is:

- **Lean** — say once, link don't restate; single source of truth per fact.
- **AI-First** — self-describing names, explicit structure, machine-scannable
  (front-loaded summaries, tables, stable headings) so agents resolve fast.
- **Minimal human-readable** — short, skimmable prose for humans; no filler.
- **Emojis / ASCII emoticons allowed** — when aid scannability or signal
  status (✅ ⚠️ ❌ `:)`); explicit carve-out from Caveman's no-decorative-
  emoji rule, for **persisted docs only**. Evidence stays verbatim regardless.

## Canon output patterns

Lifecycle artifacts (spec / plan / build / verify / review / ship) follow
**canon templates** in [`docs/ai/templates/lifecycle/`](../../docs/ai/templates/lifecycle/README.md);
filled, real worked example is
[`docs/ai/golden-lifecycle/`](../../docs/ai/golden-lifecycle/README.md). This phase
**maintains those patterns as canon** — reconcile new specs/plans/reports toward
them, keep lean, never let drift from `.github/prompts/` Expected-
output shapes (prompts stay behavior source of truth). `/punch-init` reports
their presence as `lifecycle_templates` readiness signal.

## Pre-conditions

- Host `graphify` installed (`uv tool install graphifyy`; scoped Rule-1
  exception — [ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)). If
  CLI absent, `punch-context-engineering` gate shows **Graphify
  Team Setup** message and wave proceeds with non-graph evidence.
- Map runs **in IDE session** — active model does semantic extraction,
  **no API key**. Headless `graphify extract --backend` path not used in-IDE.

## How it works (boundary)

**Graphify provides map; `punch-ai-governance` makes every decision.**
Graph is *evidence* for reconciliation, never canonical source. Nothing under
`graphify-out/` promoted to canonical without governance decision, and
never committed (gitignored — [ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)).

## Inputs

- **Wave scope** — slice of full surface above: AI-config (`.github/` +
  `docs/ai/`) · human docs (`README.md`, `docs/**`) · single subsystem.
  *Ownership* is all of `docs/`; *wave* is slice worked this pass.
- **Global Graphify repository track** (see below) — existing
  `graphify-out/` if present, else Map step builds it.

## Graphify — Global repository track

Maintain **one repo-wide ("global") Graphify graph** as standing map of
whole project, and **track** across waves:

- **Build once, global:** `/graphify .` over repository root — whole tree,
  not per-wave slices — so cross-doc duplication/orphan/stale signals visible
  project-wide.
- **Track incrementally:** between waves, keep current with
  `/graphify . --update` (re-extract only new/changed files); after doc-writing
  waves, run manual `--update` so authored docs re-enter graph.
- Still **evidence, never canonical** — `graphify-out/` gitignored and never
  promoted without governance decision ([ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)).

## What to do

1. **Map & gather (via Context Engineering).** Follow `punch-context-engineering`'s
   Graphify gate to build, query, or update graph for this wave's scope —
   reconciliation broad/governance task, so `update` usually warranted.
   Delegate to existing `/graphify` skill (1-deep, inheriting IDE session
   model — no key); never re-implement extraction. Consume native outputs (`graphify-out/graph.json`, `GRAPH_REPORT.md`)
   and targeted `query|path|explain|affected` as duplication / orphan / stale
   signals.
2. **Classify** each finding: duplicate · stale · partial · orphaned ·
   canonical-candidate.
3. **Reconcile** in ≤3-file steps — keep / merge / rewrite / archive / delete /
   promote. Update matching registry row in same step. Surface each
   intended change and wait for approval before writing.
4. **Record** wave outcome: findings closed, and what queued for next
   wave.

## Expected output

- Per-wave reconciliation report: findings (with `source_location` citations),
  decision per finding, applied edits.
- Updated docs / registries for reconciled scope.
- Queue line for next wave (or "documentation debt closed for this scope").

## Validation gate

Wave recorded and `punch-ai-governance` audit clean for touched files →
scope reconciled. Remaining debt advances to next wave.
