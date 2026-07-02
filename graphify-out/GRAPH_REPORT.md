# Graph Report - .  (2026-06-28)

## Corpus Check
- 293 files · ~209,330 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 560 nodes · 819 edges · 51 communities (35 shown, 16 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 105 edges (avg confidence: 0.86)
- Token cost: 37,000 input · 8,200 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Punch Init Scan Pipeline|Punch Init Scan Pipeline]]
- [[_COMMUNITY_AI Governance + Copilot Config|AI Governance + Copilot Config]]
- [[_COMMUNITY_Node Build Config|Node Build Config]]
- [[_COMMUNITY_AI Operating Model Docs|AI Operating Model Docs]]
- [[_COMMUNITY_Lifecycle + Architecture Docs|Lifecycle + Architecture Docs]]
- [[_COMMUNITY_Adopt Adapt Drift Tracking|Adopt Adapt Drift Tracking]]
- [[_COMMUNITY_Governance Decision Patterns|Governance Decision Patterns]]
- [[_COMMUNITY_AI Reference Patterns|AI Reference Patterns]]
- [[_COMMUNITY_Catalog API Service|Catalog API Service]]
- [[_COMMUNITY_Upstream Agent Skills|Upstream Agent Skills]]
- [[_COMMUNITY_AI Config + ADRs|AI Config + ADRs]]
- [[_COMMUNITY_Punch CLI Dispatcher|Punch CLI Dispatcher]]
- [[_COMMUNITY_Punch Run + Evidence|Punch Run + Evidence]]
- [[_COMMUNITY_Adopt Adapt Test Suite|Adopt Adapt Test Suite]]
- [[_COMMUNITY_Agent Roster|Agent Roster]]
- [[_COMMUNITY_Build Standards + Methods|Build Standards + Methods]]
- [[_COMMUNITY_Context + Graphify Skills|Context + Graphify Skills]]
- [[_COMMUNITY_Build Policy + Scope|Build Policy + Scope]]
- [[_COMMUNITY_Skill Registry|Skill Registry]]
- [[_COMMUNITY_Lifecycle Prompts|Lifecycle Prompts]]
- [[_COMMUNITY_Skill Validation Script|Skill Validation Script]]
- [[_COMMUNITY_Cavecrew Subagents|Cavecrew Subagents]]
- [[_COMMUNITY_TypeScript Config|TypeScript Config]]
- [[_COMMUNITY_Build Dispatcher|Build Dispatcher]]
- [[_COMMUNITY_Graphify Gate + Migration|Graphify Gate + Migration]]
- [[_COMMUNITY_Caveman + Cavecrew Skills|Caveman + Cavecrew Skills]]
- [[_COMMUNITY_Security References|Security References]]
- [[_COMMUNITY_Bin Scripts|Bin Scripts]]
- [[_COMMUNITY_Build + Bundle Config|Build + Bundle Config]]
- [[_COMMUNITY_Claude Code Commands|Claude Code Commands]]
- [[_COMMUNITY_Legacy Test Scripts + DB|Legacy Test Scripts + DB]]
- [[_COMMUNITY_Upstream Provenance|Upstream Provenance]]
- [[_COMMUNITY_API Design Methods|API Design Methods]]
- [[_COMMUNITY_Upstream Agent Persona|Upstream Agent Persona]]
- [[_COMMUNITY_Idea Refine Script|Idea Refine Script]]
- [[_COMMUNITY_Claude Code Settings|Claude Code Settings]]
- [[_COMMUNITY_Idea Refine Upstream|Idea Refine Upstream]]
- [[_COMMUNITY_Punch Python Package|Punch Python Package]]
- [[_COMMUNITY_Testing Method|Testing Method]]
- [[_COMMUNITY_Governance Key Migration|Governance Key Migration]]
- [[_COMMUNITY_Wenyan Risk|Wenyan Risk]]
- [[_COMMUNITY_Code Simplify Command|Code Simplify Command]]
- [[_COMMUNITY_Bug Report Template|Bug Report Template]]
- [[_COMMUNITY_Feature Request Template|Feature Request Template]]
- [[_COMMUNITY_Punch Init Module|Punch Init Module]]
- [[_COMMUNITY_Punch Package|Punch Package]]
- [[_COMMUNITY_Punch CLI Module|Punch CLI Module]]
- [[_COMMUNITY_MCP Server Config|MCP Server Config]]
- [[_COMMUNITY_Placeholder Resolution|Placeholder Resolution]]

