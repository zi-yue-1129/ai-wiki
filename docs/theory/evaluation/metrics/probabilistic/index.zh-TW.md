---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# 機率指標

機率指標評估的是模型回報的機率本身，而不只是它選出的標籤。當機率本身會被使用時（例如作為風險分數、在權衡成本的決策中，或作為另一個系統的輸入），這些指標就很重要。一個能把案例排序得很好的模型，仍可能給出過高或過低的機率，因此這些指標檢驗的是與[分類指標](../classification/index.md)不同的性質。

## 主要指標

| 指標 | 衡量什麼 | 越低或越高越好 |
|---|---|---|
| [對數損失](log-loss.md) | 模型預測的機率下，真實標籤的負對數概似 | 越低越好 |
| [Brier 分數](brier-score.md) | 預測機率與實際結果之間的平均平方差 | 越低越好 |
| [校準誤差](calibration-error.md) | 預測信心與觀察到的頻率之間，依分箱平均的差距 | 越低越好 |

對數損失與 Brier 分數同時獎勵良好的排序與誠實的機率。校準誤差則單獨衡量後者。模型的對數損失可能很好，但在某一段機率範圍內仍然失準，因此將校準誤差與前兩者一起閱讀很有幫助。

## 關聯

區分能力（把類別分開的能力）由 [ROC-AUC](../classification/roc-auc.md) 與 [PR-AUC](../classification/pr-auc.md) 衡量。Guo et al.（2017）指出，現代神經網路常常過度自信，這就是為什麼校準要單獨報告。在擬合校準步驟之前如何切分資料，見[評估協定](../../protocols/index.md)。

## 參考文獻

### 開創性論文

- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — 說明現代神經網路過度自信，並說明溫度縮放可以修正這一點。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — 比較常見分類器的機率校準，以及校準方法的效果。

### 文章與文件

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 使用預測機率的評分器概述。
