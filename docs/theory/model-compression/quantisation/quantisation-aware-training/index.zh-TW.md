---
translation_reviewed: 2026-10-28
---

# 量化感知訓練

量化感知訓練（QAT）在訓練網路時模擬推論時會遇到的捨入，使權重適應量化網格。它是[訓練後量化](../index.zh-TW.md)的訓練期對應方法，在相同位元數下通常能恢復更多準確度，代價是需要一次訓練過程。

## 概述

在 QAT 中，前向傳播套用假量化：每個權重或激活值被捨入到網格上，再映回實數，使損失函數能看見捨入誤差。反向傳播無法對捨入微分，因為捨入是幾乎處處梯度為零的階梯函數。標準的解法是**直通估計器**（STE）：把捨入運算的梯度視為一，讓梯度直接穿過，就像沒有捨入一樣。[BinaryConnect](../binary-and-ternary/index.zh-TW.md) 使用這個估計器做二值訓練。

## 關鍵概念

- **假量化**：訓練時套用的捨入，激活值仍維持浮點數，因此透過 STE 計算仍可微分。
- **步長**：量化網格的尺度。傳統 QAT 從張量的統計量設定步長；可學習的方法則把步長當作可訓練參數。
- **校準與訓練的差異**：PTQ 在一小批資料上決定尺度後就停止。QAT 會更新權重許多步，使網路能把數值移到網格上。
- **批次正規化摺疊**：部署模型通常會先把批次正規化摺進前一層卷積再量化，因此 QAT 也在摺疊後的計算圖上進行，使訓練與部署一致。

## 重要方法

### 可學習步長量化（Esser 等人，2019）

- **問題：** 固定的步長規則與損失無關，在 2 到 4 位元時，步長的選擇影響很大。
- **核心想法：** 把步長當作參數，與權重一起用梯度下降學習。對步長的梯度透過捨入函數、以直通近似取得。
- **公式或演算法：** 量化值為 \(\hat{x} = s \cdot \operatorname{round}(\operatorname{clip}(x/s, -Q_n, Q_p))\)，\(s\) 依損失更新，並選擇梯度縮放，使步長相對於權重以合理速度學習。
- **結果：** 摘要表示，此方法在 ImageNet 上對量化到 2、3、4 位元的模型達到迄今最高準確度，並且 3 位元模型能達到全精度基準的準確度。
- **限制：** 訓練成本即完整或較長時間的微調成本。結果針對影像分類，且需要有標籤的訓練資料。

### 純整數推論（Jacob 等人，2017）

- **問題：** 行動裝置執行整數運算的效率遠高於浮點數，但以浮點數訓練的網路轉成整數後會損失準確度。
- **核心想法：** 訓練時模擬純整數推論，使每個運算（包括非線性函數與殘差相加）都在量化數值上計算。
- **公式或演算法：** 以尺度與零點把實數映射到 8 位元整數，權重與激活值都如此處理，整數矩陣乘法之後再重新縮放。
- **結果：** 摘要報告，即使在本來就為高效推論設計的 MobileNet 上，改善仍然顯著。摘要沒有給出單一的主要數字。
- **限制：** 此方案針對當時的卷積網路設計，論文沒有涵蓋它在大型 Transformer 上的效果。

## 取捨

- **準確度與訓練成本**：在低位元時 QAT 比 PTQ 恢復更多準確度，但需要 PTQ 不需要的訓練過程。
- **梯度近似**：直通估計器有偏差，在極低位元時近似會變差。
- **模型規模**：對於數十億參數的模型，完整 QAT 很昂貴，因此大型語言模型更常使用 [GPTQ](../index.zh-TW.md) 這類 PTQ 方法。

## 更多變體與開放問題

- **以低秩配接器進行大型語言模型的量化感知微調**，見[訓練](../../../../engineering/training/index.zh-TW.md)。
- **開放問題**：部署後校準分布改變時，可學習步長是否仍保持穩定。
- **開放問題**：QAT 如何與離群通道互動；PTQ 方法會以 [LLM.int8()](../index.zh-TW.md) 明確處理這些通道。

## 相關連結

QAT 依賴目標[硬體](../../../../engineering/hardware/index.zh-TW.md)支援的數字格式，其成本則取決於[訓練](../../../../engineering/training/index.zh-TW.md)流程。降低精度時如何保持模型行為，在[量化](../index.zh-TW.md)頁討論。

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

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 大型語言模型上，QAT 的訓練後替代方案，詳見上層頁面。