## God Nodes (most connected - your core abstractions)
1. `Skill Registry (Domain + Lifecycle Axes)` - 24 edges
2. `using-agent-skills meta-skill` - 16 edges
3. `scan()` - 13 edges
4. `Skill: punch-k6-testing` - 13 edges
5. `Guard skill — Claude Code ↔ GitHub Copilot bridge` - 13 edges
6. `scan_copilot_assets()` - 11 edges
7. `Docker First principle (host requires only Docker + stdlib Python 3)` - 11 edges
8. `buildSummaryJson()` - 10 edges
9. `buildHtml()` - 10 edges
10. `cmd_run() Run Command Handler` - 10 edges

## Surprising Connections (you probably didn't know these)
- `graphify_readiness()` --conceptually_related_to--> `Upstream Provenance — Graphify`  [INFERRED]
  src/punch/init_scan.py → .ai-upstream/graphify/UPSTREAM.md
- `scan()` --conceptually_related_to--> `Graphify Skill Definition`  [INFERRED]
  src/punch/init_scan.py → .ai-upstream/graphify/SKILL.md
- `docker-compose.yml — full service + k6 orchestration` --shares_data_with--> `smoke test module`  [INFERRED]
  docker-compose.yml → src/tests/smoke.ts
- `Graphify Adapter Descriptor` --references--> `Graphify Add-URL and Watch Daemon Reference`  [EXTRACTED]
  ai.ingest/adapters/graphify.json → .copilot/skills/graphify/references/add-watch.md
- `Graphify Adapter Descriptor` --references--> `Graphify Extra Export Formats (neo4j, wiki, svg, mcp, falkordb)`  [EXTRACTED]
  ai.ingest/adapters/graphify.json → .copilot/skills/graphify/references/exports.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Build Phase Agents (builder + engineers + cavecrew)** — agents_punch_builder_agent, agents_punch_runtime_engineer_agent, agents_punch_performance_test_engineer_agent, agents_punch_cavecrew_builder_agent, agents_punch_cavecrew_investigator_agent, agents_punch_cavecrew_reviewer_agent [EXTRACTED 1.00]
