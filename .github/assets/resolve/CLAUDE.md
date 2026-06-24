# CLAUDE（解析佔位 · resolver stub · caveman-wenyan 鏡照範本）

> ⚠ STUB only — minimal mirror SNAPSHOT, NOT real content。
> ⚠ Resolve PUNCH bundle 指向倉根 `CLAUDE.md` 之斷鏈(2 引：`copilot-instructions.md`、`punch-context-engineering` skill)。
> ⚠ Snapshot = caveman-wenyan 摘。Human fill / replace on adopt。

此佔位,鏡倉根 `CLAUDE.md`(專案戒律源)之**最小摘**,使匯出後鏈不斷。原文乃單一真源,此唯撮其綱。

## 綱（caveman 撮）

- **Docker First**：build / run / validate 皆居 Docker。Host 唯需 Docker + stdlib Python 3。無 Node、無 k6、無 pip。
- **執行鏈（execution chain）**：TS 源 → esbuild(builder stage) → Docker image → k6 run → reports(JSON / HTML / state)。勿斷、勿繞。
- **生命週期**：Spec → Plan → Build → Test → Review → Ship。各階一 prompt(`.github/prompts/`),守其 mode。
- **戒**：小步可審 · 無冗依賴 · 無早抽象 · 存證為憑(改未驗不為成)。
- **驗證憑**：`reports/state/punch-run.json` 記 Verify run,方為「成」。

正源(hub)= `.github/copilot-instructions.md`;細則居輻。

> ⚠ On adopt: copy real `CLAUDE.md` to repo root, or rewrite to own repo rules。
