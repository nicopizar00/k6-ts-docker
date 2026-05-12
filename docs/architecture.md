# Architecture

## Execution chain

```
TypeScript source  →  esbuild  →  Docker image  →  k6 execution  →  reports
```

This linear flow is preserved by every change. Do not add branches or shortcuts.

## Folder map

| Path | Responsibility |
|------|-----------------|
| `src/tests/` | k6 test scenarios authored in TypeScript. One file per scenario (e.g., `smoke.ts`, `stress.ts`). |
| `dist/` | Bundler output — single ES module consumed by k6. Gitignored. |
| `docker/Dockerfile` | Builds the k6 runner image from `grafana/k6`. Copies the bundle and runs it. |
| `reports/` | JSON and summary output from k6 runs. Gitignored. CI uploads these as artifacts. |
| `docs/` | AI-friendly documentation: architecture, how-tos, decision log. |

## Tech stack

- **k6** — Load testing runtime (executes bundled JS).
- **TypeScript** — Authoring tests with types and editor support.
- **esbuild** — Bundles TypeScript to a single ES module k6 can run.
- **Docker** — Reproducible execution environment based on `grafana/k6`.
- **GitHub Actions** — CI entrypoint (future: runs the Docker image, uploads reports).

## Current state

- ✓ TypeScript + esbuild build working
- ✓ Dockerfile configured to run bundled tests
- ✓ One smoke test example (`src/tests/smoke.ts`)
- ⏳ GitHub Actions workflow (planned)
- ⏳ Report collection and artifact upload (planned)

## Why this shape

- **No Node module deps in tests** — k6 runs in its own runtime, cannot require Node packages. esbuild handles the bundle.
- **Single bundle file** — Keeps Docker image simple and k6 execution straightforward.
- **Docker first** — Local and CI runs are identical; no "works on my machine" surprises.
