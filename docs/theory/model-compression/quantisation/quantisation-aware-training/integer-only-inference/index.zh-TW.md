---
translation_reviewed: 2026-10-28
---

# 純整數推論

純整數推論是一種量化感知訓練方法，在訓練時模擬一個每個運算都使用整數的網路。權重、激活值、殘差相加與非線性函數都使用量化後的數值，因此訓練好的網路可以部署在純整數硬體上，而不會因為從浮點數轉換而損失準確度。它是[量化感知訓練](../index.zh-TW.md)家族的一部分。

## 問題

行動處理器執行整數運算的效率遠高於浮點數，有些加速器也只支援整數。以浮點數訓練的網路，轉換成整數後常會損失準確度，因為轉換引入的捨入，是訓練時從未見過的。

## 核心想法

訓練時使用部署模型將使用的同一種整數運算。每個張量都以 8 位元整數加上尺度與零點儲存。每一層以較寬的累加器做整數矩陣乘法，再把結果重新縮放到下一層的網格。重新縮放本身也以整數運算完成。

## 公式或演算法

實數 \(r\) 表示為 \(r = s\,(q - z)\)，其中 \(q\) 是 8 位元整數，\(s\) 是實數尺度，\(z\) 是整數零點。對於輸入與權重都已量化的層，乘積以整數累加計算，輸出再以尺度比值的定點近似映射到下一個網格。訓練圖在這些位置插入假量化，因此梯度以直通估計器穿過。

## 結果

摘要報告，純整數推論的準確度有顯著改善，即使在本來就為高效推論設計的 MobileNet 上也是如此。摘要沒有給出單一的主要數字，具體數值應查閱論文中的表格。

## 限制

此方案針對卷積網路設計，論文沒有涵蓋大型 Transformer。殘差相加與批次正規化摺疊需要謹慎處理，而訓練與部署核心之間的不一致，仍可能造成準確度損失。

## 開放問題與相關變體

- **Transformer**：注意力、softmax 與層正規化的純整數流程，比卷積更難建構；大型語言模型的方法（例如 [SmoothQuant](../../post-training/smoothquant/index.zh-TW.md)）會把這些部分保留為浮點數，或採用其他設計。
- **相關**：[LSQ](../lsq/index.zh-TW.md) 學習尺度，而不是從統計量計算；[二值與三值](../../binary-and-ternary/index.zh-TW.md)方法則更進一步，完全移除乘法。

## 相關連結

此處使用的整數格式，是行動與邊緣[硬體](../../../../../engineering/hardware/index.zh-TW.md)在矩陣單元中實作的格式，而訓練流程則位於[訓練](../../../../../engineering/training/index.zh-TW.md)之下。許多行動部署工具鏈都以相同的想法為基礎。

## 參考文獻

### 開創性論文

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 在訓練時模擬純整數推論，使部署模型與訓練圖一致。
- Esser, S. K., 等人 (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — 學習尺度而非從統計量固定，是同一家族中的後續步驟。
- Dong, Z., 等人 (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — 為層指定不同位元寬度，是純整數推論的混合精度替代方案。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 與其他精度降低方法一同回顧純整數推論。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 面向 Transformer 的 8 位元整數路徑，並把離群維度保留在 16 位元。
