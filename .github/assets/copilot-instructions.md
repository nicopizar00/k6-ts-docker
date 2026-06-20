# GitHub Copilot 倉庫指令（範本 · always-on）

> ⚠ TEMPLATE only. Human adapt before ship. Not live as-is.

此乃中樞（hub）。凡 GitHub Copilot VS Code session 皆讀。細則居輻（spoke），下連之：

- 治理輻：[`instructions/governance.instructions.md`](instructions/governance.instructions.md)（`applyTo: '**'`）
- 啟引：[`prompts/punch-init.prompt.md`](prompts/punch-init.prompt.md)
- 他 LLM 轉接：[`CLAUDE.md`](CLAUDE.md) · [`AGENTS.md`](AGENTS.md)

## 綱（核心戒律）

1. **`<原則一，如 Docker First>`**：`<一句戒律>`。
2. **小步可審**：每改獨立可閱；多小 PR 勝一大 PR。
3. **存證為憑**：改未驗不為成。
4. **人裁 Ship**：Agent 開 PR 即止；merge / release / tag 皆人事。
5. **無秘鑰、無私 URL、無內務脈絡**：源、文、prompt、測入皆禁。外部 base URL 用環境變量。

## 生命週期（lifecycle）

Spec → Plan → Build → Verify → Review → Ship。各階用 `prompts/` 對應 prompt，守其 mode（Ask 唯讀；Agent 方寫）。

## Hub-Spoke

中樞唯載戒律與連。改則改輻，勿於此復述。
