# ADR 0003 — Caveman as a Build-only assistant-prose compression adapter

**Status:** Accepted (2026-06-18)
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

Adopt Caveman as a **Build-only, opt-in prose adapter** — reuse the *style*, do
**not** run the official installer:

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
- **Default `lite`.** Allowed `lite` / `full` / `ultra`; `full`/`ultra` only on
  explicit low-risk request.
- **Evidence is sacred.** Caveman compresses assistant prose only. It never
  compresses or rewrites code, commands, paths, Python orchestration details,
  Docker Compose output, k6 output, JSON/YAML/CSV, logs, stack traces, errors,
  exit codes, test evidence, acceptance criteria, or risk notes.
- **Priority order.** Correctness > observable evidence > Build maintainability >
  Copilot compatibility > brevity > Caveman style. If brevity harms correctness,
  stop Caveman.
- **Governed.** `punch-ai-governance` owns refresh and drift; the adapter is
  registered in [`docs/ai/skill-registry.md`](../skill-registry.md).

## Consequences

- **Positive:** Build prose gets terser on demand with zero risk to evidence; no
  host runtime, no global activation, no parallel structure, no governance
  erosion. Nothing in the source → bundle → image → run → report chain changes.
- **Negative / watch:** the adapter is hand-authored, so an upstream Caveman
  change must be reconciled manually (see `.ai-upstream/caveman/UPSTREAM.md`
  *Updating*). Any Caveman activation **outside** Build, or any compression of
  technical evidence, is **drift** and a Review failure.
- **Guardrail:** Caveman is never mandatory and never default-on. It is a Build
  convenience only; other lifecycle phases answer in normal prose.
