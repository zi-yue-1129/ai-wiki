---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - bias
  - error rates
aliases:
  - 機會均衡
  - 等化勝算
  - Equalised odds
  - Equalized odds
---

# 等化勝算

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

等化勝算要求分類器在每個群體中都有相同的真陽性率與相同的假陽性率。它以真實結果為條件，因此檢驗的是模型對不同群體是否犯下同類的錯誤。Hardt、Price 與 Srebro（2016）定義了此準則，並提出訓練後達成此準則的方法。

## 問題

決策規則從整體看來可能很公平，但某些群體可能承受更多的錯誤指控，或更多的漏判。問題是以錯誤而非決定比率來定義公平，並說明預測器可以調整到符合此定義。

## 核心想法

要求決定的錯誤率，包括被正確標示為陽性的比率，以及被錯誤標示為陽性的陰性比率，都不依群體身分而改變。Hardt 等人表明，已學成的預測器可以在訓練後加以調整以符合此條件。調整後的決定只依賴預測與受保護屬性；當預測為二元時，找出最佳的此類決定是一個線性規劃問題。當預測為實數分數時，等化勝算可能需要隨機化的群體特定門檻，作者以數值方法求解。機會均等則只需要確定性的群體特定門檻。

## 公式

以受保護屬性 \(A\)、真實結果 \(Y\) 與預測 \(\hat{Y}\)，等化勝算成立時

\[
\Pr[\hat{Y}=1 \mid Y=y, A=a] = \Pr[\hat{Y}=1 \mid Y=y, A=b] \quad \text{對 } y \in \{0,1\} \text{ 與所有群體 } a, b \text{ 成立}
\]

機會均等是較弱的要求，它只要求 \(y=1\) 時的真陽性率相等。

## 結果

Hardt 等人（2016）使用信用違約的案例研究，樣本為 2003 年的 301,536 筆 TransUnion TransRisk 分數，成本比率固定為 82/18，門檻為 620。在 82% 不違約的門檻下，各規則達到最大利潤的比例如下：

| 規則 | 達到最大利潤的比例 |
|---|---|
| 不分種族 | 99.3% |
| 機會均等 | 92.8% |
| 等化勝算 | 80.2% |
| 人口統計均等 | 69.8% |

作者的結論是，機會均等的代價不到人口統計均等的四分之一。這個比較來自單一案例，使用單一分數與單一成本比率。

## 限制

- **基礎比率。** 當基礎比率不同時，等化勝算無法與相等的精確率（預測平等）同時成立（Chouldechova，2017）。群體內校準是另一項關於分數的條件，由 Kleinberg 等人（2017）處理。
- **後處理的代價。** 群體特定門檻會降低決定的利潤或準確率；調整後的規則在決定時需要受保護屬性。
- **不是公平的證明。** 論文指出，符合此準則，或任何其他只使用聯合統計量的準則，「不應被視為公平的決定性證明」。兩個具有相同聯合統計量的因果情境，無法靠這類檢驗區分。
- **標籤。** 此準則假設真實結果已被正確測量。作者指出，目標變數本身可能不可靠或有偏誤，因此對有偏誤的標籤達到相等錯誤率，只是較弱的保證。
- **有限樣本。** 分析假設聯合分布已知，未涵蓋從有限樣本進行的估計。

## 參考文獻

### 開創性論文

- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 定義等化勝算與機會均等，並提出達成它們的後處理方法。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示當各群體的盛行率不同時，相等的精確率與相等的錯誤率無法同時成立。論文以 COMPAS 再犯風險分數為例。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — 證明群體內校準與兩項平衡條件無法同時成立，除非可以完美預測或基礎比率相同。

### 綜述與教科書

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — 綜述機器學習中偏誤的來源，以及用來衡量偏誤的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 可免費線上閱讀的教科書，涵蓋錯誤率準則及其權衡。
