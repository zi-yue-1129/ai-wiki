---
translation_reviewed: 2026-10-28
---

# 原始 GAN：生成對抗網路

原始 GAN 由 Goodfellow 等人（2014）提出，它把生成器與判別器訓練成極小極大博弈的兩個參與者。它是[生成對抗網路](../index.md)主題的核心方法，也是之後所有變體的參照點。

## 概述

Goodfellow 等人提出一種透過對抗程序估計生成模型的新方法。兩個模型同時訓練：一個是捕捉資料分布的生成模型 \(G\)，另一個是判斷樣本來自訓練資料或來自 \(G\) 的判別模型 \(D\)。論文的主要設定是兩個網路都使用多層感知器（MLP）。這樣的系統可以用反向傳播與 dropout 訓練，取樣則只需一次前向傳播，不需要馬可夫鏈或近似推論。

作者的動機是深度生成模型的最大概似訓練很困難，而這個框架繞過了這個困難。

## 核心概念

- **雜訊先驗與生成器**：生成器 \(G(z; \theta_g)\) 是雜訊 \(z\) 的可微分函數，\(z\) 從先驗 \(p_z\) 抽出。它在資料空間上定義分布 \(p_g\)，但沒有顯式的密度。
- **判別器**：\(D(x; \theta_d)\) 回傳單一純量，即 \(x\) 來自資料而非來自 \(p_g\) 的機率。
- **價值函數**：博弈由 \(V(D, G)\) 定義，判別器使它最大化，生成器使它最小化。
- **最佳判別器**：固定 \(G\) 時，最佳的 \(D\) 為 \(D^*_G(x) = p_{\text{data}}(x) / (p_{\text{data}}(x) + p_g(x))\)。
- **非飽和目標**：一種變體，讓生成器最大化 \(\log D(G(z))\)，而不是最小化 \(\log(1 - D(G(z)))\)。

## 運作方式

兩個參與者求解

\[
\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}\big[\log D(x)\big] + \mathbb{E}_{z \sim p_z}\big[\log\big(1 - D(G(z))\big)\big]
\]

在論文的分析中，固定生成器時的準則變為 \(C(G) = -\log 4 + 2\,\text{JSD}(p_{\text{data}} \,\|\, p_g)\)，其中 JSD 是 Jensen–Shannon 散度。它的最小值 \(-\log 4\) 只有在 \(p_g = p_{\text{data}}\) 時才會達到。證明假設的是非參數設定，即兩個網路的容量都不受限制。

實務上，論文使用小批次隨機梯度（演算法 1）：

1. 進行 \(k\) 步：取 \(m\) 個雜訊向量與 \(m\) 個真實樣本，然後沿著 \(\frac{1}{m}\sum_i [\log D(x^{(i)}) + \log(1 - D(G(z^{(i)})))]\) 對判別器參數的梯度上升。
2. 取 \(m\) 個新的雜訊向量，沿著 \(\frac{1}{m}\sum_i \log(1 - D(G(z^{(i)})))\) 對生成器參數的梯度下降。
3. 重複。實驗使用 \(k = 1\)。

論文指出，它的收斂結果無法直接套用到 MLP，因為 MLP 的參數空間有許多臨界點。

## 結果

論文在 MNIST、Toronto Face Database（TFD）與 CIFAR-10 上訓練。由於生成器沒有概似函數，評估方式是對生成樣本擬合高斯 Parzen 窗，並回報保留測試資料的對數概似。[^1] 在 MNIST 上，對抗網路得分為 225 ± 2，是論文表格中的最高值，領先深度 GSN 的 214 ± 1.1。在 TFD 上，它得分為 2057 ± 26，低於堆疊式收縮自編碼器的 2110 ± 50。作者指出，這個估計量的變異很大，在高維度中表現不佳。作者也未聲稱其樣本優於既有模型，只認為它們至少具有競爭力。

## 限制

- **評估**：Parzen 估計很粗略，論文呼籲為不具概似的取樣器尋找更好的評估方式。
- **飽和**：原始生成器損失在訓練初期幾乎沒有梯度，此時判別器會高度自信地拒絕劣質樣本。
- **理論缺口**：最適性證明是非參數的，對 MLP 或其他實用網路並不保證收斂。
- **穩定性**：後續研究顯示，未經正則化的訓練可能不收斂，且此目標可能導致梯度消失或模式崩潰（Arjovsky 等人，2017；Mescheder 等人，2018）。

## 開放問題

- 哪些實用的訓練程序能夠收斂，需要什麼樣的正則化？Mescheder 等人（2018）為未經正則化的訓練給出反例。
- 沒有概似函數時，應如何為樣本評分？Fréchet Inception 距離是之後為此提出的（Heusel 等人，2017）。

## 參考文獻

### 開創性論文

- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — 論文本身：對抗框架、極小極大目標、證明，以及本頁所述的 MLP 實驗。
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1701.04862 — 分析 GAN 訓練為何不穩定，以及原始目標為何會飽和。
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — 提出不同的目標，並報告它能消除模式崩潰等問題，其學習曲線也能追蹤樣本品質。
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* ICML. https://arxiv.org/abs/1801.04406 — 展示未經正則化的 GAN 收斂性反例，並分析哪些正則化方法能夠收斂。
- Heusel, M. et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. NeurIPS. https://arxiv.org/abs/1706.08500 — 提出 Fréchet Inception 距離，這是一種在沒有概似函數時為 GAN 評分的樣本式指標。

### 綜述與教科書

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — 為訊號處理讀者撰寫的原始框架與其變體綜述。

### 講座與影片

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — 作者關於原始框架、訓練細節與開放問題的教學報告，並附有習題。

[^1]: Goodfellow 等人（2014）的表 1。Parzen 窗估計的變異很大，因此該表中方法之間的小差異不應過度解讀。
