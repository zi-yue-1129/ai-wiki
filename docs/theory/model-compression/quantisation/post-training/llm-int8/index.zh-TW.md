---
translation_reviewed: 2026-10-28
---

# LLM.int8()

LLM.int8() 是大型 Transformer 的訓練後 8 位元推論方法。它把少數離群隱藏維度保留在 16 位元，其餘以 8 位元計算，使原本在純 8 位元量化下會損失品質的模型，能以約一半的記憶體維持完整精度的表現。

## 問題

大型 Transformer 會出現少數隱藏狀態維度，數值非常大。模型一旦夠大，全部量化為 8 位元就會使品質急遽下降，因此模型無法在保有完整品質的情況下放進記憶體。

## 核心想法

把每次矩陣乘法拆開。少數離群維度以 16 位元精度計算，其餘以 8 位元整數與向量尺度計算。這種方法稱為混合精度分解。

## 公式或演算法

輸入 \(X\) 與權重 \(W\) 的乘積寫成兩部分之和：正常維度的部分量化為 int8；離群維度的部分以 fp16 計算。\(X\) 的每一列與 \(W\) 的每一行各有自己的尺度。

## 結果

摘要報告，此方法能把推論所需記憶體減半，同時保持與完整精度相當的效能。

## 限制

離群路徑會增加負擔，而且此方法針對 8 位元。更低位元的推論需要其他方法，例如 [GPTQ](../gptq/index.zh-TW.md) 或 [AWQ](../awq/index.zh-TW.md)。

## 開放問題與相關變體

- **離群值偵測**：把一個維度標記為離群值的門檻是人工設定的；自動選擇仍是實務上的開放問題。
- **相關**：[SmoothQuant](../smoothquant/index.zh-TW.md) 從激活值中移除離群值，而不是另外計算它們。

## 相關連結

離群值問題也是[混合精度](../../mixed-precision/index.zh-TW.md)設法解決的問題，它的做法是給敏感部分更多位元。記憶體節省在[服務](../../../../../engineering/mlops/index.zh-TW.md)時最有價值。

## 參考文獻

### 開創性論文

- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — 混合精度 8 位元矩陣乘法，把離群維度保留在 16 位元。
- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., Han, S. (2023). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. ICML 2023. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — 把離群值移到權重上的替代方法。
- Frantar, E., 等人 (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — 較低位元的訓練後替代方法。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 把 LLM.int8() 放在精度降低方法之中。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 卷積網路的早期純整數推論方法。
