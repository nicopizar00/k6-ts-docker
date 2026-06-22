# 06 · 安掃 · 秘鑰 · 存證 · validation（security / evidence）

> ⚠ IDEA scratch。Security gate blocks certify。Evidence = done。

安全與存證,易漏：

- **安掃前置**:`/punch-init` security scan 阻 certify 若見洩。考:採前自掃倉 —— 秘鑰、私 URL、內務脈絡(戒律五)入 `.github/`/`docs/ai/` 否?
- **私 URL**:範本戒「外部 base URL 用環境變量」。考:target 倉 hardcode internal host 否?測入(test fixtures)藏 URL 否。
- **秘鑰於 history**:git history 藏舊 key?考:安掃當下文,不掃 history。深掃否(gitleaks)。
- **存證軌**:範本戒「改未驗不為成」,憑 = `reports/state/punch-run.json`。考:target 倉 validation 路異!非 k6 倉無此檔。`<驗證命令>`、`<報告路徑>` 占位須填本倉真軌。
- **CI 工作流缺**:`.github/workflows/k6.yml`、`copilot-setup-steps.yml` **不在**最小範本。考:target 倉自有 CI;範本之 validation 假設或不合。
- **graphify-out 洩**:`graphify-out/` 含倉碼語義圖 —— 須 gitignore,never commit(ADR 0002)。考:採者加 ignore 否?圖洩 = 碼結構洩。
- **init 報洩**:`docs/ai/governance/init/` disposable 報 —— gitignore 否?含掃結果。
- **Agent 寫權**:範本非破壞、dry-run 默。考:採者誤 `--write` 早?或 Agent mode 越權改。守 plan-gate。
- **依賴鏈安全**:graphify(`graphifyy`)、yt-dlp(graphify video extra)外裝 —— 供應鏈。考:pin 版本、驗 source。

> ⚠ Miss → certify 假 PASS(掃漏),或存證指錯軌 → 「done」不真。
