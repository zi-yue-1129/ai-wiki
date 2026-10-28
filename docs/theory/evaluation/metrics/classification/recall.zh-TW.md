---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# 召回率

召回率是真正的正例中，被模型找出來的比例。它回答的問題是：所有真實案例中，模型抓到了多少？它也稱為靈敏度或真正例率。

## 定義

$$\text{召回率} = \frac{TP}{TP + FN}$$

當資料中沒有任何真正例時，召回率沒有定義，因為分母為零。

## 解讀

召回率衡量漏報的代價。在疾病篩檢中，召回率高的測試很少讓真正的病例漏網。與精確率一樣，召回率取決於門檻：降低門檻會抓到更多真正例、提高召回率，但也會增加誤報。

## 何時使用

當漏掉正例的代價高時使用召回率，例如疾病篩檢或安全監控。常見做法是先定出應用所需的最低召回率，再報告與之對應的精確率。

## 範例

沿用上述 100 筆案例，實際正例共 60 個，分類器找到其中 40 個。召回率為 $40 / (40 + 20) = 0.67$。它不反映 10 個誤報，那是精確率所衡量的。

## 性質與變體

- **範圍與未定義情況。** 召回率介於 $[0, 1]$ 之間，若沒有實際正例則未定義。它也稱為敏感度或真正例率。
- **不計入真負例。** 與精確率相同，增加正確的負例不會改變它。
- **平凡的最大值。** 把每個案例都預測為正例，召回率就是 1，因此應與精確率或偽正例指標一起報告。
- **變體。** 巨觀召回率先算各類別的召回率再取平均，讓稀有類別與常見類別等權重。

## 常見陷阱

- **平凡的召回率。** 一個把所有樣本都預測為正例的模型，召回率為 1.0，但毫無用處。召回率必須與精確率一起解讀。
- **門檻依賴。** 應報告所用的門檻，或用如 [ROC-AUC](roc-auc.md) 或 [PR-AUC](pr-auc.md) 這類與門檻無關的指標來比較模型。

## 相關指標

召回率與[精確率](precision.md)一起組成 [F1 分數](f1.md)。家族概述見[分類指標](index.md)。

## 參考文獻

### 文章與文件

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 將召回率定義為集合式的指標，並指出靈敏度是它的另一個名稱。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類評分器（包括召回率）的概述與計算方式。

### 補充來源

- scikit-learn contributors. *recall_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — 召回率的 API 參考，給出定義 tp / (tp + fn)。
- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。
