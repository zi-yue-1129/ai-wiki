---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - explainable AI
  - Shapley values
aliases:
  - Shapley 加性解釋
  - SHAP
  - Shapley additive explanations
---

# SHAP

!!! info "屬於特徵歸因"
    本方法頁屬於[特徵歸因](feature-attribution.md)。它詳細說明此方法；總覽頁則比較各種方法。

SHAP（SHapley Additive exPlanations）以合作賽局理論中的 Shapley 值，為每個特徵給出一份貢獻，以解釋一個預測。Lundberg 與 Lee（2017）把它提出為統一的框架：他們證明，數個較早的解釋方法都是同一種加性形式的特例。

## 問題

解釋方法彼此不一致，很難判斷哪一種才正確。問題在於找到一個意義清楚的特徵重要性定義，並讓既有方法能與之比較。

## 核心想法

把特徵視為賽局中的參與者，其報酬是只知道部分特徵時的模型預測。一個特徵的 Shapley 值，是它在所有子集合中的平均邊際貢獻。SHAP 以這些值作為解釋。

## 方程式

設特徵集合為 $N$，價值函數 $v(S)$ 為只知道 $S$ 中特徵時模型輸出的期望值，則特徵 $i$ 的 Shapley 值為

$$
\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\bigl[v(S \cup \{i\}) - v(S)\bigr].
$$

對一個預測的解釋為 $f(x) = \phi_0 + \sum_i \phi_i$，其中 $\phi_0$ 是背景資料上的期望輸出。

## 結果

Lundberg 與 Lee 指出，他們的加性特徵歸因方法類別統一了六種既有方法：LIME、DeepLIFT、逐層相關性傳播、Shapley 迴歸值、Shapley 取樣值，以及量化輸入影響。這些方法都使用同一線性形式的解釋模型。論文的主張是關於這種統一，以及所得度量的性質；它並未證明 SHAP 值對每一個模型都是正確的解釋。

## 限制

- **成本。** 精確的求和有指數多項，因此實際版本都是近似，而近似必須加以檢查。
- **背景的選擇。** Shapley 值取決於用來補上缺失特徵的參考分布。
- **相關特徵。** 評估不太可能出現的特徵組合，可能會把功勞歸給模型其實並未使用的特徵。
- **因果解讀。** 數值大只表示輸出依賴該特徵，並不表示它是結果的原因。

## 相關連結

SHAP 屬於[特徵歸因](feature-attribution.md)，與 [LIME](lime.md)、[顯著性圖](saliency-maps.md)及[積分梯度](integrated-gradients.md)並列。它所用的 Shapley 值來自合作賽局理論，也是許多公平分配概念的基礎，相關見[倫理與公平](../ethics/index.md)。與梯度方法不同，SHAP 不需要梯度，因此可用於表格模型，以及不可微分的模型。

## 應用

- 向需要檢查的分析師解釋信用、風險與臨床模型的預測。
- 以平均絕對 Shapley 值對整個資料集的特徵排序，作為全域摘要。
- 稽核模型是否依賴敏感屬性，但須注意上述限制。

## 開放問題

- 特徵高度相關時，應如何選擇背景分布？
- 近似的 Shapley 值何時會與精確值差得足以改變解釋？
- 基於 Shapley 的解釋，能否幫助人們做出更好的決定，而不只是讓人更有信心？

## 參考文獻

### 開創性論文

- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Introduces SHAP and shows that six existing methods are special cases of one additive form.
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — Uses Shapley values to explain individual predictions of general models.
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — LIME, the local surrogate method that SHAP unifies with other additive methods.

### 綜述與教科書

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Integrated gradients, a neural-network attribution method that SHAP's framework also covers.
- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Shows that some attribution maps fail basic tests, a caution that applies to any explanation method.

## 延伸學習

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. [免費線上書](https://christophm.github.io/interpretable-ml-book/)，其中有一章討論 Shapley 值與 SHAP。
