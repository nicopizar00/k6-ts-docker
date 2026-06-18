---
name: punch-build-caveman
description: "Canonical Punch Caveman policy (single source). Enforced for the /punch-build and /punch-test phases: governance/orchestration voice default `ultra`, build/test EXECUTION sub-agents `wenyan` (max efficiency); privileged elsewhere. Compresses assistant PROSE only — never code, commands, paths, logs, errors, k6/Compose output, JSON/YAML/CSV, or run evidence. Other files link here instead of restating."
applies-to: lifecycle/Build+Test — assistant-prose communication (punch-build & punch-test prompts + punch-builder/punch-verifier + the engineers); not path-scoped
source: https://github.com/JuliusBrussee/caveman
provenance: ../../../.ai-upstream/caveman/UPSTREAM.md
adr: ../../../docs/ai/decisions/0003-caveman-build-comms.md
scope: project
type: external-upstream-skill-adapter
punch_lifecycle_phase: [build, test]
default_mode: ultra
allowed_modes: [lite, full, ultra, wenyan-lite, wenyan-full, wenyan-ultra]
---

# Punch — Caveman comms (canonical policy)

This is the **single source** for Caveman behavior in Punch. The prompts, agents,
and `copilot-instructions.md` **link here** and carry only their per-context delta —
they do not restate the rules below. Canonical upstream skill:
`.agents/skills/caveman/`. Provenance:
[`.ai-upstream/caveman/UPSTREAM.md`](../../../.ai-upstream/caveman/UPSTREAM.md);
decision: [ADR 0003](../../../docs/ai/decisions/0003-caveman-build-comms.md).

## Operating tiers (the mode policy)

Caveman is **enforced** in `/punch-build` and `/punch-test`. Two tiers:

| Tier | Who | Mode |
|---|---|---|
| Governance / orchestration | `punch-build` & `punch-test` prompts, `punch-builder` dispatcher | **`ultra`** (default) |
| Execution sub-agents | `punch-runtime-engineer`, `punch-performance-test-engineer` (build work), `punch-verifier` (test run/judge) | **`wenyan`** (max efficiency; max variant `wenyan-ultra`) |

Everywhere else (Spec, Plan, Review, Ship, Governance, architecture, docs):
**privileged** — lead with normal prose for judgment-heavy work, use Caveman only
for routine prose. `stop caveman` / `normal mode` reverts for the session.

Activation follows Agent Skills logic (`using-agent-skills`): state activation
**once** on entering the phase, then let the skill's persistence carry it — no
per-message re-invocation.

## Punch priority (overrides Caveman brevity)

**Correctness > observable evidence > maintainability > Copilot compatibility >
brevity > Caveman style.** If brevity would harm correctness, evidence, or clarity,
**stop Caveman and answer normally.** Apply Caveman only **after** the task is
understood — never as a substitute for reasoning.

## Evidence preservation — never compress or rewrite

Caveman compresses **assistant prose only**. It must never compress, summarize,
reorder, or omit:

- code · shell commands · file paths
- Python orchestration details (`bin/punch`, `src/punch/**`)
- Docker Compose output · k6 output (checks, thresholds, RED/GREEN summaries)
- JSON / YAML / CSV · logs · stack traces · error messages · exit codes
- test evidence (`reports/state/punch-run.json`, `reports/**`)
- acceptance criteria · risk notes

Quote these verbatim. Compression applies to the explanatory prose around them.
This holds in every mode, including `wenyan` — the prose may be terse/classical, the
evidence stays exact and readable.

## Modes

`/caveman lite | full | ultra | wenyan-lite | wenyan-full | wenyan-ultra`.

- `lite` — keep articles + full sentences. `full` — drop articles, fragments OK.
- **`ultra`** (Build/Test default) — abbreviate prose words only; never code
  symbols, API names, or error strings.
- `wenyan*` — classical-Chinese compression for the execution tier; maximum token
  efficiency. `wenyan-ultra` = max.

## Stop conditions (Auto-Clarity)

Drop Caveman to normal prose when: evidence is incomplete · a risk needs
explanation · architecture tradeoffs matter · a security or irreversible-action
warning is involved · the user asks for normal mode · compression would reduce
clarity or correctness. Resume after the unclear part is done.
