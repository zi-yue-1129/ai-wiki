---
status: draft
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

# 機會均衡

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

機會均衡要求分類器在每個群體中都具有相同的真陽性率與相同的偽陽性率。它以真實結果為條件，因此詢問的是：模型對不同群體是否犯了同樣類型的錯誤。Hardt、Price 與 Srebro（2016）定義了此準則，並提出在訓練後達成它的方法。

## 問題

決策規則平均來看可能很公平，卻讓某些群體承受更多的錯誤定罪或更多的漏判。問題是以錯誤而非僅以決策比率來定義公平，並說明預測器可以調整到符合此準則。

## 核心想法

要求決策的錯誤率（正確標出陽性的比率，以及錯誤標出陰性的比率）不依群體身分而異。論文顯示，對任何已學得的預測器，都可以使用各群體專屬的門檻加以調整，使其滿足此準則。

## 公式

\[
\Pr[\hat{Y}=1 \mid Y=y, A=a] = \Pr[\hat{Y}=1 \mid Y=y, A=b]
\]

此式對 \(y \in \{0,1\}\) 與所有群體 \(a\)、\(b\) 成立。機會均等（equal opportunity）是較弱的要求，只要求 \(y=1\) 時的真陽性率相等。

## 結果

Hardt 等人（2016）說明如何最佳地調整已學得的預測器，以依其定義消除歧視，並指出此準則只依賴預測器、目標與受保護屬性的聯合統計量。

## 限制

- **基礎比率。** 當基礎比率不同時，機會均衡無法與群體內校準同時成立（Chouldechova，2017；Kleinberg 等人，2017）。
- **後處理的代價。** 各群體專屬的門檻會降低部分群體的準確率，並且在決策時需要受保護屬性。
- **標籤。** 此準則假設真實結果量測正確；有偏誤的標籤會使相等的錯誤率成為較弱的保證。

## 參考文獻

### 開創性論文

- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 定義機會均衡與機會均等，並給出達成它們的後處理方法。
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — 顯示當基礎比率不同時，相等的錯誤率無法與預測值均等同時成立。
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — 證明三項公平性條件除特殊情況外無法同時成立。

### 綜述與教科書

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — 如其標題所述，這是一篇公平性定義的綜述。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 免費教科書，涵蓋錯誤率準則及其取捨。
