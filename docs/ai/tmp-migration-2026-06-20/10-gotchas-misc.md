# 10 · 雜陷 · gitignore · encoding · 多倉（misc gotchas）

> ⚠ IDEA scratch。Long tail。易漏之碎。

碎陷,易漏：

- **gitignore 條目**:採者須加 `graphify-out/`、`docs/ai/governance/init/`、`dist/`、`reports/`。考:漏一 → disposable/生成物入版控,脹倉、洩。
- **encoding/BOM**:全檔 UTF-8 no-BOM。考:Windows 編輯器加 BOM?CRLF vs LF?`.gitattributes` 鎖 LF 否。
- **fullwidth 標點**:文言用 `，。：（）` fullwidth。考:grep/正則撞 ASCII `,.:()`?工具鏈處理否。
- **檔名規**:`*.prompt.md`、`*.instructions.md` 後綴須準(VS Code 識)。考:採者 rename 破後綴?
- **相對鏈深度**:`../`、`../../`、`../../../` 易 off-by-one(見 history:59)。考:採後檔移位 → 鏈深變 → 全斷。link-check CI 否。
- **link-check 自動化**:考:加 markdown link checker(scope `.github/` + `docs/ai/` + `resolve/`)於 CI,守 self-resolution。本 PR 之 0-uncovered 應入 CI gate,免回退。
- **resolve 映射文**:考:採者懂 `resolve/X → 根/X` 否?init 自移 or 手移?文一步驟。
- **多倉/monorepo**:多 `.github`?考:哪生效。sub-package 治理。
- **i18n/locale**:CI runner locale 影響 CJK sort/render?考:`LANG=C` 破中文。
- **disposable 清理**:此 `tmp-migration-2026-06-20/` 夾 disposable。考:採完即刪,勿入持久 canon。gitignore or 手刪。
- **版本快照日期**:resolve snapshot、此夾皆帶 2026-06-20。考:日期戳助辨舊。採後標源 commit hash。
- **回滾**:採壞如何退?考:init 非破壞、dry-run 默 —— 但手移 resolve/* 後須能退。git branch 採用。
- **文檔發現性**:考:`docs/how-to-run.md` 加 `punch init` 一行,助採者尋入口。

> ⚠ Miss link-check CI → self-resolution 回退無人知。最值自動化之守。
