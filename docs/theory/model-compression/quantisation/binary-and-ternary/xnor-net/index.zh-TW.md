---
translation_reviewed: 2026-10-28
---

# XNOR-Net

XNOR-Net 以二值濾波器乘上實數尺度因子來近似每個實數卷積濾波器，也可以二值化輸入激活值。當權重與激活值都是二值時，卷積會化簡為 XNOR 運算與位元計數，比浮點數乘法快得多。它是[二值與三值](../index.zh-TW.md)家族中的方法，並在 [BinaryConnect](../binaryconnect/index.zh-TW.md) 的基礎上加入尺度因子。

## 問題

沒有尺度因子的二值網路，在 ImageNet 上會損失許多準確度，因為符號函數丟棄了權重與激活值的量級。每一層的輸出於是有錯誤的尺度。

## 核心想法

以二值濾波器 \(B\) 乘上由濾波器本身算出的尺度 \(\alpha\)，來近似原始濾波器 \(W\)，使近似的總和保留原本的量級。每個卷積的輸入也以相同方式二值化。卷積於是在二值數值上進行，尺度只在每個輸出上套用一次。

## 公式或演算法

近似式為 \(W \approx \alpha B\)，其中 \(B = \operatorname{sign}(W)\)，\(\alpha = \lVert W \rVert_1 / n\)，\(n\) 是濾波器中權重的數量。在完整的 XNOR-Net 版本中，輸入 \(I\) 也以相同方式二值化，兩個二值向量的內積就變成 XNOR 運算加上位元計數。

## 結果

摘要報告，二值權重版本的 AlexNet 在 ImageNet 上的 top-1 準確度，只比全精度 AlexNet 低 2.9%。完全二值的版本損失更多準確度，數字見論文表格。

## 限制

在許多任務上，完全二值版本的準確度不如二值權重版本。速度增益取決於能有效執行位元運算的硬體，在 GPU 上實際增益很小。

## 開放問題與相關變體

- **完全二值網路的準確度**：在困難的任務上，二值權重與完全二值網路之間的差距仍然很大，後續方法試圖以更好的訓練來縮小它。
- **相關**：[三值權重網路](../ternary-weight-networks/index.zh-TW.md)保留零值，而[混合精度](../../mixed-precision/index.zh-TW.md)則把敏感的層保留在較多位元。

## 相關連結

XNOR 與位元計數的運算，是位元序列或記憶體內運算[硬體](../../../../../engineering/hardware/index.zh-TW.md)可以利用的位元層級操作。使用每濾波器尺度，也是 [AWQ](../../post-training/awq/index.zh-TW.md) 中逐通道縮放的一種形式。

## 參考文獻

### 開創性論文

- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶尺度因子的二值濾波器，使 AlexNet 的 top-1 準確度只差 2.9%。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — XNOR-Net 所擴充、以二值權重訓練的方法。
- Li, F., 等人 (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值替代方案，零值保留了部分權重。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 把二值卷積放在低位元方法之中。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 作為二值卷積比較基準的 8 位元整數方法。
