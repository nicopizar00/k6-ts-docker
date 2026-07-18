# Plan — native Graphify skill with Copilot-first Punch integration

> **Status:** Draft — human approval required before implementation.
> **Scope:** GitHub Copilot skills, AI instructions, Graphify documentation,
> governance references, and shared Graphify artifacts only. No Punch runtime,
> Docker, k6, service, or orchestrator behavior changes.

## Goal

Replace the large Punch-authored `punch-graphify` adaptation with the native
Graphify Agent Skill, while keeping Punch simple, Copilot-first, secure for
public repositories, and usable from other compatible agents through the
upstream installation instructions.

## Sources and compatibility target

- Native Graphify source: <https://github.com/Graphify-Labs/graphify>
- Native Graphify installation and team workflow:
  <https://github.com/Graphify-Labs/graphify/blob/main/README.md#install>
- VS Code Agent Skills discovery:
  <https://code.visualstudio.com/docs/agent-customization/agent-skills>
- GitHub Copilot project skill locations:
  <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills>
- Native Context Engineering source:
  <https://github.com/addyosmani/agent-skills/tree/main/skills/context-engineering>

The tested Graphify version is recorded in
`.github/skills/graphify/.graphify_version` beside the
committed native skill. The upstream installation command remains the required
manual user step:

```bash
uv tool install graphifyy
```

Version comparison is warning-only. A missing CLI or version mismatch must not
block normal Punch work.

## Decisions to implement

1. **Native skill is canonical.** Commit the upstream skill body and its
   `references/` sidecar under `.github/skills/graphify/` for native VS Code
   Copilot discovery.
2. **Minimal host metadata only.** Preserve the upstream skill body unchanged;
   add only:

   ```yaml
   user-invocable: true
   disable-model-invocation: true
   ```

   This keeps `/graphify` available while preventing Copilot from auto-loading
   Graphify for unrelated work.
3. **No second Graphify skill.** Delete `punch-graphify` and remove all
   Graphify execution paths from `punch-document`, `punch-context-engineering`,
   governance, and initialization flows.
4. **Context Engineering stays native-method aligned.** Keep
   `punch-context-engineering` as a direct Punch-adapted version of Addy
   Osmani's `context-engineering`; remove its Graphify gate and Graphify-specific
   procedure.
5. **Manual installation.** Do not run `graphify vscode install` automatically;
   it edits `.github/copilot-instructions.md`, which is hand-owned by Punch.
   Other agents may use Graphify's documented platform installation commands
   manually.
6. **Always-on security policy.** Add a short policy to
   `.github/copilot-instructions.md`: `/graphify` is explicit-only; terminal
   commands remain approval-gated; Graphify is local-first by default; no hooks,
   watchers, MCP, URL ingestion, cloud backends, or external graph databases
   are enabled automatically.
7. **Shared baseline.** Keep the committed Graphify baseline recommended by
   Graphify, limited to:

   ```text
   graphify-out/graph.json
   graphify-out/GRAPH_REPORT.md
   .graphifyignore
   ```

   Ignore cache, cost, interpreter, absolute-root, temporary extraction, and
   visualization files. Stale graphs warn and remain usable as evidence.
8. **Native maintenance workflow.** Use `/graphify . --update` for routine
   changes and `/graphify .` for structural changes. No Punch hook, watcher,
   automatic refresh, or custom Graphify refresh engine is added.

## Acceptance criteria

- `.github/skills/graphify/SKILL.md` is the only committed Graphify skill body.
- Its native Graphify body and references are preserved; only the two accepted
  invocation-control frontmatter fields are added.
- VS Code Copilot discovers the skill from `.github/skills/graphify/` and shows
  `/graphify` as a user-invocable command.
- Copilot does not auto-load Graphify for unrelated prompts.
- The skill does not pre-approve `shell` or `bash` through `allowed-tools`.
- `punch-context-engineering` contains no Graphify gate, Graphify query contract,
  Graphify installation step, or Graphify write/read ownership rule.
- `punch-document` and `punch-ai-governance` contain no executable Graphify
  delegation or sole-writer workflow.
- No prompt, agent, registry, ADR, adapter manifest, freeze entry, or init asset
  still points to `punch-graphify` as an active skill.
- The manual install instructions show the upstream `uv tool install graphifyy`
  command and platform-specific upstream options for other agents.
- `.github/skills/graphify/.graphify_version` is checked when `graphify --version` is available;
  missing CLI, missing marker, and mismatch produce warnings only.
- Only the agreed shared Graphify files are tracked; machine-local and temporary
  outputs are ignored.
- `/graphify` remains explicit-only and can query the committed graph.
- A stale graph warns and continues; it does not block orientation.
- `./bin/punch doctor` passes, `./bin/punch run smoke` passes, and the run writes
  `reports/state/punch-run.json` with a successful verdict.

