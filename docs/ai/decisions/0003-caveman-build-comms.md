# ADR 0003 — Caveman for concise assistant-prose comms (Build+Test enforced, agent-privileged)

**Status:** Accepted (2026-06-18) · **revised 2026-06-18** (Revisions 1–3 below —
canonical Copilot installer run, scope broadened, project-wide per-phase Caveman
Canon adopted per owner direction; original Decision section kept for record but
superseded where conflicts, latest revision wins).
**Deciders:** repository owner + Punch AI Governance work

## Context

Punch want way to cut assistant *prose* noise during **Build** phase — shorter
implementation updates, sub-agent handoffs, post-evidence debugging summaries —
never touch technical evidence.
[Caveman](https://github.com/JuliusBrussee/caveman) = upstream Agent Skill,
compress prose (~75% token cut), intensity modes `lite` / `full` / `ultra`, keep
code/errors/technical terms verbatim.

This = **communication/token-efficiency utility**, not runtime behavior. Must not
go global across lifecycle: Spec, Plan, Verify, Review, Ship, Governance, and
architecture reasoning keep normal prose by default.

## What the official installer does (and why it is unsafe for Punch)

Official Copilot install path dry-run on 2026-06-18:

```
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash -s -- --only copilot --with-init --dry-run
```

Reported two actions:

1. `npx -y skills add JuliusBrussee/caveman --skill * -a github-copilot --yes`
   — installs **all** Caveman skills globally for `github-copilot`.
2. `caveman-init.js --with-init` — **appends** always-on activation rule to
   existing `.github/copilot-instructions.md` (verified `mode: 'append'`), and
   writes parallel multi-agent rule set (`.cursor/`, `.windsurf/`,
   `.clinerules/`, `.opencode/AGENTS.md`, root `AGENTS.md`).

Unsafe for Punch — would (a) make Caveman **global/always-on** not Build-scoped,
(b) mutate Punch-authored **Critical Rules** file + weaken governance precedence,
(c) add **parallel structure** project layout forbids, (d) install host
hooks/statusline outside Docker-First surface. INSTALL.md's documented Copilot
path (`npx -y github:JuliusBrussee/caveman --
--only copilot --with-init`)
resolves to same two actions.

## Decision

Adopt Caveman as **Build-only, default-on prose adapter** — reuse *style*, do
**not** run official installer:

- **Authored adapter, scoped to Build.** Punch-authored skill
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)
  reproduces Caveman style + pins Punch evidence-preservation rules. Referenced
  only from `punch-build` prompt + its engineers — never other phase prompts or
  always-on Critical Rules.
- **Pristine provenance.** Verbatim upstream snapshot in
  [`.ai-upstream/caveman/`](../../../.ai-upstream/caveman/UPSTREAM.md) (frozen,
  do-not-edit), diffed on upgrade. Mirrors
  [graphify](0002-graphify-host-tool.md) adoption pattern.
- **No installer side effects.** No global `skills add`, no
  `$CLAUDE_CONFIG_DIR` hooks/statusline, no `--with-mcp-shrink`, no parallel
  `.cursor`/`.windsurf`/`.clinerules`/`.opencode` rule files, no append to
  `.github/copilot-instructions.md` Critical Rules. Optional Copilot pointer =
  clearly-marked **Build-only** section below Critical Rules, not always-on
  global rule.
- **Default-on in Build at `full`.** Build runs Caveman by default at `full`;
  allowed `lite` / `full` / `ultra`; `stop caveman` / `normal mode` reverts.
  (Initial adoption defaulted `lite`/opt-in; revised 2026-06-18 to default
  `full` in Build per owner direction — evidence-preservation rules unchanged.)
- **Evidence is sacred.** Caveman compresses assistant prose only; never
  compresses/rewrites technical evidence. Canonical never-compress list in
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)
  (§Evidence preservation).
- **Priority order.** Correctness > observable evidence > Build maintainability >
  Copilot compatibility > brevity > Caveman style. If brevity harms correctness,
  stop Caveman.
- **Governed.** `punch-ai-governance` owns refresh + drift; adapter registered in
  [`docs/ai/skill-registry.md`](../skill-registry.md).

## Revision (2026-06-18) — canonical Copilot install + broadened scope

Per owner direction, original "do not run installer / Build-only" stance above
**superseded**:

- **Canonical install, run and scoped to Copilot.** Official installer executed:
  `curl -fsSL …/install.sh | bash -s -- --only copilot --with-init`. Placed
  upstream skill pack under `.agents/skills/`, ran
  `npx skills add … -a github-copilot`, and (because `install.sh` does **not**
  forward `--only` to `caveman-init`) also wrote non-Copilot rule files +
  appended to `AGENTS.md` + `.github/copilot-instructions.md`.
- **Scoped down to Copilot afterward.** Non-Copilot artifacts (`.cursor/`,
  `.windsurf/`, `.clinerules/`, `.opencode/`) **deleted**; `AGENTS.md` raw append
  reverted + replaced with Punch-voiced note; two duplicated blocks in
  `copilot-instructions.md` merged into one canonical, Critical-Rules-respecting
  section. Skill pack **trimmed to core `caveman` skill**
  (`.agents/skills/caveman/`), dropping auxiliary packs — including
  `caveman-compress`, which ships host Python scripts conflicting with Punch's
  Docker-First / stdlib-only minimalism. `skills-lock.json` removed.