- **Punch Lifecycle Agent Roster (all phase agents)** — agents_punch_architect_agent, agents_punch_builder_agent, agents_punch_test_engineer_agent, agents_punch_code_reviewer_agent, agents_punch_release_captain_agent, agents_punch_ai_governance_agent [EXTRACTED 1.00]
- **Cavecrew Leaf Workers (bounded, non-spawning vendor adaptation)** — agents_punch_cavecrew_builder_agent, agents_punch_cavecrew_investigator_agent, agents_punch_cavecrew_reviewer_agent [EXTRACTED 1.00]
- **Ship Phase Fan-out Specialists (parallel pre-ship gate)** — agents_punch_release_captain_agent, agents_punch_code_reviewer_agent, agents_punch_security_auditor_agent, agents_punch_test_engineer_agent [EXTRACTED 1.00]
- **Hub-Spoke Asset Bundle (hub + spoke + init prompt)** — assets_copilot_instructions_document, assets_instructions_governance_document, assets_prompts_punch_init_document [EXTRACTED 1.00]
- **Self-resolutive resolver stubs (out-of-bundle link mirrors)** — assets_resolve_agents_document, assets_resolve_claude_document [EXTRACTED 1.00]
- **k6 handleSummary → Shared Report Module Pattern** — tests_smoke_handlesummary, tests_catalog_gate_handlesummary, tests_order_journey_handlesummary, tests_bff_checkout_journey_handlesummary, support_report_buildsummaryjson, support_report_buildhtml [EXTRACTED 1.00]
- **Punch Init Scanner Orchestration Pipeline** — punch_init_scan_scan, punch_init_scan_resolve_identity, punch_init_scan_scan_copilot_assets, punch_init_scan_scan_doc_surface, punch_init_scan_scan_debt_candidates, punch_init_scan_graphify_readiness, punch_init_scan_compute_readiness, punch_init_scan_build_lifecycle_map, punch_init_scan_resolve_output_dir [EXTRACTED 1.00]
- **Docker Compose Execution Chain** — punch___main___cmd_run, punch___main___compose_build, punch___main___run_one, punch___main___stream [EXTRACTED 1.00]
- **Build Phase Quality Skills** — punch_incremental_implementation_skill_method, punch_code_review_and_quality_skill_method, punch_code_simplification_skill_method, punch_doubt_driven_development_skill_method, punch_debugging_and_error_recovery_skill_method [INFERRED 0.85]
- **Graphify Skill with Reference Docs** — punch_graphify_skill_tool, references_extraction_spec_spec, references_query_reference, references_update_reference [EXTRACTED 1.00]
- **Idea Refine Skill with Companion Docs** — punch_idea_refine_skill_method, punch_idea_refine_examples_sessions, punch_idea_refine_frameworks_reference, punch_idea_refine_refinement_criteria_rubric, scripts_idea_refine_sh_init [EXTRACTED 1.00]
- **punch-k6-testing skill file bundle** — punch_k6_testing_skill, punch_k6_testing_browser_template, punch_k6_testing_http_template, punch_k6_testing_thresholds [EXTRACTED 1.00]
- **punch-python-orchestration skill file bundle** — punch_python_orchestration_skill, punch_python_orchestration_streaming_subprocess [EXTRACTED 1.00]
- **Punch lifecycle and domain skills (all referenced by punch-using-agent-skills)** — punch_using_agent_skills_skill, punch_spec_driven_development_skill, punch_planning_and_task_breakdown_skill, punch_test_driven_development_skill, punch_source_driven_development_skill, punch_performance_optimization_skill, punch_observability_and_instrumentation_skill, punch_security_and_hardening_skill, punch_k6_testing_skill, punch_python_orchestration_skill [EXTRACTED 0.95]
- **ADRs governing Docker-First exception policy** — docs_ai_decisions_0001_perf_engineer_host_npm, docs_ai_decisions_0002_graphify_host_tool, docs_ai_decisions_0004_claude_code_guard_bridge [INFERRED 0.85]
- **GitHub Actions CI workflow files** — workflows_copilot_setup_steps_workflow, workflows_k6_workflow [EXTRACTED 1.00]
- **Golden lifecycle worked example — six phases + evidence** — golden_lifecycle_01_spec_phase, golden_lifecycle_02_plan_phase, golden_lifecycle_03_build_phase, golden_lifecycle_04_test_phase, golden_lifecycle_05_review_phase, golden_lifecycle_06_ship_phase, golden_lifecycle_evidence_punch_run, golden_lifecycle_evidence_smoke_summary [EXTRACTED 1.00]
- **Agent-skills absorption review document set** — history_agent_skills_absorption_plan, history_ai_config_conflict_report, history_copilot_adaptation_plan, history_punch_ai_config_inventory, history_recommended_target_ai_architecture, history_skill_absorption_matrix, history_upstream_agent_skills_inventory [EXTRACTED 1.00]
- **Lifecycle governance docs — operating model, prompt registry, model selection, maintenance matrix** — ai_operating_model, ai_prompt_registry, ai_model_selection, ai_maintenance_matrix [INFERRED 0.95]
- **Two-axis skill model rationale — conflict report + target architecture + absorption plan** — history_ai_config_conflict_report, history_recommended_target_ai_architecture, history_agent_skills_absorption_plan, concept_two_axis_skill_model [EXTRACTED 1.00]
- **Punch Lifecycle Phase Templates (Spec→Plan→Build→Test→Review→Ship)** — lifecycle_spec_template_doc, lifecycle_plan_template_doc, lifecycle_build_template_doc, lifecycle_test_template_doc, lifecycle_review_template_doc, lifecycle_ship_template_doc [EXTRACTED 1.00]
- **Six Capped Domain Skills** — ai_skill_registry_skill_context_engineering, ai_skill_registry_skill_python_orchestration, ai_skill_registry_skill_compose_runtime, ai_skill_registry_skill_k6_testing, ai_skill_registry_skill_data_harvest, ai_skill_registry_skill_ai_governance [EXTRACTED 1.00]
- **Endorsed Orchestration Patterns (6 + Agent Teams)** — punch_references_orchestration_patterns_direct_invocation, punch_references_orchestration_patterns_parallel_fanout, punch_references_orchestration_patterns_sequential_pipeline, punch_references_orchestration_patterns_research_isolation, punch_references_orchestration_patterns_build_delegated, punch_references_orchestration_patterns_agent_teams [EXTRACTED 1.00]
- **Scoped Build Policy Agent Routing Triad** — ai_scoped_build_policy_doc, ai_scoped_build_policy_punch_builder_agent, ai_scoped_build_policy_punch_runtime_engineer, ai_scoped_build_policy_punch_perf_test_engineer [EXTRACTED 1.00]
- **Template Migration Scratch Notes Set (2026-06-20)** — tmp_migration_2026_06_20_00_preflight_host_doc, tmp_migration_2026_06_20_01_governance_identity_doc, tmp_migration_2026_06_20_02_placeholders_resolve_doc, tmp_migration_2026_06_20_03_copilot_ide_wiring_doc, tmp_migration_2026_06_20_04_wenyan_comprehension_doc, tmp_migration_2026_06_20_05_lifecycle_registries_doc, tmp_migration_2026_06_20_06_security_evidence_doc, tmp_migration_2026_06_20_07_graphify_track_doc, tmp_migration_2026_06_20_08_scope_frozen_crosstools_doc [EXTRACTED 1.00]
- **Punch Lifecycle Prompts Set (Spec→Ship)** — ai_skill_registry_punch_spec_prompt, ai_skill_registry_punch_plan_prompt, ai_skill_registry_punch_build_prompt, ai_skill_registry_punch_test_prompt, ai_skill_registry_punch_review_prompt, ai_skill_registry_punch_ship_prompt [EXTRACTED 1.00]
- **Adopt Adapt Increment Chain: MVP data model, compare command, caveman/cavecrew, graphify/punch-document** — specs_adopt_adapt_doc, specs_adopt_adapt_compare_doc, specs_adopt_adapt_caveman_cavecrew_doc, specs_adopt_adapt_graphify_punch_document_doc, specs_plan_adopt_adapt_doc, specs_plan_adopt_adapt_graphify_punch_document_doc, specs_plan_punch_graphify_natural_replacement_doc [INFERRED 0.85]
- **BFF Checkout Journey Feature: spec + CLI wiring + implementation + plans** — specs_bff_checkout_journey_test_doc, specs_bff_checkout_journey_cli_doc, specs_bff_checkout_journey_implementation_doc, specs_plan_bff_checkout_journey_doc, specs_plan_bff_checkout_journey_test_doc [INFERRED 0.95]
- **Graphify Governance Track: adoption, lean, wiring to punch-document, natural replacement, team alignment** — specs_adopt_adapt_doc, specs_adopt_adapt_compare_doc, specs_adopt_adapt_graphify_punch_document_doc, specs_plan_adopt_adapt_graphify_punch_document_doc, specs_plan_punch_graphify_natural_replacement_doc, specs_plan_punch_graphify_team_alignment_doc [INFERRED 0.85]
- **Lean AI Config Wave: spec (Waves 1-3 Caveman single-source) + cleanup plan** — specs_lean_ai_config_doc, specs_plan_lean_ai_config_doc [EXTRACTED 0.95]
- **Migration scratch folder: README index + canon-caveman notes + misc gotchas** — tmp_migration_2026_06_20_readme_doc, tmp_migration_2026_06_20_09_canon_style_caveman_doc, tmp_migration_2026_06_20_10_gotchas_misc_doc [EXTRACTED 1.00]
- **Punch Architecture Foundation: architecture doc + boundaries ownership + workflow lifecycle** — docs_architecture_doc, architecture_punch_boundaries_doc, ai_workflow_doc [INFERRED 0.85]
- **/ship parallel fan-out: code-reviewer + security-auditor + test-engineer run concurrently then merge** — ai_upstream_commands_ship_command, ai_upstream_agents_code_reviewer_persona, ai_upstream_agents_security_auditor_persona, ai_upstream_agents_test_engineer_persona [EXTRACTED 1.00]
- **Agent Skills lifecycle commands implement full SDLC workflow** — ai_upstream_commands_spec_command, ai_upstream_commands_plan_command, ai_upstream_commands_build_command, ai_upstream_commands_test_command, ai_upstream_commands_review_command, ai_upstream_commands_ship_command [EXTRACTED 1.00]
- **Punch validation contract: lifecycle phases gated by punch-run.json evidence artifact** — docs_workflows_lifecycle_guide, docs_workflows_validation_guide, docs_validation_readme_landing, docs_workflows_validation_punch_run_json [EXTRACTED 1.00]
- **Track B k6 test suite produces evidence captured in punch-run.json and report artifacts** — docs_roadmap_track_b_reference_app_roadmap, docs_roadmap_track_b_k6_test_patterns, docs_workflows_validation_punch_run_json, docs_roadmap_track_a_performance_gate_roadmap [INFERRED 0.95]
- **AI Tool Setup Guides for agent-skills** — docs_copilot_setup_guide, docs_cursor_setup_guide, docs_gemini_cli_setup_guide, docs_opencode_setup_guide, docs_windsurf_setup_guide [EXTRACTED 1.00]
- **Quality Reference Checklists** — references_security_checklist, references_performance_checklist, references_accessibility_checklist, references_testing_patterns, references_observability_checklist [EXTRACTED 1.00]
- **SKILL.md Anatomy and Validation System** — docs_skill_anatomy_spec, scripts_validate_skills_validator [EXTRACTED 1.00]
- **Domain and Quality Skills (Chunk 9)** — skills_api_and_interface_design, skills_browser_testing_with_devtools, skills_ci_cd_and_automation, skills_code_review_and_quality, skills_code_simplification, skills_context_engineering, skills_debugging_and_error_recovery, skills_deprecation_and_migration [INFERRED 0.95]
- **idea-refine skill bundle (SKILL + examples + frameworks + criteria + script)** — idea_refine_skill, idea_refine_examples, idea_refine_frameworks, idea_refine_refinement_criteria, idea_refine_script [EXTRACTED 1.00]
- **Define-phase skills cluster (interview-me, idea-refine, spec-driven-development)** — interview_me_skill, idea_refine_skill, spec_driven_development_skill [EXTRACTED 1.00]
- **Build-phase skills cluster (incremental-implementation, source-driven, doubt-driven, frontend-ui)** — incremental_implementation_skill, source_driven_development_skill, doubt_driven_development_skill, frontend_ui_engineering_skill [EXTRACTED 1.00]
- **Review-phase skills cluster (security, performance, tdd)** — security_and_hardening_skill, performance_optimization_skill, test_driven_development_skill [EXTRACTED 1.00]
- **Ship-phase skills cluster (git, documentation, observability, shipping-and-launch)** — git_workflow_and_versioning_skill, documentation_and_adrs_skill, observability_and_instrumentation_skill, shipping_and_launch_skill [EXTRACTED 1.00]
- **All upstream skills governed by using-agent-skills meta-skill** — using_agent_skills_skill, interview_me_skill, idea_refine_skill, spec_driven_development_skill, planning_and_task_breakdown_skill, incremental_implementation_skill, source_driven_development_skill, doubt_driven_development_skill, frontend_ui_engineering_skill, test_driven_development_skill, security_and_hardening_skill, performance_optimization_skill, git_workflow_and_versioning_skill, documentation_and_adrs_skill, observability_and_instrumentation_skill, shipping_and_launch_skill [EXTRACTED 1.00]
- **Graphify Skill and Reference Documents** — graphify_skill_definition, references_add_watch_reference, references_exports_reference, references_extraction_spec_prompt, references_github_and_merge_reference, references_hooks_reference, references_query_reference, references_transcribe_reference, references_update_reference [EXTRACTED 1.00]
- **Punch CLI Command Handlers** — punch___main___cmd_doctor, punch___main___cmd_run, punch___main___cmd_clean, punch___main___cmd_init [EXTRACTED 1.00]
- **Reference Application Services** — gateway_server_gateway_api, catalog_server_catalog_api, orders_server_orders_api [INFERRED 0.95]
- **Claude Code lifecycle command wraps unified by guard skill** — commands_spec_md_command, commands_plan_md_command, commands_build_md_command, commands_test_md_command, commands_review_md_command, commands_ship_md_command, commands_document_md_command, commands_init_md_command, guard_skill_md_skill [EXTRACTED 1.00]
- **k6 test reporting system (tests + shared report module)** — tests_order_journey_ts_module, tests_smoke_ts_module, support_report_ts_module, support_report_ts_buildhtml, support_report_ts_buildsummaryjson [EXTRACTED 1.00]
- **Project AI documentation set (core instruction files)** — root_agents_md_guide, root_claude_md_instructions, root_readme_md_overview [INFERRED 0.85]
- **Docker-first execution chain (compose + concepts)** — root_docker_compose_yml_config, concept_execution_chain, concept_docker_first [EXTRACTED 1.00]
- **Punch AI governance concept cluster** — concept_punch_lifecycle, concept_guard_bridge, concept_caveman_canon, guard_skill_md_skill, root_agents_md_guide [INFERRED 0.90]
- **Graphify Skill Reference File Cluster** — graphify_skill_graphify_pipeline, references_extraction_spec_subagent_protocol, references_query_bfs_dfs, references_update_incremental, references_exports_export_formats, references_add_watch_url_ingest, references_hooks_git_hook, references_github_and_merge_cross_repo, references_transcribe_whisper [EXTRACTED 1.00]
- **Drift Report Three-axis Implementation** — ai_ingest_compare_diff_axis, ai_ingest_compare_axis_version, ai_ingest_compare_live_assets, ai_ingest_compare_sha256_file, ai_ingest_compare_probe_version, ai_ingest_compare_main [EXTRACTED 1.00]
- **Adopt Adapt Core Artifacts** — ai_ingest_readme_adopt_adapt, ai_ingest_adopt_lock_lock_index, adapters_graphify_adapter_descriptor, ai_ingest_compare_drift_reporter, freeze_punch_assets_freeze_asset_manifest [EXTRACTED 1.00]
- **cavecrew three-subagent preset system** — cavecrew_skill_cavecrew_investigator, cavecrew_skill_cavecrew_builder, cavecrew_skill_cavecrew_reviewer [EXTRACTED 1.00]
- **full test suite execution — smoke, gate, journey, log collection** — bin_test_smoke_script, bin_test_suite_script, postgres_init_orders_schema [INFERRED 0.75]

