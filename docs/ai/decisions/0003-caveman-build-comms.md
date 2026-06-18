# ADR 0003 — Caveman for concise assistant-prose comms (Build+Test enforced, agent-privileged)

**Status:** Accepted (2026-06-18) · **revised 2026-06-18** (Revisions 1–3 below —
the canonical Copilot installer was run, scope was broadened, and a project-wide
per-phase Caveman Canon was adopted per owner direction; the original Decision
section is kept for the record but is superseded where it conflicts, latest
revision wins).
**Deciders:** repository owner + Punch AI Governance work

## Context

Punch wants a way to reduce assistant *prose* noise during the **Build** phase —
shorter implementation updates, sub-agent handoffs, and post-evidence debugging
summaries — without ever touching technical evidence.
[Caveman](https://github.com/JuliusBrussee/caveman) is an upstream Agent Skill
that compresses prose (~75% token cut) with intensity modes `lite` / `full` /
`ultra`, while keeping code, errors, and technical terms verbatim.

This is a **communication/token-efficiency utility**, not runtime behavior. It
must not become global across the lifecycle: Spec, Plan, Verify, Review, Ship,
Governance, and architecture reasoning keep normal prose by default.

## What the official installer does (and why it is unsafe for Punch)

The official Copilot install path was dry-run on 2026-06-18:

```
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash -s -- --only copilot --with-init --dry-run
```

It reported two actions:

1. `npx -y skills add JuliusBrussee/caveman --skill * -a github-copilot --yes`
   — installs **all** Caveman skills globally for `github-copilot`.
2. `caveman-init.js --with-init` — **appends** an always-on activation rule to
   the existing `.github/copilot-instructions.md` (verified `mode: 'append'`),
   and writes a parallel multi-agent rule set (`.cursor/`, `.windsurf/`,
   `.clinerules/`, `.opencode/AGENTS.md`, root `AGENTS.md`).

For Punch this is unsafe because it would (a) make Caveman **global/always-on**
rather than Build-scoped, (b) mutate Punch's authored **Critical Rules** file and
weaken governance precedence, (c) add a **parallel structure** the project layout
forbids, and (d) install host hooks/statusline outside the Docker-First surface.
INSTALL.md's documented Copilot path (`npx -y github:JuliusBrussee/caveman --
--only copilot --with-init`) resolves to the same two actions.

## Decision

Adopt Caveman as a **Build-only, default-on prose adapter** — reuse the *style*,
do **not** run the official installer:

- **Authored adapter, scoped to Build.** A Punch-authored skill
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)
  reproduces the Caveman style and pins Punch evidence-preservation rules. It is
  referenced only from the `punch-build` prompt and its engineers — never from
  other phase prompts or the always-on Critical Rules.
- **Pristine provenance.** A verbatim upstream snapshot lives in
  [`.ai-upstream/caveman/`](../../../.ai-upstream/caveman/UPSTREAM.md) (frozen,
  do-not-edit), diffed against on upgrade. Mirrors the
  [graphify](0002-graphify-host-tool.md) adoption pattern.
- **No installer side effects.** No global `skills add`, no
  `$CLAUDE_CONFIG_DIR` hooks/statusline, no `--with-mcp-shrink`, no parallel
  `.cursor`/`.windsurf`/`.clinerules`/`.opencode` rule files, no append to
  `.github/copilot-instructions.md` Critical Rules. The optional Copilot pointer
  is a clearly-marked **Build-only** section below the Critical Rules, not an
  always-on global rule.
- **Default-on in Build at `full`.** Build runs Caveman by default at `full`;
  allowed `lite` / `full` / `ultra`; `stop caveman` / `normal mode` reverts.
  (Initial adoption defaulted to `lite`/opt-in; revised 2026-06-18 to default
  `full` in Build per owner direction — evidence-preservation rules unchanged.)
- **Evidence is sacred.** Caveman compresses assistant prose only; it never
  compresses or rewrites technical evidence. The canonical never-compress list is
  maintained in
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)
  (§Evidence preservation).
- **Priority order.** Correctness > observable evidence > Build maintainability >
  Copilot compatibility > brevity > Caveman style. If brevity harms correctness,
  stop Caveman.
- **Governed.** `punch-ai-governance` owns refresh and drift; the adapter is
  registered in [`docs/ai/skill-registry.md`](../skill-registry.md).

## Revision (2026-06-18) — canonical Copilot install + broadened scope

Per owner direction, the original "do not run the installer / Build-only" stance
above is **superseded**:

- **Canonical install, run and scoped to Copilot.** The official installer was
  executed: `curl -fsSL …/install.sh | bash -s -- --only copilot --with-init`.
  It placed the upstream skill pack under `.agents/skills/`, ran
  `npx skills add … -a github-copilot`, and (because `install.sh` does **not**
  forward `--only` to `caveman-init`) also wrote non-Copilot rule files and
  appended to `AGENTS.md` + `.github/copilot-instructions.md`.
- **Scoped down to Copilot afterward.** The non-Copilot artifacts
  (`.cursor/`, `.windsurf/`, `.clinerules/`, `.opencode/`) were **deleted**; the
  `AGENTS.md` raw append was reverted and replaced with a Punch-voiced note; the
  two duplicated blocks in `copilot-instructions.md` were merged into one
  canonical, Critical-Rules-respecting section. The skill pack was **trimmed to
  the core `caveman` skill** (`.agents/skills/caveman/`), dropping the auxiliary
  packs — including `caveman-compress`, which ships host Python scripts that
  conflict with Punch's Docker-First / stdlib-only minimalism. `skills-lock.json`
  was removed.
- **Scope broadened.** Caveman is now **enforced (default-on `full`) for the whole
  Build phase** (prompt + dispatcher + engineers) and **privileged across all
  agents** in `.github/agents/` — builder family enforced, the rest privilege it
  for routine prose but **lead with normal prose** for judgment-heavy work
  (specs, plans, reviews, risk, governance, architecture, security). All agents
  keep their existing capabilities, tools, scope, and guards.
- **Unchanged invariants.** Evidence is still never compressed; Auto-Clarity stop
  conditions still apply; the Critical Rules still take precedence; the
  Docker-First execution chain is untouched. The canonical upstream skill
  (`.agents/skills/caveman/`) is adopted-upstream — exempt from authored-canon
  checks; the Punch adapter `punch-build-caveman` remains authored and checked.

## Revision 2 (2026-06-18) — single-source + ultra/wenyan tiering + Test

Per owner direction and the `/enhance` lean pass:

- **Single source.** `.github/skills/punch-build-caveman/SKILL.md` is now the
  **canonical** Caveman policy. The prompts, the 9 agents, and
  `copilot-instructions.md` were collapsed to one-line pointers (the ~11-line block
  was byte-for-byte duplicated across all 9 agents). The full rules — tiers, modes,
  evidence list, Auto-Clarity — live only in the SKILL.
- **Scope Build → Build + Test.** Caveman is now enforced in **both** `/punch-build`
  and `/punch-test`; `/punch-test` gained an Operating-comms section.
- **Two operating tiers.** Governance/orchestration voice (`punch-build` &
  `punch-test` prompts + `punch-builder` dispatcher) defaults to **`ultra`**;
  build/test **execution** sub-agents (`punch-runtime-engineer`,
  `punch-performance-test-engineer`, `punch-verifier`) run **`wenyan`** (maximum
  efficiency; `allowed_modes` now includes the `wenyan-lite|full|ultra` family).
- **Unchanged invariants.** Evidence is never compressed (in any mode, including
  `wenyan` — only the surrounding prose is terse/classical); Auto-Clarity stop
  conditions hold; Critical Rules take precedence; the execution chain is untouched.

## Revision 3 (2026-06-18) — Punch Caveman Canon (project default + per-phase levels)

Per owner direction, Caveman becomes a **project-wide output-efficiency canon**
rather than a Build/Test-only enforcement. Reconciled in place — the official
Copilot installer was **not** re-run (it would re-create the forbidden parallel
rule files and re-append duplicate blocks); the existing
`.agents/skills/caveman/` install is reused.

- **Project default `lite`.** Set repo-wide in `copilot-instructions.md`. Each
  lifecycle phase overrides it.
- **Per-phase canon.** Document `lite` (persistent docs; `ultra` status-only) ·
  Spec `lite` · Plan `full` · Build `ultra` · Test `ultra` · Review `full` ·
  Ship `full` · Verify `lite` prose (run output verbatim). Build + Test remain
  the **enforced** phases (voice `ultra`, execution sub-agents `wenyan`).
- **Sub-agent reports `wenyan`-compatible at every level** — preserving exact
  paths, commands, exit codes, artifacts, pass/fail status, blockers, and next
  action verbatim.
- **Wenyan forbidden in persistent artifacts** — docs, ADRs, specs, plans,
  context maps, skills, prompts, registries, handoffs, and `reports/**` use only
  `lite`/`full`; `ultra` is status-/terminal-only. Wenyan is sub-agent-report only.
- **Delegation depth — output-only separation.** Caveman governs output style,
  never tools/access/assignments (rule preserved: custom agents still own those).
  Canon allows depth-1 plus **depth-2 lazy-non-first**; depth-3+ forbidden. Punch
  implements the strict end (depth-1; engineers leaf `agents: []`;
  `chat.subagents.allowInvocationsFromSubagents` off) — depth-2-lazy is the canon
  ceiling, not enabled.
- **Slash-command mapping, no renames.** Existing `punch-*` prompt filenames are
  unchanged; they map to the Addy-Osmani lifecycle commands `/spec /plan /build
  /test /review /ship` plus Punch's `/document` (mapping table in
  [`punch-build-caveman`](../../../.github/skills/punch-build-caveman/SKILL.md)).
- **GitHub Copilot First preserved.** No optimization for Claude Code / Cursor /
  Windsurf; single-source policy stays in `.github/skills/punch-build-caveman/`,
  prompts/agents/`copilot-instructions.md`/`AGENTS.md` carry only lean pointers.
- **Unchanged invariants.** Evidence never compressed; Auto-Clarity stop
  conditions hold; Critical Rules take precedence; the execution chain is
  untouched; agent tools/scope/guards unchanged.

## Consequences

- **Positive:** Build prose gets terser by default with zero risk to evidence;
  Caveman is available repo-wide for routine prose. Nothing in the source →
  bundle → image → run → report chain changes.
- **Negative / watch:** the adapter is hand-authored, so an upstream Caveman
  change must be reconciled manually (see `.ai-upstream/caveman/UPSTREAM.md`
  *Updating*). Any Caveman activation **outside** Build, or any compression of
  technical evidence, is **drift** and a Review failure.
- **Guardrail:** Caveman follows the **per-phase canon** (Revision 3) — project
  default `lite`, Build/Test enforced (`ultra`/`wenyan`), Plan/Review/Ship `full`,
  Spec/Document `lite`. Non-Build/Test agents lead with normal prose for
  judgment-heavy work and invoke Auto-Clarity for security / irreversible /
  ambiguous / architecture-tradeoff content. Always overridable (`stop caveman`).
  Evidence is never compressed; **Wenyan in a persistent artifact**, compression
  of evidence, depth-3+ delegation, or loss of an agent's constraints is **drift**
  and a Review failure.
