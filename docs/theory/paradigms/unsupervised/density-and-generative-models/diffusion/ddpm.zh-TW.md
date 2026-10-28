---
translation_reviewed: 2026-10-28
---

# DDPM：去噪擴散機率模型

DDPM 是讓擴散模型能用於高品質影像生成的方法。它訓練網路預測在隨機時間步加入影像的雜訊，並逐步去除雜訊來生成樣本。之後幾乎所有擴散工作都以它為參照點。家族層級的全貌見[擴散模型](index.md)頁。

## 概述

Ho、Jain 與 Abbeel（2020）證明，固定的雜訊排程加上單純的雜訊預測損失，就足以產生樣本品質被論文描述為與 GAN 相當的結果，而且不需要對抗式訓練。更早的擴散工作（Sohl-Dickstein 等人，2015）有相同的前向與反向過程，但目標函數較複雜。

## 核心概念

- **前向過程**：固定的馬可夫鏈，在 \(T\) 步內以變異數 \(\beta_t\) 加入高斯雜訊。它沒有可學習的參數。
- **前向後驗** \(q(x_{t-1}\mid x_t, x_0)\)：前向鏈的精確高斯後驗，均值為 \(\tilde\mu_t\)、變異數為 \(\tilde\beta_t\)。它可以精確計算，訓練目標即由它建構。
- **反向過程**：可學習的高斯 \(p_\theta(x_{t-1}\mid x_t)\)，其均值由網路的雜訊預測計算得出。
- **雜訊排程** \(\beta_t\)：論文使用從 \(10^{-4}\) 到 \(0.02\) 的線性排程，共 \(T = 1000\) 步。

## 運作方式

令 \(\alpha_t = 1-\beta_t\)，\(\bar\alpha_t = \prod_{s\le t}\alpha_s\)，雜訊可以一步加入：

\[
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal N(0, I)
\]

前向後驗的均值為 \(\tilde\mu_t(x_t, x_0)\)，變異數為 \(\tilde\beta_t = \frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t\)。論文以雜訊預測器參數化反向均值：

\[
\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\epsilon_\theta(x_t, t)\Big)
\]

代入變分下界後，得到的各去噪項與多尺度的去噪分數匹配相似。去掉各步權重後，得到簡化損失

\[
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

訓練（論文的演算法 1）重複以下步驟：取乾淨影像 \(x_0\)、均勻的時間步 \(t\in\{1,\dots,T\}\) 與雜訊 \(\epsilon\)，對 \(\|\epsilon-\epsilon_\theta(\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon, t)\|^2\) 做一次梯度更新。取樣（演算法 2）從 \(x_T\sim\mathcal N(0,I)\) 開始。對 \(t\) 從 \(T\) 到 1，若 \(t>1\) 則抽取 \(z\sim\mathcal N(0,I)\)（否則 \(z=0\)），然後計算 \(x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\big) + \sigma_t z\)。論文把 \(\sigma_t^2\) 設為固定常數，取 \(\beta_t\) 或 \(\tilde\beta_t\) 皆可，並報告兩者結果相近。網路是帶有時間步條件的 U-Net。

## 關鍵方法

### Denoising Diffusion Probabilistic Models（Ho, Jain & Abbeel，2020）

- **問題：** GAN 能產生清晰影像但訓練不穩定；當時的概似模型樣本品質較弱。
- **核心想法：** 訓練網路預測在隨機時間步加入的雜訊，使用加權變分下界，它會簡化為雜訊預測。
- **公式或演算法：** 上節的 \(L_{\text{simple}}\) 損失、線性 \(\beta\) 排程，以及上節演算法 1 與 2 中跨越 \(T\) 步的祖先取樣。
- **結果：** 摘要報告在無條件 CIFAR-10 上 Inception score 為 9.46、FID 為 3.17，並描述當時達到最先進水準。摘要描述 256×256 LSUN 的樣本品質與 ProgressiveGAN 相近，但摘要中沒有數字。論文表 2 的消融實驗（無條件 CIFAR-10）顯示簡化損失的重要性。以未加權的 \(L_{\text{simple}}\) 預測 \(\epsilon\)，FID 為 3.17、IS 為 9.46；以完整變分下界與固定等向共變異數預測 \(\epsilon\)，FID 為 13.51、IS 為 7.67；以完整下界為基準的 \(\tilde\mu\) 預測，FID 為 13.22、IS 為 8.06。
- **限制：** 取樣使用 \(T=1000\) 步，因此生成需要約一千次網路評估，速度慢。摘要未報告訓練或取樣成本。[DDIM](ddim.md) 與潛在擴散處理了這個問題。

## 關聯

- 較快的取樣器是 [DDIM](ddim.md)，它重用同一個訓練好的模型。
- 潛在空間的後繼方法是[潛在擴散](latent-diffusion.md)，Transformer 後繼是 [DiT](../../../../models/transformer/dit/index.md)。
- 條件化方法是[無分類器引導](classifier-free-guidance.md)。
- 變分架構連結到[機率方法](../../../probabilistic/index.md)的背景。
- 同一目標的連續時間與流觀點見[流匹配](../flow/flow-matching/index.md)。

## 開放問題

- 樣本品質有多少來自這個簡單損失，又有多少來自 U-Net 與雜訊排程？
- 能否在不重新訓練的情況下減少步數？

## 參考文獻

### 開創性論文

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 提出雜訊預測目標，並報告高品質的 CIFAR-10 與 LSUN 樣本。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML（PMLR 37）. https://arxiv.org/abs/1503.03585 — DDPM 所建立於其上的早期擴散模型，前向與反向過程相同。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 說明 DDPM 是一種隨機微分方程的離散化。

### 文章與文件

- Ho, J., *diffusion* 官方程式碼庫。https://github.com/hojonathanho/diffusion — 作者原始 TensorFlow 實作，包含論文實驗的程式。
- Song, J., Meng, C. & Ermon, S. (2020). Denoising Diffusion Implicit Models. arXiv. https://arxiv.org/abs/2010.02502 — 說明 DDPM 訓練的模型可以用少很多的步數取樣。

## 延伸學習

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 逐步導讀 DDPM 的訓練與取樣，與本頁公式對應。
