# Plan — Adopt Adapt transversal freeze (caveman-full baseline)

> Plan doc. Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Freeze/log operation only — no upstream fetch, no compare, no skill upgrade, no
> behavior mutation. Current repo state = source of truth.

- **Goal** (from input): emit one local, strict-JSON transversal Adopt Adapt log
  that freezes every current Punch GitHub-Copilot asset (skills, prompts, agents,
  instructions, registries, existing `ai.ingest/` assets) with path / type /
  category-owner / caveman-full marker / sha256 / line count / word count / status /
  notes — reusable later for comparison.

## Decisions locked

- **Artifact** — `ai.ingest/freeze/punch-assets-freeze.json` (strict JSON,
  stdlib-consumable; matches existing Adopt Adapt convention). Short pointer in
  `ai.ingest/freeze/README.md`.
- **Profile** — top-level `profile: "caveman-full"`; each asset row carries
  `caveman_full: true` (baseline marker requested).
- **Granularity** — one row per file (per-file sha256, like `adopt.lock.json`
  `asset_hashes`), not per skill-dir. Lets later compare detect single-file drift.
- **Status field** — `frozen` for all rows this pass (freeze snapshot). Reserved
  values for later compare: `unchanged` / `changed` / `added` / `removed`.
- **Generation** — Build computes values with shell (`git hash-object` /
  `sha256sum`, `wc -l`, `wc -w`) then assembles the JSON by hand-free transcription.
  No generator script committed (no premature abstraction; matches Spec stance that
  `adopt --write` tooling stays future). The committed artifact is static data.

## Asset universe (≈80 files)

| Set | Glob | Count | Row `type` | Row `category` |
|---|---|---|---|---|
| Skills | `.github/skills/**/*.md` | 37 | `skill` / `skill-reference` | `method` / `domain` / `meta` |
| Prompts | `.github/prompts/*.prompt.md` | 8 | `prompt` | lifecycle phase |
| Agents | `.github/agents/*.agent.md` | 12 | `agent` | persona role |
| Instructions | `.github/instructions/*.instructions.md` | 7 | `instruction` | path-scope |
| Copilot root | `.github/copilot-instructions.md`, `.github/PULL_REQUEST_TEMPLATE.md` | 2 | `global-rule` / `template` | governance |
| Registries | `docs/ai/*.md` | 9 | `registry` | governance |
| Existing Adopt Adapt | `ai.ingest/**` tracked | 5 | `adopt-adapt` | host-tooling |

Owner per row = the `punch-*` agent/skill that governs the asset (e.g. governance,
architect, builder). `caveman_full = true` on every row (baseline tag); per-asset
declared caveman level (if any) recorded in `notes`.

## Tasks

### AA-01 — write transversal freeze JSON
- **Goal** — produce `ai.ingest/freeze/punch-assets-freeze.json` with `schema_version`,
  `profile: "caveman-full"`, `frozen_at`, `source_of_truth: "working-tree"`, and an
  `assets` array of one row per file across the seven sets above.
- **Allowed edit paths** — `ai.ingest/freeze/punch-assets-freeze.json`
- **Read-only context paths** — `.github/skills/**`, `.github/prompts/**`,
  `.github/agents/**`, `.github/instructions/**`, `.github/copilot-instructions.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`, `docs/ai/*.md`, `ai.ingest/**`
- **Forbidden paths** — everything else. Explicitly: `src/**`, `docker/**`,
  `bin/**`, `docker-compose.yml`, `.github/workflows/**`, `.ai-upstream/**`,
  `reports/**`, and **no edit to any `.github/` asset** (read-only — this is a log).
- **Expected diff size** — ~90–110 lines JSON (one compact object per asset) +
  header fields.
- **Validation commands** — `python3 -c "import json;d=json.load(open('ai.ingest/freeze/punch-assets-freeze.json'));print(len(d['assets']),'assets')"`
  (strict parse + count); `git status` shows only new `ai.ingest/freeze/` files.
- **Rollback notes** — `rm ai.ingest/freeze/punch-assets-freeze.json` (new untracked
  file; no existing artifact touched).
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build`.

### AA-02 — freeze pointer README
- **Goal** — `ai.ingest/freeze/README.md`: one short page stating what the freeze is
  (caveman-full baseline snapshot), the row fields, the seven covered sets, that it is
  read-only/non-mutating and meant for later `compare`, and how it was generated.
- **Allowed edit paths** — `ai.ingest/freeze/README.md`
- **Read-only context paths** — `ai.ingest/freeze/punch-assets-freeze.json`,
  `ai.ingest/README.md`
- **Forbidden paths** — everything else, including the freeze JSON (AA-01 owns it) and
  all `.github/**`.
- **Expected diff size** — ~30–40 lines.
- **Validation commands** — `git status` shows only `ai.ingest/freeze/` additions.
- **Rollback notes** — `rm ai.ingest/freeze/README.md`.
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build`.

## Order of execution

AA-01 → AA-02. README documents the JSON, so JSON exists first. Not a runtime change —
the usual k6 → compose → orchestrator order does not apply; both tasks are host-tooling
(`ai.ingest/`) off the execution chain.

## Cross-cutting risks

- **Read-only discipline.** The whole point is a freeze — Build must not edit any
  `.github/` or `docs/ai/` asset. Forbidden-path lists above enforce it; reviewer
  confirms `git status` shows only `ai.ingest/freeze/` additions.
- **Count drift mid-build.** If an asset file is added/removed between this Plan and
  Build, the 80-file count shifts. Build records the actual working-tree set and notes
  the count in `frozen_at` context, not the planned number.
- **Owner attribution is judgment.** `category`/`owner` per row is inferred from the
  asset's frontmatter/registry. Where ambiguous, Build records best-effort owner and
  flags uncertainty in `notes` rather than guessing silently.
- **`PULL_REQUEST_TEMPLATE.md` borderline.** Not a pure AI asset. Included for
  completeness, typed `template`; reviewer may drop it — note, don't block.
- **Not Punch run evidence.** This artifact is not a `reports/state/punch-run.json`
  record; Test for this change = strict-JSON parse + `git status` scope check, not a
  k6 run.

## Rollback plan

Both files are new and untracked under `ai.ingest/freeze/`. Whole change reverts with
`rm -r ai.ingest/freeze/`. No existing tracked file is modified, so there is nothing to
restore.

**Gate:** approved when human confirms → Build (per task ID AA-01, then AA-02).
