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

| 指標 | 衡量什麼 | 是否需要固定的標籤決策規則 | 適用時機 |
|---|---|---|---|
| [準確率](accuracy.md) | 正確標籤的比例 | 是 | 類別大致平衡，且每種錯誤代價相同 |
| [精確率](precision.md) | 預測為正例中真正為正例的比例 | 是 | 誤報代價高 |
| [召回率](recall.md) | 真正的正例中被找到的比例 | 是 | 漏報代價高 |
| [F1 分數](f1.md) | 精確率與召回率的調和平均 | 是 | 以一個數字概括正例類別 |
| [ROC-AUC](roc-auc.md) | 正例排在負例之上的程度 | 否 | 不固定門檻，比較模型 |
| [PR-AUC](pr-auc.md) | 各召回率水準下的精確率 | 否 | 正例稀少 |

對**以分數進行二元分類**的模型，調整門檻通常會改變標籤式指標；多類別模型則可能使用 `argmax`，也可能直接輸出類別標籤，因此不一定存在單一數值門檻。報告準確率、精確率、召回率與 F1 時，應一併交代標籤決策規則及適用的門檻。ROC-AUC 與 PR-AUC 彙整跨門檻的分數排序表現，而非選定單一操作點；正例稀少時還須檢查精確率與盛行率。

## 共用的人工 100 筆混淆矩陣範例

[準確率](accuracy.md)、[精確率](precision.md)、[召回率](recall.md)與 [F1](f1.md) 的數值範例都使用**同一組**二元分類混淆矩陣。表格的列代表**實際類別**，欄代表**預測類別**；每個數字都是整數筆數，而非機率。

| 實際類別 | 預測正例 | 預測負例 | 合計 |
|---|---:|---:|---:|
| 正例 | 40 (TP) | 20 (FN) | 60 |
| 負例 | 10 (FP) | 30 (TN) | 40 |
| **合計** | **50** | **50** | **100** |

對這**同一組** 100 筆案例，準確率為 **70/100 = 0.700**、精確率為 **40/50 = 0.800**、召回率為 **40/60 ≈ 0.667**，F1 則為 **80/110 ≈ 0.727**。這是**人工設定的計數範例，不是分類器實測結果**。各指標頁面的動畫另有各自明確標示的人工分數資料或母體參數，**不能將動畫視為這 100 筆案例的後續測量結果**。

## 教學動畫導覽：兩個不同的評估問題

以下兩項**人工數學示例**與詳細指標頁面共用同一組雙語動畫，不是分類器實測結果。

- **盛行率改變會使 ROC 操作點移動嗎？** [ROC／PR 盛行率動畫](roc-auc.md)固定 TPR = 0.80 與 FPR = 0.10，讓正例盛行率從 5% 改變到 60%。ROC 操作點不變，但精確率約從 0.296 增加到 0.923；[PR-AUC](pr-auc.md) 也解釋同一個例子。[GitHub 靜態預覽](../../../../assets/concept-animations/roc-pr-prevalence-still.svg)。
- **應該部署哪個分類門檻？** [Youden J 與預期損失動畫](roc-auc.md)比較六筆人工排名資料的七個決策位置。J 在 k = 2 最大；假設盛行率為 0.40、誤報成本為 1、漏報成本為 5，損失則在 k = 6 最小。若將漏報成本改為 1，最低損失的門檻會回到 k = 2。[GitHub 靜態預覽](../../../../assets/concept-animations/roc-youden-cost-still.svg)。

MkDocs 網站提供鍵盤可操作的播放／暫停；偏好減少動態效果者會看到靜態圖，窄螢幕可聚焦後水平捲動。

## 關聯

分數是否表現得像機率，是另一個問題，見[機率指標](../probabilistic/index.md)。資料切分與分類器驗證的流程，見[評估與驗證](../../../paradigms/supervised/evaluation-and-validation/index.md)。

## 參考文獻

### 綜述與文件

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 說明為什麼在稀有正例上，精確率—召回率曲線比 ROC 曲線更有資訊量。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 標準分類評分器與其定義的參考。
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — 為檢索定義精確率、召回率、F 值與平均精確率，這些定義可延伸至分類。

### 補充來源

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — 說明 ROC 曲線與 AUC 的建構、解讀與常見誤用。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。