## Communities (51 total, 16 thin omitted)

### Community 0 - "Punch Init Scan Pipeline"
Cohesion: 0.11
Nodes (41): _asset_base(), _asset_type(), AssetRecord, build_lifecycle_map(), compute_readiness(), DebtCandidate, _doc_group(), graphify_readiness() (+33 more)

### Community 1 - "AI Governance + Copilot Config"
Cohesion: 0.10
Nodes (37): Agent: punch-ai-governance (AI config maintainer, user-direct), Copilot Instructions Hub template (always-on global rules), Governance Instructions Spoke template (applyTo: '**'), Prompt: punch-init (AI governance certify + graphify invoke), Assets README (hub-spoke template export guide), Resolver stub: AGENTS.md (caveman-wenyan mirror snapshot), Resolver stub: CLAUDE.md (caveman-wenyan mirror snapshot), /build command wrap — Punch Build phase (+29 more)

### Community 2 - "Node Build Config"
Cohesion: 0.10
Nodes (27): devDependencies, esbuild, @types/k6, name, private, scripts, build, docker:build (+19 more)

### Community 3 - "AI Operating Model Docs"
Cohesion: 0.14
Nodes (29): Maintenance Matrix (file-level change cascade), Model Selection — Phase-to-model-class guide, AI Operating Model — Six-phase lifecycle, Prompt Registry — Eight prompts, one per phase, Concept — Upstream agent-skills absorption into .github/skills/, Concept — GitHub Copilot as primary AI runtime; .github/ as single source of truth, Concept — Six-phase AI lifecycle (Spec→Plan→Build→Test→Review→Ship), Concept — punch-run.json as canonical pass/fail evidence artifact (+21 more)

