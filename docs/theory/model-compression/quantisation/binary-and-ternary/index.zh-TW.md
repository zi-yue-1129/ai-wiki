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

## 重要方法

### BinaryConnect（Courbariaux 等人，2015）

- **問題：** 在前向傳播中使用二值權重訓練，看似需要二值更新，但這與梯度下降不相容。
- **核心想法：** 參數更新時保留全精度權重，只在計算前向與反向傳播時二值化。二值化本身具有正則化效果。
- **公式或演算法：** 前向傳播使用 \(\operatorname{sign}(W)\)，在二值權重上計算梯度，把更新套用到實數 \(W\)，並把 \(W\) 限制在有界範圍內。
- **結果：** 作者報告，在排列不變的 MNIST、CIFAR-10 與 SVHN 上取得接近最先進的結果，並說明二值化具有正則化效果。
- **限制：** 方法是在當時的小型網路與資料集上驗證的。它沒有後來被證明重要的逐層尺度因子。

### XNOR-Net（Rastegari 等人，2016）

- **問題：** 二值網路在 ImageNet 上會損失許多準確度，因為權重與激活值的量級被丟棄了。
- **核心想法：** 以二值濾波器乘上一個尺度來近似每個實數濾波器，尺度由濾波器的平均絕對值算出，使輸出量級得以保留。卷積以 XNOR 運算與計數（popcount）完成。
- **公式或演算法：** \(W \approx \alpha \cdot B\)，其中 \(B = \operatorname{sign}(W)\)，\(\alpha = \lVert W \rVert_1 / n\)。完整的 XNOR-Net 版本也會對激活值做類似的二值化。
- **結果：** 摘要表示，二值權重版本的 AlexNet 在 top-1 準確度上只比全精度 AlexNet 低 2.9%。
- **限制：** 二值激活值的版本損失更多準確度。方法需要支援快速位元運算的硬體才能實現加速。

### 三值權重網路（Li 等人，2016）

- **問題：** 二值權重丟棄太多資訊。三值編碼保留了零，這既便宜又有表達力。
- **核心想法：** 把每個權重量化為三個值之一：量值低於門檻的權重為零，其餘非零值使用一個尺度。
- **公式或演算法：** 門檻與尺度的選擇目標是使三值權重與全精度權重之間的期望平方誤差最小，並以每個濾波器近似求得。
- **結果：** 摘要報告最高可達 16 倍的模型壓縮。全精度與壓縮版本之間的準確度差距，應參考論文中的表格。
- **限制：** 三值運算需要硬體支援。壓縮比假設三值編碼儲存得很有效率。

## 取捨

- **壓縮與準確度**：從三值改為二值，每個權重的儲存量減半，但失去零值。準確度損失取決於任務與訓練方法，應以論文的表格為準。
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

- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 前向傳播使用二值權重訓練，同時保留實數權重做更新。
- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶尺度因子的二值濾波器，使 AlexNet 的 top-1 準確度只差 2.9%。
- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值權重，帶有學習得到的門檻與尺度，最高可達 16 倍壓縮。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 回顧低位元方法及其取捨。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 純整數推論，是上述二值方法的 8 位元對應。
