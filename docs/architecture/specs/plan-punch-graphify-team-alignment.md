# Plan — Punch + Graphify Team Alignment

> Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Spec: implied by approved team-alignment plan doc (Claude Code session 2026-06-25).
> Governance: [ADR 0002](../../ai/decisions/0002-graphify-host-tool.md).

- **Goal** (from Spec): Enable Punch to produce and share a validated team context
  graph via Graphify — scoped to code + docs, gated through Punch-owned prompts,
  with no automation or workstation leakage by default.

## Scope + ownership

All tasks are AI-config / governance layer (`.gitignore`, `.graphifyignore`,
`.github/skills/`, `.github/prompts/`, `docs/ai/`). Off Docker execution chain —
no `bin/punch`/`reports/`/runtime touch. Engineer = **`punch-ai-governance`** for
all tasks. `punch-graphify` is care-zone (adopted upstream); edits deepen the
intentional adaptation, recorded in `ai.ingest/`.

---

## Tasks

### G-01 — Update `.gitignore` with `graphify-out/` allowlist

- **Goal** — Change fully-ignored `graphify-out/` rule to allowlist pattern that un-ignores only `graph.json` + `GRAPH_REPORT.md`; all other `graphify-out/` contents remain ignored.
- **Allowed edit paths** — `.gitignore`
- **Read-only context paths** — `docs/ai/decisions/0002-graphify-host-tool.md`, `graphify-out/` (list only — do not read contents)
- **Forbidden paths** — everything else; explicitly `src/**`, `docker/**`, `bin/**`, `.github/**`, `ai.ingest/**`
- **Expected diff size** — ~3 lines (add 2 un-ignore rules after existing `graphify-out/` line)
- **Validation commands** —
  ```bash
  # Confirm allowlist parse correctly (git would track graph.json if it existed)
  git check-ignore -v graphify-out/graph.json          # must print no match (not ignored)
  git check-ignore -v graphify-out/GRAPH_REPORT.md     # must print no match (not ignored)
  git check-ignore -v graphify-out/cost.json           # must print graphify-out/ (still ignored)
  git check-ignore -v graphify-out/.graphify_python    # must print graphify-out/ (still ignored)
  git check-ignore -v graphify-out/graph.html          # must print graphify-out/ (still ignored)
  ```
- **Rollback notes** — `git checkout .gitignore`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

### G-02 — Review and extend `.graphifyignore`

