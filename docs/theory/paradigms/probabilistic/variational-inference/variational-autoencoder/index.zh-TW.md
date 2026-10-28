---
translation_reviewed: 2026-10-28
---

# 變分自編碼器

變分自編碼器（variational autoencoder, VAE）由 Kingma 與 Welling（2013）提出，它透過最大化一個變分界，同時訓練潛變數生成模型與編碼器網路。它是攤銷變分推論最有名的例子，也是[變分推論](../index.md)概述中介紹的方法之一。

## 概述

VAE 把自編碼器的編碼視為一個潛變數 \(z\)，其先驗為 \(p(z)\)，並假設資料 \(x\) 由解碼器 \(p_\theta(x\mid z)\) 產生。後驗 \(p_\theta(z\mid x)\) 無法解析求得，因此 VAE 學習一個編碼器 \(q_\phi(z\mid x)\) 來近似它，兩個網路用同一個目標一起訓練。

過去的變分方法會為每個資料點各自擬合一組近似。VAE 則讓所有資料點共用同一個編碼器，因此對新資料點做推論只需一次前向計算。Kingma 與 Welling 再搭配一種會穿過抽樣步驟的梯度估計器，使深度模型能以一般的隨機梯度方法訓練。

## 核心概念

- **編碼器（辨識模型）** \(q_\phi(z\mid x)\)：輸出 \(z\) 分布參數的網路，通常是高斯分布。
- **解碼器** \(p_\theta(x\mid z)\)：給定編碼後，輸出資料分布的網路。
- **先驗** \(p(z)\)：通常是標準高斯分布，編碼器會被拉向它。
- **重參數化技巧**：把樣本寫成參數與不依賴參數之雜訊的可微函數。對高斯分布而言，\(z = \mu_\phi(x) + \sigma_\phi(x)\odot\varepsilon\)，其中 \(\varepsilon\sim\mathcal N(0, I)\)。
- **攤銷推論**：一個推論網路服務所有資料點，因此推論的成本在訓練時就已付出。

## 運作方式

單一資料點的對數似然之界為

\[
\mathcal{L}(\theta,\phi;x) = \mathbb{E}_{q_\phi(z\mid x)}\big[\log p_\theta(x\mid z)\big] - \mathrm{KL}\big(q_\phi(z\mid x)\,\|\,p(z)\big)
\]

第一項獎勵良好的重建；第二項懲罰偏離先驗的編碼。若編碼器與先驗都是高斯分布，KL 項有閉式解，因此只有重建項需要用抽樣估計（Kingma & Welling，2013，附錄 B）。令 \(z^{(l)} = g_\phi(\varepsilon^{(l)}, x)\)，其中 \(\varepsilon^{(l)}\sim p(\varepsilon)\)，重建項變為

\[
\mathbb{E}_{q_\phi}\big[\log p_\theta(x\mid z)\big] \approx \frac{1}{L}\sum_{l=1}^{L}\log p_\theta\big(x\mid z^{(l)}\big),
\]

此式對 \(\theta\) 與 \(\phi\) 都可微。論文中的小批次流程如下：

1. 從資料集中抽出一個包含 \(M\) 個資料點的小批次。
2. 對每個資料點抽出 \(L\) 個雜訊樣本，並形成編碼 \(z^{(l)} = g_\phi(\varepsilon^{(l)}, x)\)。
3. 計算小批次上的界估計值，及其對 \(\theta\) 與 \(\phi\) 的梯度。
4. 對兩組參數同時做一步隨機梯度上升，然後重複。

## 實驗結果

論文在 MNIST 與 Frey Face 資料集上訓練生成模型。其主要比較，是在相同的編碼器與解碼器下，比較所提出的估計器與 Hinton 等人（1995）的清醒－睡眠演算法。

- **訓練時的界。** 在兩個資料集上，對每個測試的潛變數維度，VAE 都明顯比清醒－睡眠演算法收斂得快，且達到較高的界值。增加潛在單元並未造成過擬合（論文圖 2）。
- **邊際似然。** 在 MNIST 的三維潛在空間中，VAE 與清醒－睡眠演算法收斂得比以 Hybrid Monte Carlo 實作的 Monte Carlo EM 基準更快，而後者無法用於完整資料集（論文圖 3）。

這些結果以曲線呈現，衡量的是界與似然被最佳化的程度，對樣本品質的說明有限。

## 限制

- **受限的後驗。** VAE 通常假設近似上近乎因子化的後驗，其參數來自回歸網路。Burda 等人（2015）認為，這可能導致過度簡化的表徵，無法發揮模型的完整容量。
- **攤銷差距。** 單一編碼器無法為每個點找到最佳的局部後驗。Cremer 等人（2018）發現，訓練後 VAE 的誤差很大一部分來自不夠好的編碼器。
- **界，而非似然。** ELBO 是下界，因此它不能給出模型對資料的精確擬合程度。

## 開放問題

- 能否在不犧牲攤銷推論速度的前提下收緊界？更緊的界是否會帶來更好的表徵？Burda 等人（2015）報告了更豐富的潛在空間，但界與表徵有用性之間的關係尚無定論。
- 攤銷差距中，有多少需要更豐富的分布族，而不是更好的編碼器？[正規化流後驗](../normalising-flow-posteriors/index.md)處理的是後者。

## 參考文獻

### 開創性論文

- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 提出 VAE、變分界的重參數化估計器，以及共享的辨識模型。
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. arXiv. https://arxiv.org/abs/1401.4082 — 為深度潛變數模型推導出相同的重參數化梯度。
- Hinton, G. E., Dayan, P., Frey, B. J. & Neal, R. M. (1995). The "Wake-Sleep" Algorithm for Unsupervised Neural Networks. *Science*. https://doi.org/10.1126/science.7761831 — 訓練含有獨立辨識網路的多層生成網路，是 VAE 所比較的基準。

### 綜述與教科書

- Kingma, D. P. & Welling, M. (2019). *An Introduction to Variational Autoencoders*. arXiv. https://arxiv.org/abs/1906.02691 — 作者撰寫的 VAE 入門教材，涵蓋其延伸方法。
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — 將 VAE 的目標放入一般變分推論的理論中。

### 文章與文件

- Burda, Y., Grosse, R. & Salakhutdinov, R. (2015). *Importance Weighted Autoencoders*. arXiv. https://arxiv.org/abs/1509.00519 — 以多個重要性加權樣本建立更緊的界，並報告比 VAE 更豐富的潛在表徵。
- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. arXiv. https://arxiv.org/abs/1801.03558 — 顯示訓練後 VAE 的近似誤差，很大一部分來自不夠好的辨識網路。
