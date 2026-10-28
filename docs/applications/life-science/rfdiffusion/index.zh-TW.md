---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - RFdiffusion
  - RoseTTAFold Diffusion
---

# RFdiffusion（Watson 等人，2023）

RFdiffusion 以擴散模型設計新的蛋白質骨架。它是把結構預測網路 RoseTTAFold 微調為能去除蛋白質結構雜訊的模型而建成，因此能依簡單的規格生成蛋白質。在[生命科學](../index.md)概覽中，它是設計工具。

## 概況

大多數計算結構工具是預測既有序列的形狀。設計則是反過來：目標是新的骨架，然後找出能摺疊成此骨架的序列。擴散模型在影像與語言上已經成功，但在蛋白質上較難達到同樣的效果，部分原因是骨架幾何與序列和結構之間的關係很複雜（Watson et al., 2022）。

## 問題

RFdiffusion 出現之前已有深度學習設計方法，但預印本認為，一個涵蓋結合子設計、對稱組裝與酵素支架的通用生成框架尚未被描述。它探討的是：建立在結構預測網路之上的擴散模型，能否處理所有這些任務。

## 關鍵概念

- **骨架（backbone）**：蛋白質主鏈原子所構成的鏈，是摺疊結構的骨幹。RFdiffusion 生成的就是這個骨架。
- **去噪**：一個學習得來的逆向過程，以許多小步驟把隨機座標轉換為合理的骨架。
- **條件化**：引導生成的規格，例如目標摺疊、結合表面或對稱性。
- **對稱寡聚體**：數條相同的鏈依某個點群對稱排列，例如三聚體或二十面體殼。

## 核心想法

從一組隨機的骨架座標開始，逐步去噪成合理的骨架，就像影像擴散模型把雜訊轉為圖片一樣。去噪器是 RoseTTAFold，一個經過訓練以預測蛋白質結構的網路，因此已經編碼了蛋白質幾何。預印本以最少的架構改動，把它微調為生成模型，並以設計規格為條件引導結果朝向所選的形狀或功能。

## 演算法

RFdiffusion 遵循[去噪擴散](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)框架（Ho et al., 2020）。前向過程對真實結構加入雜訊，學到的逆向過程則將其去除。生成時從雜訊開始執行逆向過程，並以設計任務為條件：

1. 取樣一個隨機骨架。
2. 以微調後的 RoseTTAFold 網路，依任務條件進行多步去噪。
3. 挑選設計進行實驗測試。預印本挑選了 608 個設計進行特性鑑定。

## 結果

以下結果來自 2022 年的預印本。最終數字應以正式發表於 2023 年 *Nature* 的版本為準。

- **基準測試**：在一個 25 題的基準上，預印本報告 RFdiffusion 解決了 23 題，而 Hallucination 為 15 題，RFjoint inpainting 為 12 題。
- **任務**：預印本報告涵蓋無條件與拓撲受限的單體設計、以介面殘基為條件的蛋白質結合子設計、指定點群對稱的對稱寡聚體、酵素活性位點支架，以及對稱基序支架。
- **實驗**：608 個設計被挑選進行實驗特性鑑定。在其中一組測試的設計中，預印本報告 95 個有 55 個在 10 μM 下顯示出可偵測的結合。

## 限制

- 模型提出設計，但由實驗決定哪些可行。設計品質並無保證。
- 成功率因任務而異。在預印本驗證的二十面體對稱設計中，只有一個經負染電子顯微鏡確認形成了預期的組裝。
- 設計模型建立在 RoseTTAFold 之上，因此其在結構預測上的優點與不足也會延續下來（這是推論，並非論文的結論）。
- 結果來自電腦模擬與實驗室測試。設計的蛋白質能否在細胞或生物體內運作，是另一個問題。

## 相關連結

- [ESM-2 與 ESMFold](../esm/index.md)：只需單一序列即可預測結構的蛋白質語言模型。它們是預測工具，RFdiffusion 則是設計工具。
- [去噪擴散](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)：此方法所建立的一般框架。
- [AlphaFold 2](../alphafold-2.md)：RoseTTAFold 所屬之研究脈絡中的結構預測器。
- 腦與心智：沒有直接關聯。此方法處理的是蛋白質幾何，而非神經資料。

## 應用

- **結合子設計**：生成能與選定目標表面結合的蛋白質，用於研究工具與候選治療藥物。
- **酵素支架**：把酵素的活性位點放在新的骨架上。
- **對稱組裝**：以相同次單元設計可自行組裝的籠狀與環狀結構。

## 開放問題

- 在電腦上看起來良好的設計，經實驗測試後有多常能運作，以及此比率如何隨任務而變。
- 能否可靠地生成包含許多鏈的大型複雜組裝。
- 如何在一個步驟中，把序列設計與功能一併加入骨架生成。

## 參考文獻

### 開創性論文

- Watson et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*. https://doi.org/10.1038/s41586-023-06415-8 — 正式發表的 RFdiffusion 論文，介紹此方法。
- Watson et al. (2022). Broadly applicable and accurate protein design by integrating structure prediction networks and diffusion generative models. *bioRxiv*. https://doi.org/10.1101/2022.12.09.519842 — 上方基準與實驗數字所依據的預印本。
- Baek et al. (2021). Accurate prediction of protein structures and interactions using a three-track neural network. *Science*. https://doi.org/10.1126/science.abj8754 — RoseTTAFold，RFdiffusion 所微調的結構預測網路。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，RoseTTAFold 通常拿來比較的結構預測器。
- Ho et al. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — 此方法所建立的擴散框架。
