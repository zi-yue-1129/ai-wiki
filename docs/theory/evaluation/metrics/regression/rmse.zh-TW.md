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

## 範例

沿用同樣的數值，平方誤差為 $0.25, 0.25, 0, 1$，平均為 $0.375$，開根號後得到 RMSE $\approx 0.61$。RMSE 大於 MAE 的 0.5，因為平方後，單一誤差 1 的權重被放大了。

## 性質與變體

- **最小化者。** 使 RMSE（或等價的 MSE）最小的常數是目標值的平均數。
- **與 MAE 的關係。** 對同一組誤差，RMSE 永遠不小於 MAE，兩者相等僅當所有絕對誤差都相同。
- **變體。** 正規化 RMSE 會除以目標值的範圍或平均，以便跨資料集比較。MSE 是去掉開根號的同一量，處處平滑，因此常作為訓練損失。
- **限制。** 少數大誤差就可能主導數值，因此典型誤差很小時 RMSE 仍可能很差。

## 常見陷阱

- **離群值。** 少數極端誤差就可能主導 RMSE。應檢查誤差分布，而不只是摘要數字。
- **與 MAE 比較。** 同一資料上，RMSE 一定不小於 MAE，因此兩者不能當作同一個量來比較。

## 相關指標

[MAE](mae.md)是線性的對應指標。[R²](r-squared.md)則把誤差與基準相比。家族概述見[迴歸指標](index.md)。

## 參考文獻

### 文章與文件

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — 討論 RMSE 如何把平均誤差與誤差的變異混在一起。
- scikit-learn contributors. *root_mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html — 均方根誤差的 API 參考，包括參數與範例。

### 補充來源

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 分類、迴歸與排序評分器的概述，以及各自的適用時機。
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
- scikit-learn contributors. *mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html — 均方誤差的 API 參考，即 RMSE 的平方形式，附有範例。
