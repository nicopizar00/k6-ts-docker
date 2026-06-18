---
agent: punch-verifier
description: Test phase — drive a change with the Prove-It / TDD discipline at the k6 check & threshold level, executed through ./bin/punch.
---

# Punch — Test

**Lifecycle phase:** Test (the TDD/Prove-It companion to Verify)
**Mode:** Agent (runs `./bin/punch`; does not author code)
**Owner skill:** [`test-driven-development`](../skills/test-driven-development/SKILL.md) (the method)
+ [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md) (the k6 domain)
**Agent:** [`punch-verifier`](../agents/punch-verifier.agent.md)

## When to use

You want to *prove* a change with a test before and after it is built —
the upstream `test` command, applied to Punch's k6 + evidence model:

- A bug report → confirm a failing check/threshold reproduces it (RED) before a
  Build fixes it, then confirm it passes (GREEN).
- A new behavior → confirm the new check/threshold fails against current code,
  then passes once Build implements it.

Authoring the test itself is a Build task ([`punch-build`](punch-build.prompt.md) →
`punch-performance-test-engineer`); this prompt **runs and judges** the test, it
does not write it.

## Inputs

- The check/threshold (or test) that expresses the expected behavior.
- The Plan task or change under test.

## What to do

1. Identify the smallest test that captures the behavior (a k6 `check` or a
   threshold in the relevant `src/tests/*.ts`).
2. Run it via `./bin/punch run <test>` and confirm it **fails for the right
   reason** (RED) — a failing threshold/check, not a setup error.
3. Hand back to Build to implement the change (do not author it here).
4. After Build, run `./bin/punch run <test>` again and confirm **GREEN**.
5. Confirm `reports/state/punch-run.json` records the run.
6. If it cannot be made to fail-then-pass cleanly, **stop** and return to Plan.

## Expected output

- The test (check/threshold) used.
- RED evidence (command + failing result) and, after Build, GREEN evidence.
- `reports/state/punch-run.json` `passed:` value.
- One sentence on the next step (continue to Verify/Review, or return to Plan).

## Validation gate

A clean RED→GREEN transition with `reports/state/punch-run.json` recording the
passing run. Full end-to-end evidence is [`punch-verify`](punch-verify.prompt.md).

## Boundary rules

- Never run `docker run`/`docker compose` directly or k6 on the host — `./bin/punch` only.
- Never edit source to make a test pass — authoring/fixing is a Build task.

## Operating comms (enforced)

Caveman is enforced for Test. Activate the `caveman` Agent Skill **once** on
entering the phase (per `using-agent-skills`), then rely on its persistence:

- **Governance tier** (this prompt + the `punch-verifier` judge): **`ultra`**.
- **Execution tier** (the test-execution sub-agent path): **`wenyan`** — maximum
  efficiency.
- **Evidence is never compressed** — RED/GREEN output, commands, and
  `reports/state/punch-run.json` values are quoted verbatim in any mode.

Full policy (tiers, modes, evidence list, Auto-Clarity, priority order) lives in
[`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md) +
[ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md) — not restated here.
