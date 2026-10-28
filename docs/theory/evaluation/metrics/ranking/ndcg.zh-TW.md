---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# NDCG

正規化折損累積增益（NDCG）對排序列表的評分方式是：把每個項目的相關性加總，依其在列表中出現的位置折損，最後除以同一組項目的最佳可能分數。它的值介於 0 與 1 之間。

## 定義

對一組預測分數，項目依分數排序。每個項目的貢獻是其真實相關性除以位置的對數，因此排在越後面的項目權重越小。折損累積增益（DCG）是這些貢獻的總和。NDCG 是把 DCG 除以理想 DCG，後者是依真實相關性排序所得的值。

在 scikit-learn 中，`ndcg_score` 接受真實相關性與預測分數，並可選擇截斷值 $k$，只計算前 $k$ 個項目（見參考文獻）。

## 解讀

NDCG 為 1.0 表示排序已是理想的。由於每個位置都有折損，把一個高度相關的項目從第 1 名移到第 5 名，代價比從第 50 名移到第 54 名更大。此指標可以使用分級的相關性（例如 0 到 10），這是 MAP 做不到的。

## 何時使用

在搜尋與推薦中比較排序時使用 NDCG，特別是當相關性有多個等級，或只有前幾名結果重要時。此時應設定截斷值 $k$，並一併報告。

## 常見陷阱

- **依查詢正規化。** NDCG 先對每個查詢計算，再取平均。沒有相關項目的查詢需要說明採用的慣例。
- **截斷值。** $k = 10$ 與考慮所有項目的結果，回答的是不同問題。應連同分數一起報告截斷值。

## 相關指標

[MAP](map.md)使用二元相關性，並對相關項目的精確率取平均。家族概述見[排序指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — API 參考，給出定義、前 $k$ 名選項與範例。
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 說明排序檢索的評估，這是發展折損增益指標的情境。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — 由預測分數計算平均精確率的 API 參考，附階梯式公式。
