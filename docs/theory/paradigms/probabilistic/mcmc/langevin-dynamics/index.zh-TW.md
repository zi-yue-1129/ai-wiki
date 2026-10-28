---
translation_reviewed: 2026-10-28
---

# 朗之萬動力學

朗之萬動力學是一種取樣方法，它在每一步沿著對數密度的梯度移動一個狀態，並加入隨機雜訊。作為 [MCMC](../index.md) 方法，它從目標分布抽樣。若搭配學習得到的分數，它就能在分數式生成模型中產生樣本，而這類模型與現代擴散模型密切相關。

## 概述

朗之萬擴散是一個隨機微分方程，其平穩分布就是給定的目標 $\pi$。它沿著 $\log\pi$ 的梯度把狀態推向高機率區域，並加入高斯雜訊，使狀態不會全部塌縮到眾數上。電腦只能採用離散步長，因此得到的鏈除非加以修正，否則會有偏誤。Roberts 與 Tweedie（1996）給出了朗之萬擴散及其離散近似收斂到目標的條件。

此方法有兩個用途。在 MCMC 中，它提供可以用接受－拒絕步驟修正的提議，改善了[Metropolis–Hastings 演算法](../metropolis-hastings/index.md)中的隨機漫步。在生成式建模中，分數由資料學習得來，朗之萬步驟再從它抽出樣本。Song 與 Ermon（2019）以多個雜訊水準的退火程序提出了這個方法。

## 核心概念

- **分數**：對數密度的梯度 $\nabla_x \log p(x)$。它指向機率較高的方向，而且不需要正規化常數。
- **未修正朗之萬演算法（ULA）**：沒有接受－拒絕步驟的離散化鏈。它簡單但有偏誤，偏誤大小取決於步長。
- **MALA**：加上 Metropolis–Hastings 修正的 ULA，能消除偏誤。
- **去噪分數匹配**：藉由預測加在資料上的雜訊來學習分數（Vincent, 2011）。

## 運作方式

連續過程為

$$
dX_t = \nabla_x \log \pi(X_t)\,dt + \sqrt{2}\,dW_t,
$$

其中 $W_t$ 為布朗運動。以步長 $\eta$ 離散化的 ULA 為

$$
x_{k+1} = x_k + \eta\,\nabla_x \log\pi(x_k) + \sqrt{2\eta}\,\xi_k, \qquad \xi_k \sim \mathcal{N}(0, I).
$$

MALA 以同一表達式作為提議，並以 Metropolis–Hastings 機率接受它。Roberts 與 Rosenthal（1998）說明步長必須如何隨維度縮放，最佳接受率約為 0.574。

Song 與 Ermon（2019）把退火朗之萬動力學應用於學習得到的分數 $s_\theta(x, \sigma)$。對於雜訊水準 $\sigma_1 > \dots > \sigma_L$，他們在每個水準執行 $T$ 步

$$
x \leftarrow x + \alpha_i\, s_\theta(x, \sigma_i) + \sqrt{2\alpha_i}\,z, \qquad z \sim \mathcal{N}(0, I),
$$

其中 $\alpha_i = \varepsilon\,\sigma_i^2/\sigma_L^2$，並由最大的雜訊水準逐步走到最小的水準。

Song 等人（2020）把加噪過程的反向寫成以分數為漂移項的隨機微分方程，

$$
dX_t = \big[f(X_t, t) - g(t)^2\,\nabla_x \log p_t(X_t)\big]\,dt + g(t)\,d\bar W_t,
$$

而朗之萬步驟可以作為校正器。Ho 等人（2020）把去噪擴散模型的訓練與帶朗之萬動力學的去噪分數匹配連結起來。

## 實驗結果

Roberts 與 Rosenthal（1998）指出，對於從朗之萬擴散導出的 Metropolis 型提議，其效率由接受率決定，而非由目標決定。漸近最佳的接受率約為 0.574，計算成本隨維度的立方根增長，而隨機漫步提議則是線性增長。

Song 與 Ermon（2019）報告，他們的樣本在 MNIST、CelebA 與 CIFAR-10 上可與生成對抗網路相比。[^1] Song 等人（2020）報告，他們的分數模型在 CIFAR-10 的無條件影像生成上達到創紀錄的表現。[^2] 這些結果衡量的是生成樣本的品質，而不是取樣器作為 MCMC 方法的混合性。

[^1]: CIFAR-10 上 8.87 的 Inception 分數取自 Song 與 Ermon（2019）的摘要。
[^2]: CIFAR-10 上 9.89 的 Inception 分數與 2.20 的 FID 取自 Song 等人（2020）的摘要，它們針對特定架構與訓練設定。

## 限制

- **離散化偏誤**。ULA 對任何固定步長都有偏誤。MALA 能消除偏誤，但會拒絕一部分移動，每一步的成本也較高。
- **多峰目標**。局部的梯度方法可能停留在某一模態，這就是生成式設定中會使用退火的原因。
- **分數誤差**。生成的樣本取決於分數學得的準確度。
- **步數很多**。退火取樣在每個雜訊水準都需要許多步，因此生成很慢。

## 開放問題

- 朗之萬型取樣器的離散化誤差，與擴散模型取樣器的誤差之間有什麼關係？
- 為什麼沿雜訊水準退火會有幫助？對於某一資料分布，需要多少個水準？

## 參考文獻

### 開創性論文

- Roberts, G. O. & Tweedie, R. L. (1996). Exponential Convergence of Langevin Distributions and Their Discrete Approximations. *Bernoulli*. https://doi.org/10.2307/3318418 — 給出朗之萬擴散及其離散近似收斂到目標分布的條件。
- Song, Y. & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. arXiv. https://arxiv.org/abs/1907.05600 — 以多個雜訊水準上估計的分數，透過退火朗之萬動力學生成樣本。
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2020). Score-Based Generative Modeling through Stochastic Differential Equations. arXiv. https://arxiv.org/abs/2011.13456 — 以漂移項為分數的前向與反向隨機微分方程，統一分數模型與擴散模型。
- Vincent, P. (2011). A Connection Between Score Matching and Denoising Autoencoders. *Neural Computation*. https://doi.org/10.1162/NECO_a_00142 — 證明去噪自編碼器與某密度估計的分數相吻合，連結了去噪訓練與分數式取樣。

### 綜述與教科書

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — 以與去噪分數匹配及朗之萬動力學相關的目標訓練擴散模型。

### 文章與文件

- Roberts, G. O. & Rosenthal, J. S. (1998). Optimal Scaling of Discrete Approximations to Langevin Diffusions. *JRSS B*. https://doi.org/10.1111/1467-9868.00123 — 給出朗之萬擴散導出之 Metropolis 型提議的最佳接受率與維度縮放。
