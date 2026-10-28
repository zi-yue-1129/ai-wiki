---
translation_reviewed: 2026-10-28
---

# VQ-VAE

向量量化變分自編碼器（vector-quantised variational autoencoder, VQ-VAE）是一種潛在編碼為離散值的 VAE。編碼器的輸出會被替換為學習得到的碼本中最近的條目，再由一個獨立的自回歸先驗對這些編碼建模，因此可以透過取樣編碼並解碼來生成新的影像或音訊。它是[變分自編碼器](../index.md)中介紹的代表性變體之一。

## 概述

標準 VAE 使用具高斯後驗的連續潛變數。Oord、Vinyals 與 Kavukcuoglu（2017）則改為學習離散編碼，這些編碼保留了高階內容、捨去了低階細節。接著，就可以在這些編碼上擬合一個強大的自回歸模型，這比逐像素建模來得省力。作者還主張，離散化有助於避免後驗塌陷。

後驗是確定性的：每個編碼器輸出對應到一個編碼。編碼上的先驗是在自編碼器訓練完成後才學得的，而不是事先固定。

## 核心概念

- **碼本**：\(K\) 個學習得到的向量 \(e_1,\dots,e_K\)，屬於 \(\mathbb{R}^D\)，也稱為嵌入表。離散潛變數就是碼本的索引。
- **最近鄰量化**：編碼器輸出被替換為最接近的碼本向量，使後驗成為 one-hot。
- **直通估計器**：查找步驟沒有有用的梯度，因此把解碼器輸入處的梯度直接複製給編碼器輸出。
- **承諾項**：一種懲罰，使編碼器輸出靠近它所選取的碼本向量，避免編碼器偏離碼本。
- **自回歸先驗**：影像編碼使用 PixelCNN，音訊編碼使用 WaveNet，在訓練後對編碼擬合。

## 運作方式

量化會選出最接近編碼器輸出的碼本向量：

\[
k = \arg\min_j \lVert z_e(x) - e_j \rVert_2^2, \qquad z_q(x) = e_k
\]

後驗是確定性的，且訓練時先驗是均勻的，因此 KL 項是常數 \(\log K\)，會從目標函數中消去。訓練損失為

\[
L = -\log p\big(x \mid z_q(x)\big) + \lVert \mathrm{sg}[z_e(x)] - e_k \rVert_2^2 + \beta\,\lVert z_e(x) - \mathrm{sg}[e_k] \rVert_2^2
\]

第一項是重建損失，第二項把被選中的碼本向量拉向編碼器輸出，第三項是承諾項。其中 \(\mathrm{sg}\) 是停止梯度運算子，在前向傳播中是恆等映射，在反向傳播中導數為零。作者採用 \(\beta = 0.25\)，並報告在 0.1 到 2.0 之間取值時結果沒有明顯差異。訓練步驟如下：

1. 把輸入編碼為一格向量 \(z_e(x)\)。
2. 把每個向量替換為最近的碼本條目，形成 \(z_q(x)\)。
3. 解碼 \(z_q(x)\) 並計算重建損失；其梯度以直通估計器傳給編碼器。
4. 以第二項更新碼本，以第三項更新編碼器。
5. 凍結自編碼器，把資料編碼為編碼格，並在這些編碼上擬合自回歸先驗。生成時，從先驗取樣一個編碼格再解碼。

## 結果

- **CIFAR-10 上的似然。** 在相同架構下，連續 VAE、VQ-VAE 與 VIMCO 分別得到 4.51、4.67 與 5.14 位元每維度。這些數值皆為下界。作者稱 VQ-VAE 是第一個在此比較中挑戰連續 VAE 的離散潛變數模型。
- **影像。** ImageNet 的 128 × 128 × 3 影像被壓縮為 32 × 32 × 1 的編碼格，\(K = 512\)。重建只比原圖稍微模糊。以 PixelCNN 為先驗所產生的樣本為 128 × 128。
- **語音。** 把每個編碼映射到其最可能的音素，在 41 類上達到 49.3% 的準確率；一個基準方法則為 7.2%。

論文報告了似然與樣本，但未報告 FID 等樣本品質指標。

## 限制

- **兩階段訓練。** 先驗是在自編碼器之後擬合的。作者指出聯合訓練可能會加強結果，但將其留待未來工作。
- **沒有真正的梯度。** 論文指出，查找步驟並未定義真正的梯度，因此直通估計器只是近似。
- **模糊的重建。** 逐像素的損失使重建略為模糊。作者建議以感知或對抗損失作為未來工作。

## 未解問題

- 整個流程中，哪一部分決定樣本品質：離散瓶頸、先驗，還是解碼器？VQ-VAE-2（Razavi 等人，2019）特別強調先驗的作用。

## 與其他主題的連結

- **影像分詞器。** VQGAN（Esser 等人，2021）為卷積式 VQ 自編碼器加入以圖塊為單位的判別器與感知損失，並以 Transformer 對其編碼建模。
- **潛在擴散。** [潛在擴散](../../diffusion/latent-diffusion.md)中的自編碼器可以用 KL 懲罰或向量量化來正則化（Rombach 等人，2022）。
- **語言分詞。** VQ 編碼的角色接近子詞詞元，但它是從像素或音訊學得的；可比較[分詞（Tokenisation）](../../../../../models/llm/tokenisation/index.md)。

## 應用

- **大規模影像生成。** VQ-VAE-2（Razavi 等人，2019）建構了離散編碼的階層。作者報告其樣本在多個資料集上可與 GAN 媲美。
- **語音。** 以 WaveNet 為先驗的編碼模型，能產生可辨認出字詞與片語的樣本。

## 參考文獻

### 開創性論文

- Oord, A. van den, Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — 論文本身：VQ-VAE、其訓練損失與編碼上的自回歸先驗。
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 以連續潛變數的 VAE，VQ-VAE 以離散編碼取代它，並作為其比較基準。
- Razavi, A., van den Oord, A. & Vinyals, O. (2019). *Generating Diverse High-Fidelity Images with VQ-VAE-2*. arXiv. https://arxiv.org/abs/1906.00446 — 以離散編碼的階層擴展 VQ-VAE。
- Esser, P., Rombach, R. & Ommer, B. (2021). *Taming Transformers for High-Resolution Image Synthesis*. CVPR. https://arxiv.org/abs/2012.09841 — 學習卷積式 VQ 碼本，並以 Transformer 對其編碼建模。
- Rombach, R. et al. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. CVPR. https://arxiv.org/abs/2112.10752 — 比較 KL 正則化與向量量化的潛在空間，用於擴散。
