---
name: source-driven-development
description: Grounds framework-specific decisions in official documentation. Use in Build when implementing against k6, Docker, Postgres, or esbuild APIs where correctness depends on version. Verify, cite, and let the user check your sources — don't implement from memory.
applies-to: lifecycle/Build — invoked when writing framework-specific code; not path-scoped
---

# Source-Driven Development

## In Punch

Invoked during Build when correctness depends on a framework's current API.
Punch's relevant sources:

| Area | Official source |
|---|---|
| k6 (checks, thresholds, scenarios, `handleSummary`, `k6/http`, `SharedArray`) | `grafana.com/docs/k6` |
| Docker / Compose (multi-stage builds, healthchecks, `depends_on`) | `docs.docker.com` |
| Postgres (queries, `init.sql`, types) | `postgresql.org/docs` |
| esbuild (bundling options, ESM output) | `esbuild.github.io` |
| HTTP semantics (status codes, methods) | MDN (`developer.mozilla.org`) |

Copilot can fetch these. Pin to the **version in use**: k6 image tag in
`docker/k6.Dockerfile`, Postgres 16, esbuild/TS in `package.json`.

## Overview

Every framework-specific decision must trace to official documentation. Training
data goes stale; APIs deprecate; best practices evolve. Verify, cite, and let the
user check the source.

## When to Use

- Implementing against a framework API where the version matters (k6 thresholds
  syntax, `handleSummary` signature, Compose healthcheck schema, a `pg` call).
- Building patterns that get copied across the suite (a new test template).
- Any time you're about to write framework-specific code from memory.

**When NOT to use:** pure logic that's version-independent (loops, conditionals),
renames/typos, or when the user asked for speed.

## The Process: DETECT → FETCH → IMPLEMENT → CITE

### 1. Detect stack and versions

State what you found, explicitly:

```
STACK DETECTED:
- k6 grafana/k6:0.55.0 (from docker/k6.Dockerfile)
- esbuild ^0.x, TypeScript ^5.x (from package.json)
- Postgres 16 (from docker-compose.yml / docker/postgres)
→ fetching official docs for the relevant APIs.
```

If a version is ambiguous, **ask** — the version determines which pattern is correct.

### 2. Fetch the specific page

Fetch the exact page for the API, not the homepage. Source authority order:
official docs → official blog/changelog → web standards (MDN) → runtime/compat.
**Never** cite Stack Overflow, tutorials, or your own training data as primary.

```
BAD:  read the k6 homepage
GOOD: read grafana.com/docs/k6/latest/using-k6/thresholds/
```

When official sources conflict (a migration guide vs the reference), surface it and
verify against the version in use.

### 3. Implement following documented patterns

Use the documented API signatures, not remembered ones. If the docs deprecate a
pattern, don't use it. If the docs don't cover something, flag it as unverified.
When the docs conflict with existing repo code, **surface the choice, don't silently
pick**:

```
CONFLICT: existing tests declare thresholds inline; the k6 docs also show a
scenarios-based form. Options: A) match existing tests (inline) — consistent with
the suite; B) docs' scenarios form. → which do you prefer?
```

### 4. Cite your sources

Every framework-specific pattern gets a citation the user can check:

```typescript
// k6 thresholds gate the run (abortOnFail stops early).
// Source: https://grafana.com/docs/k6/latest/using-k6/thresholds/
export const options = { thresholds: { http_req_failed: ['rate<0.01'] } };
```

Rules: full URLs, prefer deep links with anchors, quote the passage for non-obvious
decisions. If you can't find docs, say so:

```
UNVERIFIED: no official doc found for this pattern; based on training data and may
be outdated. Verify before relying on it.
```

Honesty about what you couldn't verify beats false confidence.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident about this API" | Confidence isn't evidence; training data has outdated patterns that look correct but break against the pinned version. |
| "Fetching docs wastes tokens" | Hallucinating an API wastes more — an hour of debugging vs one fetch. |
| "The docs won't have it" | If they don't, that's signal — the pattern may not be recommended. |
| "Simple task, no need to check" | Wrong patterns become templates copied across the suite. |

## Red Flags

- Writing k6/Docker/Postgres code without checking the docs for the pinned version.
- "I believe / I think" about an API instead of citing the source.
- Citing Stack Overflow or blog posts as primary.
- Using a deprecated API because it's in training data.
- Delivering framework-specific code with no citation.

## Verification

- [ ] Versions identified from `docker/*.Dockerfile`, `docker-compose.yml`, `package.json`.
- [ ] Official docs fetched for each framework-specific pattern.
- [ ] All sources official (not blogs/SO/training data); non-trivial decisions cited with full URLs.
- [ ] No deprecated APIs (checked against the version's docs/migration notes).
- [ ] Conflicts with existing repo code surfaced to the user; unverifiable bits flagged.
