# How to Run

## Prerequisites

- Node.js (v18+)
- Docker (for the actual k6 run)

## Local execution

### 1. Install dependencies
```bash
npm install
```

### 2. Build the bundle
```bash
npm run build
```

This runs esbuild and outputs `dist/smoke.js`. esbuild:
- Bundles TypeScript to a single ES module
- Marks k6 packages (`k6`, `k6/*`) as external so they're provided by the k6 runtime
- Outputs ES2015 format compatible with k6

### 3. Build the Docker image
```bash
npm run docker:build
```

This builds the image using `docker compose`. The Dockerfile:
- Starts from `grafana/k6:latest`
- Copies the bundled script into the container
- Sets k6 as the entrypoint with the script as the command

### 4. Run the test
```bash
npm run test:smoke
```

This uses `docker compose run` to execute the container, which runs k6 on the bundled script.

Output appears on stdout/stderr. k6 can be configured to export reports via environment variables or CLI flags (future step).

## Adding a new test

1. Create `src/tests/mytest.ts` following k6 patterns (see `smoke.ts`).
2. Add a build script to `package.json`:
   ```json
   "build:mytest": "esbuild src/tests/mytest.ts --bundle --platform=browser --target=es2015 --format=esm --external:k6 --external:'k6/*' --outfile=dist/mytest.js"
   ```
3. Update the Dockerfile `COPY` and `CMD` or create a separate docker-compose service for it.

## Troubleshooting

- **Build fails** — Check `tsconfig.json` and that esbuild is installed (`npm ls esbuild`).
- **Docker build fails** — Ensure `dist/smoke.js` exists (`npm run build` first).
- **Test fails in Docker but works locally** — Docker runs the bundled JS, not TypeScript. Rebuild after changes.
