# Plan: Lean AI Config Cleanup

## Summary

Clean up stale AI-config and documentation references to the deleted split build prompt model. The work updates live docs and registries to the current `punch-build` dispatcher model, and reconciles stale spec/plan docs that still mention `punch-build-k6-*` or `punch-build-orchestrator`.

## Scope

This is a docs-only governance wave. No runtime/product code changes are required.

## Tasks

### A-01: Fix current AI-config docs and registries
- Task ID: A-01
- Goal: Replace obsolete `punch-build-k6-*` / `punch-build-orchestrator` references with the current single `punch-build` + dispatcher model in live docs and registries.
- Allowed edit paths:
  - `CLAUDE.md`
  - `README.md`
  - `AGENTS.md`
  - `docs/ai/skill-registry.md`
  - `.github/copilot-instructions.md`
- Read-only context paths:
  - `.github/agents/**`
  - `.github/prompts/**`
  - `.github/skills/**`
  - `.github/instructions/**`
  - `docs/ai/**`
  - `docs/architecture/**`
- Forbidden paths:
  - `src/**`
  - `docker/**`
  - `docker-compose.yml`
  - `reports/**`
- Expected diff size: ~30 lines
- Validation commands:
  - Run `punch-ai-governance` audit on the touched files.
  - Confirm `grep -R "punch-build-k6-http\|punch-build-k6-browser\|punch-build-orchestrator" .` returns no stale matches in live docs.
- Rollback notes: revert the touched docs/files to restore the prior lifecycle wording.
- Human checkpoint: human approval required before Build.
- Build prompt: `punch-document`

### A-02: Reconcile stale spec/plan docs
- Task ID: A-02
- Goal: Clean up or archive spec and plan documentation that still references deleted split build prompts and old AI-config architecture.
- Allowed edit paths:
  - `docs/architecture/specs/plan-bff-checkout-journey.md`
  - `docs/architecture/specs/plan-bff-checkout-journey-test.md`
  - `docs/architecture/specs/lean-ai-config.md`
  - `docs/ai/history/**`
- Read-only context paths:
  - `.github/**`
  - `docs/ai/**`
  - `AGENTS.md`
  - `CLAUDE.md`
- Forbidden paths:
  - `src/**`
  - `docker/**`
  - `docker-compose.yml`
  - `reports/**`
- Expected diff size: ~20 lines
- Validation commands:
  - Run `punch-ai-governance` audit on the touched files.
  - Confirm `grep -R "punch-build-k6-http\|punch-build-orchestrator" .` returns no stale matches in the reconciled spec/docs.
- Rollback notes: restore the original spec documentation or move archived content back if verification fails.
- Human checkpoint: human approval required before Build.
- Build prompt: `punch-document`

## Order of execution
1. A-01: update live AI-config docs and registries.
2. A-02: reconcile stale spec and plan docs.
3. Verify with `punch-ai-governance` and grep cleanup.

## Notes
- This wave is purely AI-config/document maintenance and should be verified via the governance audit, not via `./bin/punch` runtime commands.
- Until this plan lands, any builder or reviewer should treat `punch-build-k6-*` / `punch-build-orchestrator` references as stale artifacts from the prior prompt split.
