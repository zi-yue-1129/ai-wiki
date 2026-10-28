---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow
tags:
  - 生成模型
  - 最佳傳輸
  - 非監督式學習
aliases:
  - WGAN
  - Wasserstein GAN
  - 瓦瑟斯坦生成對抗網路
---

# Wasserstein GAN（WGAN）

Wasserstein GAN 以 Wasserstein-1（推土機）距離取代原始 GAN 的 Jensen–Shannon 目標。即使生成分布與真實分布沒有重疊，它給生成器的梯度仍然有用。它是 [GAN 概覽](index.zh-TW.md)頁中兩大訓練目標家族之一。

## 概覽

Arjovsky、Chintala 與 Bottou（2017）指出，當模型與資料的支撐集不相交時，GAN 目標會失效，因為 Jensen–Shannon 散度此時為常數，不給生成器任何梯度。Wasserstein 距離對模型參數是連續的，因此在整個訓練過程中都提供可用的訊號。論文也指出，評論家的損失與樣本品質相關，因此訓練曲線可以被讀取。

## 關鍵概念

- **Wasserstein-1 距離**：把一個分布運送到另一個分布的最小成本，成本等於移動的距離。
- **Kantorovich–Rubinstein 對偶**：此距離等於所有 1-Lipschitz 函數 \(f\) 上 \(\mathbb E_{P_r}[f] - \mathbb E_{P_g}[f]\) 的上確界。
- **評論家（critic）**：近似此上確界的網路 \(f_w\)。它輸出無界的分數，而非機率。
- **Lipschitz 限制**：評論家的梯度範數至多為一的要求。WGAN 以近似方式實施。
- **權重裁剪**：最初的實施方法，每次更新後把評論家的權重限制在一個小區間內。

## 運作方式

在評論家受限於 1-Lipschitz 的前提下，Wasserstein 距離為

\[
W(P_r, P_g) = \sup_{\|f\|_L \le 1} \mathbb E_{x\sim P_r}[f(x)] - \mathbb E_{x\sim P_g}[f(x)]
\]

評論家最大化真實樣本與生成樣本之間的期望分數差；生成器則從另一側最小化同一量。以生成器 \(g_\theta(z)\) 表示，兩個損失為

\[
L_{\text{critic}} = \mathbb E_{z}[f_w(g_\theta(z))] - \mathbb E_{x}[f_w(x)], \qquad L_{\text{gen}} = -\mathbb E_{z}[f_w(g_\theta(z))]
\]

在論文的演算法中，每次生成器更新前，評論家會更新數次（論文為五次），每一步之後都裁剪其權重，並建議使用 RMSProp，作者發現以動量為基礎的最佳化器較不穩定。

## 關鍵方法

WGAN 是本維基收錄的兩種 Wasserstein 系 GAN 方法之一。兩者的差別在於如何實施 Lipschitz 限制。

- **WGAN（Arjovsky 等人，2017）**：評論家使用權重裁剪。本頁。
- **WGAN-GP（Gulrajani 等人，2017）**：以梯度懲罰取代裁剪，見 [WGAN-GP](wgan-gp.zh-TW.md)。

### Wasserstein GAN（Arjovsky 等人，2017）

- **問題：** GAN 訓練不穩定，而且當模型與資料分布相距很遠時，Jensen–Shannon 目標沒有有用的梯度。
- **核心想法：** 以近似 Wasserstein-1 距離的評論家取代判別器，並以權重裁剪使評論家大致保持 1-Lipschitz。
- **公式或演算法：** 上述的評論家與生成器損失。每一輪：以真實與生成的小批次對評論家做數次帶裁剪的更新，再做一次生成器更新。
- **結果：** 論文將訓練行為與原始 GAN 比較，並指出訓練更穩定、評論家損失與樣本品質相關，且在其實驗中模式崩潰有所減少。論文在數個影像資料集上展示生成影像。數字請見論文的表格。
- **限制：** 權重裁剪會限制評論家的容量並可能拖慢訓練，而裁剪範圍是很敏感的超參數。改以懲罰項實施限制（如 WGAN-GP）可避免這些問題。

## 關聯

- Wasserstein 距離是最佳傳輸的一種形式，而評論家即為傳輸問題的對偶位勢。這使本方法自然地連到[流模型](../flow/index.zh-TW.md)，因為後者同樣學習從雜訊到資料的傳輸映射。
- 受 Lipschitz 限制的網路與譜正規化是相關的研究脈絡，見 [Spectral Normalization](https://arxiv.org/abs/1802.05957)。
- GAN 框架與其價值函數見 [GAN 概覽](index.zh-TW.md)頁。

## 應用

WGAN 被用作影像合成實驗中穩定的訓練目標，也是後來大多數 Wasserstein GAN 工作所依據的基礎，其中以梯度懲罰的變體最為普遍。

## 開放問題

- 權重裁剪或其他限制方法，何者能在容量與穩定性之間取得最佳平衡。
- 評論家損失在不同資料集與架構上預測樣本品質的能力如何。
- 哪一種限制實施方法最能擴展到非常大的模型。

## 參考文獻

### 開創性論文

- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — 提出 Wasserstein 目標，以及以權重裁剪約束的評論家，用於 GAN 訓練。
- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS（arXiv）. https://arxiv.org/abs/1704.00028 — 以梯度懲罰取代權重裁剪，即本頁的後繼方法。
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS（arXiv）. https://arxiv.org/abs/1406.2661 — 提出 WGAN 所取代的 Jensen–Shannon GAN 目標。
- Miyato, T., et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1802.05957 — 透過正規化判別器的權重矩陣來實施 Lipschitz 限制。
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* arXiv. https://arxiv.org/abs/1801.04406 — 分析基於梯度的 GAN 訓練何時收斂，包括判別器的正則性。

## 延伸學習

- Lilian Weng, *From GAN to WGAN*。https://lilianweng.github.io/posts/2017-08-20-gan/ — 以圖示逐步推導 Wasserstein 目標。
