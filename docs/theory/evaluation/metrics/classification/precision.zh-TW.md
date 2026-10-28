---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# 精確率

精確率是預測為正例的樣本中，真正為正例的比例。它回答的問題是：模型發出警報時，有多常是對的？

## 定義

$$\text{精確率} = \frac{TP}{TP + FP}$$

當模型沒有預測任何正例時，精確率沒有定義，因為分母為零。

## 解讀

精確率衡量誤報的代價。精確率高的垃圾郵件過濾器，很少把正常郵件放進垃圾信匣。精確率取決於決策門檻：提高門檻通常會減少偽正例、提高精確率，但代價是[召回率](recall.md)下降。

## 何時使用

當採取正例預測的行動代價高或有害時使用精確率，例如交易被攔截、或病人被召回做進一步檢查。應報告實際部署時所用門檻下的精確率，而不是預設值。

## 範例

沿用上述 100 筆案例，分類器共預測 50 個正例。精確率為 $40 / (40 + 10) = 0.80$：被標記的案例中，五分之四是正確的。它不反映被漏掉的 20 個正例。

## 性質與變體

- **範圍與未定義情況。** 精確率介於 $[0, 1]$ 之間。若沒有任何正例預測（$\mathrm{TP} + \mathrm{FP} = 0$），則未定義，需說明採用的約定，例如 `zero_division`。
- **不計入真負例。** 增加正確的負例預測不會改變精確率，因此在負例很多時特別有用。
- **前 $k$ 個精確率。** 在檢索中，前 $k$ 個結果裡相關項目所佔的比例。
- **限制。** 只對最有把握的案例預測為正例的模型，可以有很高的精確率，但召回率很低。

## 常見陷阱

- **門檻依賴。** 單一門檻下的精確率無法代表模型整體。應搭配如 [PR-AUC](pr-auc.md) 之類與門檻無關的指標。
- **稀有正例。** 若預測為正例的樣本很少，精確率很高也可能充滿雜訊。應報告樣本數。

## 相關指標

精確率是 [F1 分數](f1.md)的其中一半，另一半是[召回率](recall.md)。家族概述見[分類指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — API 參考，給出定義 $tp / (tp + fp)$ 及各類別平均的選項。
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 將精確率描述為集合式的檢索指標。

### 補充來源

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。
