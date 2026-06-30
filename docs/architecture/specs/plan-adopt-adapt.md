# Plan — Adopt Adapt (graphify MVP)

> Pattern source: `.github/prompts/punch-plan.prompt.md` (Caveman `full`).
> Spec: [`adopt-adapt.md`](adopt-adapt.md) (approved) +
> increment [`adopt-adapt-compare.md`](adopt-adapt-compare.md) (approved) — unblocks A-02.

- **Goal** (from Spec): give the repo a local, inspectable index (lock + per-skill
  descriptor) recording what external skill was adopted, at what version, with
  baseline + adaptation asset-hash slots — graphify the only adopted skill in MVP.

## Scope note — domain tag + Spec boundary

- Work falls **outside** standard Build domains (O/C/K/B/D). New host-tooling /
  governance-adjacent artifact set owning only `ai.ingest/`. Tag prefix **`A`**
  (Adopt-ingest). Justified deviation — no existing domain owns `ai.ingest/`.
- **Spec boundary.** Base Spec is data-model only. The approved increment
  [`adopt-adapt-compare.md`](adopt-adapt-compare.md) brings the read-only `compare`
  CLI in-scope → **A-02 is now buildable**. A-03+ stay fenced behind their own
  increments.

## Tasks

### A-01 — Finalize + verify the `ai.ingest/` data-model seed

- **Goal** — promote the seeded `ai.ingest/` files (lock + descriptor + README) to
  the committed data-model deliverable and prove they meet Spec acceptance criteria
  1–7.
- **Allowed edit paths** — `ai.ingest/**`
- **Read-only context paths** — `.ai-upstream/graphify/**`,
  `.github/skills/punch-graphify/**`, `docs/ai/decisions/0002-graphify-host-tool.md`,
  `docs/architecture/specs/adopt-adapt.md`, `.github/.ai-upstream/README.md`
- **Forbidden paths** — `src/**`, `docker/**`, `bin/**`, `docker-compose.yml`,
  `package.json`, `tsconfig.json`, `.github/**`, `docs/ai/**`, `.gitignore`,
  `reports/**`, `.ai-upstream/**`, `graphify-out/**`
- **Expected diff size** — ~0–20 lines (files already seeded; only field/typo
  corrections if verification surfaces a mismatch).
- **Validation commands** — host structural checks (off the execution chain; **no
  `./bin/punch` runtime run** — docs/config-only, mirrors the lean-ai-config spec):
  ```
  python3 -c "import json; json.load(open('ai.ingest/adopt.lock.json'))"
  python3 -c "import json; json.load(open('ai.ingest/adapters/graphify.json'))"
  # AC2: hash-slot sets match filesystem
  diff <(python3 -c "import json;print('\n'.join(sorted(json.load(open('ai.ingest/adopt.lock.json'))['skills']['graphify']['upstream_snapshot']['asset_hashes'])))") \
       <( (cd .ai-upstream/graphify && ls SKILL.md .graphify_version; ls references/*.md | sed 's#^#references/#' | sed 's#references/references/#references/#') | sort )
  ls .ai-upstream/graphify/references/ | wc -l   # expect 8
  ls .github/skills/punch-graphify/references/ | wc -l   # expect 5
  git status --porcelain   # AC6: only ai.ingest/ + the two spec docs new
  ```
