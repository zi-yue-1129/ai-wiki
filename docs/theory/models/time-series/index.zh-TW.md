---
translation_reviewed: 2026-11-06
related:
  - theory/models/rnn/index.md
---

# 時間序列預測（Time-Series Forecasting）

時間序列預測根據某個量的過去數值，以及常見的相關變數，預測它未來的數值。電力需求、銷售量、交通流量、氣溫與感測器讀數，都是隨時間觀測到的序列，好的預測能讓規劃者在事件發生前採取行動。這個問題看起來像語言建模，但資料是以固定間隔測得的數字，誤差的代價通常以該量本身的單位計，而預測的不確定性往往與中心值一樣重要。

## 概述

預測是一個函數：輸入過去觀測值的歷史，輸出一個或多個未來步的預測，其中向前預測的步數稱為*預測期（horizon）*。預測可以是給出單一數值的點預測，也可以是給出分布或一組分位數的機率預測。當決策取決於極端值的風險時，就需要機率預測，例如決定要備足多少商品或保留多少電力。Gneiting 與 Katzfuss（2014）回顧了一個好的機率預測應滿足什麼條件，以及如何評估。

評估必須尊重時間順序。模型在過去的資料上訓練，並在之後的期間上測試，測試視窗通常會在許多起點上向前滾動，使結果不依賴某一次幸運的切分。許多機器學習任務慣用的打亂資料順序，會把未來資訊洩漏到訓練中，可能使準確率被高估。當一個方法要應用於許多尺度不同的序列時，誤差也需要共同的尺度。MASE 等比例誤差，以訓練樣本內的單純預測誤差去除誤差，就是為此提出的（Hyndman 與 Koehler，2006）。M4 競賽在 10 萬個序列上比較了 61 種方法，其結果也影響了之後如何評斷方法（Makridakis 等人，2020）。

## 關鍵概念

- **預測期（horizon）**：模型向前預測多遠。多步預測會一次預測數步。
- **平穩性（stationarity）**：統計性質不隨時間改變的序列。許多經典方法假設它，或假設可以透過差分使其平穩。
- **共變量**：在未來已知的變數，例如假日或已規劃的價格，可以改善預測。
- **相關序列**：來自同一領域的許多序列，例如數千種商品的銷售。模型可以跨序列學習。
- **編碼器與解碼器**：模型中讀取歷史的部分，以及產生預測的部分。

## 運作方式

經典方法，例如指數平滑與自迴歸模型，每次只對一個序列擬合少量參數。它們快速、可解釋，並且在短而簡單的序列上很難被超越。深度學習方法則同時從許多序列學習，並能使用許多共變量。Lim 與 Zohren（2020）綜述了用於單步與多步預測的編碼器與解碼器設計，包括循環式、卷積式與注意力式模型。

**機率式自迴歸。** [DeepAR](deepar.md)（Salinas 等人，2017）在大量相關的時間序列上訓練自迴歸循環網路。每一步，網路輸出下一個值的機率分布參數，預測則是一組取樣得到的軌跡。網路在所有序列間共享，並以共變量（例如序列身分的嵌入）為條件，因此歷史很短的序列也能得到預測。

**無遞迴的基底展開。** [N-BEATS](n-beats.md)（Oreshkin 等人，2019）使用由全連接殘差區塊組成的深層堆疊，每個區塊對前面區塊未解釋的部分進行建模。作者提出一般版本與可解釋版本，後者的預測由趨勢與季節成分組成。摘要報告，此設計相較統計基準將預測準確率提升 11%，相較 M4 競賽上一屆冠軍提升 3%。

**以注意力處理長序列。** [Informer](informer.md)（Zhou 等人，2020）把 [Transformer](../transformer/index.md) 改造用於長序列預測。它以稀疏近似取代完整的自注意力，並一次產生整段預測。摘要把問題表述為長期預測需要模型具有高度的預測能力，這促成了更有效率的注意力機制。後來的比較發現，簡單的線性模型在數個基準上可以勝過 Transformer 預測器（Zeng 等人，2022），因此注意力對此任務的價值仍有爭議。