### Community 4 - "Lifecycle + Architecture Docs"
Cohesion: 0.10
Nodes (29): AI Workflow — Six-Phase Lifecycle Walkthrough, Six-Phase AI Lifecycle: Spec Plan Build Test Review Ship, Punch Architectural Boundaries — Layered Ownership Map, Layered Ownership: Host Bash Python orchestrator Compose Docker k6 Artifacts, Architecture — Execution Chain, Reference App, Folder Map, Execution Chain: TypeScript source esbuild Docker image k6 run reports, Spec — Adopt Adapt: caveman + cavecrew skills (increment), Cavecrew Skill — verbatim vendor (3 agent files punch-cavecrew, tied to caveman 0.1.0) (+21 more)

### Community 5 - "Adopt Adapt Drift Tracking"
Cohesion: 0.14
Nodes (27): Graphify Adapter Descriptor, adopt.lock.json — Adopted Skill Lock Index, axis_version(), diff_axis(), compare.py — Adopt Adapt Drift Reporter Module, live_assets(), load_json(), main() (+19 more)

### Community 6 - "Governance Decision Patterns"
Cohesion: 0.12
Nodes (27): Architecture Decision Record (ADR), Doubt Cycle (5-step adversarial review process), Idea Refine 3-Phase Process (Diverge, Evaluate, Sharpen), Increment Cycle (Implement-Test-Verify-Commit), Agent Skills Lifecycle Sequence (16 phases), Spec-Driven Gated Workflow (Specify-Plan-Tasks-Implement), TDD Cycle (Red-Green-Refactor), documentation-and-adrs skill (+19 more)

