---
translation_reviewed: 2026-10-28
---

# 量化

量化以位元數較少的數字儲存與運算，例如 8 位元整數、4 位元整數或 8 位元浮點數，取代 16 或 32 位元的浮點數。它是部署最廣泛的[模型壓縮](../index.md)形式，因為它能減少記憶體用量，並且在為低精度設計的硬體上，常能加快矩陣乘法。

## 概述

均勻仿射量化把實數 \(x\) 映射為 \(b\) 位元整數 \(q\)：

\[
q = \operatorname{clip}\!\left(\operatorname{round}\!\left(\frac{x}{s}\right) + z,\ 0,\ 2^b - 1\right), \qquad \hat{x} = s\,(q - z)
\]

其中 \(s\) 是尺度，\(z\) 是零點。依數值範圍選擇 \(s\)，會決定捨入誤差。每個張量只用一個尺度成本低，但對離群值敏感。逐通道尺度，或逐組尺度（以一組權重為單位）準確度較高；在 GPTQ 與 AWQ 中，每 128 個權重為一組是常見的設定。

## 關鍵概念

- **僅權重量化與權重加啟動量化。**僅權重的方法讓啟動值保持 16 位元，可以節省記憶體，但對運算的節省有限。若連啟動值也量化，就能做整數矩陣乘法，但啟動值含有離群值，使這件事更困難。
- **訓練後量化（PTQ）。**模型在訓練後才量化，使用一小組校準資料來選擇尺度，不需要額外的訓練。
- **量化感知訓練（QAT）。**訓練時模擬捨入。梯度以直通估計器穿過捨入操作，使權重能適應量化格點。
- **離群值。**大型 Transformer 中，少數通道的值遠大於其他通道。如何處理它們，是低位元量化的核心困難。
- **數字格式。**INT8 與 INT4 使用整數運算。FP8 與 FP4 保留浮點指數，能更好地處理大範圍的數值，部分較新的加速器支援它們，見 [AI 硬體](../../../engineering/hardware/index.md)。

## 各類方法比較

| 方法類別 | 是否需要訓練 | 常見位元寬 | 最適合 | 頁面 |
| --- | --- | --- | --- | --- |
| 訓練後量化（PTQ） | 否，只需要校準資料 | 8 位元，僅權重時為 4 位元 | 大型語言模型 | [訓練後量化](post-training/index.md) |
| 量化感知訓練 | 是 | 2 至 8 位元 | 較小的模型，以及有嚴格限制的部署目標 | [量化感知訓練](quantisation-aware-training/index.md) |
| 二元與三元 | 是 | 1 至 2 位元 | 專用硬體上的卷積網路 | [二元與三元](binary-and-ternary/index.md) |
| 混合精度 | 視方法而定 | 因層而異 | 統一位元寬無法滿足的預算 | [混合精度](mixed-precision/index.md) |

對大型語言模型而言，PTQ 通常是首選，因為在那種規模下訓練的成本很高。當負擔得起訓練時，QAT 與其他需要訓練的方法能在低位元寬下挽回更多準確度。

## 訓練後量化方法速覽

- [LLM.int8()](post-training/llm-int8/index.md)：把離群維度保持在 16 位元，其餘以 8 位元執行。
- [GPTQ](post-training/gptq/index.md)：二階的捨入方法，搭配誤差補償，用於 3 與 4 位元。
- [AWQ](post-training/awq/index.md)：依啟動統計量縮放顯著通道，以保護它們。
- [SmoothQuant](post-training/smoothquant/index.md)：把啟動離群值搬移到權重中，使權重與啟動值都能使用 8 位元。

## 權衡

- **位元數與品質。**從 8 位元降到 4 位元，權重記憶體再減半，但品質損失會增加，而且依任務而異，因此應在真正重要的任務上量測。
- **校準成本與準確度。**PTQ 成本低但能力有限；QAT 能挽回更多準確度，代價是需要訓練。
- **格式與硬體。**一種能節省記憶體的格式，除非晶片與核心函式庫支援，否則不一定能加快推論。

## 關聯

量化是[大型模型服務](../../../engineering/mlops/index.md)的標準步驟，而可用的數字格式則取決於[硬體](../../../engineering/hardware/index.md)。生物神經元有雜訊，且以有限的精度傳遞資訊（Faisal、Selen 與 Wolpert，2008），因此「一個有用的系統需要多少精度」的問題，在神經科學中也會被提出。量化模型如何微調，見[訓練](../../../engineering/training/index.md)相關頁面。

## 應用

- **裝置端推論：**整數量化就是為行動裝置設計的，這些裝置對延遲與模型大小都很敏感（Jacob 等人，2017）。
- **大型語言模型：**僅權重的 4 位元與 8 位元方法，減少在單張 GPU 上服務模型所需的記憶體（Dettmers 等人，2022；Frantar 等人，2023；Lin 等人，2024）。
- **低功耗視覺：**用於相機與機器人的高效網路，也使用降低精度的方法（Gholami 等人，2021）。

## 未解問題

- **四位元及以下。**2 與 3 位元的品質，特別是在推理任務上，仍是活躍的研究領域。
- **啟動值中的離群值。**各方法處理鍵、值與啟動值中離群值的方式不同，目前沒有明確公認最好的規則。
- **評估。**基準分數的小幅下降，可能掩蓋行為上的大改變，例如拒絕回答或校準度。需要更好的測試。
- **大規模的訓練期量化。**超大型模型的量化感知預訓練，比訓練後方法更難調校。

## 參考文獻

### 開創性論文

- Jacob, B. 等人（2017）。*Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*。arXiv:1712.05877。https://arxiv.org/abs/1712.05877 — 讓每個運算都以整數算術進行的量化感知訓練，面向行動裝置上的裝置端推論。
- Dettmers, T., Lewis, M., Belkada, Y. & Zettlemoyer, L.（2022）。*LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*。NeurIPS。https://arxiv.org/abs/2208.07339 — 混合精度的 8 位元推論，把離群維度保持在 16 位元。
- Frantar, E. 等人（2023）。*GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*。ICLR。https://arxiv.org/abs/2210.17323 — 逐層的二階誤差補償，用於 3 與 4 位元權重。
- Lin, J. 等人（2024）。*AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*。MLSys 2024。https://arxiv.org/abs/2306.00978 — 依啟動統計量選擇逐通道尺度，以保護顯著權重。
- Xiao, G. 等人（2023）。*SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*。ICML 2023。https://arxiv.org/abs/2211.10438 — 把啟動離群值搬移到權重中，使兩者都能使用 8 位元。

### 綜述與教科書

- Gholami, A. 等人（2021）。*A Survey of Quantization Methods for Efficient Neural Network Inference*。《Low-Power Computer Vision》書中章節。arXiv:2103.13630。https://arxiv.org/abs/2103.13630 — 回顧降低精度的方法及其權衡。

### 神經科學

- Faisal, A. A., Selen, L. P. J. & Wolpert, D. M.（2008）。Noise in the nervous system。*Nature Reviews Neuroscience*, 9, 292–303。https://doi.org/10.1038/nrn2258 — 回顧神經元中雜訊的來源，以及它對神經系統如何精確表示資訊的意義。
