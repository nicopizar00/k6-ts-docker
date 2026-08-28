---
agent: punch-ai-governance
description: Init — on-demand, read-only asset enablement sweep that certifies the Punch GitHub Copilot asset set (prompts, agents, skills, instructions) is present, punch-prefixed, and Copilot-compatible before the lifecycle runs, plus an informational capability check for the optional AI-Ingest vendor skill Caveman and the workspace's VS Code discovery boundary. Re-runnable anytime. Reports PASS / WARN / BLOCKED. Never reconciles docs, never runs a runtime.
---
# Punch — Init (GitHub Copilot asset enablement sweep)

**Lifecycle phase:** Init (bootstrap; precedes Spec → Ship, orthogonal to it; first
run at adoption, re-runnable on demand after drift)
**Target:** VS Code **GitHub Copilot** only. Punch is an AI abstraction layer over
Copilot — Init checks the assets Punch needs to operate **through Copilot**, nothing else.
**Mode:** Ask — **read-only** sweep of the Copilot asset layout (Read / Grep / Glob).
No runtime, no Python, no installer, no doctor.
**Owner skill:** [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md) (decision authority).
**Agent:** [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) — **enforced**.
Init runs **only** under that agent. No other agent runs Init; Init introduces no agent.
**Operating comms:** Caveman **`lite`** (optional).

## When to use

First when a repo adopts Punch for VS Code GitHub Copilot, and re-run on demand
anytime after (e.g. after drift), to certify the Copilot asset set is installed,
correctly named, and Copilot-compatible.
Init **certifies readiness**; it does **not** reconcile — doc/asset reconciliation is
[`/punch-document`](punch-document.prompt.md).

## What to check (the sweep)

Read the live Copilot assets, then grade each check **PASS / WARN / BLOCKED**.
Source of truth for the required set: the Copilot asset layout itself plus the
registries ([`prompt-registry.md`](../../docs/ai/prompt-registry.md),
[`skill-registry.md`](../../docs/ai/skill-registry.md)) plus the
[`.github/agents/`](../agents/) roster — read inventory, do not hard-code counts.

1. **Prompt commands.** Every lifecycle + orthogonal command exists in
   `.github/prompts/` with the **`punch-` prefix** and valid frontmatter
   (`agent:` + `description:`). Required: `punch-spec`, `punch-plan`,
   `punch-build`, `punch-test`, `punch-review`, `punch-ship`, `punch-document`,
   `punch-init`. Missing / non-prefixed / no-frontmatter → **BLOCKED**.
2. **Agents.** Every `.github/agents/*.agent.md` has `name:` + `description:`.
   The optional `punch-cavecrew-investigator` / `punch-cavecrew-reviewer`
   personas support Review/Test/Security only — never Build; absence is not a
   gap. Init is owned solely by `punch-ai-governance`
   (`disable-model-invocation: true`). Any agent introduced **for Init**
   outside that ownership → **BLOCKED**.
3. **Skills.** Every `skill-registry.md` row maps to a `.github/skills/*/SKILL.md`
   (and vice versa) with `name:` / `description:` / `applies-to:`. Each skill
   adapted from canon carries the **`punch-` prefix**; native skills may stay
   agnostic. Adapted-in-place skill missing the prefix → **WARN** (rename via
   `/punch-document`). Missing required skill → **BLOCKED**.
4. **Instructions.** Every `.github/instructions/*.instructions.md` has
   `applyTo:` + `description:`. Missing required instruction or bad frontmatter → **BLOCKED**.
5. **AI Skills (Caveman — optional vendor capability; graphify — adopted upstream skill).**
   Caveman presence is an **informational capability check only** — never a
   Punch prerequisite:
   - Caveman's default-`lite` rule for VS Code GitHub Copilot Chat lives directly
     in [`copilot-instructions.md`](../copilot-instructions.md) — no separate
     Punch presentation-adapter skill. Every phase runs entirely in normal
     prose when Caveman is absent or inactive; not a gap.
   - The vendor skill `caveman` is installed via the **accepted AI-Ingest path**
     ([`.github/.ai-upstream/README.md`](../.ai-upstream/README.md)), scoped to
     `github-copilot`, relocated once to `.github/skills/caveman/` (the Copilot
     project-skill location — installer default `.agents/skills/caveman/` must
     not remain populated). Not installed → **WARN** (user installs manually;
     purely optional — Build never depends on it).
   - The optional `punch-cavecrew-investigator` / `punch-cavecrew-reviewer`
     Copilot custom agents in `.github/agents/` (see check 2) are
     self-contained and certified on their own frontmatter — they require no
     `.agents/**` vendor skill to be present. `.agents/**` is outside this
     workspace's VS Code Chat discovery boundary and is never a Punch
     capability, prerequisite, resolver target, or canon.
   - The native upstream skill [`graphify`](../skills/graphify/SKILL.md) exists,
     adopted verbatim (only `user-invocable:` / `disable-model-invocation:` host
     metadata added — no Punch-authored fork; native skills stay agnostic per
     check 3). Explicit-only (`/graphify`), never gated behind another Punch
     skill. Missing skill file → **BLOCKED**. Its host CLI (PyPI `graphifyy`,
     host `graphify`) is the **recommended install** for the `/punch-document`
     mapping subagent — `uv tool install graphifyy`
     ([ADR 0002](../../docs/ai/decisions/0002-graphify-host-tool.md)).
     CLI not on PATH → **WARN** (optional, off the evidence/execution path; Init
     never shells out to it — `/punch-document` only — and the lifecycle still
     runs without it).
   - Optional [canon adopt-adapt parity](../skills/punch-ai-governance/SKILL.md)
     against `.ai-upstream/` flags any `.github/skills` adaptation still owing a
     `punch-` rename. Canon snapshot absent → note `canon-unavailable` (never BLOCKED).