- **Scope broadened.** Caveman now **enforced (default-on `full`) for whole Build
  phase** (prompt + dispatcher + engineers) and **privileged across all agents**
  in `.github/agents/` — builder family enforced, rest privilege it for routine
  prose but **lead with normal prose** for judgment-heavy work (specs, plans,
  reviews, risk, governance, architecture, security). All agents keep existing
  capabilities, tools, scope, guards.
- **Unchanged invariants.** Evidence still never compressed; Auto-Clarity stop
  conditions still apply; Critical Rules still take precedence; Docker-First
  execution chain untouched. Canonical upstream skill (`.agents/skills/caveman/`)
  = adopted-upstream — exempt from authored-canon checks; Punch adapter
  `punch-build-caveman` remains authored + checked.

## Revision 2 (2026-06-18) — single-source + ultra/wenyan tiering + Test

Per owner direction + `/enhance` lean pass:

- **Single source.** `.github/skills/punch-build-caveman/SKILL.md` now
  **canonical** Caveman policy. Prompts, 9 agents, `copilot-instructions.md`
  collapsed to one-line pointers (~11-line block was byte-for-byte duplicated
  across all 9 agents). Full rules — tiers, modes, evidence list, Auto-Clarity —
  live only in SKILL.
- **Scope Build → Build + Test.** Caveman now enforced in **both** `/punch-build`
  and `/punch-test`; `/punch-test` gained Operating-comms section.
- **Two operating tiers.** Governance/orchestration voice (`punch-build` &
  `punch-test` prompts + `punch-builder` dispatcher) defaults **`ultra`**;
  build/test **execution** sub-agents (`punch-runtime-engineer`,
  `punch-performance-test-engineer`, `punch-verifier`) run **`wenyan`** (max
  efficiency; `allowed_modes` now includes `wenyan-lite|full|ultra` family).
- **Unchanged invariants.** Evidence never compressed (any mode, including
  `wenyan` — only surrounding prose terse/classical); Auto-Clarity stop
  conditions hold; Critical Rules take precedence; execution chain untouched.

## Revision 3 (2026-06-18) — Punch Caveman Canon (project default + per-phase levels)

Per owner direction, Caveman becomes **project-wide output-efficiency canon**
not Build/Test-only enforcement. Reconciled in place — official Copilot installer
**not** re-run (would re-create forbidden parallel rule files + re-append
duplicate blocks); existing `.agents/skills/caveman/` install reused.

- **Project default `lite`.** Set repo-wide in `copilot-instructions.md`. Each
  lifecycle phase overrides.
- **Per-phase canon.** Document `lite` (persistent docs; `ultra` status-only) ·
  Spec `lite` · Plan `full` · Build `ultra` · Test `ultra` · Review `full` ·
  Ship `full` · Verify `lite` prose (run output verbatim). Build + Test stay
  **enforced** phases (voice `ultra`, execution sub-agents `wenyan`).
- **Sub-agent reports `wenyan`-compatible at every level** — preserve exact
  paths, commands, exit codes, artifacts, pass/fail status, blockers, next action
  verbatim.
- **Wenyan forbidden in persistent artifacts** — docs, ADRs, specs, plans,
  context maps, skills, prompts, registries, handoffs, `reports/**` use only
  `lite`/`full`; `ultra` is status-/terminal-only. Wenyan = sub-agent-report only.
- **Delegation depth — output-only separation.** Caveman governs output style,
  never tools/access/assignments (rule preserved: custom agents still own those).
  Canon allows depth-1 plus **depth-2 lazy-non-first**; depth-3+ forbidden. Punch
  implements strict end (depth-1; engineers leaf `agents: []`;
  `chat.subagents.allowInvocationsFromSubagents` off) — depth-2-lazy = canon
  ceiling, not enabled.
- **Slash-command mapping, no renames.** Existing `punch-*` prompt filenames
  unchanged; map to Addy-Osmani lifecycle commands `/spec /plan /build
  /test /review /ship` plus Punch's `/document` (mapping table in
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)).
- **GitHub Copilot First preserved.** No optimization for Claude Code / Cursor /
  Windsurf; single-source policy stays in `.github/skills/punch-build-caveman/`,
  prompts/agents/`copilot-instructions.md`/`AGENTS.md` carry only lean pointers.
- **Unchanged invariants.** Evidence never compressed; Auto-Clarity stop
  conditions hold; Critical Rules take precedence; execution chain untouched;
  agent tools/scope/guards unchanged.

## Consequences

- **Positive:** Build prose terser by default, zero risk to evidence; Caveman
  available repo-wide for routine prose. Nothing in source → bundle → image →
  run → report chain changes.
- **Negative / watch:** adapter hand-authored, so upstream Caveman change must be
  reconciled manually (see `.ai-upstream/caveman/UPSTREAM.md` *Updating*). Any
  Caveman activation **outside** Build, or any compression of technical evidence,
  = **drift** + Review failure.
- **Guardrail:** Caveman follows **per-phase canon** (Revision 3) — project
  default `lite`, Build/Test enforced (`ultra`/`wenyan`), Plan/Review/Ship `full`,
  Spec/Document `lite`. Non-Build/Test agents lead with normal prose for
  judgment-heavy work + invoke Auto-Clarity for security / irreversible /
  ambiguous / architecture-tradeoff content. Always overridable (`stop caveman`).
  Evidence never compressed; **Wenyan in persistent artifact**, compression of
  evidence, depth-3+ delegation, or loss of agent's constraints = **drift** +
  Review failure.
