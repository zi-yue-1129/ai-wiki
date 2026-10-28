---
translation_reviewed: 2026-10-28
status: complete
last_reviewed: 2026-10-28
tags:
- neuroscience
- perception
- speech
aliases:
  - 任務最佳化神經網路
  - 聽覺皮層的深度網路模型
  - Task-Optimized Neural Network
  - Kell et al. 2018
---

# 任務最佳化網路模擬聽覺皮層（Kell 等人，2018）

只在語音與音樂任務上訓練的深度網路，能重現人類的聆聽行為，並預測聽覺皮層的反應，其各層大致對應皮層的階層。

本頁是[聽覺系統](../index.md)的一個方法。它是[效能最佳化網路（Yamins 等人，2014）](../../visual-perception/yamins-2014/index.md)的聽覺對應。

## 概述

聽覺皮層的模型應當表現得像聽者，也應當反應得像大腦。Kell 等人（2018）檢驗一個為日常聲音任務而建的網路，能否在不以大腦資料擬合的情況下做到這兩點。網路被訓練辨識語音中的字詞，並為音樂分類類型。接著，它的行為與人類聽者比較，它的內部各層則與皮層的 fMRI 反應比較。

## 問題

人工設計的聽覺皮層模型，例如頻譜時間濾波器模型，能捕捉自然聲音的部分反應，但它們建立在對哪些特徵重要的假設之上。問題在於：從真實任務中學到的特徵，是否能不依賴這些假設而與人類聽覺系統相符，並與皮層各區域的排列相符。

## 核心想法

網路訓練的對象是聽者會做的任務，而非大腦的記錄。它的輸入是類似耳蝸的聲音表示。訓練後，比較學到的特徵與人類及大腦資料，使用的是相同的測試聲音。在前七層共享之後，網路分為字詞分支與類型分支。

## 方程式或演算法

1. **輸入。** 每段 2 秒的片段被轉為耳蝸圖：211 個濾波器，中心頻率涵蓋 30 至 7860 Hz。結果被調整為 256 × 256。
2. **架構。** 網路共 12 層。前七層共享，之後分為兩組各五層的任務專用層，分別負責字詞與類型。
3. **訓練。** 字詞任務是對兩秒片段中字詞的 587 類分類，並混入背景聲，平均訊噪比為 3 dB（聽覺場景與語音嘈雜聲）或 6 dB（音樂）。類型任務是對兩秒音樂片段做 41 類分類，混入四種背景之一，平均訊噪比為 12 dB。
4. **評估。** 對每一層，以線性編碼模型預測對測試聲音的 fMRI 反應，並比較各區域的變異解釋量。


## 結果

- **行為。** 在字詞辨識上，網路在各種背景與訊噪比下的準確率，與 18 位聽者相符（r² = 0.92）。一個簡單的耳蝸圖失真量測解釋的變異少得多（r² = 0.37）。
- **音樂類型。** 準確率大致達到人類水準，錯誤型態與人類的混淆相關。這項任務的差異最大。
- **與大腦的吻合。** 在整個聽覺皮層，訓練後的網路解釋了 165 段自然聲音在 8 位受試者中 fMRI 反應變異的 69.9%。頻譜濾波器基準解釋了 55.1%。同樣架構但權重隨機的網路，表現比兩者都差。
- **階層。** 初級（音調拓撲）皮層最適合由中間層預測。核心之外，較深的層給出最佳預測；但對音高與音樂有選擇性的體素，中間層與深層的預測效果大致相當。

## 限制

- **吻合不完整。** 類型任務上網路與人類聽者的差異最大，雖然網路大致達到人類的表現水準。
- **未解釋的變異。** 網路沒有解釋所有可靠的體素變異。該模型是前饋的，沒有遞迴或回饋。
- **對靈長類排列的證據薄弱。** 資料並未清楚顯示非人類靈長類所見的三階段核心、帶狀與副帶狀階層。
- **學習方式。** 每項任務使用約二百五十萬筆有標籤的片段，遠多於聽者學習字詞所需，且訓練程序並非生物學習的模型。
- **測量。** fMRI 的時間解析度有限，而模型沒有真實的時間動態或行為狀態。

## 連結

- **視覺對應**：同樣的邏輯，即以任務訓練的網路與皮層比較，最先是在視覺上檢驗的。見[效能最佳化網路（Yamins 等人，2014）](../../visual-perception/yamins-2014/index.md)。
- **基準**：與它比較的頻譜時間模型，是本主題的另一個方法。見[多解析度頻譜時間模型（Chi 等人，2005）](../chi-2005/index.md)。
- **NeuroAI**：任務最佳化範式中的聽覺一列，見[NeuroAI](../../neuroai/index.md)頁面。
- **語音**：字詞任務連結到[語音與音訊](../../../theory/models/speech/index.md)中的語音模型，以及[Hickok 與 Poeppel 的雙路徑模型](../../language-in-brain/hickok-poeppel-2007/index.md)中的皮層語音路徑。

## 應用

- **檢驗聽覺假說**：研究者可以探問哪些任務會產生特定的皮層排列，以及哪些特徵是符合人類錯誤所必需的。
- **以任務為本的解釋**：網路的字詞辨識行為在各種條件下與人類聽者吻合（r² = 0.92），但並未以人類資料訓練。這支持部分聆聽行為源自任務本身的觀點，但這仍是需要進一步檢驗的研究主張。

## 開放問題

- **哪些任務？** Kell 等人（2018）只用了兩項任務。若改用聲源定位或說話者辨識等其他任務，是否會改變與皮層相符的層，目前不得而知。
- **回饋與注意力。** 前饋設計缺少回饋與注意力，這或許能解釋未被解釋的變異。
- **訓練資料。** 類型判斷的落差顯示，部分人類判斷依賴訓練資料未包含的經驗。

## 參考文獻

### 開創性論文

- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H.（2018）。A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*, 98(3), 630–644。https://doi.org/10.1016/j.neuron.2018.03.044 — 原始論文。在字詞與類型任務上訓練網路，並與人類行為及聽覺皮層 fMRI 比較。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J.（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex. *Proceedings of the National Academy of Sciences*, 111(23), 8619–8624。https://doi.org/10.1073/pnas.1403112111 — 任務最佳化方法的視覺前身，能預測高階視覺皮層的神經反應。
- Chi, T., Ru, P. & Shamma, S. A.（2005）。Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*, 118(2), 887–906。https://doi.org/10.1121/1.1945807 — 本研究用來與網路比較的頻譜時間基準，提出頻譜與時間特徵的統一多解析度表示。

### 綜述與教科書

- Hickok, G. & Poeppel, D.（2007）。The cortical organization of speech processing. *Nature Reviews Neuroscience*, 8(5), 393–402。https://doi.org/10.1038/nrn2113 — 語音處理的雙路徑模型，是本文語音分支可能相符之皮層語音路徑的背景。
- Robles, L. & Ruggero, M. A.（2001）。Mechanics of the mammalian cochlea. *Physiological Reviews*。https://doi.org/10.1152/physrev.2001.81.3.1305 — 綜述耳蝸力學：行進波、音調的位置編碼與外毛細胞放大，是類耳蝸輸入的生物學背景。
- Rauschecker, J. P. & Scott, S. K.（2009）。Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*。https://doi.org/10.1038/nn.2331 — 綜述聽覺皮層中的圖與路徑，參照靈長類研究，並討論其對人類語音處理的意義。
