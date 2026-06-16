GitHub Copilot — Repository Instructions (always-on)

These rules apply to **every** Copilot session in this repository. They are deliberately short. Detailed guidance lives in `docs/ai/operating-protocol.md` and the path-specific files under `.github/instructions/`.

## Non-negotiables

1. Docker First execution. Tests, services, and bundling run inside Docker. The host needs only Docker and a stdlib Python 3 runtime.
2. Python orchestration façade. The user-facing CLI is `bin/punch` (stdlib-only Python). Do not introduce host-side Node, npm, k6, or any pip-installed package.
3. k6 is the performance execution engine. No other load-test tool.
4. Lifecycle-driven work. Every change follows Understand → Shape → Build → Verify → Review → Ship.
5. Validation evidence is mandatory. A change is not "done" until `reports/state/punch-run.json` or equivalent validation artifacts exist.

## Lifecycle entry points

Understand: `.github/prompts/punch-understand.prompt.md` (Ask)
Shape: `.github/prompts/punch-shape.prompt.md` (Plan)
Build: `.github/prompts/punch-build-slice.prompt.md` (Agent)
Verify: `.github/prompts/punch-verify.prompt.md` (Agent / Ask)
Review: `.github/prompts/punch-review.prompt.md` (Ask)
Ship: `.github/prompts/punch-ship.prompt.md` (Agent — mechanical only)

## Maintenance Matrix (file-level change cascade)

This matrix maps a change in one area to the places reviewers and agents must check/adjust. Use it to populate PR checklists and to guide Copilot-style agents.

1) src/tests/* (k6 TypeScript tests)
   - When tests are added/removed/renamed:
     - Update Docker build expectations (dist/* bundling) — ensure new test is bundled during image build.
     - Update `.github/workflows/k6.yml` if the test should be part of CI (add run step and artifact expectations).
     - Update `AGENTS.md` & `CONTRIBUTING.md` to reflect new test semantics if public-facing.
     - Update `reports/` expected filenames and `validate-artifacts` job list if output names differ.

2) dist/* and build pipeline (esbuild outputs)
   - When bundle shape or output file names change:
     - Update Dockerfiles that copy `dist/` into k6 image build context (docker/k6.Dockerfile, docker-compose.yml if scripts path changes).
     - Update CI workflow artifact list and validation checks in `.github/workflows/k6.yml`.
     - Add a smoke validation in `copilot-setup-steps.yml` for local contributor verification.

3) docker/*.Dockerfile, docker-compose.yml
   - When images, exposed ports, or service names change:
     - Update `.mcp.json` service entries and AGENTS.md ports.
     - Update `.github/workflows/k6.yml` job steps (service names used in docker compose commands and log collection loop).
     - Update CONTRIBUTING.md run examples and docs/how-to-run.md.

4) src/services/* (gateway, catalog, orders)
   - When API surface (paths, ports) or behavior changes:
     - Update tests under src/tests/* that call those endpoints.
     - Update report parsing assumptions in src/tests/support/report.ts if response shapes change.
     - Update integration steps in CI workflow and any healthcheck commands.

5) src/services/orders/db schema (docker/postgres/init.sql)
   - When schema changes:
     - Bump migration notes in AGENTS.md and CHANGELOG.md.
     - Update seed/init SQL and ensure CI uses a fresh volume or includes a migration step.
     - Verify order-journey test still validates created entity fields.

6) bin/punch and src/punch/* (orchestration CLI)
   - When CLI flags, subcommands, or behavior change:
     - Update README quick-start commands, CONTRIBUTING.md, and .github/workflows/copilot-setup-steps.yml to reflect new usage.
     - Ensure changes remain stdlib-only; flag any accidental pip/npm additions in review.

7) reports/ shape and filenames
   - When report names or content change:
     - Update the `validate-artifacts` list in `.github/workflows/k6.yml` and the job summary table.
     - Update AGENTS.md and docs/validation/README.md with new artifact mapping.

8) package.json (root and src/services/orders)
   - When dependencies change or new scripts are added:
     - Update Dockerfile layers that run `npm ci` in the builder stage.
     - Add Dependabot ignores or exceptions (if a pinned package requires manual upgrades).
     - Update .mcp.json only if a new external service is introduced.

9) .github/workflows/* and action usage
   - When workflow triggers, job names, or upload artifact paths change:
     - Update AGENTS.md and README documentation that reference workflow semantics.
     - Keep CI workflow names stable — agents and dashboards look up by name.

10) docs/ and README.md
    - When documentation pages move or rename:
      - Update cross-references in AGENTS.md, CONTRIBUTING.md, and .github/copilot-setup-steps.yml.

## PR reviewer checklist (auto-apply in PR template suggestions)
- [ ] Does the change run inside Docker locally using `./bin/punch`?
- [ ] Are artifacts produced in `reports/` and validated by CI expectations?
- [ ] If code changed under src/tests/, are dist bundles and CI steps updated?
- [ ] If schema or DB changes were made, are migration/seed steps included?
- [ ] Docs updated (README / AGENTS.md / CHANGELOG.md) when behavior or public interfaces change.
- [ ] No host-side tool assumptions (no host npm/k6/pip required)

## PR review patterns mined from history

Repository PR history contains limited explicit review comments. Where history is sparse, follow the above matrix strictly and prefer small, verifiable PRs with a local `./bin/punch run smoke` validation step.

If additional recurring review guidance appears in future PRs, the maintenance matrix should be updated to reflect it.

## When in doubt

Refer to `docs/ai/operating-protocol.md` and the instruction fragments under `.github/instructions/`. When proposing changes that touch multiple matrix rows, document the verification plan in the PR description.

