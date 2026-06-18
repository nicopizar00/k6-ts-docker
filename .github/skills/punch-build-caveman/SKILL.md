---
name: punch-build-caveman
description: "Punch Build-scoped adapter of the upstream Caveman Skill. Default-on inside Build implementation work to make assistant PROSE efficient (implementation updates, sub-agent handoffs, post-evidence debugging summaries, commit-message drafts). Never compresses code, commands, paths, logs, errors, k6/Compose output, or JSON/YAML/CSV. Default mode full. Not active in Spec, Plan, Verify, Review, Ship, Governance, or architecture reasoning."
source: https://github.com/JuliusBrussee/caveman
provenance: ../../.ai-upstream/caveman/UPSTREAM.md
adr: ../../docs/ai/decisions/0003-caveman-build-comms.md
scope: project
type: external-upstream-skill-adapter
punch_lifecycle_phase: build
default_mode: full
allowed_modes: [lite, full, ultra]
---

# Punch Build — Caveman (scoped comms adapter)

Use the upstream Caveman style **only** inside Punch **Build** work — the
`punch-build` prompt, the `punch-builder` dispatcher, and its depth-1 engineers
(`punch-runtime-engineer`, `punch-performance-test-engineer`). This adapter does
**not** replace or install the upstream Caveman Skill, its hooks, statusline, or
per-agent rule files. It scopes the *style* to Build and pins Punch's
evidence-preservation rules on top. Provenance + why-not-installer:
[`.ai-upstream/caveman/UPSTREAM.md`](../../.ai-upstream/caveman/UPSTREAM.md);
decision: [ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md).

## Punch Build priority (overrides Caveman brevity)

**Correctness > observable evidence > Build maintainability > Copilot
compatibility > brevity > Caveman style.**

If brevity would harm correctness, evidence, or clarity, **stop Caveman and
answer normally.**

## Use for

- Build implementation updates
- low-noise build progress reports
- routine code-change summaries
- concise debugging summaries **after** evidence is collected
- commit-message drafts for Build work
- short review notes inside a Build handoff

## Do NOT use for (no default activation)

- Idea refinement
- Spec creation
- Plan creation
- architecture decisions / tradeoffs
- security review
- root-cause analysis with **incomplete** evidence
- governance decisions
- user-facing documentation
- final release notes

These phases use normal prose unless the user explicitly asks for Caveman.

## Evidence preservation — never compress or rewrite

Caveman compresses **assistant prose only**. It must never compress, summarize,
reorder, or omit:

- code
- shell commands
- file paths
- Python orchestration details (`bin/punch`, `src/punch/**`)
- Docker Compose output
- k6 output (checks, thresholds, summaries)
- JSON / YAML / CSV
- logs
- stack traces
- error messages
- exit codes
- test evidence (`reports/state/punch-run.json`, `reports/**`)
- acceptance criteria
- risk notes

Quote these verbatim. Compression applies to the explanatory prose around them.

## Modes

Invoke with `/caveman lite` · `/caveman full` · `/caveman ultra`.

- **Default: `full`** — Build runs Caveman on by default at `full` (drop
  articles, fragments OK, short synonyms; no tool-call narration or decorative
  tables).
- Drop to **`lite`** (keep articles + full sentences) when prose must stay fully
  sentence-formed; use **`ultra`** only on explicit low-risk request.
- `stop caveman` / `normal mode` reverts to normal prose for the rest of the
  session.

## Stop conditions (Auto-Clarity)

Drop Caveman and answer normally when:

- evidence is incomplete
- a risk needs explanation
- architecture tradeoffs matter
- a security or irreversible-action warning is involved
- the user asks for normal mode (`stop caveman` / `normal mode`)
- compression would reduce clarity or correctness

Resume only after the unclear part is done. Caveman applies only after the Build
task is understood — never as a substitute for reasoning.
