# 02 · `<...>` 占位 · resolve 鏡照填實（placeholders / resolve snapshots）

> ⚠ IDEA scratch。Template ships holes + mirror stubs。Human fill on adopt。

範本之空,易漏填：

- **`<...>` 占位**：`copilot-instructions.md`(原則一、戒律)、`governance.instructions.md`(`<驗證命令>`、`<報告路徑>`、路徑規則)皆帶 `<...>`。考：grep `<.*>` 掃盡,逐一填本倉值。漏一 → Copilot 讀佔位為字面,亂。
- **原則一(rule 1)**：範本 `<原則一,如 Docker First>`。考：本倉首戒為何？非-Docker 倉則異。
- **resolve 鏡照填實**：`resolve/CLAUDE.md`、`resolve/AGENTS.md`、`resolve/docs/architecture/punch-boundaries.md`、`resolve/docs/workflows/validation.md` 皆 **caveman-wenyan 最小 snapshot**,非真文。考：採後 copy → 真路 + 填實文,或重寫合本倉。
- **鏡照 vs 真文漂移**：snapshot 凍於 2026-06-20 源倉態。考：採後鏡照即舊。`/punch-init` certify 覆蓋(coverage),**不** certify 新鮮(freshness)。誰保鏡照同步真文？
- **resolve 路映射**：`resolve/X` → 倉根 `X`;`resolve/docs/Y` → `docs/Y`。考：採者懂此映射否？文之、或 init 自移？
- **占位漏掃自動化**：考：加 CI / pre-commit grep `<[^>]+>` 於 `.github/**` 擋未填占位。
- **空 instruction 輻**：範本唯 `governance.instructions.md` 一輻。考：本倉需更多 path-specific 輻(src/**、tests/**)？範本留鉤(`<於此增本倉路徑規則>`)。

> ⚠ Miss → Copilot 見 `<驗證命令>` 當真,或鏈指空 snapshot。
