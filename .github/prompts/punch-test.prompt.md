---
agent: punch-test-engineer
description: Test phase — the canonical, independent test gate for the current change. Prove-It / TDD at the k6 check & threshold level via ./bin/punch; returns PASS | FAIL | BLOCKED.
---
# Punch — Test

**Lifecycle phase:** Test (TDD/Prove-It; the verification phase — addyosmani `/test`)
**Mode:** Agent (runs `./bin/punch`; no code authoring)
**Owner skill:** [`test-driven-development`](../skills/test-driven-development/SKILL.md) (method)
+ [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md) (k6 domain)
**Agent:** [`punch-test-engineer`](../agents/punch-test-engineer.agent.md) — the independent test gate; the only final PASS/FAIL authority. Builder may lazy-load `test-driven-development` while building, but does not own this gate.

## When to use

*Prove* change with test before+after build — upstream `test` command, applied to Punch k6 + evidence model:

- Bug report → confirm failing check/threshold reproduces it (RED) before Build fixes, then confirm pass (GREEN).
- New behavior → confirm new check/threshold fails vs current code, then passes once Build implements.

Authoring test = Build task ([`punch-build`](punch-build.prompt.md) → `punch-performance-test-engineer`); this prompt **runs and judges** test, no write.

## Inputs

- Check/threshold (or test) expressing expected behavior.
- Plan task or change under test.

## What to do

1. Find smallest test capturing behavior (k6 `check` or threshold in relevant `src/tests/*.ts`).
2. Run via `./bin/punch run <test>`, confirm **fails for right reason** (RED) — failing threshold/check, not setup error.
3. Hand to Build to implement (no authoring here).
4. After Build, run `./bin/punch run <test>` again, confirm **GREEN**.
5. Confirm `reports/state/punch-run.json` records run.
6. If no clean fail-then-pass, **stop**, return to Plan.

## Expected output

- **Verdict: PASS | FAIL | BLOCKED.**
- Test (check/threshold) used; commands run with exit codes.
- RED evidence (command + failing result) and, after Build, GREEN evidence;
  `reports/state/punch-run.json` `passed:` value.
- Failures with file/check/threshold references; missing coverage (or "none").
- Handoff: Review on PASS · Plan/Build if product code must change · human on
  environment/pre-existing failure.

## Delegation (bounded worker)

`punch-test-engineer` is the Test coordinator. It may spawn one **read-only**
cavecrew leaf worker (depth-1),
[`cavecrew-investigator`](../agents/cavecrew-investigator.agent.md), to locate
the change's `src/tests/*.ts` checks/thresholds and coverage gaps. It only
*locates*: the **PASS | FAIL | BLOCKED verdict stays this gate's own**, never
delegated.

## Validation gate

Clean RED→GREEN transition with `reports/state/punch-run.json` recording the passing run — the end-to-end evidence gate.

## Boundary rules

- Never run `docker run`/`docker compose` directly or k6 on host — `./bin/punch` only.
- Never edit source to pass test — authoring/fixing = Build task.

## Operating comms

Caveman **`ultra`** for Test; execution sub-agents `wenyan`. Evidence (RED/GREEN
output, commands, `reports/state/punch-run.json`) verbatim. Canon:
[`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md).
