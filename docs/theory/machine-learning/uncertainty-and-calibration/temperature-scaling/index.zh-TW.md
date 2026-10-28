---
translation_reviewed: 2026-10-28
---

# 溫度縮放

溫度縮放是一種訓練後方法，使已訓練分類器的信心與其準確率相符。它把網路的 logit 除以一個學到的單一數值，即溫度。Guo 等人（2017）把它提出，作為[不確定性與校準](../index.md)主題的一部分。

## 概述

現代網路往往過度自信。Guo 等人（2017）回報，現代神經網路校準得很差，並在影像與文件分類上測試了數種訓練後修正方法。他們的摘要把溫度縮放描述為 Platt scaling 的單參數變體，並回報它在多數資料集上能出奇地有效地校準預測。這也是一套簡單的做法。由於此方法只改變分數的尺度，它不會改變哪一類分數最高，因此預測標籤與準確率都保持不變，只有信心改變。

## 關鍵概念

- **Logit。** 網路在 softmax 把它轉為機率之前所產生的原始分數 \(z\)。
- **溫度。** 一個正的純量 \(T\)。大於 1 的值會使分布變平，降低信心；小於 1 的值則使分布變尖。
- **負對數概似（NLL）。** 用來選擇 \(T\) 的損失函數。它是適當評分規則，因此會獎勵誠實的機率。
- **保留集。** 網路在訓練時沒有看過的驗證資料，來自與未來所面對資料相同的分布。

## 運作方式

設 \(\sigma_{\text{SM}}\) 為 softmax。對於輸入 \(x_i\) 與其 logit \(z_i\)，校準後的預測為 \(\sigma_{\text{SM}}(z_i / T)\)。單一參數的選擇方式，是在一個含 \(n\) 個範例、標籤為 \(y_i\) 的驗證集上最小化 NLL：

\[
T^{*} = \arg\min_{T > 0} \; -\sum_{i=1}^{n} \log \sigma_{\text{SM}}\big(z_i / T\big)_{y_i}.
\]

流程如下。

1. 照常訓練網路，然後凍結它。
2. 對保留的驗證集中每個範例計算 logit \(z_i\)，且此驗證集不得與訓練資料重疊。
3. 求出使 NLL 最小的 \(T^{*}\)。這是一維問題，用線搜尋或一般的梯度方法即可。
4. 測試時，在 softmax 之前把每個 logit 向量除以 \(T^{*}\)。除以一個正數會保留分數的順序，因此預測類別不變。

之後再用可靠度圖或 ECE，於另一個測試集上檢查縮放前後的校準情形。

## 結果

Guo 等人（2017）的摘要指出，在所使用的多數影像與文件分類資料集上，溫度縮放在校準預測方面出奇地有效，並為實務情境提供了簡單而直接的做法。同一篇論文也回報，深度、寬度、權重衰減與批次正規化是影響校準的重要因素。確切數字見原論文，本頁未重新執行。

## 限制

- **只有一個全域數值。** 單一 \(T\) 無法修正在類別之間或輸入之間不同的校準偏差。較豐富的映射是存在的，但需要更多驗證資料。
- **同分布假設。** 溫度是在與測試資料相似的資料上擬合的。在資料集偏移下，它可能無法轉移；Ovadia 等人（2019）正是在這種情境下發現傳統的訓練後校準表現不足。
- **依賴 ECE。** 常用的檢查指標 ECE 取決於區間如何劃分，因此指標的小幅變化可能反映的是分箱方式，而非模型本身。
- **沒有新資訊。** 縮放不會讓模型更準確，也無助於辨識它從未見過的輸入。針對這些問題的方法見[深度集成](../deep-ensembles/index.md)與 [MC 丟棄法](../mc-dropout/index.md)頁面。

## 未解問題

- 何時單一溫度就足夠？何時需要每個類別或每個輸入的修正？
- 資料隨時間漂移時，如何在沒有持續新標籤的情況下維持校準？
- 在套用任何訓練後步驟之前，有多少校準問題可以透過訓練中的正則化與正規化選擇來解決？

## 相關連結

溫度縮放是貝氏方法在訓練後的對應做法。[機率方法](../../../probabilistic/index.md)頁面描述了原則性的替代方案，其中不確定性來自參數上的分布。信心應與可靠度相符，這個想法也是人類後設認知研究的對象，如 Fleming 與 Lau（2014）所回顧；見[認知科學](../../../../brain-mind/cognitive-science/index.md)。驗證的實務面，見[評估](../../../../engineering/evaluation/index.md)。

## 參考文獻

### 開創性論文

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. ICML. https://arxiv.org/abs/1706.04599 — 提出溫度縮放，並顯示相較於較早的網路，現代網路校準得很差。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — 比較不同學習器產生校準機率的能力，以及訓練後校準如何改變它們。
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*. https://doi.org/10.1198/016214506000001437 — 提供評分規則的理論，證明以 NLL 擬合溫度的合理性。

### 綜述與教科書

- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — 綜述深度網路中不確定性的來源，以及訓練後與訓練期間的估計方法。
- Hüllermeier, E. & Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://arxiv.org/abs/1910.09457 — 介紹校準與不確定性估計所依賴的概念。
- Fleming, S. M. & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2014.00443 — 回顧測量後設認知的方法，即一個人的信心與其自身準確率的吻合程度。

### 文章與文件

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — 在資料集偏移下對訓練後校準進行基準測試，結果顯示其表現不足。