### Community 7 - "AI Reference Patterns"
Cohesion: 0.11
Nodes (27): Agent Teams (Experimental Claude Code Feature), Chesterton's Fence Principle, Core Web Vitals (LCP, INP, CLS), Spec-Plan-Build-Test-Review-Ship Lifecycle, Model Context Protocol (MCP) Integration, OWASP Top 10 Security Framework, WCAG 2.1 AA Accessibility Standard, GitHub Copilot Setup Guide (+19 more)

### Community 8 - "Catalog API Service"
Cohesion: 0.09
Nodes (22): Catalog API HTTP Server, http, productMap, products, server, Gateway API HTTP Server, http, httpGet() (+14 more)

### Community 9 - "Upstream Agent Skills"
Cohesion: 0.11
Nodes (25): Agent Skills AGENTS.md (Upstream), Skill-Driven Execution Model, Code Reviewer Persona, Security Auditor Persona, Test Engineer Persona, Web Performance Auditor Persona, /review Command, /ship Command (+17 more)

### Community 10 - "AI Config + ADRs"
Cohesion: 0.13
Nodes (22): Agent Guards (runtime discipline rules), AI Context (project philosophy and constraints), Copilot Mode Mapping (lifecycle to Ask/Agent mode), ADR 0001: punch-performance-test-engineer may use host npm, ADR 0002: graphify as scoped host-tool for documentation mapping, ADR 0004: Claude Code guard bridge reuses GitHub-Copilot-First config, options, productIds (+14 more)

