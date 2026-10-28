---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - calibration
  - risk scores
aliases:
  - 群體內校準
  - Calibration within groups
  - Calibration
---

# 群體內校準

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

群體內校準要求風險分數在每個群體中的意義相同：被給予分數 \(s\) 的人，無論屬於哪個群體，具有該結果的比例都相同。它是 Kleinberg、Mullainathan 與 Raghavan 不可能性結果中的三項條件之一。

## 問題

整體上校準良好的分數，仍可能對某個群體系統性地偏高、對另一群體系統性地偏低。問題是精確說明：一個分數對每個群體都同樣可信，究竟意味著什麼；以及此性質何時能與其他公平性準則同時成立。

## 核心想法

依分數將人分組，然後在每個群體內，檢查各分數水準下結果發生的頻率。群體內校準要求：對每個群體與每個分數區間，群體成員在該區間中屬於正類的比例，與該區間的分數相符。Kleinberg 等人將此列為三項條件之一，另外兩項是正類的平衡與負類的平衡。

## 公式

以分數 \(S\) 與受保護屬性 \(A\)，群體內校準成立時

\[
\Pr[Y=1 \mid S=s, A=a] = s \quad \text{對所有分數 } s \text{ 與所有群體 } a \text{ 成立}
\]

## 結果

Kleinberg 等人（2017）證明：若風險指派同時滿足三項條件，則該情境必須允許完美預測，或兩個群體的基礎比率必須相同。因此，當基礎比率不同時，群體內校準無法與兩項平衡條件同時成立，除非是這些特殊情況。

Chouldechova（2017）研究再犯風險預測工具，包括 COMPAS。當各群體的盛行率不同時，具有相等陽性預測值（預測平等）的分數，無法同時具有相等的假陽性率與假陰性率。她的結果涉及錯誤率與精確率，因此並未直接陳述上述校準條件。

## 限制

- **分數平衡與錯誤率。** 不可能性結果針對的是兩項分數平衡條件，而非門檻決定的錯誤率。當基礎比率不同時，經過校準的分數仍可能產生不等的假陽性率與假陰性率，因此相等的錯誤率需要另外檢驗。
- **分數的意義。** 校準並未說明在某個門檻上所做的決定；經過校準的分數仍可能導致不等的決定。
- **資料需求。** 要在小群體內檢驗校準，需要每個分數水準都有足夠的結果資料。

## 參考文獻

### 開創性論文

- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — 證明在基礎比率不同時，群體內校準與兩項平衡條件無法同時成立，除非可以完美預測。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示當各群體的盛行率不同時，相等的精確率與相等的錯誤率無法同時成立。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 定義與校準形成對照的錯誤率準則。

### 綜述與教科書

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — 綜述機器學習中偏誤的來源，以及用來衡量偏誤的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 可免費線上閱讀的教科書，涵蓋校準及其與其他準則的權衡。
