---
translation_reviewed: 2026-10-28
---

# DeepAR（Salinas 等人，2020）

DeepAR 是一種循環預測模型，會同時在許多相關的時間序列上訓練。對每個未來數值，它輸出的是一個機率分布，而非單一數字，因此適合用於決定庫存。它是父頁面[物流與供應鏈](../index.md)所介紹的方法之一。

## 概述

指數平滑等古典方法通常一次只擬合一條序列。零售商則有許多品項在許多地點銷售，其中很多序列起伏劇烈或具間歇性，而新產品的歷史資料又很少。DeepAR 探討的問題是：能否以一個同時在所有序列上訓練的模型，學到它們共同的結構，並產生準確的機率預測。論文報告指出它做得到，並且預測範圍內的不確定性成長是從資料中學得的，而非假設為線性。

## 關鍵概念

- **全域模型**：所有序列共用同一組參數。
- **自回歸**：在每一步，模型都以前一個觀測值作為輸入。
- **循環狀態**：一個 [LSTM](../../../theory/models/rnn/gated-cells/lstm/index.md) 隱藏狀態，把已觀測的過去帶入預測期間。
- **似然**：每一步由網路輸出的分布。論文對實數資料使用高斯分布，對計數資料使用負二項分布。
- **祖先抽樣**：把每個抽樣值回饋進網路，從而抽出完整的未來路徑，使分位數可以被估計。
- **ρ 風險**：評估時使用的分位數損失。

## 運作方式

令 $z_{i,t}$ 為序列 $i$ 在時間 $t$ 的值，$x_{i,t}$ 為其共變量。給定已觀測的過去，序列的未來被分解為若干似然項：

$$
Q_\Theta(z_{i,t_0:T} \mid z_{i,1:t_0-1}, x_{i,1:T}) = \prod_{t=t_0}^{T} \ell\big(z_{i,t} \mid \theta(h_{i,t}, \Theta)\big), \qquad h_{i,t} = h(h_{i,t-1}, z_{i,t-1}, x_{i,t}, \Theta),
$$

其中 $h$ 是多層 LSTM，$\theta$ 由其輸出產生。若採用高斯分布，平均數是 $h_{i,t}$ 的仿射函數，標準差則經過 softplus 以保持為正。編碼器與解碼器共用權重。

1. **縮放。**將每條序列除以其在已觀測範圍內的平均值，使規模差異很大的序列能共用同一個網路。輸出時再乘回去。
2. **訓練。**把每條序列切成視窗，並最大化已觀測值的對數似然，訓練時以已觀測值回饋作為輸入。
3. **加權抽樣。**以與序列規模成正比的機率選取視窗。論文的消融實驗顯示，移除縮放與這種加權抽樣會降低準確度。
4. **預測。**先跑過已觀測範圍，再透過祖先抽樣抽出許多樣本路徑，並計算所需的分位數或總和。

## 結果

在零件資料集（每月汽車零件銷售）與兩個 Amazon 每週銷售資料集上，論文報告 DeepAR 的表現顯著優於所比較的方法。使用高斯似然的變體在計數資料上明顯較差，這支持了採用負二項分布的選擇（Salinas 等人，2020）。在電力與交通資料上，DeepAR 的標準化偏差為 0.07 與 0.17，而矩陣分解基線為 0.16 與 0.20。[^1]

## 限制

- **依賴彙整。**增益來自於跨許多序列的學習。擁有少數長序列的公司，或面對新產品的公司，獲益較少。
- **雜訊模型。**預測的好壞取決於所選的似然，其他類型的資料需要其他的似然。
- **共變量。**促銷、供應商故障與其他造成需求變化的原因，必須以共變量的形式提供。
- **抽樣成本。**分位數來自許多樣本路徑，雖然論文報告預測速度很快。
- **時代性。**這些實驗早於 Temporal Fusion Transformer 等以 Transformer 為基礎的預測器（Lim 等人，2019）。

## 開放問題

- 機率評分的改善，能否降低缺貨與持有成本？論文衡量的是預測準確度，而非庫存結果。
- 循環式全域模型與以 Transformer 為基礎的模型，在相同的零售資料上表現如何比較？
- 能否以[共形預測](../../../theory/machine-learning/uncertainty-and-calibration/conformal-prediction/index.md)重新校準這些分布，以保證涵蓋率？

[^1]: 數據來自 Salinas 等人（2020）的表 2。同一篇論文的 arXiv 摘要（arXiv:1704.04110）將相對於最先進方法的增益總結為約 15%。

## 參考文獻

### 開創性論文

- Salinas, D. et al. (2020). DeepAR: probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2019.07.001 — 在許多相關序列上訓練一個循環模型，以輸出完整的預測分布，並在零售與公開的能源和交通資料上測試。
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — 提出 DeepAR 所用循環狀態的 LSTM 單元。
- Lim, B. et al. (2019). Temporal fusion transformers for interpretable multi-horizon time series forecasting. arXiv. https://arxiv.org/abs/1912.09363 — 以 Transformer 為基礎的多期預測器，結合靜態共變量、已知的未來輸入與歷史序列。

### 綜述與教科書

- Petropoulos, F. et al. (2020). Forecasting: theory and practice. arXiv. https://arxiv.org/abs/2012.03854 — 對跨領域預測方法的非系統性回顧，從古典統計到機器學習。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: results, findings, and conclusions. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2021.11.013 — 報告大型的階層式零售預測基準測試，其中比較了許多方法。
