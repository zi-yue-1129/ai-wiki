---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# 迴歸指標

迴歸指標把預測的數值與真實數值相比較。它們的主要差異在於如何處理大誤差，以及是以目標值的尺度解讀，還是相對於某個基準來解讀。選擇其中一個，就是在決定哪一種誤差最重要。

## 主要指標

| 指標 | 衡量什麼 | 單位 | 大誤差的處理 |
|---|---|---|---|
| [MAE](mae.md) | 平均絕對誤差 | 與目標值相同 | 線性懲罰 |
| [RMSE](rmse.md) | 平均平方誤差的平方根 | 與目標值相同 | 比 MAE 懲罰更重 |
| [R²](r-squared.md) | 相對於預測平均值所解釋的變異比例 | 無單位 | 透過平方誤差懲罰 |

MAE 與 RMSE 都能以目標值的單位直接解讀。R² 則與常數基準比較，適合用來判斷模型是否真的解釋了什麼；但若測試資料的分散程度與訓練資料不同，它可能會產生誤導。

## 關聯

Willmott 與 Matsuura（2005）主張，在許多情境下 MAE 比 RMSE 更自然地衡量平均誤差，因為 RMSE 把平均誤差與誤差的變異混在一起。預測機率的指標見[機率指標](../probabilistic/index.md)。

## 參考文獻

### 文章與文件

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — 主張 MAE 是比 RMSE 更自然的平均模型誤差指標。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 迴歸評分器與其定義的概述。
