# 天氣預報與地球觀測

天氣預報是機器學習在科學中最明確的成功案例之一。在許多中期預報指標上，學習式模型已經追平或超越以物理為基礎的預報，而所需運算只是一小部分。地球觀測則把類似的模型應用於衛星與其他遙測資料，用來製作土地、災害與經濟活動的地圖。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 中期全球預報 | GraphCast（圖神經網路）；Pangu-Weather（帶有地球特定先驗的三維 Transformer）；FourCastNet（自適應傅立葉神經算子） | 在 GPU 上只需數秒到數分鐘；數值模式仍是物理基準 |
| 地球系統基礎模型 | Aurora（Bodnar et al., 2025） | 在多樣的地球資料上預訓練，再適應多項預報任務 |
| 評估 | WeatherBench 2（Rasp et al., 2023） | 為學習式模型與數值模式提供共同的評分方式 |
| 衛星與遙測 | 影像的卷積與 Transformer 分割 | 土地覆蓋、洪水與火災製圖 |
| 由影像進行社經製圖 | 將影像特徵轉移，用以預測資產財富 | Jean et al.（2016） |
| 與氣候相關的機器學習 | 涵蓋預報與監測應用的綜述 | Rolnick et al.（2022） |

## 運作方式

數值天氣預報在網格上求解大氣物理方程，並以目前狀態的估計為起點。學習式模型通常以數十年的再分析資料訓練。再分析資料是把觀測與數值模式結合起來，對過去天氣的重建。給定目前的狀態，模型預測數小時後的狀態，並以自我迴歸的方式逐步推進，得到數天後的預報。

## 為什麼困難

- **極端事件**：颶風、熱浪與大氣河等事件在訓練紀錄中很罕見，模型可能低估其強度。
- **繼承偏誤**：再分析資料由數值模式產生，學習式模型可能吸收其中的誤差。
- **物理一致性**：模型可能平均上準確，卻違反守恆律，而這對下游應用很重要。
- **觀測稀疏**：許多地區與感測器的量測很少，限制了訓練與檢驗。

## 關鍵方法

- [圖神經網路](../../theory/models/gnn/index.md)：GraphCast 在覆蓋全球的網格上運作，在相鄰格點之間傳遞訊息。一般形式見[訊息傳遞](../../theory/models/gnn/message-passing/index.md)。
- [卷積網路與 U-Net](../../theory/models/cnn/unet/index.md)：分割衛星影像的標準架構，例如洪水或燒毀範圍地圖。
- [電腦視覺](../../theory/models/computer-vision/index.md)：遙測背後的影像任務，從分類到偵測。
- [領域適應](../../theory/paradigms/transfer/domain-adaptation/index.md)：當在某一感測器、地區或氣候下訓練的模型，必須用於另一種情況時需要。

## 相關連結

- 氣候減緩與能源見[氣候與能源](../climate-energy/index.md)。本頁談的是預報與觀測，該頁也會用到這些技術。
- AI 在科學預測中的更廣泛角色，包括對物理模擬器的代理模型，見[科學發現](../science/index.md)。

## 應用

- 業務化的中期預報與臨近預報
- 以衛星監測洪水、野火、乾旱與作物狀況（見[農業與食品](../agriculture/index.md)）
- 由影像估計貧窮與基礎建設
- 早期預警與災害應變

## 風險與限制

- **驗證缺口**：基準分數可能掩蓋模型在罕見而影響重大的事件上的表現不佳。
- **營運信任**：預報員需要知道學習式模型何時可能失效。
- **資料取得與公平**：各國的觀測覆蓋率並不均勻。
- **依賴性**：若預報來自少數幾個學習式模型，它們的錯誤可能彼此相關。

## 開放問題

- 學習式模型能否可靠地預報從未見過的極端事件。
- 如何在營運系統中結合資料驅動與以物理為基礎的預報。

## 參考文獻

### 開創性論文

- Lam, R. et al. (2023). Learning skillful medium-range global weather forecasting. *Science*. https://doi.org/10.1126/science.adi2336 — 介紹 GraphCast，一種圖神經網路，在許多中期預報指標上超越領先的數值預報。
- Bi, K. et al. (2023). Accurate medium-range global weather forecasting with 3D neural networks. *Nature*. https://doi.org/10.1038/s41586-023-06185-3 — 介紹 Pangu-Weather，一種帶有地球特定先驗的三維網路，用於中期預報。
- Pathak, J. et al. (2022). FourCastNet: A Global Data-driven High-resolution Weather Model using Adaptive Fourier Neural Operators. arXiv. https://arxiv.org/abs/2202.11214 — 以傅立葉神經算子在高空間解析度下進行的全球資料驅動預報模型。
- Ronneberger, O., Fischer, P. & Brox, T. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. arXiv. https://arxiv.org/abs/1505.04597 — 廣泛用於稠密分割（包括衛星影像）的編碼器–解碼器架構。
- Jean, N. et al. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*. https://doi.org/10.1126/science.aaf7894 — 利用從白天衛星影像學到的特徵，預測多個非洲國家的家戶財富。

### 綜述與教科書

- Schultz, M. G. et al. (2021). Can deep learning beat numerical weather prediction? *Philosophical Transactions of the Royal Society A*. https://doi.org/10.1098/rsta.2020.0097 — 檢視學習式模型相對於數值預報目前能做與不能做的事。
- Rolnick, D. et al. (2022). Tackling Climate Change with Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3485128 — 綜述機器學習在預報、監測與減緩上的應用，並討論其限制。
- Rasp, S. et al. (2023). WeatherBench 2: A benchmark for the next generation of data-driven global weather models. arXiv. https://arxiv.org/abs/2308.15560 — 比較學習式與數值天氣模型的共同評估框架。

### 文章與文件

- Bodnar, C. et al. (2025). A foundation model for the Earth system. *Nature*. https://doi.org/10.1038/s41586-025-09005-y — Aurora，在多樣的地球系統資料上預訓練，並適應多項預報任務的模型。
