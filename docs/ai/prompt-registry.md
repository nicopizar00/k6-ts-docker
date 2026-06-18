# Prompt Registry

Punch has one prompt per lifecycle phase — Spec, Plan, **Build** (a single
`punch-build` dispatcher, added in Phase F), Verify, Review, Ship — plus
`punch-test` (the TDD/Prove-It companion to Verify). Spec absorbs the former
Define phase. Each prompt has a single, well-defined entry point. See
`.github/prompts/` for the prompt bodies.

> **Transition note.** The five per-domain `punch-build-*` prompts were retired
> in favour of one `punch-build` prompt bound to the `punch-builder` dispatcher
> agent, which delegates to `punch-runtime-engineer` / `punch-performance-test-engineer`.
> The `punch-build` row is added when its prompt lands (Phase F).

## Active prompts

| Prompt | Lifecycle phase | Mode | Agent | Use when |
|---|---|---|---|---|
| [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | Spec | Ask (writes spec doc) | `punch-architect-readonly` | A request needs clarifying (former Define) then specifying into goals / non-goals / acceptance criteria. |
| [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | Plan | Ask (Plan discipline) | `punch-planner` | You have a Spec and need scoped tasks with allowed/read-only/forbidden paths. |
| [`punch-test`](../../.github/prompts/punch-test.prompt.md) | Test (Verify companion) | Agent | `punch-verifier` | Prove a change RED→GREEN at the k6 check/threshold level via `./bin/punch`. |
| [`punch-verify`](../../.github/prompts/punch-verify.prompt.md) | Verify | Agent / Ask | `punch-verifier` | Build is complete; you need `reports/state/punch-run.json` evidence. |
| [`punch-review`](../../.github/prompts/punch-review.prompt.md) | Review | Ask | `punch-reviewer` | Verify passed; audit the diff before Ship. |
| [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | Ship | Agent (mechanical only) | `punch-reviewer` | Review approved; commit, push, open PR. **Never merges.** |

## One prompt per phase

Every lifecycle phase — including Build — has a single prompt. Splitting them by
ticket type would multiply maintenance without adding value. (`punch-test` is a
thin Verify companion, not a separate phase.)

Build's per-domain scope discipline moved **from prompts into agents**: the one
`punch-build` prompt activates the `punch-builder` dispatcher, which routes to a
domain engineer carrying that domain's allowed / read-only / forbidden scope.
This keeps a single Build entry point while preserving tight, reviewable scope.

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
specific custom agent (e.g. `agent: punch-builder-orchestrator`).

And cover, in this order:

1. **Lifecycle phase** — which of Spec / Plan / Build / Verify / Review /
   Ship this serves (Spec absorbs the former Define).
2. **Mode** — Ask, Agent (scoped), or Agent (mechanical only).
3. **Owner skill(s)** — which skill(s) this prompt activates (domain + lifecycle).
4. **Agent** — which agent persona runs this prompt (4 core personas + the 5-member builder family).
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

Eleven prompts cover the entire matrix of (phase) × (Build domain). Each
extra prompt is one more interface to maintain, one more place for
guidance to drift. Add a new prompt only when:

- A real recurring task does not fit any existing phase or Build
  domain, **and**
- Splitting it from an existing prompt would shrink, not duplicate.

The deliberate choice was: **scale prompts by Build domain, not by
phase nuance.** Resist the temptation to add `punch-spec-fast` or
`punch-review-deep`.
