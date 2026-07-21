---
name: punch-comms-policy
description: "Optional Punch presentation-voice policy (single source). Caveman is a user-invoked, output-only convenience — normal prose is the complete fallback when it is absent or inactive, and Punch's lifecycle authority, scope, evidence, and verdicts are identical either way. Build (`punch-build` → `punch-builder` → engineers) does not reference this skill; it is fully decoupled from Caveman/cavecrew."
applies-to: optional presentation/communication voice for Spec, Plan, Document, Test, Review, Ship, Init — not path-scoped, not required for Punch execution
---

# Punch — Comms policy (optional, output-only)

This is the **single source** for Caveman voice in the phases that opt into it.
Those prompts/agents **link here** and carry only their per-context delta — they
do not restate the rules below. **Build never links here** (see
[`agent-guards.md`](../../../docs/ai/agent-guards.md) and
[`punch-build.prompt.md`](../../prompts/punch-build.prompt.md) for its
independent, comms-free contract).

**Optional by construction.** Caveman and cavecrew are vendor skills from
upstream [Caveman](https://github.com/JuliusBrussee/caveman), installed for VS
Code GitHub Copilot and kept **as-is** (install manifest:
[`.github/.ai-upstream/README.md`](../../.ai-upstream/README.md)). Neither is a
Punch prerequisite. Absent or inactive, every phase below runs in plain,
complete prose — same scope, same evidence, same verdicts, same lifecycle
authority. This skill governs **voice only**; it never changes tools, task
order, delegation roster, or verdict ownership — those live in each agent's own
definition and in [`agent-guards.md`](../../../docs/ai/agent-guards.md).

## Per-phase voice (the mode policy)

Repo default is **`lite`** (set in `copilot-instructions.md`) for phases that
opt in:

| Phase (Punch prompt) | Lifecycle cmd | Voice level |
|---|---|---|
| Spec (`punch-spec`) | `/spec` | **`lite`** (Punch default) |
| Plan (`punch-plan`) | `/plan` | **`full`** |
| Test (`punch-test`) | `/test` | **`ultra`**; evidence verbatim (the verification phase) |
| Review (`punch-review`) | `/review` | **`full`** |
| Ship (`punch-ship`) | `/ship` | **`full`** |
| Document (`punch-document`) | `/document` | **`lite`** persisted (docs/reports); **`full`** wave working comms (diagnose/classify/plan); evidence verbatim |
| Init (`punch-init`) | `/punch-init` | **`lite`** |

Build (`punch-build`) has no row here — it is fully decoupled and carries no
Punch-prescribed voice.

An agent that spawns an optional cavecrew worker (Review/Test/Security only —
never Build) may brief it in a `wenyan-*` tier; that delegation detail is the
spawning agent's own, stated in its own definition, not restated here. Worker
reports are **non-guarded (lazy)** — the spawner may use the artifact as-is.

The Punch `punch-*` prompt filenames are not renamed; the *Lifecycle cmd*
column is the Agent-Skills command each maps to (compatibility, not a rename).
`stop caveman` / `normal mode` reverts for the session. Activation follows
Agent Skills logic (`using-agent-skills`): state activation **once** on
entering the phase, then let the skill's persistence carry it.

## Punch priority (overrides Caveman brevity)

**Correctness > observable evidence > maintainability > Copilot compatibility >
brevity > Caveman style.** If brevity would harm correctness, evidence, or
clarity, **stop Caveman and answer normally.** Apply Caveman only **after** the
task is understood — never as a substitute for reasoning.

## Persistent artifacts — never Wenyan

`wenyan*` is **forbidden** in any source-of-truth artifact: docs, ADRs, specs,
plans, context maps, skills, prompts, registries, handoffs, and `reports/**`. It
is allowed **only** in sub-agent reports. Persisted documentation uses **`lite`**
or **`full`**; **`ultra` is avoided in persisted docs — status-/terminal-only**,
never inside a doc body. `/document` (the `punch-document` reconciliation phase)
writes persistent docs/reports in `lite` and uses `full` for wave working comms
(diagnosis / classification / planning) — no AI-narrative filler in persisted
assets. **Emoji carve-out:** emojis / ASCII emoticons (✅ ⚠️ ❌ `:)`) are
**permitted in persisted docs** when they aid scannability or signal status — an
explicit `/document` exception to the no-decorative-emoji rule.

## Modes

`/caveman lite | full | ultra | wenyan-lite | wenyan-full | wenyan-ultra`.

- `lite` — keep articles + full sentences. `full` — drop articles, fragments OK.
- **`ultra`** — abbreviate prose words only; never code symbols, API names, or
  error strings.
- `wenyan-lite` / `wenyan-full` / `wenyan-ultra` — classical-Chinese compression
  for an optional sub-agent brief; which tier a spawner uses is that spawner's
  own choice, stated in its own definition.

## Stop conditions (Auto-Clarity)

Drop Caveman to normal prose when: evidence is incomplete · a risk needs
explanation · architecture tradeoffs matter · a security or irreversible-action
warning is involved · the user asks for normal mode · compression would reduce
clarity or correctness. Resume after the unclear part is done.
