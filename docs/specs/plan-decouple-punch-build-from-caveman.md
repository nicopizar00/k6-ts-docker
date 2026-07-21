# Plan — Decouple Punch Build from Caveman

> **Status:** Implemented 2026-07-20 — AI-01 → AI-02 → AI-03 → AI-04 complete via
> `punch-ai-governance`. Vendor hashes reconfirmed unchanged. Two known residuals
> outside this Plan's declared scope: (1) the `.claude/` Claude Code wrap layer
> (9 files) still names `punch-build-caveman` — no task above included `.claude/`;
> (2) runtime re-verification (`./bin/punch doctor` / `./bin/punch run smoke`) is
> deferred to `/punch-test`, since `punch-ai-governance` is guarded from running
> the Punch runtime. Neither blocks this Plan's own acceptance criteria, which
> covered only `.github/**` + `docs/**`.
>
> **Decision basis:** The source comparison established that Caveman is an
> output-style skill and Cavecrew is a delegation optimization, while Punch
> Build owns lifecycle behavior, scope, testing, evidence, and handoffs. This
> Plan makes that separation explicit without modifying the vendor assets.

- **Goal:** Make Punch Build fully independent of Caveman and Cavecrew while
  preserving the installed vendor skills verbatim and keeping optional prose or
  read-only worker assistance outside the Build contract.

## Invariants and acceptance criteria

1. Punch Build behaves the same when Caveman and Cavecrew are unavailable.
2. The Build prompt, Builder, and both Build engineers contain no Caveman,
   Cavecrew, Wenyan, or vendor-skill dependency.
3. `punch-builder` delegates only to `punch-runtime-engineer` or
   `punch-performance-test-engineer`; both engineers are non-spawning leaves.
4. `.agents/skills/caveman/**` and `.agents/skills/cavecrew/**` remain
   byte-for-byte unchanged.
5. Caveman remains an optional user-invoked presentation aid. It never changes
   tools, task order, scope, evidence, verdicts, or lifecycle authority.
6. Cavecrew remains optional outside Build. Read-only investigator/reviewer
   adapters may support Test or Review, but the Build-only editor adapter is
   retired.
7. Missing optional vendor skills never blocks Punch initialization or any
   lifecycle phase.

Pinned vendor hashes for the implementation and Review gates:

| Asset | SHA-256 |
|---|---|
| `.agents/skills/caveman/SKILL.md` | `e38ec671ecbee47ce234190be12615daf60ac667d775b7340d49d07f4f63c7bc` |
| `.agents/skills/caveman/README.md` | `95b62190565e0d5b21ced563cf36c0f549abe1ceceff540914102481c9c5849c` |
| `.agents/skills/cavecrew/SKILL.md` | `b74f374f6aae6e9a31e78e7d876860406fe5833378e9298536edf176c12f379b` |
| `.agents/skills/cavecrew/README.md` | `965622be25416e1c59d0f69edf359dceeebdf2fa650c3fd5c254081045f27c12` |

## Non-goals

- Do not edit, reinstall, normalize, or reformat vendor files under
  `.agents/skills/caveman/**`, `.agents/skills/cavecrew/**`, or
  `.ai-upstream/**`.
- Do not remove Caveman or Cavecrew from the repository.
- Do not change product code, Docker Compose, k6 tests, workflows, or report
  contracts.
- Do not change Test, Review, or Ship verdict ownership.
- Do not resolve the separate `/build auto`, Build-versus-Test terminal
  authority, TDD applicability, or Build-versus-Ship commit-ownership drift in
  this Plan. Those require their own Spec and Plan.

## Tasks

### AI-01 — Remove Caveman and Cavecrew from the Build entry point

- **Goal:** Make the Build prompt and coordinator express only Punch lifecycle,
  scope, engineer routing, evidence, and handoff behavior.
- **Allowed edit paths:**
  - `.github/prompts/punch-build.prompt.md`
  - `.github/agents/punch-builder.agent.md`
- **Read-only context paths:**
  - `.github/agents/punch-runtime-engineer.agent.md`
  - `.github/agents/punch-performance-test-engineer.agent.md`
  - `.github/skills/punch-incremental-implementation/SKILL.md`
  - `.github/skills/punch-test-driven-development/SKILL.md`
  - `.github/skills/punch-build-caveman/SKILL.md`
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
  - `AGENTS.md`
