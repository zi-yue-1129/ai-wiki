---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
---

# FixMatch：以一致性與信心簡化半監督學習

FixMatch 是一種半監督方法。它把模型對弱增強未標註影像所做的高信心預測，當作硬偽標籤，然後訓練模型從同一張影像的強增強版本預測該標籤。低於信心門檻的預測會被忽略。家族層級的全貌見[一致性正則化](index.md)頁。

## 概述

Sohn 等人（2020）在 NeurIPS 2020 發表 FixMatch。論文結合了半監督學習中常見的兩個想法：同一輸入的擾動版本之間的一致性，以及高信心的偽標籤。它的目標是簡化。論文保留這兩個部分，並捨棄 MixMatch 使用的混合與銳化步驟。摘要報告，在 CIFAR-10 上使用 250 個標籤時準確率為 94.93%，使用 40 個標籤（每類 4 個）時準確率為 88.61%。論文在 CIFAR-10、CIFAR-100、SVHN、STL-10 與 ImageNet 上評估，皆為影像分類。

## 核心概念

- **弱增強** \(\alpha(\cdot)\)：隨機水平翻轉（SVHN 不使用），以及垂直與水平方向最多 12.5% 的隨機平移。
- **強增強** \(A(\cdot)\)：RandAugment 或 CTAugment，之後再加上 Cutout。
- **硬偽標籤** \(\hat q_b\)：在弱視角下機率最高的類別。
- **信心門檻** \(\tau\)：CIFAR-10、CIFAR-100、SVHN 與 STL-10 使用 0.95；論文表 4 中的 ImageNet 使用 0.7。
- **分布對齊（DA）**：對偽標籤分布所做的可選調整。論文在部分實驗中使用，並報告 CIFAR-100 以及僅有 1% 標籤的 ImageNet 需要它。

## 運作方式

每個訓練步驟取一批大小為 \(B\) 的有標籤資料，以及一批大小為 \(\mu B\) 的無標籤資料。監督損失是弱增強有標籤範例上的交叉熵：

\[
\ell_s = \frac{1}{B}\sum_{b=1}^{B} H\big(p_b,\; p_m(y \mid \alpha(x_b))\big)
\]

對每個無標籤範例，弱視角給出 \(q_b = p_m(y \mid \alpha(u_b))\) 與硬偽標籤 \(\hat q_b = \arg\max q_b\)。非監督損失只在偽標籤的信心達到 \(\tau\) 時保留它，並訓練強視角去預測它：

\[
\ell_u = \frac{1}{\mu B}\sum_{b=1}^{\mu B} \mathbb 1\big(\max q_b \ge \tau\big)\, H\big(\hat q_b,\; p_m(y \mid A(u_b))\big)
\]

其中 \(H\) 是交叉熵，\(p_m\) 是模型預測的分布。總損失為 \(\ell_s + \lambda_u \ell_u\)。論文在公式中把門檻判斷寫為 \(\ge \tau\)，但在演算法方框中寫為 \(> \tau\)。本頁依循公式。

論文在 CIFAR、SVHN 與 STL-10 實驗中的主要超參數為 \(B = 64\)、\(\mu = 7\) 與 \(\lambda_u = 1\)，使用 SGD、Nesterov 動量 0.9、學習率 0.03，並採用餘弦學習率衰減。權重衰減在 CIFAR-10、SVHN 與 STL-10 為 0.0005，在 CIFAR-100 為 0.001。

## 關鍵方法

### FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence（Sohn 等人，2020）

- **問題：** 許多半監督方法會結合多個損失與額外元件。當標籤很少時，它們的結果變動很大，而且很難把成效歸因於其中任何一個部分。
- **核心想法：** 把弱增強視角上的高信心預測，當作同一張影像強增強視角的目標。信心門檻會把雜訊較大的目標排除在外。
- **公式或演算法：** 監督損失、經門檻篩選的非監督損失，以及兩者的加權和，如上所述。
- **結果：** 以下錯誤率為五次交叉驗證的平均值，RA 與 CTA 為兩種強增強（表 2）。
  - CIFAR-10，250 個標籤：5.07 ± 0.65%（RA）與 5.07 ± 0.33%（CTA）。
  - CIFAR-10，4000 個標籤：4.26 ± 0.05%（RA）與 4.31 ± 0.15%（CTA）。
  - SVHN，1000 個標籤：2.28 ± 0.11%（RA）與 2.36 ± 0.19%（CTA）。
  - STL-10，1000 個標籤：7.98 ± 1.50%（RA）與 5.17 ± 0.63%（CTA）。
  - ImageNet 使用 10% 的標籤：top-1 錯誤率 28.54 ± 0.52%，τ = 0.7。
  - 摘要給出的對應準確率為：CIFAR-10 使用 250 與 40 個標籤時分別為 94.93% 與 88.61%。
  - 在門檻研究（第 5.1 節）中，τ = 0.95 在論文比較的數值中錯誤率最低。
  - 在 CIFAR-10 使用 40 個標籤時，五個隨機種子的錯誤率介於 5.46% 與 13.32% 之間（表 8）。
- **限制：** 作者形容在少量標籤下的結果「特別高變異」，並表示隨機種子的選擇影響很大。低門檻會放入雜訊較多的偽標籤，並可能造成確認偏誤。權重衰減與學習率對結果影響很大，論文也指出，同一技術「不一定能在不同實作之間直接比較」。在僅有 1% 標籤的 ImageNet 上，若沒有分布對齊，訓練「效果不佳」。實驗只涵蓋影像。論文沒有獨立的限制一節，以上內容取自其正文與附錄。

## 關聯

- FixMatch 屬於[一致性正則化](index.md)家族。它的偽標籤是[偽標籤與自訓練](../pseudo-labelling-and-self-training/index.md)中相關想法的一種經門檻篩選形式。
- [Mean Teacher](mean-teacher.md) 是另一種一致性方法。它使用權重平均的教師，而非經門檻篩選的偽標籤。
- 一致性方法所依賴的平滑性假設，由[基於圖的方法](../graph-based-methods/index.md)明確地表述。
- 對影像而言，增強方式是主要的設計選擇。見[電腦視覺](../../../models/computer-vision/index.md)。強增強策略也出現在[自監督學習](../../self-supervised/index.md)中。

## 開放問題

- 0.95 的門檻在影像以外的領域是否適當？當標籤稀少、模型較弱時，應如何設定？
- 分布對齊在 CIFAR-100 與僅有 1% 標籤的 ImageNet 上為何必要，而在其他資料集上則不一定？
- 能否讓此方法在每類一個標籤的情境下，對隨機種子較不敏感？

## 參考文獻

### 開創性論文

- Sohn, K. 等人 (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. NeurIPS 2020. https://arxiv.org/abs/2001.07685 — 提出 FixMatch，並提供本頁使用的結果。
- Berthelot, D. 等人 (2019). MixMatch: A Holistic Approach to Semi-Supervised Learning. arXiv:1905.02249. https://arxiv.org/abs/1905.02249 — 把一致性、銳化與 MixUp 結合成單一目標。FixMatch 簡化了這種設計。
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — 以較早 epoch 的預測平均值作為一致性目標。
- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models. NeurIPS 2017. https://arxiv.org/abs/1703.01780 — 使用由學生權重平均而成的教師。另見 [Mean Teacher](mean-teacher.md)。

### 綜述與教科書

- Oliver, A. 等人 (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — 顯示當基準方法經過公平調校後，許多已報告的進步會縮小。比較 FixMatch 等方法時應留意這點。
