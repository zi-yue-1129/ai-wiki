---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
---

# Mean Teacher：平均教師

Mean Teacher 訓練一個學生網路去匹配教師網路的預測，其中教師的權重是學生權重的指數移動平均（EMA）。學生在有標籤資料上以一般損失訓練，並在所有資料上以對教師的一致性損失訓練。平均的是權重而非預測，因此得到的目標變化平滑，而且比學生本身更準確。家族層級的概觀見[一致性正則化](index.md)頁面。

## 概述

Tarvainen 與 Valpola（2017）提出 Mean Teacher。它建立在 Temporal Ensembling 之上，後者的目標是較早 epoch 之預測的平均。Mean Teacher 改為平均權重，並在每個訓練步驟之後更新教師。摘要報告了幾項結果。在 SVHN 使用 250 個標籤時，錯誤率為 4.35%。在 CIFAR-10 使用 4000 個標籤時，ResNet 把最先進水準的錯誤率從 10.55% 改進到 6.28%。在 ImageNet 使用 10% 的標籤時，錯誤率從 35.24% 降到 9.11%。

## 核心概念

- **學生**：正在訓練的模型，權重為 \(\theta\)。
- **教師**：另一個網路，其權重 \(\theta'\) 是學生權重的指數移動平均。
- **平滑係數** \(\alpha\)：接近 1。論文對 SVHN 上的 ConvNet 使用 0.99，對 CIFAR-10 上的 ConvNet 使用 0.999；CIFAR-10 上 ResNet 使用 1000 與 4000 個標籤時分別為 0.97 與 0.99；ImageNet 上的 ResNet 使用 0.9997。
- **一致性代價**：學生與教師在不同雜訊與增強下的 softmax 輸出之間的距離。教師視為常數，因此梯度不流入教師。
- **升溫**：一致性項的權重在訓練初期從零逐步上升。

## 運作方式

每個訓練步驟之後，教師的權重依學生的權重更新：

\[
\theta'_t = \alpha\,\theta'_{t-1} + (1-\alpha)\,\theta_t
\]

一致性代價是學生與教師輸出之間的期望平方距離，取自輸入以及兩組獨立的雜訊抽樣，學生為 \(\eta\)，教師為 \(\eta'\)：

\[
J_{\text{cons}}(\theta) = \mathbb E_{x,\eta,\eta'}\Big[\big\|f(x;\theta,\eta) - f(x;\theta',\eta')\big\|^2\Big]
\]

論文在大多數實驗中以 softmax 輸出的均方誤差作為一致性代價。ImageNet 則使用 KL 散度。總代價是有標籤樣本的分類代價與所有樣本之一致性代價的加權和。論文沒有給出單一的方程式。一致性權重在訓練初期逐步上升。對於 ConvNet，附錄 B.1 給出在 40,000 步內的 S 形升溫。第 3 節寫的是「前 80 個 epoch」，與附錄不一致，因此本頁採用附錄的值。

每個步驟在同一批次上以不同雜訊計算學生與教師的輸出，計算損失，只對學生做一次梯度更新，然後以 EMA 更新教師。

## 關鍵方法

### Mean teachers are better role models（Tarvainen 與 Valpola，2017）

- **問題：**Temporal Ensembling 的目標是較早 epoch 之預測的平均，因此落後於目前的模型。論文探討平均權重是否能給出更好的目標。
- **核心想法：**使用由學生權重 EMA 建立的教師，並訓練學生在不同雜訊下匹配教師的預測。EMA 能跨越許多步驟平滑目標，而不需要逐樣本的記憶。
- **方程式或演算法：**如上所述的 EMA 更新、一致性代價，以及加權的總代價。
- **結果：**
  - SVHN，10 次執行的錯誤率（表 1）：250 個標籤為 4.35 ± 0.50%，500 個為 4.18 ± 0.27%，1000 個為 3.95 ± 0.19%，全部標籤為 2.50 ± 0.05%。
  - CIFAR-10，ConvNet，10 次執行的錯誤率（表 2）：1000 個標籤為 21.55 ± 1.48%，2000 個為 15.73 ± 0.31%，4000 個為 12.31 ± 0.28%，全部標籤為 5.94 ± 0.15%。
  - CIFAR-10 使用 4000 個標籤、ResNet（表 4）：6.28 ± 0.15%，先前最佳為 VAT+EntMin 的 10.55%。
  - ImageNet 使用 10% 的標籤、ResNet，在驗證集上：9.11% 錯誤率，為兩次執行的平均。
  - 使用全部標籤時，Mean Teacher 與 Π 模型幾乎相同，因此增益主要出現在少標籤的情況。
- **限制：**論文指出，在某些設定下 VAT 優於 Mean Teacher。以 ConvNet 為例，在 SVHN 使用 1000 個標籤時，VAT 為 3.86%，Mean Teacher 為 3.95%；在 CIFAR-10 使用 4000 個標籤時，VAT 為 10.55%，Mean Teacher 為 12.31%。把 Mean Teacher 與 VAT 結合，則「超出本論文的範圍」。\(\alpha\) 與一致性權重的良好取值約跨越一個數量級，超出該範圍時效能「迅速下降」。ImageNet 結果使用驗證集，因為測試集不公開。作者表示，MSE 優於 KL 散度的原因「仍不清楚」。

## 關聯

- 前身方法 Temporal Ensembling 是[一致性正則化](index.md)家族的一部分。
- [FixMatch](fixmatch.md) 以來自弱與強增強之有門檻的偽標籤取代教師。
- Mean Teacher 的教師輸出可作為軟偽標籤，因此它也是一種自訓練方法。見[偽標籤與自訓練](../pseudo-labelling-and-self-training/index.md)。
- 虛擬對抗訓練（VAT）是 Mean Teacher 所比較的對抗擾動方法，也是相關的一致性方法。
- 更廣泛的半監督學習概觀見[半監督學習](../index.md)頁面。
- 增強與雜訊的選擇對這些方法至關重要。見[電腦視覺](../../../models/computer-vision/index.md)。

## 開放問題

- 為什麼 MSE 作為一致性代價比 KL 散度更好？論文沒有解答。
- 面對新的資料集或模型大小，應如何設定 \(\alpha\)？良好範圍雖寬，但仍然有限。
- 像 VAT 那樣加入對抗擾動，能否改善 Mean Teacher？論文認為這超出其範圍。

## 參考文獻

### 代表性論文

- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. arXiv:1703.01780. https://arxiv.org/abs/1703.01780 — 提出 Mean Teacher，教師由學生權重的 EMA 建立。
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — 前身方法，以較早 epoch 的平均預測作為目標。
- Sohn, K. et al. (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. arXiv:2001.07685. https://arxiv.org/abs/2001.07685 — 以弱增強得到的高信心偽標籤作為強增強的目標。
- Miyato, T., Maeda, S., Koyama, M. & Ishii, S. (2018). Virtual Adversarial Training: A Regularization Method for Supervised and Semi-supervised Learning. arXiv:1704.03976. https://arxiv.org/abs/1704.03976 — 對抗式一致性正則化，是 Mean Teacher 比較的基準，並在某些設定下勝過它。

### 綜述與教科書

- Oliver, A. et al. (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — 指出許多已報告的增益在基準經過公平調校後會縮小。
