---
agent: punch-verifier
description: Phase 5 — Verify. Produce validation evidence by running official Punch commands.
---

# Punch — Verify

**Lifecycle phase:** Verify
**Mode:** Agent (runs commands) or Ask (interprets existing artifacts)
**Owner skill:** [`debugging-and-error-recovery`](../skills/debugging-and-error-recovery/SKILL.md) (failure-handling method)
+ [`punch-python-orchestration`](../skills/punch-python-orchestration/SKILL.md)
+ [`punch-k6-testing`](../skills/punch-k6-testing/SKILL.md)
+ [`punch-data-harvest`](../skills/punch-data-harvest/SKILL.md)
**Agent:** [`punch-verifier`](../agents/punch-verifier.agent.md)

## When to use

Build reported a clean diff and you need evidence the change works.
Verify runs the orchestrator end-to-end against real Docker, then
classifies the result.

## Inputs

- The Plan task or whole Plan being verified.
- (Optional) `TARGET_BASE_URL` if the run targets an external service.

## What to do

1. `./bin/punch doctor` — confirms host prerequisites.
2. `./bin/punch run smoke` — fastest signal the stack is healthy.
3. Run the test(s) most relevant to the change:
   - HTTP gate change → `./bin/punch run gate`
   - Journey change → `./bin/punch run journey`
   - End-to-end → `./bin/punch run all --collect-logs`
4. Confirm `reports/state/punch-run.json` exists and shows `passed: true`.
5. Read the relevant HTML and JSON reports for context.
6. If anything fails, **stop**. Do not silently patch.

## Expected output

A Verify report with:

- **Commands run** — each with its exit code.
- **Artifacts produced** — paths only.
- **Result** — pass / fail.
- **If fail, classification** — implementation-related,
  environment-related, or pre-existing.
- **Minimal next action** — one sentence (continue to Review, return to
  Plan with a corrective task, or escalate to human).

## Validation gate

- Pass → Review.
- Fail (implementation) → Plan (corrective task) → Build.
- Fail (environment) → human triage.
- Fail (pre-existing) → human triage; this PR not blocked.

## Boundary rules

- Never run `docker run` or `docker compose` directly outside Punch.
  Use `./bin/punch`.
- Never run k6 on the host.
- Never edit source files to make Verify pass. (Failures classify and
  return to Plan.)
