---
translation_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - 生成模型
  - 卷積網路
  - 非監督式學習
aliases:
  - DCGAN
  - 深度卷積 GAN
  - Deep convolutional GAN
---

# 深度卷積生成對抗網路（DCGAN）

DCGAN 是一組從卷積層建構 GAN 的架構規則，目的是讓影像上的訓練穩定。它是影像 GAN 的標準起點，[GAN 概覽](index.md)頁把它與 Wasserstein 變體並列。

## 概覽

當時的 GAN 很難在影像上訓練，而且鮮少使用卷積架構。Radford、Metz 與 Chintala（2016）找到一組卷積設計的組合，能在多個影像資料集上穩定訓練，並且顯示判別器學到的特徵可以用於其他任務。

## 關鍵概念

- **步幅卷積（strided convolution）**：判別器以學習得來的步幅卷積取代池化來降採樣。
- **分數步幅（轉置）卷積**：生成器以可學習的層來升採樣，而非固定的插值。
- **批次正規化**：在兩個網路中都使用，但生成器的輸出層與判別器的輸入層除外。
- **LeakyReLU 與 ReLU**：判別器使用 LeakyReLU，生成器使用 ReLU，輸出端使用 tanh。

## 運作方式

生成器接收雜訊向量 \(z\)（論文中為均勻分布抽樣），投影到一個小的空間網格，再套用一疊轉置卷積，得到 64 乘 64 的影像。判別器以步幅卷積對稱地建構，最後接一個 sigmoid 單元。論文去除隱藏的全連接層，改用卷積堆疊，並在原本會放全連接層的位置使用全域平均池化。

訓練目標是 Goodfellow 等人（2014）的原始極小極大 GAN 損失，搭配非飽和的生成器更新。論文使用 Adam，學習率 0.0002，\(\beta_1 = 0.5\)。

## 關鍵方法

DCGAN 是卷積 GAN 的配方，而不是獨立的訓練目標。它在 [GAN 概覽](index.md)頁與其他 GAN 變體一起比較。它在家族中的鄰居是 [WGAN](wgan.md) 與 [WGAN-GP](wgan-gp.md)，這兩者改變的是目標而非架構。

### 深度卷積生成對抗網路（Radford 等人，2016）

- **問題：** 原始 GAN 使用全連接網路，在影像上不穩定。早期的卷積嘗試也不可靠。
- **核心想法：** 一組固定的卷積設計規則（步幅與轉置卷積、批次正規化、LeakyReLU 與 ReLU 激活、不使用隱藏的全連接層），使對抗賽局能在自然影像上訓練。
- **公式或演算法：** 使用 [GAN 概覽](index.md)頁的 GAN 價值函數，並以上述架構最佳化。每一步以一個真實與一個生成的小批次更新判別器，再更新生成器。
- **結果：** 論文展示臥室與人臉的生成影像、潛在空間內插，以及人臉屬性上的簡單向量運算。它也在影像分類上評估判別器學到的特徵。確切數字請見論文。
- **限制：** 單靠架構無法消除 GAN 一般的問題，例如模式覆蓋與缺乏似然函數。向量運算顯示潛在空間有一些結構，但並非解耦。此工作針對 64 乘 64 的影像。

## 關聯

- DCGAN 是[卷積網路家族](../../../../models/cnn/index.md)中處理影像的卷積網路。
- 相同的訓練配方也適用於 [VAE](../vae/index.md) 與[流模型](../flow/index.md)的影像模型，它們同樣使用卷積編碼器或流。
- DCGAN 所依賴的批次正規化，是由 Ioffe 與 Szegedy（2015）提出的；見下方參考文獻。

## 應用

論文自己的實驗是小型影像合成任務。DCGAN 式的生成器成為影像 GAN 研究的預設基準，而其判別器特徵則作為非監督式的影像表示。

## 開放問題

- 這些設計規則能否在不修改的情況下，推廣到更高的解析度。
- 穩定性有多少來自架構，又有多少來自最佳化器設定。
- 潛在空間的向量運算是否在一般情況下對應有意義的語意方向。

## 參考文獻

### 開創性論文

- Radford, A., Metz, L. & Chintala, S. (2016). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR（arXiv）. https://arxiv.org/abs/1511.06434 — 提出 DCGAN，並給出在影像上穩定訓練卷積 GAN 的架構指引。
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS（arXiv）. https://arxiv.org/abs/1406.2661 — 提出 DCGAN 所訓練的對抗框架與價值函數。
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. arXiv. https://arxiv.org/abs/1502.03167 — 提出批次正規化，這是 DCGAN 為了穩定訓練而依賴的層之一。
- Salimans, T., et al. (2016). *Improved Techniques for Training GANs*. arXiv. https://arxiv.org/abs/1606.03498 — 彙整 GAN 的訓練技巧，包括特徵匹配與小批次判別，用來處理同樣的穩定性問題。
- Zhu, J.-Y., et al. (2017). *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks*. arXiv. https://arxiv.org/abs/1703.10593 — 在影像到影像的轉換中使用 DCGAN 式的卷積生成器。

## 延伸學習

- Lilian Weng, *From GAN to WGAN*。https://lilianweng.github.io/posts/2017-08-20-gan/ — 為初學者提供 GAN 訓練與 Wasserstein 變體的推導與圖示。
