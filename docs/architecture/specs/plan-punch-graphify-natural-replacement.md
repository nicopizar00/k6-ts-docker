# Plan — `punch-graphify` as the natural replacement for default graphify (+ Review follow-ups)

> Plan doc. Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Follows the approved `/punch-document` integration plan
> ([`plan-adopt-adapt-graphify-punch-document.md`](plan-adopt-adapt-graphify-punch-document.md))
> and the Review of G-01..G-04. Closes the two Review follow-ups + makes the leaned
> `punch-graphify` skill the safe, gated, Copilot-native replacement for upstream
> default graphify. Governance: [ADR 0002](../../ai/decisions/0002-graphify-host-tool.md).

**Status:** Plan — **corrective revision** (rev 2). Build of the prior GR-01 (lean SKILL
+ delete 2 refs) is already applied in the working tree but Test **FAILED**: deleting the
references while their keys still live in `adopt.lock.json` makes
`test_compare.py::test_main_against_seed_is_readonly_and_complete` see `drift detected:
adaptation`. Root cause = the prior split (GR-01 lean, GR-02 metadata) is **not
independently green**; the working tree is red between the two. This rev **merges them into
one atomic task** so every task boundary leaves the suite green.

---

## Goal (from input)

Make the in-repo `punch-graphify` skill the **natural replacement for default
graphify** — invoking graphify in this repo runs the leaned, gated, Copilot-native
skill, never the upstream autonomous/non-Copilot surface — and resolve the two Review
follow-ups (lean the residual skill surface; dedupe the drift pointer).

## Why (findings)

Residual surface in `punch-graphify` contradicted the shipped gating:

- **`references/hooks.md`** documented `graphify claude install` → writes an **always-on
  `## graphify` section into `CLAUDE.md`** ("no manual `/graphify` needed") — the exact
  autonomous-default + non-Copilot behavior G-01 removed; plus a post-commit hook
  (non-goal: no hooks).
- **`references/add-watch.md`** documented `/graphify add <url>` (external web fetch,
  incl. removed-feature video transcription) and `--watch` (background daemon).
- **`SKILL.md`** Usage + two sections advertised that surface.
- **Review follow-up 1:** `compare.py graphify` drift pointer stated twice (gate +
  `/punch-document` pre-conditions).

Retained doc-map subset: build · `--update` · `--cluster-only` · `query` · `path` ·
`explain`, HTML viz (`graph.html` is a descriptor evidence output), + references
`extraction-spec.md`, `query.md`, `update.md`.

## Lesson driving rev 2 (compare.py logic)

`compare.py` adaptation axis: a lock `adaptation.asset_hashes` key with **no live file** →
`removed` → drift, **unless** the basename is in descriptor `expected_absent_references`
→ `intentional-absent` (suppressed). Therefore the SKILL lean, the ref deletions, **and**
the lock/descriptor truth-up are one coupled unit — any partial subset trips the coherence
test. They must build + test together.

---

## Scope + ownership

- **Governance / AI-config** (`.github/skills/punch-graphify/**`, `.github/prompts/punch-document.prompt.md`)
  + **host-tooling** (`ai.ingest/adapters/graphify.json`, `ai.ingest/adopt.lock.json`):
  engineer = **`punch-ai-governance`** for all tasks (the lock/descriptor are governance
  metadata mirroring `.github`; `ai.ingest/` routing **approved** for this agent,
  consistent with prior G-04). `punch-graphify` is a **care-zone** (adopted upstream); the
  edit deepens the *intentional* leaned-fork, so the Adopt Adapt record moves with it.
- Off the Docker execution chain; no `bin/punch`/`reports/`/runtime touch.

---

## Tasks

### GR-01 (atomic) — lean `punch-graphify` + truth-up Adopt Adapt, in one green step
- **Goal** — trim `SKILL.md` to the retained doc-map subset (drop `add`/`--watch` Usage
  lines, the `add` subcommand-guard mention, the `## For /graphify add and --watch` and
  `## For the commit hook and native CLAUDE.md integration` sections); add the
  "canonical Punch-leaned replacement — gated, CLI-only install, no official
  skill-install/`claude install`/hooks" framing; delete `references/add-watch.md` +
  `references/hooks.md`; **and in the same task** record the removals in the Adopt Adapt
  index so `compare` reports them `intentional-absent`, not drift: add `add-watch.md` +
  `hooks.md` to descriptor `expected_absent_references` + `removed_upstream_features`, and
  drop their two keys from lock `adaptation.asset_hashes`.
- **Allowed edit paths** —
  `.github/skills/punch-graphify/SKILL.md`,
  `.github/skills/punch-graphify/references/add-watch.md` (delete),
  `.github/skills/punch-graphify/references/hooks.md` (delete),
  `ai.ingest/adapters/graphify.json`,
  `ai.ingest/adopt.lock.json`
