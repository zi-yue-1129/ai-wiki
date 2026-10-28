---
translation_reviewed: 2026-10-28
---

# 過程獎勵模型

過程獎勵模型（PRM）為解答的每個中間步驟評分，而不只評估最終答案。它以步驟層級的回饋訓練，用來為候選解答排序，或引導對它們的搜尋。此方法屬於[推理模型](index.md)頁所列的以驗證器為基礎的研究路線，也是[測試時運算擴展](test-time-scaling.md)中測試時方法所使用的驗證器。

## 概述

多步驟問題的解答，可能經由有缺陷的步驟得到正確答案，也可能因單一錯誤而得到錯誤答案。只看最終答案的獎勵無法區分這些情況。PRM 為每個步驟評分，因此能找出有缺陷的步驟，並且能同時依推理過程與結果來評判候選解答。

## 關鍵概念

- **結果監督（outcome supervision）**：只根據最終答案進行訓練或評分。
- **過程監督（process supervision）**：根據每個中間步驟的正確性進行訓練或評分。
- **過程獎勵模型（PRM）**：為解答的每個步驟輸出分數的模型。
- **驗證器（verifier）**：為候選解答評分的模型，PRM 是其中一種。

## 問題

語言模型會在多步驟解答的中間犯錯，而只檢查最終答案無法找出這些錯誤。問題在於：步驟層級的回饋，是否比結果回饋更能為訓練驗證器提供好的訊號，而推論時又該如何使用這個驗證器。

## 核心想法

以每個步驟的正確性訓練獎勵模型，然後用它逐步為候選解答評分。Lightman 等人（2023）在 MATH 資料集上比較步驟層級與結果層級的回饋。Snell 等人（2024）在測試時使用 PRM，而他們的 PRM 是在沒有人工步驟標籤的情況下訓練的。

## 運作方式

1. 針對一個問題，從語言模型取樣一或多個候選解答。
2. 以 PRM 為每個候選解答的每個步驟評分。
3. 利用步驟分數挑選解答，例如為完整解答排序，或引導對部分解答的搜尋。

把步驟分數彙總為整個解答的分數，各篇論文的做法不同。此處參考的摘要並未指定單一規則，因此重用前應查閱完整論文。

## 演算法

- **訓練**：收集步驟層級的正確性標籤（來自人工標註，或來自估計的 rollout），並以此擬合獎勵模型。
- **推論**：逐步為候選解答評分並挑選，如上述運作方式所述。

## 核心方法

- **結果獎勵模型**：只為最終答案評分，是 Lightman 等人（2023）的基線。
- **人工標註的 PRM**：以人工撰寫的步驟標籤訓練。Lightman 等人（2023）以 PRM800K 資料建立了這類模型。
- **rollout 標註的 PRM**：以 Monte Carlo rollout 估計的逐步正確性訓練，即 Snell 等人（2024）所用的方法。

## 結果

- Lightman 等人（2023）報告，過程監督在 MATH 資料集上明顯優於結果監督。根據摘要，其過程監督模型能解出 MATH 測試集一個具代表性子集中的 78% 問題。
- Snell 等人（2024）以 Monte Carlo rollout 所得的逐步正確性估計訓練 PRM，而非人工步驟標籤。他們報告，人工標註的 PRM800K 資料對他們而言效果不大。

## 限制

- 步驟標籤成本高。人工標籤的訊號很強，但大規模收集的成本高昂。
- 以 rollout 為基礎的標籤避免了人工標註，但它依賴基礎模型本身的成功率，並需要額外的取樣成本。
- 在一個領域訓練的 PRM 未必能推廣到其他領域。[測試時運算](test-time-scaling.md)頁的開放問題討論了這一點。
- 這些論文的增益是以數學基準量測的，摘要也未主張它們可以推廣到其他任務。

## 變體與更多變體

- **結果獎勵模型**：較簡單的基線，只為最終答案評分。
- **自洽性**：不需驗證器的替代做法，改為對取樣的答案投票，見[自洽性](self-consistency.md)。
- **驗證器引導的搜尋**：以 PRM 引導對部分解答的搜尋，如[測試時運算擴展](test-time-scaling.md)中的測試時方法。

## 關聯

- [測試時運算擴展](test-time-scaling.md)使用 PRM 進行驗證器引導的搜尋。
- [自洽性](self-consistency.md)是最簡單的不需驗證器的替代做法。
- [強化學習](../../paradigms/reinforcement-learning/index.md)提供更廣泛的框架，獎勵模型在其中用來訓練策略。

## 應用

- 推論時為數學問題的候選解答排序。
- 找出解答中第一個錯誤的步驟，用於錯誤分析或教學。

## 開放問題

- 應如何把步驟分數彙總為整個解答的分數？
- 以 rollout 為基礎的標籤，能否在大規模下與人工標籤相比，並適用於數學以外的領域？

## 參考文獻

### 開創性論文

- Lightman, H., et al.（2023）。*Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — 在 MATH 上比較過程監督與結果監督，並報告過程監督模型能解出 MATH 測試問題具代表性子集中的 78%。
- Snell, C., Lee, J., Xu, K. & Kumar, A.（2024）。*Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — 在測試時使用以 Monte Carlo rollout 估計訓練的 PRM 進行驗證器引導的搜尋。
- Wang, X., et al.（2023）。*Self-Consistency Improves Chain of Thought Reasoning in Language Models*. ICLR. https://arxiv.org/abs/2203.11171 — 不需驗證器的替代做法，對取樣的推理路徑投票。
- DeepSeek-AI（2025）。*DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. Nature, 645, 633–638. https://doi.org/10.1038/s41586-025-09422-z — 使用規則式獎勵而非學習得來的 PRM，與本頁的步驟層級做法形成對照。

### 綜述與教科書

- Huang, J. & Chang, K. C.-C.（2023）。*Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — 綜述以驗證與搜尋為基礎的推理方法。
