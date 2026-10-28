---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - reinforcement learning
  - memory
aliases:
  - Reflexion
  - Verbal Reinforcement Learning
  - 語言回饋強化
  - 反思式代理
---

# Reflexion（Shinn 等人，2023）

Reflexion 是一個框架，能在不改變權重的情況下，讓語言代理跨越多次嘗試而改進。每次失敗後，代理會就所收到的回饋寫下語言形式的反思，並把它存入記憶緩衝區，該反思隨後會影響下一次嘗試。Shinn 等人（2023）提出此框架，並報告在決策、程式與推理任務上的進步。

本頁是[代理工程](index.zh-TW.md)的一部分，也是本節所涵蓋的命名方法之一。

## 概述

傳統強化學習透過許多回合、許多次梯度更新來改進代理，對大型語言模型而言成本很高。Reflexion 採取另一條路線。它不改變權重，而是改變上下文：代理以文字形式從一次嘗試的結果中學習，並把這段文字帶入下一次嘗試。

## 問題

與遊戲、編譯器或 API 等環境互動的語言代理，可能一再以相同方式失敗。每次失敗後都微調，既慢又昂貴。問題在於：代理如何在不做大規模訓練的情況下，從試誤中快速學習。

## 核心想法

Reflexion 有三個角色。行動者（actor）在環境中產生一段行動軌跡。評估者（evaluator）為軌跡評分，回饋訊號可以是純量或自由形式的語言，可來自外部，也可由內部模擬。接著，自我反思步驟會寫下一段簡短的語言分析，說明哪裡出錯、下一次該試什麼。反思被保存在情節記憶緩衝區中，行動者在下一次嘗試開始時讀取它。論文指出，回饋可以是純量或語言，可以來自代理外部，也可以是內部模擬的。

## 方程式或演算法

對每項任務，重複固定次數的嘗試：

1. 行動者在目前任務與已儲存的反思引導下執行一次嘗試。
2. 評估者為這次嘗試評分。
3. 若成功，即停止；否則，自我反思步驟依據軌跡與回饋寫出反思。
4. 把反思附加到記憶緩衝區，然後開始下一次嘗試。

整個迴圈中，權重都不會改變。

## 結果

摘要指出，Reflexion 在序列決策、程式與語言推理任務上，相對於基線代理都有顯著的進步。在 HumanEval 程式基準上，它達到 91% 的 pass@1，高於摘要所給出、作為先前最佳結果的 GPT-4 的 80%。論文也對回饋類型、回饋納入方法與代理類型進行了消融與分析。在 AlfWorld 上，Reflexion 相較 ReAct 在 12 次學習試驗中絕對提升 22%。

## 限制

- **依賴回饋品質。**評估者薄弱，反思就會薄弱，而且反思可能編碼錯誤的教訓。
- **記憶讓上下文變長。**儲存的反思會佔用上下文視窗，因此長期記憶需要篩選。
- **重複嘗試成本較高。**進步來自額外的嘗試，因此與單次嘗試系統的比較，取決於所用的預算。
- **基準範圍。**報告的結果只涵蓋論文中的任務；能否推廣到開放式情境，仍是未解問題。

## 關聯

- Reflexion 建立在 [ReAct](react.zh-TW.md) 的迴圈之上，並加入跨次嘗試的回饋。
- 以回饋訊號驅動改進的強化學習框架，見[強化學習](../../theory/paradigms/reinforcement-learning/index.zh-TW.md)。
- 情節記憶及其在學習中的角色，見[大腦中的記憶與學習](../../brain-mind/memory-learning/index.zh-TW.md)。
- 這類代理測試所用的程式基準包括 [HumanEval](../../theory/evaluation/benchmarks/math-and-code/humaneval.zh-TW.md)。

## 應用

- 執行測試、讀取失敗訊息並重試的程式代理。
- 不需重新訓練，就能跨回合學習策略的遊戲或模擬代理。

## 開放問題

- 反思在存入記憶前，應如何檢查？
- 語言記憶在什麼時候停止幫助、開始誤導？

## 參考文獻

### 開創性論文

- Shinn, N. 等人（2023）。*Reflexion: Language Agents with Verbal Reinforcement Learning*。NeurIPS。https://doi.org/10.52202/075280-0377 — 提出 Reflexion，把語言反思存入情節記憶，不更新權重即可改進之後的嘗試。
- Yao, S. 等人（2023）。*ReAct: Synergizing Reasoning and Acting in Language Models*。ICLR。https://arxiv.org/abs/2210.03629 — Reflexion 所延伸的推理與行動迴圈。
- Madaan, A. 等人（2023）。*Self-Refine: Iterative Refinement with Self-Feedback*。NeurIPS。https://doi.org/10.52202/075280-2019 — 透過反覆的自我回饋來改進輸出，是相關的構想，但沒有跨任務的情節記憶。
- Chen, M. 等人（2021）。*Evaluating Large Language Models Trained on Code*。arXiv。https://arxiv.org/abs/2107.03374 — 提出 HumanEval 與用來為程式嘗試評分的 pass@k 指標。

### 調查與教科書

- Xi, Z. 等人（2023）。*The Rise and Potential of Large Language Model Based Agents: A Survey*。arXiv。https://arxiv.org/abs/2309.07864 — 對以 LLM 為基礎之代理的廣泛調查，涵蓋代理設計中的反思與記憶。
