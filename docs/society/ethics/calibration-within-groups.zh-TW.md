---
status: draft
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

群體內校準要求風險分數在每個群體中都代表相同的意義：得到分數 \(s\) 的人，無論屬於哪個群體，具有該結果的比例都應相同。它是 Kleinberg、Mullainathan 與 Raghavan 的不可能性結果中的三項條件之一。

## 問題

整體上校準良好的分數，仍可能系統性地對某一群體偏高、對另一群體偏低。問題是精確陳述一個分數對每個群體都同樣可信意味著什麼，以及此性質何時能與其他公平性準則同時成立。

## 核心想法

依分數將人分組，並在每個群體內檢查每個分數水準上結果發生的頻率。若對每個群體而言，各分數水準的觀察比率都與該分數相符，則群體內校準成立。

## 公式

對分數 \(S\) 與受保護屬性 \(A\)，群體內校準成立時

\[
\Pr[Y=1 \mid S=s, A=a] = s.
\]

此式對所有分數 \(s\) 與所有群體 \(a\) 成立。

## 結果

Kleinberg 等人（2017）顯示，除高度受限的特殊情況外，群體內校準無法與正類及負類的平衡條件同時成立。Chouldechova（2017）顯示，對二元預測而言，當再犯率在各群體間不同時，校準型準則與錯誤率平衡相互衝突。

## 限制

- **錯誤率的衝突。** 當基礎比率不同時，群體內校準無法與相等的錯誤率同時成立，因此經過校準的工具仍可能產生不等的偽陽性率。
- **分數的意義。** 校準並未說明在某個門檻下所做的決定；經過校準的分數仍可能導致不等的決定。
- **資料需求。** 在小群體中檢查校準，需要每個分數水準上有足夠的結果資料。

## 參考文獻

### 開創性論文

- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — 證明當基礎比率不同時，群體內校準與兩項平衡條件無法同時成立。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示當預測率不同時，多項公平性準則無法同時成立。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 定義與校準形成對照的錯誤率準則。

### 綜述與教科書

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 如其標題所述，這是一篇公平性定義的綜述。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，涵蓋校準及其與其他準則的取捨。
