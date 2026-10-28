---
status: complete
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

積分梯度（integrated gradients）沿著從基準輸入到實際輸入的直線路徑，累積模型的梯度，以此把預測歸因到各個輸入特徵。Sundararajan、Taly 與 Yan（2017）從兩條他們認為任何歸因方法都應滿足的公理推導出它。

## 問題

顯著性圖所用的普通梯度可能不可靠：在網路的飽和區域，即使某個特徵非常重要，梯度也可能接近零。問題在於找到一種歸因方法，不依賴梯度恰好平坦的位置，並且有充分的理論依據。

## 核心想法

選擇一個不含資訊的基準 $x'$，例如全黑影像或零向量。沿直線從基準移動到輸入，並沿途把梯度加總。總和即為每個特徵的歸因，相對於基準計算。

## 方程式

對輸入 $x$、基準 $x'$ 與模型 $F$，特徵 $i$ 的歸因為

$$
\mathrm{IG}_i(x) = (x_i - x'_i) \int_0^1 \frac{\partial F\bigl(x' + \alpha (x - x')\bigr)}{\partial x_i}\, d\alpha.
$$

實務上，積分以有限步數的和近似。

## 結果

論文以兩條公理設計此方法。敏感性（sensitivity）要求：改變輸出的特徵必須獲得非零歸因。實作不變性（implementation invariance）要求：功能等價的網路必須獲得相同的歸因。作者主張，多數既有的歸因方法至少違反其中一條公理。他們把積分梯度應用於兩個影像模型（包括 GoogLeNet 的 ImageNet 分類器與糖尿病視網膜病變分級網路）、兩個文字模型，以及一個分子圖模型。這些例子是說明性的；論文並未證明歸因在所有用途中都正確。

## 限制

- **依賴基準。** 結果取決於基準，而選擇中性的基準本身就是一種判斷。
- **近似。** 積分以數值方式估計，因此歸因帶有必須檢查的近似誤差。
- **描述模型，而非世界。** 歸因描述的是路徑上模型的敏感性，而非世界中的因果效應。
- **合理性檢驗。** 與其他梯度方法一樣，看起來合理的歸因本身並不能證明模型依賴該特徵（Adebayo et al., 2018）。

## 相關連結

積分梯度是[特徵歸因](feature-attribution.md)中的梯度方法。它以沿路徑求和來處理[顯著性圖](saliency-maps.md)的局部斜率問題；DeepLIFT（Shrikumar et al., 2017）則以相對於參考值的差分採取另一條路線。[SHAP](shap.md) 同樣使用參考，即背景分布，但它以賽局理論的平均來歸因，而非路徑積分。關於這些方法共同面對的基準依賴問題，見[可解釋性總覽](index.md)。

## 應用

- 以黑色或模糊的基準解釋影像分類，並檢查突顯的區域是否吻合物體。
- 以嵌入作為路徑變數，把文字模型的預測歸因到各個 token。
- 比較同一任務下不同模型的歸因。

## 開放問題

- 對特定領域而言，哪個基準是中性的？歸因對這個選擇有多敏感？
- 需要多少積分步數，才能得到可靠的近似？
- 對於有大量飽和單元的模型，基於路徑的歸因能否保持忠實？

## 參考文獻

### 開創性論文

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Introduces integrated gradients and the sensitivity and implementation-invariance axioms.
- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. arXiv:1312.6034. https://arxiv.org/abs/1312.6034 — The gradient-based saliency maps that integrated gradients refines.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — DeepLIFT, a reference-based alternative to gradient attribution.

### 綜述與教科書

- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Presents SHAP, which compares attributions with Shapley values rather than gradients.
- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Shows that some gradient-based maps are independent of the model and the data.

## 延伸學習

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. [免費線上書](https://christophm.github.io/interpretable-ml-book/)，涵蓋歸因方法與實例。
