---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - explainable AI
  - surrogate models
aliases:
  - 局部可解釋模型
  - LIME
  - Local interpretable model-agnostic explanations
---

# LIME

!!! info "屬於特徵歸因"
    本方法頁屬於[特徵歸因](feature-attribution.md)。它詳細說明此方法；概述頁則比較各種方法。

LIME（Local Interpretable Model-agnostic Explanations，局部可解釋的模型無關解釋）在一個輸入附近，以一個簡單、可解釋的模型去擬合任何分類器的行為，藉此解釋該次預測。Ribeiro、Singh 與 Guestrin（2016）提出此方法，它不需要存取模型的內部結構。

## 問題

複雜的分類器可能很準確，但使用者若要根據某次預測行事，就需要知道它為何被做出。問題在於僅使用模型的輸入與輸出，以人能讀懂的方式解釋單一決定。

## 核心想法

擾動輸入以產生許多相近的樣本，記錄分類器對每個樣本的輸出，並依樣本與原始輸入的接近程度加權。對這些加權樣本擬合一個稀疏的線性模型。該模型的係數就是解釋，而它只在原始輸入附近忠實。

## 公式

LIME 選擇可解釋模型 \(g\) 作為解釋 \(\xi(x)\)，在局部忠實與簡潔之間取得平衡：

\[
\xi(x) = \operatorname*{argmin}_{g \in G} \; \mathcal{L}(f, g, \pi_x) + \Omega(g),
\]

其中 \(f\) 為分類器，\(\pi_x\) 為圍繞 \(x\) 的接近度加權，\(\mathcal{L}\) 衡量 \(g\) 在 \(x\) 附近與 \(f\) 的不符程度，\(\Omega(g)\) 則懲罰複雜度。

## 結果

論文報告模擬實驗與人類受試者實驗。人類受試者研究檢驗解釋是否幫助人決定是否信任某一預測，以及是否幫助人在模型間做選擇。結果支持這些解釋在這些決定上的用處，但不代表它們是對模型的準確描述。

## 限制

- **只有局部。** 解釋描述的是模型在某一輸入附近的行為，對其他輸入未必成立。
- **不穩定。** 擾動是隨機的，除非控制取樣，否則重複執行可能得到不同的解釋。
- **表示法的選擇。** 可解釋的特徵（例如詞或超像素）由設計者選定，並決定解釋的形狀。
- **忠實度。** 低複雜度的代理模型可能看似可信，卻誤述了原模型；必須加以量測。

## 參考文獻

### 開創性論文

- Ribeiro, M. T., Singh, S. & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *Proceedings of KDD 2016*. https://arxiv.org/abs/1602.04938 — 提出 LIME，並報告模擬與人類受試者實驗。
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — 提出 SHAP，這是相關的加性方法，統一了六種既有解釋方法。
- Štrumbelj, E. & Kononenko, I. (2014). Explaining prediction models and individual predictions with feature contributions. *Knowledge and Information Systems*, 41(3), 647–665. https://doi.org/10.1007/s10115-013-0679-x — 以 Shapley 值基礎的特徵貢獻，解釋一般模型的個別預測。

### 綜述與教科書

- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — 神經網路的基於梯度替代方法，用於比較。
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — 免費線上書籍，其中一章討論局部代理模型，包括 LIME。