- **Rollback notes** — `ai.ingest/` is untracked; `rm -rf ai.ingest/` fully
  reverts. No other path touched.
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build` → **`punch-runtime-engineer`** (stdlib/host
  data files), with **`punch-ai-governance` review** (artifact set is AI-config
  adjacent and references `.github/` canon).

### A-02 — Read-only `compare` command  ✅ BUILDABLE (increment approved)

> Scoped by [`adopt-adapt-compare.md`](adopt-adapt-compare.md). Read-only,
> stdlib-only, zero mutation.

- **Goal** — a stdlib-Python read-only command (`python3 ai.ingest/compare.py
  [skill]`, default `graphify`) that loads `ai.ingest/adopt.lock.json` + the named
  adapter, probes/hashes live snapshot + adaptation assets, and prints the three
  drift axes (version / upstream-asset / adaptation) — **no writes, no mutation, no
  auto-apply**.
- **Allowed edit paths** — `ai.ingest/compare.py` (single new module). New helper
  files, if any, only under `ai.ingest/**` (no `ai.ingest/adopt.lock.json` or
  `ai.ingest/adapters/**` edits — those are read-only inputs).
- **Read-only context paths** — `ai.ingest/adopt.lock.json`,
  `ai.ingest/adapters/*.json`, `ai.ingest/README.md`, `.ai-upstream/graphify/**`,
  `.github/skills/punch-graphify/**`,
  `docs/architecture/specs/adopt-adapt-compare.md`
- **Forbidden paths** — all of A-01's forbidden list, **plus** *writing to*
  `ai.ingest/adopt.lock.json`, `ai.ingest/adapters/**`, `.ai-upstream/**`,
  `.github/**`, `graphify-out/**`. No pip deps; no Docker; no `bin/punch` wiring.
- **Expected diff size** — ~150–220 lines (one stdlib module: lock/adapter load,
  sha256 hashing per `track_globs`, three-axis report, degrade paths).
- **Validation commands** — host structural (off execution chain; **no
  `./bin/punch` run** — docs/tooling, mirrors A-01 + lean-ai-config). Maps to the
  increment's 8 acceptance criteria:
  ```
  # AC8: parses + stdlib-only (no third-party imports)
  python3 -c "import ast; ast.parse(open('ai.ingest/compare.py').read())"
  python3 - <<'PY'
  import ast; t=ast.parse(open('ai.ingest/compare.py').read())
  mods={n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module}
  mods|={a.name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names}
  std={'hashlib','json','pathlib','subprocess','argparse','sys','os','fnmatch','re'}
  assert mods<=std, f"non-stdlib import: {mods-std}"; print("stdlib-only OK")
  PY
  # AC1: read-only — git identical before/after
  B=$(git status --porcelain | sort)
  python3 ai.ingest/compare.py graphify
  A=$(git status --porcelain | sort); [ "$B" = "$A" ] && echo "AC1 read-only OK" || echo "AC1 FAIL: wrote files"
  # AC2: three axes + summary line present in output
  python3 ai.ingest/compare.py graphify | grep -Eqi 'version' && \
  python3 ai.ingest/compare.py graphify | grep -Eqi 'upstream' && \
  python3 ai.ingest/compare.py graphify | grep -Eqi 'adaptation' && echo "AC2 axes OK"
  # AC4: null baseline → baseline-not-recorded (not 'changed')
  python3 ai.ingest/compare.py graphify | grep -qi 'baseline-not-recorded' && echo "AC4 OK"
  # AC5: missing snapshot → missing-baseline, no crash (temp-rename baseline)
  #   run with .ai-upstream/graphify absent in a scratch check; expect 'missing-baseline'
  # AC3 (graphify absent → not-installed) + AC6/AC7 (intentional gaps suppressed,
  #   graphify-out never hashed) asserted by reading output + the hashing code path.
  ```
- **Rollback notes** — `rm ai.ingest/compare.py` fully reverts; inputs untouched
  (command never writes). No runtime/compose state.
- **Human checkpoint** — human approval required before Build.
- **Build prompt** — `punch-build` → **`punch-runtime-engineer`** (stdlib Python /
  host tooling), proof via `punch-test-driven-development` (RED→GREEN on the AC
  checks above). `punch-ai-governance` review (reads `.github/` canon, edits none).

### Future increments (not planned here — listed for roadmap only)

`verify` · `status` · `adopt` (snapshot + hash-population) · `plan`-report ·
`adapt --apply` (governance-gated mutation). Each needs its own Spec→Plan. No
generic adapter registry until graphify MVP validated.

## Order of execution

1. **A-01** — DONE (data-model seed verified, 7/7 AC).
2. **A-02** — buildable now (increment approved); independent of A-01's content,
   but A-01 must stay green (A-02 reads the lock + descriptor it finalized).

## Cross-cutting risks

- **Scope creep past the Spec.** Biggest risk; A-02+ are fenced behind Spec
  increments precisely to prevent it.
- **Gitignored baseline.** `.ai-upstream/` absent on fresh clone → A-01 verification
  diff (AC2) fails if run there. Mitigation: AC2 is meaningful only where the
  snapshot exists; the lock's `upstream_snapshot.present` flag carries the
  fresh-clone case. Note in A-01 verification, don't treat absence as a data error.
- **Hash slots stay `null`.** A-01 must **not** hand-populate hashes (AC5);
  population belongs to a future `adopt` task. Reviewer checks all slots null.
- **`.github/` canon untouched.** A-01 references but never edits Copilot canon;
  governance review confirms `git status` shows no `.github/` change.

## Rollback plan

Whole change is additive + untracked until committed: `rm -rf ai.ingest/` and
discard the two spec docs (`docs/architecture/specs/adopt-adapt.md`,
`plan-adopt-adapt.md`) fully reverts. No runtime, compose, or `.github/` state to
unwind.

**Gate:** approved when human confirms → Build per task ID. A-01 DONE; **A-02 is
the next buildable task**. A-03+ stay fenced behind their own Spec increments.
