# Prompt Registry

Punch have **seven** prompts — one per lifecycle phase (Spec, Plan, Build, Test,
Review, Ship; `punch-test` is the Test/verification phase, addyosmani `/test`),
plus `punch-document` (recurring doc-reconciliation phase, orthogonal to linear
lifecycle).
Spec absorb former Define phase. Each prompt have single, well-defined entry point.
See `.github/prompts/` for prompt bodies.

## Active prompts

| Prompt | Lifecycle phase | Mode | Agent | Use when |
|---|---|---|---|---|
| [`punch-spec`](../../.github/prompts/punch-spec.prompt.md) | Spec | Ask (writes spec doc) | `punch-architect` | Request need clarifying (former Define) then specifying into goals / non-goals / acceptance criteria. |
| [`punch-plan`](../../.github/prompts/punch-plan.prompt.md) | Plan | Ask (Plan discipline) | `punch-architect` | Have Spec, need scoped tasks with allowed/read-only/forbidden paths. |
| [`punch-build`](../../.github/prompts/punch-build.prompt.md) | Build | Agent (scoped) | `punch-builder` | Approved Plan task need implementing; classifies into a subsystem (runtime or performance-test) and implements directly. |
| [`punch-test`](../../.github/prompts/punch-test.prompt.md) | Test | Agent / Ask | `punch-test-engineer` | Prove change RED→GREEN at k6 check/threshold level via `./bin/punch`; produce `reports/state/punch-run.json` evidence; final PASS/FAIL gate. |
| [`punch-review`](../../.github/prompts/punch-review.prompt.md) | Review | Ask | `punch-code-reviewer` | Test passed; audit diff before Ship. |
| [`punch-ship`](../../.github/prompts/punch-ship.prompt.md) | Ship | Agent (mechanical only) | no dedicated persona | Review approved; commit, push, open PR. **Never merges.** |
| [`punch-document`](../../.github/prompts/punch-document.prompt.md) | Documentate (recurring maintenance) | Ask / Agent | `punch-ai-governance` | Remediate doc debt + AI-artifact lifecycle in waves: verify inherited artifacts (untrusted by default), then keep / merge / compact / convert / promote / archive / delete / review. |

## One prompt per phase

Every lifecycle phase — including Build — have single prompt. Splitting by ticket
type multiply maintenance, add no value. (`punch-test` is the Test/verification
phase — addyosmani `/test`; no separate Verify prompt.)

Build's per-subsystem scope discipline moved **from prompts into the agent**:
one `punch-build` prompt activates `punch-builder`, which classifies the task
into a subsystem (runtime or performance-test) and applies that subsystem's
allowed / read-only / forbidden scope directly — no dispatch. Keeps single
Build entry point while preserving tight, reviewable scope.

`punch-document` **not** lifecycle phase — recurring maintenance workflow running
orthogonal to Spec → Ship, reconciling doc debt in waves. Earns own prompt because
fits no existing phase and reuses existing `punch-ai-governance` agent (no new
agent, no new skill).

## Prompt contract

Every prompt file under `.github/prompts/` must declare:

```yaml
---
agent: ask | agent | plan | <custom-agent-name>
description: <one line, used by the Copilot UI>
---
```

VS Code prompt files use **`agent:`** field (not `mode:`) — names built-in mode or
custom agent under `.github/agents/`. Punch prompts bind to specific custom agent
(e.g. `agent: punch-builder`).

And cover, this order:

1. **Lifecycle phase** — which of Spec / Plan / Build / Test / Review /
   Ship this serves (Spec absorb former Define).
2. **Mode** — Ask, Agent (scoped), or Agent (mechanical only).
3. **Owner skill(s)** — which skill(s) this prompt activates (domain + lifecycle).
4. **Agent** — which agent persona runs this prompt (core personas, `punch-builder`, or "no dedicated persona" for Ship's prompt-level fan-out).
5. **When to use** — concrete trigger.
6. **Pre-conditions** (Build prompts only) — Plan + task ID + human
   approval.
7. **Typical scope** (Build prompts only) — allowed / read-only /
   forbidden paths.
8. **Inputs** — what agent need given.
9. **What to do** — numbered, finite, terminating steps.
10. **Expected output** — artifact the prompt produces.
11. **Validation gate** — what advances change to next phase.

If new prompt proposed,
[`punch-ai-governance`](../../.github/agents/punch-ai-governance.agent.md)
agent checks phase / domain not already covered and file follows this contract.

## Why not more prompts

Seven prompts cover whole lifecycle. Each extra prompt one more interface to
maintain, one more place for guidance to drift. Add new prompt only when:

- Real recurring task fit no existing phase, **and**
- Splitting from existing prompt would shrink, not duplicate.

Deliberate choice was: **one prompt per phase; Build's per-domain scope lives in
engineers, not extra prompts.** Resist temptation to add `punch-spec-fast` or
`punch-review-deep`.
