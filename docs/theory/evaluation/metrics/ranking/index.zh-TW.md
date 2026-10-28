---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# 排序指標

排序指標用來評估一個有順序的列表。它們用於搜尋、推薦與檢索，問題是最相關的項目是否排在最前面。準確率等指標忽略順序，因此無法分辨同樣的項目組成，排序的好壞。

## 主要指標

| 指標 | 衡量什麼 | 相關性標籤 |
|---|---|---|
| [NDCG](ndcg.md) | 相關項目的增益，依位置折損，並相對於理想排序正規化 | 分級或二元 |
| [MAP](map.md) | 每個相關項目位置上精確率的平均，再對查詢取平均 | 二元 |

NDCG 獎勵把高度相關的項目放在靠前的位置，並且能處理分級的相關性。MAP 把相關性視為是或否，常見於資訊檢索的基準測試。

## 關聯

作為 MAP 基礎的每個查詢平均精確率，與[分類指標](../classification/index.md)中的精確率—召回率指標密切相關。參考文獻中的 Manning 等人章節為檢索定義了這些度量。

## 參考文獻

### 文章與文件

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 為單一排序列表定義平均精確率，並說明用來比較排序的檢索指標。
- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — 正規化折損累積增益的 API 參考，附有範例。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — 由預測分數計算平均精確率的 API 參考，附階梯式公式。
- Wang, Y., Wang, L., Li, Y., He, D., Chen, W. & Liu, T.-Y. (2013). A theoretical analysis of NDCG type ranking measures. arXiv:1304.6480. https://arxiv.org/abs/1304.6480 — 對 NDCG 類排序指標及其位置折扣的理論分析。
