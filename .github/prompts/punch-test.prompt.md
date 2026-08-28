---
agent: punch-test-engineer
description: Test phase — the canonical, independent test gate for the current change. Prove-It / TDD at the k6 check & threshold level via ./bin/punch; returns PASS | FAIL | BLOCKED.
---
# Punch — Test

**Lifecycle phase:** Test (TDD/Prove-It; the verification phase — addyosmani `/test`)
**Mode:** Agent (runs `./bin/punch`; no code authoring)
**Owner skill:** [`punch-test-driven-development`](../skills/punch-test-driven-development/SKILL.md) (method)
+ [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md) (k6 domain)
**Agent:** [`punch-test-engineer`](../agents/punch-test-engineer.agent.md) — the independent test gate; the only final PASS/FAIL authority. Builder may lazy-load `punch-test-driven-development` while building, but does not own this gate.

## When to use

*Prove* an already-Built change — upstream `test` command, applied to Punch k6 +
evidence model. Test **follows** Build, it never wraps it: Build (lazy-loading
`punch-test-driven-development` while it works) records RED before implementing
and GREEN after; this gate inspects that evidence, then independently reruns to
confirm GREEN itself.

- Bug report → Build's handoff must include a failing check/threshold (RED)
  predating the fix. Missing/unconvincing RED evidence → **BLOCKED**, back to
  Build — this gate does not author it.
- New behavior → Build's new check/threshold must have failed before
  implementation, pass after. Same BLOCKED rule if that evidence is absent.

Authoring test = Build task ([`punch-build`](punch-build.prompt.md) → `punch-performance-test-engineer`); this prompt **runs and judges** test, no write.

## Inputs

- Build's handoff: diff, check/threshold touched, RED evidence (if a
  behavioral change).
- Plan task or change under test.

## What to do

1. Read Build's handoff — diff, check/threshold, and any recorded RED evidence.
2. Behavioral change (bug fix / new behavior) with no RED evidence, or RED
   evidence that fails for the wrong reason (setup/connection error, not the
   behavior) → **stop, BLOCKED**, return to Build.
3. Independently rerun `./bin/punch run <test>` — never take Build's
   self-report as proof. Confirm **GREEN**, for the right reason.
4. Confirm `reports/state/punch-run.json` records the run (`passed: true`).
5. Classify any failure: implementation-related / environment-related / pre-existing.
6. No clean RED→GREEN story for a behavioral change → **stop, BLOCKED**, return to Build (not Plan — the task was already approved; Build's evidence is what's missing).

## Expected output

- **Verdict: PASS | FAIL | BLOCKED.**
- Test (check/threshold) used; commands run with exit codes.
- RED evidence (from Build's handoff) and this gate's own independently
  reproduced GREEN evidence; `reports/state/punch-run.json` `passed:` value.
- Failures with file/check/threshold references; missing coverage (or "none").
- Handoff: Review on PASS · Build on FAIL/BLOCKED (missing RED evidence or
  implementation failure) · human on environment/pre-existing failure.

## Delegation

`punch-test-engineer` is the Test coordinator and has no `agent` tool, so it
spawns no sub-agents. Locating the change's `src/tests/*.ts` checks/thresholds and
coverage gaps happens inline. The **PASS | FAIL | BLOCKED verdict stays this
gate's own**, never delegated.

## Validation gate

Clean RED→GREEN transition with `reports/state/punch-run.json` recording the passing run — the end-to-end evidence gate.

## Boundary rules

- Never run `docker run`/`docker compose` directly or k6 on host — `./bin/punch` only.
- Never edit source to pass test — authoring/fixing = Build task.

## Operating comms

Caveman **`ultra`** for Test. Evidence (RED/GREEN output,
commands, `reports/state/punch-run.json`) stays verbatim.
