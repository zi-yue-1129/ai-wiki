---
status: draft
last_reviewed: 2026-11-27
translation_reviewed: 2026-11-27
related:
  - theory/models/agents
tags:
  - agents
  - observability
  - LLMOps
aliases:
  - AgentOps
  - Enabling Observability of LLM Agents
  - AgentOps taxonomy
  - 代理運維
---

# AgentOps

AgentOps 指的是 LLM 代理的營運工具，也就是從開發到正式運作之間，負責追蹤、監控與評估代理的系統。Dong、Lu 與 Zhu（2024）描述此類工具應記錄哪些產物與資料。這篇論文提出的是分類法而非系統，且未報告實驗。

## 問題

語言模型的可觀測性工具通常記錄提示與模型呼叫。論文提出的問題是：代理系統應在整個生命週期中追蹤哪些產物與資料，才能從開發到正式運作都能被觀測。作者也指出，既有平台並未特別涵蓋代理的執行步驟，例如規劃、推理與記憶。

## 核心想法

作者回顧既有的 AgentOps 與 LLM 可觀測性工具，包括 AgentOps、Langfuse、LangSmith、Arize 與 Datadog，並將它們記錄的內容整理成分類法。依論文各節的呈現，類別包括：代理建立登錄；上下文增強，例如上下文內學習與檢索；提示；護欄；代理執行，涵蓋規劃、推理、記憶與工作流程；評估與回饋；追蹤，包含工作階段、trace 與 span；以及監控，包含指標與其維度。

閱讀論文時有兩點值得注意：除錯只在結論中作為未來目標出現，並非分類中的元件；合規性以歐盟 AI 法案為動機被提及，同樣不是元件。

## 演算法或公式

論文沒有給出演算法或公式。其貢獻是一套分類，告訴建構者應記錄哪些產物，以及記錄到什麼細緻程度。

## 結果

論文未報告任何工具或代理的實驗、基準測試或量測。其成果就是分類法本身，建立於對既有工具的回顧之上。

## 限制

作者在威脅效度一節列出四項限制：回顧的工具可能遺漏相關工具；概述可能未涵蓋所有與 AI 代理相關的資料屬性；既有平台未涵蓋代理的執行步驟；而跨生命週期的 trace 連結，以及步驟之間的互動，則留待未來研究。

論文曾以兩個標題發表。第一版題為 *A Taxonomy of AgentOps for Enabling Observability of Foundation Model based Agents*，目前摘要頁顯示的標題為 *AgentOps: Enabling Observability of LLM Agents*。

## 關聯

- [代理可觀測性與追蹤](agent-observability.zh-TW.md)說明分類法所假設的 trace 與 span 紀錄。
- [Dapper](dapper.zh-TW.md)提供代理追蹤所沿用的、較早的 trace 與 span 模型。
- [代理評估](agent-evaluation.zh-TW.md)涵蓋分類法同樣列出的評估紀錄。

## 參考文獻

### 開創性論文

- Dong, L.、Lu, Q. 與 Zhu, L.（2024）。*AgentOps: Enabling Observability of LLM Agents*。arXiv。https://arxiv.org/abs/2411.05285 — 本頁所討論的分類法；摘要頁顯示目前的標題。
- Sigelman, B. H. 等人（2010）。*Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*。Google 技術報告 dapper-2010-1。https://research.google.com/archive/papers/dapper-2010-1.pdf — 代理追蹤所沿用的 trace 與 span 模型。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其建構方式、應用與待解挑戰。

### 文章與文件

- OpenTelemetry。*Semantic Conventions for GenAI agent and framework spans*。https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — 代理操作的 span 慣例。頁面標示為開發中。
- Model Context Protocol。*Specification, revision 2025-06-18*。https://modelcontextprotocol.io/specification/2025-06-18 — 把日誌列為協定的額外公用功能之一。
