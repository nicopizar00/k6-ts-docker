# 03 · VS Code Copilot · prompt/instruction 識別（IDE wiring）

> ⚠ IDEA scratch。Files exist ≠ Copilot loads them。

VS Code Copilot 配線,易漏：

- **prompt 檔識別**：`.github/prompts/*.prompt.md` 須設 `chat.promptFiles: true`(workspace `.vscode/settings.json` 或 user)。考：範本附 `.vscode/settings.json` 否？採者自設否？未設 → `/punch-init` 不現於 Chat。
- **instruction applyTo**：`.github/instructions/*.instructions.md` 之 `applyTo: '**'` 方全域生效。考：frontmatter 完否？glob 對否？`governance.instructions.md` 須 always-on。
- **copilot-instructions 自載**：`.github/copilot-instructions.md` Copilot 自讀(無需設定,新版)。考：版本支援否。
- **Ask vs Agent mode**：prompt 宣 mode(Ask 唯讀、Agent 方寫)。考：採者於對 mode 執否？Init = Agent。誤 mode → 不寫 or 越權。
- **mode frontmatter 鍵**：範本 `punch-init.prompt.md` 用 `mode: agent`;活倉版用 `agent: <name>`。考：二鍵異！VS Code 識 `mode`?還是 `agent`? 驗之。漏 → prompt 不綁代理。
- **agents/skills 載**：`.github/agents/`、`.github/skills/` —— 最小範本**不附**(唯 init prompt)。考：採者欲全生命週期,須另採 agents/skills。文之。
- **slash 命名撞**：`/punch-init`、`/graphify` 為 Copilot slash。考：與既有 slash 撞否。
- **workspace trust**：VS Code 需 trust workspace 方執 prompt/tool。考：CI / headless 無 UI trust。
- **多根 workspace**：monorepo 多 `.github`?考：哪個 `.github` 生效。

> ⚠ Miss `chat.promptFiles` → 範本最重之 init prompt 隱形。第一陷。