- **Forbidden paths:**
  - Every path not explicitly allowed above
  - `.ai-upstream/**`
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`
  - `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Remove Caveman/Wenyan communication rules and the Caveman-policy link.
  - Remove Cavecrew workers from `punch-builder`'s `agents:` roster and body.
  - Remove Cavecrew-specific report fields; retain engineer and evidence fields.
  - Preserve the single approved-task scope, engineer routing, validation, and
    Test/Review/Ship handoffs unchanged.
- **Acceptance criteria:**
  - `punch-builder` lists exactly the two Build engineers in `agents:`.
  - No case-insensitive match for `caveman`, `cavecrew`, or `wenyan` remains in
    either allowed file.
  - Build still requires approved scope and `reports/state/punch-run.json`
    evidence.
- **Expected diff size:** Approximately 60–120 lines, mostly deletions.
- **Validation commands:**
  - `rg -ni 'caveman|cavecrew|wenyan|punch-build-caveman' .github/prompts/punch-build.prompt.md .github/agents/punch-builder.agent.md` → no matches.
  - `git diff --check`
  - Read-only `punch-ai-governance` audit → clean for prompt/agent links and frontmatter.
- **Rollback notes:** Revert AI-01 as one AI-configuration commit.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration maintenance;
  never `punch-build`.

### AI-02 — Make both Build engineers non-spawning and style-neutral

- **Goal:** Remove Cavecrew delegation and Caveman output behavior from the two
  engineer personas without changing their engineering scopes.
- **Allowed edit paths:**
  - `.github/agents/punch-runtime-engineer.agent.md`
  - `.github/agents/punch-performance-test-engineer.agent.md`
- **Read-only context paths:**
  - `.github/agents/punch-builder.agent.md`
  - `docs/ai/scoped-build-policy.md`
  - `docs/ai/agent-guards.md`
  - `.github/skills/punch-python-orchestration/**`
  - `.github/skills/punch-compose-runtime/**`
  - `.github/skills/punch-data-harvest/**`
  - `.github/skills/punch-k6-testing/**`
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
- **Forbidden paths:**
  - Every path not explicitly allowed above
  - `.ai-upstream/**`
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`
  - `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Set each engineer's `agents:` list to empty.
  - Remove Cavecrew delegation sections and Wenyan/Caveman communication rules.
  - Preserve allowed/read-only/forbidden scope, domain skills, and evidence
    obligations exactly.
- **Acceptance criteria:**
  - Both engineers are non-spawning leaves.
  - No case-insensitive match for `caveman`, `cavecrew`, or `wenyan` remains in
    either engineer file.
  - Tool declarations and engineering boundaries do not expand.
- **Expected diff size:** Approximately 40–90 lines, mostly deletions.
- **Validation commands:**
  - `rg -ni 'caveman|cavecrew|wenyan|punch-build-caveman' .github/agents/punch-runtime-engineer.agent.md .github/agents/punch-performance-test-engineer.agent.md` → no matches.
  - `git diff --check`
  - Read-only `punch-ai-governance` audit → clean agent roster and tool-subset checks.
- **Rollback notes:** Revert AI-02 independently; AI-01 may remain valid.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration maintenance.

### AI-03 — Retire Build-only Cavecrew wiring and make vendor use optional

- **Goal:** Remove the unused editing worker and update governance so Caveman and
  Cavecrew are optional vendor capabilities, not Punch prerequisites.
- **Allowed edit paths:**
  - `.github/agents/punch-cavecrew-builder.agent.md` (delete)
  - `.github/agents/punch-cavecrew-investigator.agent.md`
  - `.github/agents/punch-cavecrew-reviewer.agent.md`
  - `.github/skills/punch-using-agent-skills/SKILL.md`
  - `.github/skills/punch-ai-governance/SKILL.md`
  - `.github/prompts/punch-init.prompt.md`
  - `.github/.ai-upstream/README.md`
  - `docs/ai/agent-guards.md`
  - `docs/ai/prompt-registry.md`
  - `docs/ai/skill-registry.md`
  - `AGENTS.md`
- **Read-only context paths:**
  - `.github/prompts/punch-test.prompt.md`
  - `.github/prompts/punch-review.prompt.md`
  - `.github/agents/punch-test-engineer.agent.md`
  - `.github/agents/punch-code-reviewer.agent.md`
  - `.github/agents/punch-security-auditor.agent.md`
  - `.github/copilot-instructions.md`
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
- **Forbidden paths:**
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
  - `.ai-upstream/**`
  - Every other path not explicitly allowed above
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`
  - `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Delete `punch-cavecrew-builder`; no non-Build coordinator may edit.
  - Generalize the investigator and reviewer descriptions so they are optional,
    read-only helpers for explicitly authorized non-Build coordinators.
  - Remove Build delegation from `punch-using-agent-skills`.
  - Change Init and the vendor manifest from required/BLOCKED semantics to
    optional informational capability checks.
  - Preserve Test/Review/Security verdict ownership and read-only tool subsets.
