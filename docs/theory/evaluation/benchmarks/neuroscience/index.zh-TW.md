---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - brain-mind/visual-perception
tags:
  - evaluation
  - benchmarks
  - neuroscience
aliases:
  - Neuroscience benchmarks
  - 神經科學基準
---

# 神經科學基準

神經科學基準測試模型的內部反應與實測的神經或行為資料有多接近。它們問的問題與準確率不同：模型可以把影像分類得很好，卻仍以與大腦不同的方式表徵它們。

## 概述

這些基準背後的想法早於目前這一代模型。Yamins et al.（2014）顯示，為物件辨識最佳化的階層式模型能預測高階視覺皮質的反應，使網路與神經記錄的比較成為一個實際的問題。Brain-Score 把這種比較變成一個共享基準：模型的內部層被對應到記錄下來的神經位點，其輸出前的最後一層則與人類對物件影像的行為資料比較，並依其對保留資料的預測能力排名（Schrimpf et al., 2018）。同樣的比較之後也用於人類語言處理，論文中把語言模型與人類對句子的神經反應相連（Schrimpf et al., 2021）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [Brain-Score](brain-score.md) | 預測物件影像上的神經與行為反應 | 對保留的神經與行為資料的預測力 |

Brain-Score 是此家族的主要基準，其頁面詳述資料集與計分方式。高分表示在所用的對應方式下，模型的表徵與記錄資料相似。它並不表示模型的運算方式與大腦相同。

## 關鍵概念

- **神經位點**：被記錄的位置，例如某個皮質區域中的神經元群，模型必須預測其反應。
- **預測力**：模型反應對應到記錄位點後，解釋保留資料的能力，在 Brain-Score 中，以在訓練影像上擬合、並於保留影像上測試的偏最小平方迴歸（partial least squares）測量。
- **表徵相似度**：不比對個別單元，而是比較兩個系統對同一刺激的反應之相似結構（Kriegeskorte, 2008）。

## 運作方式

模型以向動物或人展示的同一批影像執行。其選定層的活化會被對應到記錄資料。在 Brain-Score 中，此對應是以 25 個成分的偏最小平方迴歸，在訓練影像上擬合、在保留影像上測試，並重複多次訓練與測試切分。行為分數則使用輸出前的最後一層。分數是保留部分的預測力，並分別報告各區域與行為資料。由於對應是經過擬合的，迴歸方法與所選的層必須與數字一併報告。

## 常見問題

- **對應方式的選擇。** 分數取決於模型單元如何對應到神經位點，因此迴歸方法與層都必須報告。
- **記錄數量有限。** 位點與影像少，會造成很寬的不確定性，因此模型之間的小差異並不可靠。
- **相似不等於機制。** 高分表示模型與大腦的表徵在該測試上相似，並不表示模型與大腦的運作方式相同。
- **刺激範圍窄。** 物件影像與短句只是大腦工作的一小部分，以它們建立的基準對其他功能的說明有限。

## 相關連結

- [視覺感知](../../../../brain-mind/visual-perception/index.md) 說明大腦如何辨識物件，這是視覺模型比較所要對齊的目標。[Yamins et al.（2014）頁面](../../../../brain-mind/visual-perception/yamins-2014/index.md) 涵蓋啟動這條研究路線的論文。
- [感受野](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md) 解釋這些模型所比較的階層式皮質組織。
- [視覺](../vision/index.md) 涵蓋模型所訓練的影像基準。

## 開放問題

- 在多個神經資料集上得高分的模型，究竟學到了與大腦相同的運算，還是只是從刺激到反應有相似的對應。
- 如何把比較從視覺與語言擴展到決策、記憶與運動控制，這些領域的記錄較難取得。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [協定](../../protocols/index.md) 涵蓋切分與報告方式。

## 參考文獻

### 開創性論文

- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識最佳化的模型能預測高階視覺皮質的反應。
- Kriegeskorte, N. (2008). *Representational similarity analysis – connecting the branches of systems neuroscience*. Frontiers in Systems Neuroscience. https://doi.org/10.3389/neuro.06.004.2008 — 介紹以反應的相似結構比較兩個系統。
- Kell, A. J. E. et al. (2018). *A Task-Optimized Neural Network Replicates Human Auditory Behavior, Predicts Brain Responses, and Reveals a Cortical Processing Hierarchy*. Neuron. https://doi.org/10.1016/j.neuron.2018.03.044 — 將同樣的任務最佳化比較應用於聽覺皮質與人類行為。

### 文章與文件

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — 介紹此基準及其神經與行為分數。
- Schrimpf, M. et al. (2021). *The neural architecture of language: Integrative modeling converges on predictive processing*. PNAS. https://doi.org/10.1073/pnas.2105646118 — 將同一框架擴展到語言處理區域。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 檢視基準的建構效度，以及廣泛宣稱的限制。
