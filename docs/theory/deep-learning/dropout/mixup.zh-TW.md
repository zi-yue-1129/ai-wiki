---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/dropout
tags:
  - mixup
  - data augmentation
  - regularisation
aliases:
  - 混合增強
  - Mixup
---

# 混合增強（Mixup）

混合增強在成對樣本及其標籤的凸組合上訓練網路。對每一對樣本，從 Beta 分布抽出的隨機權重同時混合兩個輸入與兩個獨熱標籤，網路則在混合後的配對上訓練。此方法改變的是訓練資料，而非網路本身。

## 概觀

[本章](index.zh-TW.md)涵蓋隨機正則化。本頁說明混合增強，它透過改變資料來達到正則化。

## 問題

經驗風險最小化會擬合訓練點，但在訓練點之間的行為可能不可預測，使模型對輸入的微小擾動與損毀的標籤都很敏感。Zhang 等人提出混合增強，作為處理這些問題的簡單原則 [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412)。

## 核心想法

對兩個樣本 $(x_i, y_i)$ 與 $(x_j, y_j)$，抽取 $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$，並形成 $\tilde{x} = \lambda x_i + (1-\lambda) x_j$ 與 $\tilde{y} = \lambda y_i + (1-\lambda) y_j$。網路在配對 $(\tilde{x}, \tilde{y})$ 上訓練。

## 方程式

混合後的訓練損失為

$$\mathcal{L}_{\text{mix}} = \mathbb{E}_{\lambda, i, j}\left[\,\ell\big(f_\theta(\lambda x_i + (1-\lambda)x_j),\; \lambda y_i + (1-\lambda) y_j\big)\right]$$

其中 $\ell$ 是通常的分類損失，$y_i$、$y_j$ 為獨熱標籤。超參數 $\alpha$ 設定抽取 $\lambda$ 所用的 Beta 分布。

## 結果

摘要報告，混合增強在 ImageNet-2012、CIFAR-10、CIFAR-100、Google commands 與 UCI 資料集上提升了泛化能力。它也報告，混合增強能減少對損毀標籤的記憶、提升對對抗樣本的穩健性，並穩定生成對抗網路的訓練。確切數字見論文的實驗。

## 限制

- 報告的效益針對論文實驗中的資料集與模型，不會自動套用到其他任務。
- 摘要只透過實驗呈現不同 $\alpha$ 值的結果，因此新設定下的最佳選擇仍需自行檢驗。

## 關聯

[本章](index.zh-TW.md)涵蓋本節中的其他隨機正則化方法，這些方法作用於網路而非資料。

## 應用

影像分類、語音與表格任務，這些正是論文評估的任務類型。

## 開放問題

- 對於標籤具有空間結構的任務，例如偵測與分割，哪種混合方式最合適？
- 混合增強除了提升準確度，是否也會改變校準？

## 參考文獻

### 奠基性論文

- Zhang、Cisse、Dauphin 與 Lopez-Paz，*mixup: Beyond Empirical Risk Minimization*（2017）。https://arxiv.org/abs/1710.09412 — 提出混合增強，即樣本與標籤的凸組合。
- Szegedy 等人，*Rethinking the Inception Architecture for Computer Vision*，IEEE Conference on Computer Vision and Pattern Recognition（2016）。https://arxiv.org/abs/1512.00567 — 提出以標籤平滑來軟化訓練目標。
- Srivastava、Hinton、Krizhevsky、Sutskever 與 Salakhutdinov，*Dropout: A Simple Way to Prevent Neural Networks from Overfitting*，Journal of Machine Learning Research（2014）。https://jmlr.org/papers/v15/srivastava14a.html — 提出丟棄法，是神經網路的標準正則化器。
- Huang、Sun、Liu、Sedra 與 Weinberger，*Deep Networks with Stochastic Depth*（2016）。https://arxiv.org/abs/1603.09382 — 提出隨機深度，在訓練時隨機略過殘差區塊。
- Gal 與 Ghahramani，*Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning*（2016）。https://arxiv.org/abs/1506.02142 — 把丟棄法與近似貝氏推論連結起來。
