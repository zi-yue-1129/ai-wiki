---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - attribution
aliases:
  - 積分梯度
  - Integrated gradients
---

# 積分梯度

!!! info "屬於特徵歸因"
    本方法頁屬於[特徵歸因](feature-attribution.md)。它詳細說明此方法；概述頁則比較各種方法。

積分梯度沿著從基準輸入到實際輸入的直線路徑累加模型的梯度，藉此將預測歸因到輸入特徵。Sundararajan、Taly 與 Yan（2017）從兩項他們認為任何歸因方法都應滿足的公理推導出此方法。

## 問題

如同顯著性圖所用的純梯度，可能不可靠：在網路的飽和區域，即使某特徵很重要，梯度也可能接近零。問題在於找到一種不依賴梯度恰好平坦之處、且有充分原理支持的歸因方法。

## 核心想法

選擇一個不含資訊的基準 \(x'\)，例如全黑影像或零向量。沿直線從基準移動到輸入，並沿途累加梯度。總和即為每個特徵相對於基準的歸因。

## 公式

對輸入 \(x\)、基準 \(x'\) 與模型 \(F\)，特徵 \(i\) 的歸因為

\[
\mathrm{IG}_i(x) = (x_i - x'_i) \int_0^1 \frac{\partial F\bigl(x' + \alpha (x - x')\bigr)}{\partial x_i}\, d\alpha.
\]

實務上，積分以有限步數的和來近似。

## 結果

論文以敏感性（會改變輸出的特徵得到非零歸因）與實作不變性（功能等價的網路得到相同歸因）兩項公理來設計此方法。論文報告，多數已知的歸因方法不滿足這些公理。作者將此方法應用於兩個影像模型、兩個文字模型與一個化學模型，並顯示它可協助除錯網路。

## 限制

- **依賴基準。** 結果取決於基準，而選擇中性的基準本身就是一項判斷。
- **近似。** 積分以數值方式估計，因此歸因帶有必須檢查的近似誤差。
- **描述模型，而非世界。** 歸因描述的是模型沿路徑的敏感度，而非世界中的因果效應。
- **健全性。** 與其他梯度方法一樣，看似合理的歸因本身並不能證明模型依賴該特徵（Adebayo 等人，2018）。

## 參考文獻

### 開創性論文

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — 引入積分梯度，以及敏感性與實作不變性公理。
- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — 積分梯度所改進的基於梯度的顯著性圖。
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — 提出 SHAP，它以 Shapley 值而非梯度來比較歸因。

### 綜述與教科書

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — 顯示部分基於梯度的地圖與模型及資料無關。
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — 免費線上書籍，以範例涵蓋歸因方法。
