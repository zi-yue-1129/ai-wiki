---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# 分類指標

分類指標用來評估輸出為類別標籤或各類別分數的模型。有些指標在單一決策門檻下讀取標籤：準確率、精確率、召回率與 F1。另一些則跨越所有門檻，檢查分數是否把正例排在負例之上：ROC-AUC 與 PR-AUC。兩組指標回答的問題不同，因此模型可能在一組指標上表現很好，在另一組上表現很差。

## 主要指標

| 指標 | 衡量什麼 | 是否需要門檻 | 適用時機 |
|---|---|---|---|
| [準確率](accuracy.md) | 正確標籤的比例 | 是 | 類別大致平衡，且每種錯誤代價相同 |
| [精確率](precision.md) | 預測為正例中真正為正例的比例 | 是 | 誤報代價高 |
| [召回率](recall.md) | 真正的正例中被找到的比例 | 是 | 漏報代價高 |
| [F1 分數](f1.md) | 精確率與召回率的調和平均 | 是 | 以一個數字概括正例類別 |
| [ROC-AUC](roc-auc.md) | 正例排在負例之上的程度 | 否 | 不固定門檻，比較模型 |
| [PR-AUC](pr-auc.md) | 各召回率水準下的精確率 | 否 | 正例稀少 |

依標籤的指標會隨門檻改變，因此報告數字時也要報告門檻。排序指標不依賴單一門檻，但在正例稀少時可能過於樂觀。

## 關聯

分數是否表現得像機率，是另一個問題，見[機率指標](../probabilistic/index.md)。資料切分與分類器驗證的流程，見[評估與驗證](../../../paradigms/supervised/evaluation-and-validation/index.md)。

## 參考文獻

### 綜述與文件

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 標準分類評分器與其定義的參考。
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 為檢索定義精確率、召回率、F 值與平均精確率，這些定義可延伸至分類。
