---
agent: punch-ai-governance
description: Documentate — documentation-debt remediation + AI-artifact lifecycle over ALL of docs/ (+ .github config, README.md), in waves. Inherited docs and prior AI artifacts (specs, plans, maps, temp scripts, reports) untrusted until verified. Maintain lean, AI-First, minimal-human-readable docs (emojis / ASCII emoticons allowed). Map with the Global Graphify repository track, then keep / merge / compact / convert / promote / archive / delete / review.
---
# Punch — Documentate

**Lifecycle phase:** Documentate (recurring maintenance; orthogonal to Spec → Ship)
**Mode:** Ask / Agent — reconciliation edits via `punch-ai-governance`
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
(decision authority). Delegates — not competitors:
[`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md)
(Graphify gate) · [`punch-documentation-and-adrs`](../skills/punch-documentation-and-adrs/SKILL.md)
(writing method) · [`punch-code-simplification`](../skills/punch-code-simplification/SKILL.md)
(on demand — compacting script-/code-bearing assets). Structural map delegated to
existing `/graphify` skill. Legacy retirement / migration follows
`punch-documentation-and-adrs` + `punch-git-workflow-and-versioning` (upstream
`deprecation-and-migration` stays deferred — [skill registry](../../docs/ai/skill-registry.md)).
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (Documentation mode)
**Operating comms:** Caveman **`full`** for wave working comms — diagnosis, classification, planning; **`lite`** for every persisted artifact (docs, prompt text, instructions, reports) — no verbose AI narrative in persistent assets. **Wenyan forbidden** in docs, ADRs, context maps, skills, prompts, registries, handoffs — these source-of-truth artifacts. `/graphify` map fork (1-deep) returns `wenyan`-compatible report; evidence consumed, never written verbatim into docs. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Periodically, or after feature lands and docs drift, to retire documentation
debt — duplicated, stale, partial, orphaned knowledge — **plus inherited AI
artifacts**: prior specs / plans, bootstrap + wave reports, graph maps, temporary
scripts, prompt/instruction text — across **all of `docs/`** and config/doc
surface this prompt owns. Run **one wave at a time**; defer rest.

**Not** a generic doc-writing prompt — new-feature docs belong to the change
that ships them ([`punch-documentation-and-adrs`](../skills/punch-documentation-and-adrs/SKILL.md)).

## Scope — resolves all `docs/`

This prompt (via `punch-ai-governance`, holds complete admin over `.github/`
and `docs/`) owns and reconciles **entire** documentation surface:

- **All human docs** — `README.md`, `docs/**` (incl. `docs/architecture/**`,
  `docs/workflows/**`, `docs/validation/**`, top-level `docs/*.md`), ADRs.
- **All AI-facing docs** — `docs/ai/**` and
  `.github/` instructions / prompts / skills / agents + registries.
- **AI working artifacts** — `docs/architecture/specs/**` (prior specs / plans),
  `docs/ai/governance/**` (init bootstrap + wave reports), committed graph
  artifacts, leftover temporary scripts/assets inside the owned surface.

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
**canon templates** in `docs/ai/templates/lifecycle/`;
filled, real worked example is
`docs/ai/golden-lifecycle/`. This phase
**maintains those patterns as canon** — reconcile new specs/plans/reports toward
them, keep lean, never let drift from `.github/prompts/` Expected-
output shapes (prompts stay behavior source of truth). `/punch-init` reports
their presence as `lifecycle_templates` readiness signal.

## Pre-conditions

- Host `graphify` installed (`uv tool install graphifyy`; scoped Rule-1
  exception — ADR 0002). If
  CLI absent, `punch-context-engineering` gate shows **Graphify
  Team Setup** message and wave proceeds with non-graph evidence.
- Map runs **in IDE session** — active model does semantic extraction,
  **no API key**. Headless `graphify extract --backend` path not used in-IDE.
- **Adopt Adapt drift (optional, read-only).** Gated via [`punch-context-engineering`](../skills/punch-context-engineering/SKILL.md) (single source). Surface any `drift detected` / `baseline incomplete` as a governance finding for the wave — never a hard block.
- **Shared graph (if committed).** If `graphify-out/graph.json` is a committed repo artifact, team members may run `graphify query "<question>"` directly without rebuilding. Before updating the committed graph in a wave: run the validation checklist in the [`punch-graphify` Team Share section](../skills/punch-graphify/SKILL.md#team-share) and get `punch-ai-governance` sign-off before committing `graph.json` + `GRAPH_REPORT.md`.

## How it works (boundary)

**Inherited artifacts untrusted by default.** Old docs and AI-generated
artifacts are claims, not facts — verify against code / runtime / git history
before `keep` or `promote`; unverifiable → classify `review`, never silently keep.

**Graphify provides map; `punch-ai-governance` makes every decision.**
Graph is *evidence* for reconciliation, never canonical source. Nothing under
`graphify-out/` promoted to canonical without governance decision. `graph.json`
and `GRAPH_REPORT.md` may be committed as shared team artifacts after passing
the leakage validation checklist ([`punch-graphify` Team Share](../skills/punch-graphify/SKILL.md#team-share),
[ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)); all other
`graphify-out/` contents remain gitignored.

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
- Still **evidence, never canonical** — `graphify-out/` contents never promoted
  without governance decision; `graph.json` + `GRAPH_REPORT.md` may be committed
  as shared team artifacts after validation (ADR 0002, Team Share).

## What to do

1. **Map & gather (via Context Engineering).** Follow `punch-context-engineering`'s
   Graphify gate to build, query, or update graph for this wave's scope —
   reconciliation broad/governance task, so `update` usually warranted.
   Delegate to existing `/graphify` skill (1-deep, inheriting IDE session
   model — no key); never re-implement extraction. Consume native outputs (`graphify-out/graph.json`, `GRAPH_REPORT.md`)
   and targeted `query|path|explain|affected` as duplication / orphan / stale
   signals.
2. **Classify** each finding: duplicate · stale · partial · orphaned ·
   unverified · canonical-candidate. Inherited / AI-generated artifacts start
   untrusted — verify before any `keep` / `promote`.
3. **Reconcile** in ≤3-file steps — keep / merge / compact / convert / promote /
   archive / delete / review (unverified → human decision). Update matching
   registry row in same step. Surface each intended change and wait for approval
   before writing.
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
