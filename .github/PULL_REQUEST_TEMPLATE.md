## Summary

Describe the change and why it is needed.

## Changes

- What changed
- Why

## How to verify

- Commands to run locally: `./bin/punch run smoke`
- Files to check: reports/* and reports/state/punch-run.json (the canonical run evidence — `passed: true` gates the change)

## Checklist

- [ ] Ran `./bin/punch run smoke` inside Docker (no host `npm`/`k6`/`pip` required)
- [ ] Artifacts produced in `reports/`, with `reports/state/punch-run.json` recording `passed: true`
- [ ] If `src/tests/` changed: dist bundles and CI steps updated
- [ ] If schema or DB changed: migration/seed steps included
- [ ] Docs updated (README / AGENTS.md / CHANGELOG.md) when behavior or public interfaces change
- [ ] Change is small and focused (one feature / fix per PR)

## Notes for reviewers

Add any context or areas you want reviewers to focus on.
