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

混合增強在成對樣本及其標籤的凸組合上訓練網路。一個隨機權重同時混合兩張影像及其獨熱標籤，模型學習預測混合後的標籤。此方法作為資料層級的正則化器，並鼓勵訓練點之間呈現近似線性、較簡單的行為。

## 概觀

[本章](index.zh-TW.md)涵蓋隨機正則化。本頁說明混合增強，它改變的是資料而非網路，以此達到正則化。

## 問題

標準的經驗風險最小化會擬合訓練點，但在訓練點之間的行為可能很不穩定，使模型對輸入的微小變化與標籤雜訊都很敏感。Zhang 等人提出混合增強作為緩解這些問題的簡單原則 [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412)。

## 核心想法

對兩個樣本 $(x_i, y_i)$ 與 $(x_j, y_j)$，抽取 $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$，並形成 $\tilde{x} = \lambda x_i + (1-\lambda) x_j$ 與 $\tilde{y} = \lambda y_i + (1-\lambda) y_j$。網路在混合後的配對上訓練。訓練信號因此要求模型在原始樣本之間表現出線性行為。

## 方程式

混合後的訓練損失為

$$\mathcal{L}_{\text{mix}} = \mathbb{E}_{\lambda, i, j}\left[\,\ell\big(f_\theta(\lambda x_i + (1-\lambda)x_j),\; \lambda y_i + (1-\lambda) y_j\big)\right]$$

其中 $\ell$ 是通常的分類損失，$y_i$ 與 $y_j$ 為獨熱標籤。參數 $\alpha$ 控制混合的強度；較小的值使大多數混合配對接近其中一個原始樣本。

## 結果

論文報告，在影像分類基準上泛化能力有所提升，對某些類型的損毀標籤與對抗樣本也更為穩健。確切數字見其實驗章節。

## 限制

- 混合後的影像不一定對應到真實的輸入，對於要求內容可被辨識的任務，這可能成為問題。
- 對於文字或圖等結構化輸入，混合較不自然，因為凸組合沒有明顯的意義。
- 效益取決於 $\alpha$ 的選擇與訓練長度。

## 關聯

混合增強與[章節](index.zh-TW.md)中的標籤平滑概念相關，兩者都會軟化目標。它是與 [丟棄法](dropout-method.zh-TW.md)與[隨機深度](stochastic-depth.zh-TW.md)並用的正則化器之一。

## 應用

影像分類，以及部分語音與表格任務，常被當作標準的資料增強使用。

## 開放問題

- 對於標籤具有空間結構的偵測與分割任務，哪種混合方式最好？
- 混合增強除了提升準確度，是否也有助於校準？

## 參考文獻

### 奠基性論文

- Zhang、Cisse、Dauphin 與 Lopez-Paz，*mixup: Beyond Empirical Risk Minimization*（2017）。https://arxiv.org/abs/1710.09412 — 提出混合增強，即樣本與標籤的凸組合。
- Szegedy 等人，*Rethinking the Inception Architecture for Computer Vision*，IEEE Conference on Computer Vision and Pattern Recognition（2016）。https://arxiv.org/abs/1512.00567 — 透過標籤平滑得到的軟目標，是最接近的相關想法。
- Srivastava、Hinton、Krizhevsky、Sutskever 與 Salakhutdinov，*Dropout: A Simple Way to Prevent Neural Networks from Overfitting*，Journal of Machine Learning Research（2014）。https://jmlr.org/papers/v15/srivastava14a.html — 常與混合增強併用的標準正則化器。
- Huang、Sun、Liu、Sedra 與 Weinberger，*Deep Networks with Stochastic Depth*（2016）。https://arxiv.org/abs/1603.09382 — 深層視覺模型中使用的另一種正則化器。
- Gal 與 Ghahramani，*Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning*（2016）。https://arxiv.org/abs/1506.02142 — 不確定性觀點，與校準良好的預測有相同目標。