6. **Reference integrity.** Every prompt/skill/instruction/agent cross-reference
   resolves to a real file in the Copilot asset layout. A reference that points
   at an **unsupported external dependency** (a runtime, a host script, a cloud
   config, a non-Copilot agent tool) → **BLOCKED**.
7. **No external runtime canon.** No asset may declare `CLAUDE.md`, Claude Code,
   Cloud Code, a Python runtime, or any external config as **canonical for Punch**.
   Any such declaration → **BLOCKED**. The GitHub Copilot asset layout
   (`.github/**` + `docs/ai/**`) is Punch's only source of truth; non-native
   files belong in `.github/assets/resolve/`, not referenced as canon.
8. **Allowed-dependency rule.** Any dependency outside the Copilot asset layout
   (`.github/**`) must come through the **accepted AI-Ingest path** and its rules
   (`.ai-upstream` manifest, Copilot-scoped, kept verbatim). A dependency outside
   both the asset layout and the AI-Ingest path → **BLOCKED**.
9. **Docs orientation.** AI-facing docs, architecture notes, and boundaries docs
   must not misdirect Copilot away from Punch's GitHub-Copilot-first design (e.g.
   telling Copilot the runtime or an external tool is the entry point for Punch
   asset work). Misdirection → **WARN** (fix via `/punch-document`).
10. **VS Code discovery boundary.** [`.vscode/settings.json`](../../.vscode/settings.json)
    exists and is valid JSON; `chat.useAgentsMdFile`, `chat.useNestedAgentsMdFiles`,
    and `chat.useClaudeMdFile` are `false`; `chat.instructionsFilesLocations`,
    `chat.promptFilesLocations`, `chat.agentFilesLocations`, and
    `chat.agentSkillsLocations` each enable their `.github/*` root
    (`.github/instructions`, `.github/prompts`, `.github/agents`,
    `.github/skills`). Missing file, invalid JSON, or a required key set to the
    wrong value → **BLOCKED**.

## Grading

- **PASS** — present, `punch-`prefixed where required, valid frontmatter,
  Copilot-compatible, references resolve, no external-runtime canon.
- **WARN** — present but misnamed / non-prefixed / unfilled placeholder /
  needs adapt; or a vendor AI Skill not yet installed; or a doc misdirection.
  Adoption may proceed once a human reviews each WARN.
- **BLOCKED** — a required asset is missing or has broken frontmatter; an asset
  is not Copilot-compatible; a reference points at an unsupported external
  dependency; or an asset declares an external runtime/config as Punch canon.

**Asset existence is not enough** — an asset that exists but is not
Copilot-compatible (wrong frontmatter, external-only references) grades **BLOCKED**,
not PASS. Any **BLOCKED** → overall `not_ready`; Spec → Ship and `/punch-document`
stay closed until it clears.

## Report (concise)

Emit a short table — one row per check (1–9) → **PASS / WARN / BLOCKED** + a
one-line reason — then:

- **Missing / misnamed / non-prefixed** assets, each with its path.
- **Externally dependent / Copilot-incompatible** assets, each with its path.
- **Overall verdict:** `adoption_ready` (all PASS/WARN, human cleared WARNs) or
  `not_ready` (≥1 BLOCKED).
- **One next command:** `adoption_ready` → `/punch-document` (reconcile) or the
  first lifecycle phase (`/punch-spec`); `not_ready` → fix the BLOCKED rows first.

## Boundary rules

- **Read-only.** Never renames, deletes, rewrites, or creates assets; never
  rewrites unrelated docs. Findings hand off to `/punch-document`.
- **No runtime, no repair.** Never executes or repairs Python; never runs
  `./bin/punch`, Docker, or k6; never acts as a doctor, installer, migrator, or
  broad fixer. Scripts under the repo are **not** mutable Init assets — Init does
  not embed or edit Python, shell, `setup.py`, or launchers.
- **Copilot-first.** Checks only the assets Punch needs to operate through VS Code
  GitHub Copilot. Vendor tools (graphify, Caveman) are in scope **only** via the
  accepted AI-Ingest path; `.agents/**` vendor skills (e.g. `cavecrew`) and
  non-Copilot agent runtimes (Claude Code, Cloud Code) are out of scope
  entirely.
- **Lifecycle preserved.** Init certifies; it does not alter the Spec → Plan →
  Build → Test → Review → Ship → Document lifecycle it gates.

## Validation gate

Init succeeds when every check grades **PASS** (or **WARN** a human has cleared)
and the report names every gap. Any **BLOCKED** row keeps the repo `not_ready` and
blocks adoption until resolved.
