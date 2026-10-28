---
translation_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - 生成模型
  - 最佳傳輸
  - 非監督式學習
aliases:
  - WGAN-GP
  - Improved WGAN
  - 梯度懲罰瓦瑟斯坦生成對抗網路
---

# 帶梯度懲罰的 WGAN（WGAN-GP）

WGAN-GP 保留 [WGAN](wgan.zh-TW.md) 的 Wasserstein 目標，但以梯度懲罰取代權重裁剪來實施 Lipschitz 限制。如此評論家便能發揮完整的容量，並能在更廣泛的架構上訓練。它是最普遍使用的 Wasserstein GAN 變體，在 [GAN 概覽](index.zh-TW.md)頁中與 [WGAN](wgan.zh-TW.md) 並列。

## 概覽

Gulrajani、Ahmed、Arjovsky、Dumoulin 與 Courville（2017）指出，權重裁剪會把評論家的權重推向少數極端值，限制其可表示的函數，也使訓練對裁剪範圍很敏感。他們以對評論家梯度範數的懲罰取代裁剪，懲罰施加在真實與生成樣本之間的點上。

## 關鍵概念

- **梯度懲罰**：加到評論家損失中的一項，當評論家梯度範數為一時為零，否則為正。
- **內插樣本**：真實樣本與生成樣本之間直線上的點，懲罰施加於此。
- **懲罰係數 \(\lambda\)**：懲罰的強度。論文使用 \(\lambda = 10\)。

## 運作方式

令 \(\tilde x = g_\theta(z)\)，\(\hat x = \epsilon x + (1-\epsilon)\tilde x\)，其中 \(\epsilon \sim U[0,1]\)。評論家損失為

\[
L_{\text{critic}} = \mathbb E_{\tilde x}[f_w(\tilde x)] - \mathbb E_{x}[f_w(x)] + \lambda\,\mathbb E_{\hat x}\big[(\|\nabla_{\hat x} f_w(\hat x)\|_2 - 1)^2\big]
\]

生成器損失與 WGAN 相同，即 \(-\mathbb E_z[f_w(g_\theta(z))]\)。由於懲罰項需要評論家的梯度，每一步評論家更新都要計算梯度的梯度。論文也建議評論家不要使用批次正規化，因為批次統計量會混合不同樣本，破壞逐樣本的懲罰。

## 關鍵方法

WGAN-GP 與 [WGAN](wgan.zh-TW.md) 的差別只在於如何實施 Lipschitz 限制。兩者都屬於 [GAN 概覽](index.zh-TW.md)頁中的 Wasserstein 家族。

- **WGAN（Arjovsky 等人，2017）**：權重裁剪，見 [WGAN](wgan.zh-TW.md)。
- **WGAN-GP（Gulrajani 等人，2017）**：在內插樣本上施加梯度懲罰。本頁。

### 改良的 Wasserstein GAN 訓練（Gulrajani 等人，2017）

- **問題：** [WGAN](wgan.zh-TW.md) 的權重裁剪限制了評論家，也使訓練對裁剪門檻很敏感。
- **核心想法：** 在真實與生成樣本的隨機內插點上，懲罰評論家梯度範數偏離一的程度，藉此約束評論家。
- **公式或演算法：** 上述評論家損失，\(\lambda = 10\)，生成器損失沿用 WGAN。論文每次生成器更新前，會對評論家更新數次。
- **結果：** 摘要指出，此方法可在幾乎不需超參數調校的情況下，穩定訓練多種 GAN 架構，包括深層殘差網路與離散資料上的語言模型。影像結果見論文的實驗。
- **限制：** 懲罰只在內插點上施加，因此限制只能近似地在各處成立。每個評論家步驟都需要額外的梯度計算。此方法仍需要合適的評論家架構，而論文對正規化的建議也是針對此方法而言。

## 關聯

- 此懲罰是實施 Wasserstein 距離所需 Lipschitz 限制的一種方式，[WGAN](wgan.zh-TW.md) 的參考文獻中也將其與譜正規化比較。
- Wasserstein 目標把此方法與最佳傳輸連結，而最佳傳輸也是[流模型](../flow/index.zh-TW.md)的基礎。
- 影像資料的卷積評論家屬於[卷積網路家族](../../../../models/cnn/index.zh-TW.md)。

## 應用

WGAN-GP 被用作影像與序列 GAN 中穩定的訓練目標，也常作為 GAN 比較的基準。

## 開放問題

- 基於內插的懲罰，在內插點之外是否仍能提供良好的約束。
- 在非常大的模型規模下，雙重梯度的成本。
- 此懲罰能否以更便宜的約束取代，同時不失去穩定性。

## 參考文獻

### 開創性論文

- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS（arXiv）. https://arxiv.org/abs/1704.00028 — 提出評論家的梯度懲罰，即本頁的方法。
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — 提出 WGAN-GP 所保留的 Wasserstein 目標，以及權重裁剪的版本。
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS（arXiv）. https://arxiv.org/abs/1406.2661 — 提出 Wasserstein 變體所修改的對抗框架。
- Miyato, T., et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1802.05957 — 透過正規化判別器的權重來實施 Lipschitz 限制，作為梯度懲罰的替代方案。
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* arXiv. https://arxiv.org/abs/1801.04406 — 分析 GAN 訓練的收斂性，包括對判別器的梯度懲罰。

## 延伸學習

- Lilian Weng, *From GAN to WGAN*。https://lilianweng.github.io/posts/2017-08-20-gan/ — 以圖示說明 Wasserstein 與梯度懲罰變體。
