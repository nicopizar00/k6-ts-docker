---
agent: punch-release-captain
description: Phase 7 — Ship. punch-release-captain fans out the specialists, decides GO | NO-GO + rollback, then mechanically commits/pushes/opens the PR. Humans merge.
---
# Punch — Ship

**Lifecycle phase:** Ship
**Mode:** Agent (gate + mechanical finalization — no logic edits)
**Owner skill:** [`punch-git-workflow-and-versioning`](../skills/punch-git-workflow-and-versioning/SKILL.md) (commit/branch discipline)
+ [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md) (`git` + `gh` mechanics)
+ [`punch-ai-governance`](../skills/punch-ai-governance/SKILL.md) (readiness summary)
**Agent:** [`punch-release-captain`](../agents/punch-release-captain.agent.md) — owns the gate (fan-out → GO/NO-GO + rollback) **and** the mechanical commit/push/PR.
**Operating comms:** Caveman **`full`** (per-phase canon). Release decision is a persistent artifact — no Wenyan. Canon: [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).

## When to use

Review approved change. Ship handles mechanical steps: commit, push, open PR, **and produce ship-readiness summary**. Ship never merges, never tags releases, never pushes direct to `main`.

## Inputs

- Approved Review report.
- Branch + target base branch (default `main`).
- Test evidence path.

## Pre-ship fan-out (parallel, read-only)

Before any git step, fan out **in parallel** to the trio for a final gate:

- [`punch-code-reviewer`](../agents/punch-code-reviewer.agent.md) — 5-dimension diff review.
- [`punch-security-auditor`](../agents/punch-security-auditor.agent.md) — secrets/PII/input/supply-chain pass.
- [`punch-test-engineer`](../agents/punch-test-engineer.agent.md) — independent test verdict (`./bin/punch run`).

Each returns its own verdict. **Any REQUEST CHANGES / FAIL → stop, do not commit**,
return findings (→ Plan/Build). Ship proceeds only when all three clear (or a human
explicitly overrides). The trio are leaves here — they report, they don't act.

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
   literally. Test plan section points at Test evidence.
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
  - Pre-ship fan-out: punch-code-reviewer <APPROVE|CHANGES> · punch-security-auditor <PASS|FAIL> · punch-test-engineer <PASS|FAIL|BLOCKED>

Known risks:
  - <one-liner or "none">

Operational impact:
  - artifacts changed: <none, or contract entries>
  - service contract changed: <none, or details>
  - host requirements changed: <none, or details>

Documentation status: <updated / not applicable>

Rollback plan: <how to revert — branch/commit, revert PR, data/migration notes>

Release decision: GO | NO-GO
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

Pipeline (GitHub Actions) re-runs Test in CI. Human reviews PR
and merges. Ship complete when PR merged by human.
