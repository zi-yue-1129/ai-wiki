---
translation_reviewed: 2026-11-06
related:
  - theory/models/rnn/index.md
---

# DeepAR

DeepAR 是一種機率預測方法：在許多相關的時間序列上訓練同一個自迴歸循環網路，並為每個未來步輸出完整的預測分布。它是[時間序列預測](index.md)頁面比較的三個代表性方法之一。

## 問題

古典預測方法為每個序列擬合一個模型。這在歷史長而乾淨時可行，但零售商可能需要數千種商品的預測，其中許多商品的銷售紀錄很短或不連續。為每種商品各自建模，無法借用其他商品的資訊。決策也需要的不只是一個數字：備貨計畫取決於需求超過某個水準的可能性，因此預測必須描述其不確定性。

## 核心想法

DeepAR 使用一個由所有序列共享的循環網路。在每個時間步，網路讀入前一個觀測值、該步的共變量（例如日曆特徵），以及辨識序列身分的學習嵌入，更新隱藏狀態，並輸出下一個值的機率分布參數。有三個細節使它能處理真實資料：

- **尺度化。** 每個序列在進入網路前，會除以依其平均水準計算的尺度因子；與尺度有關的輸出之後再乘回去。因此網路學到的是在大小差異很大的序列間共通的模式。
- **來自短序列的訓練視窗。** 訓練視窗可以從序列開始之前的位置起算，未觀測的值以零填補。共變量與嵌入使模型能為歷史很短的新序列產生預測。
- **視窗取樣。** 訓練視窗依尺度因子成比例地抽樣，使大型序列被抽到的次數足以被好好學習。

## 方程式與演算法

設序列 $i$ 在時間 $t$ 的觀測值為 $z_{i,t}$，共變量為 $x_{i,t}$，共享參數為 $\Theta$，隱藏狀態為

$$h_{i,t} = h\big(h_{i,t-1},\, z_{i,t-1},\, x_{i,t},\, \Theta\big),$$

輸出參數為 $\theta_{i,t} = \theta(h_{i,t}, \Theta)$。實值目標使用高斯似然，正整數計數則使用負二項分布。訓練最大化所有序列與所有訓練時間步的對數似然總和：

$$\mathcal{L}(\Theta) = \sum_{i}\sum_{t} \log \ell\big(z_{i,t} \mid \theta_{i,t}\big).$$

由於隱藏狀態是觀測輸入的確定性函數，此目標可以用一般的隨機梯度下降法最佳化。

預測時使用祖先取樣（ancestral sampling）：從預測分布抽出下一個值，把抽出的值回饋為下一個輸入，重複直到預測期結束。每次執行得到一條軌跡。論文的實驗抽取 200 條樣本路徑，分位數則取自這些路徑的經驗分布。

## 結果

摘要報告，相較於最先進方法，在數個真實預測資料集上準確率提升約 15%。論文以分位數式的風險指標評估預測，並且是對每組序列在預測期內的加總計算。具體的各資料集數字應查閱論文的表格，而不應只依賴摘要中的單一數字。

## 限制

- **參數化的不確定性。** 預測分布是高斯或負二項分布。若真實誤差分布的形狀不同，例如重尾或多峰，分位數會失準。
- **取樣成本。** 要得到分布，每次預測都需要許多條依序產生的樣本路徑，比單次確定性計算慢。
- **誤差回饋。** 把取樣值回饋為輸入，會使誤差在長預測期中累積。
- **依賴相關序列。** 其優勢來自跨許多序列學習。單一的長序列從共享模型中獲益，少於一個調校良好的局部模型。

## 關聯

DeepAR 是使用 LSTM 等門控單元的自迴歸[循環網路](../rnn/index.md)。若只需點預測，非遞迴的替代方法是 [N-BEATS](n-beats.md)，以注意力為基礎的替代方法是 [Informer](informer.md)。把預測分布視為對未來的信念，見[機率與貝氏方法](../../paradigms/probabilistic/index.md)頁面。

## 參考文獻

### 開創性論文

- Salinas, D., Flunkert, V. & Gasthaus, J. (2017). *DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks*. arXiv. https://arxiv.org/abs/1704.04110 — 原始論文：具有分布輸出與取樣式預測的全域自迴歸循環網路。
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*, 9(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735 — 提出 LSTM 單元，即原始 DeepAR 網路所用的循環單元。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014 — 為後續方法設定基準的大型預測競賽。

### 綜述與教科書

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — 綜述單步與多步預測的編碼器與解碼器設計。
- Gneiting, T. & Katzfuss, M. (2014). Probabilistic Forecasting. *Annual Review of Statistics and Its Application*, 1, 125–151. https://doi.org/10.1146/annurev-statistics-062713-085831 — 回顧機率預測的評估標準，這正是 DeepAR 所接受的檢驗。
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — 可免費線上閱讀的預測教科書，附有實例。
