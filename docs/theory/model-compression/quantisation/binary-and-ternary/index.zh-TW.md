---
translation_reviewed: 2026-10-28
---

# 二值與三值量化

二值與三值量化把權重（有時也包括激活值）限制在兩個值（\(\pm 1\)）或三個值（\(-1, 0, +1\)）。這是[量化](../index.zh-TW.md)的極端情形：每個權重的儲存量降到一或兩位元，乘法可以改成正負號翻轉與加法。準確度較難保住，因此這個家族的方法著重於尺度如何處理，以及梯度如何穿過離散數值。

## 概述

二值權重網路使用 \(W_b = \alpha \cdot \operatorname{sign}(W)\)，其中 \(\alpha\) 是實數尺度。三值網路使用 \(\{-\alpha, 0, +\alpha\}\) 中的值，因此可以把小權重量化為零。兩者在訓練時都需要[直通估計器](../quantisation-aware-training/index.zh-TW.md)，因為符號函數幾乎處處梯度為零。

## 關鍵概念

- **尺度因子**：每層或每個濾波器一個實數尺度，使輸出量級接近全精度層。沒有它，二值網路會失去大部分準確度。
- **三值網路中的零**：零值讓三值網路在量化的同時修剪權重，因此它介於二值網路與[剪枝](../../pruning/index.zh-TW.md)之間。
- **二值激活值**：同時量化權重與激活值可以消除大部分乘法，但會丟棄更多資訊，也更難訓練。

## 各方法比較

| 方法 | 權重值 | 尺度 | 是否二值化激活值 | 頁面 |
| --- | --- | --- | --- | --- |
| BinaryConnect | \(\pm 1\) | 無 | 否 | [BinaryConnect](binaryconnect/index.zh-TW.md) |
| XNOR-Net | 每濾波器 \(\pm \alpha\) | 每濾波器，由平均量值算出 | 完整版本為是 | [XNOR-Net](xnor-net/index.zh-TW.md) |
| 三值權重網路 | \(\{-\alpha, 0, +\alpha\}\) | 每濾波器，附量值門檻 | 否 | [三值權重網路](ternary-weight-networks/index.zh-TW.md) |

BinaryConnect 證明二值權重可以訓練；XNOR-Net 加上保留輸出量級的尺度；三值權重網路則加上一個零，使接近零的權重能精確表示。

## 取捨

- **壓縮與準確度**：二值權重每個權重佔一位元，三值權重緊密打包時約占 1.6 位元（log₂ 3），因此從三值改為二值，節省的儲存量不到一半，並且失去零值。準確度損失取決於任務與訓練方法，應以論文的表格為準。
- **硬體支援**：二值與三值網路在晶片實作位元運算時獲益最多。在 GPU 上，獲益有限。
- **訓練困難**：梯度近似有偏差，結果也取決於訓練排程。

## 更多變體與開放問題

- **開放問題**：二值網路能否在大型 Transformer 上達到全精度準確度；目前大多數報告的成果來自小型卷積網路。
- **開放問題**：如何在大規模下穩定地訓練二值激活值。
- **變體**：每個通道學習尺度因子，使二值網路更接近[混合精度](../mixed-precision/index.zh-TW.md)方案。

## 相關連結

極低位元的範圍與[硬體](../../../../engineering/hardware/index.zh-TW.md)討論中的位元序列與記憶體內運算相關。三值網路中的零與[剪枝](../../pruning/index.zh-TW.md)相連，而離散權重的訓練則與[神經科學](../../../../brain-mind/neuroscience/index.zh-TW.md)中低精度突觸的問題相關。

## 參考文獻

### 開創性論文

- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with binary weights during propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 在前向與反向傳播中使用二值權重，同時保留實數權重以累積梯度。
- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶尺度因子的二值濾波器。其二值權重版本的 AlexNet 與全精度的 top-1 準確度相差僅 2.9%；另將輸入也二值化的 XNOR-Net，卷積運算快 58 倍。
- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值權重由門檻函數決定，並以尺度因子最小化與全精度權重的距離，最高可達 16 倍壓縮。
- Hubara, I., Soudry, D., El-Yaniv, R. (2016). *Binarized Neural Networks*. arXiv:1602.02505. https://arxiv.org/abs/1602.02505 — 執行時權重與激活值皆為二值的網路。
- Zhu, C., Han, S., Mao, H., Dally, W. J. (2016). *Trained Ternary Quantization*. arXiv:1612.01064. https://arxiv.org/abs/1612.01064 — 為每層中正負兩類三值權重分別學習尺度因子。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧低位元方法及其取捨。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 純整數推論，是上述二值方法的 8 位元對應。
