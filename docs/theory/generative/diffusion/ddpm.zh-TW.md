---
translation_reviewed: 2026-10-28
---

# DDPM：去噪擴散機率模型

DDPM 是讓擴散模型能用於高品質影像生成的方法。它訓練網路預測在隨機時間步加入影像的雜訊，並逐步去除雜訊來生成樣本。之後幾乎所有擴散工作都以它為參照點。家族層級的全貌見[擴散模型](index.md)頁。

## 概述

Ho、Jain 與 Abbeel（2020）證明，固定的雜訊排程加上單純的雜訊預測損失，就足以產生與當時最好 GAN 相當的樣本，而且不需要對抗式訓練。更早的擴散工作（Sohl-Dickstein 等人，2015）有相同的前向與反向過程，但目標函數較複雜。

## 核心概念

- **前向過程**：固定的馬可夫鏈，在 \(T\) 步內以變異數 \(\beta_t\) 加入高斯雜訊。它沒有可學習的參數。
- **反向過程**：可學習的高斯 \(p_\theta(x_{t-1}\mid x_t)\)，其均值由網路的雜訊預測計算得出。
- **雜訊排程** \(\beta_t\)：論文使用從 \(10^{-4}\) 到 \(0.02\) 的線性排程，共 \(T = 1000\) 步。

## 運作方式

令 \(\alpha_t = 1-\beta_t\)，\(\bar\alpha_t = \prod_{s\le t}\alpha_s\)，雜訊可以一步加入：

\[
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal N(0, I)
\]

論文指出，變分下界在加權後可簡化為

\[
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

訓練時取一張乾淨影像、一個隨機的 \(t\) 與雜訊 \(\epsilon\)，對這個損失做一次梯度更新。取樣從 \(x_T \sim \mathcal N(0, I)\) 開始，套用學到的反向更新 \(T\) 次，除最後一步外每步都加入新雜訊。網路是帶有時間步條件的 U-Net。

## 關鍵方法

### Denoising Diffusion Probabilistic Models（Ho, Jain & Abbeel，2020）

- **問題：** GAN 能產生清晰影像但訓練不穩定；當時的概似模型樣本品質較弱。
- **核心想法：** 訓練網路預測在隨機時間步加入的雜訊，使用加權變分下界，它會簡化為雜訊預測。
- **公式或演算法：** 上節的 \(L_{\text{simple}}\) 損失，搭配線性 \(\beta\) 排程與跨越 \(T\) 步的祖先取樣。
- **結果：** 摘要報告在無條件 CIFAR-10 上 Inception score 為 9.46、FID 為 3.17，並描述當時達到最先進水準。摘要描述 256×256 LSUN 的樣本品質與 ProgressiveGAN 相近，但摘要中沒有數字。
- **限制：** 取樣需要數百次網路評估，生成速度慢。摘要未報告訓練或取樣成本。[DDIM](ddim.md) 與潛在擴散處理了這個問題。

## 關聯

- 較快的取樣器是 [DDIM](ddim.md)，它重用同一個訓練好的模型。
- 潛在空間的後繼方法是[潛在擴散](latent-diffusion.md)，Transformer 後繼是 [DiT](dit.md)。
- 條件化方法是[無分類器引導](classifier-free-guidance.md)。
- 變分架構連結到[機率方法](../../probabilistic/index.md)的背景。

## 開放問題

- 樣本品質有多少來自這個簡單損失，又有多少來自 U-Net 與雜訊排程？
- 能否在不重新訓練的情況下減少步數？

## 參考文獻

### 開創性論文

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 提出雜訊預測目標，並報告高品質的 CIFAR-10 與 LSUN 樣本。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — DDPM 所建立於其上的早期擴散模型，前向與反向過程相同。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 說明 DDPM 是一種隨機微分方程的離散化。

### 文章與文件

- Ho, J., *diffusion* 官方程式碼庫。https://github.com/hojonathanho/diffusion — 作者原始 TensorFlow 實作，包含論文實驗的程式。
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — 說明 DDPM 訓練的模型可以用少很多的步數取樣。
