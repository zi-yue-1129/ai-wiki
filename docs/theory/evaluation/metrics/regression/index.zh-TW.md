---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# 迴歸指標

迴歸指標把預測的數值與真實數值相比較。它們的主要差異在於如何處理大誤差，以及是以目標值的尺度解讀，還是相對於某個基準來解讀。選擇其中一個，就是在決定哪一種誤差最重要。

## 問題

給定 \(n\) 個樣本的真實值 \(y_i\) 與預測值 \(\hat y_i\)，指標必須把這些配對轉換為一個數字。這個選擇同時決定三件事：結果的單位、大誤差的計算權重，以及分數是否要與一個簡單的預測器比較。

## 關鍵概念

- **殘差：** 單一樣本的誤差 \(y_i - \hat y_i\)。
- **尺度：** 以目標值單位表示的指標容易解讀，無單位的指標則可以跨目標比較。
- **基準：** 參考的預測器，通常是目標值的平均，無單位分數即與它比較。

## 關鍵方法

### 平均絕對誤差（MAE）

\[
\mathrm{MAE} = \frac{1}{n} \sum_{i=1}^{n} \lvert y_i - \hat y_i \rvert
\]

MAE 以目標值的單位平均誤差的大小，並線性地懲罰大誤差。細節見 [MAE](mae.md) 頁面。

- **結果：** Willmott 與 Matsuura（2005）主張，MAE 比 RMSE 更自然地衡量平均模型誤差，因為 RMSE 把平均誤差與誤差的變異混在一起。
- **限制：** MAE 無法區分少數大誤差與許多中等誤差，也不提供誤差正負號的資訊。

### 均方根誤差（RMSE）

\[
\mathrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat y_i)^2}
\]

RMSE 同樣以目標值的單位表示，但平均前先平方，因此對大誤差的懲罰比 MAE 重。細節見 [RMSE](rmse.md) 頁面。

- **限制：** RMSE 主要由最大的誤差決定，因此一個離群值就可能大幅改變它的值。依二次均值與算術均值的不等式，RMSE 永遠不小於 MAE，且只有在所有絕對誤差都相等時兩者才相等。

### 判定係數（R²）

\[
R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat y_i)^2}{\sum_{i=1}^{n} (y_i - \bar y)^2}, \qquad \bar y = \frac{1}{n} \sum_{i=1}^{n} y_i
\]

R² 把模型的平方誤差與預測平均值的平方誤差相比，1 表示完美擬合，0 表示與平均值預測器相同。細節見 [R²](r-squared.md) 頁面。

- **限制：** 對於比平均值還差的預測，R² 可能為負。當測試目標的分散程度與訓練目標不同時，它可能產生誤導，因為分母會改變。

## 與其他主題的連結

在 MAE 與 RMSE 之間做選擇，也是在選擇訓練所用的損失：平方誤差訓練會把預測拉向平均值，絕對誤差訓練則會把預測拉向中位數。預測機率的指標見[機率指標](../probabilistic/index.md)。

## 開放問題

- 當目標值跨越數個數量級時，如何回報迴歸誤差，因為相對誤差可能才是正確的尺度。
- 指標的選擇應如何依特定應用中誤差的成本而定。

## 參考文獻

### 文章與文件

- Willmott, C. J. & Matsuura, K.（2005）。Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance。*Climate Research* 30，79–82。https://doi.org/10.3354/cr030079 — 主張 MAE 是比 RMSE 更自然的平均模型誤差指標。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 迴歸評分器與其定義的概述。

### 補充來源

- scikit-learn contributors. *mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html — 均方誤差的 API 參考，即 RMSE 的平方形式，附有範例。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — 統計學習的標準教科書，涵蓋其評估方法。
