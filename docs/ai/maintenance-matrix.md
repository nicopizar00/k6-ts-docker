# Maintenance Matrix (file-level change cascade)

This matrix maps a change in one area to the places reviewers and agents
must check/adjust. Use it to populate PR checklists and to guide
Copilot-style agents.

1) src/tests/* (k6 TypeScript tests)
   - When tests are added/removed/renamed:
     - Update Docker build expectations (dist/* bundling) — ensure new test is bundled during image build.
     - Update `.github/workflows/k6.yml` if the test should be part of CI (add run step and artifact expectations).
     - Update `AGENTS.md` & `CONTRIBUTING.md` to reflect new test semantics if public-facing.
     - Update `reports/` expected filenames and `validate-artifacts` job list if output names differ.
     - Update the artifact contract entries in `.github/skills/punch-data-harvest/artifact-contract.md`.

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
     - Update the compose contract in `.github/skills/punch-docker-compose/compose-contract.md`.

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
     - Update the streaming pattern example in `.github/skills/punch-python-orchestration/examples/` if the streaming contract evolves.

7) reports/ shape and filenames
   - When report names or content change:
     - Update the `validate-artifacts` list in `.github/workflows/k6.yml` and the job summary table.
     - Update AGENTS.md and docs/validation/README.md with new artifact mapping.
     - Update the artifact contract entries in `.github/skills/punch-data-harvest/artifact-contract.md` — this is a contract change.

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

11) .github/prompts/* (prompts)
    - When prompts are added, removed, or renamed:
      - Update `docs/ai/prompt-registry.md` in the same PR.
      - Update `.github/copilot-instructions.md` lifecycle table if a phase prompt name changes.
      - Update `AGENTS.md` if the phase-to-prompt mapping changes.
      - Run `punch-governance-review` to confirm frontmatter and registry sync.

12) .github/skills/* (skills)
    - When skills are added, removed, or renamed:
      - Update `docs/ai/skill-registry.md` in the same PR.
      - Update every prompt/agent file that names the skill in its "Owner skill" / "Skill activation" section.
      - Run `punch-governance-review` to confirm references resolve.

13) .github/agents/* (agents) — new in the redesigned lifecycle
    - When agents are added, removed, or renamed:
      - Update `AGENTS.md` in the same PR.
      - Update every prompt file that names the agent in its "Agent" line.
      - Update `docs/ai/copilot-mode-mapping.md` if the phase-to-agent mapping changes.
      - Run `punch-governance-review` to confirm references resolve.
