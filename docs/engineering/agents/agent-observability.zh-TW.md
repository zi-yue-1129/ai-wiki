---
status: draft
last_reviewed: 2026-11-27
translation_reviewed: 2026-11-27
tags:
  - agents
  - observability
  - monitoring
aliases:
  - Agent Observability
  - Agent Tracing
  - LLM Tracing
  - LLM observability
  - 代理可觀測性
  - 代理追蹤
---

# 代理可觀測性與追蹤

代理可觀測性（agent observability）是指記錄足夠多的代理執行過程，以便在正式運作中除錯、評估與監控。追蹤（trace）依序記錄每次模型呼叫、工具呼叫與決定，使失敗的任務能一步一步重建。

本頁是[代理工程](index.zh-TW.md)的一部分。

## 概述

代理的行為分散在許多步驟與元件之中，最終的輸出通常看不出執行在哪裡出了錯。可觀測性讓執行過程可以被檢視。它能回答諸如：呼叫了哪個工具、使用什麼參數、回傳了什麼、用了多少 token、每一步花了多少時間。同一批紀錄也支援成本追蹤、事故審查，以及比較兩個代理版本。

追蹤在分散式系統中是成熟的概念。Dapper（Sigelman 等人，2010）是 Google 的正式運作追蹤系統，其基本要求是廣泛部署與持續監控，具體目標則為低開銷、應用層透明與可擴展性。代理追蹤把同一套 trace 與 span 模型套用到一連串模型與工具呼叫上。

## 關鍵概念

- **追蹤（trace）：**一項任務從請求到結果的完整紀錄。
- **span：**追蹤中的一個工作單位，例如一次模型呼叫或工具呼叫。OpenTelemetry 的代理慣例為每個代理操作提供一個具名稱與種類的 span（見下方「運作方式」）。
- **事件（event）：**附在 span 上的帶時間戳記註記，例如錯誤或使用者確認。
- **指標（metric）：**跨多次執行的彙總，例如 token 數、延遲、成本或錯誤率。
- **遮蔽（redaction）：**在儲存提示與工具結果之前，移除其中的個人資料或機密。

## 運作方式

每次模型呼叫、工具呼叫、檢索與代理步驟都會被包裝成一個 span，並巢狀排列，使整次執行形成一棵樹。屬性記錄模型名稱、token 數與工具參數。span 被匯出到後端，可在其中搜尋、繪圖或抽樣。追蹤也支援重播：失敗的執行可以逐步重新執行，找出與預期分歧的步驟；追蹤也可以被自動評分，見[代理評估](agent-evaluation.zh-TW.md)。

OpenTelemetry 已發布生成式 AI 的語意慣例。其代理 span 慣例目前為開發中（Development）狀態，定義了 create-agent span（種類 CLIENT）與 invoke-agent span（種類 INTERNAL）。invoke-agent span 會記錄操作名稱、可用時的代理名稱，以及應用程式具備時的對話識別碼。這些慣例已移至獨立的儲存庫，且可能改變，因此實作應固定所用的版本。

## 關鍵方法

兩種具代表性的做法構成本主題的基礎。每種都有自己的頁面，包含問題、機制、實測結果與限制。

- [Dapper](dapper.zh-TW.md)（分散式追蹤，2010）：以 span 樹表示追蹤，並借助抽樣使常態追蹤負擔得起。代理追蹤沿用其模型，但其開銷數據來自網路搜尋服務，而非代理。
- [AgentOps](agentops.zh-TW.md)（Dong、Lu 與 Zhu，2024）：一份分類法，列出代理系統在整個生命週期中應追蹤的產物與資料。論文未報告實驗。

OpenTelemetry 代理 span 慣例屬於規範，而非有自身結果的方法，因此放在「運作方式」中說明。

## 隱私與安全

提示、檢索到的文件與工具結果，可能含有個人資料、憑證或機密文字。儲存這些內容的追蹤，本身就成為一個有風險的新資料儲存處。良好做法是在匯出前遮蔽敏感欄位、設定保留期限、限制誰能讀取追蹤，並為稽核而記錄工具呼叫。這些紀錄也支援[LLM 應用安全](../llm-security/index.zh-TW.md)中所述的最小權限與確認控制。

## 限制

- **資料量。**長時間執行的完整追蹤非常龐大，抽樣雖能降低成本，卻可能漏掉罕見的失敗。
- **解釋。**追蹤顯示發生了什麼，卻不顯示模型為何選擇某個行動。解釋選擇需要其他方法。
- **標準仍在變動。**不同版本的慣例可能不同，依賴它們的儀表板需要維護。
- **隱私取捨。**為除錯而記錄得越多，儲存的敏感資料也越多。
- **證據。**追蹤開銷的量測來自 2010 年 Google 的服務，AgentOps 分類法也未在實際使用中量測。代理工作負載的追蹤成本需要另行量測。

## 關聯

- 評估與可觀測性使用相同的軌跡，見[代理評估](agent-evaluation.zh-TW.md)。
- 模型上下文協定規範把日誌列為其額外公用功能之一，使伺服器能以標準方式回報事件，見[工具呼叫與 MCP](tool-calling-and-mcp.zh-TW.md)。
- 以監控作為注入防禦的做法，見[LLM 應用安全](../llm-security/index.zh-TW.md)。

## 應用

- **除錯迴圈**：代理重複相同的工具呼叫而沒有進展。
- **依任務類型、模型或使用者群組追蹤成本**。
- **事故審查**：在有害行動發生後，利用紀錄下來的步驟檢視經過。
- **比較版本**：在真實流量上比較代理的不同版本，並以追蹤作為證據。

## 開放問題

- 詳細追蹤與隱私之間，應如何取得平衡？
- 追蹤能否解釋模型的選擇，而不只是記錄它？
- 哪些指標最能預測代理在新任務上會失敗？

## 參考文獻

### 文章與文件

- OpenTelemetry。*Semantic Conventions for GenAI agent and framework spans*。https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — 定義代理的 create-agent 與 invoke-agent span 及其屬性。頁面標示為開發中，固定版本前請查看目前的內容。
- Model Context Protocol。*Specification, revision 2025-06-18*。https://modelcontextprotocol.io/specification/2025-06-18 — 把日誌列為協定的額外公用功能之一。

### 開創性論文

- Sigelman, B. H. 等人（2010）。*Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*。Google 技術報告 dapper-2010-1。https://research.google.com/archive/papers/dapper-2010-1.pdf — 描述 trace、span 與註記模型，以及正式運作系統的開銷數據。
- Dong, L.、Lu, Q. 與 Zhu, L.（2024）。*AgentOps: Enabling Observability of LLM Agents*。arXiv。https://arxiv.org/abs/2411.05285 — 本頁所討論、列出代理生命週期中應追蹤產物與資料的分類法；摘要頁顯示目前的標題。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其建構方式、應用與待解挑戰。
