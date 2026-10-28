---
translation_reviewed: 2026-10-28
---

# RealNVP

RealNVP（Dinh、Sohl-Dickstein 與 Bengio，2016）是一種由仿射耦合層構成的[正規化流](../index.md)。每一層把輸入的一半原封不動地複製，並以複製的那一半的函數來縮放與平移另一半。它的逆映射與雅可比行列式都容易計算，因此模型能給出精確的似然與精確的取樣。

## 概述

NICE（Dinh 等人，2014）引入了加性耦合層。它把輸入的一半以另一半的函數平移，因此雅可比行列式為一，並保持體積不變。RealNVP 在平移之外加上縮放，使各層不再保持體積：一層可以拉伸某些方向，同時壓縮另一些方向。標題中的「非體積保持」指的就是這項改變。

## 核心概念

- **仿射耦合**：輸入被分成 \(x_{1:d}\) 與 \(x_{d+1:D}\)。前一部分原封不動地通過，並決定後一部分的變換方式；後一部分乘以 \(\exp(s(\cdot))\)，再加上 \(t(\cdot)\)。函數 \(s\) 與 \(t\) 是任意的網路，它們本身不需要求逆。
- **遮罩與壓縮**：二元遮罩決定哪些維度被複製。對於影像，論文交替使用空間上的棋盤式遮罩與通道式遮罩，並把每個 2 × 2 的像素區塊壓縮成通道。
- **多尺度架構**：經過若干層後，一半的維度被直接分出，送入潛在向量；其餘一半則繼續經過更多的層。

## 運作方式

在生成方向上，資料由潛在變數形成如下：

\[
x_{1:d} = z_{1:d}, \qquad x_{d+1:D} = z_{d+1:D} \odot \exp\big(s(z_{1:d})\big) + t(z_{1:d})
\]

逆映射不需要對 \(s\) 或 \(t\) 求逆：

\[
z_{d+1:D} = \big(x_{d+1:D} - t(x_{1:d})\big) \odot \exp\big(-s(x_{1:d})\big)
\]

雅可比矩陣是分塊三角的，包含一個單位矩陣區塊與一個對角區塊 \(\operatorname{diag}(\exp s)\)。因此其對數行列式就是縮放輸出的總和。若以標準高斯作為基底，

\[
\log p(x) = \log \mathcal{N}(z; 0, I) - \sum_{\text{層}} \sum_j s_j
\]

其中 \(z\) 是對 \(x\) 執行逆映射所得到的。論文中，\(s\) 是經 \(\tanh\) 輸出並乘以一個可學習的尺度，而 \(t\) 則是殘差網路的仿射輸出。

訓練時，先以 logit 變換把每個像素映射到連續空間，再把資料送入多尺度堆疊的逆方向，累加尺度項，並以 Adam 最大化平均對數似然。取樣時，從高斯分布抽取 \(z\)，沿生成方向執行；每一層都會平行地更新其所有維度。

## 結果

論文把它的每維位元數與自回歸基準模型 PixelRNN 比較。數值越低越好。CIFAR-10 報告的是測試集，其餘資料集報告的是驗證集。

| 資料集 | RealNVP | PixelRNN |
|---|---|---|
| CIFAR-10（測試集） | 3.49 | 3.00 |
| ImageNet 32 × 32（驗證集） | 4.28 | 3.86 |
| ImageNet 64 × 64（驗證集） | 3.98 | 3.63 |

在 LSUN 與 CelebA 上，論文報告的數值分別為 2.72 至 3.08，以及 3.02。作者表示，RealNVP 在每維位元數上並未超越 PixelRNN，但具有競爭力，而且效能隨參數數量增加而提升。它在自然影像上的樣本看起來清晰。

## 限制

- **似然的差距。**RealNVP 在 CIFAR-10 上約落後 PixelRNN 0.5 位元每維。每一層都會保留一半的維度不變，因此需要許多層。
- **仿射變換。**縮放加平移是重塑分布的一種有限方式。Ho 等人（2019）把仿射流列為流的限制之一，Durkan 等人（2019）則以樣條取代它們。
- **樣本品質。**最大似然在模型容量有限時重視多樣性而非樣本品質；部分 CelebA 樣本的機率非常低。

## 未解問題

- 與自回歸模型的差距，有多少來自耦合結構，又有多少來自尺度、去量化或條件網路的選擇？之後的工作，例如 [Glow](../glow/index.md) 與 Flow++，同時改動了其中數項。
- 能否在保持逆映射容易計算的同時，讓變換更具彈性？樣條是一種答案，但取捨尚未完全釐清。

## 參考文獻

### 開創性論文

- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — 論文本身：仿射耦合層、多尺度架構，以及本頁討論的自然影像結果。
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — 前身，具有加性耦合層，其單位雅可比行列式被 RealNVP 推廣為縮放的層。
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS. https://arxiv.org/abs/1807.03039 — 以可學習的可逆 1×1 卷積，取代 RealNVP 固定的通道反轉。
- Ho, J., Chen, X., Srinivas, A., Duan, Y. & Abbeel, P. (2019). *Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design*. ICML. https://arxiv.org/abs/1902.00275 — 顯示耦合層的仿射變換可以被改進。
- Durkan, C., Bekasov, A., Murray, I. & Papamakarios, G. (2019). *Neural Spline Flows*. NeurIPS. https://arxiv.org/abs/1906.04032 — 以單調樣條取代仿射耦合變換，樣條仍可解析求逆。

### 綜述與教科書

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 綜述正規化流，包括耦合設計，以及表達能力與計算成本之間的取捨。
