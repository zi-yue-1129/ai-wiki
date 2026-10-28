---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# Dice 係數

Dice 係數衡量預測區域與參考區域之間的重疊程度，並經過縮放，使兩個完全相同的區域得 1 分。它在醫學影像分割中被廣泛使用，常被稱為 Dice 相似係數。

## 定義

對於預測區域 $A$ 與參考區域 $B$：

$$\text{Dice} = \frac{2\,|A \cap B|}{|A| + |B|}$$

在二元遮罩上，若逐像素計算 $TP$、$FP$ 與 $FN$，則等於 $\frac{2\,TP}{2\,TP + FP + FN}$，也就是正例類別的 [F1 分數](../classification/f1.md)。正因為這個恆等式，兩者常被視為同一個量來報告。

## 解讀

對於完全相同的區域，Dice 為 1；沒有重疊時為 0。由於 $\text{Dice} = 2\,\text{IoU} / (1 + \text{IoU})$，對於同一組遮罩，Dice 一定不小於 [IoU](iou.md)。因此 Dice 為 0.8 對應的 IoU 約為 0.67。若要比較不同論文中的 Dice 與 IoU，需要先做換算。

## 何時使用

當區域大小變化很大，且分數是逐案例計算後再平均時，例如醫學影像，使用 Dice 係數。應報告分數是依影像平均還是依像素平均，因為當區域大小不同時，兩種方式的結果會不一樣。

## 範例

沿用 [IoU](iou.md) 範例的兩個區域：預測 6 個像素、參考 4 個像素、共享 3 個。Dice 為 $2 \cdot 3 / (6 + 4) = 0.60$。作為檢查，$2 \cdot 0.43 / (1 + 0.43) \approx 0.60$。若兩個遮罩都是空的，公式會變成 $0/0$，即下方陷阱所說的空遮罩情況。

## 性質與變體

- **像素形式。** $\mathrm{Dice} = 2\,\mathrm{TP} / (2\,\mathrm{TP} + \mathrm{FP} + \mathrm{FN})$。係數 2 讓重疊在兩個區域中各計一次，因此只有兩個區域完全相同時分數才為 1。
- **軟性 Dice 損失。** 訓練時以預測機率取代硬遮罩，並最小化 $1 - \mathrm{Dice}$。Milletari 等人（2016）以這類基於 Dice 的目標函數訓練體積分割網路。
- **廣義 Dice。** Sudre 等人（2017）以各類別大小的平方倒數加權，使小型結構在整體分數中的影響與大型結構相近。
- **限制。** Dice 獎勵大區域的重疊，但對邊界位置的說明有限。常會與邊界距離指標一起報告。

## 常見陷阱

- **空遮罩。** 若兩個遮罩都是空的，公式為 0/0。必須說明這種情況所用的慣例。
- **慣例混用。** Dice 與 IoU 都是同一組遮罩上的重疊指標，但比較不同論文時，需要知道每篇各用哪一種。

## 相關指標

[IoU](iou.md)是分母不同的同類重疊指標。[F1](../classification/f1.md)則是把同一公式用在像素標籤上。家族概述見[分割指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API 參考，給出公式 $2TP / (2TP + FP + FN)$，在二元遮罩上即為 Dice 係數。
- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — Dice 相關的重疊指標之 API 參考。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- Dice, L. R. (1945). Measures of the amount of ecologic association between species. *Ecology* 26(3), 297–302. https://doi.org/10.2307/1932409 — 首次定義此係數的原始論文，當時用於衡量物種之間的關聯。
- Milletari, F., Navab, N. & Ahmadi, S.-A. (2016). V-Net: fully convolutional neural networks for volumetric medical image segmentation. 3DV 2016. https://arxiv.org/abs/1606.04797 — 提出體積醫學影像分割網路，並以基於 Dice 的目標函數訓練。
