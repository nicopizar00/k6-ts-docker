---
applyTo: ".github/**,docs/ai/**,CLAUDE.md,AGENTS.md"
description: How the six-phase agentic lifecycle is enforced in this repo.
---
# Agentic Workflow — Path Instructions

Scope: every file defining or describing how AI assistants work in this
repo. Operating-model details: [`docs/ai/operating-model.md`](../../docs/ai/operating-model.md).
Walkthrough: [`docs/ai/workflow.md`](../../docs/ai/workflow.md).

## Phase mode discipline

| Phase | Mode | Edits | Reads |
|---|---|---|---|
| Spec     | Ask | spec doc only (if any) | broad |
| Plan     | Ask (Plan discipline) | plan doc only (if any) | broad |
| Build    | Agent (scoped) | allowed paths only | allowed + read-only |
| Verify   | Agent / Ask | only patches in scope | narrow |
| Review   | Ask | none | the diff + plan |
| Ship     | Agent (mechanical only) | git + gh only | the diff |

Spec absorbs former Define phase (opens with clarify/refine step).

## Rules

- **Spec / Plan are read-heavy.** Output prose — Spec clarifies
  request (former Define), writes spec; Plan writes plan. No code edits.
- **Build is edit-limited.** Every Build prompt declares allowed /
  read-only / forbidden paths. Agent refuses touch anything
  outside `allowed`.
- **Verify runs project commands.** Prefer `./bin/punch` over ad-hoc
  `docker run` or host `k6`. See
  [`punch-verify`](../prompts/punch-verify.prompt.md).
- **Review evaluates risk, correctness, boundary violations.**
  Read-only critique against Plan. Activates
  [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
  when diff touches `.github/` or `docs/ai/`.
- **Ship summarizes state, finalizes mechanically.** Commits, push,
  PR. Humans merge. Ship never expands scope.
- **Any scope expansion returns to Plan.** Mid-Build discoveries do not
  authorize edits outside current task's allowed paths.

## Frontmatter contract

Every artifact in `.github/` declares frontmatter:

- **Instructions** (`*.instructions.md`): `applyTo:` glob, `description:`
  one-liner.
- **Prompts** (`*.prompt.md`): `agent: ask|agent|plan|<custom-agent>`,
  `description:` one-liner. (VS Code prompt files use `agent:`, not `mode:`.)
- **Skills** (`SKILL.md`): `name:`, `description:`, `applies-to:`
  (free-form scope hint).
- **Agents** (`*.agent.md`): `name:`, `description:`, `tools:` (capability
  scope). `model:` optional.

[`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md)
skill verifies this every time `.github/` or `docs/ai/` touched.

## When adding a new AI asset

New prompt, skill, agent, or instruction is itself a *Spec → Plan →
Build* cycle. Plan must answer:

1. Which existing asset could not absorb this responsibility?
2. What concrete recurring task currently mishandled?
3. Which registry entries and cross-references update in same PR?

If question 1 or 2 unanswerable concretely, answer is "don't add it".

## When this file activates

Always — for any change under `.github/`, `docs/ai/`, `CLAUDE.md`, or
`AGENTS.md`.