- **Goal** — Confirm existing `.graphifyignore` covers safe-first corpus (code + Markdown only); add missing exclusions for media, PDF, Office, and generated paths.
- **Allowed edit paths** — `.graphifyignore`
- **Read-only context paths** — `.graphifyignore` (read current), `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly `src/**`, `docker/**`, `.github/**`
- **Expected diff size** — ~8–12 lines (add missing exclusion patterns if absent)
- **Required exclusions (must be present after Build):**
  ```
  dist/          reports/        graphify-out/   node_modules/
  __pycache__/   *.pyc           .venv/          .git/
  *.log          *.tmp           *.lock          package-lock.json
  *.pdf          *.png           *.jpg           *.jpeg
  *.webp         *.mp4           *.mp3           *.docx    *.xlsx
  ```
- **Validation commands** —
  ```bash
  # Each of these must appear in .graphifyignore
  grep -E "^(dist/|reports/|graphify-out/|node_modules/)" .graphifyignore
  grep -E "^\*\.(pdf|png|mp4|mp3|docx)" .graphifyignore
  ```
- **Rollback notes** — `git checkout .graphifyignore`
- **Human checkpoint** — human approval required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

### G-03 — Add Team Share section to `punch-graphify` SKILL.md

- **Goal** — Document which `graphify-out/` artifacts are team-shareable, the validation checklist required before commit, rebuild guidance for fresh clones, and the explicit forbidden-commands list — all as a single new section in the skill.
- **Allowed edit paths** — `.github/skills/punch-graphify/SKILL.md`
- **Read-only context paths** — `docs/ai/decisions/0002-graphify-host-tool.md`, `ai.ingest/adapters/graphify.json`, `.gitignore`, `.graphifyignore`, `.github/skills/punch-context-engineering/SKILL.md`
- **Forbidden paths** — everything else; explicitly other skills/prompts/agents, `src/**`, `docker/**`, `bin/**`, `ai.ingest/**`
- **Expected diff size** — ~70 lines (new `## Team Share` section)
- **Section must include:**
  1. **Committed artifacts** — `graph.json` + `GRAPH_REPORT.md` only (after validation); `graph.html`, `cost.json`, `.graphify_*`, `cache/` never committed
  2. **Validation checklist** — 6 grep/python checks (absolute paths, venv paths, hostname, JSON validity, node-ID relative check, no cost data); all must pass before commit
  3. **Rebuild guidance** — fresh clone uses committed graph; rebuild only on major shape change or if designated updater
  4. **Forbidden commands** — `graphify *install`, `hook install`, `--watch`, `--mcp`, `graphify add <url>`, cloud backends (`GEMINI_API_KEY`), Neo4j/FalkorDB, cross-repo clone — never default, require Governance sign-off
  5. **Reference to ADR 0002** for the policy rationale
- **Validation commands** —
  ```bash
  grep -n "## Team Share" .github/skills/punch-graphify/SKILL.md
  grep -nE "(graph\.json|GRAPH_REPORT|validation checklist|forbidden)" \
      .github/skills/punch-graphify/SKILL.md
  # Link resolution
  grep "ADR 0002" .github/skills/punch-graphify/SKILL.md
  python3 -m unittest discover -s ai.ingest/tests   # governance suite still green
  ```
- **Rollback notes** — `git checkout .github/skills/punch-graphify/SKILL.md`
- **Human checkpoint** — human approval required before Build; AI Governance reviews new section for policy accuracy before merge
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

### G-04 — Add Team Bootstrap guidance to `punch-context-engineering` SKILL.md *(Phase 2)*

- **Goal** — Add a Team Bootstrap sub-section to the Graphify gate distinguishing fresh-clone usage (use committed graph, skip rebuild) from designated-updater usage (validate + commit), and clarifying local rebuild vs. shared-graph update.
- **Allowed edit paths** — `.github/skills/punch-context-engineering/SKILL.md`
- **Read-only context paths** — `.github/skills/punch-graphify/SKILL.md` (G-03 output), `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly other skills/prompts/agents, `src/**`, `docker/**`
- **Expected diff size** — ~20 lines (new sub-section inside existing Graphify gate block)
- **Validation commands** —
  ```bash
  grep -n "Team Bootstrap\|fresh clone\|committed graph" \
      .github/skills/punch-context-engineering/SKILL.md
  python3 -m unittest discover -s ai.ingest/tests
  ```
- **Rollback notes** — `git checkout .github/skills/punch-context-engineering/SKILL.md`
- **Human checkpoint** — human approval required before Build
- **Dependency** — G-03 must be built and merged first (Team Share section is the policy source)
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

### G-05 — Update `punch-document` pre-conditions and evidence section *(Phase 2)*

- **Goal** — Add two items to `punch-document.prompt.md`: (1) pre-condition noting team members may query the committed graph without rebuilding; (2) evidence note confirming the committed graph is still evidence, not canonical — Governance makes decisions.
- **Allowed edit paths** — `.github/prompts/punch-document.prompt.md`
- **Read-only context paths** — `.github/skills/punch-graphify/SKILL.md` (G-03 output), `.github/skills/punch-context-engineering/SKILL.md` (G-04 output), `docs/ai/decisions/0002-graphify-host-tool.md`
- **Forbidden paths** — everything else; explicitly other prompts/skills/agents, `src/**`, `docker/**`
- **Expected diff size** — ~10 lines (2 additions in pre-conditions + 2 in evidence/boundary)
- **Validation commands** —
  ```bash
  grep -n "committed graph\|team member\|evidence" \
      .github/prompts/punch-document.prompt.md
  grep -c "compare.py graphify" .github/prompts/punch-document.prompt.md  # still ≤1
  python3 -m unittest discover -s ai.ingest/tests
  ```
- **Rollback notes** — `git checkout .github/prompts/punch-document.prompt.md`
- **Human checkpoint** — human approval required before Build
- **Dependency** — G-04 must be built and merged first
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

### G-06 — Extend ADR 0002 with team-sharing policy *(Phase 2)*

- **Goal** — Append a "Team Sharing" section to ADR 0002 recording the decision to commit `graph.json` + `GRAPH_REPORT.md` under the allowlist policy, the validation gate requirement, and the forbidden-by-default automation list.
- **Allowed edit paths** — `docs/ai/decisions/0002-graphify-host-tool.md`
- **Read-only context paths** — `.github/skills/punch-graphify/SKILL.md` (G-03 output), `.gitignore`, `.graphifyignore`
- **Forbidden paths** — everything else; explicitly `src/**`, `docker/**`, `.github/**`, `ai.ingest/**`
- **Expected diff size** — ~30 lines (new section appended to ADR)
- **Validation commands** —
  ```bash
  grep -n "Team Sharing\|allowlist\|validation" docs/ai/decisions/0002-graphify-host-tool.md
  ```
- **Rollback notes** — `git checkout docs/ai/decisions/0002-graphify-host-tool.md`
- **Human checkpoint** — human approval required before Build; this is a permanent governance record
- **Dependency** — G-03 must be built and merged first; G-05 preferred before this
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

## Order of execution

**MVP (ship together or in tight sequence):**

G-01 (gitignore allowlist) → G-02 (graphifyignore) → G-03 (Team Share section)

After G-01–G-03 merge, build and validate first shared graph (human step — run
`/graphify .`, execute validation checklist §10, commit `graph.json` + `GRAPH_REPORT.md`).

**Phase 2 (after MVP graph committed):**

G-04 (context-engineering bootstrap) → G-05 (punch-document) → G-06 (ADR extension)

Not a runtime change — k6 → compose → orchestrator order does not apply.
All tasks are governance / AI-config, off the Docker execution chain.

---

## Cross-cutting risks + constraints

- **Leakage in committed graph.** `graph.json` node IDs may contain absolute paths if
  graphify resolves them at extraction time. Validation checklist check #5 catches this.
  Do not skip. Run on every graph update before commit, not just the first.
- **Stale committed graph.** Team members may query a graph that predates recent
  structural changes. Freshness policy (G-03 + G-04) defines update triggers; reviewer
  confirms on every PR touching service structure.
- **Care-zone edits.** `punch-graphify` SKILL.md is an adopted upstream file (refresh-preferred).
  G-03 deepens the intentional adaptation; update `ai.ingest/adapters/graphify.json`
  and `ai.ingest/adopt.lock.json` in the same step if the adaptation surface changes.
- **No new skills/prompts/agents.** This plan adds sections to existing assets only.
  No new registry rows required. If a new asset is introduced mid-Build, stop and return
  to Plan.
- **Not Punch run evidence.** Validation = grep + python checks + unittest + audit.
  `reports/state/punch-run.json` is unaffected (off execution chain).

---

## Rollback plan

Per-task `git checkout` of named paths:
- G-01: `git checkout .gitignore`
- G-02: `git checkout .graphifyignore`
- G-03: `git checkout .github/skills/punch-graphify/SKILL.md`
- G-04: `git checkout .github/skills/punch-context-engineering/SKILL.md`
- G-05: `git checkout .github/prompts/punch-document.prompt.md`
- G-06: `git checkout docs/ai/decisions/0002-graphify-host-tool.md`

No runtime artifact. Committed `graphify-out/graph.json` + `GRAPH_REPORT.md` revert via
`git checkout graphify-out/` if the shared graph is rolled back.

---

**Gate:** approved when human confirms → Build G-01, G-02, G-03 (MVP) → human validates
and commits shared graph → Build G-04, G-05, G-06 (Phase 2).
