---
translation_reviewed: 2026-10-28
---

# DDPM：去噪擴散機率模型

DDPM（Ho、Jain 與 Abbeel，2020）是讓擴散模型能夠用於高品質影像生成的方法。它訓練一個網路，預測在隨機時間步加入乾淨影像的雜訊，然後一步一步去除雜訊來生成影像。之後的擴散模型研究大多以這個目標為基礎。家族層級的概觀請見[擴散模型](index.md)頁面。

## 概述

擴散模型最早由 Sohl-Dickstein 等人（2015）提出。它們定義了一個固定的前向過程，對資料逐步加入雜訊，以及一個可學習的反向過程，用來去除雜訊。Ho 等人（2020）指出，更簡單的訓練方式，即固定的雜訊排程加上單純的雜訊預測損失，就能產生高品質的影像樣本。論文報告，在無條件 CIFAR-10 上的 FID 為 3.17，並稱當時這是最先進的結果。

## 問題

2020 年的影像生成模型面臨一種取捨。GAN 能產生清晰的影像，但訓練不穩定，也沒有可計算的似然。以似然為基礎的模型訓練較穩定，但論文認為它們產生的樣本品質較弱。較早的擴散模型形式在原理上可以穩定訓練，但它的變分目標很難調整到影像品質良好。DDPM 要問的是：一個簡單的目標能否讓擴散模型產生高品質樣本。

## 核心想法

前向過程是一條固定的馬可夫鏈，在 \(T\) 步內加入高斯雜訊，沒有可學習的參數。反向過程則是一個網路，用來預測加在雜訊影像 \(x_t\) 上的雜訊 \(\epsilon\)。論文指出，似然的變分下界可以寫成一組去噪項的和；對這個下界加權後，會化簡為對雜訊的均方誤差。這個簡化的損失函數正是產生最佳樣本的關鍵。論文也把它與多個雜訊層級上、搭配朗之萬動力學的去噪分數比對聯繫起來。

## 演算法

令 \(\alpha_t = 1-\beta_t\)，\(\bar\alpha_t = \prod_{s\le t}\alpha_s\)。前向過程可以從 \(x_0\) 一步跳到任意時間步：

\[
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal N(0, I)
\]

簡化後的訓練損失為

\[
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

**訓練（論文演算法 1）：**重複以下步驟。取一張乾淨影像 \(x_0\)，從 \(\{1,\dots,T\}\) 中均勻抽取時間步 \(t\)，並抽取雜訊 \(\epsilon\)。對 \(\|\epsilon-\epsilon_\theta(\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon, t)\|^2\) 做一次梯度更新。

**取樣（論文演算法 2）：**從 \(x_T \sim \mathcal N(0, I)\) 開始。對 \(t = T\) 到 1，若 \(t > 1\) 則抽取 \(z \sim \mathcal N(0, I)\)（否則 \(z = 0\)），然後計算

\[
x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\epsilon_\theta(x_t, t)\Big) + \sigma_t z
\]

論文將 \(\sigma_t^2\) 固定為常數，可選 \(\beta_t\) 或 \(\tilde\beta_t\)，兩者結果相近。

**設定：**\(T = 1000\) 步，\(\beta_t\) 從 \(10^{-4}\) 到 \(0.02\) 線性增加。去噪器是帶有時間步條件的 U-Net，改編自 PixelCNN++。

## 結果

論文的表 2 比較了無條件 CIFAR-10 上的不同訓練目標。FID 以訓練集計算。

| 目標 | Inception score ↑ | FID ↓ |
|---|---|---|
| 以 \(L_{\text{simple}}\) 做 \(\epsilon\) 預測（論文的方法） | 9.46 ± 0.11 | 3.17 |
| 完整下界、固定等向共變異數的 \(\epsilon\) 預測 | 7.67 ± 0.13 | 13.51 |
| 完整下界、固定等向共變異數的 \(\tilde\mu\) 預測 | 8.06 ± 0.09 | 13.22 |

在 256×256 的 LSUN 上，表 3 報告小模型的 FID 為 Bedroom 6.36、Church 7.89、Cat 19.75，大型 Bedroom 模型為 4.90。ProgressiveGAN 則為 8.34、6.42 與 37.52。DDPM 在 Bedroom 上較好，在 Church 與 Cat 上較差，因此摘要所說的「與 ProgressiveGAN 相近」是準確的概括。

## 限制

- **取樣慢。**每個樣本需要 \(T = 1000\) 次網路評估。[DDIM](ddim.md)與[潛在擴散](latent-diffusion.md)降低了這個成本。
- **似然的取捨。**簡化損失並不是最大化似然的下界。在表 2 中，它的似然界略差（最多 3.75 bits/dim，完整下界為 3.70），因此樣本品質的提升伴隨著些微的似然損失。
- **對目標敏感。**表 2 顯示，訓練目標的選擇會使 FID 相差約四倍。這個增益取決於特定的加權方式，論文也沒有系統地測試許多替代方案。
- **結果的範圍。**主要結果來自 CIFAR-10 與幾個 256×256 的 LSUN 類別。後續研究把 DDPM 擴展到 ImageNet 與文字條件。

## 關聯

- 重用同一個已訓練模型、加速取樣的方法是 [DDIM](ddim.md)。
- 潛在空間版本是[潛在擴散](latent-diffusion.md)，其 Transformer 去噪器是 [DiT](../../../../models/transformer/dit/index.md)。
- 以類別或文字提示進行條件控制的方法，見[無分類器引導](classifier-free-guidance.md)。
- 把 DDPM 視為離散化隨機微分方程的連續時間觀點，見下方引用的 Song 等人（2021）。

## 未解問題

- 樣本品質有多少來自簡化損失，有多少來自 U-Net 與雜訊排程？
- 在不重新訓練的情況下，步數能減少到多少，代價是多少品質？
- 為什麼對下界重新加權會改善樣本，同時降低似然？

## 參考文獻

### 開創性論文

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 提出 \(L_{\text{simple}}\) 雜訊預測目標、線性排程與取樣器，並在 CIFAR-10 與 LSUN 上報告結果。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — 定義了 DDPM 所建立於其上的前向加噪鏈與可學習的反向鏈。
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — 顯示 DDPM 訓練出的模型可以用少得多的步數取樣。
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — 以架構消融與分類器引導，在 ImageNet 上擴展 DDPM。

### 綜述與教科書

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 顯示 DDPM 是變異數保持型隨機微分方程的離散化。

### 文章與文件

- Ho, J. 等人。*diffusion*，官方程式碼儲存庫。https://github.com/hojonathanho/diffusion — 作者以 TensorFlow 實作的論文實驗。

## 延伸學習

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 逐步解說 DDPM 的訓練與取樣程式，與本頁的公式相對應。
