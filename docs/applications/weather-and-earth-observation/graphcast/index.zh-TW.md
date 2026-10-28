---
translation_reviewed: 2026-10-28
---

# GraphCast（Lam 等人，2023）

GraphCast 是一個圖神經網路，能預測六小時後的全球天氣。若重複執行，它可產生長達 10 天的預報，並且直接以數十年的再分析資料訓練。它是父頁面[天氣預報與地球觀測](../index.md)介紹的兩種里程碑式方法之一。

## 概述

業務上的中期預報來自數值天氣預報，即在超級電腦上求解大氣的物理方程式。Lam 等人（2023）提出一個問題：從歷史資料學得的模型，能否以極低的成本達到相當的準確度？GraphCast 對確定性預報的回答是肯定的。它能預測數百個天氣變數，作者報告，在他們評估的大多數目標上，它勝過 ECMWF 的高解析度預報（HRES），而 HRES 是他們比較的最準確業務確定性系統。它的架構承襲了學習型模擬器的思路，即以圖網路學習流體與固體的動力學（Sanchez-Gonzalez 等人，2020）。

## 關鍵概念

- **格點與狀態**：大氣以 0.25 度的經緯格點儲存，共 721 乘 1,440 個點。每個點包含 5 個地面變數，以及位於 37 個氣壓層上的 6 個大氣變數。
- **多重網格（multi-mesh）**：由正二十面體經六次細分所建立的圖。其 40,962 個節點在全球幾乎均勻分布，而來自各細分層級的邊，讓資訊既能在局部傳遞，也能跨越長距離。
- **編碼、處理、解碼**：可學習的編碼器把格點上的值映射到網格上，處理器在網格上傳遞訊息，解碼器再把結果映射回格點。

## 運作方式

GraphCast 以兩個連續的狀態為輸入，即當前狀態與六小時前的狀態，並預測下一個狀態。其步驟如下：

1. **編碼。** 一層圖網路層把經標準化（平均為零、變異數為一）的輸入變數，從格點映射到多重網格上。
2. **處理。** 十六層權重不共享的圖網路層，在多重網格上進行可學習的訊息傳遞。
3. **解碼。** 一層把特徵映射回格點，並輸出每個節點的預測 $\hat{Y}_t$。
4. **更新。** 下一個狀態等於當前狀態加上該預測：

$$\hat{X}_{t+1} = X_t + \hat{Y}_t$$

訓練時，最小化的是以垂直層加權、並在 $N$ 個自迴歸步驟上取平均的均方誤差。訓練期間，步數 $N$ 從 1 逐步提高到 12，也就是從六小時到三天。模型以 ERA5 再分析資料中 39 年（1979 至 2017 年）的資料訓練，使用梯度下降與反向傳播，在 32 個 Cloud TPU v4 上訓練約四週。模型有 3,670 萬個參數。一個 10 天的預報相當於 40 個六小時步，在單一 TPU v4 上不到一分鐘即可完成。

## 結果

主要的基準是把 GraphCast 與 HRES 在 2018 年起的保留資料上相比。以 ERA5 作為真值，而 HRES 則與其基於分析的資料集比較，以免其第一步受到懲罰。技術指標是 1,380 個目標（即各變數在各氣壓層上、跨越 10 天預報時效）的均方根誤差（RMSE）。arXiv 預印本報告，GraphCast 在 90.3% 的目標上勝過 HRES，其中有 89.9% 達到顯著差異。[^1] Science 摘要給出四捨五入的 90%。作者亦報告，在 Pangu-Weather 所提出的 252 個目標中，GraphCast 勝過 Pangu-Weather 的比例為 99.2%，並且在 2018 至 2021 年間，其熱帶氣旋路徑誤差的中位數低於 HRES。

## 限制

- **確定性輸出。** GraphCast 只給出一組預報。其均方誤差目標會使長預報時效的輸出在空間上趨於平滑，因而變得模糊。作者把集合預報列為關鍵的下一步。
- **比 HRES 小。** GraphCast 的解析度為 0.25 度、37 個氣壓層、六小時步長，而 HRES 為 0.1 度、137 個層，步長最短可到一小時。作者保留了他們在實際上能夠容納的最大模型。
- **排除的變數。** 總降水量未納入評估，因為 ERA5 的降水資料有已知的偏差。
- **對再分析的依賴。** 訓練與評分都依賴 ERA5，而 ERA5 本身也是由預報模型產生的。

## 開放問題

- 學習型模型能否在不產生單一均方誤差預報所造成模糊的情況下，給出經過校準的機率？後來的 GenCast 等機率模型（Price 等人，2024）即針對此問題。
- 其能力能否延伸到降水與罕見的極端事件？評估只部分涵蓋這些情況。
- 作者預期此方法能隨運算與高解析度資料而擴展。然而，論文中並未測試更高解析度時準確度是否持續提升。

## 參考文獻

### 開創性論文

- Lam, R. 等人（2023）。*Learning skillful medium-range global weather forecasting*。Science。https://doi.org/10.1126/science.adi2336 — GraphCast 原論文，涵蓋模型、訓練，以及與 ECMWF 的 HRES 的比較。
- Sanchez-Gonzalez, A. 等人（2020）。*Learning to Simulate Complex Physics with Graph Networks*。arXiv。https://arxiv.org/abs/2002.09405 — 以訊息傳遞學習流體與固體動力學的圖網路模擬器，是 GraphCast 編碼器－處理器－解碼器的設計來源。
- Keisler, R.（2022）。*Forecasting Global Weather with Graph Neural Networks*。arXiv。https://arxiv.org/abs/2202.07575 — 較早的圖網路全球預報方法，以 ERA5 訓練並與業務模型比較。

### 文章與文件

- Hersbach, H. 等人（2020）。*The ERA5 global reanalysis*。Quarterly Journal of the Royal Meteorological Society。https://doi.org/10.1002/qj.3803 — 說明 ERA5，即 GraphCast 所訓練與評估使用的再分析資料。
- Rasp, S. 等人（2023）。*WeatherBench 2: A benchmark for the next generation of data-driven global weather models*。arXiv。https://arxiv.org/abs/2308.15560 — 資料驅動天氣模型的開放評估框架與基線。
- Bi, K. 等人（2023）。*Accurate medium-range global weather forecasting with 3D neural networks*。Nature。https://doi.org/10.1038/s41586-023-06185-3 — Pangu-Weather 原論文，是同期的學習型預報模型。

[^1]: 90.3% 與 89.9% 的數字取自預印本（arXiv:2212.12794）；已發表的摘要給出四捨五入的 90%。
