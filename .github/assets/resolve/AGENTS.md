# AGENTS（解析佔位 · resolver stub · caveman-wenyan 鏡照範本）

> ⚠ STUB only — minimal mirror SNAPSHOT, NOT real content。
> ⚠ Resolve PUNCH bundle 指向倉根 `AGENTS.md` 之斷鏈(1 引：`punch-ai-governance` skill)。
> ⚠ Snapshot = caveman-wenyan 摘。Human fill / replace on adopt。

此佔位,鏡倉根 `AGENTS.md`(AI 代理導覽)之**最小摘**,使匯出後鏈不斷。

## 綱（caveman 撮）

- **編排器（orchestrator）= Punch**：`bin/punch`、`src/punch/`(stdlib Python,thin CLI)。
- **倉構**：`src/services/`(reference 服務) · `src/tests/`(k6 TS) · `src/punch/`(編排) · `docker/` · `.github/`(workflows / prompts / skills / instructions / agents)。
- **Docker First**：build / test 皆居 Docker;勿假設 host 有 node / k6。
- **執行鏈**：TS → esbuild(Docker 內) → k6 image → run → `reports/`。
- **生命週期**：Spec → Plan → Build → Verify → Review → Ship。一階一 prompt(`.github/prompts/`) + 一 agent(`.github/agents/`);Build 由 `punch-builder` dispatcher 派 `punch-runtime-engineer` / `punch-performance-test-engineer`。
- **驗證**：每 Verify run 出 `reports/state/punch-run.json`。

正源(hub)= `.github/copilot-instructions.md`。

> ⚠ On adopt: copy real `AGENTS.md` to repo root, or rewrite to own repo agents。
