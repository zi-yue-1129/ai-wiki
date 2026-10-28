---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# ROC-AUC

ROC-AUC 是接收者操作特徵曲線（ROC 曲線）下的面積。曲線在決策門檻由高到低變動時，描繪真正例率對偽正例率的關係。曲線下面積概括了分數把正例與負例分開的能力，且不需要選定單一門檻。

## 定義

在每個門檻 $t$ 上，真正例率為 $TP/(TP+FN)$，偽正例率為 $FP/(FP+TN)$。ROC 曲線收集這些點，ROC-AUC 就是曲線下的面積。

一個有用的解讀是排序解讀：ROC-AUC 等於隨機選取的一個正例，得到的分數高於隨機選取的一個負例的機率。完美排序得 1.0，隨機分數得 0.5（Fawcett, 2006）。

## 解讀

ROC-AUC 只需要分數，不需要依門檻得出的標籤，因此可以在不固定操作點的情況下比較模型。它取決於分數的排序，而不是分數的校準：模型的 ROC-AUC 可以很高，但機率的尺度可能嚴重失準。見[校準誤差](../probabilistic/calibration-error.md)。

## 何時使用

當操作門檻尚未確定，而且正例與負例的數量相當時，使用 ROC-AUC 比較模型。

## 範例

取四筆有分數的案例：兩個正例分數為 0.9 與 0.6，兩個負例分數為 0.8 與 0.3。共有四組正負配對，其中正例分數較高的有三組（0.9 對 0.8、0.9 對 0.3、0.6 對 0.3），只有一組較低（0.6 對 0.8）。因此 ROC-AUC 為 $3 / 4 = 0.75$。

## 性質與變體

- **機率意義。** ROC-AUC 等於隨機一個正例的分數高於隨機一個負例的機率，分數相同時計為一半。這就是曼–惠特尼 U 統計量除以正負配對數。
- **不變性。** 對分數做任何嚴格遞增的轉換，數值都不變。它也不受盛行率影響，因為 TPR 與 FPR 都是各類別內的比例。
- **部分 AUC。** 只取 FPR 的某一段範圍（例如 0 到 0.1）計算面積，聚焦在低誤報的區域。
- **限制。** 正例稀少時，ROC-AUC 可以很高而精確率很差；它也不衡量校準。

## 常見陷阱

- **稀有正例。** 當負例遠多於正例時，即使有很多誤報，偽正例率仍然很小，因此 ROC-AUC 可能比模型對正例的實際表現看起來更好。Saito 與 Rehmsmeier（2015）指出，在這種情況下精確率—召回率的觀點更有資訊量。遇到稀有事件時，應改用 [PR-AUC](pr-auc.md)。
- **多類別使用。** 在 scikit-learn 中，多類別 ROC-AUC 必須明確設定 `multi_class` 參數為 `'ovr'` 或 `'ovo'`；預設值會引發錯誤。

## 相關指標

[PR-AUC](pr-auc.md)是對應的精確率—召回率版本。家族概述見[分類指標](index.md)。

## 參考文獻

### 開創性論文

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — 說明 ROC 曲線與 AUC 的建構、解讀與常見誤用。
- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — 比較不平衡資料上的 ROC 曲線與精確率—召回率曲線。

### 文章與文件

- scikit-learn contributors. *roc_auc_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html — API 參考，說明如何從預測分數計算 ROC AUC，並包含二元與多類別的用法。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。
