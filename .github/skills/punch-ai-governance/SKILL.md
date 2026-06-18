---
name: punch-ai-governance
description: Audits AI configuration — instructions, prompts, skills, agents, lifecycle docs — for boundary compliance, scope discipline, handoff hygiene, frontmatter contracts, and cross-reference drift.
applies-to: .github/**, docs/ai/**, AGENTS.md, CLAUDE.md
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
  `skill-registry.md`, `AGENTS.md`, and `copilot-instructions.md`
  resolves; every asset referenced exists.
- The duplication-detection pass — no rule restated across files.

It does **not** own:

- Repository code (Python, TS, Docker) — that is the domain skills'
  territory.
- The architecture itself — that lives in `CLAUDE.md` and
  `docs/architecture/`.

## Replaces

This skill replaces the earlier `punch-ai-governance-audit` skill. The
previous version enforced an absolute three-skill cap and a one-prompt-
per-phase rule; this version enforces *boundary discipline* and *handoff
hygiene* on a deliberately larger asset set (6 domain + 13 lifecycle skills,
10 agents — 4 core personas, a 5-member builder family, and the `security-auditor`
specialist — and 11 prompts). The justification for lifting the cap lives in
[`docs/ai/skill-registry.md`](../../../docs/ai/skill-registry.md) and
[`docs/ai/prompt-registry.md`](../../../docs/ai/prompt-registry.md).

It also **subsumes the upstream `scripts/validate-skills.js`** (a Node frontmatter
validator): its checks — valid `name`/`description`, frontmatter completeness,
registry parity — are covered by the audit procedure below and run with no host
Node (this skill is read-only: Read/Grep/Glob). Punch does not run host Node.

## When to use

- A PR touches `.github/` or `docs/ai/`.
- The Review phase runs against a diff that includes AI configuration.
- Periodic governance review (quarterly cadence recommended).

## Inputs expected

- The current state of `.github/` and `docs/ai/` (Glob/Read).
- (Optional) a diff if the audit is PR-scoped.

## Procedure (the audit pass)

> **Frozen / adopted scope.** Treat `docs/ai/history/**` as frozen provenance,
> `.ai-upstream/**` as **gitignored local upstream staging** (may be absent on a
> fresh clone), and both `.github/skills/graphify/**` and `.agents/skills/**` (the
> canonical Copilot Caveman install) as adopted-upstream skills: all are
> **excluded** from the frontmatter-completeness, cross-reference, naming,
> duplication, and stale-asset checks below. `graphify` and `.agents/skills/caveman`
> are still **registered** (parity) in `skill-registry.md`, but are
> upstream-maintained — refresh from upstream, never hand-edit. The authored
> adapter `.github/skills/punch-build-caveman/**` is **not** exempt — it is
> Punch-authored and subject to all checks. These record point-in-time / external
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
   - Every file in `.github/agents/*.agent.md` is listed in `AGENTS.md`.
3. **Boundary declarations.**
   - Every Build prompt
     (`.github/prompts/punch-build.prompt.md`) lists allowed,
     read-only, and forbidden paths.
   - Every agent file lists allowed and forbidden behavior.
4. **Lifecycle alignment.**
   - Each lifecycle phase (Spec, Plan, Verify, Review, Ship) has
     exactly one prompt (Spec absorbs the former Define; `punch-test` is a
     Verify companion).
  - Build has a single `punch-build` prompt and a dispatcher that routes to domain engineers.
   - Every prompt's "Owner skill" line points at an existing skill.
   - Every prompt's "Agent" line points at an existing agent.
5. **Cross-references.**
   - Grep `.github/` and `docs/` for the names of all assets; every
     reference resolves to an existing file.
6. **Duplication / conflict.**
   - No verbatim rule appears in two files.
   - No path instruction contradicts `CLAUDE.md`,
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
  `CLAUDE.md`, `punch-architecture.instructions.md`, or another file is
  referenced, not restated.

## Why this is a separate skill

Governance drift is a distinct failure mode from "the code doesn't work".
Without a dedicated skill, governance regressions accumulate silently as
each PR adds "just one more" instruction or prompt. Isolating governance
makes the cost of new AI assets visible.
