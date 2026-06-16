# Prompt Registry

The MVP supports exactly **seven** prompts: one per lifecycle phase plus a
dedicated governance audit. Each prompt has a single, well-defined entry
point. See `.github/prompts/` for the prompt bodies.

## Active prompts

| Prompt | Lifecycle phase | Mode | Use when |
|---|---|---|---|
| [`punch-understand`](../../.github/prompts/punch-understand.prompt.md) | Understand | Ask | You need to trace behavior or understand a failure before changing anything. |
| [`punch-shape`](../../.github/prompts/punch-shape.prompt.md) | Shape | Ask (plan discipline) | You have a question answered and need a scoped implementation plan. |
| [`punch-build-slice`](../../.github/prompts/punch-build-slice.prompt.md) | Build | Agent | You have a confirmed Shape plan and want to execute **one** numbered step. |
| [`punch-verify`](../../.github/prompts/punch-verify.prompt.md) | Verify | Agent / Ask | Build is complete; you need `reports/state/punch-run.json` evidence. |
| [`punch-review`](../../.github/prompts/punch-review.prompt.md) | Review | Ask | Verify passed; audit the diff before Ship. |
| [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | Ship | Agent (mechanical only) | Review approved; commit, push, open PR. **Never merges.** |
| [`punch-governance-audit`](../../.github/prompts/punch-governance-audit.prompt.md) | cross-cutting | Ask | A PR touches `.github/` or `docs/ai/`, or as a periodic governance check. |

## One prompt per phase

Avoid "fast" and "deep" variants. The lifecycle is the unit of variation —
not the prompt. If a phase needs more time, run the prompt longer; do not
fork it.

## Prompt contract

Every prompt file under `.github/prompts/` must declare:

```yaml
---
mode: ask | edit | agent
description: <one line, used by the Copilot UI>
---
```

And cover, in this order:

1. **Lifecycle phase** — which of Understand / Shape / Build / Verify /
   Review / Ship this serves.
2. **Mode** — Ask, Agent (scoped), or Agent (mechanical only).
3. **Owner skill** — which of the three skills, if any, this prompt activates.
4. **When to use** — concrete trigger.
5. **Inputs** — what the agent needs to be given.
6. **What to do** — numbered, finite, terminating steps.
7. **Expected output** — the artifact the prompt produces.
8. **Validation gate** — what advances the change to the next phase.

If a new prompt is proposed, the `punch-governance-audit` skill checks the
phase is not already covered and that the file follows this contract.

## Why not more prompts

A prompt per lifecycle phase is enough to drive a complete change. Each
extra prompt is one more interface to maintain, one more place for guidance
to drift. Add a new prompt only when:

- A real recurring task does not fit any existing phase, **and**
- Splitting it from an existing prompt would shrink, not duplicate.
