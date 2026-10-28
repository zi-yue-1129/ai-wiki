---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - multi-agent
  - orchestration
aliases:
  - Multi-Agent Orchestration
  - Multi-Agent Systems
  - LLM Multi-Agent
  - 多代理編排
  - 多代理系統
---

# 多代理編排模式

多代理編排（multi-agent orchestration）安排數個各有角色的語言模型代理，使它們能共同完成任務。設計上的問題包括如何分工、代理之間如何傳遞資訊，以及何時結束整個群組的運作。

本頁是[代理工程](index.zh-TW.md)的一部分。

## 概述

一個配備許多工具的代理，往往就能完成任務。當子任務需要不同的指令、不同的工具或獨立的上下文視窗時，把工作拆給多個代理會有幫助。代價是協調。每增加一個代理，就增加模型呼叫、延遲，以及錯誤進入系統的一個新位置。這個領域還很年輕，多數模式是在框架論文中描述，而非在受控比較中檢驗。

## 關鍵概念

- **角色：**一個代理的指令、工具與預期輸出，例如規劃者、程式撰寫者或審查者。
- **編排者（路由器）：**決定下一個由哪個代理行動的代理或固定程式。
- **交接（handoff）：**控制權與上下文從一個代理轉移到另一個代理。
- **共享狀態：**代理共同讀寫的儲存空間，例如文件或訊息紀錄。
- **終止條件：**結束交流的規則，例如測試通過、達到最大輪數，或人類做出決定。

## 運作方式

文獻與框架中反覆出現四種模式。

1. **編排者。**規劃者拆分任務、把各部分交給專家，並合併結果。這是最容易檢查的模式，因為所有訊息都經過同一個點。
2. **順序流水線。**每個代理轉換前一個代理的輸出，例如從需求到設計，再到程式與測試。MetaGPT（Hong 等人，2023）把軟體團隊的標準作業程序編碼為各角色的提示序列。
3. **對話群組。**代理在共享的對話串中交談，直到滿足終止條件。AutoGen（Wu 等人，2023）是一個框架，用來以可對話的代理建構應用程式，這些代理可以結合語言模型、人工輸入與工具，且對話模式可用程式碼或自然語言設定。
4. **模擬社會。**代理生活在共享的模擬世界中，或作為彼此溝通的對象。Generative Agents（Park 等人，2023）以互動式代理來模擬人的行為，CAMEL（Li 等人，2023）則研究語言模型社會中的溝通代理。

## 取捨

- **成本與延遲。**每個代理都會在每一步增加模型呼叫，而對話式模式可能拖得很長。
- **錯誤串連。**沒有結構地串接模型，會讓早期錯誤擴散。MetaGPT 的作者將多代理系統中的邏輯不一致歸因於簡單串接所造成的幻覺累積，並以結構化程序作為解法。
- **難以評估。**成功取決於整個群組。可用的衡量方式見[代理評估](agent-evaluation.zh-TW.md)。
- **協調隱藏。**共享狀態與訊息紀錄必須被追蹤，才能查出某個決定為何而做。見[代理可觀測性](agent-observability.zh-TW.md)。

## 關聯

- 強化學習中的多代理學習，包括學會溝通的代理，見[多代理強化學習](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.zh-TW.md)。
- 共享狀態式編排與認知科學中的廣播理論之間，有一個寬鬆的類比，見[全域工作空間](../../brain-mind/consciousness/global-workspace/index.zh-TW.md)。這只是設計上的類比，並非兩個系統的實證證據。
- 代理的一般框架，見[AI 代理](../../theory/models/agents/index.zh-TW.md)。

## 應用

- **軟體開發**：由規劃者、程式撰寫者、測試者與審查者分工。
- **研究協助**：一個代理搜尋，另一個閱讀，第三個撰寫摘要。
- **客服營運**：路由器把每個請求交給擁有專屬工具的專家。

## 開放問題

- 在相同預算下，何時一群代理會勝過一個擁有相同工具的代理？
- 在開放式對話中，什麼機制能讓終止條件可靠？
- 當共享狀態中的錯誤來自某個代理的輸出時，責任應如何劃分？

## 參考文獻

### 開創性論文

- Wu, Q. 等人（2023）。*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*。arXiv。https://arxiv.org/abs/2308.08155 — 以可對話代理建構應用程式的框架，可加入人工輸入與工具。
- Hong, S. 等人（2023）。*MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*。arXiv。https://arxiv.org/abs/2308.00352 — 把標準作業程序編碼為角色代理的提示序列，並報告簡單串接造成的錯誤累積。
- Li, G. 等人（2023）。*CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society*。arXiv。https://arxiv.org/abs/2303.17760 — 研究在語言模型社會中合作的溝通代理。
- Park, J. S. 等人（2023）。*Generative Agents: Interactive Simulacra of Human Behavior*。arXiv。https://arxiv.org/abs/2304.03442 — 在共享環境中模擬互動式代理，作為人類行為的模型。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋其建構方式、應用與待解挑戰。
