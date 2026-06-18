# Prompt Registry

Punch has **nine** prompts — one per lifecycle phase (Spec, Plan, Build, Verify,
Review, Ship), plus `punch-test` (the TDD/Prove-It companion to Verify),
`punch-document` (a recurring documentation-reconciliation phase, orthogonal to
the linear lifecycle), and `punch-init` (a one-time bootstrap/adoption guard that
precedes the lifecycle). Spec absorbs the former Define phase. Each prompt has a
single, well-defined entry point. See `.github/prompts/` for the prompt bodies.

## Active prompts

| Prompt | Lifecycle phase | Mode | Agent | Use when |
|---|---|---|---|---|
| [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | Spec | Ask (writes spec doc) | `punch-architect-readonly` | A request needs clarifying (former Define) then specifying into goals / non-goals / acceptance criteria. |
| [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | Plan | Ask (Plan discipline) | `punch-planner` | You have a Spec and need scoped tasks with allowed/read-only/forbidden paths. |
| [`punch-build`](../../.github/prompts/punch-build.prompt.md) | Build | Agent (scoped, via dispatch) | `punch-builder` | An approved Plan task needs implementing; the dispatcher routes it to the runtime or performance-test engineer. |
| [`punch-test`](../../.github/prompts/punch-test.prompt.md) | Test (Verify companion) | Agent | `punch-verifier` | Prove a change RED→GREEN at the k6 check/threshold level via `./bin/punch`. |
| [`punch-verify`](../../.github/prompts/punch-verify.prompt.md) | Verify | Agent / Ask | `punch-verifier` | Build is complete; you need `reports/state/punch-run.json` evidence. |
| [`punch-review`](../../.github/prompts/punch-review.prompt.md) | Review | Ask | `punch-reviewer` | Verify passed; audit the diff before Ship. |
| [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | Ship | Agent (mechanical only) | `punch-reviewer` | Review approved; commit, push, open PR. **Never merges.** |
| [`punch-document`](../../.github/prompts/punch-document.prompt.md) | Documentate (recurring maintenance) | Ask / Agent | `punch-ai-governance` | Retire documentation debt in waves: map with `/graphify`, then keep / merge / rewrite / archive / delete / promote. |
| [`punch-init`](../../.github/prompts/punch-init.prompt.md) | Init (one-time bootstrap) | Agent (runs `./bin/punch init`) | `punch-ai-governance` (enforced) | Bootstrapping a repo for Punch: scan Copilot assets + docs readiness, guard pending adoption items, hand off to `/punch-document`. |

## One prompt per phase

Every lifecycle phase — including Build — has a single prompt. Splitting them by
ticket type would multiply maintenance without adding value. (`punch-test` is a
thin Verify companion, not a separate phase.)

Build's per-domain scope discipline moved **from prompts into agents**: the one
`punch-build` prompt activates the `punch-builder` dispatcher, which routes to a
domain engineer carrying that domain's allowed / read-only / forbidden scope.
This keeps a single Build entry point while preserving tight, reviewable scope.

`punch-document` is **not** a lifecycle phase — it is a recurring maintenance
workflow that runs orthogonal to Spec → Ship, reconciling documentation debt in
waves. It earns its own prompt because it fits no existing phase and reuses the
existing `punch-ai-governance` agent (no new agent, no new skill).

## Prompt contract

Every prompt file under `.github/prompts/` must declare:

```yaml
---
agent: ask | agent | plan | <custom-agent-name>
description: <one line, used by the Copilot UI>
---
```

VS Code prompt files use the **`agent:`** field (not `mode:`) — it names a
built-in mode or a custom agent under `.github/agents/`. Punch prompts bind to a
specific custom agent (e.g. `agent: punch-builder`).

And cover, in this order:

1. **Lifecycle phase** — which of Spec / Plan / Build / Verify / Review /
   Ship this serves (Spec absorbs the former Define).
2. **Mode** — Ask, Agent (scoped), or Agent (mechanical only).
3. **Owner skill(s)** — which skill(s) this prompt activates (domain + lifecycle).
4. **Agent** — which agent persona runs this prompt (core personas + the `punch-builder` dispatcher + its two engineers).
5. **When to use** — concrete trigger.
6. **Pre-conditions** (Build prompts only) — Plan + task ID + human
   approval.
7. **Typical scope** (Build prompts only) — allowed / read-only /
   forbidden paths.
8. **Inputs** — what the agent needs to be given.
9. **What to do** — numbered, finite, terminating steps.
10. **Expected output** — the artifact the prompt produces.
11. **Validation gate** — what advances the change to the next phase.

If a new prompt is proposed, the
[`punch-ai-governance`](../../.github/skills/punch-ai-governance/SKILL.md)
skill checks the phase / domain is not already covered and that the file
follows this contract.

## Why not more prompts

Seven prompts cover the whole lifecycle. Each extra prompt is one more interface
to maintain, one more place for guidance to drift. Add a new prompt only when:

- A real recurring task does not fit any existing phase, **and**
- Splitting it from an existing prompt would shrink, not duplicate.

The deliberate choice was: **one prompt per phase; Build's per-domain scope lives
in the engineers, not in extra prompts.** Resist the temptation to add
`punch-spec-fast` or `punch-review-deep`.
