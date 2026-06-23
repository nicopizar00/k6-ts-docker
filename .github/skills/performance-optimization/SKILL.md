---
name: performance-optimization
description: Measure-first performance work for Punch's k6 perf model. Use when a gate/journey threshold regresses, when adding behavior under load, or when service latency/error-rate drifts. Adapts upstream agent-skills `performance-optimization` to k6 + Docker + Postgres; frontend/Web-Vitals guidance removed (Punch has no frontend).
applies-to: lifecycle/Build+Test — k6 perf bottlenecks in the reference services; not path-scoped
---

# Performance Optimization (Punch)

Measure before optimizing. In Punch the measurement **is** the k6 run — never
guess from reading code. Profile via `./bin/punch run gate|journey`, find the
real bottleneck, fix it, re-run, guard with a threshold.

## When to use

- A `gate`/`journey` threshold went RED (p90/p95 latency, error rate, check rate).
- Adding behavior that runs under load (new route, query, service hop).
- Suspected regression after a Build.

**Not for:** micro-optimizing without a RED threshold or measured number first.

## Workflow

```
1. MEASURE   → ./bin/punch run gate   (baseline from reports/state/punch-run.json + reports/<test>.json)
2. IDENTIFY  → read the failing threshold + service logs (reports/logs/) — the real hop
3. FIX       → address that bottleneck only
4. VERIFY    → ./bin/punch run gate again; compare numbers
5. GUARD     → keep/ tighten the k6 threshold so the regression can't return
```

## k6 signals (what to read)

| Signal | In `reports/<test>.json` | Reading |
|---|---|---|
| Latency | `http_req_duration` p90/p95/p99 | percentiles, never average — an average hides the slow tail |
| Errors | `errorRate` / failed checks | any non-zero on a gate = investigate |
| Throughput | `totalRequests`, RPS / VUs | did load actually apply? |
| Check pass | `checkPassRate` | 1.0 expected on a healthy gate |

Thresholds live at the top of each `src/tests/*.ts` (owned by
`punch-performance-test-engineer`).

## Backend bottlenecks (the reference services)

| Symptom | Likely cause | Investigation |
|---|---|---|
| One route slow | N+1 query, missing Postgres index, unoptimized query | `orders-api` query path + `docker/postgres/init.sql` |
| All routes slow | connection pool exhaustion, CPU/memory, gateway proxy overhead | service logs in `reports/logs/` |
| Intermittent | lock contention, GC pause, cold container | repeated runs; healthcheck gating |

Common fixes: collapse N+1 into one query; add the missing index; bound/ paginate
list endpoints; cache rarely-changed reads; pin/raise the pool size. Keep the fix
inside the owning layer (services = `punch-runtime-engineer` domain).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "We'll optimize later" | Perf debt compounds. Fix obvious anti-patterns now. |
| "It's fast locally" | Measure under k6 load, not a single curl. |
| "This optimization is obvious" | If you didn't run the gate, you don't know. |

## Red flags

- Optimizing with no baseline k6 number.
- Loosening a threshold instead of fixing the cause.
- N+1 / unbounded fetch in a service path.
- List endpoint without pagination.

## Verification

- [ ] Before/after numbers exist (from `reports/<test>.json`).
- [ ] The specific bottleneck is named and addressed.
- [ ] `./bin/punch run gate` → `reports/state/punch-run.json` `passed: true`.
- [ ] Threshold guards the regression; no behavior broke (`run all`).

(CI is external to Punch — it re-runs the same gate, it is not where you tune.)