- **Read-only context paths** — `.ai-upstream/graphify/**`, `ai.ingest/README.md`,
  `ai.ingest/compare.py`, `docs/ai/decisions/0002-graphify-host-tool.md`,
  `.github/copilot-instructions.md`
- **Forbidden paths** — everything else; explicitly `references/extraction-spec.md`,
  `references/query.md`, `references/update.md` (retained — keep), `ai.ingest/compare.py`
  (no tooling change), other skills/prompts/agents, runtime layers
- **Expected diff size** — SKILL ~ −40; 2 files deleted; ~8 lines across the 2 JSONs
- **5-file note (≤3 guard, justified waiver).** Exceeds the ≤3-files/step governance
  guard, deliberately: the Test FAIL proved these five files are one coherent leaned-fork
  transition; splitting leaves a red tree. Reviewer reviews them as one diff. **Most of
  the `.github` half is already applied** in the working tree (SKILL leaned, 2 refs `D`);
  the remaining Build work is the 2 `ai.ingest/` JSONs.
- **Validation** —
  - `grep -nE "claude install|--watch|/graphify add|commit hook" <SKILL>` → only the
    negated framing mention; Usage block clean
  - `add-watch.md` + `hooks.md` gone; retained 3 refs still linked; no dangling links
  - both JSONs parse strict JSON; lock `adaptation.asset_hashes` keys == live
    `punch-graphify/*.md` (4: SKILL, extraction-spec, query, update); descriptor
    `expected_absent_references` lists 5 (`exports`, `github-and-merge`, `transcribe`,
    `add-watch`, `hooks`)
  - `python3 ai.ingest/compare.py graphify` exit 0, **no `drift detected`** in output
  - **`python3 -m unittest discover -s ai.ingest/tests` PASSES** (the gate the prior
    split failed)
- **Rollback** — `git checkout .github/skills/punch-graphify/ ai.ingest/`
- **Human checkpoint** — required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

### GR-02 — dedupe the drift pointer (Review follow-up 1)
- **Goal** — in `/punch-document` pre-conditions, replace the restated `compare.py graphify`
  guidance with a pointer to the Context Engineering gate's drift line (single source);
  keep it optional + read-only + non-blocking.
- **Allowed edit paths** — `.github/prompts/punch-document.prompt.md`
- **Read-only context paths** — `.github/skills/punch-context-engineering/SKILL.md`,
  `ai.ingest/README.md`
- **Forbidden paths** — everything else; explicitly other prompts/skills/agents,
  `ai.ingest/**`, runtime layers
- **Expected diff size** — ~ −3 net (collapse to a pointer)
- **Validation** — pre-condition still names the optional read-only drift check but defers
  detail to the gate; `grep -c "compare.py graphify" .github/prompts/punch-document.prompt.md`
  ≤1; link to the gate resolves; `unittest` still passes; audit clean
- **Rollback** — `git checkout .github/prompts/punch-document.prompt.md`
- **Human checkpoint** — required before Build
- **Build prompt** — `punch-build` (`punch-ai-governance`)

---

## Order of execution

GR-01 (atomic, ends green) → GR-02 (independent, green on its own). No `/test` is run
**inside** GR-01 — the suite is validated **once, at GR-01 completion**, after the lock
truth-up; that is the rev-2 fix. Not a runtime change — k6→compose→orchestrator order
does not apply (governance/host-tooling off the execution chain).

---

## Cross-cutting risks + constraints

- **Green-at-every-boundary (the rev-2 lesson).** Coupled metadata + asset changes ship in
  one task; never `/test` a half-applied leaned-fork. Reviewer confirms `compare` reports
  the drops as `intentional-absent` and `unittest` is green at GR-01 close.
- **Care-zone edit.** `punch-graphify` is adopted upstream (refresh-preferred). GR-01
  deepens the *intentional* leaned-fork; the recorded baseline moves with it.
- **No new tooling.** `compare.py` unchanged; hashes stay `null`; no `adopt`/apply built.
- **Non-goals preserved.** No hooks installed (we *remove* the hook docs); no MCP;
  Build/Test/Review/Ship/Spec prompts untouched; no broad framework change.
- **Pristine snapshot untouched.** `.ai-upstream/graphify/` (still all 8 refs) is the
  drift baseline — read-only; the lean is recorded as intentional in the descriptor.
  Upstream-axis keys for the 2 refs stay (upstream still has them) → `baseline-not-recorded`,
  not drift.
- **Not Punch run evidence.** Test = grep + strict-JSON parse + `compare` + unittest +
  audit, not a k6 run; `reports/state/punch-run.json` unaffected.

---

## Rollback plan

Per-task `git checkout` of the named paths. GR-01 deletes two tracked files — `git
checkout` restores them; the two JSONs revert in the same command. No runtime artifact.

**Gate:** approved when human confirms the atomic GR-01 (incl. the 5-file waiver) → Build
GR-01, validate green, then GR-02.
