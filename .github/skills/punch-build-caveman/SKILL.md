---
name: punch-build-caveman
description: "Canonical Punch Caveman policy (single source). Project default `lite`; per-phase canon — Document/Spec `lite`, Plan/Review/Ship `full`, Build/Test `ultra` (execution sub-agents `wenyan`). Wenyan is forbidden in persistent artifacts (docs/maps/registries/handoffs) — sub-agent reports only. Compresses assistant PROSE only — never code, commands, paths, logs, errors, exit codes, k6/Compose output, JSON/YAML/CSV, or run evidence. Other files link here instead of restating."
applies-to: lifecycle/Build+Test — assistant-prose communication (punch-build & punch-test prompts + punch-builder/punch-verifier + the engineers); not path-scoped
---

# Punch — Caveman comms (canonical policy)

This is the **single source** for Caveman behavior in Punch. The prompts, agents,
and `copilot-instructions.md` **link here** and carry only their per-context delta —
they do not restate the rules below.

**Adoption — external upstream skill adapter (project scope).** Adapted from
upstream [Caveman](https://github.com/JuliusBrussee/caveman); canonical install at
`.agents/skills/caveman/`; pristine snapshot + provenance in
[`.ai-upstream/caveman/UPSTREAM.md`](../../../.ai-upstream/caveman/UPSTREAM.md);
decision + governed scope in
[ADR 0003](../../../docs/ai/decisions/0003-caveman-build-comms.md). Lifecycle
phases: **Build + Test**. Default mode **`ultra`**; full mode list under
[Modes](#modes). (Adopt → filter → adapt: only `name`/`description`/`applies-to`
stay in frontmatter — the official Copilot SKILL schema — the rest lives here.)

## Caveman canon — per-phase levels (the mode policy)

Project default is **`lite`** (set repo-wide in `copilot-instructions.md`). Each
lifecycle phase overrides it with the level below; sub-agents at every level
return **wenyan-compatible** compact reports.

| Phase (Punch prompt) | Lifecycle cmd | Voice level | Sub-agent reports |
|---|---|---|---|
| Document (`punch-document`) | `/document` | **`lite`** for persistent docs; **`ultra` only for terminal/status** summaries | `wenyan` |
| Spec (`punch-spec`) | `/spec` | **`lite`** | `wenyan` |
| Plan (`punch-plan`) | `/plan` | **`full`** | `wenyan` |
| Build (`punch-build`) | `/build` | **`ultra`** | **`wenyan`** |
| Test (`punch-test`) | `/test` | **`ultra`** | **`wenyan`** |
| Review (`punch-review`) | `/review` | **`full`** | `wenyan` |
| Ship (`punch-ship`) | `/ship` | **`full`** | `wenyan` |
| Verify (`punch-verify`) | — (evidence companion to Test) | run output verbatim; surrounding prose **`lite`** | `wenyan` |

The Punch `punch-*` prompt filenames are not renamed; the *Lifecycle cmd* column
is the Addy-Osmani Agent-Skills command each maps to (compatibility, not a rename).
Build + Test remain the **enforced** phases (voice `ultra`, execution sub-agents
`wenyan`); the other phases lead with normal prose for judgment-heavy work and use
their level for routine prose. `stop caveman` / `normal mode` reverts for the session.

Activation follows Agent Skills logic (`using-agent-skills`): state activation
**once** on entering the phase, then let the skill's persistence carry it — no
per-message re-invocation.

## Delegation depth (Caveman is output-only)

Caveman governs **output style only** — never tool access, assignments, or which
sub-agents an agent may call; those stay with each custom agent and
[`agent-guards.md`](../../../docs/ai/agent-guards.md). Canon: coordinator → worker
is **depth-1**; **depth-2 is allowed only as lazy non-first** delegation (a level-1
worker may fork a level-2 worker *after* discovering a bounded technical subtask);
level-2 workers do **not** delegate; **depth-3+ is forbidden**. Punch implements the
strict end of this canon — VS Code `chat.subagents.allowInvocationsFromSubagents`
stays **off**, the two Build engineers are leaf (`agents: []`), so Punch runs
**depth-1 only**; depth-2-lazy is the canon ceiling, not enabled. The one sanctioned
1-deep fork is `/graphify` in Document mode. Every sub-agent report — at any depth —
is **wenyan-compatible** and preserves exact paths, commands, exit codes, artifacts,
pass/fail status, blockers, and next action verbatim.

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

## Persistent artifacts — never Wenyan

`wenyan*` is **forbidden** in any source-of-truth artifact: docs, ADRs, specs,
plans, context maps, skills, prompts, registries, handoffs, and `reports/**`. It is
allowed **only** in sub-agent reports. Persisted documentation uses **`lite`** or
**`full`**; **`ultra` is avoided in persisted docs — status-/terminal-only**, never
inside a doc body. `/document` (the `punch-document` reconciliation phase) writes
persistent docs in `lite` and may use `ultra` only for its terminal/status summary.
**Emoji carve-out:** emojis / ASCII emoticons (✅ ⚠️ ❌ `:)`) are **permitted in
persisted docs** when they aid scannability or signal status — an explicit
`/document` exception to the no-decorative-emoji rule. Evidence stays verbatim.

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
