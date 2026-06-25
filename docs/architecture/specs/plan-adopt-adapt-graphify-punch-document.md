# Plan — Graphify as a tool-backed context adapter (Document + Context Engineering only)

> Plan doc. Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Scope: integrate Graphify **only** through `/punch-document` + `punch-context-engineering`.
> Treat Graphify as a **tool-backed context adapter**, not a generic lifecycle skill.
> All Graphify invocation stays controlled by Punch prompts — no autonomous default.
> Governance: [ADR 0002](../../ai/decisions/0002-graphify-host-tool.md). Owner of every
> `.github/` edit: `punch-ai-governance`. **Plan only — no files implemented yet.**

**Status:** Plan — awaiting approval. Build deferred (per non-goal "do not implement yet").

---

## 1. Current repo findings

Graphify already partly present; gaps are surgical, not greenfield.

| Asset | State | Gap vs goal |
|---|---|---|
| `.github/skills/punch-graphify/` (SKILL.md + 5 refs + `.graphify_version`) | Leaned-fork adapter, in-IDE subset | Carries residual non-doc surface (URL `add`, `--watch`, "native CLAUDE.md" wording). Out of *this* plan's edit scope (non-goal: no skill overwrite) — flagged only. |
| `.github/copilot-instructions.md` §graphify (124–140) | **Always-on default**: "your first action should be `graphify query`" | Violates "no autonomous default outside Punch prompts". Line 135 cites removed `graphify-out/wiki/index.md`. → **G-01**. |
| `.github/skills/punch-context-engineering/SKILL.md` §Graphify gate (99–133) | Already the single decision-point: install msg, build/query/update flow, "single gate" | Missing adapter framing + drift-awareness pointer. → **G-02** (additive). |
| `.github/prompts/punch-document.prompt.md` | Invokes `/graphify` map, global-track, ADR 0002 boundary | No read-only drift-check step; invocation implicit. → **G-03** (additive). |
| `ai.ingest/adopt.lock.json` + `adapters/graphify.json` + `compare.py` | Adopt Adapt MVP: lock + descriptor + read-only 3-axis `compare`; hash slots `null` | Adopt Adapt metadata shape already exists; only needs confirm/align. → **G-04**. No new tooling. |
| `.ai-upstream/graphify/` | Pristine v0.8.41 snapshot, gitignored drift baseline | Present locally; OK. |

---

## 2. Graphify upstream facts + commands (inspected `.ai-upstream/graphify/`, not inferred)

Source: `.ai-upstream/graphify/UPSTREAM.md` + `SKILL.md` + `.graphify_version` (snapshot 2026-06-18).

- **Upstream project:** `https://github.com/safishamsi/graphify`
- **Distribution:** PyPI `graphifyy`. Host CLI: `graphify`, `graphify-mcp`.
- **Version captured:** `0.8.41` (PyPI version-kind; `commit`/`tag` null by design — no git pin upstream).
- **Official install (host):** `uv tool install graphifyy` (upgrade: `--upgrade`; fallback `pip install graphifyy`).
- **Entrypoint:** `SKILL.md`, invoked `/graphify`; `references/` lazy-loaded.
- **In-IDE run model:** active IDE model does semantic extraction — **no API key**. Headless `graphify extract --backend` is off-IDE/CI only (throws `no LLM API key found` in-IDE).
- **Read-side commands Punch uses:** `query` (BFS) / `query --dfs` / `path "<A>" "<B>"` / `explain "<node>"` / `affected`.
- **Build/maintain commands:** `/graphify .` (build) · `--update` (incremental) · `--cluster-only` (recluster).
- **Native outputs (`graphify-out/`):** `graph.json` (GraphRAG JSON), `GRAPH_REPORT.md` (audit), `graph.html` (viz).
- **Upstream-only surface NOT used by Punch** (per ADR 0002): remote-repo clone + cross-repo merge, Whisper transcription, wiki/SVG/GraphML/obsidian + Neo4j/FalkorDB exports, MCP server.

---

## 3. Proposed Punch integration model

Graphify = **tool-backed context adapter** with exactly **two controlled entry points**; nothing else invokes it.

```
                 ┌─────────────────────────────────────────┐
   user/agent ──▶│ punch-context-engineering · Graphify gate│  decides IF graphify runs
                 │  (build? query? update? or skip)         │  → query/path/explain flow
                 └───────────────┬─────────────────────────┘
                                 │ consumes graphify-out/ (evidence)
                 ┌───────────────▼─────────────────────────┐
   /punch-document ──────────────▶ invokes /graphify map ──▶│ reconciliation evidence
   (governed wave)               │  (build/update global)   │  (never canonical)
                 └──────────────────────────────────────────┘
   Adopt Adapt (ai.ingest/, read-only `compare`) ── audits adapter drift, off to the side
```

