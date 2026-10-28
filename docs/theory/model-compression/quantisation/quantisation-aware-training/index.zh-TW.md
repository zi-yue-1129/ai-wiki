---
translation_reviewed: 2026-10-28
---

# 量化感知訓練

量化感知訓練（QAT）在訓練網路時模擬推論時會遇到的捨入，使權重適應量化網格。它是[訓練後量化](../post-training/index.zh-TW.md)的訓練期對應方法，在相同位元數下通常能恢復更多準確度，代價是需要一次訓練過程。

## 概述

在 QAT 中，前向傳播套用假量化：每個權重或激活值被捨入到網格上，再映回實數，使損失函數能看見捨入誤差。反向傳播無法對捨入微分，因為捨入是幾乎處處梯度為零的階梯函數。標準的解法是**直通估計器**（STE）：把捨入運算的梯度視為一，讓梯度直接穿過，就像沒有捨入一樣。[BinaryConnect](../binary-and-ternary/binaryconnect/index.zh-TW.md) 對二值權重也使用同一個估計器。

## 關鍵概念

- **假量化**：訓練時套用的捨入，激活值仍維持浮點數，因此透過 STE 計算仍可微分。
- **步長**：量化網格的尺度。傳統 QAT 從張量的統計量設定步長；可學習的方法則把步長當作可訓練參數。
- **校準與訓練的差異**：PTQ 在一小批資料上決定尺度後就停止。QAT 會更新權重許多步，使網路能把數值移到網格上。
- **批次正規化摺疊**：部署模型通常會先把批次正規化摺進前一層卷積再量化，因此 QAT 也在摺疊後的計算圖上進行，使訓練與部署一致。

## 各方法比較

| 方法 | 學習或固定的對象 | 典型位元數 | 頁面 |
| --- | --- | --- | --- |
| 可學習步長（LSQ） | 以梯度下降與權重一起學習步長 | 2 到 4 位元 | [LSQ](lsq/index.zh-TW.md) |
| 純整數推論 | 在訓練中模擬所有整數運算，包括殘差相加 | 8 位元 | [純整數推論](integer-only-inference/index.zh-TW.md) |

當低位元下的準確度很重要，且負擔得起訓練時，應先試 LSQ。當目標裝置沒有浮點單元（許多行動晶片屬於此類），而且訓練圖必須與整數核心完全一致時，則選純整數推論。

## 取捨

- **準確度與訓練成本**：在低位元時 QAT 比 PTQ 恢復更多準確度，但需要 PTQ 不需要的訓練過程。
- **梯度近似**：直通估計器有偏差，在極低位元時近似會變差。
- **模型規模**：對於數十億參數的模型，完整 QAT 很昂貴，因此大型語言模型更常使用 [GPTQ](../post-training/gptq/index.zh-TW.md) 這類 PTQ 方法。

## 更多變體與開放問題

- **以低秩配接器進行大型語言模型的量化感知微調**，見[訓練](../../../../engineering/training/index.zh-TW.md)。
- **開放問題**：部署後校準分布改變時，可學習步長是否仍保持穩定。
- **開放問題**：QAT 如何與離群通道互動；PTQ 方法會以 [LLM.int8()](../post-training/llm-int8/index.zh-TW.md) 明確處理這些通道。

## 相關連結

QAT 依賴目標[硬體](../../../../engineering/hardware/index.zh-TW.md)支援的數字格式，其成本則取決於[訓練](../../../../engineering/training/index.zh-TW.md)流程。使用二值或三值權重的方法見[二值與三值](../binary-and-ternary/index.zh-TW.md)，位元分配的問題見[混合精度](../mixed-precision/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Esser, S. K., 等人 (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — 以梯度下降學習量化步長，3 位元即可達到全精度準確度。
- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 量化感知訓練，並讓每個運算都以整數算術進行。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 前向傳播使用二值權重訓練，更新時保留實數權重。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧精度降低方法及其取捨，包括訓練期方法。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 大型語言模型上，QAT 的訓練後替代方案，詳見訓練後量化頁面。
