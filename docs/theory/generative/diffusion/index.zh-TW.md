---
translation_reviewed: 2026-10-28
---

# 擴散模型

擴散模型是一類生成網路，透過逆轉逐步加噪的過程來產生資料。今日大多數影像、影片與音訊生成器都以它為基礎。擴散是一種生成演算法，其一般位置在[生成模型](../index.md)中。本頁討論演算法本身：前向與反向過程、去噪網路如何以文字或其他輸入進行條件化，以及如何取樣。執行去噪的網路屬於一般架構家族，見[卷積網路](../../models/cnn/index.md)與[Transformer 與注意力](../../models/transformer/index.md)。

## 概述

擴散模型有兩個過程。**前向過程**在 \(T\) 步內對資料樣本 \(x_0\) 加入高斯雜訊，直到接近純雜訊 \(x_T\)，這個過程不需要學習。**反向過程**則是一個神經網路 \(\epsilon_\theta(x_t, t)\)，訓練它預測每一步被加入的雜訊。生成時從隨機雜訊開始，逐步套用學到的反向步驟，直到出現樣本 \(x_0\)。

和其他生成家族相比，擴散模型以速度換取穩定性與品質。訓練只是簡單的迴歸問題，避免了對抗式訓練的不穩定，但取樣需要很多次網路評估。近年許多工作都在降低這個成本。

## 核心概念

- **雜訊排程**：每一步加入多少雜訊，常寫作 \(\bar\alpha_t\)。
- **去噪器**：從帶噪輸入與時間步預測雜訊（或乾淨影像、或速度）的網路。
- **骨幹**：去噪器的架構。早期模型使用 U-Net，即帶有跳接的卷積編碼器—解碼器；較新的模型則在潛在影像的圖塊上使用 Transformer。
- **潛在擴散**：在自編碼器壓縮後的潛在空間中進行擴散，而不是直接在像素上進行。
- **條件化**：提供額外輸入，例如文字提示，去噪器通常透過交叉注意力來處理。
- **無分類器引導**：結合條件與無條件預測，以加強條件化效果的方法。
- **取樣器**：把反向步驟轉成快速取樣程序的規則，例如 DDIM。

## 運作方式

最簡單的訓練目標是雜訊預測損失：

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big], \qquad x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon
\]

每個訓練樣本是一個乾淨樣本，加上隨機的時間步與隨機雜訊。網路看到帶噪輸入與時間步，並學習預測雜訊。取樣則是一個迭代更新，每一步去除一部分預測的雜訊。

### 骨幹

- **U-Net**：帶跳接的卷積編碼器—解碼器，在較低解析度處使用注意力。它是像素空間影像模型的預設選擇。
- **Transformer（DiT）**：把潛在影像切成圖塊，每個圖塊成為一個 token，再由 Transformer 處理，並把時間步與條件當作額外輸入。它的品質隨運算量增加而可預測地提升，與語言模型類似。

### 潛在擴散與條件化

潛在擴散先以預先訓練的自編碼器壓縮影像，再於較小的潛在表示上做擴散。這使每一步的成本約降低壓縮倍率。文字條件通常透過去噪器到文字編碼器嵌入的交叉注意力來實現。

### 較快的取樣

單純的取樣器需要和訓練一樣多的步數。兩種想法可以減少步數：DDIM 這類非馬可夫取樣器能以少很多的步數重用同一個訓練好的模型；蒸餾則訓練學生模型，讓它一步就能達到教師模型數步的效果。無分類器引導以多樣性換取提示的忠實度，並在取樣時套用，不需要另外的分類器。

## 關鍵方法

### Denoising Diffusion Probabilistic Models（Ho, Jain & Abbeel，2020）

- **問題：** GAN 能產生清晰影像，但訓練不穩定；當時的概似模型生成的樣本品質較弱。
- **核心想法：** 訓練網路預測在隨機時間步加入的雜訊，並使用加權的變分下界，它會簡化為上述的雜訊預測損失。
- **公式或演算法：** 即上節的損失，搭配固定的線性雜訊排程，以及跨越 \(T\) 步的祖先取樣。
- **結果：** 摘要報告在無條件 CIFAR-10 上 Inception score 為 9.46、FID 為 3.17，並描述當時達到最先進水準。摘要描述 256×256 LSUN 的樣本品質與 ProgressiveGAN 相近，但摘要中沒有數字。
- **限制：** 取樣需要數百次網路評估，生成速度慢。摘要未報告訓練或取樣成本。

