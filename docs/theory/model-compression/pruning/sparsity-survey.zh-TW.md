---
related:
  - theory/model-compression/pruning
  - engineering/hardware/co-design
tags:
  - model compression
  - sparsity
  - pruning
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - Sparsity in Deep Learning
  - Hoefler sparsity survey
  - 深度學習中的稀疏性
---

# 深度學習中的稀疏性（Hoefler et al., 2021）

Hoefler、Alistarh 與 Ben-Nun（2021）綜述了讓神經網路稀疏化的方法，也就是把許多權重或活化值設為零。這份綜述同時是綜述與教學：它同時處理推論與訓練的稀疏化，並探討稀疏網路在真實硬體上何時值得付出額外成本（Hoefler et al., 2021）。

## 概觀

綜述從深度學習的成本出發。大型網路需要能源、記憶體與訓練時間，而稀疏性是同時降低這三者的方法之一。摘要指出，稀疏網路的泛化能力可以和原本的稠密網路一樣好，甚至更好，而且稀疏化能把模型縮小到足以放進行動裝置（Hoefler et al., 2021）。

這份綜述並不主張每個稀疏網路都很便宜。它的核心主題是參數數量的減少與執行時間的減少之間的落差，而大部分討論都在處理如何縮小這個落差。

## 關鍵概念

- **非結構化稀疏性**：任何單一權重都可能為零。它在選擇要移除哪些權重時最有彈性，但每個保留下來的值都需要一個索引。
- **結構化稀疏性**：移除整個濾波器、通道、注意力頭或區塊。綜述指出它的儲存負擔最低、效能最高，但可能導致較差的模型（Hoefler et al., 2021，第 3.1 節）。
- **索引的負擔**：隨機移除元素後，必須儲存保留非零值的位置（第 2.2 節）。因此，任意的稀疏模式在為稠密運算設計的硬體上，執行效率低於稠密計算（第 2.3 節）。
- **Occam 山丘**：稀疏化移除學習到的雜訊時，準確率先上升，之後下降。在高稀疏度下，網路品質會迅速惡化（第 2.1 節）。

## 運作方式

綜述把稀疏化分為三個階段：決定移除什麼、改變網路結構，以及恢復準確率。它涵蓋以大小為依據的移除、訓練過程中加入連接的方法，以及在訓練開始前就決定稀疏模式的方法（Hoefler et al., 2021）。

綜述指出，它的討論同時適用於推論與訓練（第 2 節）。對訓練而言，有趣的問題是稀疏網路能否從頭訓練。綜述引用的 Liu et al. 認為，若仔細選擇架構與超參數，這是可行的。他們也報告，非結構化剪枝後從頭訓練的方法在大型 ImageNet 模型上會失敗，而微調仍然有幫助（第 2.4.3 節）。

初始化時剪枝是另一類方法。SNIP 以連接敏感度，在訓練前以資料驅動的方式找出要移除的連接（Lee et al., 2018）。綜述指出，隨機初始化對這些方法而言是很強的基線（第 2.4.3 節）。

## 關鍵方法

以下簡要比較各類方法，細節請見各方法頁面：

- [學習權重與連接](learning-weights-and-connections/index.md)：剪枝後再重新訓練，是經典的迭代剪枝方法（Han et al., 2015）。
- [量值剪枝](magnitude-pruning/index.md)：移除最小的權重，可以漸進進行，也可以一次完成。
- [彩票假設](lottery-ticket/index.md)：一個能從原始初始化良好訓練的稀疏子網路。
- [結構化剪枝](structured-pruning/index.md)：移除整個通道或濾波器，可在稠密硬體上執行。

## 證據與結果

綜述報告，在某些設定下，現有方法可以把模型大小縮小約 10 到 100 倍，且沒有明顯的準確率損失（第 1.1 節）。綜述引用的 dense-sparse-dense 訓練，報告的泛化表現明顯高於稠密基線（第 2.4.2 節；Han et al., 2016）。

成效高度依賴目標。除非稀疏模式與硬體相符，否則參數減少不會轉換成等比例的加速，這也是綜述如此謹慎地區分非結構化與結構化方法的原因。

## 限制

- **硬體落差。** 非結構化稀疏性能節省儲存，但通常無法節省時間，除非核心或硬體支援該模式。
- **極端稀疏。** 綜述指出，目前尚不清楚深度模型能否達到極高的稀疏度，也不清楚在那些稀疏程度下準確率的取捨是否仍然成立（第 2.2 與 2.4.3 節）。
- **調參。** 在訓練中改變結構的方法會增加超參數，綜述指出很少有研究說明如何調整它們（第 2.4.6 節）。

## 相關連結

- [硬體協同設計](../../../engineering/hardware/co-design/index.md) 涵蓋落差的另一側：硬體需要什麼，才能有效率地執行稀疏網路。
- [量化綜述](../quantisation/quantisation-survey.md) 涵蓋另一條常見的壓縮路線，它降低每個值的精度，而不是移除值。

## 應用

稀疏網路用於記憶體與能源是主要限制的場合，例如行動裝置，也用於以較少運算訓練非常大的網路（Hoefler et al., 2021）。

## 未解問題

- 稀疏性是否能改善可解釋性，綜述未有定論（第 1 節）。
- 如何在通用硬體上，從非結構化稀疏性獲得真正的加速。

## 參考文獻

### 開創性論文

- Hoefler, T., Alistarh, D. & Ben-Nun, T. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv. https://arxiv.org/abs/2102.00554 — 關於推論與訓練稀疏化的綜述與教學，本頁討論的硬體取捨即出自此文。
- Han, S., Pool, J., Tran, J. & Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv. https://arxiv.org/abs/1506.02626 — 剪枝後重新訓練，是經典的迭代剪枝方法。
- Han, S. et al. (2016). *DSD: Dense-Sparse-Dense Training for Deep Neural Networks*. arXiv. https://arxiv.org/abs/1607.04381 — Dense-sparse-dense 訓練，綜述引用它來說明泛化的改善。
- Lee, N., Ajanthan, T. & Torr, P. H. S. (2018). *SNIP: Single-shot Network Pruning based on Connection Sensitivity*. arXiv. https://arxiv.org/abs/1810.02340 — 以連接敏感度在訓練前進行剪枝。

### 綜述與基準

- Gale, T., Elsen, E. & Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv. https://arxiv.org/abs/1902.09574 — 比較多種稀疏化方法，作為當時領域現況的參考。
- Frankle, J. & Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv. https://arxiv.org/abs/1803.03635 — 綜述在討論剪枝與權重重設時引用的稀疏子網路假說。