### Community 11 - "Punch CLI Dispatcher"
Cohesion: 0.17
Nodes (19): ArgumentParser, build_parser(), cmd_clean(), cmd_doctor(), cmd_init(), cmd_run(), _collect_service_logs(), _compose_build() (+11 more)

### Community 12 - "Punch Run + Evidence"
Cohesion: 0.14
Nodes (18): Smoke Test Evidence Summary (Golden), _collect_service_logs, _compose_build, _run_one, _stream, _write_evidence, build_parser() Argument Parser Builder, cmd_clean() Clean Command Handler (+10 more)

### Community 13 - "Adopt Adapt Test Suite"
Cohesion: 0.11
Nodes (4): DiffAxis, EndToEnd, LiveAssets, ProbeAndVersion

### Community 14 - "Agent Roster"
Cohesion: 0.29
Nodes (16): Agent: punch-architect (Spec + Plan owner), Agent: punch-builder (Build router/dispatcher), Agent: punch-cavecrew-builder (surgical 1-2 file editor, leaf), Agent: punch-cavecrew-investigator (read-only locator, leaf), Agent: punch-cavecrew-reviewer (compact diff reviewer, leaf), Agent: punch-code-reviewer (Review phase verdict owner, five-dimension), Agent: punch-performance-test-engineer (k6 + TS/esbuild engineer), Agent: punch-release-captain (Ship phase GO/NO-GO owner) (+8 more)

### Community 15 - "Build Standards + Methods"
Cohesion: 0.16
Nodes (16): Punch Build Caveman Policy, Code Review and Quality Method, Code Simplification Method, Compose Service Contract Template, Compose Runtime Authority, Artifact Contract Template, Data Harvest Authority, Debugging and Error Recovery Method (+8 more)

### Community 16 - "Context + Graphify Skills"
Cohesion: 0.15
Nodes (14): Graphify Skill Definition, Upstream Provenance — Graphify, Context Engineering Project Primer, Documentation and ADRs Method, Punch Graphify Knowledge Graph Tool, Graphify Add URL and Watch Folder Reference, Graphify Extra Exports Reference, Graphify Extraction Subagent Prompt Spec (+6 more)

### Community 17 - "Build Policy + Scope"
Cohesion: 0.18
Nodes (13): Scoped Build Policy, punch-performance-test-engineer Agent, punch-runtime-engineer Agent, Three-list Scope Model (allowed / readonly / forbidden paths), Pattern: Agent Teams (Competing Hypotheses Debug), Pattern 6: Build-Phase Delegated Execution (Depth-1 Coordinator), Pattern 1: Direct Invocation (Single Persona), Orchestration Patterns Reference Catalog (+5 more)

### Community 18 - "Skill Registry"
Cohesion: 0.18
Nodes (12): Skill Registry (Domain + Lifecycle Axes), Domain Skills Cap (Six Maximum), Lifecycle Skills Axis (Not Capped, Method-based), Skill: punch-ai-governance (Registry + Boundary Compliance), Skill: punch-build-caveman (Canonical Caveman Policy, Per-phase Voice), Skill: punch-compose-runtime (Service Contracts), Skill: punch-data-harvest (Artifact Paths + Schemas), Skill Discovery Table (Which Skill When) (+4 more)

### Community 19 - "Lifecycle Prompts"
Cohesion: 0.17
Nodes (12): Prompt: punch-plan (.github/prompts/), Prompt: punch-review (.github/prompts/), Prompt: punch-ship (.github/prompts/), Prompt: punch-spec (.github/prompts/), Prompt: punch-test (.github/prompts/), Plan Phase Template, Lifecycle Templates README, Review Phase Template (+4 more)

### Community 20 - "Skill Validation Script"
Cohesion: 0.24
Nodes (10): extractSkillReferences(), fs, main(), parseFrontmatter(), path, REQUIRED_SECTIONS, SECTION_EXEMPT_SKILLS, SKILL_REF_PATTERNS (+2 more)

