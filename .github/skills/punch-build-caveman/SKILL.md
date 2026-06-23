---
name: punch-build-caveman
description: "Canonical Punch Caveman policy (single source). Repo default `lite`; per-phase voice — Spec/Document `lite`, Plan/Build/Review/Ship `full`, Test `ultra`. Build execution sub-agents speak `wenyan-lite`; engineer→cavecrew briefs `wenyan-full`; cavecrew workers `wenyan-ultra`. Wenyan is forbidden in persistent artifacts (docs/maps/registries) — sub-agent reports only. Evidence follows the producing agent's caveman level. Other files link here instead of restating."
applies-to: lifecycle/Build+Test — assistant-prose communication (punch-build & punch-test prompts + punch-builder/punch-test-engineer + the engineers); not path-scoped
---

# Punch — Caveman comms (canonical policy)

This is the **single source** for Caveman behavior in Punch. The prompts, agents,
and `copilot-instructions.md` **link here** and carry only their per-context delta —
they do not restate the rules below.

**Adoption — external upstream skill adapter (project scope).** Caveman **and
cavecrew** are vendor skills from upstream
[Caveman](https://github.com/JuliusBrussee/caveman), installed for VS Code GitHub
Copilot and kept **as-is** (prefer default install; do not fork vendor files).
Punch adopts only the scoped subset it needs; this skill carries the Punch
adaptation, vendor skills stay unmodified (install manifest:
[`.github/.ai-upstream/README.md`](../../.ai-upstream/README.md)). The live policy
is this skill plus the Build chain (`punch-build` → `punch-builder` → engineer →
cavecrew; a phase coordinator may also spawn cavecrew directly). (Adopt → filter → adapt: only `name`/`description`/`applies-to` stay in
frontmatter — the official Copilot SKILL schema — the rest lives here.)

## Caveman canon — per-phase levels (the mode policy)

Repo default is **`lite`** (set in `copilot-instructions.md`). Each lifecycle
phase overrides it with the voice below.

| Phase (Punch prompt) | Lifecycle cmd | Voice level |
|---|---|---|
| Spec (`punch-spec`) | `/spec` | **`lite`** (Punch default) |
| Plan (`punch-plan`) | `/plan` | **`full`** |
| Build (`punch-build`) — to humans | `/build` | **`full`** |
| Test (`punch-test`) | `/test` | **`ultra`**; evidence verbatim (the verification phase) |
| Review (`punch-review`) | `/review` | **`full`** |
| Ship (`punch-ship`) | `/ship` | **`full`** |
| Document (`punch-document`) | `/document` | **`lite`** persisted; **`ultra` terminal/status only**; evidence verbatim |

**Build delegation tiers** (compression deepens per tier):

- Human-facing output (coordinator **or** engineer → humans): **`full`**.
- Sub-agent-facing briefs use `wenyan`:
  - Coordinator → engineer (`punch-runtime-engineer` / `punch-performance-test-engineer`): **`wenyan-lite`**.
  - Engineer **or** coordinator → **cavecrew** worker: **`wenyan-full`**; the worker reports **`wenyan-ultra`**.

cavecrew workers are **leaves** (`agents:` empty) — they never spawn a further
tier, so depth is roster-bounded (max `builder → engineer → cavecrew`). Nesting
needs `chat.subagents.allowInvocationsFromSubagents: true` (lazy default).

The Punch `punch-*` prompt filenames are not renamed; the *Lifecycle cmd* column
is the Agent-Skills command each maps to (compatibility, not a rename).
`stop caveman` / `normal mode` reverts for the session.

Activation follows Agent Skills logic (`using-agent-skills`): state activation
**once** on entering the phase, then let the skill's persistence carry it — no
per-message re-invocation.

## Delegation (Caveman is output-only)

Caveman governs **output style only** — never tool access or which sub-agents an
agent may call. Spawners: the phase **coordinator** (`punch-builder` Build,
`punch-reviewer` Review, `punch-test-engineer` Test) and, nested, the Build
**engineer**. At Build the coordinator delegates the complete build to one
engineer; the engineer (or the coordinator directly) may spawn bounded
**cavecrew** leaf workers — engineer-spawned inherit by **lineage**,
coordinator-spawned by **injected brief** (VS Code custom agents have no skills
field); a worker's `tools` are a subset of its spawner. Compression deepens per
tier (`wenyan-lite` to the engineer, `wenyan-full` to a cavecrew worker, which
reports `wenyan-ultra`). Nesting uses GitHub Copilot's default sub-agent behavior
with `chat.subagents.allowInvocationsFromSubagents: true`; depth is
roster-bounded — cavecrew workers carry no `agents:`. Evidence in a worker report
follows that worker's caveman level. Canon depth/guards:
[`agent-guards.md`](../../../docs/ai/agent-guards.md).

## Punch priority (overrides Caveman brevity)

**Correctness > observable evidence > maintainability > Copilot compatibility >
brevity > Caveman style.** If brevity would harm correctness, evidence, or clarity,
**stop Caveman and answer normally.** Apply Caveman only **after** the task is
understood — never as a substitute for reasoning.

## Persistent artifacts — never Wenyan

`wenyan*` is **forbidden** in any source-of-truth artifact: docs, ADRs, specs,
plans, context maps, skills, prompts, registries, handoffs, and `reports/**`. It is
allowed **only** in sub-agent reports. Persisted documentation uses **`lite`** or
**`full`**; **`ultra` is avoided in persisted docs — status-/terminal-only**, never
inside a doc body. `/document` (the `punch-document` reconciliation phase) writes
persistent docs in `lite` and may use `ultra` only for its terminal/status summary.
**Emoji carve-out:** emojis / ASCII emoticons (✅ ⚠️ ❌ `:)`) are **permitted in
persisted docs** when they aid scannability or signal status — an explicit
`/document` exception to the no-decorative-emoji rule.

## Modes

`/caveman lite | full | ultra | wenyan-lite | wenyan-full | wenyan-ultra`.

- `lite` — keep articles + full sentences. `full` — drop articles, fragments OK.
- **`ultra`** — abbreviate prose words only; never code symbols, API names, or
  error strings.
- `wenyan-lite` / `wenyan-full` / `wenyan-ultra` — classical-Chinese compression
  for the execution tier; efficiency deepens down the delegation chain
  (`wenyan-ultra` = max).

## Stop conditions (Auto-Clarity)

Drop Caveman to normal prose when: evidence is incomplete · a risk needs
explanation · architecture tradeoffs matter · a security or irreversible-action
warning is involved · the user asks for normal mode · compression would reduce
clarity or correctness. Resume after the unclear part is done.
