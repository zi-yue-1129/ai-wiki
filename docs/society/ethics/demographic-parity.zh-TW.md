---
status: complete
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
\Pr[\hat{Y}=1 \mid A=a] = \Pr[\hat{Y}=1 \mid A=b] \quad \text{對所有群體 } a, b \text{ 成立}
\]

## 結果

- **差別影響與資訊洩漏。** Feldman 等人（2015）採用推廣的四分之五規則：當正向決定比率的比值至多為 τ = 0.8 時，資料集具有差別影響。他們證明，資料集具有差別影響，若且唯若可以從非受保護的特徵預測出受保護屬性，且平衡錯誤率至多為 1/2 − β/8，其中 β 是受保護群體被選中的比例。他們也提出一種修復方法，將非受保護的數值朝各群體內的中位數分布移動，並以參數 λ 控制修復的程度。
- **限制的代價。** Corbett-Davies 等人（2017）研究美國佛羅里達州布勞沃德郡（Broward County）的審前羈押決定，其中 30% 的被告被羈押（100 次隨機訓練－測試切分）。強制統計均等後，被羈押者中有 17% 屬於相對低風險。作者估計，這會使獲釋被告的暴力再犯率上升 9%，比較的基準是只追求公共安全的規則。預測平等的限制分別為 14% 與 7%，條件統計均等的限制則為 10% 與 4%。

## 限制

- **忽略準確率。** 透過接受某些群體中較不準確的決定，可以達到相等的比率。上述布勞沃德郡的數字，正是此權衡的實證版本。
- **基礎比率。** Kleinberg 等人（2017）與 Chouldechova（2017）顯示，當基礎比率不同時，校準與錯誤率準則無法同時成立。人口統計均等不是那些定理中的條件，因此這些結果不能直接判定它是否與之相容。
- **群體的定義。** 結果取決於定義了哪些群體，以及如何定義。

## 參考文獻

### 開創性論文

- Feldman, M., Friedler, S. A., Moeller, J., Scheidegger, C. & Venkatasubramanian, S. (2015). Certifying and Removing Disparate Impact. *Proceedings of KDD 2015*, 259–268. https://doi.org/10.1145/2783258.2783311 — 將差別影響與分類器揭露受保護屬性的資訊連結起來，並描述去除差別影響的修復方法。
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*, 214–226. https://doi.org/10.1145/2090236.2090255 — 提出個體公平，它常被拿來與群體準則對照。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 根據預測、目標與屬性的聯合統計量定義等化勝算與機會均等，並提出後處理方法。
- Corbett-Davies, S., Pierson, E., Feller, A., Goel, S. & Huq, A. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*, 797–806. https://doi.org/10.1145/3097983.3098095 — 衡量在風險導向的決定上施加公平性限制，對公共安全造成的代價。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — 證明群體內校準與兩項平衡條件，只有在允許完美預測或基礎比率相同時才能同時成立。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示當各群體的盛行率不同時，相等的精確率與相等的錯誤率無法同時成立。

### 綜述與教科書

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — 綜述機器學習中偏誤的來源，以及用來衡量偏誤的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 可免費線上閱讀的教科書，涵蓋群體準則及其權衡。

## 延伸學習

- [Fairlearn](https://fairlearn.org/) — 開源工具箱，包含人口統計均等指標與緩解方法。
