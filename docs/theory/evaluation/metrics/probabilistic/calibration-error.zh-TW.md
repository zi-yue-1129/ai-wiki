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
