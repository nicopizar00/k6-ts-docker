# Track A: Docker First Performance Gate

## Current baseline

The project already has a working Docker First pipeline:

- Docker Compose starts a local API service (`docker/api.Dockerfile`).
- k6 runs in Docker against that API (`docker/k6.Dockerfile`).
- GitHub Actions executes the build → API health check → k6 run → artifact upload flow.
- `bin/` scripts (`build`, `test-smoke`, `clean`) are the local Docker First interface — the host requires only Docker.

The execution chain is:

```
TypeScript source  →  esbuild  →  Docker image  →  k6 run  →  reports (JSON / summary)
```

## Track A target

Evolve this POC into a **service-owned performance gate**: a focused, portable validation tool that a single service team can own, run in CI, and interpret without infrastructure expertise.

Not a framework. Not a dashboarding solution. A gate.

## Evolution stages

Each stage is a small, reviewable PR. No stage should be skipped to accelerate a later one.

### Stage 1 — Lightweight HTML report via `handleSummary`

Add a `handleSummary` export to the smoke test that produces a self-contained HTML file alongside the existing JSON output. No new dependencies; k6 supports this natively.

### Stage 2 — Upload HTML report as GitHub Actions artifact

Extend the workflow to upload the HTML report as a named artifact. Reviewers and stakeholders can download and open it without cloning the repo.

### Stage 3 — Basic thresholds

Add k6 `thresholds` for:
- HTTP status success rate
- Error rate
- p95 response latency

The gate fails the CI job if thresholds are breached. This is the first time the pipeline provides a binary pass/fail signal.

### Stage 4 — Mock or fixture-fed API behavior

Add a simple fixture or mock mode to the local API so k6 tests can validate specific response shapes without relying on live data or external services.

### Stage 5 — Endpoint-level smoke tests

Expand `src/tests/` with individual smoke checks per endpoint. Each check is minimal: one virtual user, one request, one assertion. The goal is coverage breadth, not load.

### Stage 6 — Mini end-to-end flow

Add a scenario that chains 2–3 endpoints in sequence (e.g. create → read → delete). This validates that the API behaves correctly across a realistic usage path, not just in isolation.

### Stage 7 — `workflow_dispatch` execution profiles

Add `workflow_dispatch` inputs to the GitHub Actions workflow so operators can trigger runs with named profiles (e.g. `smoke`, `light-load`) without editing code. Profiles map to different VU counts and durations.

### Stage 8 — Consider reusable patterns (deferred)

Only after stages 1–7 are stable and the patterns have proven themselves across multiple scenarios: evaluate extracting shared helpers or a thin internal library. Do not do this earlier.

## Non-goals (for now)

- No Grafana integration.
- No claim to replace Gatling.
- No reusable framework or shared library.
- No complex scenario orchestration.
- No advanced dashboarding.
- No production-like sustained load testing.

## k6 vs Gatling: positioning note

k6 fits here as a **lightweight DevOps performance automation layer**. It is easy to embed in a Docker First CI/CD pipeline, produces portable evidence (JSON, HTML), and requires no JVM or separate infrastructure. It is well-suited for per-PR smoke gates and on-demand validation runs.

Gatling remains stronger for rich out-of-the-box reporting, complex simulation workflows, and teams that need a full performance testing platform rather than a CI gate.

These tools solve different problems. This project is firmly in k6's lane.

## Recommended next implementation PR

**Stage 1:** Add `handleSummary` to the smoke test to produce an HTML report, and extend the GitHub Actions workflow to upload it as an artifact (Stage 2 follows immediately since it is a one-line workflow addition).

This is the highest-value, lowest-risk first step: it makes test results reviewable without any new dependencies or architectural changes.
