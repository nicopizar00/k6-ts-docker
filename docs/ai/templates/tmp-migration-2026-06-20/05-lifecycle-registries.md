# 05 · 生命週期 · agents · skills · registry（lifecycle completeness）

> ⚠ IDEA scratch。Minimal template = init only。Full lifecycle = later adoption。

生命週期完整性,易漏：

- **唯 init 附**：最小範本唯 `punch-init.prompt.md`。Spec → Plan → Build → Verify → Review → Ship 之 prompt **不在**。考：採者欲全週期,須二次採全 `prompts/`。文之、序之。
- **agents 缺**：`punch-ai-governance`、`punch-builder`、`punch-runtime-engineer`、`punch-performance-test-engineer` 等 persona 不附。考：init prompt 綁 `punch-ai-governance` —— 但 agent 檔不在範本！綁空？考:最小範本之 init 用 `mode: agent`(無 agent 名)避此。驗。
- **skills 缺**：`punch-context-engineering`(graphify gate)、`punch-build-caveman`(canon)、`documentation-and-adrs`、`graphify` skill 皆不附。考:init 喚 `/graphify` 倚 graphify skill —— 缺則喚空？考:`/graphify` 為外裝 skill,非範本附。鏈清否。
- **registry 缺**：`skill-registry.md`、`prompt-registry.md` 不附。考:採全後須建 registry + parity 檢。無 registry → 無 drift 守。
- **dispatcher 鏈**：`punch-builder` depth-1 派二 engineer。考:採 build 階須全鏈,半採則斷。
- **lifecycle_templates**:`docs/ai/templates/lifecycle/` + `golden-lifecycle/` worked example。考:`/punch-init` 報其 readiness,但範本附否?缺 → document_ready WARN。
- **scoped-build-policy**:ADR 0001 host npm 例外、`scoped-build-policy.md`。考:target 倉有 k6 TS 工具鏈否?無則此例外無關。
- **採用次序**:init → document → 全 lifecycle。考:文一條 migration 路徑,免採者亂序。

> ⚠ Miss → init 綁不存在之 agent,或 `/graphify` 喚空 skill。半套生命週期 = 斷鏈。
