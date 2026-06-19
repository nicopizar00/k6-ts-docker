---
agent: punch-reviewer
description: Phase 7 — Ship. Mechanical finalization; human approves merge.
---
# Punch — Ship

**Lifecycle phase:** Ship
**Mode:** Agent (mechanical only — no logic edits)
**Owner skill:** [`git-workflow-and-versioning`](../skills/git-workflow-and-versioning/SKILL.md) (commit/branch discipline)
+ [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md) (`git` + `gh` mechanics)
+ [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md) (readiness summary)
**Agent:** [`punch-reviewer`](../agents/punch-reviewer.agent.md)
**Operating comms:** Caveman **`full`** (per-phase canon). Git/`gh` commands, commit/PR text, Verify evidence verbatim; ship-readiness summary persistent artifact — no Wenyan. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Review approved change. Ship handles mechanical steps: commit, push, open PR, **and produce ship-readiness summary**. Ship never merges, never tags releases, never pushes direct to `main`.

## Inputs

- Approved Review report.
- Branch + target base branch (default `main`).
- Verify evidence path.

## What to do

1. `git status` — confirm only expected files modified.
2. `git add` in-scope files explicitly (no `git add -A`, no
   `git add .`).
3. Compose commit message:
   - One-line subject, imperative mood.
   - Body reference Plan task(s), 2–3 lines.
   - No marketing language.
4. `git commit` — signing/hooks intact (never `--no-verify`).
5. `git push -u origin <branch>` if branch local.
6. `gh pr create` using `.github/PULL_REQUEST_TEMPLATE.md` checklist
   literally. Test plan section points at Verify evidence.
7. Produce **ship-readiness summary** (see below), include
   in PR description or chat reply.
8. Return PR URL.

## Ship-readiness summary

```
Summary: <one paragraph — what the change does and why>

Completed tasks:
  - <task ID — one-line goal>
  - ...

Validation status:
  - reports/state/punch-run.json: passed: <bool>
  - Tests run: <list>

Known risks:
  - <one-liner or "none">

Operational impact:
  - artifacts changed: <none, or contract entries>
  - service contract changed: <none, or details>
  - host requirements changed: <none, or details>

Documentation status: <updated / not applicable>

Recommendation: ship | hold
  Reason: <one sentence>
```

## What NOT to do

- No merge PR. Human is final approval gate.
- No push tags, no trigger releases.
- No force-push or amend commits without explicit human approval.
- No skip hooks or signing.
- No new code in Ship. Any "while I'm here" fix returns to
  Plan.

## Validation gate

Pipeline (GitHub Actions) re-runs Verify in CI. Human reviews PR
and merges. Ship complete when PR merged by human.
