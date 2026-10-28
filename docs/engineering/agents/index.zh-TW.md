---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - engineering
aliases:
  - Agent Engineering
  - 代理工程
  - AI 代理工程
---

# 代理工程

代理工程是建構讓語言模型採取行動之系統的實務：模型會呼叫工具、在環境中工作、與其他代理協調，並在正式運作時接受評估與監控。模型只是其中一個元件，大部分工程工作落在模型周圍的介面、控制與量測上。

## 概述

[AI 代理](../../theory/models/agents/index.zh-TW.md)頁說明代理是什麼。本節則說明如何建構一個能被信任、可執行真實行動的代理。只回答問題的代理，需要一個提示與一組測試集；會採取行動的代理，則需要明確定義的工具組、對這些工具可觸及範圍的限制、在單一代理不足時拆分工作的方式、以結果而非文字來衡量的基準，以及每次執行的紀錄。

## 關鍵概念

- **駕馭層（harness）：**讓模型在迴圈中運作、傳遞工具與觀察結果並決定何時停止的程式碼。
- **環境（environment）：**代理可以觀察與改變的系統，例如檔案系統、瀏覽器或 API。
- **軌跡（trajectory）：**一次執行的紀錄，從最初請求到最終狀態。
- **控制（control）：**權限、確認或上限，用來限制代理可以做的事。

## 運作方式

典型的代理迴圈會觀察目前狀態，請模型決定下一步行動，透過工具執行該行動，並記錄結果。當目標達成、達到上限或人員介入時，迴圈結束。每個階段都有對應的工程考量：工具設計決定模型能請求什麼；沙箱決定一個壞的行動能觸及什麼；編排決定工作如何拆分；評估決定迴圈是否成功；可觀測性決定事後能否解釋失敗。

## 關鍵方法

本節有五頁，各自涵蓋工作的一部分。每頁都比較一組做法，方便讀者選擇。

- [工具呼叫與模型上下文協定（MCP）](tool-calling-and-mcp.md)：模型如何請求行動，以及標準協定如何把工具連接到應用程式。
- [沙箱與電腦操作代理](sandboxing-and-computer-use.md)：透過畫面操作軟體的代理如何被隔離，並維持在其權限之內。
- [多代理編排模式](multi-agent-orchestration.md)：編排者、流水線、對話群組與模擬社會，以及各自的成本。
- [代理評估](agent-evaluation.md)：檢查最終狀態的基準，以及與之並用的可靠度與成本指標。
- [代理可觀測性與追蹤](agent-observability.md)：記錄 span 與 trace，使執行過程可以除錯、監控與稽核。

## 關聯

- 代理的理論，包括規劃與記憶，見[AI 代理](../../theory/models/agents/index.zh-TW.md)。
- 讀取不受信任內容的代理會面臨[LLM 應用安全](../llm-security/index.zh-TW.md)所述的風險。
- 檢索常是代理的工具之一，見[檢索增強生成](../rag/index.zh-TW.md)。
- 推理與代理的基準，見[推理與代理基準](../../theory/evaluation/benchmarks/reasoning-agents/index.zh-TW.md)。

## 應用

- **軟體工程代理**：閱讀程式庫、編輯檔案並執行測試。
- **客服營運代理**：查詢帳戶並執行已核准的變更。
- **研究助理**：搜尋、閱讀來源，並撰寫附引用的摘要草稿。

## 開放問題

- 哪些代理設計在具有許多工具的長任務中仍保持可靠？
- 人、代理與它所改變的系統之間，責任應如何劃分？
- 能否在執行前預估代理的成本？

## 參考文獻

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其建構方式、應用與待解挑戰。
- Kapoor, S. 等人（2024）。*AI Agents That Matter*。arXiv。https://arxiv.org/abs/2407.01502 — 主張代理評估應同時報告成本與準確率。

### 開創性論文

- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — 交錯推理與行動，使模型能依工具結果規劃並更新步驟。
- Schick, T. 等人（2023）。*Toolformer: Language Models Can Teach Themselves to Use Tools*。arXiv。https://arxiv.org/abs/2302.04761 — 訓練模型決定何時及如何呼叫外部工具。
- Wu, Q. 等人（2023）。*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*。arXiv。https://arxiv.org/abs/2308.08155 — 以對話中的代理建構應用的框架。

### 文章與文件

- Model Context Protocol。*Specification, revision 2025-06-18*。https://modelcontextprotocol.io/specification/2025-06-18 — 把模型連接到工具、資料與提示的開放協定。
