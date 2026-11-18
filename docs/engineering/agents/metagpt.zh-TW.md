---
status: draft
last_reviewed: 2026-11-18
translation_reviewed: 2026-11-18
tags:
  - agents
  - multi-agent
  - software engineering
aliases:
  - MetaGPT
  - Meta Programming
  - 標準作業程序代理
  - 元程式設計多代理框架
---

# MetaGPT（Hong 等人，2023）

MetaGPT 是一個多代理框架，讓語言模型代理扮演軟體公司的角色：產品經理、架構師、專案經理、工程師與 QA 工程師。每個角色產出一份定義明確的文件，文件沿著流水線傳遞。Hong 等人（2023）報告，這種結構在 HumanEval 與 MBPP 程式碼基準上的 Pass@1 分數，高於其比較的程式碼模型。論文發表於 ICLR 2024。

本頁是[多代理編排模式](multi-agent-orchestration.zh-TW.md)中順序流水線模式背後的命名方法之一。本頁也是[代理工程](index.zh-TW.md)的一部分。

## 概述

軟體開發很適合用流水線處理，因為工作本來就分成若干階段，各階段都有可辨識的產出：需求、設計、計畫、程式與測試。MetaGPT 沿用人類實務中的這種分工，並把每個階段交給一個代理。論文的核心主張是，結構化的中間文件能防止錯誤沿著鏈條累積。

## 問題

未經結構化而串接的語言模型，可能產生彼此矛盾的結果，因為早期錯誤會被帶往後續步驟並逐步放大。摘要將先前系統在複雜任務上的失敗歸因於「簡單串接 LLM 所造成的串聯幻覺，進而導致邏輯不一致」。論文要探討的是，一組代理如何處理複雜任務，同時讓每一步的輸出都能被檢查。

## 核心想法

作者把標準作業程序（SOP），也就是人類團隊遵循的書面例行流程，編碼為提示序列，並要求每個角色產出指定的內容：

- **產品經理**撰寫產品需求文件（PRD），包含使用者故事與需求池。
- **架構師**把 PRD 轉換為檔案清單、資料結構、介面定義與序列流程圖。
- **專案經理**把設計拆成任務清單，每個程式檔案是一項任務。
- **工程師**實作指派的類別與函式，撰寫單元測試、執行並除錯。
- **QA 工程師**撰寫測試案例，以確保程式品質。

論文把這稱為組裝線（assembly-line）範式。中間文件是角色之間的約定：每個代理接收定義好的輸入，並必須產出定義好的輸出。

## 方程式或演算法

此程序是固定的步驟序列：

1. 接收使用者提供的一行需求。
2. 產品經理產出 PRD。
3. 架構師產出系統設計。
4. 專案經理產出任務清單，每個程式檔案一項任務。
5. 工程師實作每個檔案、撰寫單元測試、執行測試，並依結果修正程式。
6. QA 工程師撰寫測試案例。
7. 輸出是共同構成軟體解決方案的文件與程式碼。

可執行回饋在第 5 步加入。作者在消融實驗中移除這一步，以衡量其效果。

## 結果

在 HumanEval（164 個任務）與 MBPP 上，以 Pass@1 衡量，MetaGPT 分別得到 85.9% 與 87.7%。若沒有可執行回饋，則分別為 81.7% 與 82.3%，因此回饋帶來 4.2 與 5.4 個百分點的提升。論文報告的數字高於其比較中的程式碼模型。

相對於強大的單一模型，優勢則較小。作者自行進行的單一代理 GPT-4 實驗中，HumanEval 採直接 API 呼叫時得分為 72.4%；加入系統提示或較佳的答案解析後，則為 80.0% 至 81.2%。因此，與早期系統之間的差距，很大程度取決於基準的執行方式。

在論文的 SoftwareDev 比較中，MetaGPT 的可執行性得分為 3.75，ChatDev 為 2.25；人工修訂成本方面，MetaGPT 為 0.83，ChatDev 為 2.5。它也使用了更多 Token：MetaGPT 為 31,255，ChatDev 為 19,292。

## 限制

- **角色範圍。**作者表示，此系統無法完整涵蓋 UI 與前端等情境，因為它沒有對應的代理與多模態工具。
- **複雜需求。**儘管產出的程式碼比同類框架多，作者承認，要滿足真實應用中多樣而複雜的需求仍然困難。
- **中斷。**使用者面臨的一項關鍵挑戰，是中斷代理正在執行的程序，或設定檢查點。
- **自我改進。**自我改進機制只修改角色限制，不修改角色之間的通訊介面（附錄 A.1）。各個專案也彼此獨立運行。
- **基準範圍窄。**HumanEval 與 MBPP 測試的是簡短的函式層級程式，其分數無法衡量整個軟體專案的交付能力。
- **成本。**SoftwareDev 的 Token 數顯示，結構化的角色流水線可能比其他做法耗用更多 Token。

## 關聯

- 以對話為基礎的替代方案是 [AutoGen](autogen.zh-TW.md)，其流程來自訊息交換，而非固定角色。
- 處理儲存庫問題的單一代理軟體工程師是 [SWE-agent](swe-agent.zh-TW.md)。
- 代理的一般框架見 [AI 代理](../../theory/models/agents/index.zh-TW.md)。

## 應用

- **原型產生**：從簡短需求出發，在接受程式碼之前先審查設計文件。
- **工程文件**：需求與設計文件由人類審查前的草稿撰寫。

## 開放問題

- 為軟體開發撰寫的 SOP，能否轉移到硬體設計或研究等其他領域？
- 人類應如何介入長流水線，同時不破壞共享文件？
- 流水線進行到中途時需求改變，會發生什麼事？

## 參考文獻

### 開創性論文

- Hong, S. 等人（2023）。*MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*。arXiv；發表於 ICLR 2024。https://arxiv.org/abs/2308.00352 — 讓代理扮演軟體公司角色，把 SOP 編碼為提示，並報告有與無可執行回饋時的 HumanEval 與 MBPP 結果。
- Chen, M. 等人（2021）。*Evaluating Large Language Models Trained on Code*。arXiv。https://arxiv.org/abs/2107.03374 — 提出 HumanEval，這是從文件字串合成程式的基準。
- Austin, J. 等人（2021）。*Program Synthesis with Large Language Models*。arXiv。https://arxiv.org/abs/2108.07732 — 提出 MBPP，這是一組由白話描述撰寫的簡短 Python 程式基準。
- Qian, C. 等人（2023）。*ChatDev: Communicative Agents for Software Development*。arXiv。https://arxiv.org/abs/2307.07924 — 論文所比較的角色式軟體開發框架。
- Wu, Q. 等人（2023）。*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*。arXiv。https://arxiv.org/abs/2308.08155 — 固定角色流水線的對話式替代方案。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — LLM 代理的綜述，包括多代理協作。
