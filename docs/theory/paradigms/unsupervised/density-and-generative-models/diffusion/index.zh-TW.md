---
translation_reviewed: 2026-10-28
---

# 擴散模型

擴散模型是一類生成網路，透過逆轉逐步加噪的過程來產生資料。今日大多數影像、影片與音訊生成器都以它為基礎。擴散是一種生成演算法，因此它的一般定位在[生成模型](../generative-models/index.md)之中。本頁說明演算法本身：前向與反向過程、如何以文字或其他輸入為去噪網路設定條件，以及如何抽取樣本。執行去噪的網路屬於一般的架構家族，分別見[卷積網路](../../../../models/cnn/index.md)與[Transformer 與注意力](../../../../models/transformer/index.md)。

## 概述

擴散模型有兩個過程。**前向過程**在 \(T\) 步內對資料樣本 \(x_0\) 加入高斯雜訊，直到接近純雜訊 \(x_T\)。這個過程不需要學習。**反向過程**則是一個神經網路 \(\epsilon_\theta(x_t, t)\)，經訓練以預測每一步加入的雜訊。生成從隨機雜訊開始，套用學到的反向步驟，直到得到樣本 \(x_0\)。

與其他生成模型家族相比，擴散模型以速度換取穩定性與品質。訓練只是簡單的迴歸問題，避免了對抗式訓練的不穩定，但取樣需要很多次網路評估。近期許多研究都在降低這個成本。

## 核心概念

- **雜訊排程**：每一步加入多少雜訊，常寫作 \(\bar\alpha_t\)。
- **去噪器**：從帶噪輸入與時間步預測雜訊（或乾淨影像，或速度）的網路。
- **骨幹**：去噪器的架構。早期的影像模型使用 U-Net，即帶有跳接的卷積網路；較新的模型則在潛在影像的圖塊上使用 Transformer。
- **潛在擴散**：在自編碼器壓縮後的潛在空間中進行擴散，而不是直接在原始像素上進行。
- **條件化**：提供額外的輸入，例如類別標籤或文字提示，去噪器透過交叉注意力或在其層中加入這些輸入來使用它們。
- **無分類器引導**：結合條件預測與無條件預測，以加強條件控制的方法。
- **取樣器**：把反向步驟轉換成取樣程序的規則，例如 DDPM 的祖先取樣或 [DDIM](ddim.md)。

## 運作方式

最簡單的訓練目標是雜訊預測損失：

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big], \qquad x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon
\]

每個訓練樣本都是一張乾淨影像，搭配隨機的時間步與隨機雜訊。網路看到帶噪輸入與時間步，學會預測雜訊。取樣則是一連串迭代更新，在每一步去除一部分預測出的雜訊。[DDPM](ddpm.md) 以簡化的損失引入了這個目標，這已足以產生高品質影像。

### 骨幹

- **U-Net**：帶有跳接、並在較低解析度使用注意力的卷積編碼器—解碼器。它是像素空間影像模型的預設骨幹。
- **Transformer（DiT）**：潛在表徵被切成圖塊，每個圖塊成為一個 token，再由 Transformer 處理。時間步與類別標籤透過自適應層正規化注入。Peebles 與 Xie（2023）報告，隨著模型的 Gflops 增加，FID 會改善。

### 潛在擴散與條件化

潛在擴散先以預先訓練的自編碼器壓縮影像，再於小得多的潛在空間上做擴散，從而降低每一步去噪的記憶體與計算成本。[潛在擴散](latent-diffusion.md)（Rombach 等人，2022）在去噪器中加入交叉注意力，連接文字編碼器或其他條件輸入的嵌入，並把同一個架構框架應用於圖像修補與超解析度等任務。

### 加速取樣

若不加處理，取樣所需的步數與訓練時一樣多。下列三類方法可降低步數：

- **非馬可夫取樣器**，例如 [DDIM](ddim.md)，重用同一個已訓練的模型，以少得多的步數取樣。在無條件 CIFAR-10 上，DDIM 用 50 步即可達到 FID 4.67，而 DDPM 在相同步數下為 8.01。
- **蒸餾**訓練一個學生模型，讓它以一步匹配教師模型的兩步取樣。Salimans 與 Ho（2022）逐步套用這個方法，每一輪把步數減半。
- **引導**在取樣時以多樣性換取對提示的忠實度。[無分類器引導](classifier-free-guidance.md)不需要另外的分類器，只需要模型自己的條件與無條件預測。

## 主要方法

每個有名稱的方法都有自己的頁面，內容包括問題、核心想法、公式、結果與限制。

- [DDPM](ddpm.md)（Ho、Jain 與 Abbeel，2020）：雜訊預測目標，以及讓擴散模型在影像上變得實用的取樣器。
- [DDIM](ddim.md)（Song、Meng 與 Ermon，2021）：非馬可夫取樣器，重用 DDPM 模型，以少得多的步數取樣。
- [一致性模型與快速取樣器](consistency-models.md)（Song 等人，2023）：把軌跡上的任一點映射到其輸出，支援一步生成。
- [潛在擴散](latent-diffusion.md)（Rombach 等人，2022）：在自編碼器的潛在空間中進行擴散，並以交叉注意力做條件化。
- [DiT](../../../../models/transformer/dit/index.md)（Peebles 與 Xie，2023）：以 Transformer 取代 U-Net 的去噪器，且隨計算量擴展。
- [無分類器引導](classifier-free-guidance.md)（Ho 與 Salimans，2022）：不需要另外分類器的條件控制方法。

