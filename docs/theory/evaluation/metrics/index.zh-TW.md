---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
---

# 指標

指標把模型的輸出與正確答案轉換成一個數字。合適的指標取決於這個數字要支持的決定，因此選擇指標本身就是設計的一部分。本區依任務分組。每個家族都有自己的概述頁，每個指標也都有獨立的頁面。

## 家族

| 家族 | 任務 | 指標 |
|---|---|---|
| [分類](classification/index.md) | 預測類別 | [準確率](classification/accuracy.md)、[精確率](classification/precision.md)、[召回率](classification/recall.md)、[F1 分數](classification/f1.md)、[ROC-AUC](classification/roc-auc.md)、[PR-AUC](classification/pr-auc.md) |
| [機率](probabilistic/index.md) | 評判預測的機率 | [對數損失](probabilistic/log-loss.md)、[Brier 分數](probabilistic/brier-score.md)、[校準誤差](probabilistic/calibration-error.md) |
| [迴歸](regression/index.md) | 預測一個數值 | [MAE](regression/mae.md)、[RMSE](regression/rmse.md)、[R²](regression/r-squared.md) |
| [排序](ranking/index.md) | 為一個列表排序 | [NDCG](ranking/ndcg.md)、[MAP](ranking/map.md) |
| [分割](segmentation/index.md) | 預測區域與正確區域的重疊程度 | [IoU](segmentation/iou.md)、[Dice](segmentation/dice.md) |

經典的監督式學習情境，包括資料切分與模型驗證，已在[評估與驗證](../../paradigms/supervised/evaluation-and-validation/index.md)中說明。

## 如何選擇指標

- **從決定出發。** 問問看誤報、漏報、大誤差或排錯的列表各會造成什麼代價，然後選擇能衡量該代價的家族。
- **同時報告一個與門檻無關的指標，以及一個依門檻計算的指標。** ROC-AUC 或 PR-AUC 這類排序指標不依賴單一截斷點；精確率、召回率與 F1 則依賴。若實際會使用某個門檻，兩類都應呈現。
- **直接使用機率時，檢查校準。** 只看排序是不夠的。
- **說明基準線。** 沒有平凡模型的分數作為對照，指標數值的意義有限，例如多數類別的比例或平均預測值。

## 開放問題

指標只是一種代理。它是否符合使用者重視的價值，是應用層面的問題，無法靠公式解決。由於沒有單一指標能涵蓋所有取捨，應同時報告數個指標，並附上它們的定義與門檻。使用這些指標的協定，見[評估協定](../protocols/index.md)。
