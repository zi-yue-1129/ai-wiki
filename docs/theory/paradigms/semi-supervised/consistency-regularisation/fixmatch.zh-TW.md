---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
---

# FixMatch

FixMatch 是一種半監督方法。它以模型對弱增強之未標籤影像的高信心預測作為硬偽標籤，然後訓練模型從同一張影像的強增強版本預測該標籤。低於信心門檻的預測會被忽略。家族層級的概觀見[一致性正則化](index.md)頁面。

## 概述

Sohn 等人（2020）提出 FixMatch。論文結合了半監督學習中常見的兩個想法：對同一輸入之擾動視角的一致性，以及高信心的偽標籤。它的目標是簡單。它保留這兩個部分，並捨棄 MixMatch 使用的混合與銳化步驟。摘要報告，在 CIFAR-10 上使用 250 個標籤時準確率為 94.93%，使用 40 個標籤（每類四個）時為 88.61%。論文在 CIFAR-10、CIFAR-100、SVHN、STL-10 與 ImageNet 上評估，皆為影像分類。

## 核心概念

- **弱增強** \(\alpha(\cdot)\)：隨機水平翻轉（SVHN 不使用）與垂直、水平最多 12.5% 的隨機平移。
- **強增強** \(A(\cdot)\)：RandAugment 或 CTAugment，之後接 Cutout。
- **硬偽標籤** \(\hat q_b\)：弱視角下機率最高的類別。
- **信心門檻** \(\tau\)：CIFAR-10、CIFAR-100、SVHN 與 STL-10 為 0.95，ImageNet 為 0.7（附錄 C）。
- **分布對齊（DA）**：對偽標籤分布的可選調整。論文在部分實驗中使用，並報告 CIFAR-100 與只有 1% 標籤的 ImageNet 需要它。

## 運作方式

每個訓練步驟取一個大小為 \(B\) 的有標籤批次，與一個大小為 \(\mu B\) 的未標籤批次。監督損失是弱增強有標籤樣本上的交叉熵：

\[
\ell_s = \frac{1}{B}\sum_{b=1}^{B} H\big(p_b,\; p_m(y \mid \alpha(x_b))\big)
\]

對每個未標籤樣本，弱視角給出 \(q_b = p_m(y \mid \alpha(u_b))\) 與硬偽標籤 \(\hat q_b = \arg\max q_b\)。只有當信心達到 \(\tau\) 時，無監督損失才保留該偽標籤，並訓練強視角去預測它：

\[
\ell_u = \frac{1}{\mu B}\sum_{b=1}^{\mu B} \mathbb 1\big(\max q_b \ge \tau\big)\, H\big(\hat q_b,\; p_m(y \mid A(u_b))\big)
\]

這裡 \(H\) 是交叉熵，\(p_m\) 是模型預測的分布。總損失為 \(\ell_s + \lambda_u \ell_u\)。論文在方程式中把門檻判斷寫成 \(\ge \tau\)，在演算法方框中寫成 \(> \tau\)。本頁依循方程式。

ImageNet 方面，論文使用 \(\tau = 0.7\) 與 \(\lambda_u = 10\)（附錄 C）。其他資料集使用 \(\tau = 0.95\)。

## 關鍵方法

### FixMatch：以一致性與信心簡化半監督學習（Sohn 等人，2020）

- **問題：**許多半監督方法結合多個損失與額外元件。只有少量標籤時，結果差異很大，而且很難把增益歸因於任何單一部分。
- **核心想法：**以弱增強視角上的高信心預測，作為同一張影像強增強視角的目標。信心門檻能把雜訊較大的目標排除在外。
- **方程式或演算法：**如上所述的監督損失、有門檻的無監督損失，以及它們的加權和。
- **結果：**以下錯誤率來自表 2，RA 與 CTA 為兩種強增強，以平均 ± 標準差表示。
  - CIFAR-10，250 個標籤：5.07 ± 0.65%（RA）與 5.07 ± 0.33%（CTA）。
  - CIFAR-10，4000 個標籤：4.26 ± 0.05%（RA）與 4.31 ± 0.15%（CTA）。
  - SVHN，1000 個標籤：2.28 ± 0.11%（RA）與 2.36 ± 0.19%（CTA）。
  - STL-10，1000 個標籤：7.98 ± 1.50%（RA）與 5.17 ± 0.63%（CTA）。
  - ImageNet 使用 10% 標籤，τ = 0.7、λu = 10：top-1 錯誤率 28.54 ± 0.52%，top-5 錯誤率 10.87 ± 0.28%。
  - 摘要給出 CIFAR-10 使用 250 與 40 個標籤時對應的準確率 94.93% 與 88.61%。
- **限制：**作者形容少標籤情況下的結果「特別高變異」，並指出種子的選擇很重要。門檻太低會放入雜訊較大的偽標籤，並可能造成確認偏誤。權重衰減與學習率對結果影響很大，論文指出同樣的技術「在不同實作之間不一定能直接比較」。在只有 1% 標籤的 ImageNet 上，沒有分布對齊時訓練「效果不佳」。實驗只涵蓋影像。論文沒有專門的限制一節，因此這些內容取自其正文與附錄。

## 關聯

- FixMatch 屬於[一致性正則化](index.md)家族。它的偽標籤是[偽標籤與自訓練](../pseudo-labelling-and-self-training/index.md)中想法的門檻化形式。
- 它的強增強包含 [RandAugment](https://arxiv.org/abs/1909.13719)，一種搜尋空間縮減的自動化增強策略。
- [Mean Teacher](mean-teacher.md) 是另一種一致性方法，它使用權重平均的教師，而不是有門檻的偽標籤。
- 一致性方法所依賴的平滑性假設，在[圖方法](../graph-based-methods/index.md)中明確提出。
- 對影像而言，增強是主要的設計選擇。見[電腦視覺](../../../models/computer-vision/index.md)。強增強策略也出現在[自監督學習](../../self-supervised/index.md)中。

## 開放問題

- 0.95 的門檻在影像以外是否仍是正確選擇？當標籤稀少且模型較弱時，應如何設定？
- 為什麼分布對齊在某些資料集（如 CIFAR-100 與只有 1% 標籤的 ImageNet）上重要，在其他資料集上則否？
- 在每類只有一個標籤的情況下，能否讓此方法對種子較不敏感？

## 參考文獻

### 代表性論文

- Sohn, K. et al. (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. arXiv:2001.07685. https://arxiv.org/abs/2001.07685 — 提出 FixMatch，本頁使用的結果來自此論文。
- Cubuk, E. D., Zoph, B., Shlens, J. & Le, Q. V. (2019). RandAugment: Practical automated data augmentation with a reduced search space. arXiv:1909.13719. https://arxiv.org/abs/1909.13719 — 定義 RandAugment，即 FixMatch 所用兩種強增強之一。
- Berthelot, D. et al. (2019). MixMatch: A Holistic Approach to Semi-Supervised Learning. arXiv:1905.02249. https://arxiv.org/abs/1905.02249 — 把一致性、銳化與 MixUp 結合成單一目標。FixMatch 簡化了這種設計。
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — 以較早 epoch 的預測平均值作為一致性目標。
- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. arXiv:1703.01780. https://arxiv.org/abs/1703.01780 — 使用由學生權重平均構成的教師。另見 [Mean Teacher](mean-teacher.md)。

### 綜述與教科書

- Oliver, A. et al. (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — 指出許多已報告的增益在基準經過公平調校後會縮小，比較 FixMatch 等方法時需要留意。
