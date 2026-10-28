---
related:
- theory/models/cnn
- theory/paradigms/active
- theory/paradigms/unsupervised/anomaly-detection
- applications/science
aliases:
  - 太空與天文
  - 天文學
  - Astronomy
---

# 太空與天文

天文學產生的資料多到人無法逐一用眼睛檢視：望遠鏡巡天觀測一次就記錄數十億張影像，重力波偵測器持續記錄應變量，太空船則從遙遠的行星傳回影像與遙測資料。機器學習在這個領域已經是常規工具，而在太空作業中，也用於自主控制與追蹤軌道上的物體。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 星系與天體分類 | 對巡天影像使用卷積網路；以公民科學的標註作為訓練資料 | 已相當成熟；Galaxy Zoo 式的群眾標註是重要的資料來源 |
| 系外行星偵測 | 對 Kepler、TESS 光變曲線使用神經網路；凌日訊號分類器 | 在既有資料中找到新行星（Shallue & Vanderburg, 2018） |
| 重力波 | 對偵測器應變資料使用卷積網路，進行即時偵測與參數估計 | 推論速度快；結果以匹配濾波法核對 |
| 暫態與異常 | 異常偵測、結合天文學家回饋的主動學習 | 由專家決定什麼值得關注 |
| 模擬與仿真 | 以神經仿真器取代昂貴的宇宙學與星系形成模擬 | 主要收益是加速 |
| 太空作業 | 星上自主、衛星影像分析、軌道物體追蹤 | 受限於抗輻射的運算資源與通訊延遲 |

## 為什麼天文學是很好的測試場域

- **標註資料稀少。** 天空中多數天體從未被人檢視過，模型必須在標籤很少的情況下運作。
- **物理限制答案。** 尊重已知對稱性或物理定律的模型，比一般用途的模型更能泛化。
- **巡天會改變。** 儀器、濾光片與觀測條件會隨時間改變，造成與其他領域相同的分布偏移問題。
- **結論需要後續驗證。** 宣稱的偵測要靠進一步觀測確認，因此評估有一部分是靠望遠鏡觀測時間完成，而不只是靠測試集。

## 關鍵方法

有三類方法承擔大部分工作；該領域的綜述（Fluke & Jacobs, 2019）說明了這些方法已擴散到多廣的範圍。

- [卷積神經網路](../../theory/models/cnn/index.md)：分類影像，以及光變曲線、重力波應變等一維訊號。
- [主動學習](../../theory/paradigms/active/index.md)：挑選專家下一步該標註哪些天體，讓有限的標註時間發揮最大效用。Astronomaly（Lochner & Bassett, 2021）把它用於異常搜尋。
- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：找出不符合已知天體族群的物件，是多數發現流程的基礎。

## 關聯

AI 在科學上的應用見[科學研究](../science/index.md)。以少量標籤學習的方法見[主動學習](../../theory/paradigms/active/index.md)，儀器與巡天條件之間的偏移見[領域適應](../../theory/paradigms/transfer/domain-adaptation/index.md)。

## 應用

- 在大型巡天中自動分類星系形態，並以群眾標註訓練模型（Dieleman 等人，2015）。
- 從偵測器資料即時偵測重力波事件，以便望遠鏡及早跟進（George & Huerta, 2018）。
- 在既有太空望遠鏡資料中偵測系外行星凌日，包括早期搜尋漏掉的行星（Shallue & Vanderburg, 2018）。

## 開放問題

- 在一個巡天上訓練的模型，如何在不重新標註所有資料的情況下，轉移到下一台儀器？
- 仿真器要驗證到什麼程度，才能在發表的結果中取代完整模擬？
- 由自動化流程做出的發現，該如何認定功勞並確認？
- 當通訊延遲使人無法即時介入時，太空船應擁有多少自主權？

## 參考文獻

### 開創性論文

- Dieleman, S., Willett, K. W. & Dambre, J. (2015). Rotation-invariant convolutional neural networks for galaxy morphology prediction. arXiv. https://arxiv.org/abs/1503.07077 — 顯示卷積網路能以群眾標註的影像預測星系形態，並內建旋轉不變性。
- George, D. & Huerta, E. A. (2018). Deep Learning for real-time gravitational wave detection and parameter estimation: Results with Advanced LIGO data. *Physics Letters B*. https://doi.org/10.1016/j.physletb.2017.12.053 — 報告神經網路能在真實偵測器資料中偵測重力波訊號，速度足以即時發出警報。
- Shallue, C. J. & Vanderburg, A. (2018). Identifying Exoplanets with Deep Learning: A Five-planet Resonant Chain around Kepler-80 and an Eighth Planet around Kepler-90. *The Astronomical Journal*. https://doi.org/10.3847/1538-3881/aa9e09 — 以神經網路分析 Kepler 光變曲線，在既有資料中找出新行星。
- Lochner, M. & Bassett, B. A. (2021). Astronomaly: Personalised active anomaly detection in astronomical data. *Astronomy and Computing*. https://doi.org/10.1016/j.ascom.2021.100481 — 結合異常偵測與主動學習，讓天文學家的回饋引導搜尋方向。

### 綜述與教科書

- Fluke, C. J. & Jacobs, C. (2019). Surveying the reach and maturity of machine learning and artificial intelligence in astronomy. *WIREs Data Mining and Knowledge Discovery*. https://doi.org/10.1002/widm.1349 — 綜述機器學習在天文學各領域的採用情況，以及仍不成熟之處。
