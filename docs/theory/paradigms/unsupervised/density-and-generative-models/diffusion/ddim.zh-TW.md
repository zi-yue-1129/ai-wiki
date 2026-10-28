---
translation_reviewed: 2026-10-28
---

# DDIM：去噪擴散隱式模型

DDIM 是擴散模型的一種取樣器，它重用以 DDPM 目標訓練好的模型，但能以少得多的步數生成。它改變了反向過程，使其不再是馬可夫鏈，因此可以跳過某些步驟。家族層級的全貌見[擴散模型](index.md)頁，訓練目標見 [DDPM](ddpm.md)。

## 概述

DDPM 透過模擬約一千步的馬可夫鏈來生成樣本。Song、Meng 與 Ermon（2021）觀察到，同一個訓練目標與一族非馬可夫前向過程都相容。這一族中的每個成員給出相同的雜訊預測器，但取樣規則不同。其中一個成員是確定性取樣器，且可以使用任意步數。

## 核心概念

- **非馬可夫前向過程**：每個帶噪樣本 \(x_t\) 依賴於乾淨影像 \(x_0\)，而不只是 \(x_{t-1}\)。訓練損失不變。
- **確定性取樣**：每一步不加入新的雜訊，因此相同的起始雜訊總會產生相同的影像。
- **步數子序列**：取樣可以使用訓練時間步中遞增的子集 \(\tau_1 < \dots < \tau_S\)，因此步數 \(S\) 是可自由選擇的參數。
- **隨機性 \(\sigma\)**：每一步可調的參數。取 DDPM 的值即還原祖先取樣，\(\sigma = 0\) 則得到 DDIM。

## 運作方式

給定網路的雜訊預測 \(\epsilon_\theta(x_t, t)\)，預測的乾淨影像為

\[
\hat x_0 = \frac{x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta(x_t,t)}{\sqrt{\bar\alpha_t}}
\]

下一個雜訊較少的樣本為

\[
x_{t_{\text{prev}}} = \sqrt{\bar\alpha_{t_{\text{prev}}}}\,\hat x_0 + \sqrt{1-\bar\alpha_{t_{\text{prev}}}-\sigma^2}\,\epsilon_\theta(x_t,t) + \sigma\,z
\]

其中 \(z\sim\mathcal N(0,I)\) 是新的雜訊，\(\sigma\) 控制隨機性。令 \(\sigma = 0\) 即得確定性取樣器。當 \(\sigma\) 取 DDPM 的值時，更新式會還原為祖先取樣，因此 DDIM 包含 DDPM 作為特例。任何 \(\sigma\) 的選擇都重用同一個訓練好的模型。

## 關鍵方法

### Denoising Diffusion Implicit Models（Song、Meng 與 Ermon，2021）

- **問題：** DDPM 取樣需要很多次網路評估，而其馬可夫反向鏈無法跳步。
- **核心想法：** 保留 DDPM 的訓練目標，但使用非馬可夫前向過程，使反向更新可以套用在較短的步數子序列上。
- **公式或演算法：** 上述更新式，確定性取樣時 \(\sigma = 0\)。論文的式 12 即是以 \(\alpha_t\) 表示累積乘積的同一更新式。
- **結果：** 摘要報告 DDIM 產生高品質樣本的速度，以實際時間計，比 DDPM 快 10 到 50 倍。在無條件 CIFAR-10 上（論文表 1），DDIM 以 50 步得到 FID 4.67，100 步為 4.16，1000 步為 4.04。DDPM 同樣步數分別為 8.01、5.78 與 4.73。步數為 10 時差距最大：DDIM 為 13.36，DDPM 為 41.07。
- **限制：** 步數非常少時品質仍會下降，如 10 步的結果所示。加速是以論文設定中的實際時間衡量，而論文本身在不同段落分別引用了 10 到 50 倍與 10 到 100 倍兩種說法。確定性取樣器對每個起始雜訊只給出一個輸出，因此無法取得 DDPM 那樣的隨機多樣性。

## 關聯

- 訓練目標來自 [DDPM](ddpm.md)。
- 其他取樣與蒸餾構想整理在[擴散模型](index.md)頁的較快取樣段落。
- [潛在擴散](latent-diffusion.md)中的潛在空間取樣可以使用 DDIM 式的更新。
- 確定性取樣器的機率流常微分方程觀點，見下方參考文獻中的 Song 等人（2021）。

## 開放問題

- 確定性取樣器在多少步時品質會崩潰，這是否取決於影像領域？
- 對於特定的多樣性與速度取捨，哪一種取樣器最好？

## 參考文獻

### 開創性論文

- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — 提出非馬可夫取樣器，並在表 1 中給出 CIFAR-10 的 FID 與步數。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — DDIM 所加速的訓練目標與馬可夫取樣器。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 將確定性取樣器表示為機率流常微分方程。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 比較各擴散模型的取樣排程與求解器。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — DDIM 所推廣的原始馬可夫鏈取樣器。

## 延伸學習

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 導讀 DDIM 所推廣的 DDPM 取樣器。