## Tasks

### NG-01 — Promote the native Graphify skill to the Copilot project location

**Goal:** Replace the Punch Graphify skill body with the upstream Graphify skill
and preserve its references as a native project skill.

**Allowed edit paths:**

- `.github/skills/graphify/**`
- `.github/skills/punch-graphify/**` (delete only)
- `.github/skills/graphify/.graphify_version`

**Read-only context paths:**

- `.ai-upstream/graphify/**`
- `ai.ingest/adapters/graphify.json`
- `docs/ai/decisions/0002-graphify-host-tool.md`
- VS Code/GitHub source URLs listed above

**Forbidden paths:**

- `.github/copilot-instructions.md`
- `.github/prompts/**`
- `.github/agents/**`
- `.github/skills/punch-context-engineering/**`
- `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`, `reports/**`
- `graphify-out/**`

**Validation:**

- Confirm native body/reference parity against the tested upstream snapshot.
- Confirm only `user-invocable` and `disable-model-invocation` were added to
  frontmatter.
- Confirm no `allowed-tools: shell` or `allowed-tools: bash` is present.
- `git diff --check`.

**Rollback:** Restore the prior skill directory and version marker.

**Expected diff size:** Medium; skill relocation and deletion of the old copy.

**Human checkpoint:** Required before implementation.

**Build via:** Governance/documentation maintenance; no product-code engineer.

### NG-02 — Make Punch Context Engineering a direct native-method adaptation

**Goal:** Retain Punch architecture/lifecycle context while removing Graphify as
an internal dependency and automatic routing mechanism.

**Allowed edit paths:**

- `.github/skills/punch-context-engineering/SKILL.md`

**Read-only context paths:**

- Upstream `context-engineering/SKILL.md`
- `docs/architecture/punch-boundaries.md`
- `docs/ai/operating-model.md`
- `.github/copilot-instructions.md`

**Forbidden paths:**

- `.github/skills/graphify/**`
- `.github/skills/punch-graphify/**`
- `.github/prompts/**`, `.github/agents/**`
- `docs/ai/**`, except the plan and source references explicitly named here
- `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`, `reports/**`

**Acceptance details:**

- Preserve the native hierarchy, selective context, trust-level, stale-context,
  confusion-management, and verification concepts.
- Keep Punch-specific architecture and lifecycle pointers.
- Remove `Graphify gate`, Graphify installation, Graphify query references, and
  Graphify team-bootstrap language.
- Fix the existing “7 phases” inconsistency to six phases.

**Validation:**

- Search the file for `Graphify`, `graphify`, and `punch-graphify`; none remain.
- `git diff --check`.
- Read-only governance cross-reference check.

**Rollback:** Revert the single skill change if native context behavior or Punch
architecture routing is lost.

**Expected diff size:** Small to medium.

**Human checkpoint:** Required before implementation.

**Build via:** Governance/documentation maintenance.

### NG-03 — Remove legacy Graphify callers and reconcile documentation

**Goal:** Ensure there is no hidden Graphify invocation through Punch workflows.

**Allowed edit paths:**

- `.github/prompts/punch-document.prompt.md`
- `.github/agents/punch-ai-governance.agent.md`
- `.github/skills/punch-ai-governance/SKILL.md`
- `.github/assets/prompts/punch-init.prompt.md`
- `.github/prompts/punch-build.prompt.md`
- `docs/ai/skill-registry.md`
- `docs/ai/decisions/0002-graphify-host-tool.md`
- `docs/ai/agent-guards.md`
- `docs/ai/maintenance-matrix.md`
- `ai.ingest/adapters/graphify.json`
- `ai.ingest/freeze/punch-assets-freeze.json`
- `AGENTS.md`
- `CLAUDE.md`

**Read-only context paths:**

- `.github/skills/graphify/**`
- `.github/skills/punch-context-engineering/SKILL.md`
- `docs/ai/operating-model.md`
- `AGENTS.md`, `CLAUDE.md`

**Forbidden paths:**

- `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`, `reports/**`
- `graphify-out/**`
- `.ai-upstream/**` (read-only provenance only)

**Acceptance details:**

- Remove Graphify execution from `punch-document`, Context Engineering, and
  initialization.
- Replace active `punch-graphify` ownership references with native Graphify
  references or the documented manual-install policy.
- Preserve ADR history; append a superseding decision instead of rewriting
  historical findings.
- Classify the new native skill as adopted/upstream, not Punch-authored.

**Validation:**

- `rg -n "punch-graphify|Graphify gate|sole Graphify write|/punch-document.*graphify"
  .github docs ai.ingest` returns no active execution references.
- Validate registry and skill-path parity.
- `git diff --check`.

**Rollback:** Revert the documentation reconciliation while retaining the
  historical ADR record.

