---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# 平均精確率均值

平均精確率均值（MAP）是各查詢的平均精確率（average precision）再對所有查詢取平均。單一查詢的平均精確率，是排序列表中每個出現相關項目的位置上，精確率的平均。MAP 以二元相關性標籤來總結排序品質。

## 定義

對於一個查詢，設排序列表為 $1..N$，$P(k)$ 為前 $k$ 個結果中的精確率，且若第 $k$ 個項目相關則 $\text{rel}(k) = 1$。則

$$\text{AP} = \frac{1}{R} \sum_{k=1}^{N} P(k)\, \text{rel}(k)$$

其中 $R$ 是相關項目的數量。MAP 是所有查詢的 AP 平均。參考文獻中的 Manning 等人章節以此方式定義平均精確率。

請注意，scikit-learn 的 `average_precision_score` 是對一組分數計算 AP，即精確率—召回率曲線下面積的階梯式形式，對單一排序而言是同一個概念（見參考文獻）。

## 解讀

當相關項目被一致地放在前面時，MAP 會很高。它也獎勵找出所有相關項目，因為從未被檢索到的相關項目，對總和沒有任何貢獻。

## 何時使用

在相關性為是或否、且每個相關項目都重要的資訊檢索基準中，使用 MAP。當相關性有多個等級，或只有前幾名結果重要時，應改用 [NDCG](ndcg.md)。

## 常見陷阱

- **查詢權重。** MAP 對每個查詢給予相同權重，因此少數有很多相關項目的查詢不會主導結果。應報告查詢數量。
- **判斷不完整。** 若有些相關項目沒有被標記，MAP 會被低估。這是測試集合的特性，不是排序本身的問題。

## 相關指標

[NDCG](ndcg.md)使用分級相關性，並依位置折損。家族概述見[排序指標](index.md)。

## 參考文獻

### 文章與文件

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 為單一排序列表定義平均精確率，MAP 即是對查詢取平均。
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — 由分數計算平均精確率的 API 參考，以及其階梯式公式。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
