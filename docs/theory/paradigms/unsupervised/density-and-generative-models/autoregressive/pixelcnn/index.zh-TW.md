---
translation_reviewed: 2026-10-28
---

# PixelCNN

PixelCNN 是一種自回歸的自然影像模型，它用一疊遮罩卷積，由每個像素之前的像素預測該像素。它與其遞迴型的同類模型 PixelRNN 一同由 van den Oord、Kalchbrenner 與 Kavukcuoglu（2016）提出，是 [自回歸生成模型](../index.md)概述中的代表性方法之一。

## 概述

自回歸影像模型把影像的分布分解為每個像素一個條件分布，並依固定順序排列。PixelRNN 以二維 LSTM 層計算每個條件分布，它能提供很大的上下文，但必須一步接一步計算。

PixelCNN 保留相同的分解方式，但以遮罩卷積取代遞迴層，遮罩會阻止每次預測使用排在後面的像素。由於卷積可以同時計算所有位置，訓練影像中所有像素的條件分布都能平行計算。代價是上下文有限：在原始實驗中，上下文最小的卷積模型，在三個被比較的模型中準確度最低。兩者的採樣仍然都必須依序進行。

## 核心概念

- **光柵順序**：像素依序由左上到右下逐列走訪。某個像素的條件分布只依賴此順序中排在它前面的像素。
- **遮罩卷積**：把濾波器中會接觸到尚未生成像素的權重設為零的卷積。第一層使用遮罩 A，後續各層使用遮罩 B，後者允許顏色通道與自身相連。
- **離散 softmax 輸出**：每個顏色通道取 256 個值之一，網路輸出它們上的類別分布。
- **盲點**：單一遮罩堆疊會忽略當前像素之前的一部分像素。Gated PixelCNN 以兩個堆疊移除了盲點。

## 運作方式

對於 \(n \times n\) 像素的影像 \(x\)，模型定義

\[
p(x) = \prod_{i=1}^{n^2} \prod_{c \in \{R, G, B\}} p\big(x_{i,c} \mid x_{<i},\, x_{i,<c}\big)
\]

其中 \(x_{i,<c}\) 是同一像素中排在通道 \(c\) 之前的顏色值。每個因子都是 256 個值上的 softmax。訓練時最大化對數似然，結果以每維位元數（bits per dimension）報告，即以 2 為底的平均負對數似然除以影像中的數值個數。[^1]

1. **訓練。** 對整張影像做一次遮罩計算，就能同時算出所有條件分布，因為真實像素值已知。
2. **採樣。** 從空白影像開始。依光柵順序，對每個像素與每個顏色通道執行網路、從 softmax 中抽取一個值，並寫回影像。一張 32 × 32 的 RGB 影像需要 3,072 次網路計算。

## 結果

- **CIFAR-10，測試集。** PixelRNN 論文報告的每維位元數：PixelCNN 為 3.14，Row LSTM 為 3.07，Diagonal BiLSTM 為 3.00；後者的上下文在三者中最大。
- **Gated PixelCNN。** 後續論文加入了閘控單元與雙堆疊設計。它在 CIFAR-10 測試集上報告 3.03 位元，比 PixelCNN 好 0.11；在 ImageNet 上，32 × 32 與 64 × 64 分別為 3.83 與 3.57，略優於 PixelRNN。作者表示，它與 PixelRNN 的表現相當，但訓練時間不到一半。[^2]

## 限制

- **上下文有限與採樣緩慢。** 感受野只隨深度增長，而生成時每個顏色值都需要一次網路計算。
- **離散輸出。** 256 類的 softmax 把相鄰的亮度視為彼此無關的類別。PixelRNN 的作者指出，模型並不知道像素值 51 與 52 是相鄰的。PixelCNN++ 以離散化的邏輯斯諦混合取代 softmax，作者報告它能加快訓練。[^3]

## 未解問題

- **上下文與平行性的取捨。** 目前不清楚，僅靠加深網路能否在保持訓練平行的同時，縮小與遞迴模型之間的差距。
- **順序。** 光柵順序是一種選擇，而這些論文並未測試其他順序。
- **像素與編碼。** 以一小格學得的編碼為對象的 PixelCNN 先驗，比以每個像素為對象的先驗便宜，正如 [VQ-VAE](../../vae/vq-vae/index.md) 中所示，但在同等品質下是否總是如此，仍在研究中。

## 與其他主題的連結

- **母主題。** 本模型所共用的分解、遮罩與採樣程序，也適用於 [自回歸生成模型](../index.md)這一整個家族。
- **音訊。** [WaveNet](../wavenet/index.md) 把同樣的設計改為對音訊樣本做因果卷積。
- **Transformer。** [Image GPT](../image-gpt/index.md) 則以自注意力來處理下一像素的目標。

## 應用

- **類別條件生成。** 以類別標籤或學得的嵌入作為條件，可以得到指定類別的多樣影像（van den Oord 等人，2016b）。
- **編碼的先驗。** PixelCNN 為 [VQ-VAE](../../vae/vq-vae/index.md) 影像生成器建模離散編碼。

[^1]: 每維位元數是以 2 為底的平均負對數似然，再除以影像中的數值個數（32 × 32 的 RGB 影像為 3,072）。數值越低越好。

[^2]: 文中的 PixelRNN ImageNet 數字取自 Gated PixelCNN 論文中的表格。原始 PixelRNN 論文報告的 ImageNet 結果是在驗證集上得到的，因此兩組數字並不嚴格可比。

[^3]: PixelCNN++ 摘要列出的修改包括邏輯斯諦混合、降採樣、捷徑連接與 dropout，並報告了該模型在 CIFAR-10 上的最佳對數似然結果。

## 參考文獻

### 開創性論文

- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. ICML (PMLR 48). https://arxiv.org/abs/1601.06759 — 提出 PixelRNN 與 PixelCNN，並在 MNIST、CIFAR-10 與 ImageNet 上報告結果。
- van den Oord, A., Kalchbrenner, N., Vinyals, O., Espeholt, L., Graves, A. & Kavukcuoglu, K. (2016). *Conditional Image Generation with PixelCNN Decoders*. arXiv. https://arxiv.org/abs/1606.05328 — 加入閘控單元與雙堆疊設計，以消除盲點。
- Salimans, T., Karpathy, A., Chen, X. & Kingma, D. P. (2017). *PixelCNN++: Improving the PixelCNN with Discretized Logistic Mixture Likelihood and Other Modifications*. arXiv. https://arxiv.org/abs/1701.05517 — 以邏輯斯諦混合取代 256 類 softmax，並加入捷徑連接。
- Germain, M., Gregor, K., Murray, I. & Larochelle, H. (2015). *MADE: Masked Autoencoder for Distribution Estimation*. arXiv. https://arxiv.org/abs/1502.03509 — 對自編碼器加上遮罩，使每個輸出只依賴較早的輸入。

### 綜述與教科書

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — 比較自回歸模型與其他深度生成模型家族。
