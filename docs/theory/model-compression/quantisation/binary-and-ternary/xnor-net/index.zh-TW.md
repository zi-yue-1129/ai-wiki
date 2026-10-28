---
translation_reviewed: 2026-10-28
---

# XNOR-Net

XNOR-Net 以二值濾波器乘上實數縮放係數來近似每個實數卷積濾波器，也可以把輸入激活二值化。當權重與輸入都是二值時，卷積化為 XNOR 運算與位元計數，比浮點乘法快得多。它是[二值與三值](../index.zh-TW.md)系列中的一種方法，並為 [BinaryConnect](../binaryconnect/index.zh-TW.md) 加入了縮放係數。

## 問題

沒有縮放係數的二值網路在 ImageNet 上會損失很多準確率，因為符號函式丟棄了權重與激活的幅度。每一層的輸出於是有錯誤的尺度。

## 核心想法

以二值濾波器 \(B\) 乘上由濾波器本身計算出的縮放 \(\alpha\) 來近似每個濾波器 \(W\)，使近似結果保留原濾波器的幅度。每個卷積的輸入也以相同方式二值化。卷積於是在二值數值上進行，縮放則在每個輸出上只套用一次。

## 公式或演算法

權重近似為 \(W \approx \alpha B\)，其中 \(B = \operatorname{sign}(W)\)，且

\[
\alpha^\ast = \frac{\lVert W \rVert_{\ell_1}}{n}
\]

其中 \(n\) 是濾波器中的權重數。因此縮放係數就是該濾波器權重的平均絕對值。卷積近似為 \(I \ast W \approx (I \oplus B)\,\alpha\)，其中 \(\oplus\) 只使用加法與減法。在完整的 XNOR-Net 變體中，輸入 \(I\) 以相同方式二值化，兩個二值向量的內積便成為 XNOR 加上位元計數（popcount）。

## 結果

摘要報告，二值權重版本的 AlexNet 在 ImageNet 上的分類準確率與全精度 AlexNet 相同。完全二值的 XNOR-Net 準確率較低：論文的表 1 顯示，XNOR-Net 的 top-1 準確率為 44.2%，全精度 AlexNet 為 56.6%，差距 12.4 個百分點。摘要也報告，它的準確率比 BinaryConnect 與 BinaryNet 高出 16% 以上。

## 限制

完全二值的變體損失的準確率，是二值權重版本所沒有的，因此在這個任務上，加速的收益伴隨著較大的準確率代價。加速取決於能有效實作位元運算的硬體，而在 GPU 上實際獲益很少。

## 未解問題與相關變體

- **完全二值網路的準確率。** 在困難的任務上，二值權重網路與完全二值網路之間的差距仍然很大，後續方法試圖以更好的訓練來縮小它。
- **相關。** [三值權重網路](../ternary-weight-networks/index.zh-TW.md)保留零值；[混合精度](../../mixed-precision/index.zh-TW.md)則讓敏感的層保留更多位元。

## 與其他主題的連結

XNOR 與位元計數運算是位元層級的操作，具有位元串列或記憶體內運算能力的 [硬體](../../../../../engineering/hardware/index.zh-TW.md)可以利用它。每個濾波器一個縮放，在精神上類似 [AWQ](../../post-training/awq/index.zh-TW.md) 的逐通道縮放，不過兩者縮放的對象不同。

## 參考文獻

### 奠基性論文

- Rastegari, M., Ordonez, V., Redmon, J., Farhadi, A. (2016). *XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks*. arXiv:1603.05279. https://arxiv.org/abs/1603.05279 — 帶每個濾波器縮放的二值濾波器；二值權重 AlexNet 與全精度相當，完全二值的 XNOR-Net 為 44.2% top-1，全精度為 56.6%。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — XNOR-Net 以縮放加以延伸的二值權重訓練方法。
- Li, F., Liu, B., Wang, X., Zhang, B., Yan, J. (2016). *Ternary Weight Networks*. arXiv:1605.04711. https://arxiv.org/abs/1605.04711 — 三值替代方案，以零值保留部分權重。

### 綜述與教科書

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 把二值卷積放在低位元方法之中。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., Adam, H., Kalenichenko, D. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 用於比較二值卷積的 8 位元整數基準。
