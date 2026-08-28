---
agent: agent
description: Phase 6 — Ship. This prompt fans out the specialists, decides GO | NO-GO + rollback, then mechanically commits/pushes/opens the PR. Humans merge.
---
# Punch — Ship

**Lifecycle phase:** Ship
**Mode:** Agent (generic — gate + mechanical finalization, no logic edits)
**Owner skill:** [`punch-git-workflow-and-versioning`](../skills/punch-git-workflow-and-versioning/SKILL.md) (commit/branch discipline)
+ [`punch-ai-governance`](../agents/punch-ai-governance.agent.md) (readiness summary, when the diff touches `.github/`/`docs/ai/`)
**Owner:** no dedicated persona — this prompt itself, run under generic Agent
mode, owns the gate (fan-out → GO/NO-GO + rollback) **and** the mechanical
commit/push/PR. It fans out to three specialist personas as report-only
leaves (below); it does not wrap itself in a fourth coordinator persona, so
the upstream "a persona does not invoke another persona" rule holds — the
fan-out is the prompt's own procedure, not one persona delegating to others.

## When to use

Review approved change. Ship handles mechanical steps: commit, push, open PR, **and produce ship-readiness summary**. Ship never merges, never tags releases, never pushes direct to `main`.

## Inputs

- Approved Review report.
- Branch + target base branch (default `main`).
- Test evidence path.

## Small-change exception

A change may **skip the fan-out entirely** — not just reuse evidence, forgo
invoking the trio at all — when **all** hold: single-file or near-single-file
diff, doc-only or trivially-localized (no runtime-contract impact), does not
touch `.github/**`, `docker/**`, secrets/env, or dependency manifests, and
Review already approved it. State the skip and why in the ship-readiness
summary's Pre-ship fan-out line (`skipped — <reason>`) instead of a verdict.
Any doubt about whether a change qualifies → don't skip, run the fan-out.

## Pre-ship fan-out (parallel, read-only) — reuse fresh evidence, don't duplicate gates

For everything else: before any git step, check each specialist's most recent
evidence for this diff. **Rerun a specialist only when** its evidence is
missing, stale (predates the current diff), invalidated by a changed diff
since it ran, required by a sensitive-surface rule (e.g. `.github/`, `docker/`,
secrets/env, supply chain), or explicitly requested. Otherwise **reuse** its
fresh, unchanged verdict — do not re-invoke a specialist just because Ship is
running.

For whichever of the trio needs a (re)run, fan out **in parallel**:

- [`punch-code-reviewer`](../agents/punch-code-reviewer.agent.md) — 5-dimension diff review.
- [`punch-security-auditor`](../agents/punch-security-auditor.agent.md) — secrets/PII/input/supply-chain pass.
- [`punch-test-engineer`](../agents/punch-test-engineer.agent.md) — independent test verdict (`./bin/punch run`).

Each returns its own verdict. **Any REQUEST CHANGES / FAIL → stop, do not commit**,
return findings (→ Plan/Build). Ship proceeds only when all three clear — fresh or
reused (or a human explicitly overrides). The trio are leaves here — they report,
they don't act. GO/NO-GO and the rollback plan stay mandatory regardless of reuse.

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

Validation status (per the [evidence matrix](../../docs/workflows/validation.md)):
  - Runtime-affecting: reports/state/punch-run.json: passed: <bool>; tests run: <list>
  - Documentation/Copilot-only: punch-ai-governance pass: <clean|findings> (no punch-run.json expected)
  - Pre-ship fan-out (fresh|reused|skipped — <reason> if skipped): punch-code-reviewer <APPROVE|CHANGES> · punch-security-auditor <PASS|FAIL> · punch-test-engineer <PASS|FAIL|BLOCKED>

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
