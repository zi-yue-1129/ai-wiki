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

## 常見陷阱

- **平凡的召回率。** 一個把所有樣本都預測為正例的模型，召回率為 1.0，但毫無用處。召回率必須與精確率一起解讀。
- **門檻依賴。** 應報告所用的門檻，或用如 [ROC-AUC](roc-auc.md) 或 [PR-AUC](pr-auc.md) 這類與門檻無關的指標來比較模型。

## 相關指標

召回率與[精確率](precision.md)一起組成 [F1 分數](f1.md)。家族概述見[分類指標](index.md)。

## 參考文獻

### 文章與文件

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 將召回率定義為集合式的指標，並指出靈敏度是它的另一個名稱。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類評分器（包括召回率）的概述與計算方式。
