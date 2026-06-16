# Validation Workflow

A change is not "done" until it has produced **validation evidence**. This
file specifies what evidence looks like and how to produce it.

## Evidence contract

Every Verify run writes a single canonical artifact:

```
reports/state/punch-run.json
```

Schema (informal — produced by `src/punch/__main__.py`):

```json
{
  "command": "run",
  "tests": ["smoke", "gate", "journey"],
  "results": [
    {"test": "smoke",   "exitCode": 0, "passed": true},
    {"test": "gate",    "exitCode": 0, "passed": true},
    {"test": "journey", "exitCode": 0, "passed": true}
  ],
  "exitCode": 0,
  "passed": true,
  "startedAt": "<ISO-8601 UTC timestamp>",
  "durationSeconds": 78.3
}
```

In addition, each test writes its own evidence under `reports/`:

| Test | Artifacts |
|---|---|
| smoke   | `smoke-report.html`, `smoke.json` |
| gate    | `catalog-gate-report.html`, `catalog-gate.json` |
| journey | `order-journey-report.html`, `order-journey.json`, `state/test-context.json` |

When `--collect-logs` is set, `reports/logs/{gateway,catalog,orders,postgres}.log`
are also written.

## How to validate the MVP locally

```bash
bin/punch doctor              # Confirm host has docker + python
bin/punch run smoke           # Fastest signal that the stack is healthy
bin/punch run all --collect-logs
cat reports/state/punch-run.json
```

The final `cat` must show `"passed": true`.

## How to validate failure behavior

```bash
TARGET_BASE_URL=http://does-not-exist.invalid bin/punch run smoke || echo "FAILED as expected"
cat reports/state/punch-run.json
```

The artifact must show `"passed": false` and a non-zero exit code. If the
artifact is missing, the orchestrator violated the "evidence first" rule.

## How to validate AI configuration

```bash
ls .github/copilot-instructions.md
ls .github/instructions/*.instructions.md
ls .github/prompts/*.prompt.md
ls .github/skills/*/SKILL.md
```

Then invoke the Review phase (`punch-review` prompt), which activates
the `punch-governance-review` skill when `.github/` or `docs/ai/` is
touched. Its expected output is a findings list ending with "Governance
is clean".

## How CI re-validates

The GitHub Actions workflow at `.github/workflows/k6.yml` runs the full
suite, collects logs, uploads `reports/` as the `performance-suite-reports`
artifact, then a second job validates the artifact contents are present.

This proves the local validation contract and the CI validation contract
produce the same evidence.

## What evidence is NOT

- A green local terminal alone (transient, not auditable).
- A passing unit test in isolation (does not exercise the stack).
- A PR description claim ("I ran it and it worked").

If `reports/state/punch-run.json` does not exist, the change has not been
verified.
