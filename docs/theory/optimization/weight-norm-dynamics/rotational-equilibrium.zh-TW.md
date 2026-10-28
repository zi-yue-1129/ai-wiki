---
translation_reviewed: 2026-10-28
tags:
  - optimization
  - weight decay
  - normalisation
aliases:
  - Rotational equilibrium
  - 旋轉平衡
---

# 旋轉平衡

Kosson、Messmer 與 Jaggi（2023）研究權重衰減如何影響個別神經元的更新行為。他們的主要主張是：在 AdamW 下，每個神經元的權重會達到一個平衡，此時衰減與梯度更新互相抵消。平衡的達成時間尺度由學習率與衰減的乘積決定，而梯度統計不同的神經元會停在不同的旋轉速率。上層子主題是[權重範數動態](index.md)。

## 概述

尺度不變的神經元是指：權重乘上常數時，輸出不會改變。這種神經元的梯度與其權重向量正交，因此每次更新都會旋轉權重並增加範數，而衰減則把範數拉回。論文追蹤的正是每一步權重的旋轉量。

## 問題

當權重衰減很小時，訓練曲線上的權重範數常會持續增長，有效學習率也隨之縮小。實務上衰減值多半依慣例設定，而不清楚某個數值在訓練預算內是否小到幾乎沒有作用。論文問的是：權重衰減如何決定每個神經元的範數與旋轉，而系統要花多久才能到達那個狀態。

## 核心想法

論文在 AdamW、學習率 \(\eta\) 與衰減 \(\lambda\) 下追蹤每個神經元的權重 \(\omega\)。它給出的平衡範數約為 \(\sqrt{\eta C / 2\lambda}\)（\(C\) 為該神經元的權重數），以及每步期望旋轉約為 \(\sqrt{2\eta\lambda(1-\beta_1)/(1+\beta_1)}\)。範數以 \((1-\eta\lambda)^t\) 的速率接近平衡，因此時間尺度約為 \(1/(\eta\lambda)\) 步。

依此說法，衰減太小時，時間尺度會遠長於訓練長度。權重因此永遠到不了平衡，範數持續增長。衰減較大則縮短時間尺度，使旋轉在訓練中達到穩定值。

## 運作方式

1. 選定學習率 \(\eta\) 與衰減 \(\lambda\)，以步數計算時間尺度 \(1/(\eta\lambda)\)。
2. 與訓練步數比較。若時間尺度遠大於訓練步數，衰減在本次訓練中幾乎沒有作用。
3. 監測每個神經元的範數與旋轉，而不只是整層。梯度徑向分量不平衡的神經元會以不同速率旋轉。
4. 平衡旋轉速率，例如使用論文提到能消除神經元間不平衡的權重標準化（Weight Standardisation）。

## 結果

論文同時提供理論與殘差網路、GPT 類模型的實驗。它在固定數值下掃描乘積 \(\eta\lambda\)，並檢查旋轉是否符合預測的平衡。論文也指出，相較於帶 L2 懲罰的 Adam，AdamW 能使神經元間的旋轉更平衡，因為 L2 會把衰減與梯度大小耦合。確切數字應在論文的表格中核對後再使用。

## 限制

- 平衡結果是針對尺度不變的神經元推導的。沒有接正規化的層（例如分類頭）不在推導範圍內，其行為需要另外的證據。
- 旋轉量的估計依賴推導中的近似。論文以實驗檢驗，但常數對每種架構不一定精確。
- 時間尺度規則以步數表示。只有在每個 epoch 的步數固定時，它才會變成以 epoch 計的規則，這一點在 [AdamW 權重衰減縮放](adamw-weight-decay-scaling.md) 中有進一步說明。

## 相關主題

- [權重範數動態](index.md) 把此結果放在其他範數增長的解釋之中。
- [AdamW](../adaptive/adamw.md) 是推導平衡所針對的最佳化器。
- [正則化與權重衰減](../regularisation-and-weight-decay.md) 提供衰減的一般觀點。
- 範數增長在注意力 logit 上的一面，見 [QK 正規化](../../models/transformer/qk-norm.md) 頁面。

## 開放問題

- 平衡的圖像是否適用於非尺度不變的層，也就是衰減直接作用於輸出尺度的情況。
- 神經元間的旋轉不平衡，與超大模型中自適應最佳化器的逐參數縮放如何互動。

## 參考文獻

- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — 平衡範數、旋轉與時間尺度結果的來源。
- Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — 提出分析所用的解耦權重衰減。
- Wan, R., Zhu, Z., Zhang, X., & Sun, J. (2020). *Spherical Motion Dynamics: Learning Dynamics of Neural Network with Normalization, Weight Decay, and SGD*. arXiv:2006.08419. https://arxiv.org/abs/2006.08419 — 較早分析 SGD 加衰減時的範數動態。
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. ICLR 2020. https://arxiv.org/abs/1910.07454 — 說明衰減與正規化共同作用時，像是一個增長的學習率。
- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — 以相同的時間尺度觀點，為不同規模選擇衰減。
