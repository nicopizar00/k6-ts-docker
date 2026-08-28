---
agent: punch-ai-governance
description: Documentate — documentation-debt remediation + AI-artifact lifecycle over ALL of docs/ (+ .github config, README.md), in waves. Inherited docs and prior AI artifacts (specs, plans, maps, temp scripts, reports) untrusted until verified. Maintain lean, AI-First, minimal-human-readable docs (emojis / ASCII emoticons allowed). Reconcile via keep / merge / compact / convert / promote / archive / delete / review.
---
# Punch — Documentate

**Lifecycle phase:** Documentate (recurring maintenance; orthogonal to Spec → Ship)
**Mode:** Ask / Agent — reconciliation edits via `punch-ai-governance`
**Owner skill:** `punch-ai-governance` agent (decision authority; audit
procedure folded in). Delegates — not competitor:
[`punch-documentation-and-adrs`](../skills/punch-documentation-and-adrs/SKILL.md)
(writing method). Legacy retirement / migration follows
`punch-documentation-and-adrs` + `punch-git-workflow-and-versioning` (upstream
`deprecation-and-migration` stays deferred — [skill registry](../../docs/ai/skill-registry.md)).
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (Documentation mode)
**Operating comms:** No verbose AI narrative in persistent assets (docs, prompt text, instructions, reports) — these are source-of-truth artifacts.

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
  `docs/workflows/**` [covers `docs/workflows/validation.md`], top-level
  `docs/*.md`), ADRs.
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
  status (✅ ⚠️ ❌ `:)`), for **persisted docs only**. Evidence stays verbatim regardless.

## Canon output patterns

Lifecycle artifacts (spec / plan / build / verify / review / ship) follow
**canon templates** in `docs/ai/templates/lifecycle/`;
filled, real worked example is
`docs/ai/golden-lifecycle/`. This phase
**maintains those patterns as canon** — reconcile new specs/plans/reports toward
them, keep lean, never let drift from `.github/prompts/` Expected-
output shapes (prompts stay behavior source of truth).

## Pre-conditions

- **Adopt Adapt drift (optional, read-only).** Available directly via
  `python3 ai.ingest/compare.py`. Surface any `drift detected` / `baseline
  incomplete` as a governance finding for the wave — never a hard block.

## How it works (boundary)

**Inherited artifacts untrusted by default.** Old docs and AI-generated
artifacts are claims, not facts — verify against code / runtime / git history
before `keep` or `promote`; unverifiable → classify `review`, never silently keep.

**`punch-ai-governance` makes every reconciliation decision.** Nothing under
`docs/` or `.github/` is reconciled without this agent's classification and,
where a write is involved, the user's approval. `.github/**` and `docs/**`
(plus the explicitly owned `README.md` / `.vscode/settings.json` surfaces)
stay authoritative for VS Code GitHub Copilot Chat; `CLAUDE.md` is disabled
Copilot canon in this workspace (see the Discovery boundary in
`copilot-instructions.md`) and is never called authoritative here.

## Inputs

- **Explicit free-form instruction** — user may name exact files, a single
  localized cleanup, a reconciliation target, or leave scope implicit
  (defaults to next queued wave item from the prior run's Record). A
  free-form instruction always overrides default wave-selection.
- **Wave scope** — slice of full surface above: AI-config (`.github/` +
  `docs/ai/`) · human docs (`README.md`, `docs/**`) · single subsystem ·
  or the single file/localized target named by the instruction above.
  *Ownership* is all of `docs/`; *wave* is slice worked this pass — a wave
  may be as narrow as one file.

## What to do

1. **Map & gather.** Read the wave's target files/docs directly (Read/Grep/Glob).
2. **Classify** each finding: duplicate · stale · partial · orphaned ·
   unverified · canonical-candidate. Inherited / AI-generated artifacts start
   untrusted — verify before any `keep` / `promote`.
3. **Reconcile** in small, reviewable steps — keep / merge / compact / convert /
   promote / archive / delete / review (unverified → human decision). Update
   matching registry row in same step. Surface each intended change and wait
   for approval before writing.
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
