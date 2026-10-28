---
translation_reviewed: 2026-10-28
---

# Gillan et al. 2016（目標導向控制與強迫性）

Gillan、Kosinski、Whelan、Phelps 與 Daw（2016）以規劃任務與擬合模型，在大型線上樣本中測量目標導向控制。他們發現，目標導向控制的缺陷與一個強迫行為與侵入性思維的症狀維度關聯最強。本頁是[計算精神醫學](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 概述

強迫症與成癮都涉及明知有代價、卻仍持續進行的重複行為。一種解釋認為，這些問題共享目標導向控制的缺陷，也就是依據行動結果的推理來選擇行動的能力，而缺陷使人依賴習慣。然而，目標導向的缺陷也曾在沒有明顯強迫成分的疾患中被報告。Gillan et al. 認為，這種不吻合可能反映了診斷類別的劃分方式。他們以維度式設計加以檢驗：在一般人群中把症狀測量為連續特質，並將之與任務表現連結。

## 核心概念

- **兩步任務**：一種序列決策任務，第一步的選擇以機率導向兩個第二階段狀態之一，而那些狀態的獎勵會隨時間改變。因為轉移結構是已知的，此任務能區分依模型所引導的選擇與依過去獎勵所引導的選擇。
- **無模型價值**：從過去獎勵中為每個選項學到的價值，以預測誤差更新。見[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)。
- **有模型價值**：利用已知轉移結構進行規劃而算出的價值。
- **混合模型**：以一個權重結合兩種價值的模型。權重本身即是所關心的量。
- **症狀維度**：由問卷分數得出的連續特質，而非診斷類別。

## 運作方式

受試者完成許多次試驗。在每次試驗中，第一階段在兩個選項之間做選擇，接著以機率轉移到第二階段的一個狀態並獲得獎勵。模型為每個第一階段的選項保留兩個價值估計。

無模型價值在每次獲得獎勵後以預測誤差更新，$Q_{\text{MF}}(a) \leftarrow Q_{\text{MF}}(a) + \alpha\,\delta$。有模型價值則沿著已知的轉移向前推演，$Q_{\text{MB}}(a) = \sum_{s} P(s \mid a)\,\max_{b} Q(s, b)$。依 Daw et al.（2011），一種常見的混合形式把兩者結合為 $Q_{\text{net}} = wQ_{\text{MB}} + (1-w)Q_{\text{MF}}$，而選擇遵循 softmax 規則 $P(a) \propto \exp(\beta Q_{\text{net}}(a))$。把此模型擬合到每位受試者的選擇上，即可估計 $\alpha$、$\beta$ 與有模型權重 $w$。$w$ 越低，表示選擇越少依賴規劃。

Gillan et al. 在大型線上樣本中收集這些任務，並把估計出的參數與問卷式的症狀分數連結，而不是與臨床診斷連結。

## 結果

論文報告了兩個彼此獨立的一般人群樣本。依摘要，其主要結果是：目標導向控制的缺陷與一個結合強迫行為與侵入性思維的症狀維度最為相關。作者報告，相較於其他非強迫性的精神病理面向，這種關聯具有特異性。本頁未引述效應量；效應量見於論文，應直接查閱論文。

## 限制

- 樣本是透過線上招募的一般人群，因此結果涉及的是症狀維度，而非臨床診斷。
- 此模型只是該任務的幾種可能模型之一。參數之間可能相互抵消，因此估計值依賴於模型大致正確。
- 研究依據的是行為與問卷，依摘要，並不能確立神經機制。
- 症狀維度與模型參數之間的關聯，並不證明缺陷會導致症狀。

## 開放問題

- 目標導向缺陷是否為能預測誰會發展強迫症狀的穩定特質，還是會隨壓力或治療而改變的狀態？
- 同樣的缺陷是否也出現在臨床族群中？摘要指出，它伴隨數種疾患而出現。Maia 與 Frank（2011）回顧了這類模型在精神與神經疾患上的應用。
- 此參數能否在單一個人身上被可靠地估計？這需要重測研究。

## 參考文獻

### 開創性論文

- Gillan, C. M., Kosinski, M., Whelan, R., Phelps, E. A. & Daw, N. D. (2016). Characterizing a psychiatric symptom dimension related to deficits in goal-directed control. *eLife*. https://doi.org/10.7554/eLife.11305 — 報告兩個一般人群樣本，其中目標導向控制的缺陷與一個強迫行為與侵入性思維的維度相關。
- Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P. & Dolan, R. J. (2011). Model-Based Influences on Humans' Choices and Striatal Prediction Errors. *Neuron*. https://doi.org/10.1016/j.neuron.2011.02.027 — 顯示人類的選擇帶有有模型的影響，並把紋狀體的預測誤差與同一任務中的學習訊號連結起來。

### 綜述與教科書

- Maia, T. V. & Frank, M. J. (2011). From reinforcement learning models to psychiatric and neurological disorders. *Nature Neuroscience*. https://doi.org/10.1038/nn.2723 — 早期回顧，說明強化學習模型如何描述精神與神經疾患的症狀。
- Huys, Q. J. M., Maia, T. V. & Frank, M. J. (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — 回顧計算模型如何把神經科學與精神醫學的臨床實務連結起來。
- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P. (2012). Computational psychiatry. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2011.11.018 — 回顧文獻，把計算精神醫學界定為以學習與決策模型理解精神疾病的研究取向。

### 文章與文件

- Insel, T. et al. (2010). Research Domain Criteria (RDoC): Toward a New Classification Framework for Research on Mental Disorders. *American Journal of Psychiatry*. https://doi.org/10.1176/appi.ajp.2010.09091379 — 提出一個研究框架，依功能維度而非固定的診斷類別來組織精神疾病，是本研究這類維度式研究的架構基礎。
