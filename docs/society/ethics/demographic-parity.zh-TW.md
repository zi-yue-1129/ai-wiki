---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - bias
aliases:
  - 人口統計均等
  - 統計均等
  - Demographic parity
  - Statistical parity
---

# 人口統計均等

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

人口統計均等要求分類器在受保護屬性所定義的每個群體中，給出正向決定的比率都相同。它是最簡單的群體準則，並與法律上的差別影響（disparate impact）概念密切相關。Feldman 等人（2015）將差別影響與分類器洩漏受保護屬性資訊的程度連結起來。

## 問題

決策過程即使沒有人刻意為之，仍可能讓不同群體得到非常不同的結果。問題是為這些結果定義一個可量測的標準，並說明何種比率差異才算差別影響。

## 核心想法

選定一個決策規則，比較它在各群體中的正向決定比率。若比率相等，即滿足人口統計均等。此準則忽略真實結果，因此衡量的是決定如何分布，而非決定是否正確。

## 公式

以受保護屬性 \(A\) 與預測 \(\hat{Y}\)，人口統計均等成立時

\[
\Pr[\hat{Y}=1 \mid A=a] = \Pr[\hat{Y}=1 \mid A=b].
\]

此式對所有群體 \(a\) 與 \(b\) 成立。

## 結果

Feldman 等人（2015）將差別影響這一法律概念，與分類器輸出洩漏受保護屬性的程度連結起來，並描述去除偏誤資料的方法。

## 限制

- **忽略準確率。** 透過接受某些群體中較不準確的預測，可以達到相等的比率；Corbett-Davies 等人（2017）顯示此類限制有其代價。
- **基礎比率。** 當真實結果的比率在各群體間不同時，相等的決定比率會與校準及錯誤率準則衝突（Kleinberg 等人，2017；Chouldechova，2017）。
- **群體的定義。** 結果取決於定義了哪些群體，以及如何定義。

## 參考文獻

### 開創性論文

- Feldman, M., Friedler, S. A., Moeller, J., Scheidegger, C. & Venkatasubramanian, S. (2015). Certifying and Removing Disparate Impact. *Proceedings of KDD 2015*. https://doi.org/10.1145/2783258.2783311 — 將差別影響與分類器揭露受保護屬性的資訊連結起來，並描述去除差別影響的方法。
- Dwork, C. et al. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — 提出個體公平，它常被拿來與群體準則對照。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 基於預測、目標與屬性之聯合統計量定義準則，並提出後處理方法。
- Corbett-Davies, S., Pierson, E., Feller, A. & Goel, S. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*. https://doi.org/10.1145/3097983.3098095 — 分析在風險導向的決定上施加公平性限制對公共安全的代價。
- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 如其標題所述，這是一篇公平性定義的綜述。

## 延伸學習

- [Fairlearn](https://fairlearn.org/) — 開源工具箱，包含人口統計均等指標與緩解方法。