### High-Resolution Image Synthesis with Latent Diffusion Models（Rombach 等人，2021/2022）

- **問題：** 像素空間的擴散消耗極大的運算量，作者描述常需要數百個 GPU 日。
- **核心想法：** 在預先訓練的自編碼器潛在空間中訓練擴散模型，並加入交叉注意力層，使模型能以文字、版面或其他輸入進行條件化。
- **公式或演算法：** 把 DDPM 的目標套用在潛在表示 \(z = E(x)\) 上，並在去噪器的中間特徵上做交叉注意力。
- **結果：** 摘要報告在影像資料上達到最先進結果，並在影像補全上創下新的最先進水準；在無條件生成、語意場景合成與超解析度上，以低於像素空間模型的運算量取得有競爭力的結果。摘要未給出基準數字。
- **限制：** 自編碼器限制了可以重建的細節。摘要未量化運算量的節省，主文才有。

### Scalable Diffusion Models with Transformers（Peebles & Xie，2022/2023）

- **問題：** U-Net 骨幹是人工設計的，而且不清楚擴散模型的品質是否像 Transformer 語言模型一樣隨運算量擴展。
- **核心想法：** 在潛在擴散中以 Transformer 取代 U-Net，作用於潛在圖塊上，並以前向傳播的 Gflops 衡量品質。
- **公式或演算法：** 潛在表示被切成大小為 \(p\) 的圖塊、嵌入為 token，並以自適應層正規化處理，時間步與類別標籤作為條件。
- **結果：** 摘要指出，來自深度、寬度或更多 token 的 Gflops 越高，模型的 FID 就持續越低。最大的模型 DiT-XL/2 在類別條件的 ImageNet 256×256 上達到 FID 2.27，超越先前的擴散模型。摘要未給出 512×512 的 FID。
- **限制：** 結果基於類別條件的 ImageNet，比文字生成影像的基準範圍窄。摘要未提供訓練運算量數字。

## 關聯

- **生成模型：** 擴散是數種生成演算法之一，與自回歸模型、VAE、GAN 並列，見[生成模型](../index.md)。
- **Transformer：** DiT 骨幹重用了[Transformer 與注意力](../../models/transformer/index.md)中的注意力機制。
- **卷積網路：** U-Net 骨幹由[卷積網路](../../models/cnn/index.md)中的層所構成。
- **大腦與心智：** 擴散模型已被用於從腦部活動解碼影像，見[腦機介面](../../../brain-mind/bci/index.md)。至於大腦自身的學習如何與這些訓練目標比較，見 [NeuroAI](../../../brain-mind/neuroai/index.md)。

## 應用

- 文字生成影像，以及修補、超解析度等影像編輯。
- 以擴散 Transformer 生成影片。
- 音訊與語音合成。
- 以去噪過程對動作序列建模的機器人控制策略。

## 開放問題

- 取樣步數能減少到一步，同時不損失品質或多樣性到什麼程度？
- 在影片上，Transformer 骨幹是否比 U-Net 擴展得更好，代價又是多少？
- 引導的好處有多少是模型真正的改進，又有多少只是犧牲多樣性換來的權衡？

## 參考文獻

### 開創性論文

- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — 第一個以擴散為基礎的生成模型，學習逆轉逐步加噪的過程。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 將訓練簡化為雜訊預測，並展示高品質的影像生成。
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — 非馬可夫取樣器，取樣速度比 DDPM 快 10 到 50 倍。
- Rombach, R. 等人 (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — 在自編碼器潛在空間中進行擴散，並以交叉注意力進行條件化。
- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV. https://arxiv.org/abs/2212.09748 — 以 Transformer 取代 U-Net，並顯示 FID 隨運算量改善。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 將擴散模型的設計選擇分開，使每一項都能獨立調整。
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — 結合條件與無條件預測的引導方法，不需要外部分類器。

### 綜述與教科書

- Song, Y. 等人 (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 將擴散模型與分數模型統一為隨機微分方程。

### 文章與文件

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*。Hugging Face 部落格。https://huggingface.co/blog/annotated-diffusion — DDPM 的逐步程式碼導讀，適合對照本頁的公式。
