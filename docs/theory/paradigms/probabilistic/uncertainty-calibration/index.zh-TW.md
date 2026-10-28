---
translation_reviewed: 2026-10-28
---

# 不確定性量化與校準

不確定性量化探討模型的預測有多可信，以及如何表示它不知道的部分。校準則探討模型給出的機率是否與實際觀察到的頻率相符。本頁是[機率與貝氏方法](../index.md)的一部分。

## 概述

一個說「90% 有把握」的模型，在以這種把握程度做出的預測中，應該大約有九成是對的。現代神經網路常常無法通過這項檢驗：它們準確，但過度自信。通常會區分兩種不確定性。**偶然性（aleatoric）**不確定性來自資料中的雜訊，無法靠更多資料消除。**認知性（epistemic）**不確定性來自模型缺乏的知識，會隨資料增加而縮小。不確定性方法通常處理其中一種或兩種。

## 關鍵概念

- **校準**：某事件的預測機率與其頻率相符。完美校準的預測者所報告的機率是可靠的，DeGroot 與 Fienberg（1983）為預測者形式化了此概念。
- **適當評分規則**：一種損失函數（例如 Brier 分數），只有在回報真實機率時才會最小化（Brier，1950）。
- **期望校準誤差**：依信心分組後，信心與準確率之間差距的加權平均，定義見[校準指標頁](expected-calibration-error.md)。
- **預測集合**：一組可能的標籤，並保證以某機率包含真實標籤。這是共形預測的輸出。

## 運作方式

方法大致分為三類。**事後校準**在保留的資料上調整已訓練模型的機率。[溫度縮放](temperature-scaling.md)是最簡單的例子，對神經分類器很有效（Guo 等人，2017）。**集成**平均多個以不同隨機性訓練之模型的預測，可同時改善準確率與校準（Lakshminarayanan 等人，2017）。**共形預測**可包裹任何預測器，並在資料的溫和假設下回傳具覆蓋保證的集合（Angelopoulos 與 Bates，2023）。

貝氏方法則表示參數上的分布，而非單一組權重。神經網路通常無法取得精確後驗，因此會使用如 dropout 型的近似推論來估計不確定性（Gal 與 Ghahramani，2016）。

## 主要方法

- [共形預測](conformal-prediction.md)：不依賴分布假設、具覆蓋保證的預測集合。
- [溫度縮放](temperature-scaling.md)：以單一參數重新縮放 logits 以修正過度自信。
- [深度集成](deep-ensembles.md)：獨立訓練多個網路並平均其預測。
- [期望校準誤差](expected-calibration-error.md)：以分箱方式衡量校準偏差。

## 與其他頁面的連結

- [變分推論](../variational-inference/index.md)與[馬可夫鏈蒙地卡羅](../mcmc/index.md)提供完整的後驗近似，是處理認知性不確定性的原則性途徑。
- [機率與統計](../../../math/probability-statistics/index.md)提供評分規則與校準的概念。
- [貝氏深度學習](../index.md)是這些方法使用的更大脈絡。

## 應用

- **醫療 AI**：標記需要人工檢視的預測，此時校準後的機率與覆蓋保證都很重要（Angelopoulos 與 Bates，2023）。
- **安全與決策**：依模型的不確定程度決定何時行動、何時棄權。
- **預測**：回報使用者可以信賴的機率，這需要校準後的輸出。

## 開放問題

- 分布偏移下的校準比同分布的校準困難，多數事後方法假設測試資料與校準資料相似。
- 共形保證是邊際的，而非針對每個輸入條件成立，因此不同子群的覆蓋率可能不同。
- 在實務中可靠地區分偶然性與認知性不確定性仍然困難，而且這種分解取決於所選的模型。

## 參考文獻

### 奠基性論文

- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — 提出 Brier 分數，即機率預測的適當評分規則。
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — 顯示現代網路校準不佳，並以溫度縮放加以修正。
- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. In *Advances in Neural Information Processing Systems* 30. https://proceedings.neurips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html — 提出以深度集成估計預測不確定性的可擴展方法。
- Angelopoulos, A. N. & Bates, S. (2023). Conformal prediction: a gentle introduction. *Foundations and Trends in Machine Learning* 16(4), 494–591. https://doi.org/10.1561/2200000101 — 介紹共形預測及其覆蓋保證。

### 綜述與教科書

- DeGroot, M. H. & Fienberg, S. E. (1983). The comparison and evaluation of forecasters. *The Statistician* 32(1/2), 12–22. https://doi.org/10.2307/2987588 — 定義機率預測的校準，並分解預測分數。
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/gal16.html — 把 dropout 解釋為近似貝氏推論，以估計模型不確定性。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋校準、適當評分規則與貝氏不確定性。