### Community 21 - "Cavecrew Subagents"
Cohesion: 0.43
Nodes (8): cavecrew decision guide README, cavecrew-builder subagent — surgical 1-2 file edit, cavecrew-investigator subagent — read-only code locator, cavecrew-reviewer subagent — diff and file severity review, cavecrew SKILL.md — subagent delegation decision guide, caveman compressed communication README, caveman SKILL.md — ultra-compressed communication mode, caveman intensity levels — lite, full, ultra, wenyan variants

### Community 22 - "TypeScript Config"
Cohesion: 0.25
Nodes (7): compilerOptions, module, moduleResolution, noEmit, strict, target, include

### Community 23 - "Build Dispatcher"
Cohesion: 0.40
Nodes (5): punch-builder Dispatcher Agent, Scope Expansion Stop-and-Replan Rule, Prompt: punch-build (.github/prompts/), Build Phase Template, Migration Scratch: 05 Lifecycle / Agents / Skills / Registry Completeness

### Community 24 - "Graphify Gate + Migration"
Cohesion: 0.40
Nodes (5): Skill: punch-context-engineering (Graphify Gate + Primer), Skill: punch-graphify (Adopted Upstream, Knowledge Graph), Migration Scratch: 00 Preflight / Host / Tooling, Migration Scratch: 07 Graphify Full-Repo Track, Concept: Graphify First-Build Cost + .graphifyignore Setup

### Community 25 - "Caveman + Cavecrew Skills"
Cohesion: 0.60
Nodes (5): Cavecrew Skill README, Cavecrew SKILL Definition, Caveman Skill README, Caveman SKILL Definition, Cavecrew Subagents (investigator, builder, reviewer)

### Community 26 - "Security References"
Cohesion: 0.40
Nodes (5): Security Checklist, OWASP Top 10 for LLMs Quick Reference, OWASP Top 10 Quick Reference, Threat Modeling (STRIDE per Trust Boundary), Migration Scratch: 06 Security Scan / Evidence Track

### Community 27 - "Bin Scripts"
Cohesion: 0.67
Nodes (4): bin/clean — Docker Compose Teardown, bin/punch — Python Orchestrator Shim, bin/test-gate — Catalog Performance Gate Runner, bin/test-journey — Order Journey Test Runner

### Community 28 - "Build + Bundle Config"
Cohesion: 0.50
Nodes (4): esbuild Bundle Script, package.json — Project Config, smoke:local Host k6 Pre-check, TypeScript Compiler Config (ES2015 target, bundler resolution)

### Community 29 - "Claude Code Commands"
Cohesion: 0.67
Nodes (3): /build Command, /plan Command, /spec Command

### Community 30 - "Legacy Test Scripts + DB"
Cohesion: 0.67
Nodes (3): test-smoke bash script, test-suite bash script — full suite runner with log collection, orders table SQL schema — id, product_id, quantity, created_at

### Community 31 - "Upstream Provenance"
Cohesion: 0.67
Nodes (3): Upstream Provenance — Cavecrew, Caveman Skill Definition, Upstream Provenance — Caveman

### Community 32 - "API Design Methods"
Cohesion: 1.00
Nodes (3): Hyrum's Law, API and Interface Design Skill, Deprecation and Migration Skill

## Knowledge Gaps
- **163 isolated node(s):** `fs`, `path`, `SKILLS_DIR`, `REQUIRED_SECTIONS`, `SECTION_EXEMPT_SKILLS` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Smoke Test Evidence Summary (Golden)` connect `Punch Run + Evidence` to `Punch Init Scan Pipeline`, `Node Build Config`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `buildSummaryJson()` connect `Node Build Config` to `Punch Run + Evidence`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `graphify_readiness()` connect `Punch Init Scan Pipeline` to `Context + Graphify Skills`, `Punch Run + Evidence`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Skill Registry (Domain + Lifecycle Axes)` (e.g. with `Scoped Build Policy` and `Performance Checklist`) actually correct?**
  _`Skill Registry (Domain + Lifecycle Axes)` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `scan()` (e.g. with `Graphify Skill Definition` and `ScanResult`) actually correct?**
  _`scan()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Skill: punch-k6-testing` (e.g. with `Copilot Setup Steps Workflow` and `Performance Gate Playground CI Workflow (k6.yml)`) actually correct?**
  _`Skill: punch-k6-testing` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fs`, `path`, `SKILLS_DIR` to the rest of the system?**
  _174 weakly-connected nodes found - possible documentation gaps or missing edges._