# 00 · 前置 · 主機 · 工具裝備（preflight / host / tooling）

> ⚠ IDEA scratch。Consider before migrate。

採範本前,主機備否？易漏：

- **VS Code 版本**：Copilot Chat `prompts/*.prompt.md` 功能須新版 + 設 `chat.promptFiles: true`。舊版不識 prompt 檔。考：target 倉貢者皆裝否？
- **GitHub Copilot 訂閱/權**：Agent Mode 須 Copilot 啟。免費層或無 Agent。考：team seat 備否。
- **Graphify 裝**：`/punch-init` 喚 `/graphify`,須 `uv tool install graphifyy` 先裝於本機。考：`uv` 在否？Python 版合否？Mac/Linux/WSL 差異。
- **Python 3 stdlib**：Punch 編排 stdlib only。考：target 主機 python3 在 PATH 否？版本(3.10+ 用 `str | None` syntax)？
- **Docker / Compose**：Docker First。考：target 倉有 Docker 工作流否？或純 Copilot 治理採用(無 Docker)？範本之 Docker 戒律或不合非-Docker 倉。
- **OS/shell 差異**：darwin vs linux CI；zsh vs bash;路徑分隔。考：bin/* 腳本可移植否。
- **網路/代理**：graphify semantic extract 用 in-IDE model(無 key);headless backend 需 key。考：企業代理擋否。
- **uv 工具污染**：`uv tool install` 全域裝。考：版本鎖否(`graphifyy` v0.8.41 baseline,ADR 0002)。
- **首次 clone 體積**：`.github/` + `docs/ai/` 文量。考：target 倉容忍否。

> ⚠ Miss 一者 → `/punch-init` graphify 軌或 WARN,或 prompt 不被識。先 doctor。
