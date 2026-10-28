---
translation_reviewed: 2026-10-28
---

# Pangu-Weather（Bi 等人，2023）

Pangu-Weather 是一個用於全球中期天氣預報的深度學習系統。它把大氣視為三維的立方體，以一個適應地球幾何的 Transformer 處理，並為數個預報時效各自訓練一個模型。它是父頁面[天氣預報與地球觀測](../index.md)介紹的兩種里程碑式方法之一。

## 概述

數值天氣預報求解離散化的物理方程式，準確但成本高昂。Bi 等人（2023）指出早期 AI 預報器的兩個問題。把大氣視為一疊二維地圖，會捨棄垂直結構；而反覆呼叫同一個模型，則會使誤差逐步累積。Pangu-Weather 同時處理了這兩個問題。它使用跨越各氣壓層的三維網路，並為多個預報時效訓練模型，使所需的模型呼叫次數減少。Nature 論文報告，在再分析資料上，它在所有測試變數上的確定性結果都優於業務上的 ECMWF 整合預報系統（IFS）。

## 關鍵概念

- **三維地球特定 Transformer（3DEST）**：視覺 Transformer 的變體，作用於氣壓層、緯度與經度所構成的立方體，並帶有地球特定的位置偏置。見[視覺 Transformer](../../../theory/models/transformer/vision-transformer/index.md)。
- **移位視窗（shifted windows）**：注意力在局部視窗內計算，視窗在各層之間移動，這是 Swin Transformer 的機制（Liu 等人，2021）。作者把此機制調整到天氣資料上。
- **階層式時間聚合**：為 1、3、6、24 小時等預報時效分別訓練模型。24 小時模型一次呼叫即可涵蓋一天，因此五天的預報只需五次呼叫，而不必對一小時模型呼叫 120 次。
- **氣壓層**：大氣的垂直維度，資料位於從地面向上的固定氣壓面上。

## 運作方式

輸入是 ERA5 再分析資料，網格為 1440 乘 721 個點，解析度為 0.25 度。預印本使用 13 個氣壓層，包含五個高層變數（位勢、比濕、溫度，以及兩個風分量）、四個地面變數（2 公尺溫度、10 公尺風的兩個分量與平均海平面氣壓），以及三個常數遮罩（地形、海陸與土壤類型）。

一個參數為 $\theta$ 的模型 $f$，把時刻 $t$ 的狀態映射到固定預報時效 $\Delta t$ 之後的狀態：

$$\hat{A}_{t+\Delta t} = f(A_t;\, \theta)$$

網路是編碼器－解碼器結構。高層資料與地面資料分別嵌入為兩個立方體，再沿高度維度串接。編碼器區塊降低解析度，解碼器則以對稱方式還原。每個區塊都是一個 3DEST 區塊，即一個視覺 Transformer 區塊，其移位視窗機制與位置偏置都符合地球的幾何。訓練使用約 39 年、自 1979 年起的 ERA5 資料。每個模型訓練 100 個 epoch，使用 192 個 GPU，每個模型約需 15 天。

## 結果

基準是以 ERA5 作為真值，並與業務上的 IFS 及 FourCastNet 比較，指標為緯度加權的均方根誤差（RMSE）與距平相關係數（ACC），涵蓋多個變數與預報時效。arXiv 預印本報告，在單一成員的預報中，5 天的 500 hPa 位勢高度（Z500）RMSE 為 296.7，而 IFS 為 333.7，FourCastNet 為 462.5。[^1] 預印本亦報告，一次預報在單一 GPU 上的推論時間為 1,400 毫秒，比業務上的 IFS 快逾 10,000 倍。Nature 摘要進一步指出，以再分析資料起始時，此模型追蹤熱帶氣旋的準確度高於 ECMWF 的高解析度預報，並且它在集合預報上的表現良好。

## 限制

- **氣旋強度。** 預測的最低氣壓通常比 ERA5 數值高出約 50 hPa，但路徑誤差尚屬合理。預印本部分歸因於訓練資料中缺乏未經偏差校正的氣旋強度資料。
- **訓練未收斂。** 作者指出，100 個 epoch 是他們能使用的最大預算，更多的資料或時間可能會改進準確度。
- **變數有限。** 降水不在預測變數之列，作者把納入更多觀測變數列為未來工作。
- **多個模型。** 階層式聚合需要為每個預報時效各訓練一個模型，這會增加訓練與儲存的成本。

## 開放問題

- 若改用即時觀測作為起始條件，而非這些比較所用的再分析起始條件，相對於 NWP 的優勢是否仍然成立？
- 作者提出三個方向：納入更多觀測變數、加入第四個（時間）維度，以及使用更深或更寬的網路。哪一項能以最少的運算帶來最多的準確度，尚未經過測試。
- 更好的強度預報，可能需要包含未經偏差校正的氣旋觀測、解析度更高的訓練資料。

## 參考文獻

### 開創性論文

- Bi, K. 等人（2023）。*Accurate medium-range global weather forecasting with 3D neural networks*。Nature。https://doi.org/10.1038/s41586-023-06185-3 — 已發表的 Pangu-Weather 論文，介紹三維地球特定 Transformer 與階層式時間聚合。
- Bi, K. 等人（2022）。*Pangu-Weather: A 3D High-Resolution Model for Fast and Accurate Global Weather Forecast*。arXiv。https://arxiv.org/abs/2211.02556 — 預印本，本頁所引用的詳細 RMSE 與時間數字即來自此版本。
- Pathak, J. 等人（2022）。*FourCastNet: A Global Data-driven High-resolution Weather Model using Adaptive Fourier Neural Operators*。arXiv。https://arxiv.org/abs/2202.11214 — Pangu-Weather 比較中的主要 AI 基線，使用傅立葉神經算子。

### 文章與文件

- Liu, Z. 等人（2021）。*Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*。arXiv。https://arxiv.org/abs/2103.14030 — 採用移位視窗注意力的 Transformer，其機制為 3DEST 區塊所改編。
- Hersbach, H. 等人（2020）。*The ERA5 global reanalysis*。Quarterly Journal of the Royal Meteorological Society。https://doi.org/10.1002/qj.3803 — 說明 ERA5，用於訓練與評估的再分析資料。
- Rasp, S. 等人（2023）。*WeatherBench 2: A benchmark for the next generation of data-driven global weather models*。arXiv。https://arxiv.org/abs/2308.15560 — 資料驅動全球天氣模型的開放評估框架與基線。

[^1]: 這些數字取自 arXiv 預印本（arXiv:2211.02556）。已發表的版本數字可能不同，引用前請加以核對。
