---
related:
  - theory/model-compression/pruning
  - engineering/hardware/co-design
tags:
  - model compression
  - quantisation
  - inference
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - A Survey of Quantization Methods
  - Gholami quantisation survey
  - 神經網路量化方法綜述
---

# 神經網路量化方法綜述（Gholami et al., 2021）

Gholami、Kim、Dong 等人（2021）綜述如何以較少的位元表示神經網路的數值，並在這個過程中維持準確率。這份綜述是量化領域的標準入門文獻之一。它涵蓋數值格式、調整或訓練量化模型的兩種主要方式，以及整數運算能帶來的加速（Gholami et al., 2021）。

## 概觀

量化把實數值的權重與活化值映射到一小組離散的水準。綜述把問題表述為一個表示的問題：如何把連續的數值分布到固定的離散數字集合上，使所需位元數很少，同時計算仍然準確。之所以重要，是因為記憶體與運算都受限。位元越少，需要搬移的資料越少；在合適的硬體上，整數運算也可能比浮點運算更快（Gholami et al., 2021）。

## 關鍵概念

- **均勻仿射量化**：論文把實數值寫成整數乘以尺度 S，再加上整數零點 Z 的平移。尺度由裁剪範圍 [α, β] 與位元寬 b 決定，即 S = (β − α)/(2^b − 1)（第 III-C 節）。
- **訓練後量化（PTQ）**：對已訓練的模型進行量化，不需重新訓練，只需要一小組校準資料（第 III-G.2 節）。
- **量化感知訓練（QAT）**：在訓練中模擬量化，使權重在每次梯度更新後都被量化（第 III-G.1 節）。
- **零樣本量化**：在無法存取訓練或驗證資料的情況下進行量化（第 III-G.3 節）。

## 運作方式

綜述把數值格式的選擇與訓練程序的選擇分開。就格式而言，它描述均勻仿射量化，以及裁剪範圍的選擇所產生的影響。就程序而言，它比較 PTQ 與 QAT。

QAT 需要重新訓練模型，論文指出重新訓練的運算成本是它的主要缺點。論文認為，若模型將長期部署，這筆投資可能值得；它也指出有些模型的使用壽命很短（第 III-G.1 節）。PTQ 避免重新訓練，論文指出，與 QAT 相比，它常常以準確率為代價（第 III-G.2 節）。

## 關鍵方法

以下簡要比較各類方法，細節請見各方法頁面：

- [訓練後量化](post-training/index.md)：在不重新訓練的情況下校準已訓練的模型，包括為大型語言模型設計的方法。
- [量化感知訓練](quantisation-aware-training/index.md)：在訓練迴圈中加入量化。
- [純整數推論](quantisation-aware-training/integer-only-inference/index.md)：以整數運算執行整個網路。
- [混合精度](mixed-precision/index.md)：逐層選擇位元寬。

## 證據與結果

摘要指出，量化可以用四個位元或更少來表示數值，而實務上常能實現四到八倍的縮減。第 I 節指出，使用 INT8 或更低精度時，可以在 4 倍以上的壓縮下維持效能（Gholami et al., 2021）。

就 INT8 而言，論文指出許多模型可以直接部署而不損失準確率（第 VI 節）。它的硬體結果顯示，在 NVIDIA GTX 1080 上，常見視覺模型的 INT8 加速分別為 3.89、3.32 與 5.02 倍；BERT 的 INT8 推論則比 FP32 最多快 4.0 倍（第 VII 節）。

## 限制

- **低位元下的準確率。** 綜述指出，PTQ 常在準確率上不如 QAT，因此選擇取決於重新訓練的預算，以及準確率的重要程度。
- **硬體依賴。** 加速數字來自特定硬體與核心。整數格式只有在目標硬體能有效執行時才有幫助。
- **公式慣例。** 論文在量化與反量化公式中對零點的符號慣例不一致，因此讀者在重用公式前應先確認慣例。

## 相關連結

- [剪枝與稀疏性](../pruning/index.md) 減少的是數值的數量，而量化減少的是每個數值的精度。兩者可以結合。
- [硬體協同設計](../../../engineering/hardware/co-design/index.md) 說明為何整數與低精度格式對加速器很重要。

## 應用

這份綜述的動機來自受限裝置的記憶體與運算限制。它的硬體結果涉及視覺模型與 BERT（Gholami et al., 2021）。

## 未解問題

- 對於特定架構，在不重新訓練的情況下，精度可以降到多低，準確率才會失效。
- 格式、校準與訓練的哪種組合，能在語言模型上得到最佳的每位元組準確率。

## 參考文獻

### 開創性論文

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W. & Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv. https://arxiv.org/abs/2103.13630 — 綜述數值格式、PTQ 與 QAT，以及本頁討論的硬體加速。
- Jacob, B., Kligys, S., Chen, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv. https://arxiv.org/abs/1712.05877 — 以量化感知訓練實現純整數推論。
- Banner, R., Nahshan, Y. & Hoffer, E. (2018). *Post-training 4-bit quantization of convolution networks for rapid-deployment*. arXiv. https://arxiv.org/abs/1810.05723 — 卷積網路在四位元下的訓練後量化。
- Dettmers, T., Lewis, M., Belkada, Y. & Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv. https://arxiv.org/abs/2208.07339 — 大型 Transformer 的八位元矩陣乘法。
- Frantar, E., Ashkboos, S., Hoefler, T. & Alistarh, D. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv. https://arxiv.org/abs/2210.17323 — 大型語言模型的低位元訓練後量化。

### 綜述與白皮書

- Nagel, M. et al. (2021). *A White Paper on Neural Network Quantization*. arXiv. https://arxiv.org/abs/2106.08295 — 關於 PTQ 與 QAT 方法的神經網路量化白皮書。
