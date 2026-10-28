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

## 常見陷阱

- **門檻依賴。** 單一門檻下的精確率無法代表模型整體。應搭配如 [PR-AUC](pr-auc.md) 之類與門檻無關的指標。
- **稀有正例。** 若預測為正例的樣本很少，精確率很高也可能充滿雜訊。應報告樣本數。

## 相關指標

精確率是 [F1 分數](f1.md)的其中一半，另一半是[召回率](recall.md)。家族概述見[分類指標](index.md)。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — API 參考，給出定義 $tp / (tp + fp)$ 及各類別平均的選項。
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 將精確率描述為集合式的檢索指標。
