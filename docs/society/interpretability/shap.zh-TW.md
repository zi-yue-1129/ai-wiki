---
status: draft
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
    本方法頁屬於[特徵歸因](feature-attribution.md)。它詳細說明此方法；概述頁則比較各種方法。

SHAP（SHapley Additive exPlanations）將每個特徵的貢獻設為其 Shapley 值，此概念來自合作賽局理論，藉此解釋一次預測。Lundberg 與 Lee（2017）提出它作為統一的框架：他們顯示數種既有的解釋方法都是同一種加性形式的特例。

## 問題

解釋方法彼此不一致，很難說哪一種才是對的。問題在於找到一個單一的特徵重要性定義，它有清楚的意義，並可讓既有方法與之比較。

## 核心想法

把特徵視為一場賽局中的參與者，其報酬是僅知道部分特徵時模型的預測。特徵的 Shapley 值是它在所有子集合中的平均邊際貢獻。SHAP 以這些值作為解釋。

## 公式

對特徵集合 \(N\) 與價值函數 \(v(S)\)（僅知道 \(S\) 中特徵時模型的期望輸出），特徵 \(i\) 的 Shapley 值為

\[
\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N|-|S|-1)!}{|N|!}\,\bigl[v(S \cup \{i\}) - v(S)\bigr].
\]

對某次預測的解釋為 \(f(x) = \phi_0 + \sum_i \phi_i\)，其中 \(\phi_0\) 是背景資料上的期望輸出。

## 結果

Lundberg 與 Lee 報告，他們的加性特徵重要性度量類別統一了六種既有方法。論文的主張是關於這種統一，以及這些度量所具有的性質；它們並不能證明 SHAP 值對每個模型都是正確的解釋。

## 限制

- **成本。** 精確的總和有指數多項，因此實用版本需要近似，而近似必須加以檢查。
- **背景選擇。** Shapley 值取決於用來填補缺失特徵的參考分布。
- **相關特徵。** 評估不太可能出現的特徵組合，可能歸功於模型並未使用的特徵。
- **因果解讀。** 數值大只表示輸出依賴什麼，並不表示什麼導致結果。

## 參考文獻

### 開創性論文

- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — 提出 SHAP，並顯示六種既有方法是同一加性形式的特例。
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — 以 Shapley 值解釋一般模型的個別預測。
- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — LIME，SHAP 所統一的局部代理方法之一。

### 綜述與教科書

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — 積分梯度，SHAP 的框架也涵蓋的神經網路歸因方法。
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — 免費線上書籍，其中一章討論 Shapley 值與 SHAP。