- **Acceptance criteria:**
  - No `punch-cavecrew-builder` file or live reference remains.
  - No Build prompt, Builder, or Build engineer may invoke Cavecrew.
  - Missing Caveman/Cavecrew produces no BLOCKED Punch readiness verdict.
  - Investigator/reviewer remain read-only leaves and cannot own a phase verdict.
- **Expected diff size:** Approximately 180–320 lines, primarily deletions and
  registry/guard reconciliation.
- **Validation commands:**
  - `rg -n 'punch-cavecrew-builder' .github docs AGENTS.md` → no matches.
  - `rg -ni 'caveman|cavecrew|wenyan' .github/prompts/punch-build.prompt.md .github/agents/punch-builder.agent.md .github/agents/punch-runtime-engineer.agent.md .github/agents/punch-performance-test-engineer.agent.md` → no matches.
  - `git diff --check`
  - Read-only `punch-ai-governance` audit → clean roster, registry, and reference checks.
- **Rollback notes:** Restore the deleted worker and related governance entries
  together by reverting AI-03.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration maintenance.

### AI-04 — Replace the Build-named Caveman adapter with an optional comms policy

- **Goal:** Move all remaining Punch-specific prose guidance to a phase-neutral,
  optional adapter with no execution or delegation semantics.
- **Allowed edit paths:**
  - `.github/skills/punch-build-caveman/**` (delete)
  - `.github/skills/punch-comms-policy/**` (create)
  - `.github/prompts/punch-spec.prompt.md`
  - `.github/prompts/punch-plan.prompt.md`
  - `.github/prompts/punch-document.prompt.md`
  - `.github/prompts/punch-test.prompt.md`
  - `.github/prompts/punch-review.prompt.md`
  - `.github/prompts/punch-ship.prompt.md`
  - `.github/prompts/punch-init.prompt.md`
  - `.github/agents/punch-ai-governance.agent.md`
  - `.github/agents/punch-architect.agent.md`
  - `.github/agents/punch-test-engineer.agent.md`
  - `.github/agents/punch-code-reviewer.agent.md`
  - `.github/agents/punch-security-auditor.agent.md`
  - `.github/agents/punch-release-captain.agent.md`
  - `.github/agents/punch-cavecrew-investigator.agent.md`
  - `.github/agents/punch-cavecrew-reviewer.agent.md`
  - `.github/copilot-instructions.md`
  - `.github/skills/punch-ai-governance/SKILL.md`
  - `docs/ai/skill-registry.md`
  - `docs/ai/decisions/0004-claude-code-guard-bridge.md`
  - `AGENTS.md`
- **Read-only context paths:**
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
  - `.github/.ai-upstream/README.md`
  - `.github/prompts/punch-build.prompt.md`
  - `.github/agents/punch-builder.agent.md`
  - `.github/agents/punch-runtime-engineer.agent.md`
  - `.github/agents/punch-performance-test-engineer.agent.md`
- **Forbidden paths:**
  - `.agents/skills/caveman/**`
  - `.agents/skills/cavecrew/**`
  - `.ai-upstream/**`
  - Every other path not explicitly allowed above
  - `src/**`, `bin/**`, `docker/**`, `docker-compose.yml`
  - `.github/workflows/**`, `reports/**`
- **Implementation notes:**
  - Replace `punch-build-caveman` with `punch-comms-policy` atomically so no
    broken references land.
  - Keep only optional presentation rules: preserve exact evidence, commands,
    paths, errors, acceptance criteria, blockers, and next actions.
  - State that normal prose is the fallback when Caveman is absent or inactive.
  - Remove Build-chain, worker-roster, tool, scope, and delegation rules; those
    belong to lifecycle prompts, agents, and `agent-guards.md`.
  - Do not add any `punch-comms-policy` reference to Build or its engineers.
- **Acceptance criteria:**
  - No live `punch-build-caveman` path or reference remains.
  - `punch-comms-policy` is registered as optional and output-only.
  - Build-chain files contain no reference to either comms policy or vendor.
  - Persistent artifacts still forbid Wenyan and preserve evidence verbatim.
- **Expected diff size:** Approximately 250–450 lines, mostly mechanical link
  migration and policy deletion.
