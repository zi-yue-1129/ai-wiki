---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# 校準誤差

校準誤差衡量預測的信心是否與觀察到的頻率相符。一個校準良好的模型，若預測機率為 0.8，那麼它大約有 80% 的時候是對的。校準只取決於機率本身，與模型把案例排序得多好是分開的。

## 定義

依信心把預測分成 $M$ 個分箱（bin）。對每個分箱 $B_m$，比較平均預測信心與觀察到的正例比例。期望校準誤差（expected calibration error, ECE）是它們的加權平均：

$$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

其中 $\text{acc}(B_m)$ 是分箱 $m$ 中觀察到的正例比例，$\text{conf}(B_m)$ 是該分箱中平均的預測機率。Naeini et al.（2015）發展了這類以分箱為基礎的估計方法。結果取決於使用的分箱數，因此必須報告分箱數。

## 解讀

ECE 接近零，表示信心平均而言接近觀察到的頻率。ECE 無法指出是哪一段信心範圍出了問題；可靠性圖（reliability diagram）會依分箱畫出觀察頻率對信心的關係，才能看出來。現代深度網路常常過度自信，這會拉高 ECE（Guo et al., 2017）。

## 何時使用

當機率被用於決策、呈現給使用者，或傳給另一個系統，而問題是這些數字是否真的代表它們所說的意思時，使用校準誤差。

## 範例

沿用同樣四個預測，使用兩個等寬的分箱。兩個分箱對真實評估來說太少，這裡只是為了示範計算。分箱 $[0, 0.5)$ 有一個案例，平均信心 0.30，觀察到的正例比例為 0。分箱 $[0.5, 1]$ 有三個案例，平均信心 0.77，觀察到的正例比例為 0.67。ECE 為 $\tfrac{1}{4} \cdot 0.30 + \tfrac{3}{4} \cdot 0.10 = 0.15$。

## 性質與變體

- **定義。** ECE 為 $\sum_m \frac{|B_m|}{n}\,\left|\mathrm{acc}(B_m) - \mathrm{conf}(B_m)\right|$，即各分箱 $B_m$ 中信心與準確率差距的加權平均。變體包括取各分箱中的最大差距（最大校準誤差），或多類別時按類別計算。
- **分箱。** 等寬分箱最簡單。等量（自適應）分箱讓每箱案例數大致相同，在預測值集中的地方估計較穩定。
- **平凡的校準。** 永遠輸出盛行率的常數預測器，在母體上的 ECE 為零，但它完全沒有排序案例的能力。讀 ECE 時應搭配 ROC-AUC 或對數損失等區辨指標。
- **限制。** 分箱很小時估計有偏差，且數值依分箱數而變。

## 常見陷阱

- **分箱選擇。** 等寬分箱對分箱數與稀疏的範圍很敏感。應報告分箱數與分箱方式。
- **小樣本。** 樣本少的分箱估計很嘈雜。應顯示每個分箱的樣本數。
- **校準不等於準確。** 校準良好的模型仍可能是很差的分類器。應同時參考 [ROC-AUC](../classification/roc-auc.md) 或 [PR-AUC](../classification/pr-auc.md)。

## 關聯

溫度縮放是針對過度自信網路的單參數修正方法，Guo et al.（2017）有相關描述。它通常在保留的驗證集上擬合，然後在測試集上衡量校準誤差。家族概述見[機率指標](index.md)。

## 參考文獻

### 開創性論文

- Naeini, M. P., Cooper, G. & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence* 29(1). https://ojs.aaai.org/index.php/AAAI/article/view/9602 — 發展以分箱為基礎的估計方法，用來衡量模型機率的校準程度。
- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — 說明現代網路過度自信，並說明溫度縮放可以修正這一點。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — 比較常見分類器的機率校準，以及校準方法的效果。

### 文章與文件

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 與校準檢查一起使用的機率評分器概述。

### 補充來源

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — 提供免費線上草稿的機率機器學習教科書。
