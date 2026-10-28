---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# 均方根誤差

均方根誤差（RMSE）是預測值與真實值之差的平方之平均，再取平方根。它與[MAE](mae.md)一樣，與目標值的單位相同，但對大誤差的懲罰更重。

## 定義

$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2}$$

完美的模型得分為 0。取平方根是為了把數值換回目標值的單位。

## 解讀

平方使一個大小為 10 的誤差，其影響等同於一百個大小為 1 的誤差。因此 RMSE 對離群值與稀有的大誤差很敏感。它正是最小平方擬合所最小化的量，這也是它在迴歸訓練與預測中常見的原因。Willmott 與 Matsuura（2005）指出，RMSE 把平均誤差與誤差的變異混在一起，因此 RMSE 很大不一定表示平均誤差很大。

## 何時使用

當大誤差的代價特別高，或假設目標值的誤差大致為高斯分布時，使用 RMSE。若兩者結果不一致，應與 MAE 一起報告，因為兩者的差距顯示了少數大誤差對分數的影響有多大。

## 常見陷阱

- **離群值。** 少數極端誤差就可能主導 RMSE。應檢查誤差分布，而不只是摘要數字。
- **與 MAE 比較。** 同一資料上，RMSE 一定不小於 MAE，因此兩者不能當作同一個量來比較。

## 相關指標

[MAE](mae.md)是線性的對應指標。[R²](r-squared.md)則把誤差與基準相比。家族概述見[迴歸指標](index.md)。

## 參考文獻

### 文章與文件

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — 討論 RMSE 如何把平均誤差與誤差的變異混在一起。
- scikit-learn contributors. *root_mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html — 均方根誤差的 API 參考，包括參數與範例。
