---
translation_reviewed: 2026-10-28
---

# 正規化流後驗

正規化流後驗（normalising-flow posteriors）由 Rezende 與 Mohamed（2015）提出，它讓[變分推論](../index.md)中的變分分布族變得更加豐富。方法是把一個簡單的密度推過一連串可逆映射，而這些映射的雅可比行列式很容易計算。這串映射與模型一起訓練，使近似後驗可以有高斯分布無法表達的形狀。

## 概述

平均場族把潛變數視為彼此獨立，而高斯族無法表達偏態或變數之間的強相依。Rezende 與 Mohamed 認為，這樣的限制會明顯影響推論的品質。

流已被用作密度模型，也就是以可逆映射把簡單分布轉換為複雜分布（Dinh 等人，2014）。2015 年的論文則把它用作深度潛變數高斯模型中的近似後驗（Rezende 等人，2014），並由推論網路把每個資料點映射到其流的參數，因此它同時具有彈性與攤銷的特性。

## 核心概念

- **變數變換**：若 \(z = f(z_0)\) 可逆，則 \(z\) 的密度等於基底密度在 \(z_0\) 的值除以 \(f\) 的雅可比行列式絕對值。
- **流的長度 \(K\)**：串接的變換數量。
- **平面流**：\(f(z) = z + u\,h(w^\top z + b)\)。它在垂直於一個超平面的方向上收縮與擴張空間。
- **體積守恆流**：行列式為一的變換，如 NICE。它計算便宜，但層與層之間需要額外的混合步驟。

## 運作方式

對於鏈 \(z_K = f_K \circ \cdots \circ f_1(z_0)\)，其密度由變數變換規則給出：

\[
\ln q_K(z_K) = \ln q_0(z_0) - \sum_{k=1}^{K}\ln\left|\det\frac{\partial f_k}{\partial z_{k-1}}\right|.
\]

對平面流而言，依矩陣行列式引理，行列式化簡為 \(|1 + u^\top\psi(z)|\)，其中 \(\psi(z) = h'(w^\top z + b)\,w\)。因此它的計算時間與維度呈線性關係。目標函數是以此族表示的 ELBO：

\[
\mathcal{L} = \mathbb{E}_{q_0}\big[\log p(x, z_K) - \log q_K(z_K)\big].
\]

訓練流程如下：

1. 推論網路把資料點 \(x\) 映射到流的參數。
2. 從簡單的基底密度抽出 \(z_0\)。
3. 套用 \(K\) 次變換，並累加對數行列式項。
4. 用此樣本估計 ELBO，並穿過流與推論網路做反向傳播，因為樣本是參數的可微函數。
5. 在前 10,000 次迭代中，把逆溫度 \(\beta\) 從 0.01 退火到 1。

## 實驗結果

論文提供三類證據。

- **二維密度。** 對四個非高斯目標分布，隨著流的長度從 2 增加到 8 再到 32，近似品質明顯提升。平面流與 NICE 在層數增加後能達到相近的表現，但平面流所需參數少得多（論文圖 3）。
- **二值化 MNIST。** 以 40 個潛變數的深度潛變數高斯模型訓練 500,000 次更新。論文報告的是負對數機率的上界（越低越好）。對角高斯後驗最多為 89.9；平面流在 \(K = 10\) 時最多為 87.5，在 \(K = 80\) 時最多為 85.1。\(K = 80\) 的 NICE 最多為 87.2（表 2）。
- **CIFAR-10 影像區塊。** 在相同的模型族下，較長的流系統性地提升了測試集的對數似然（表 3）。

## 限制

- **成本。** 每一層都增加參數與計算，而平面層只在一個方向上收縮或擴張空間，因此可能需要很多層。
- **結構。** 便宜的行列式計算限制了每個映射的形式。Papamakarios 等人（2019）綜述了表達力與成本之間的設計取捨。
- **繼承的限制。** 更豐富的分布族並不改變 ELBO 的非凸性（Blei 等人，2016）。Cremer 等人（2018）發現，攤銷推論的誤差常來自不夠好的辨識網路，而非近似分布的複雜度不足。因此，若推論網路不佳，彈性更大的族也未必有太大幫助。

## 開放問題

- 在高維中，哪一種流架構能在表達力與成本之間取得最好的平衡？Papamakarios 等人（2019）整理了各種選擇。Kingma 等人（2016）為大型潛在空間提出了自回歸流，而 Glow（Kingma & Dhariwal，2018）顯示可逆卷積能在生成模型中大規模運作。
- 能否同時改善分布族與推論網路，以縮小攤銷差距？

## 參考文獻

### 開創性論文

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. arXiv. https://arxiv.org/abs/1505.05770 — 藉由組合可逆映射建立彈性後驗，包含平面流與徑向流，並在深度潛變數模型中訓練。
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — 為密度建模提出體積守恆的可逆映射，本頁將它與平面流作比較。
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. arXiv. https://arxiv.org/abs/1401.4082 — 提出實驗中所用的深度潛變數高斯模型。
- Kingma, D. P., Salimans, T., Jozefowicz, R., Chen, X., Sutskever, I. & Welling, M. (2016). *Improving Variational Inference with Inverse Autoregressive Flow*. arXiv. https://arxiv.org/abs/1606.04934 — 提出可擴展到高維潛在空間的自回歸流，並改善了對角高斯後驗。

### 綜述與教科書

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 從機率建模與推論的角度綜述流，並說明流設計的原則。
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — 綜述變分推論、其目標函數與 ELBO 的局部最佳解。

### 文章與文件

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. arXiv. https://arxiv.org/abs/1807.03039 — 在生成流中使用可逆 1x1 卷積，在標準基準上的對數似然有明顯提升。
- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. arXiv. https://arxiv.org/abs/1801.03558 — 顯示訓練後 VAE 的近似誤差，很大一部分來自不夠好的辨識網路。
