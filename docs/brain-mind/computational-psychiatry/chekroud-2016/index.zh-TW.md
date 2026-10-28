---
translation_reviewed: 2026-10-28
---

# Chekroud et al. 2016（跨試驗的治療結果預測）

Chekroud et al.（2016）以憂鬱症患者的基線資料訓練機器學習模型，並測試它能否在另一個獨立試驗中預測治療結果。它是一種預測方法，而非機制的解釋。本頁是[計算精神醫學](../index.md)的子頁。上層頁面提供概述，本頁說明方法、其步驟以及證據的限制。

## 概述

選擇抗憂鬱藥往往是一個反覆試錯的過程，許多病人對第一次嘗試的治療並無反應。若一個模型能預測哪種治療可能奏效，將會很有用，但這樣的模型必須謹慎地加以測試。一個在建立它的資料上預測良好的模型，可能只是學到了該樣本的特殊性。

Chekroud 及其同事採用了更嚴格的測試。模型在一個試驗上訓練，並在另一個試驗上評估，因此它必須能夠轉移到另一組病人與另一個研究情境。這些模型所應用的較廣臨床場景，見於[心理健康](../../../applications/mental-health/index.md)。

## 核心概念

- **基線特徵**：治療開始前記錄的資訊，例如人口學資料、臨床病史與症狀評分。
- **結果**：要預測的結果，此處是病人是否達到緩解的二元測量。
- **分類器**：把基線特徵對應到預測結果的模型。
- **交叉驗證**：在同一資料集中以保留的部分測試模型。它有用，但不能測試轉移到新情境的能力。
- **跨試驗驗證**：在一個試驗上訓練，在另一個試驗上測試。它測試預測能否在不同研究之間延續。
- **準確率**：結果被正確預測的病人比例，$\text{accuracy} = \frac{TP + TN}{N}$，應與隨機基線比較。

## 運作方式

此方法依循四個步驟。

1. 為每位病人收集治療前的基線資料，包括人口學、臨床與症狀測量。
2. 在一個試驗上訓練分類器，由這些基線特徵預測結果。
3. 把訓練好的模型（不重新擬合）套用到另一個試驗的資料上。這一步是跨試驗測試，可能涉及不同的病人、研究地點或治療。
4. 把預測與實際記錄的結果比較，並與隨機基線相比，報告準確率與相關指標。

關鍵在第三步。一個只在建立它的試驗內有效的模型，並不能證明它可以在別處使用。

## 結果

論文測試了跨試驗的預測，其核心主張是預測價值能延續到另一個獨立試驗。本頁不引述準確率數字或樣本數，這些見於論文，應直接查閱論文。論文對臨床應用的看法，讀者也應在論文中查證。

## 限制

- 在這類研究中，僅依基線特徵的預測準確率通常有限，因此個別預測帶有相當大的不確定性。
- 基線臨床特徵常是潛在原因的代理變數。分類器可以預測結果，卻不能解釋病人為何會有反應。
- 不同試驗的族群、測量方式與研究地點各不相同，這些差異限制了模型的轉移能力。
- 預測模型不是治療建議。把它用於決策，需要臨床判斷與評估。

## 開放問題

- 加入 [Gillan et al. 2016](../gillan-2016/index.md) 那類計算測量，能否在臨床特徵之上進一步提高預測能力？
- 在某一醫療體系中訓練的模型，能否轉移到其他醫療體系，以及其他疾病？
- 如何把機率式的預測傳達給病人與臨床醫師，使其支持而非取代決策？

## 參考文獻

### 開創性論文

- Chekroud, A. M. et al. (2016). Cross-trial prediction of treatment outcome in depression: a machine learning approach. *The Lancet Psychiatry*. https://doi.org/10.1016/S2215-0366(15)00471-X — 以基線資料訓練機器學習模型，並測試它能否在另一個試驗中預測憂鬱症的治療結果。

### 綜述與教科書

- Dwyer, D. B., Falkai, P. & Koutsouleris, N. (2018). Machine Learning Approaches for Clinical Psychology and Psychiatry. *Annual Review of Clinical Psychology*. https://doi.org/10.1146/annurev-clinpsy-032816-045037 — 回顧機器學習在診斷、預後與治療上的方法，以及臨床轉化所面對的限制。
- Huys, Q. J. M., Maia, T. V. & Frank, M. J. (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — 回顧計算模型如何把神經科學與精神醫學的臨床實務連結起來。
- Adams, R. A., Huys, Q. J. M. & Roiser, J. P. (2015). Computational Psychiatry: towards a mathematically informed understanding of mental illness. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp-2015-310737 — 回顧形式模型如何有助於理解精神疾病。

### 文章與文件

- Bzdok, D. & Meyer-Lindenberg, A. (2018). Machine Learning for Precision Psychiatry: Opportunities and Challenges. *Biological Psychiatry: Cognitive Neuroscience and Neuroimaging*. https://doi.org/10.1016/j.bpsc.2017.11.007 — 討論機器學習如何支持精準精神醫學，以及它面對的驗證問題。
