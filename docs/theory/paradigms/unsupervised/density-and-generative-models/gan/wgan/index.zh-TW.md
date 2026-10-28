---
translation_reviewed: 2026-10-28
---

# Wasserstein GAN

Wasserstein GAN（WGAN）由 Arjovsky、Chintala 與 Bottou（2017）提出，它以 Earth Mover 距離（也稱 Wasserstein-1 距離）取代原始 GAN 基於 Jensen–Shannon 的目標。判別器變成一個輸出實數而非機率的*評論家*，其損失追蹤生成樣本與資料之間的距離。WGAN 是[生成對抗網路](../index.md)主題中的代表性方法之一。

## 概述

原始 GAN 的準則與 Jensen–Shannon 散度密切相關（見[原始 GAN](../original-gan/index.md)頁）。論文主張，當資料分布與生成器分布位於互不重疊的低維流形上時，這個散度是很差的訓練訊號。此時散度保持常數，生成器的梯度為零，即使樣本離資料很遠。相較之下，Earth Mover 距離仍會隨生成器的移動而平滑變化，因此能提供可用的梯度。論文把這個觀察轉化為一套訓練演算法。

## 核心概念

- **Earth Mover（Wasserstein-1）距離**：把機率質量從一個分布搬運到另一個分布的最小成本，成本由距離給定。
- **Kantorovich–Rubinstein 對偶性**：此距離等於所有 1-Lipschitz 函數 \(f\) 中，\(f\) 在真實資料與生成資料上期望值之差的上確界。
- **評論家**：近似該上確界的網路 \(f_w\)。它沒有 sigmoid 輸出，因此分數不是機率。
- **Lipschitz 約束**：評論家必須是 1-Lipschitz，也就是其輸出的變化速度不能超過輸入。論文以把權重裁剪到一個小範圍內的方式近似地執行這個約束。

## 運作方式

評論家最大化距離的估計，生成器則使它最小化：

\[
\max_{w \in \mathcal{W}} \; \mathbb{E}_{x \sim P_r}\big[f_w(x)\big] - \mathbb{E}_{z \sim p(z)}\big[f_w(g_\theta(z))\big], \qquad \min_\theta \; -\mathbb{E}_{z \sim p(z)}\big[f_w(g_\theta(z))\big]
\]

其中 \(P_r\) 是資料分布，\(g_\theta\) 是生成器，\(\mathcal{W}\) 是評論家權重的集合。論文的演算法 1 如下進行：

1. 重複 \(n_{\text{critic}}\) 次：取 \(m\) 個真實樣本與 \(m\) 個雜訊向量，以 RMSProp 沿著上述估計的梯度更新評論家權重，然後把每個權重裁剪到 \([-c, c]\)。
2. 取 \(m\) 個雜訊向量，以 RMSProp 沿著 \(-\frac{1}{m}\sum_i f_w(g_\theta(z^{(i)}))\) 的梯度更新生成器參數。

論文所有實驗都使用學習率 \(\alpha = 0.00005\)、裁剪參數 \(c = 0.01\)、批次大小 \(m = 64\) 與 \(n_{\text{critic}} = 5\)。作者選擇 RMSProp 而非 Adam，因為他們發現基於動量的最佳化器會使評論家非平穩的損失變得不穩定。

## 結果

論文提供三類證據。其影像實驗使用 LSUN-Bedrooms 資料集，並以 DCGAN 作為基準。

- **損失與品質。**與標準 GAN 基於判別器的估計不同，評論家對距離的估計會隨樣本品質提升而下降。論文報告，它與目視品質相關，因此有助於除錯與比較超參數設定。
- **架構穩健性。**論文訓練了一個卷積生成器、一個沒有批次正規化且濾波器數量固定的 DCGAN 生成器，以及一個具有 512 個隱藏單元、四層 ReLU 的 MLP 生成器。作者指出，這後兩種生成器在標準 GAN 中已知表現很差，並報告 WGAN 在三種生成器上都保持穩健。
- **模式崩潰。**論文指出，在任何實驗中都未見 WGAN 演算法出現模式崩潰的跡象。

## 限制

- **權重裁剪。**論文稱以裁剪來執行 Lipschitz 約束是「明顯很糟的做法」。若裁剪上限很大，權重需要很長時間才會到達上限；若上限很小，深層評論家的梯度可能消失。
- **評論家訓練緩慢。**每次生成器更新都需要數次評論家更新，因此訓練成本較高。
- **最佳化器敏感性。**學習率過高或使用基於動量的最佳化器時，訓練會不穩定，如上所述。
- **跨模型比較分數。**估計值會因評論家的架構而有一個常數倍率，因此使用不同評論家的模型之間，分數難以比較。

## 開放問題

- 在大規模下，哪一種 Lipschitz 約束的實施方式最好？Gulrajani 等人（2017）以梯度懲罰取代裁剪，Miyato 等人（2018）則約束每一層的譜範數。
- 應如何在不同架構之間為 GAN 樣本評分？單靠評論家的數值並不公平，後來因此出現了 Fréchet Inception 距離等基於樣本的指標。

## 參考文獻

### 開創性論文

- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — 論文本身：Wasserstein 目標、演算法 1、訓練分析與本頁所述的影像實驗。
- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — 原始 GAN 目標，WGAN 取代其 Jensen–Shannon 準則。
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1701.04862 — 分析原始目標的飽和與不穩定，這正是 WGAN 所要解決的問題。
- Gulrajani, I. et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS. https://arxiv.org/abs/1704.00028 — 以梯度懲罰取代評論家中的權重裁剪，並報告更可靠的訓練。
- Miyato, T. et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1802.05957 — 透過正規化每個權重矩陣的譜範數，對判別器施加 Lipschitz 約束。

### 綜述與教科書

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — 為訊號處理讀者撰寫的 GAN 目標與訓練方法綜述。

### 講座與影片

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — 作者關於 GAN 目標與訓練方法的教學報告，包括改變損失函數的各種變體，並附有習題。
