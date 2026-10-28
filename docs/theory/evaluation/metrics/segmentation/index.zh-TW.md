---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# 分割指標

分割指標把預測遮罩與參考遮罩逐像素或逐體素地比較。它們衡量的是重疊程度，而不是平均而言類別是否正確，因此當區域的位置與範圍很重要時，這些指標是自然的選擇。

## 主要指標

| 指標 | 衡量什麼 | 範圍 |
|---|---|---|
| [IoU](iou.md) | 預測區域與參考區域的交集除以聯集 | 0 到 1 |
| [Dice](dice.md) | 兩者交集的兩倍除以兩個區域大小的總和 | 0 到 1 |

IoU 與 Dice 都是重疊指標，對單一區域而言排序結果相同，但數值不能互相替換。對於同樣的遮罩，Dice 一定不小於 IoU，因此應說明使用的是哪一種。

## 關聯

在二元遮罩上，Dice 係數與像素標籤上的 [F1 分數](../classification/f1.md)是同一個公式，因此兩者描述的是相同的重疊。重疊指標不說明邊界與參考邊界相距多遠，這就是分割評估常會再加入邊界距離指標的原因。

## 參考文獻

### 文章與文件

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API 參考，將 Jaccard 指數描述為兩個標籤集合的交集大小除以聯集大小。
- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API 參考，給出公式 $2TP / (2TP + FP + FN)$，這與二元遮罩上的 Dice 係數是同一個比率。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 可用於像素標籤比較的分類評分器概述。
