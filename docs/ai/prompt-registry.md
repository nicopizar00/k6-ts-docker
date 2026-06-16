# Prompt Registry

Punch supports **eleven** prompts: one for each non-Build lifecycle phase
plus five domain-specialized Build prompts. Each prompt has a single,
well-defined entry point. See `.github/prompts/` for the prompt bodies.

## Active prompts

| Prompt | Lifecycle phase | Mode | Agent | Use when |
|---|---|---|---|---|
| [`punch-define`](../../.github/prompts/punch-define.prompt.md) | Define | Ask | `punch-architect-readonly` | You need to translate a request into a clean problem statement. |
| [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | Spec | Ask | `punch-architect-readonly` | You have a Define note and need goals / non-goals / acceptance criteria. |
| [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | Plan | Ask (Plan discipline) | `punch-planner` | You have a Spec and need scoped tasks with allowed/read-only/forbidden paths. |
| [`punch-build-orchestrator`](../../.github/prompts/punch-build-orchestrator.prompt.md) | Build | Agent | `punch-builder-scoped` | Approved Plan task touches `src/punch/**` or `bin/punch`. |
| [`punch-build-compose`](../../.github/prompts/punch-build-compose.prompt.md) | Build | Agent | `punch-builder-scoped` | Approved Plan task touches `docker-compose.yml` or `docker/**`. |
| [`punch-build-k6-http`](../../.github/prompts/punch-build-k6-http.prompt.md) | Build | Agent | `punch-builder-scoped` | Approved Plan task touches HTTP tests in `src/tests/`. |
| [`punch-build-k6-browser`](../../.github/prompts/punch-build-k6-browser.prompt.md) | Build | Agent | `punch-builder-scoped` | Approved Plan task touches Browser tests (currently deferred). |
| [`punch-build-data-harvest`](../../.github/prompts/punch-build-data-harvest.prompt.md) | Build | Agent | `punch-builder-scoped` | Approved Plan task changes an artifact, log, or report. |
| [`punch-verify`](../../.github/prompts/punch-verify.prompt.md) | Verify | Agent / Ask | `punch-verifier` | Build is complete; you need `reports/state/punch-run.json` evidence. |
| [`punch-review`](../../.github/prompts/punch-review.prompt.md) | Review | Ask | `punch-reviewer` | Verify passed; audit the diff before Ship. |
| [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | Ship | Agent (mechanical only) | `punch-reviewer` | Review approved; commit, push, open PR. **Never merges.** |

## One prompt per phase — except Build

The Define, Spec, Plan, Verify, Review, and Ship phases each have a
single prompt. Splitting them by ticket type would multiply maintenance
without adding value.

Build is the exception: it has five domain prompts (orchestrator,
compose, k6-http, k6-browser, data-harvest). Build is the only phase
that *edits product code*; per-domain prompts let each Build call
declare allowed / read-only / forbidden paths tuned to that domain. The
result is tighter scope discipline and clearer reviews.

## Prompt contract

Every prompt file under `.github/prompts/` must declare:

```yaml
---
mode: ask | edit | agent
description: <one line, used by the Copilot UI>
---
```

And cover, in this order:

1. **Lifecycle phase** — which of Define / Spec / Plan / Build / Verify
   / Review / Ship this serves.
2. **Mode** — Ask, Agent (scoped), or Agent (mechanical only).
3. **Owner skill(s)** — which of the six skills this prompt activates.
4. **Agent** — which of the five agent personas runs this prompt.
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
[`punch-governance-review`](../../.github/skills/punch-governance-review/SKILL.md)
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
