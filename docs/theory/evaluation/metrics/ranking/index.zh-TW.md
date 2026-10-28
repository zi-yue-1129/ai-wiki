---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# 排序指標

排序指標用來評估一個有順序的列表。它們用於搜尋、推薦與檢索，問題是最相關的項目是否排在最前面。準確率等指標忽略順序，因此無法分辨同樣的項目組成，排序的好壞。

## 問題

系統針對一個查詢回傳一串項目，每個項目都有相關性判斷，可以是二元或分級的。有用的排序指標應獎勵把相關項目放在靠前的位置，對排在較後面的相關性給予較少的分數，並且能在多個查詢間取平均。精確率與召回率這類集合式指標忽略位置，因此必須先加以延伸，才能用來評估排序。

## 關鍵概念

- **相關性標籤：** 每個項目的二元判斷（相關或不相關），或分級分數。
- **截斷值 \(k\)：** 被評分的最前面幾個位置。指標常以固定的截斷值回報，例如 \(k = 10\)。
- **位置折損：** 隨排名下降的權重，因此排在第 1 名的相關項目，比排在第 10 名的同一項目更有價值。
- **正規化：** 除以理想排序的值，使完美的列表得 1 分，並讓不同查詢的分數可以比較。

## 關鍵方法

### 正規化折損累積增益（NDCG）

NDCG 使用分級相關性與對數位置折損。截斷值為 \(k\) 時，折損累積增益為

\[
\mathrm{DCG}_k = \sum_{i=1}^{k} \frac{g(\mathrm{rel}_i)}{\log_2(i+1)},
\]

其中 \(\mathrm{rel}_i\) 是排名第 \(i\) 的項目的等級，\(g\) 是隨等級增加的增益函數。實作中常用 \(g(r) = 2^r - 1\)。NDCG 再除以理想排序的 DCG，即 \(\mathrm{IDCG}_k\)，因此 \(\mathrm{NDCG}_k = \mathrm{DCG}_k / \mathrm{IDCG}_k\) 介於 0 與 1 之間。Järvelin 與 Kekäläinen（2002）提出了具有這類折損的累積增益指標。細節見 [NDCG](ndcg.md) 頁面。

- **結果：** Wang 等人（2013）分析 NDCG 類指標的理論性質，包括它們所用的位置折損。
- **限制：** NDCG 取決於增益、折損與截斷值的選擇，也取決於理想排序，而理想排序需要所有相關項目的判斷。

### 平均精確率均值（MAP）

對二元相關性，單一查詢的平均精確率為

\[
\mathrm{AP} = \frac{1}{R} \sum_{k} P(k)\, \mathrm{rel}(k),
\]

其中 \(P(k)\) 是排名 \(k\) 處的精確率，若排名 \(k\) 的項目相關則 \(\mathrm{rel}(k) = 1\)，否則為 0，\(R\) 是相關項目的數量。MAP 是各查詢 AP 的平均。Manning、Raghavan 與 Schütze（2008）為排序檢索定義了這些度量。細節見 [MAP](map.md) 頁面。

- **結果：** MAP 是資訊檢索基準中的標準摘要，相關性通常以是或否判斷。
- **限制：** MAP 忽略分級相關性。對所有查詢取平均時，每個查詢的權重相同，不論其相關項目數量多寡。

## 與其他主題的連結

作為 MAP 基礎的每個查詢平均精確率，與[分類指標](../classification/index.md)中的精確率—召回率指標密切相關。排序指標是分類分數在列表層級的對應，同一個列表可以用任一類指標評分。

## 開放問題

- 哪一種增益與折損最符合使用者的閱讀方式，模型比較對這個選擇有多敏感？
- 指標應如何處理從未被判斷的項目，這在大型檢索集合中很常見？

## 參考文獻

### 奠基性論文

- Järvelin, K. 與 Kekäläinen, J.（2002）。Cumulated gain-based evaluation of IR techniques。*ACM Transactions on Information Systems* 20(4)，422–446。https://doi.org/10.1145/582415.582418 — 提出帶有位置折損的累積增益指標，是 NDCG 的基礎。
- Wang, Y., Wang, L., Li, Y., He, D., Chen, W. 與 Liu, T.-Y.（2013）。A theoretical analysis of NDCG type ranking measures。COLT 2013，PMLR 30。https://proceedings.mlr.press/v30/Wang13.html — 對 NDCG 類排序指標及其位置折損的理論分析。

### 綜述與教科書

- Manning, C. D., Raghavan, P. 與 Schütze, H.（2008）。*Evaluation of ranked retrieval results*，*Introduction to Information Retrieval* 線上版。https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 為排序列表定義平均精確率，並說明用來比較排序的檢索指標。

### 文章與文件

- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — 正規化折損累積增益的 API 參考，附有範例。
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — 由預測分數計算平均精確率的 API 參考。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述。
