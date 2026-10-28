---
translation_reviewed: 2026-10-28
---

# 訓練後量化

訓練後量化（PTQ）在不重新訓練模型的情況下，把已訓練好的模型轉成較低精度。它用一小批校準資料決定尺度，並逐層固定或調整捨入。對大型語言模型來說，PTQ 是最常見的做法，因為完整的量化感知訓練成本過高。

## 概述

最簡單的 PTQ 是最近捨入：為每個張量或每組計算尺度，並把每個值捨入到最近的網格點。它很快，但在 4 位元及以下時會損失準確度，因為捨入一個權重時，忽略了它對輸出的影響。本頁的方法以不同方式改進基準：以二階資訊選擇捨入方式（GPTQ）、保護最重要的權重（AWQ）、把激活離群值移到權重上（SmoothQuant），或把離群維度保留在較高精度（LLM.int8()）。

## 關鍵概念

- **校準集**：數百到數千筆輸入，用來量測激活統計量，並選擇尺度或計算重建誤差。
- **分組尺度**：把權重分成 32 到 128 個值一組，每組有自己的尺度，可以減輕離群值造成的損害。
- **逐層目標**：大多數 PTQ 方法最小化單一層的輸出誤差 \(\lVert WX - \hat{W}X \rVert^2\)，而不是權重誤差。
- **僅權重與權重加激活**：僅權重方法節省記憶體，但運算仍以浮點數進行；權重加激活的方法則可使用整數運算。

## 方法

每個方法都有自己的頁面：

- [LLM.int8()](llm-int8/index.zh-TW.md)：混合精度分解，把離群維度保留在 16 位元。
- [GPTQ](gptq/index.zh-TW.md)：以二階資訊進行捨入，並補償誤差，適用 3 與 4 位元。
- [AWQ](awq/index.zh-TW.md)：依激活統計量縮放顯著通道，加以保護。
- [SmoothQuant](smoothquant/index.zh-TW.md)：把激活離群值移到權重上，使權重與激活值都能是 8 位元。

## 取捨

- **成本與準確度**：PTQ 需要數分鐘到數小時的校準。解決逐層問題的方法成本較高，但在低位元時能保留更多準確度。
- **位元寬度**：多數方法在 8 位元時可靠，但在 4 位元及以下時變得敏感。
- **核心支援**：只有推論函式庫能快速執行某種格式，該方法才有實用價值。

## 相關連結

PTQ 是 LLM 服務的預設做法，見[MLOps 與部署](../../../../engineering/mlops/index.zh-TW.md)。PTQ 所針對的數字格式由 [AI 硬體](../../../../engineering/hardware/index.zh-TW.md)決定。若要使用訓練期的替代做法，見[量化感知訓練](../quantisation-aware-training/index.zh-TW.md)。

## 開放問題

- **4 位元以下**：單靠 PTQ，2 與 3 位元的品質（尤其是推理任務）仍未解決。
- **校準偏差**：校準集可能偏向某些領域，對其他領域的影響尚未充分量測。
- **方法組合**：GPTQ 式的捨入與 AWQ 式的縮放能否同時使用而不互相干擾，是待解的工程問題。

## 參考文獻

### 開創性論文

- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 逐層二階捨入，用於 3 與 4 位元權重。
- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 混合精度 8 位元推論，把離群維度保留在 16 位元。
- Lin, J., 等人 (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. arXiv:2306.00978. https://arxiv.org/abs/2306.00978 — 依激活統計量選擇逐通道尺度，以保護顯著權重。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧精度降低方法及其取捨。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Xiao, G., 等人 (2022). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — 把激活離群值移到權重上，使兩者都能是 8 位元。