- **Validation commands:**
  - `rg -n 'punch-build-caveman' .github docs AGENTS.md CLAUDE.md` → no matches.
  - `rg -ni 'caveman|cavecrew|wenyan|punch-comms-policy' .github/prompts/punch-build.prompt.md .github/agents/punch-builder.agent.md .github/agents/punch-runtime-engineer.agent.md .github/agents/punch-performance-test-engineer.agent.md` → no matches.
  - `git diff --check`
  - Read-only `punch-ai-governance` audit → clean skills, prompts, agents, and registries.
- **Rollback notes:** Revert the adapter rename and all inbound-link changes as
  one atomic commit.
- **Human checkpoint:** Human approval required before implementation.
- **Build via:** `punch-ai-governance` documentation/configuration maintenance.

## Order of execution

1. **AI-01** — remove vendor coupling from the Build entry and coordinator.
2. **AI-02** — make both engineers independent, non-spawning leaves.
3. **AI-03** — retire Build-only Cavecrew wiring and make vendor capabilities optional.
4. **AI-04** — atomically introduce the phase-neutral optional comms policy.
5. Run the complete validation and governance gates below.

AI-01 and AI-02 must be sequential because the coordinator roster and engineer
capabilities form one delegation contract. AI-03 follows them so the editing
worker has no caller before deletion. AI-04 runs last to migrate the remaining
cross-references after the Build chain is already vendor-free.

## Complete validation gate

1. Confirm vendor asset hashes:

   ```bash
   shasum -a 256 \
     .agents/skills/caveman/SKILL.md \
     .agents/skills/caveman/README.md \
     .agents/skills/cavecrew/SKILL.md \
     .agents/skills/cavecrew/README.md
   ```

2. Confirm Build independence:

   ```bash
   rg -ni 'caveman|cavecrew|wenyan|punch-comms-policy|punch-build-caveman' \
     .github/prompts/punch-build.prompt.md \
     .github/agents/punch-builder.agent.md \
     .github/agents/punch-runtime-engineer.agent.md \
     .github/agents/punch-performance-test-engineer.agent.md
   ```

   Expected result: no matches; `rg` exits `1`.

3. Confirm retired references and formatting:

   ```bash
   rg -n 'punch-cavecrew-builder|punch-build-caveman' .github docs AGENTS.md CLAUDE.md
   git diff --check
   ```

   Expected result: no matches from `rg`; `git diff --check` exits `0`.

4. Run the read-only `punch-ai-governance` audit. Require clean frontmatter,
   registry, link, roster, and vendor-immutability results.
5. Run official Punch verification:

   ```bash
   ./bin/punch doctor
   ./bin/punch run smoke
   ```

6. Require `reports/state/punch-run.json` with `passed: true`.

## Cross-cutting risks

- **Hidden coupling:** Build references occur across prompt, coordinator,
  engineers, discovery skill, guards, instructions, and registries. The final
  repository-wide searches prevent a partial decoupling.
- **Broken Copilot rosters:** Removing a worker without updating every `agents:`
  list or governance expectation creates invalid custom-agent configuration.
- **Policy duplication:** A new neutral comms skill could restate Caveman or
  agent guards. It must remain a small optional adapter and link to vendor
  provenance instead of copying vendor instructions.
- **Accidental vendor edits:** Formatter or newline normalization could alter
  adopted assets. Hash verification is blocking.
- **Over-broad cleanup:** Current Build auto/testing/commit contradictions are
  related but outside this decision. Mixing them here would make rollback and
  Review unreliable.
- **Optionality mismatch:** Init, manifest, registry, and governance must all
  agree that vendor absence is non-blocking.

## Rollback plan

Revert AI-04, AI-03, AI-02, and AI-01 in reverse order. Each task is an
AI-configuration-only commit. No product or data rollback is required. Vendor
assets remain unchanged throughout, so rollback never reinstalls or rewrites
them.

## Assumptions

- The user's request to generate this Plan confirms the architectural direction,
  but does not authorize implementation; explicit Plan approval is still needed.
- “Punch Build not connected” means no prompt, agent roster, prose mode,
  delegation path, or availability dependency on Caveman/Cavecrew.
- “Preserve Caveman Skills assets untouched” covers both tracked vendor skill
  directories and local upstream snapshots.
- Optional read-only Cavecrew assistance in Test/Review remains acceptable
  because it is outside Build and cannot own a verdict.

**Gate:** Approved when a human confirms this Plan. Implementation then proceeds
AI-01 → AI-02 → AI-03 → AI-04 through `punch-ai-governance`, followed by Test and
Review. Humans merge.
