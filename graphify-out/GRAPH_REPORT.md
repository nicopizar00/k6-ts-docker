# Graph Report - .  (2026-07-02)

## Corpus Check
- 142 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 388 nodes · 515 edges · 47 communities (23 shown, 24 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_AI Config Canon + Caveman|AI Config Canon + Caveman]]
- [[_COMMUNITY_Punch Init Scan Pipeline|Punch Init Scan Pipeline]]
- [[_COMMUNITY_Node Build Config|Node Build Config]]
- [[_COMMUNITY_Catalog API Service|Catalog API Service]]
- [[_COMMUNITY_Agent Roster (Specialists)|Agent Roster (Specialists)]]
- [[_COMMUNITY_AI Governance Docs + ADRs|AI Governance Docs + ADRs]]
- [[_COMMUNITY_Punch CLI Dispatcher|Punch CLI Dispatcher]]
- [[_COMMUNITY_Adopt Adapt Drift Tracking|Adopt Adapt Drift Tracking]]
- [[_COMMUNITY_AI Operating Model|AI Operating Model]]
- [[_COMMUNITY_Punch Run Evidence Pipeline|Punch Run Evidence Pipeline]]
- [[_COMMUNITY_Adopt Adapt Test Suite|Adopt Adapt Test Suite]]
- [[_COMMUNITY_Skill Method Library|Skill Method Library]]
- [[_COMMUNITY_Scoped Build Policy|Scoped Build Policy]]
- [[_COMMUNITY_Golden Lifecycle Example|Golden Lifecycle Example]]
- [[_COMMUNITY_Cavecrew Vendor Docs|Cavecrew Vendor Docs]]
- [[_COMMUNITY_TypeScript Config|TypeScript Config]]
- [[_COMMUNITY_Bash Runner Scripts|Bash Runner Scripts]]
- [[_COMMUNITY_Vendor Skill Definitions|Vendor Skill Definitions]]
- [[_COMMUNITY_Build Toolchain|Build Toolchain]]
- [[_COMMUNITY_Test Scripts + DB Schema|Test Scripts + DB Schema]]
- [[_COMMUNITY_Architecture Boundaries|Architecture Boundaries]]
- [[_COMMUNITY_Validation Workflow|Validation Workflow]]
- [[_COMMUNITY_Python Package Shell|Python Package Shell]]
- [[_COMMUNITY_Agent punch-cavecrew-builder (surgical|Agent: punch-cavecrew-builder (surgical ]]
- [[_COMMUNITY_Maintenance Matrix (file-level change ca|Maintenance Matrix (file-level change ca]]
- [[_COMMUNITY_Model Selection — Phase-to-model-class g|Model Selection — Phase-to-model-class g]]
- [[_COMMUNITY_Claude Code project settings (enabledPlu|Claude Code project settings (enabledPlu]]
- [[_COMMUNITY_build command wrap — Punch Build phase|/build command wrap — Punch Build phase]]
- [[_COMMUNITY_init command wrap — Punch Init phase|/init command wrap — Punch Init phase]]
- [[_COMMUNITY_plan command wrap — Punch Plan phase|/plan command wrap — Punch Plan phase]]
- [[_COMMUNITY_review command wrap — Punch Review phas|/review command wrap — Punch Review phas]]
- [[_COMMUNITY_ship command wrap — Punch Ship phase|/ship command wrap — Punch Ship phase]]
- [[_COMMUNITY_spec command wrap — Punch Spec phase|/spec command wrap — Punch Spec phase]]
- [[_COMMUNITY_test command wrap — Punch Test phase|/test command wrap — Punch Test phase]]
- [[_COMMUNITY_Bug Report Issue Template|Bug Report Issue Template]]
- [[_COMMUNITY_Feature Request Issue Template|Feature Request Issue Template]]
- [[_COMMUNITY_Punch Module Init|Punch Module Init]]
- [[_COMMUNITY_Punch Python Package Module|Punch Python Package Module]]
- [[_COMMUNITY_Punch CLI Entry Point Module|Punch CLI Entry Point Module]]
- [[_COMMUNITY_Documentation and ADRs Method|Documentation and ADRs Method]]
- [[_COMMUNITY_Graphify Extraction Subagent Prompt Spec|Graphify Extraction Subagent Prompt Spec]]
- [[_COMMUNITY_Graphify Query Path Explain Reference|Graphify Query Path Explain Reference]]
- [[_COMMUNITY_Graphify Incremental Update Reference|Graphify Incremental Update Reference]]
- [[_COMMUNITY_.mcp.json — MCP server config (empty)|.mcp.json — MCP server config (empty)]]

## God Nodes (most connected - your core abstractions)
1. `Skill: punch-k6-testing` - 12 edges
2. `scan_copilot_assets()` - 12 edges
3. `scan()` - 12 edges
4. `buildSummaryJson()` - 10 edges
5. `buildHtml()` - 10 edges
6. `cmd_run() Run Command Handler` - 10 edges
7. `punch-build-caveman (skill)` - 10 edges
8. `punch-document (prompt)` - 10 edges
9. `main()` - 9 edges
10. `scan_debt_candidates()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `scan_copilot_assets()` --conceptually_related_to--> `punch init Command (Bootstrap Scanner)`  [INFERRED]
  src/punch/init_scan.py → CLAUDE.md
- `graphify_readiness()` --conceptually_related_to--> `punch-graphify (skill)`  [INFERRED]
  src/punch/init_scan.py → .github/skills/punch-graphify/SKILL.md
- `punch-ai-governance Agent` --semantically_similar_to--> `punch-ai-governance (agent)`  [INFERRED] [semantically similar]
  AGENTS.md → .github/agents/punch-ai-governance.agent.md
- `punch-builder Dispatcher` --semantically_similar_to--> `punch-builder (agent)`  [INFERRED] [semantically similar]
  AGENTS.md → .github/agents/punch-builder.agent.md
- `Six-Check Graph Leakage Validation Gate` --semantically_similar_to--> `Graphify Team Share policy`  [INFERRED] [semantically similar]
  docs/ai/decisions/0002-graphify-host-tool.md → .github/skills/punch-graphify/SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cavecrew Leaf Workers (bounded, non-spawning vendor adaptation)** — agents_punch_cavecrew_builder_agent, agents_punch_cavecrew_investigator_agent, agents_punch_cavecrew_reviewer_agent [EXTRACTED 1.00]
- **Ship Phase Fan-out Specialists (parallel pre-ship gate)** — agents_punch_release_captain_agent, agents_punch_code_reviewer_agent, agents_punch_security_auditor_agent, agents_punch_test_engineer_agent [EXTRACTED 1.00]
- **Hub-Spoke Asset Bundle (hub + spoke + init prompt)** — assets_copilot_instructions_document, assets_instructions_governance_document, assets_prompts_punch_init_document [EXTRACTED 1.00]
- **Self-resolutive resolver stubs (out-of-bundle link mirrors)** — assets_resolve_agents_document, assets_resolve_claude_document [EXTRACTED 1.00]
- **k6 handleSummary → Shared Report Module Pattern** — tests_smoke_handlesummary, tests_catalog_gate_handlesummary, tests_order_journey_handlesummary, tests_bff_checkout_journey_handlesummary, support_report_buildsummaryjson, support_report_buildhtml [EXTRACTED 1.00]
- **Docker Compose Execution Chain** — punch___main___cmd_run, punch___main___compose_build, punch___main___run_one, punch___main___stream [EXTRACTED 1.00]
- **Build Phase Quality Skills** — punch_incremental_implementation_skill_method, punch_code_review_and_quality_skill_method, punch_code_simplification_skill_method, punch_doubt_driven_development_skill_method, punch_debugging_and_error_recovery_skill_method [INFERRED 0.85]
- **Idea Refine Skill with Companion Docs** — punch_idea_refine_skill_method, punch_idea_refine_examples_sessions, punch_idea_refine_frameworks_reference, punch_idea_refine_refinement_criteria_rubric, scripts_idea_refine_sh_init [EXTRACTED 1.00]
- **punch-k6-testing skill file bundle** — punch_k6_testing_skill, punch_k6_testing_browser_template, punch_k6_testing_http_template, punch_k6_testing_thresholds [EXTRACTED 1.00]
- **punch-python-orchestration skill file bundle** — punch_python_orchestration_skill, punch_python_orchestration_streaming_subprocess [EXTRACTED 1.00]
- **GitHub Actions CI workflow files** — workflows_copilot_setup_steps_workflow, workflows_k6_workflow [EXTRACTED 1.00]
- **Golden lifecycle worked example — six phases + evidence** — golden_lifecycle_01_spec_phase, golden_lifecycle_02_plan_phase, golden_lifecycle_03_build_phase, golden_lifecycle_04_test_phase, golden_lifecycle_05_review_phase, golden_lifecycle_06_ship_phase, golden_lifecycle_evidence_punch_run, golden_lifecycle_evidence_smoke_summary [EXTRACTED 1.00]
- **Punch Lifecycle Phase Templates (Spec→Plan→Build→Test→Review→Ship)** — lifecycle_spec_template_doc, lifecycle_plan_template_doc, lifecycle_build_template_doc, lifecycle_test_template_doc, lifecycle_review_template_doc, lifecycle_ship_template_doc [EXTRACTED 1.00]
- **Scoped Build Policy Agent Routing Triad** — ai_scoped_build_policy_doc, ai_scoped_build_policy_punch_builder_agent, ai_scoped_build_policy_punch_runtime_engineer, ai_scoped_build_policy_punch_perf_test_engineer [EXTRACTED 1.00]
- **Punch CLI Command Handlers** — punch___main___cmd_doctor, punch___main___cmd_run, punch___main___cmd_clean, punch___main___cmd_init [EXTRACTED 1.00]
- **Reference Application Services** — gateway_server_gateway_api, catalog_server_catalog_api, orders_server_orders_api [INFERRED 0.95]
- **k6 test reporting system (tests + shared report module)** — tests_order_journey_ts_module, tests_smoke_ts_module, support_report_ts_module, support_report_ts_buildhtml, support_report_ts_buildsummaryjson [EXTRACTED 1.00]
- **Drift Report Three-axis Implementation** — ai_ingest_compare_diff_axis, ai_ingest_compare_axis_version, ai_ingest_compare_live_assets, ai_ingest_compare_sha256_file, ai_ingest_compare_probe_version, ai_ingest_compare_main [EXTRACTED 1.00]
- **Adopt Adapt Core Artifacts** — ai_ingest_readme_adopt_adapt, ai_ingest_adopt_lock_lock_index, adapters_graphify_adapter_descriptor, ai_ingest_compare_drift_reporter, freeze_punch_assets_freeze_asset_manifest [EXTRACTED 1.00]
- **cavecrew three-subagent preset system** — cavecrew_skill_cavecrew_investigator, cavecrew_skill_cavecrew_builder, cavecrew_skill_cavecrew_reviewer [EXTRACTED 1.00]
- **full test suite execution — smoke, gate, journey, log collection** — bin_test_smoke_script, bin_test_suite_script, postgres_init_orders_schema [INFERRED 0.75]
- **Punch Document wave flow (prompt, governance agent+skill, gate, graphify)** — prompts_punch_document_prompt_punch_document, agents_punch_ai_governance_agent_punch_ai_governance, punch_ai_governance_skill_punch_ai_governance, punch_context_engineering_skill_graphify_gate, punch_graphify_skill_punch_graphify [EXTRACTED 1.00]
- **Caveman canon single-source policy chain** — punch_build_caveman_skill_punch_build_caveman, punch_build_caveman_skill_wenyan_tiers, _ai_upstream_readme_vendor_skill_manifest, agents_depth1_delegation [INFERRED 0.85]

## Communities (47 total, 24 thin omitted)

### Community 0 - "AI Config Canon + Caveman"
Cohesion: 0.06
Nodes (49): Cavecrew (vendor skill), Caveman (vendor skill), Vendor skill manifest (.ai-upstream), Docker First execution rule, Copilot Instructions (always-on hub), Human approves Ship, Punch lifecycle (Spec-Plan-Build-Test-Review-Ship), Validation evidence mandate (punch-run.json) (+41 more)

### Community 1 - "Punch Init Scan Pipeline"
Cohesion: 0.11
Nodes (41): Namespace, Path, _asset_base(), _asset_type(), AssetRecord, build_lifecycle_map(), compute_readiness(), DebtCandidate (+33 more)

### Community 2 - "Node Build Config"
Cohesion: 0.10
Nodes (27): devDependencies, esbuild, @types/k6, name, private, scripts, build, docker:build (+19 more)

### Community 3 - "Catalog API Service"
Cohesion: 0.09
Nodes (22): Catalog API HTTP Server, http, productMap, products, server, Gateway API HTTP Server, http, httpGet() (+14 more)

### Community 4 - "Agent Roster (Specialists)"
Cohesion: 0.11
Nodes (24): Agent: punch-architect (Spec + Plan owner), Agent: punch-cavecrew-investigator (read-only locator, leaf), Agent: punch-cavecrew-reviewer (compact diff reviewer, leaf), Agent: punch-code-reviewer (Review phase verdict owner, five-dimension), Agent: punch-release-captain (Ship phase GO/NO-GO owner), Agent: punch-security-auditor (security verdict owner, read-only), Agent: punch-test-engineer (independent Test gate, PASS/FAIL/BLOCKED), Copilot Instructions Hub template (always-on global rules) (+16 more)

### Community 5 - "AI Governance Docs + ADRs"
Cohesion: 0.11
Nodes (19): Agent Guards (runtime discipline rules), Copilot Mode Mapping (lifecycle to Ask/Agent mode), ADR 0001: punch-performance-test-engineer may use host npm, ADR 0004: Claude Code guard bridge reuses GitHub-Copilot-First config, options, productIds, Skill: punch-k6-testing, Threshold Cheatsheet (smoke / gate / journey / browser) (+11 more)

### Community 6 - "Punch CLI Dispatcher"
Cohesion: 0.17
Nodes (19): ArgumentParser, build_parser(), cmd_clean(), cmd_doctor(), cmd_init(), cmd_run(), _collect_service_logs(), _compose_build() (+11 more)

### Community 7 - "Adopt Adapt Drift Tracking"
Cohesion: 0.22
Nodes (18): Graphify Adapter Descriptor, adopt.lock.json — Adopted Skill Lock Index, axis_version(), diff_axis(), compare.py — Adopt Adapt Drift Reporter Module, live_assets(), load_json(), main() (+10 more)

### Community 8 - "AI Operating Model"
Cohesion: 0.11
Nodes (18): Punch Orchestrator (bin/punch + src/punch), Agent Sprawl Control (Function-Based Ceiling), Six-Phase AI Lifecycle (Spec-Plan-Build-Test-Review-Ship), Lifecycle Validation Gates, One Prompt Per Phase Principle, punch-document Prompt (Doc Reconciliation), punch-init Prompt (Bootstrap/Adoption Guard), Prompt Registry (eight lifecycle prompts + init) (+10 more)

### Community 9 - "Punch Run Evidence Pipeline"
Cohesion: 0.14
Nodes (18): Smoke Test Evidence Summary (Golden), _collect_service_logs, _compose_build, _run_one, _stream, _write_evidence, build_parser() Argument Parser Builder, cmd_clean() Clean Command Handler (+10 more)

### Community 10 - "Adopt Adapt Test Suite"
Cohesion: 0.11
Nodes (4): DiffAxis, EndToEnd, LiveAssets, ProbeAndVersion

### Community 11 - "Skill Method Library"
Cohesion: 0.17
Nodes (15): Code Review and Quality Method, Code Simplification Method, Compose Service Contract Template, Compose Runtime Authority, Artifact Contract Template, Data Harvest Authority, Debugging and Error Recovery Method, Doubt-Driven Development Method (+7 more)

### Community 12 - "Scoped Build Policy"
Cohesion: 0.17
Nodes (13): Scoped Build Policy, punch-builder Dispatcher Agent, punch-performance-test-engineer Agent, punch-runtime-engineer Agent, Scope Expansion Stop-and-Replan Rule, Three-list Scope Model (allowed / readonly / forbidden paths), Build Phase Template, Plan Phase Template (+5 more)

### Community 13 - "Golden Lifecycle Example"
Cohesion: 0.36
Nodes (10): Concept — Verification-class task (Build as documented no-op), Golden Lifecycle — Spec Phase (01-spec.md), Golden Lifecycle — Plan Phase (02-plan.md), Golden Lifecycle — Build Phase (03-build.md), Golden Lifecycle — Test Phase (04-test.md), Golden Lifecycle — Review Phase (05-review.md), Golden Lifecycle — Ship Phase (06-ship.md), Golden Lifecycle Evidence — punch-run.json (+2 more)

### Community 14 - "Cavecrew Vendor Docs"
Cohesion: 0.43
Nodes (8): cavecrew decision guide README, cavecrew-builder subagent — surgical 1-2 file edit, cavecrew-investigator subagent — read-only code locator, cavecrew-reviewer subagent — diff and file severity review, cavecrew SKILL.md — subagent delegation decision guide, caveman compressed communication README, caveman SKILL.md — ultra-compressed communication mode, caveman intensity levels — lite, full, ultra, wenyan variants

### Community 15 - "TypeScript Config"
Cohesion: 0.25
Nodes (7): compilerOptions, module, moduleResolution, noEmit, strict, target, include

### Community 16 - "Bash Runner Scripts"
Cohesion: 0.67
Nodes (4): bin/clean — Docker Compose Teardown, bin/punch — Python Orchestrator Shim, bin/test-gate — Catalog Performance Gate Runner, bin/test-journey — Order Journey Test Runner

### Community 17 - "Vendor Skill Definitions"
Cohesion: 0.67
Nodes (4): Cavecrew Skill README, Cavecrew SKILL Definition, Caveman Skill README, Caveman SKILL Definition

### Community 18 - "Build Toolchain"
Cohesion: 0.50
Nodes (4): esbuild Bundle Script, package.json — Project Config, smoke:local Host k6 Pre-check, TypeScript Compiler Config (ES2015 target, bundler resolution)

### Community 19 - "Test Scripts + DB Schema"
Cohesion: 0.67
Nodes (3): test-smoke bash script, test-suite bash script — full suite runner with log collection, orders table SQL schema — id, product_id, quantity, created_at

## Knowledge Gaps
- **124 isolated node(s):** `options`, `productIds`, `name`, `version`, `private` (+119 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `punch-graphify (skill)` connect `AI Config Canon + Caveman` to `Punch Init Scan Pipeline`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `graphify_readiness()` connect `Punch Init Scan Pipeline` to `AI Config Canon + Caveman`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `punch-document (prompt)` connect `AI Config Canon + Caveman` to `AI Operating Model`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Skill: punch-k6-testing` (e.g. with `Copilot Setup Steps Workflow` and `Performance Gate Playground CI Workflow (k6.yml)`) actually correct?**
  _`Skill: punch-k6-testing` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `options`, `productIds`, `Map relative-path -> sha256 for files under root matching track_globs.      `exc` to the rest of the system?**
  _146 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AI Config Canon + Caveman` be split into smaller, more focused modules?**
  _Cohesion score 0.05697278911564626 - nodes in this community are weakly interconnected._
- **Should `Punch Init Scan Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.11382113821138211 - nodes in this community are weakly interconnected._