## 關鍵方法

三個代表性方法的簡要比較。每個方法都有自己的頁面，載明問題、核心想法、方程式、結果與限制。

- [**DeepAR**（Salinas 等人，2017）](deepar.md)：共享的自迴歸循環網路，輸出為分布，預測以取樣方式得出。當每個預測的不確定性很重要時是首選，代價是需要逐步取樣。
- [**N-BEATS**（Oreshkin 等人，2019）](n-beats.md)：由全連接區塊組成的殘差堆疊，沒有遞迴或注意力，有一般與可解釋兩個版本。輸出點預測，並在 M 系列競賽基準上表現強勁。
- [**Informer**（Zhou 等人，2020）](informer.md)：為長預測期設計的 Transformer 變體，採用稀疏注意力、縮短層間序列，並以一次通過的解碼器產生預測。它相較於較簡單模型的優勢曾受到質疑。

## 關聯

循環式設計見[循環神經網路](../rnn/index.md)頁面，注意力式設計見 [Transformer](../transformer/index.md) 頁面。狀態空間模型能以線性時間的更新提供長期記憶，見[狀態空間模型](../ssm/index.md)頁面。預測也與機率推理相連，因為機率預測的輸出是對未來的一種信念，見[機率與貝氏方法](../../paradigms/probabilistic/index.md)。

神經記錄同樣是時間序列，因此神經科學中也會出現相同的建模問題。這個連結在 [NeuroAI](../../../brain-mind/neuroai/index.md) 中討論。

## 應用

- **能源。** 預測用電需求與再生能源發電量，以平衡供給。
- **零售與供應鏈。** 預測許多商品的需求，決策是要備多少貨。
- **交通與氣象。** 預測車流與氣象變數，機率預測可支援預警與路線規劃。

## 開放問題

- 深度模型常在大量序列的集合上被評估，在那裡它們最可能受益。它們在小型或雜訊較多的序列上的優勢較不清楚，因此需要仔細解讀基準結果。
- 當過程改變時，分布偏移會使預測失效，而即時偵測這種改變很困難。
- 公平的評估需要保留的期間，以及與新模型同樣仔細調校的基準，但這並非總是做得到。
- 長期預測是否需要注意力式模型，或簡單模型能否與之匹敵，目前仍有爭議（Zeng 等人，2022）。
- 以本身不確定的共變量來結合預測，是一個開放的建模問題。

## 參考文獻

### 開創性論文

- Salinas, D., Flunkert, V. & Gasthaus, J. (2017). *DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks*. arXiv. https://arxiv.org/abs/1704.04110 — 在許多相關序列上訓練自迴歸循環網路，輸出機率預測。
- Oreshkin, B. N., Carpov, D., Chapados, N. & Bengio, Y. (2019). *N-BEATS: Neural basis expansion analysis for interpretable time series forecasting*. arXiv. https://arxiv.org/abs/1905.10437 — 一種深度殘差預測架構，在 M4 基準上報告了進步。
- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2020). *Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting*. arXiv. https://arxiv.org/abs/2012.07436 — 用於長期預測的 Transformer 變體，採用較有效率的注意力機制。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014 — 上述大多數方法所對照的基準競賽。
- Hyndman, R. J. & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001 — 討論可跨序列比較預測的無尺度誤差指標，包括 MASE。

### 綜述與教科書

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — 綜述用於單步與多步預測的編碼器與解碼器設計。
- Gneiting, T. & Katzfuss, M. (2014). Probabilistic Forecasting. *Annual Review of Statistics and Its Application*, 1, 125–151. https://doi.org/10.1146/annurev-statistics-062713-085831 — 回顧一個機率預測應滿足的條件與評估方式。
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — 關於古典與現代預測方法的教科書，可免費線上閱讀。
- Zeng, A., Chen, M., Zhang, L. & Xu, Q. (2022). *Are Transformers Effective for Time Series Forecasting?* arXiv. https://arxiv.org/abs/2205.13504 — 將 Transformer 預測器與簡單線性模型比較，並在九個真實資料集上檢驗注意力在此情境中的必要性。
