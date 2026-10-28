---
translation_reviewed: 2026-10-28
---

# 潛在擴散模型

潛在擴散在預先訓練的自編碼器所壓縮的潛在空間中進行擴散，而不是直接作用在原始像素上。Rombach 等人（2022）另外加入交叉注意力層，使同一個模型能以文字、版面與其他輸入為條件。家族層級的概觀請見[擴散模型](index.md)頁面。

## 概述

像素空間的擴散把大部分計算花在細節上，而自編碼器可以用很緊湊的方式表示這些細節。Rombach 等人把兩個工作分開：自編碼器負責感知壓縮，擴散模型則在小得多的潛在空間中負責生成建模。這使訓練與取樣都更便宜，論文的實驗也顯示，潛在模型在多項任務上達到更好的樣本品質。

## 問題

像素空間的擴散模型在影像合成上已是最先進的方法，但它們的訓練與取樣成本很高，因為每一個去噪步驟都要處理全解析度的影像。此外，加入文字、版面等一般性的條件輸入，也不是這種方法內建的功能。Rombach 等人要解決的問題是：如何保留像素空間擴散的品質，同時降低成本並讓條件輸入更有彈性。

## 核心想法

先訓練一次感知自編碼器，把影像壓縮為潛在表徵 \(z = E(x)\)，然後在潛在表徵上訓練擴散模型。去噪器包含交叉注意力層，使影像特徵能夠關注任何條件的編碼。論文研究了多種下採樣因子 \(f\)，發現適度的壓縮能在效率與品質之間取得最好的平衡。

## 演算法

訓練分兩個階段。首先訓練或重用自編碼器 \(E, D\) 來壓縮影像。接著在潛在表徵上以雜訊預測損失訓練擴散模型：

\[
L_{\text{LDM}} = \mathbb{E}_{E(x),\epsilon,t,c}\big[\|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|^2\big]
\]

其中 \(\tau_\theta(c)\) 是條件 \(c\) 的編碼。在每個交叉注意力層中，去噪器的中間特徵提供查詢 \(Q\)，編碼後的條件提供鍵 \(K\) 與值 \(V\)，因此注意力為 \(\mathrm{softmax}(QK^\top/\sqrt d)\,V\)。編碼器 \(\tau_\theta\) 與去噪器一起訓練。取樣時在潛在空間中執行反向過程，最後由解碼器 \(D\) 把潛在表徵映回影像。

自編碼器可以用 KL 懲罰或向量量化做正則化。論文的表 8 顯示，經正則化的第一階段（KL 與 VQ）所得結果，會比連續版本稍差，因此正則化的選擇同時影響樣本品質與重建品質。

## 結果

- **壓縮因子。**論文訓練了 \(f \in \{1, 2, 4, 8, 16, 32\}\) 的模型，其中 \(f = 1\) 是像素空間的基線。論文的結論是，LDM-4 與 LDM-8 提供高品質合成的最佳條件。小的因子訓練慢，大的因子則限制了保真度。
- **CelebA-HQ 256×256。**LDM-4 以 500 步 DDIM 取樣，達到 FID 5.11，論文稱之為新的最先進結果，超越先前的似然模型與 GAN。
- **圖像修補。**與像素空間擴散相比，潛在模型在訓練與取樣的吞吐量上至少快 2.7 倍，並使 FID 至少改善 1.6 倍。

## 限制

- **自編碼器的限制。**自編碼器的重建誤差限制了擴散模型能產生的細節。論文也指出，ImageNet 等複雜資料集需要較小的壓縮率，才不會降低品質。
- **因子的選擇。**最佳的 \(f\) 取決於資料集，因此每個任務都需要調校。
- **比較的範圍。**計算與吞吐量的數字來自論文自己在單張 NVIDIA A100 上、預算相同的實驗，並非所有任務的通用基準。

## 關聯

- 潛在目標就是把 [DDPM](ddpm.md) 的目標套用在潛在表徵上。
- 論文中的潛在取樣使用 [DDIM](ddim.md) 這類較快的取樣器。
- 後來的 Transformer 去噪器是 [DiT](../../../../models/transformer/dit/index.md)。
- 文字條件化依賴[無分類器引導](classifier-free-guidance.md)這個引導方法。
- 去噪器中的卷積與注意力層，見[卷積網路](../../../../models/cnn/index.md)與[Transformer 與注意力](../../../../models/transformer/index.md)。

## 未解問題

- 自編碼器會損失多少重建品質？這是否會限制文字渲染或人臉的細緻程度？
- 對於影片這類需要時間一致性的任務，應如何設計潛在空間？

## 參考文獻

### 開創性論文

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — 提出在自編碼器潛在空間中進行擴散，並以交叉注意力做條件化，報告 CelebA-HQ 與圖像修補的結果。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 潛在擴散所套用到潛在表徵上的像素空間目標。
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — 潛在擴散文字生成模型所使用的引導方法。

### 綜述與教科書

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 擴散模型的連續時間觀點；潛在模型使用的是離散的雜訊預測形式。
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — 把擴散模型的設計選擇分開討論，這些選擇同樣適用於潛在模型。

### 文章與文件

- Rombach, R. 等人。*latent-diffusion*，官方程式碼儲存庫。https://github.com/CompVis/latent-diffusion — 作者實作潛在擴散模型及其實驗的程式碼。
