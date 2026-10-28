---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/transformer
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - ViNT
  - Visual Navigation Transformer
  - 視覺導航 Transformer
---

# ViNT：視覺導航的基礎模型

ViNT 由 Shah、Sridhar、Dashora、Stachowicz、Black、Hirose 與 Levine 提出（arXiv 2023），是一個以 Transformer 為基礎、以目標影像進行導航的基礎模型。它在許多既有的導航資料集上訓練，只需少量資料即可調整到新任務；並可搭配擴散模型提出的子目標影像，進行長距離探索。所屬的子主題是 [以視覺目標導航](index.md)。

## 概述

通用的預訓練模型已在許多機器學習問題上發揮作用，因為大型、弱標註的預訓練資料集，使得小型下游資料集也足以應用。ViNT 探討同樣的做法是否適用於導航。作者以一般的目標到達目標，訓練一個 Transformer，使其可以使用任何導航資料集；他們報告，所得模型會出現正向遷移，表現勝過只在單一資料集上訓練的專家模型（Shah et al., 2023）。

此模型不只是單一策略。結合提出子目標影像的擴散模型後，ViNT 可以探索新環境；作者並報告了公里級的導航執行，分別以 GPS 或衛星影像作為引導。

## 問題

導航資料集來自不同的機器人、相機與環境，而且每個資料集都很小。在某一資料集上訓練的策略，很少能在另一個平台上運作。要匯集這些資料，需要一個能吸收異質資料的模型，以及一種只需少量資料即可適應每個新任務的調整方法。

## 核心想法

使用一個 Transformer 讀取一小段觀測歷史與一張目標影像，同時預測目標有多遠，以及一串未來的路點。先在所有資料上訓練，再以小學習率微調整個模型，以適應新任務。若要長距離探索，則由擴散模型取樣子目標影像，並以一個以目標為啟發式的搜尋來選擇。

## 方程式或演算法

架構包含四個主要部分：

1. **編碼器。** 兩個 EfficientNet-B0 編碼器，分別處理目前的觀測及其過去的上下文，以及目標。目標編碼器的輸出與目前的觀測在通道方向堆疊後融合。
2. **Transformer。** 一個只含解碼器的 Transformer，有四層、四個注意力頭，token 維度為 512。模型約有 3,100 萬個參數，論文使用五個過去的畫面作為上下文。
3. **輸出。** 一個輸出頭預測到子目標的時間距離，另一個輸出頭預測五個未來的相對路點。
4. **子目標搜尋。** 一個約有 3.18 億個參數的擴散模型，以 200 步 DDIM 取樣，提出候選子目標影像。ViNT 對每個候選預測其距離，然後由一個以目標為啟發式的類 A* 搜尋，選出下一個子目標。

在調整時，整個模型以 10⁻⁴ 的學習率端到端微調五個 epoch。學習得到的目標 token 可以取代影像目標編碼器，使模型也能接受其他形式的目標，例如 GPS 路點或路線指令。

## 結果

論文主文描述訓練資料為八個機器人平台上的十一個資料集，並給出超過 100 小時的軌跡。論文的其他表格與圖說給出不同的總量，因此確切數量應以論文的資料表為準。在無方向的目標到達任務中，ViNT 在室內與室外分別得分 0.94 與 1.00；同樣的設定下，端到端的行為克隆分別為 0.72 與 0.44，RECON 則為 0.19 與 0.23（Shah et al., 2023, Table 1）。

搭配子目標擴散時，論文報告 GPS 引導的執行距離為 1,270 公尺，衛星影像引導的執行距離為 1,040 公尺，成功率分別為 0.95 與 1.00（Table 2）。在新機器人的零樣本實驗中，ViNT 在 LoCoBot（120 公尺對 60 公尺）、Go 1（45 公尺對 8 公尺）與 Vizbot（110 公尺對 20 公尺）上的覆蓋距離都大於 GNM。在 Clearpath Jackal 上兩者幾乎相等，分別為 438 公尺與 427 公尺（Table 3）。論文指出，微調約一小時的資料即可掌握新環境，成功率約為 80%。

## 限制

- 公里級的結果依賴額外加入的子目標擴散與圖搜尋。這類執行中的成功，是以「未經人工介入而抵達目標」來非正式判定，論文除此之外沒有給出正式定義。
- 論文在不同段落中給出的資料集總量不一致，因此關於資料量的主張應對照論文檢查。
- 影像目標雖然通用，卻不一定是使用者指定目的地最自然的方式。作者提出學習得到的目標 token，以支援其他形式的目標，但報告的實驗都是以影像進行。
- Jackal 的結果顯示，在某些平台上 ViNT 與 GNM 表現大致相同，因此改善並非在所有機器人上都一致。

## 相關連結

- [GNM](gnm.md) 是共享資料的導航模型，ViNT 在它的基礎上以更大的 Transformer 與更多資料加以延伸。
- [ViNG](ving.md) 是較早的圖式方法，ViNT 的子目標選擇與其圖搜尋相似。
- [NoMaD](nomad.md) 使用相關的 Transformer 編碼器與擴散解碼器，並加入目標遮罩以支援探索。
- [Transformer](../../../theory/models/transformer/index.md) 涵蓋 ViNT 所使用的架構。

## 開放問題

- 導航基礎模型能否以相當的資料量，適應差異很大的任務，例如機器人附近的操作。
- 公里級的表現中，有多少來自學習得到的模型，又有多少來自搜尋與擴散提出的子目標。

## 參考文獻

- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — 模型、訓練資料、調整方法與公里級結果的來源。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — ViNT 多資料集訓練所沿用的共享導航模型。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — ViNT 的子目標選擇所延伸的前身圖式方法。
- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — 較晚的擴散式模型，使用相關的 Transformer 編碼器。
- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — ViNT 的子目標搜尋所建立的拓撲記憶。
