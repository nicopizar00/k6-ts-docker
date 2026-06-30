# Spec — Adopt Adapt graphify → lean `punch-graphify` wired to `/punch-document`

> Increment on approved Spec [`adopt-adapt.md`](adopt-adapt.md) (MVP data model) and
> the read-only [`adopt-adapt-compare.md`](adopt-adapt-compare.md) (the `compare`
> command). This spec carries graphify from an isolated `ai.ingest/` MVP to **fully
> adopted-adapted**: a lean, Punch-governed `punch-graphify` that `/punch-document`
> consumes, with the existing read-only `compare` as adoption-drift governance.
> Pattern source: `.github/prompts/punch-spec.prompt.md` (Caveman `lite`).
> Governance: [ADR 0002](../../ai/decisions/0002-graphify-host-tool.md).

**Status:** Spec — awaiting approval. Plan = next phase.

## Problem (clarify)

ADR 0002 declared graphify a **scoped host-tool**, leaned to an in-IDE subset, and
`/punch-document` the one governed workflow that uses it. Two gaps remain against
that declaration:

1. **The adaptation is not actually lean.** `.github/skills/punch-graphify/` and the
   `.github/copilot-instructions.md` graphify section still carry upstream-only
   surface that ADR 0002 says was removed or that `/punch-document`'s doc-map never
   needs — e.g. `copilot-instructions.md:135` still points at
   `graphify-out/wiki/index.md` (wiki export, declared removed), `references/hooks.md`
   still describes "native CLAUDE.md integration" (non-Copilot host), and
   `references/add-watch.md` carries URL `add` + `--watch` (web fetch / daemon) that
   the documentation map does not use. The live skill therefore diverges from the
   `leaned-fork` the descriptor (`ai.ingest/adapters/graphify.json`) claims.

2. **The adoption is ungoverned at doc time.** `/punch-document` invokes the
   `punch-graphify` map but never consults the Adopt Adapt drift report. The
   read-only `ai.ingest/compare.py graphify` exists but is wired to nothing, so a
   documentation pass cannot tell whether the skill it is about to run still matches
   its pinned baseline.

This spec closes both: filter+adapt `punch-graphify` to the **minimal `/graphify`
subset** `/punch-document` needs (Punch governs tool access — not graphify's default
official installer), and surface the existing read-only drift report inside that
workflow. No apply/install/auto-merge tooling is built.

- **Goal** — `/punch-document` drives a **lean `punch-graphify`** — the minimal
  `/graphify` map subset (build · `--update` · `--cluster-only` · `query` · `path` ·
  `explain`, plus the minimal config/guide assets to run it) — with Punch-governed
  tool access, and each pass gates on the existing **read-only** `compare` drift
  report so the adoption stays auditable. Lean the adaptation to match its declared
  `leaned-fork`; wire drift in; build no new Adopt Adapt command.

- **Non-goals** — this work explicitly will NOT:
  - Build any new Adopt Adapt command (`adopt`/`--write` baseline population,
    `verify`, `adapt`/apply). Hash slots stay `null`; only the existing read-only
    `compare` is used. (Q1 = "wire read-only compare".)
  - Run or endorse graphify's **default official installer** (global install /
    `--with-init` / parallel `.cursor`/`.windsurf` rule files). Punch keeps its own
    scoped, safe host-install path (`uv tool install graphifyy`) — consistent with
    the unsafe-installer finding in [`adopt-adapt-caveman-cavecrew.md`](adopt-adapt-caveman-cavecrew.md).
  - Re-implement graphify extraction/indexing — reuse its native outputs
    (`graphify-out/graph.json`, `GRAPH_REPORT.md`) per ADR 0002.
  - Mutate `.ai-upstream/graphify/` (frozen provenance — read only).
  - Touch the Docker execution chain, `bin/punch`, `reports/`, or any runtime
    service. graphify stays a host authoring/maintenance tool off the evidence path.
  - Generalize to a multi-skill registry or auto-apply. graphify only.
  - Add graphify dependence to any agent/command other than `/punch-document` (+ its
    `punch-context-engineering` gate) — no new host-tool surface.

- **Functional requirements** — observable shape delivered, in two groups Plan may
  ship as separate small PRs:

  **A. Lean the adaptation (`punch-graphify`)**
  - `.github/skills/punch-graphify/SKILL.md` reduced to the minimal `/punch-document`
    map subset: build, `--update`, `--cluster-only`, `query`, `path`, `explain`, and
    the minimal config needed in-IDE (interpreter resolution, no-API-key path).
    Residual upstream-only surface still present is removed or delinked: wiki nav,
    URL `add`, `--watch` daemon, HTML-export prose not needed by the doc map, and any
    non-Copilot ("native CLAUDE.md") wording.
  - `.github/copilot-instructions.md` graphify section corrected to the lean surface —
    drop the `graphify-out/wiki/index.md` reference (removed feature).
  - References under `.github/skills/punch-graphify/references/` pruned/aligned to the
    retained subset; any reference describing only a removed feature is dropped, and
    the descriptor's `expected_absent_references` / `removed_upstream_features` updated
    to match if the retained file-set changes.
  - The lean result is internally consistent: every command the SKILL still documents
    is one the descriptor and copilot-instructions also reflect (no dangling surface).

  **B. Wire read-only drift governance into `/punch-document`**
  - `/punch-document` (`.github/prompts/punch-document.prompt.md`) gains a
    pre-condition / evidence step that runs `python3 ai.ingest/compare.py graphify`
    (read-only) and treats the three-axis report as governance evidence before the
    map wave proceeds.
  - The integration point is the existing **`punch-context-engineering` Graphify
    gate** (already the single place graphify is wired) — the gate references the
    drift report; the prompt names it as a pre-condition. No third integration site.
  - Drift never blocks hard or auto-fixes: a `drift detected` / `baseline incomplete`
    report is surfaced to `punch-ai-governance` as a finding (keep/flag), consistent
    with report-only default and `apply_requires_review: true`.