Rules of the model:
- **No autonomous default.** copilot-instructions no longer says "first action = graphify query". Graphify runs only when a Punch prompt routes through the Context Engineering gate.
- **Context Engineering owns the run decision** (gate already states this). Document is a consumer that may request a build/update wave.
- **Reuse, not fork.** Consume native `graph.json` / `GRAPH_REPORT.md`; no re-implementation.
- **Evidence, never canonical.** `graphify-out/` gitignored, throwaway (ADR 0002).
- **Adopt Adapt is read-only governance**, parallel to the run path — not in the invocation flow.

---

## 4. Proposed file/path map + generated-file disposition

| Path | Category | Disposition | Note |
|---|---|---|---|
| `ai.ingest/adopt.lock.json` | Adopt Adapt metadata | **committed** | version + asset-hash index |
| `ai.ingest/adapters/graphify.json` | Adopt Adapt descriptor | **committed** | identity/install/outputs/adaptation |
| `ai.ingest/compare.py` + `tests/` | read-only drift tool | **committed** | stdlib, no new tooling added |
| `.github/skills/punch-graphify/.graphify_version` | version capture | **committed** | pins adopted `0.8.41` |
| `.ai-upstream/graphify/**` | pristine upstream snapshot | **ignored** | gitignored drift baseline; re-fetchable |
| `graphify-out/graph.json` | graph state | **generated-only / ignored** | evidence |
| `graphify-out/GRAPH_REPORT.md` | audit report | **generated-only / ignored** | evidence |
| `graphify-out/graph.html` | viz | **optional / generated-only / ignored** | only if not `--no-viz` |
| `graphify-out/{cost.json,.graphify_python,.graphify_root,.graphify_*.json}` | cache | **generated-only / ignored** | churns each run; `exclude_from_drift` |
| `graphify-out/wiki/**`, exports | upstream-only | **not produced** | removed feature; drop references |

`.gitignore` unchanged: `ai.ingest/` tracked; `.ai-upstream/`, `graphify-out/` ignored.

---

## 5. Proposed prompt/skill changes (additive + surgical — no overwrite)

All three are small, in-place edits; none rewrites a prompt/skill.

- **copilot-instructions §graphify** → demote from autonomous default to a **pointer**: "Graphify runs only through `/punch-document` + the `punch-context-engineering` Graphify gate; do not invoke by default." Drop the wiki line. (G-01)
- **punch-context-engineering Graphify gate** → add one line framing Graphify as a tool-backed context adapter + a pointer to the read-only drift check (`ai.ingest/compare.py graphify`) as optional governance awareness. Keep the existing 5-step gate intact. (G-02)
- **punch-document Pre-conditions / Map step** → name the `/graphify` invocation explicitly as gated through Context Engineering, and add an optional read-only drift-check pointer (surfaced to `punch-ai-governance` as a finding, never a hard block). (G-03)

---

## 6. Proposed Adopt Adapt metadata shape for Graphify (minimal, already seeded)

The existing `ai.ingest/` shape already satisfies req 8; this plan **confirms** it, no redesign:

| Req | Field in existing shape |
|---|---|
| Upstream source | `adapters/graphify.json` → `identity.upstream_repo`, `distribution` |
| Version / commit capture | `adopt.lock.json` → `adopted_version{package_version:"0.8.41", commit:null, tag:null, install_method}` + skill `.graphify_version` |
| Generated asset inventory | `adapters/graphify.json` → `outputs{evidence,cache,exclude_from_drift}` |
| Comparison vs local adaptation | `compare.py` axes: version · upstream-snapshot · adaptation (read-only) |
| Future drift detection | `adaptation.asset_hashes` slots (`null` now) populated by a future `adopt` step — **out of scope here** |

No metadata file change required unless G-01..G-03 alter the tracked surface; if so, descriptor `track_globs` re-aligned (covered in G-04).

---

## 7. Tasks (contracts)

Domain note: these are **governance / host-tooling** tasks (no O/C/K/B/D runtime domain); engineer = `punch-ai-governance` for every `.github/` edit. Each is independently reviewable.

