---
translation_reviewed: 2026-10-28
---

# BinaryConnect

BinaryConnect 訓練一個在前向與反向傳播中使用二值權重（\(\pm 1\)）的神經網路，同時保留實數權重做參數更新。它是第一個證明深度網路可以用二值權重訓練的方法，也是[二值與三值](../index.zh-TW.md)家族中大多數後續研究的起點。

## 問題

梯度下降需要對權重做微小的實數更新。權重只有 \(\pm 1\) 的網路無法直接接受這樣的更新，因此若沒有不同的學習規則，二值權重訓練看似不可能。

## 核心想法

保留一份全精度的權重副本用於更新。每個小批次中，以符號函數二值化這份副本，用二值權重進行前向與反向計算，再把得到的梯度套用到實數副本上。實數權重會被限制在有界範圍內，使它們保持接近二值化的門檻。

## 公式或演算法

前向傳播使用 \(W_b = \operatorname{sign}(W)\)。損失對 \(W_b\) 的梯度照常計算，再以直通估計器傳給 \(W\)，因為符號函數幾乎處處梯度為零。每次更新後，把 \(W\) 限制在 \([-1, 1]\)。在論文的一個變體中，二值化是隨機的，作者把它視為一種正則化。

## 結果

作者報告，在排列不變的 MNIST、CIFAR-10 與 SVHN 上取得接近最先進的結果，並說明二值化在訓練期間具有正則化效果。

## 限制

實驗使用當時的小型網路與資料集。此方法沒有逐層的尺度因子，後續研究發現這對維持輸出量級接近全精度層很重要。它的運算增益，取決於能利用二值權重的硬體。

## 開放問題與相關變體

- **尺度因子**：如 [XNOR-Net](../xnor-net/index.zh-TW.md) 那樣為每個濾波器加上實數尺度，可以找回單純符號函數所損失的大部分準確度。
- **三值權重**：允許零值，如[三值權重網路](../ternary-weight-networks/index.zh-TW.md)，能以稍微增加的儲存量換取稀疏編碼。
- **隨機二值化**：隨機形式是否在各種任務上優於確定性二值化，尚無定論。

## 相關連結

此處使用的直通估計器，與[量化感知訓練](../../quantisation-aware-training/index.zh-TW.md)中使用的裝置相同。二值權重的運算，則與 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)中的位元層級運算相關。

## 參考文獻

### 開創性論文

- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — 前向傳播使用二值權重訓練，同時保留實數權重做更新。
- Rastegari, M., 等人 (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 為二值權重加上每濾波器尺度因子，大幅縮小準確度差距。
- Li, F., 等人 (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 把二值權重擴充為三個值，零值保留了稀疏編碼。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 在其他低位元方法之中回顧二值訓練。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 與二值權重相對的 8 位元整數方法，用於比較準確度代價。