- **Technical constraints** — implementation must respect:
  - **Read-only Adopt Adapt.** No new command; `compare.py` stays stdlib-only and
    writes nothing. Hash slots remain `null` (degrade to `baseline-not-recorded`,
    not false drift) until a future `adopt` increment.
  - **Reuse, not fork.** Preserve graphify identity verbatim (repo, `pypi:graphifyy`,
    CLI `graphify`, `uv tool install graphifyy`, pinned `0.8.41`). Leaning removes
    surface; it does not re-author graphify behavior.
  - **Copilot-First single source of truth.** `.github/` stays canon; edits to the
    skill/prompt/instructions are governance edits owned by `punch-ai-governance`
    (this touches `.github/` + `docs/ai/` → governance cycle).
  - **No non-Copilot targets** in the leaned assets (delink, keep substance) —
    matches the Copilot-only sanitization convention.
  - **Docker-First not relaxed.** Both groups are host authoring/maintenance off the
    `source → bundle → image → run → report` chain.
  - **Descriptor stays truthful.** If group A changes the retained file-set,
    `ai.ingest/adapters/graphify.json` (`track_globs`, `expected_absent_references`,
    `removed_upstream_features`) and the lock's `adaptation.asset_hashes` key list are
    updated to match — the descriptor must keep describing the real adaptation.

- **Affected layers** ([punch-boundaries.md](../punch-boundaries.md)) —
  **governance / AI-config** is the owning layer (`.github/skills/punch-graphify/`,
  `.github/copilot-instructions.md`, `.github/prompts/punch-document.prompt.md`,
  `.github/skills/punch-context-engineering/`), plus the **host-tooling** layer
  (`ai.ingest/adapters/graphify.json` + `adopt.lock.json`) read/aligned by group A.
  `punch-ai-governance` owns every `.github/` edit. No orchestrator, compose, k6, or
  data layer is touched; nothing is added to the execution chain.

- **Artifact / log / reporting implications** —
  - Edited tracked artifacts: the `punch-graphify` skill set, `copilot-instructions.md`
    graphify section, `punch-document` prompt, `punch-context-engineering` skill, and
    (if file-set changes) `ai.ingest/adapters/graphify.json` + `adopt.lock.json`.
  - **Not** Punch run evidence — `reports/state/punch-run.json` unaffected; no
    `reports/` schema change.
  - `compare` output is throwaway terminal evidence (like `graphify-out/`); it is
    never promoted to canonical docs and never committed.
  - `.gitignore` unchanged: `ai.ingest/` tracked; `.ai-upstream/`, `graphify-out/`
    stay gitignored.

- **Acceptance criteria** — what Test asserts:
  1. `.github/skills/punch-graphify/SKILL.md` documents only the retained subset
     (build · `--update` · `--cluster-only` · `query` · `path` · `explain` + minimal
     config); no wiki, URL `add`, `--watch`, or non-Copilot ("native CLAUDE.md")
     surface remains.
  2. `grep -rn "wiki/index.md"` `.github/copilot-instructions.md` returns nothing
     (removed-feature reference gone); the graphify section names only retained
     commands.
  3. Every command named in the leaned SKILL is also reflected in the descriptor and
     copilot-instructions — no dangling surface; references describe only retained
     features.
  4. If the retained reference file-set changed, `ai.ingest/adapters/graphify.json`
     (`track_globs`, `expected_absent_references`, `removed_upstream_features`) and
     `adopt.lock.json` `adaptation.asset_hashes` keys match the new set, and both
     still parse as strict JSON.
  5. `.github/prompts/punch-document.prompt.md` Pre-conditions name a read-only
     `python3 ai.ingest/compare.py graphify` drift-check step, routed through the
     `punch-context-engineering` Graphify gate (single integration point), with no
     hard-block / auto-fix behavior.
  6. `python3 ai.ingest/compare.py graphify` still runs read-only and exits `0`
     (drift in output, not exit code); hash slots remain `null` (no `adopt` tooling
     added). `python3 -m unittest discover -s ai.ingest/tests` passes.
  7. Punch keeps its scoped install path (`uv tool install graphifyy`); no
     `--with-init` / default-official-installer guidance appears in the touched
     assets. `.ai-upstream/graphify/` byte-unchanged.
  8. `git status` shows only the named governance/host-tooling files (+ this spec);
     `src/`, `docker/`, `bin/`, `docker-compose.yml`, `.github/workflows/`,
     `reports/` untouched.

## Open interpretation (resolve at approval)

"Include minimal config — guide features / assets" is read as **trim to** the minimal
viable subset + keep the in-IDE config needed to run it. If instead the intent is to
**add** a new condensed config/guide asset (a `punch-graphify` quick-card), say so at
approval — that shifts group A from a trim to a trim+author, and Plan adds a task.

## Plan handoff

`punch-plan` should decompose into two scoped Build groups — **A** (lean the
adaptation; governance edit to `.github/` + descriptor truth-up) and **B** (wire the
read-only `compare` drift gate into `/punch-document` via the context-engineering
gate) — each a small, separately-reviewable PR, with `punch-ai-governance` as the
engineer for the `.github/` edits.

**Gate:** approved when Goal, Non-goals, and Acceptance criteria are agreed (and the
Open-interpretation question answered) → Plan.