### 比較

| 方法 | 改變了什麼 | 去噪器 | 條件化 |
|---|---|---|---|
| [DDPM](ddpm.md) | 訓練目標與馬可夫取樣器 | U-Net | 時間步 |
| [DDIM](ddim.md) | 同一個已訓練模型上的非馬可夫取樣器 | 與 DDPM 相同 | 與 DDPM 相同 |
| [潛在擴散](latent-diffusion.md) | 在自編碼器潛在空間中擴散 | U-Net | 交叉注意力 |
| [DiT](../../../../models/transformer/dit/index.md) | 作用在潛在圖塊上的 Transformer 去噪器 | Transformer | 時間步與類別標籤，透過自適應層正規化 |
| [無分類器引導](classifier-free-guidance.md) | 取樣時結合兩種預測 | 任意 | 引導權重 \(w\)；\(w = 0\) 即為單純的條件模型 |

## 關聯

- **生成建模：**擴散是數種生成演算法之一，與自迴歸模型、VAE 與 GAN 並列，詳見[生成模型](../generative-models/index.md)。
- **Transformer：**DiT 骨幹重用了 [Transformer 與注意力](../../../../models/transformer/index.md)中的注意力機制。
- **卷積網路：**U-Net 骨幹由[卷積網路](../../../../models/cnn/index.md)中的層構成。
- **腦與心智：**條件式擴散模型已被用來從 fMRI 記錄重建影像，例如 MinD-Vis（Chen 等人，2023），見[腦機介面](../../../../../brain-mind/bci/index.md)。若要比較大腦自身的學習與這些訓練目標，見 [NeuroAI](../../../../../brain-mind/neuroai/index.md)。

## 應用

- **文字生成影像與編輯：**潛在擴散模型可以從文字生成影像，同一框架也支援圖像修補與超解析度（Rombach 等人，2022）。
- **影片：**Ho 等人（2022）把影像架構擴展到影片，並在影像與影片資料上聯合訓練。
- **機器人控制：**Chi 等人（2023）把視覺運動策略表示為條件式去噪擴散過程，並在 15 項任務上報告優於早期機器人學習方法的結果。
- **腦解碼：**MinD-Vis（Chen 等人，2023）以 fMRI 訊號為條件，重建受試者所看到的影像。

## 未解問題

- 取樣步數可以減少到多少，而不損失品質或多樣性？
- 對於影片，Transformer 骨幹是否比 U-Net 擴展得更好，代價又是多少？
- 引導的好處中，有多少是模型真正的改進，又有多少是以多樣性換來的取捨？

## 參考文獻

### 開創性論文

- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — 把擴散模型定義為逐步加噪的過程，搭配可學習的反向過程。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 把訓練簡化為雜訊預測，並展示高品質的影像生成。
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — 非馬可夫取樣器，能以少得多的步數達到 1000 步的品質。
- Rombach, R. 等人（2022）。High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — 在自編碼器潛在空間中擴散，並以交叉注意力做條件化。
- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV. https://arxiv.org/abs/2212.09748 — 以 Transformer 取代 U-Net，並顯示 FID 隨計算量改善。
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — 結合條件與無條件預測的引導方法，不需要外部分類器。
- Salimans, T. & Ho, J. (2022). Progressive Distillation for Fast Sampling of Diffusion Models. ICLR. https://arxiv.org/abs/2202.00512 — 把取樣器蒸餾為步數減半的模型，並反覆套用。
- Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M. & Fleet, D. J. (2022). Video Diffusion Models. NeurIPS. https://arxiv.org/abs/2204.03458 — 把影像擴散擴展到影片，並在影像與影片資料上聯合訓練。
- Chi, C. 等人（2023）。Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. RSS. https://arxiv.org/abs/2303.04137 — 把機器人策略表示為條件式去噪擴散過程。
- Chen, Z. 等人（2023）。Seeing Beyond the Brain: Conditional Diffusion Model with Sparse Masked Modeling for Vision Decoding. CVPR. https://arxiv.org/abs/2211.06956 — 以 fMRI 訊號為條件的擴散模型，用來重建受試者所看到的影像。

### 綜述與教科書

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 把擴散模型與分數模型統一為隨機微分方程。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 把擴散模型的設計選擇分開，使每一項都能單獨調校。

### 文章與文件

- Rombach, R. 等人。*latent-diffusion*，官方程式碼儲存庫。https://github.com/CompVis/latent-diffusion — 作者實作的潛在擴散模型及其實驗。

## 延伸學習

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — 逐步解說 DDPM 的程式碼，適合用來核對本頁的公式。
