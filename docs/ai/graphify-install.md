# Graphify — install, security, version, and sharing policy

Native, upstream Graphify Agent Skill
([`.github/skills/graphify/`](../../.github/skills/graphify/SKILL.md)) —
adopted as-is, no Punch fork. `/graphify` explicit-only; never auto-loaded,
never gated behind another Punch prompt.

## Install (mandatory manual step)

```bash
uv tool install graphifyy==0.8.41
```

Pinned version tracked in
[`.github/skills/graphify/.graphify_version`](../../.github/skills/graphify/.graphify_version).
No Punch prompt runs this — a one-time human/contributor step, same scoped
host-tool exception as [ADR 0002](decisions/0002-graphify-host-tool.md).

Upgrade: `uv tool install --upgrade graphifyy`. Fallback: `pip install graphifyy`.

## Other agents (Claude Code, Codex, generic MCP-capable agents)

Native Graphify ships its own documented per-platform installers. Punch does
**not** run or commit any of them — install decisions and personal-scope
config stay with whoever runs them, on their own machine. Do not commit
`.claude/`, `.codex/`, or any other personal-scope install output.

## Version check (warning-only) and CLI-missing behavior (observed)

If `graphify --version` is available, compare it to `.graphify_version`.
Missing marker file or version mismatch → **warning only**, never a block;
Punch work continues without Graphify.

Missing CLI is **not** purely passive: the native skill's own documented
procedure (committed verbatim in `.github/skills/graphify/SKILL.md`) tries
to self-install — creating a local `.graphify-venv/` and `pip install
graphifyy` into it — rather than only printing the manual-install command
and stopping. Observed directly (2026-07-18): a real `/graphify` run with no
CLI on `PATH` created `.graphify-venv/` unattended, then proceeded with a
real extraction. This is upstream's own fallback, not a Punch-added
behavior; it runs entirely locally (no cloud call), the venv is
self-gitignored (Python's `venv` module writes its own `.gitignore` inside
itself), and it still stopped and asked before using any cloud semantic
backend (Gemini/Google API key) for doc/paper/image extraction. Running
`uv tool install graphifyy==0.8.41` (above) first remains the recommended,
pinned, explicit install — it avoids the unpinned ad-hoc venv fallback.

## Security policy

- `/graphify` is **explicit-only** — invoke it directly, never auto-triggered
  by any Punch prompt or agent.
- Terminal commands stay **approval-gated**, same as every other command in
  this repo. No standing shell pre-approval for `graphify`.
- **Local-first by default.** No hooks, watchers, MCP server, URL ingestion
  (`graphify add <url>`), cloud semantic backends, or external
  graph-database push (Neo4j/FalkorDB) run automatically. Each requires its
  own explicit, separate user decision — never bundled into a Punch prompt.
- `graphify *install` (any platform) stays forbidden-by-default in Punch
  flows — see [ADR 0002](decisions/0002-graphify-host-tool.md) (the "Native
  install/registration — investigated, rejected" section: a prior
  investigation found it rewrites `.github/copilot-instructions.md`
  destructively by heading-name match).

## `.graphifyignore`

Excludes obvious sensitive/noisy patterns from the shared corpus by default
(build output, `node_modules/`, `.venv/`, media files, lockfiles). Media
types (`*.pdf`, `*.png`, `*.docx`, etc.) are **deferred, not forbidden** — a
user may explicitly remove a line to opt a file type into the graph. Changes
to `.graphifyignore` go through a `punch-ai-governance` pass — it controls
what enters the shared, committed graph.

## Shared baseline (what's tracked)

Two-tier `graphify-out/` policy — local-only state plus a narrow committed
allowlist:

| File | Status |
|---|---|
| `graphify-out/graph.json` | Committed (after validation) — shared team query baseline |
| `graphify-out/GRAPH_REPORT.md` | Committed (after validation) — human-readable audit trail |
| `.graphifyignore` | Committed — shared corpus filter |
| Everything else under `graphify-out/` | Gitignored, local-only |
| Nested/renamed `graphify-out*/` dirs | Gitignored + CI-blocked |

Full allowlist mechanics live in `.gitignore` (wildcard rules + `!` negation
for the two canonical files).

## Validation gate (required before every commit of the shared baseline)

```bash
python3 ai.ingest/validate_graphify_share.py
```

Six checks (ADR 0002, Team Sharing): no absolute paths, no venv/interpreter
paths, no hostname strings, `graph.json` parses as valid JSON, all node IDs
relative, no raw cost/token keys. `punch-ai-governance` sign-off required
before committing an update to the shared graph.

## Staleness

A stale graph (predates a structural change) **warns and remains usable as
evidence** — it never blocks orientation or any Punch lifecycle phase.
Refresh manually:

```bash
/graphify . --update   # routine changes
/graphify .             # structural changes
```

No Punch hook, watcher, or automatic refresh triggers either command —
always a manual, native, explicit invocation.