### G-01 — demote copilot-instructions §graphify to a gated pointer
- **Goal** — replace the always-on "first action = graphify query" block with a pointer that Graphify runs only via `/punch-document` + Context Engineering gate; remove the removed-wiki reference.
- **Allowed edit paths** — `.github/copilot-instructions.md` (only the `## graphify` section, lines ~124–140)
- **Read-only context paths** — `.github/prompts/punch-document.prompt.md`, `.github/skills/punch-context-engineering/SKILL.md`, `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly all other `.github/` sections, `src/**`, `docker/**`, `bin/**`, `ai.ingest/**`, other prompts/skills/agents
- **Expected diff size** — ~10–15 lines (net reduction)
- **Validation** — `grep -n "wiki/index.md" .github/copilot-instructions.md` returns nothing; `grep -n "first action" .github/copilot-instructions.md` no longer asserts autonomous graphify; `punch-ai-governance` audit clean
- **Rollback** — `git checkout .github/copilot-instructions.md`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (governance edit; `punch-ai-governance`)

### G-02 — frame Graphify as context adapter in the Context Engineering gate
- **Goal** — add adapter framing + read-only drift-awareness pointer to the existing Graphify gate without altering its 5 steps.
- **Allowed edit paths** — `.github/skills/punch-context-engineering/SKILL.md` (Graphify gate section only)
- **Read-only context paths** — `ai.ingest/README.md`, `ai.ingest/adapters/graphify.json`, `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly other skills, prompts, agents, `ai.ingest/*.py`, runtime layers
- **Expected diff size** — ~5–10 lines added
- **Validation** — gate still lists steps 0–5; new lines reference adapter + `compare.py` as optional; no behavior made autonomous; `punch-ai-governance` audit clean
- **Rollback** — `git checkout .github/skills/punch-context-engineering/SKILL.md`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

### G-03 — make `/punch-document` invocation explicit + add read-only drift pointer
- **Goal** — in punch-document, name the gated `/graphify` invocation and add an optional read-only `compare` drift-check surfaced as a governance finding (no hard block, no auto-fix).
- **Allowed edit paths** — `.github/prompts/punch-document.prompt.md` (Pre-conditions / Map step only)
- **Read-only context paths** — `.github/skills/punch-context-engineering/SKILL.md`, `ai.ingest/README.md`, `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly other prompts/skills/agents, runtime layers, `ai.ingest/*.py`
- **Expected diff size** — ~6–12 lines added
- **Validation** — prompt names `python3 ai.ingest/compare.py graphify` as optional read-only step routed through the gate; no auto-apply wording; `punch-ai-governance` audit clean
- **Rollback** — `git checkout .github/prompts/punch-document.prompt.md`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

### G-04 — confirm/align Adopt Adapt metadata (only if G-01..G-03 shift tracked surface)
- **Goal** — verify lock + descriptor still describe the real adapter; re-align `track_globs` / `expected_absent_references` only if the retained surface changed. No new command.
- **Allowed edit paths** — `ai.ingest/adapters/graphify.json`, `ai.ingest/adopt.lock.json` (only if needed)
- **Read-only context paths** — `.github/skills/punch-graphify/**`, `.ai-upstream/graphify/**`, `ai.ingest/README.md`
- **Forbidden paths** — everything else; explicitly `ai.ingest/compare.py` (no tooling change), all `.github/` prompts/agents, runtime layers
- **Expected diff size** — 0–10 lines (likely no-op)
- **Validation** — `python3 -c "import json;json.load(open('ai.ingest/adopt.lock.json'));json.load(open('ai.ingest/adapters/graphify.json'))"`; `python3 ai.ingest/compare.py graphify` exits 0; `python3 -m unittest discover -s ai.ingest/tests` passes; hash slots remain `null`
- **Rollback** — `git checkout ai.ingest/`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

## 8. Order of execution

G-01 → G-02 → G-03 → G-04. (Demote autonomous default first, then make the two governed entry points explicit, then truth-up metadata.) Not a runtime change — k6 → compose → orchestrator order does not apply; all tasks are governance/host-tooling off the execution chain.

---

## 9. Cross-cutting risks + constraints

- **No autonomous default (primary).** G-01 is the load-bearing change; if skipped, Graphify stays an always-on behavior outside Punch prompts — the exact thing the goal forbids.
- **No-overwrite discipline.** G-02/G-03 are additive; reviewer confirms the existing gate steps and prompt waves are intact (diff is insertion, not rewrite).
- **Read-only Adopt Adapt.** No `adopt`/`verify`/`apply` tooling built; hashes stay `null`; `compare` writes nothing.
- **Docker-First intact.** All edits are host authoring/governance off `source → bundle → image → run → report`. No `bin/punch`, `reports/`, runtime touch.
- **MCP deferred.** `graphify-mcp` exists upstream but stays **optional future work** — not wired (non-goal).
- **No hooks by default.** Post-commit auto-rebuild hook (upstream `references/hooks.md`) **not** installed (non-goal).
- **Lifecycle phases untouched.** Build/Test/Review/Ship/Spec prompts/agents not modified (non-goal).
- **Not Punch run evidence.** Test for these = grep/JSON-parse/governance-audit, not a k6 run; `reports/state/punch-run.json` unaffected.
- **Residual skill surface** (URL `add`, `--watch`, "native CLAUDE.md" in `punch-graphify`) is out of scope here (no skill overwrite); flagged for a separate governance task if wanted.

---

## 10. Minimal next implementation steps

1. Approve this Plan (+ confirm G-04 likely no-op).
2. Build **G-01** (demote autonomous default) — smallest, highest-value, isolatable PR.
3. Build **G-02** then **G-03** (governed entry points) — one PR or two.
4. Run **G-04** check; commit only if surface shifted.
5. Each via `/build` → `punch-ai-governance`, then `/test` (grep + JSON-parse + audit), `/review`, `/ship`.

## Rollback plan

Every task edits one tracked file with a clean `git checkout` revert; G-04 likely no-op. No new files created by Build; no runtime artifact to restore.

**Gate:** approved when human confirms task set + scope → Build per task ID (G-01 first).
