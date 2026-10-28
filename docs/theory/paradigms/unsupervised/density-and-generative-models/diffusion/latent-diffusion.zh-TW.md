---
translation_reviewed: 2026-10-28
---

# 潛在擴散模型

潛在擴散在預先訓練的自編碼器壓縮潛在空間中進行擴散，而不是直接在原始像素上。Rombach 等人（2022）還加入了交叉注意力，使同一個模型能以文字與其他輸入進行條件化。這個設計是 Stable Diffusion 家族的基礎。家族層級的全貌見[擴散模型](index.md)頁。

## 概述

像素空間的擴散把大部分運算花在自編碼器能緊湊表示的精細細節上。Rombach 等人將兩項工作分開：自編碼器負責感知壓縮，擴散模型在小得多的潛在空間中負責生成建模。作者描述像素空間擴散常需要數百個 GPU 日。

## 核心概念

- **感知自編碼器**：編碼器 \(E\) 與解碼器 \(D\)，訓練目標是重建影像，同時保持潛在空間緊湊。
- **潛在表示**：\(z = E(x)\)，擴散模型實際處理的表示。DDPM 目標套用在 \(z\) 上。
- **交叉注意力條件化**：去噪器中的層，讓影像特徵去注意條件的編碼，例如文字 token。
- **下採樣倍率**：潛在表示比影像小多少。這個選擇在重建品質與運算量之間取捨。

## 運作方式

訓練分兩步。先訓練（或重用）自編碼器來壓縮影像，再於潛在表示上以一般的雜訊預測損失訓練擴散模型：

\[
L_{\text{LDM}} = \mathbb{E}_{E(x),\epsilon,t,c}\big[\|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|^2\big]
\]

其中 \(\tau_\theta(c)\) 是條件 \(c\) 的編碼，去噪器透過交叉注意力關注它。取樣時在潛在空間中進行反向過程，最後由解碼器 \(D\) 把潛在表示映射回影像。

## 關鍵方法

### High-Resolution Image Synthesis with Latent Diffusion Models（Rombach 等人，2021/2022）

- **問題：** 像素空間的擴散模型訓練與取樣成本高，而且難以加入一般的條件輸入。
- **核心想法：** 在預先訓練的自編碼器潛在空間中訓練擴散模型，並加入交叉注意力層，使其能以文字、版面或其他輸入進行條件化。
- **公式或演算法：** 上述潛在損失，去噪器的中間特徵會關注條件編碼。
- **結果：** 摘要報告在影像資料上達到最先進的合成結果，在影像補全上創下新的最先進水準，並在無條件生成、語意場景合成與超解析度上取得有競爭力的結果，且運算量低於像素空間模型。摘要未給出基準數字。
- **限制：** 自編碼器限制了可以重建的精細細節。摘要未量化運算量的節省，論文主文才有。

## 關聯

- 潛在目標就是套用在潛在表示上的 [DDPM](ddpm.md) 目標。
- 潛在取樣可以使用 [DDIM](ddim.md) 較快的取樣器。
- 後來的 Transformer 去噪器是 [DiT](../../../../models/transformer/dit/index.md)。
- 文字條件化依賴[無分類器引導](classifier-free-guidance.md)。
- 去噪器的卷積與注意力層分別見[卷積網路](../../../../models/cnn/index.md)與[Transformer 與注意力](../../../../models/transformer/index.md)。

## 開放問題

- 自編碼器會損失多少重建品質？這是否限制了細緻文字或人臉的生成？
- 影片需要時間一致性，潛在空間應如何設計？

## 參考文獻

### 開創性論文

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — 提出在自編碼器潛在空間中的擴散，並以交叉注意力進行條件化。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 潛在擴散套用於潛在表示的像素空間目標。
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — 潛在擴散家族中用於文字條件化的引導方法。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 提供潛在表示所用雜訊預測目標的連續時間觀點。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 討論可延用到潛在擴散模型的設計選擇。

### 文章與文件

- Rombach, R. 等人，*Stable Diffusion* 公開版程式碼庫。https://github.com/CompVis/stable-diffusion — 潛在擴散加文字條件化的官方參考實作。
