---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
---

# Mean Teacher：平均教師

Mean Teacher 訓練一個學生網路去匹配教師網路的預測，其中教師的權重是學生權重的指數移動平均（EMA）。學生在有標籤資料上以一般損失訓練，並在所有資料上以對教師的一致性損失訓練。平均的是權重而非預測，因此得到的目標變化平滑，比學生單獨的預測更準確。家族層級的全貌見[一致性正則化](index.md)頁。

## 概述

Tarvainen 與 Valpola（2017）在 NeurIPS 2017 發表 Mean Teacher。它建立在 Temporal Ensembling 之上，後者的目標是較早 epoch 預測的平均值。Mean Teacher 改為平均權重，並在每個訓練步驟之後更新教師。摘要報告了多項結果。在 SVHN 使用 250 個標籤時，錯誤率為 4.35%。在 CIFAR-10 使用 4000 個標籤時，ResNet 將先前最佳的結果從 10.55% 錯誤率改進為 6.28%。在 ImageNet 使用 10% 的標籤時，錯誤率從 35.24% 降至 9.11%。

## 核心概念

- **學生**：正在訓練的模型，權重為 \(\theta\)。
- **教師**：另一個網路，其權重 \(\theta'\) 是學生權重的指數移動平均。
- **平滑係數** \(\alpha\)：接近 1。論文在 CIFAR-10 與 SVHN 上的 ConvNet 使用 0.999；CIFAR-10 上 ResNet 使用的值，在 1000 與 4000 個標籤時分別為 0.97 與 0.99；ImageNet 上 ResNet 使用 0.9997。
- **一致性代價**：在不同雜訊與增強下，學生與教師 softmax 輸出之間的平方距離。教師視為常數，因此梯度不會流入教師。
- **升溫（ramp-up）**：一致性項的權重在訓練初期從零逐步增加。

## 運作方式

每個訓練步驟之後，教師的權重依學生的權重更新：

\[
\theta'_t = \alpha\,\theta'_{t-1} + (1-\alpha)\,\theta_t
\]

一致性代價是在輸入與兩次獨立雜訊抽樣上的期望平方距離，學生使用雜訊 \(\eta\)，教師使用雜訊 \(\eta'\)：

\[
J_{\text{cons}}(\theta) = \mathbb E_{x,\eta,\eta'}\Big[\big\|f(x;\theta,\eta) - f(x;\theta',\eta')\big\|^2\Big]
\]

論文在多數實驗中使用 softmax 輸出上的均方誤差作為一致性代價。總代價是有標籤資料上的分類代價，加上所有資料上的一致性代價，兩者的加權和。論文沒有給出單一的公式。一致性權重在訓練初期逐步升溫。對於 ConvNet，附錄 B.1 給出以 S 形曲線在 40,000 步內升溫的方式。第 3 節則寫「前 80 個 epoch」，與附錄矛盾，因此本頁採用附錄的數值。

每一步中，學生與教師以不同雜訊對同一批資料計算輸出，計算損失，只對學生做一次梯度步驟，然後以 EMA 更新教師。

## 關鍵方法

### Mean teachers are better role models（Tarvainen 與 Valpola，2017）

- **問題：** Temporal Ensembling 的目標是較早 epoch 預測的平均，因此會落後於目前的模型。論文探討平均權重能否得到更好的目標。
- **核心想法：** 使用由學生權重 EMA 構成的教師，並訓練學生在不同雜訊下匹配教師的預測。EMA 能在許多步驟上平滑目標，而不需要為每個範例保存記憶。
- **公式或演算法：** 如上所述的 EMA 更新、一致性代價與加權總代價。
- **結果：**
  - SVHN，10 次實驗的錯誤率（表 1）：250 個標籤為 4.35 ± 0.50%，500 個為 4.18 ± 0.27%，1000 個為 3.95 ± 0.19%，全部標籤為 2.50 ± 0.05%。
  - CIFAR-10，ConvNet，10 次實驗的錯誤率（表 2）：1000 個標籤為 21.55 ± 1.48%，2000 個為 15.73 ± 0.31%，4000 個為 12.31 ± 0.28%，全部標籤為 5.94 ± 0.15%。
  - CIFAR-10 使用 4000 個標籤，ResNet（表 4）：6.28 ± 0.15%，先前最佳的 VAT 為 10.55%。
  - ImageNet 使用 10% 的標籤，ResNet，在驗證集上（表 4）：9.11 ± 0.12%。
  - 使用全部標籤時，Mean Teacher 與 Π 模型幾乎相同，因此其進步主要出現在標籤較少的情境。
- **限制：** 論文指出，在某些設定中 VAT 的表現優於 Mean Teacher，例如 1000 個標籤的 SVHN 與 4000 個標籤的 CIFAR-10。把 Mean Teacher 與 VAT 結合「超出本文範圍」。\(\alpha\) 與一致性權重的良好取值範圍大約跨越一個數量級，超出此範圍時效能會「快速下降」。ImageNet 的結果使用驗證集，因為測試集並未公開。作者表示，均方誤差為何優於 KL 散度，「仍不清楚」。

## 關聯

- 前身方法 Temporal Ensembling 屬於[一致性正則化](index.md)家族。
- [FixMatch](fixmatch.md) 以弱增強與強增強所得的經門檻篩選偽標籤，取代教師網路。
- Mean Teacher 的教師輸出可視為軟偽標籤，因此它也是一種自訓練方法。見[偽標籤與自訓練](../pseudo-labelling-and-self-training/index.md)。
- 更廣泛的半監督學習全貌見[半監督學習](../index.md)頁。
- 增強與雜訊的選擇對這些方法至關重要。見[電腦視覺](../../../models/computer-vision/index.md)。

## 開放問題

- 為何均方誤差作為一致性代價時，會優於 KL 散度？論文沒有解答。
- 對於新的資料集或模型規模，應如何設定 \(\alpha\)？良好範圍雖然寬，但仍然有限。
- 若加入 VAT 那樣的對抗擾動，能否改善 Mean Teacher？論文認為這超出本文範圍。

## 參考文獻

### 開創性論文

- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. NeurIPS 2017. https://arxiv.org/abs/1703.01780 — 提出 Mean Teacher，教師由學生權重的 EMA 構成。
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — 前身方法，以較早 epoch 的平均預測作為目標。
- Sohn, K. 等人 (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. NeurIPS 2020. https://arxiv.org/abs/2001.07685 — 以弱增強得到的高信心偽標籤作為強增強的目標。
- Berthelot, D. 等人 (2019). MixMatch: A Holistic Approach to Semi-Supervised Learning. arXiv:1905.02249. https://arxiv.org/abs/1905.02249 — 把一致性、銳化與 MixUp 結合成單一半監督目標。

### 綜述與教科書

- Oliver, A. 等人 (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — 顯示當基準方法經過公平調校後，許多已報告的進步會縮小。
