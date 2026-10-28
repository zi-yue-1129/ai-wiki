---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/cnn
tags:
  - 生成模型
  - 變分推論
  - 非監督式學習
aliases:
  - 變分自編碼器
  - VAE
  - Variational autoencoder
---

# 變分自編碼器（VAE）

變分自編碼器是一種潛在變數生成模型，透過最大化資料似然的下界來訓練。編碼器把每個輸入映射為潛在編碼上的分布，解碼器則把編碼映射回資料。由於潛在空間連續且先驗簡單，模型可以從先驗抽樣編碼、再解碼產生新樣本。它是三大經典生成演算法之一，另外兩個是 [GAN](../gan/index.md) 與[流模型](../flow/index.md)。家族層級的比較見[生成模型](../generative-models/index.md)頁。

## 概覽

Kingma 與 Welling（2013）以及 Rezende、Mohamed 與 Wierstra（2014）幾乎同時提出同一個模型。兩者都結合了一個估計後驗的神經網路（識別模型），以及透過重參數化下界訓練的生成模型。結果是一個可以用隨機梯度下降在大型資料集上最佳化的單一目標函數。

## 關鍵概念

- **潛在變數** \(z\)：未被觀察到的編碼，先驗為 \(p(z) = \mathcal N(0, I)\)。
- **編碼器（識別模型）** \(q_\phi(z\mid x)\)：對每個輸入輸出 \(z\) 上高斯分布之平均與變異數的網路。
- **解碼器** \(p_\theta(x\mid z)\)：在給定編碼下定義資料似然的網路。
- **證據下界（ELBO）**：訓練目標，為 \(\log p_\theta(x)\) 的下界。
- **重參數化技巧**：寫成 \(z = \mu + \sigma \odot \epsilon\)，其中 \(\epsilon \sim \mathcal N(0, I)\)，使梯度能穿過抽樣步驟。

## 運作方式

單一資料點的 ELBO 為

\[
\mathcal L(\theta,\phi; x) = \mathbb E_{q_\phi(z\mid x)}\big[\log p_\theta(x\mid z)\big] - D_{\mathrm{KL}}\big(q_\phi(z\mid x)\,\|\,p(z)\big) \le \log p_\theta(x)
\]

第一項鼓勵重建結果；第二項使近似後驗接近先驗，讓潛在空間夠平滑，可以抽樣。下界與 \(\log p_\theta(x)\) 之間的差距，正好是近似後驗與真實後驗之間的 KL 散度，因此較好的編碼器會讓下界更緊。

訓練時，對每個資料點抽取 \(\epsilon\)，計算 \(z = \mu_\phi(x) + \sigma_\phi(x)\odot\epsilon\)，經過解碼器後對 \(-\mathcal L\) 做一步梯度更新。當先驗與後驗都是高斯時，KL 項有封閉解。生成時，從 \(z\sim\mathcal N(0,I)\) 抽樣，並取解碼器的平均或樣本。

## 關鍵方法

多個變體會改變潛在先驗、解碼器或下界本身。每個變體日後都應有自己的頁面；此處的簡短比較足以概述家族。

- **隨機反向傳播與近似推論（Rezende 等人，2014）**：相同的模型與重參數化估計量，從深層潛在高斯模型的角度發展。
- **向量量化 VAE（VQ-VAE）**：以碼本學習的離散潛在編碼，常用於影像與音訊的符號化。方法頁待撰寫。
- **條件式 VAE（CVAE）**：讓編碼器與解碼器都以標籤或其他輸入為條件。方法頁待撰寫。

### Auto-Encoding Variational Bayes（Kingma 與 Welling，2013）

- **問題：** 具連續潛在變數的有向模型中，精確的後驗推論難以計算；平均場或基於抽樣的方法難以擴展到大型資料集。
- **核心想法：** 以重參數化的蒙地卡羅估計量最佳化 ELBO，並以一個跨所有資料點共用的編碼器攤銷推論成本。
- **公式或演算法：** 上述 ELBO 與高斯重參數化 \(z = \mu_\phi(x) + \sigma_\phi(x)\odot\epsilon\)。每一步使用一個小批次、每個點抽取一次 \(\epsilon\)，並同時更新 \(\theta\) 與 \(\phi\)。
- **結果：** 論文報告在 MNIST 與 Frey Face 資料集上的實驗，包括生成樣本與邊際似然估計。摘要描述此方法在大型資料集上很有效率，並在實驗中反映其理論優勢，但未引用具體數字。
- **限制：** 高斯後驗與解碼器可能產生模糊的樣本，因為似然項會平均所有合理的輸出。編碼器較弱時，下界也會較鬆。後續研究處理了後驗族、先驗與下界本身。

### 隨機反向傳播與近似推論（Rezende 等人，2014）

- **問題：** 與上述相同，針對具連續潛在變數的深層有向生成模型。
- **核心想法：** 識別模型扮演隨機編碼器，並以重參數化穿過抽樣步驟傳遞梯度。
- **公式或演算法：** 變分下界的重參數化估計量，同時最佳化生成模型與識別模型。
- **結果：** 摘要指出，在數個真實資料集上，模型能生成逼真樣本、準確填補缺失資料，並有助於高維資料視覺化。摘要未給出具體數字。
- **限制：** 同上。論文著重於估計量與模型類別，而非單一基準測試。

## 關聯

- 重參數化技巧與[強化學習](../../../reinforcement-learning/policy-gradient-and-actor-critic/index.md)中蒙地卡羅梯度估計使用的技巧相同。
- 擴散模型可視為具固定編碼器的階層式 VAE，見 [DDPM](../diffusion/ddpm.md)。
- 影像 VAE 的編碼器是卷積式的，見[卷積網路](../../../../models/cnn/index.md)；擴散潛在空間中常用的解碼器是 [U-Net](../../../../models/cnn/unet/index.md)。
- ELBO 是變分推論的一個例子，連結到[機率方法](../../../probabilistic/index.md)。
- 關於腦啟發的生成模型如何與這些目標函數相關，見 [NeuroAI](../../../../../brain-mind/neuroai/index.md)。

## 應用

影像、音訊與分子的表徵學習；以重建誤差偵測異常；半監督分類；以及為大型生成模型把影像符號化。

## 開放問題

- 模糊樣本：更豐富的後驗或離散潛在變數能否縮小與 GAN、擴散模型之間的樣本品質差距。
- 後驗塌陷：過於強大的解碼器可能忽略潛在編碼。
- ELBO 與對數似然之間的差距，以及它如何限制模型比較。

## 參考文獻

### 開創性論文

- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 提出 VAE、ELBO 與用於攤銷推論的重參數化估計量。
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. ICML. https://arxiv.org/abs/1401.4082 — 以隨機反向傳播與識別模型發展同一類模型。

### 綜述與教科書

- Kingma, D. P. & Welling, M. (2019). *An Introduction to Variational Autoencoders*. arXiv. https://arxiv.org/abs/1906.02691 — VAE 框架及其延伸的教程式綜述。

### 文章與文件

- Doersch, C. (2016). *Tutorial on Variational Autoencoders*. arXiv. https://arxiv.org/abs/1606.05908 — 逐步推導 VAE 目標函數與其訓練方式。

## 延伸學習

- Lilian Weng, *From Autoencoder to Beta-VAE*。連結：https://lilianweng.github.io/posts/2018-08-12-vae/ — 以圖示逐步介紹自編碼器、VAE 與其變體。
