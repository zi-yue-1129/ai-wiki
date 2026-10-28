---
translation_reviewed: 2026-10-28
---

# 量化

量化以位元數較少的數字來儲存與計算，例如 8 位元整數、4 位元整數或 8 位元浮點數，取代 16 或 32 位元的浮點數。它是部署最廣泛的[模型壓縮](../index.zh-TW.md)形式，因為它能減少記憶體，而且在為低精度設計的硬體上常能加速矩陣乘法。

## 概述

均勻仿射量化把實數 \(x\) 映射到 \(b\) 位元整數 \(q\)：

\[
q = \operatorname{clip}\!\left(\operatorname{round}\!\left(\frac{x}{s}\right) + z,\ 0,\ 2^b - 1\right), \qquad \hat{x} = s\,(q - z)
\]

其中 \(s\) 是尺度、\(z\) 是零點。尺度依數值範圍選定，會決定捨入誤差。每個張量用一個尺度最省事，但對離群值很敏感。每個通道的尺度，或每 32 至 128 個值一組的分組尺度，準確度較高，也是大型語言模型權重的標準做法。

## 關鍵概念

- **僅權重量化與權重加激活量化**：僅權重方法讓激活值維持 16 位元，能省記憶體，但運算節省有限。同時量化激活值可以做整數矩陣乘法，但激活值含有離群值，使這件事更困難。
- **訓練後量化（PTQ）**：訓練完成後才量化，用一小批校準資料決定尺度，不需要額外訓練。
- **量化感知訓練（QAT）**：訓練時模擬捨入。梯度以直通估計器穿過捨入運算，使權重適應量化網格。
- **離群值**：大型 Transformer 中有少數通道的數值遠大於其他通道。處理它們是低位元量化的核心難題。
- **數字格式**：INT8 與 INT4 使用整數運算。FP8 與 FP4 保留浮點指數，能更好地處理寬廣的數值範圍，新一代加速器也支援；見 [AI 硬體](../../../engineering/hardware/index.zh-TW.md)。

## 各家族比較

| 家族 | 是否需要訓練 | 典型位元數 | 最適合 | 頁面 |
| --- | --- | --- | --- | --- |
| 訓練後量化（PTQ） | 否，只需校準資料 | 8 位元，僅權重量化可到 4 位元 | 大型語言模型 | [訓練後量化](post-training/index.zh-TW.md) |
| 量化感知訓練 | 是 | 2 到 8 位元 | 較小模型與有嚴格限制的部署目標 | [量化感知訓練](quantisation-aware-training/index.zh-TW.md) |
| 二值與三值 | 是 | 1 到 2 位元 | 專用硬體上的卷積網路 | [二值與三值](binary-and-ternary/index.zh-TW.md) |
| 混合精度 | 視方法而定 | 每層不同 | 均勻位元寬度無法滿足的預算 | [混合精度](mixed-precision/index.zh-TW.md) |

大型語言模型通常以 PTQ 為預設，因為這個規模的訓練成本太高。若負擔得起訓練，QAT 與其他需要訓練的家族在低位元時能恢復更多準確度。

## 訓練後方法一覽

- [LLM.int8()](post-training/llm-int8/index.zh-TW.md)：把離群維度保留在 16 位元，其餘以 8 位元計算。
- [GPTQ](post-training/gptq/index.zh-TW.md)：以二階資訊進行捨入，並補償誤差，適用 3 與 4 位元。
- [AWQ](post-training/awq/index.zh-TW.md)：依激活統計量縮放顯著通道，加以保護。
- [SmoothQuant](post-training/smoothquant/index.zh-TW.md)：把激活離群值的困難移到權重上，使權重與激活值都能是 8 位元。

## 取捨

- **位元數與品質**：從 8 位元降到 4 位元，記憶體大約再減半，但品質損失隨之增加，並依任務而異。推理與長脈絡任務通常最先退化。
- **校準成本與準確度**：訓練後量化便宜但有限；量化感知訓練能恢復更多準確度，代價是一次訓練過程。
- **格式與硬體**：一種能節省記憶體的格式，除非晶片與核心函式庫支援，否則不一定能加速推論。

## 相關連結

量化是[大型模型服務](../../../engineering/mlops/index.zh-TW.md)的標準步驟，也是[訓練](../../../engineering/training/index.zh-TW.md)中 QLoRA 微調方法的基礎。它使用的數字格式由[硬體](../../../engineering/hardware/index.zh-TW.md)決定。低精度與有雜訊的運算也出現在神經科學中，神經元以有限的精度傳遞資訊；一個有用的系統需要多少精度，是兩個領域共同的問題。

## 應用

- **本地語言模型**：在消費級筆電與手機上執行量化權重。
- **雲端推論**：每張 GPU 可服務更多同時連線的使用者，成本更低。
- **嵌入式視覺**：在小型晶片上為機器人與攝影機執行偵測器。

## 開放問題

- **4 位元及以下**：2 與 3 位元的品質，尤其是推理任務上的表現，仍是活躍的研究領域。
- **激活值離群值**：各方法處理鍵、值與激活值離群值的方式不同，目前沒有明確公認的最佳規則。
- **評估**：基準分數的小幅下降，可能掩蓋行為上的大變化，例如拒答或校準。需要更好的測試。
- **大規模的訓練期量化**：超大模型的量化感知預訓練，比訓練後方法更難調整。

## 參考文獻

### 開創性論文

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 量化感知訓練，並讓每個運算都以整數算術進行，是許多行動部署的基礎。
- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — 混合精度 8 位元推論，把離群維度保留在 16 位元。
- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. ICLR 2023. https://arxiv.org/abs/2210.17323 — 逐層的二階誤差補償，用於 3 與 4 位元權重。
- Lin, J., 等人 (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. MLSys 2024. https://arxiv.org/abs/2306.00978 — 依激活統計量選擇逐通道尺度，以保護顯著權重。
- Xiao, G., 等人 (2022). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — 把激活離群值的困難轉移到權重上，使兩者都能是 8 位元。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧精度降低方法及其取捨。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

（本頁尚未查核任何項目）
