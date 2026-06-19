---
agent: punch-verifier
description: Test phase — drive a change with the Prove-It / TDD discipline at the k6 check & threshold level, executed through ./bin/punch.
---
# Punch — Test

**Lifecycle phase:** Test (TDD/Prove-It companion to Verify)
**Mode:** Agent (runs `./bin/punch`; no code authoring)
**Owner skill:** [`test-driven-development`](../skills/test-driven-development/SKILL.md) (method)
+ [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md) (k6 domain)
**Agent:** [`punch-verifier`](../agents/punch-verifier.agent.md)

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

- Test (check/threshold) used.
- RED evidence (command + failing result) and, after Build, GREEN evidence.
- `reports/state/punch-run.json` `passed:` value.
- One sentence next step (continue to Verify/Review, or return to Plan).

## Validation gate

Clean RED→GREEN transition with `reports/state/punch-run.json` recording passing run. Full end-to-end evidence = [`punch-verify`](punch-verify.prompt.md).

## Boundary rules

- Never run `docker run`/`docker compose` directly or k6 on host — `./bin/punch` only.
- Never edit source to pass test — authoring/fixing = Build task.

## Operating comms (enforced)

Caveman enforced for Test. Activate `caveman` Agent Skill **once** on entering phase (per `using-agent-skills`), then rely on persistence:

- **Governance tier** (this prompt + `punch-verifier` judge): **`ultra`**.
- **Execution tier** (test-execution sub-agent path): **`wenyan`** — max efficiency.
- **Evidence never compressed** — RED/GREEN output, commands, `reports/state/punch-run.json` values quoted verbatim in any mode.

Full policy (tiers, modes, evidence list, Auto-Clarity, priority order) lives in [`punch-build-caveman`](../skills/punch-build-caveman/SKILL.md) + [ADR 0003](../../docs/ai/decisions/0003-caveman-build-comms.md) — not restated here.
