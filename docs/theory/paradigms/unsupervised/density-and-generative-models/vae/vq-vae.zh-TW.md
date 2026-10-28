---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/autoencoders-and-representations
tags:
  - 生成模型
  - 離散潛在變數
  - 表徵學習
aliases:
  - VQ-VAE
  - 向量量化 VAE
  - Vector-quantised VAE
---

# 向量量化 VAE（VQ-VAE）

VQ-VAE 以從學到的碼本中選出的離散編碼，取代[變分自編碼器](index.md)的連續潛在變數，再對這些編碼訓練一個獨立的自迴歸先驗。離散編碼讓潛在空間更容易以強大的先驗建模。此方法屬於 [VAE](index.md) 家族。

## 概覽

van den Oord、Vinyals 與 Kavukcuoglu（2017）指出，潛在變數為一組離散編碼的 VAE 可以端到端訓練，碼本與編碼器、解碼器一起學習。訓練完成後，在影像上對離散潛在變數擬合一個 PixelCNN 先驗，原始音訊則使用 WaveNet。生成時，從先驗抽取編碼，再解碼為影像。

## 關鍵概念

- **碼本**：一組嵌入向量 \(e_1, \dots, e_K\)。每個編碼器輸出會對映到最近的那一個。
- **最近鄰量化**：編碼索引為 \(k = \arg\min_j \lVert z_e(x) - e_j \rVert_2\)，解碼器接收 \(e_k\)。
- **直通梯度（straight-through）**：量化步驟沒有梯度，因此把解碼器輸入的梯度原樣複製到編碼器輸出。
- **承諾損失（commitment loss）**：讓編碼器輸出貼近其所選的編碼，以 \(\beta\) 加權。
- **兩階段訓練**：先訓練自編碼器，之後才在離散編碼上擬合先驗。

## 運作方式

編碼器產生 \(z_e(x)\)，量化為最近的碼本向量 \(e_k\)，解碼器再由 \(e_k\) 重建 \(x\)。損失為

\[
L = \log p(x \mid z_q(x)) + \lVert \operatorname{sg}[z_e(x)] - e \rVert_2^2 + \beta\,\lVert z_e(x) - \operatorname{sg}[e] \rVert_2^2
\]

其中 \(\operatorname{sg}\) 為停止梯度運算子。第一項為重建，第二項把碼本向量拉向編碼器輸出，第三項防止編碼器輸出漂移。論文在所有實驗中使用 \(\beta = 0.25\)。

對於 128 乘 128 乘 3 的 ImageNet 影像，論文以 \(K = 512\) 個編碼，把每張影像壓縮為 32 乘 32 乘 1 的離散潛在變數。接著 PixelCNN 以自迴歸方式對此潛在網格建模，因此取樣得到的潛在變數可以解碼為影像。

## 關鍵方法

### Neural Discrete Representation Learning（van den Oord 等人，2017）

- **問題：** 具連續潛在變數與強大解碼器的 VAE，往往忽略部分潛在編碼，或產生模糊的樣本。離散潛在變數較容易以自迴歸先驗建模，但標準訓練無法穿過離散選擇反向傳播。
- **核心想法：** 以學到的碼本做最近鄰查找，形成離散的瓶頸，並以直通估計量與上述碼本與承諾損失訓練；之後再在編碼上擬合自迴歸先驗。
- **公式或演算法：** 上述損失與最近鄰規則。訓練同時更新編碼器、解碼器與碼本。訓練後，在編碼網格上擬合先驗。
- **結果：** 論文的 CIFAR-10 比較中，VQ-VAE 為 4.67 每維位元，連續 VAE 為 4.51，VIMCO 為 5.14。三者皆為似然的下界。論文也報告以 PixelCNN 與 WaveNet 先驗從離散潛在變數生成的影像與音訊。
- **限制：** 先驗是在自編碼器之後擬合，而非與之聯合訓練，論文將此列為未來工作。在 CIFAR-10 比較中，VQ-VAE 的下界略弱於連續 VAE。離散瓶頸也限制了單一編碼能承載的細節。

## 關聯

- VQ-VAE 所修改的連續 VAE 定義於 [VAE 總覽](index.md)，其 ELBO 與先前相同。
- VQ-VAE 的離散編碼在後續的階層式模型中作為影像符號，例如 Razavi 等人（2019）的 [VQ-VAE-2](https://arxiv.org/abs/1906.00446)。
- 學習資料的緊湊表徵，這個想法屬於[自編碼器與表徵](../../autoencoders-and-representations/index.md)的範疇。

## 應用

把影像與音訊壓縮為離散編碼，以及以符號為基礎的影像生成：學到的碼本把影像轉為自迴歸模型可以預測的序列。

## 開放問題

- 讓每個碼本向量都被使用，避免離散瓶頸塌縮到少數幾個編碼上。
- 聯合訓練先驗與自編碼器，論文將此列為未來工作。
- 離散編碼要多大，才能與連續潛在變數的細節相當。

## 參考文獻

### 開創性論文

- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. NeurIPS（arXiv）. https://arxiv.org/abs/1711.00937 — 提出 VQ-VAE，以直通估計量與離散碼本作為瓶頸，即本頁的方法。
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 提出 VAE 與 VQ-VAE 所修改的重參數化估計量。
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. ICML. https://arxiv.org/abs/1401.4082 — 以隨機反向傳播與識別模型發展同一類模型。
- Burda, Y., Grosse, R. & Salakhutdinov, R. (2016). *Importance Weighted Autoencoders*. ICLR. https://arxiv.org/abs/1509.00519 — 以重要性加權樣本收緊同一模型類別的 ELBO。
- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. arXiv. https://arxiv.org/abs/1601.06759 — 提出自迴歸的像素模型，其 PixelCNN 形式被用作 VQ-VAE 影像的先驗。
- Razavi, A., van den Oord, A. & Vinyals, O. (2019). *Generating Diverse High-Fidelity Images with VQ-VAE-2*. arXiv. https://arxiv.org/abs/1906.00446 — 把 VQ-VAE 擴展為離散編碼的階層，用於高保真影像生成。

## 延伸學習

- Lilian Weng, *From Autoencoder to Beta-VAE*。連結：https://lilianweng.github.io/posts/2018-08-12-vae/ — 以圖示逐步介紹自編碼器、VAE 與其變體，包括離散潛在變數。
