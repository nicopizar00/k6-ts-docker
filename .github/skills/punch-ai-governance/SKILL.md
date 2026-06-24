---
name: punch-ai-governance
description: Audits AI configuration — instructions, prompts, skills, agents, lifecycle docs — for boundary compliance, scope discipline, handoff hygiene, frontmatter contracts, and cross-reference drift.
applies-to: .github/**, docs/**, README.md
allowed-tools: Read, Grep, Glob
---

# Skill: punch-ai-governance

## Responsibility

This skill is the authority on **whether the AI operating model is
healthy**.

It owns:

- The frontmatter contract for instructions, prompts, skills, and agents.
- Boundary compliance: every Build prompt declares allowed / read-only /
  forbidden paths, and every recent diff respected them.
- Scope discipline: no Build call has expanded scope mid-flight without a
  return to Plan.
- Handoff hygiene: each prompt's "Owner skill" and agent line up; each
  agent's allowed/forbidden behavior matches the prompts that activate it.
- Cross-reference health: every link in `prompt-registry.md`,
  `skill-registry.md`, and `copilot-instructions.md`
  resolves; every asset referenced exists.
- Delegation-depth integrity: every `agents:` roster stays depth-1 — only a
  phase coordinator (`punch-builder` / `punch-code-reviewer` / `punch-test-engineer`
  / `punch-security-auditor`) lists sub-agents; engineers and `punch-cavecrew-*` workers
  carry empty / absent
  `agents:`. Each cavecrew worker's `tools` must be a **subset** of every
  coordinator that lists it (so `punch-cavecrew-builder`'s `edit/editFiles` keeps it
  Build-only). Canon: [`agent-guards.md`](../../../docs/ai/agent-guards.md).
- The duplication-detection pass — no rule restated across files.
- The **canon adopt-adapt parity** report: which `.ai-upstream` canon skills
  are adopted untouched, adapted-in-place, or unadopted — and which adaptations
  still owe a `punch-` rename (read-only; see procedure below).

It does **not** own:

- Repository code (Python, TS, Docker) — that is the domain skills'
  territory.
- The architecture itself — that lives in `punch-architecture.instructions.md`
  and `docs/architecture/`.

## Replaces

This skill replaces the earlier `punch-ai-governance-audit` skill. The
previous version enforced an absolute three-skill cap and a one-prompt-
per-phase rule; this version enforces *boundary discipline* and *handoff
hygiene* on a deliberately larger asset set (domain + lifecycle skills, the
agent roster, and the lifecycle prompts — **live inventory in the registries**,
not hard-coded here). The justification for lifting the cap, and the current
counts, live in
[`docs/ai/skill-registry.md`](../../../docs/ai/skill-registry.md) and
[`docs/ai/prompt-registry.md`](../../../docs/ai/prompt-registry.md); the agent
roster lives in [`.github/agents/`](../../agents/) and the
[`copilot-instructions.md`](../../copilot-instructions.md) lifecycle table.

It also **subsumes the upstream `scripts/validate-skills.js`** (a Node frontmatter
validator): its checks — valid `name`/`description`, frontmatter completeness,
registry parity — are covered by the audit procedure below and run with no host
Node (this skill is read-only: Read/Grep/Glob). Punch does not run host Node.

## When to use

- A PR touches `.github/` or `docs/ai/`.
- The Review phase runs against a diff that includes AI configuration.
- Periodic governance review (quarterly cadence recommended).

**Not for:** product code (Python/TS/Docker — the domain skills) or the architecture itself (`punch-architecture.instructions.md`, `docs/architecture/`).

## Inputs expected

- The current state of `.github/` and `docs/ai/` (Glob/Read).
- (Optional) a diff if the audit is PR-scoped.

## Procedure (the audit pass)

> **Frozen / adopted scope.** Treat `docs/ai/history/**` as frozen provenance,
> `.ai-upstream/**` as **gitignored local upstream staging** (may be absent on a
> fresh clone), and `.agents/skills/**` (the canonical Copilot Caveman install) as
> an adopted-upstream skill: these are **excluded** from the frontmatter-
> completeness, cross-reference, naming, duplication, and stale-asset checks below.
> `.agents/skills/caveman` is still **registered** (parity) in `skill-registry.md`
> but is upstream-maintained — refresh from upstream, never hand-edit.
> `.github/skills/punch-graphify/**` is now a **Punch-leaned adaptation** (trimmed to the
> in-IDE build/update/query subset; pristine upstream kept in
> `.ai-upstream/graphify/`) — like `.github/skills/punch-build-caveman/**` it is
> **authored and subject to all checks**. These record point-in-time / external
> state.

1. **Frontmatter completeness.**
   - Every `*.instructions.md` has `applyTo:` + `description:`.
   - Every `*.prompt.md` has `agent: ask|agent|plan|<custom-agent>` + `description:` (VS Code prompt files use `agent:`, not `mode:`).
   - Every `SKILL.md` has `name:`, `description:`, `applies-to:`.
   - Every `*.agent.md` has `name:` + `description:`.
2. **Asset inventory matches registries.**
   - Every file in `.github/skills/*/SKILL.md` has a row in
     `docs/ai/skill-registry.md`, and vice versa.
   - Every file in `.github/prompts/*.prompt.md` has a row in
     `docs/ai/prompt-registry.md`, and vice versa.
   - Every file in `.github/agents/*.agent.md` is referenced in the
     `copilot-instructions.md` lifecycle table or `docs/ai/prompt-registry.md`.
3. **Boundary declarations.**
   - Every Build prompt
     (`.github/prompts/punch-build.prompt.md`) lists allowed,
     read-only, and forbidden paths.
   - Every agent file lists allowed and forbidden behavior.
4. **Lifecycle alignment.**
   - Each lifecycle phase (Spec, Plan, Test, Review, Ship) has
     exactly one prompt (Spec absorbs the former Define; `punch-test` is the
     Test/verification phase, agent `punch-test-engineer` — no separate Verify).
  - Build has a single `punch-build` prompt and a dispatcher that routes to domain engineers.
   - Every prompt's "Owner skill" line points at an existing skill.
   - Every prompt's "Agent" line points at an existing agent.
5. **Cross-references.**
   - Grep `.github/` and `docs/` for the names of all assets; every
     reference resolves to an existing file.
6. **Duplication / conflict.**
   - No verbatim rule appears in two files.
   - No path instruction contradicts `.github/copilot-instructions.md`,
     `punch-architecture.instructions.md`, or
     `agentic-workflow.instructions.md`.
7. **Mode discipline.**
   - Prompts bound to a builder agent declare an explicit scope (allowed
     paths from a Plan, or named "mechanical only" purpose).
8. **Scope discipline (diff-scoped audits only).**
   - For each file changed under a Build prompt's path, confirm it is in
     the Plan's allowed list. Flag any out-of-scope edits.
9. **No phase-named skills.**
   - Flag any skill matching
     `punch-(define|spec|plan|build|verify|review|ship)`.

## Canon adopt-adapt report (read-only)

A second pass, **report only** — it classifies every `.github/skills/*` against
the `.ai-upstream/agent-skills/skills/` canon and recommends prefixing; it
**never renames, edits, or deletes**. The mechanical comparison runs read-only
under the AI Governance agent's terminal
(`git diff --no-index <canon> <adapted>` / `diff -rq`); decision authority is
this skill. Surfaced as the optional canon-parity sub-check of the AI-Skills
step in [`/punch-init`](../../prompts/punch-init.prompt.md) (canon absent →
`canon-unavailable`, never a block).

**Precondition (user-required).** `.ai-upstream/**` is gitignored local upstream
staging and may be absent. This report **does not** fetch or refresh it —
syncing the canon snapshot is an intentional **user action** (see
[`.github/.ai-upstream/README.md`](../../.ai-upstream/README.md)). Canon absent →
emit `canon-unavailable` and skip the parity verdict (never a hard fail).

For each canon skill `<name>` and each `.github/skills` entry, classify:

| class | condition | recommendation (report only) |
| --- | --- | --- |
| **adopted-untouched** | `<name>` both sides, byte-identical to canon | leave agnostic — no prefix |
| **adapted-in-place** | `<name>` both sides, **any** diff vs canon | **recommend `punch-<name>` rename** + ref update — the "one diff → prefix" rule |
| **adapted-prefixed** | `punch-<name>` maps to canon `<name>` | OK — adaptation already named |
| **native** | `.github/skills` entry with no canon `<name>` | OK — Punch-authored |
| **unadopted** | canon `<name>` absent from `.github/skills` (bare or `punch-`) | list as available; **adopting is a user decision** |

**Hand-off, not mutation.** Renames (`adapted-in-place` → `punch-*`) and
adoptions (`unadopted` → adopt) go through a normal Plan → Build (or
[`/punch-document`](../../prompts/punch-document.prompt.md)) — never this report.
`.ai-upstream` refresh and adopt/decline decisions stay with the user.

**Output.** A parity table (class per skill) + a numbered recommendation list for
every `adapted-in-place` skill owing a prefix, then a verdict line:
**"Canon parity clean"** or **"Canon drift — N skills owe `punch-` prefix"**.

## Output format

A numbered findings list. For each:

- File + line range.
- Finding (one sentence).
- Suggested fix.

Conclude with a verdict line: **"Governance is clean"** or **"Governance
drift — see findings"**.

## Safety / boundary rules

- **Read-only.** This skill flags drift; it does not edit. Fixes go
  through a normal Plan → Build cycle.
- **No silent additions.** New skills, prompts, agents, or instructions
  need a Plan, a registry entry, and a `punch-ai-governance` pass
  before merge.
- **Cross-link, don't duplicate.** Any rule that already exists in
  `.github/copilot-instructions.md`, `punch-architecture.instructions.md`, or
  another file is referenced, not restated.

## Why this is a separate skill

Governance drift is a distinct failure mode from "the code doesn't work".
Without a dedicated skill, governance regressions accumulate silently as
each PR adds "just one more" instruction or prompt. Isolating governance
makes the cost of new AI assets visible.
