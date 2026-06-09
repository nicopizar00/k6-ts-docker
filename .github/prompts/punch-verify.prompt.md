---
mode: agent
description: Phase 4 — Verify. Produce validation evidence for the current changes.
---

# Punch — Verify

**Lifecycle phase:** Verify
**Mode:** Agent (runs commands) or Ask (interprets existing artifacts)
**Owner skill:** `punch-orchestration` (drives `bin/punch`) +
`punch-performance-k6` (interprets k6 evidence)

## When to use

Build is complete and you need evidence the change works. Verify runs the
orchestrator end-to-end against real Docker, then reports pass/fail.

## Inputs

- The slice or full plan being verified.
- (Optional) `TARGET_BASE_URL` if the run is against an external service.

## What to do

1. `bin/punch doctor` — confirms host prerequisites.
2. `bin/punch run smoke` — fastest signal the stack is healthy.
3. Run the test(s) most relevant to the change:
   - HTTP gate change → `bin/punch run gate`
   - Journey change → `bin/punch run journey`
   - End-to-end → `bin/punch run all --collect-logs`
4. Confirm `reports/state/punch-run.json` was written and `passed: true`.
5. If anything fails, **stop**. Do not patch silently — return to Shape with
   the failure as a new Understand input.

## Expected output

- The exit code of each run.
- A pointer to `reports/state/punch-run.json` and the relevant HTML reports.
- One sentence: "Change is verified" or "Change failed verification — see X".

## Validation gate

- Pass: proceed to Review.
- Fail: loop back to Shape (or Understand). Never proceed to Ship on a fail.
