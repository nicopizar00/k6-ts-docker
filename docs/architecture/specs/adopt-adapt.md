# Spec — Adopt Adapt (graphify MVP)

> Pattern source: `.github/prompts/punch-spec.prompt.md` (Caveman `lite`).
> Design draft: `~/.claude/plans/draft-the-lock-schema-delightful-pebble.md`.
> Seed artifacts already created: `ai.ingest/adopt.lock.json`,
> `ai.ingest/adapters/graphify.json`, `ai.ingest/README.md`.

**Status:** Spec — awaiting approval. Plan = next phase.

## Problem

External Agent Skills (graphify today, more later) get adopted by hand: install
via the tool's own method, copy a pristine snapshot to `.ai-upstream/`, lean-fork
the canon into `.github/`, then eyeball `diff -ru` when upstream moves (the manual
flow `.ai-upstream/graphify/UPSTREAM.md` prescribes). No machine record of *what
version was adopted*, *what the baseline hashes are*, or *what diverged on purpose
vs by drift*. Drift detection is human memory. This spec defines a local,
auditable, report-first mechanism — **Adopt Adapt** — that records adoption and
detects drift without mutating the skill.

- **Goal** — Give the repo a local, inspectable index (lock + per-skill
  descriptor) that records what external skill was adopted, at what version, with
  baseline + adaptation asset hashes, so a future read-only command can report
  three-axis drift against a pinned upstream — graphify being the only adopted
  skill in this MVP.

- **Non-goals** — this work explicitly will NOT:
  - Build any executable code / CLI (`compare`, `verify`, `adopt`, `adapt`) — this
    MVP is the **data model only** (lock schema + descriptor + README).
  - Auto-apply or auto-merge upstream changes. Reports propose; humans/governance
    decide.
  - Build a generic adapter registry, plugin loader, or multi-skill abstraction.
    One hardcoded graphify adapter validates the shape first.
  - Integrate with Punch lifecycle, `bin/punch`, or the Docker execution chain.
  - Wire into VS Code GitHub Copilot (future direction only).
  - Mutate graphify, `.github/`, or `.ai-upstream/`.
  - Re-implement graphify extraction/indexing — reuse its native install + outputs
    (consistent with [ADR 0002](../../ai/decisions/0002-graphify-host-tool.md)).

- **Functional requirements** — observable shape the MVP delivers:
  - A tracked top-level `ai.ingest/` dir, **outside** `.github/` (which stays
    Copilot-canon single source of truth).
  - `adopt.lock.json` (schema v1): one entry per adopted skill; records pinned
    `adopted_version` (PyPI `graphifyy` 0.8.41, `commit`/`tag` null by design),
    `upstream_snapshot` path + present-flag + per-asset hash slots, `adaptation`
    path + `kind` + per-asset hash slots, `last_compared_at`. Hash slots are
    `null` placeholders — populated later by tooling, never hand-typed.
  - `adapters/graphify.json` (schema v1): declarative skill knowledge — identity,
    install/upgrade/fallback commands, verify probes (import check, `--version`,
    version-marker file), asset roots + track globs, output classification
    (evidence vs cache vs `exclude_from_drift`), and the **intentional**
    leaned-fork divergences (`removed_upstream_features`,
    `expected_absent_references`) so deliberate gaps aren't reported as drift.
  - `README.md`: states report-only default, the three artifact categories
    (upstream / adapted / generated-cache), and full lock + descriptor field
    reference (meanings live here since files are strict-JSON, no inline comments).
  - Three independent drift axes named for the future `compare` command:
    version drift, upstream-asset drift, adaptation drift — never collapsed to one
    yes/no.

- **Technical constraints** — implementation must respect:
  - **Strict JSON** for lock + descriptor (no comments) → any stdlib `json.load`
    consumer works zero-fuss. No JSONC.
  - **Stdlib-only** trajectory (matches `src/punch/` precedent + Critical Rule #3);
    no pip deps introduced. This MVP adds no runtime code at all.
  - **Docker-First not relaxed.** Adopt Adapt is host authoring/maintenance
    tooling off the `source → bundle → image → run → report` chain, like graphify
    itself ([ADR 0002](../../ai/decisions/0002-graphify-host-tool.md)). It must not
    touch that chain.
  - **Three categories kept separate:** upstream (gitignored snapshot) / adapted
    (tracked canon) / generated-cache (`graphify-out/`, gitignored, never hashed).
  - **No overwrite of existing files**; all created paths are new.
  - Graphify identity preserved verbatim: repo, `pypi:graphifyy`, CLI
    `graphify`/`graphify-mcp`, install `uv tool install graphifyy`, baseline 0.8.41.
  - Reuse, not fork: descriptor points at graphify's own install/probe/outputs; no
    custom indexing.

- **Affected layers** ([punch-boundaries.md](../punch-boundaries.md)) — introduces a
  new **host-tooling / governance-adjacent** artifact set that *operates on*
  `.ai-upstream/` (gitignored staging) and reads `.github/skills/punch-graphify/`
  (Copilot canon). It owns only `ai.ingest/`. It does **not** own or modify the
  orchestrator, compose-runtime, k6, or data layers, and adds nothing to the
  execution chain. Governance (`punch-ai-governance`) owns any future gate on
  applying an adaptation.

- **Artifact / log / reporting implications** —
  - New tracked artifacts under `ai.ingest/` (`adopt.lock.json`,
    `adapters/graphify.json`, `README.md`). These are **not** Punch run evidence —
    `reports/state/punch-run.json` is unaffected; no `reports/` schema change.
  - No terminal-noise change; MVP ships no command.
  - Future drift reports (`compare`) land under `ai.ingest/reports/` — storage
    (tracked vs gitignored) is a Plan-phase decision, out of scope here.
  - `.gitignore` unchanged: `ai.ingest/` is tracked; `.ai-upstream/` and
    `graphify-out/` stay gitignored as today.

- **Acceptance criteria** — what Test asserts:
  1. `ai.ingest/adopt.lock.json` and `ai.ingest/adapters/graphify.json` both
     parse with `python3 -c "import json; json.load(open(PATH))"` (strict JSON).
  2. Lock `upstream_snapshot.asset_hashes` enumerates exactly the files present in
     `.ai-upstream/graphify/` (SKILL.md + **8** references + `.graphify_version`);
     `adaptation.asset_hashes` enumerates `.github/skills/punch-graphify/` (SKILL.md
     + **5** references). The 3-file gap matches descriptor
     `expected_absent_references` (`exports.md`, `github-and-merge.md`,
     `transcribe.md`).
  3. Descriptor `assets` + `outputs` + `governance.adr` paths all resolve to real
     repo locations.
  4. Pinned version is `0.8.41`; install method is `uv tool install graphifyy`;
     `commit`/`tag` are `null`.
  5. All hash slots are `null` (no hand-typed hashes).
  6. `git status` shows only new `ai.ingest/` paths — graphify, `.github/`,
     `.ai-upstream/`, `.gitignore`, and `reports/` untouched.
  7. README documents report-only default, the three artifact categories, and the
     lock + descriptor field reference.

**Gate:** approved when Goal, Non-goals, Acceptance criteria agreed → Plan
(`punch-plan` decomposes the read-only `compare` command as the first build task).