**Expected diff size:** Medium to large documentation reconciliation.

**Human checkpoint:** Required before implementation.

**Build via:** Governance/documentation maintenance.

### NG-04 — Add concise install, security, version, and sharing policy

**Goal:** Document the upstream manual installation while keeping the template
secure and easy to reuse.

**Allowed edit paths:**

- `.github/copilot-instructions.md`
- `docs/ai/graphify-install.md`
- `.gitignore`
- `.graphifyignore`
- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`

**Read-only context paths:**

- Native Graphify README and source
- `ai.ingest/validate_graphify_share.py`
- Existing Graphify output and validation tests
- `.github/skills/graphify/**`

**Forbidden paths:**

- `src/**`, `docker/**`, `docker-compose.yml`, `bin/**`
- `.github/skills/graphify/SKILL.md` and `references/**` except version metadata
- `.github/prompts/**`, `.github/agents/**`

**Acceptance details:**

- Document `uv tool install graphifyy` as a mandatory manual step.
- Document other-agent installation using upstream platform commands without
  committing user-scope installs.
- State that `/graphify` is explicit-only and stale/version mismatch warnings
  continue.
- Use `.graphifyignore` for obvious sensitive patterns while allowing Graphify
  to support its native inputs if a future user explicitly adds them.
- Keep only the agreed shared baseline files tracked.
- Do not add shell pre-approval to the skill or Copilot policy.

**Validation:**

- `python3 ai.ingest/validate_graphify_share.py`.
- `git diff --check`.
- JSON parse of `graphify-out/graph.json`.
- Confirm no absolute paths, hostnames, interpreter paths, secrets, raw token
  keys, or temporary extraction files are in shared artifacts.

**Rollback:** Restore prior ignore rules and shared artifacts; retain the
  upstream installation documentation if it is independently correct.

**Expected diff size:** Small to medium.

**Human checkpoint:** Required before implementation.

**Build via:** Governance/documentation maintenance.

### NG-05 — Verify native discovery, explicit invocation, and Punch health

**Goal:** Prove that the new arrangement works in the primary VS Code Copilot
  environment without changing Punch runtime behavior.

**Allowed edit paths:**

- `reports/state/punch-run.json` (generated verification artifact only)
- `reports/**` (generated verification artifacts only)

**Read-only context paths:**

- All changed files from NG-01 through NG-04
- Native Graphify sources

**Forbidden paths:**

- All source, Docker, Compose, orchestrator, and test-code paths
- `.github/**` and `docs/**` after NG-04 unless verification finds a documented
  defect and Plan is reopened

**Verification scenarios:**

| Scenario | Expected result |
|---|---|
| VS Code opens the repository | `.github/skills/graphify/SKILL.md` is discoverable |
| `/graphify` is invoked | Native skill runs explicitly |
| Unrelated coding task | Graphify is not auto-loaded |
| CLI missing | Graphify reports the upstream install command; Punch remains usable |
| Version mismatch | Warning only; no skill overwrite |
| Existing graph query | Query works from committed `graph.json` |
| Stale graph query | Warning, then query continues |
| Routine refresh | `/graphify . --update` is the documented path |
| Structural refresh | `/graphify .` is the documented path |
| Punch runtime smoke | Official Punch verification remains green |

**Validation commands:**

```bash
./bin/punch doctor
./bin/punch run smoke
python3 ai.ingest/validate_graphify_share.py
git diff --check
```

The smoke run must produce `reports/state/punch-run.json` with a successful
verdict. Native Graphify CLI testing is manual and only runs when the user has
completed the required upstream installation step.

**Rollback:** Revert the implementation commit if native discovery fails,
Graphify becomes auto-invoked, shared artifacts fail validation, or Punch smoke
verification regresses.

**Expected diff size:** No intentional source diff; generated reports only.

**Human checkpoint:** Review final diff and verification evidence before ship.

**Build via:** Test/documentation verification; no product-code engineer.

## Execution order

1. NG-01 — install the native skill body and remove the old skill directory.
2. NG-02 — remove Graphify from Context Engineering.
3. NG-03 — remove all legacy Graphify callers and reconcile ownership records.
4. NG-04 — add the concise Copilot policy, manual installation guide, version
   marker, ignore rules, and validated shared baseline.
5. NG-05 — run discovery review, artifact validation, and official Punch smoke.

No task may expand into Punch runtime code. If a required file falls outside an
allowed path, stop and reopen this Plan.

## Rollback plan

Revert the implementation commit in reverse order: NG-04, NG-03, NG-02, NG-01.
Do not delete historical ADR evidence. If upstream Graphify changes its skill
contract during implementation, record the new version and reopen the Plan
instead of silently adapting the native body.

**Approval gate:** Human approval of this Plan is required before any
implementation task begins.
