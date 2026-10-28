---
translation_reviewed: 2026-10-28
---

# 符號與記號

本維基中使用的數學符號，讓讀者在任何頁面都能分辨一個字母代表什麼。各表涵蓋向量與矩陣、機率與期望值、損失與梯度、強化學習與生成模型，並標出承載不只一種意義的字母。

## 概述

本維基涵蓋數學、機器學習、神經科學與應用，頁面由不同作者撰寫。大多數頁面會在首次出現時介紹自己的符號，並遵循通用慣例，例如用 $\theta$ 表示模型參數、$\mathcal{L}$ 表示損失、$\gamma$ 表示折扣因子。本頁記錄這些慣例，以及同一個字母被用於不只一種意義的地方。

本頁是閱讀輔助，而不是標準。緊密遵循某篇特定論文的頁面，會在其正文中定義該論文的符號；各表描述的是讀者通常會遇到的情況。

撰寫本頁時對英文頁面中數學內容所做的統計，可以看出哪些符號較常見。最常見的是 $\theta$，出現在 66 個頁面的數學中；其次是 $\sigma$（38 個頁面）、$\lambda$（23 個頁面），以及 $\pi$、$\gamma$ 與 $\eta$（各 22 個頁面）。這些數字只是概估，因為同一頁面可能以多種角色使用同一符號。

## 核心概念

- **純量、向量、矩陣**：純量是單一數字，向量是有序的數列，矩陣是二維陣列。純量使用斜體，矩陣使用大寫字母，向量使用小寫字母，依頁面不同可能以粗體或一般字體書寫。
- **下標與上標**：下標通常標示會變動的對象，例如時間 $t$ 或第 $i$ 個單元。上標通常標示某種變體，例如 $Q^\pi$ 中的策略，或 $A^\top$ 中的轉置。
- **條件與取樣**：$p(x \mid \theta)$ 表示在給定 $\theta$ 的條件下 $x$ 的機率，$x \sim p$ 表示 $x$ 是從分布 $p$ 抽取的。
- **符號過載**：同一個字母有兩種或更多意義。這在數學中很常見，也是跨頁面混淆的主要來源，因此最後一張表列出本維基中的各種情況。
- **對數**：除非頁面另有說明，不寫底數的 $\log$ 指自然對數。若頁面報告位元數，會明確說明底數為 2，例如 [PixelCNN](../../theory/paradigms/unsupervised/density-and-generative-models/autoregressive/pixelcnn/index.md) 頁面。

## 向量、矩陣與張量

| 對象 | 慣例 | 範例 | 出現位置 |
|---|---|---|---|
| 純量 | 小寫斜體字母；許多係數使用希臘字母 | $\eta$、$\gamma$、$\lambda$ | 幾乎每個頁面 |
| 向量 | 小寫。電腦視覺與多智能體頁面用粗體 $\mathbf{x}$；[線性代數](../../theory/math/linear-algebra/index.md) 概覽用一般斜體 $x$ | $x \in \mathbb{R}^d$ | [可變形卷積](../../theory/models/cnn/convolution-variants/deformable-convolution/index.md) |
| 矩陣 | 大寫字母。權重寫為 $W$；資料矩陣寫為 $X$，每列一個樣本 | $X \in \mathbb{R}^{n\times d}$ | [PCA](../../theory/math/linear-algebra/pca/index.md) |
| 轉置與內積 | $A^\top$ 表示轉置（未使用 $A^{T}$ 的寫法）；$a^\top b$ 表示內積 | $\cos\theta = \frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}$ | [線性代數](../../theory/math/linear-algebra/index.md) |
| 範數 | $\lVert\cdot\rVert$，並以下標標示類型 | $\lVert x\rVert_2$、$\lVert M\rVert_F$ | [線性代數](../../theory/math/linear-algebra/index.md) |
| 逐元素乘積 | $\odot$ | $\sigma(W_g x)\odot \tanh(W_f x)$ | [GRU](../../theory/models/rnn/gated-cells/gru/index.md) |
| 特徵值與奇異值 | $Av=\lambda v$；$A = U\Sigma V^\top$，奇異值為 $\sigma_i$ | $A_k = U_k \Sigma_k V_k^\top$ | [截斷奇異值分解](../../theory/math/linear-algebra/truncated-svd/index.md) |
| 特殊矩陣與向量 | $I$ 表示單位矩陣，$\mathbf{0}$ 表示零向量，$\mathbf{1}$ 表示全為一的向量 | $\mathcal{N}(0, I)$ | [機率與統計](../../theory/math/probability-statistics/index.md) |
| 指示函數 | $\mathbb{1}[\cdot]$ 在條件成立時為 1，否則為 0 | $\mathbb{1}[y_i = k]$ | [機率與統計](../../theory/math/probability-statistics/index.md) |

## 機率、期望值與資訊

| 量 | 慣例 | 範例 | 出現位置 |
|---|---|---|---|
| 密度或質量 | $p(\cdot)$ 表示資料或模型分布；$p_\theta$ 表示參數為 $\theta$ 的模型；$q$ 表示近似分布 | $p_\theta(x)$ | [機率方法](../../theory/paradigms/probabilistic/index.md) |
| 條件 | 以 `\mid` 書寫的直線，並保留間距 | $p(x \mid \theta)$ | [最大似然](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| 取樣 | $x \sim p$；高斯分布寫為 $\mathcal{N}(\mu, \sigma^2)$ | $\varepsilon \sim \mathcal{N}(0, I)$ | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| 期望值 | $\mathbb{E}_{x\sim p}[f(x)]$。下標標示分布，若意義明確則省略 | $\mathbb{E}_\pi[G_t \mid s_t = s]$ | [機率與統計](../../theory/math/probability-statistics/index.md) |
| 變異數 | $\mathrm{Var}(X)$；共變異數矩陣寫為 $C$ 或 $\Sigma$，見過載表 | $\mathrm{Var}(X)$ | [機率與統計](../../theory/math/probability-statistics/index.md) |
| 似然 | $L(\theta)$ 表示似然，$\ell(\theta)$ 表示對數似然，$\arg\max$ 表示使其最大的參數 | $\ell(\theta) = \sum_i \log p(x_i \mid \theta)$ | [最大似然](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| 事前與事後分布 | $p(\theta)$ 表示事前分布；$p(\theta \mid \mathcal{D})$ 表示事後分布 | $p(y \mid x, \mathcal{D})$ | [不確定性與校準](../../theory/machine-learning/uncertainty-and-calibration/index.md) |
| 熵 | $H(p)$ 表示熵，$H(p,q)$ 表示交叉熵 | $H(p,q) = H(p) + D_{\mathrm{KL}}(p \Vert q)$ | [資訊理論](../../theory/information-theory/index.md) |
| 散度 | 資訊理論頁面寫為 $D_{\mathrm{KL}}(p \Vert q)$；VAE 與變分推論頁面寫為 $\mathrm{KL}(q \Vert p)$ | $\mathrm{KL}(q_\phi(z \mid x) \,\Vert\, p(z))$ | [資訊理論](../../theory/information-theory/index.md) |

兩種 KL 散度的寫法指的是同一個量。資訊理論頁面以下標寫 $D_{\mathrm{KL}}$，變分頁面則寫 $\mathrm{KL}$，後接括號中的兩個分布。

## 損失、梯度與參數

| 量 | 慣例 | 範例 | 出現位置 |
|---|---|---|---|
| 參數 | $\theta$ 表示模型的參數；$\phi$ 表示第二組參數，通常是編碼器；$\theta^{-}$ 表示凍結的目標網路 | $Q(s, a; \theta)$ | [深度 Q 網路](../../theory/paradigms/reinforcement-learning/deep-q-networks/index.md) |
| 模型與預測 | $f_\theta$ 將輸入映射為輸出；$\hat{y}$ 為預測值，$y$ 為標籤 | $\hat{y} = f_\theta(x)$ | [機器學習](../../theory/machine-learning/index.md) |
| 損失 | $\mathcal{L}$，通常被最小化 | $\mathcal{L}(\theta)$ | [機器學習](../../theory/machine-learning/index.md) |
| 梯度 | $\nabla_\theta$ 表示對其下方所列變數的梯度 | $\nabla_\theta \mathcal{L}(\theta)$ | [梯度下降](../../theory/math/calculus/gradient-descent/index.md) |
| 學習率與步數 | $\eta$ 表示學習率；$t$ 表示步數，$\theta_{t-1}$ 為該步之前的值 | $\theta_t = \theta_{t-1} - \eta\,\nabla_\theta\mathcal{L}$ | [Adam](../../theory/optimization/adaptive/adam.md) |
| 正規化 | $\lambda$ 表示懲罰項或權重衰減的強度 | $\theta_t = \theta_{t-1} - \eta\,(\dots + \lambda\,\theta_{t-1})$ | [AdamW](../../theory/optimization/adaptive/adamw.md) |
| 資料 | $D$ 或 $\mathcal{D}$ 表示資料集；$(x_i, y_i)$ 表示第 $i$ 個樣本；$N$ 或 $n$ 表示其大小 | $D = \{(x_i, y_i)\}_{i=1}^{N}$ | [最大似然](../../theory/math/probability-statistics/maximum-likelihood/index.md) |
| 層 | $W$ 與 $b$ 分別表示權重與偏置；$\sigma$ 表示非線性函數 | $h = \sigma(Wx + b)$ | [線性代數](../../theory/math/linear-algebra/index.md) |
| 溫度 | softmax 或指數函數內的 $\tau$ 或 $T$ | $\exp(s/\tau)$ | [對比學習](../../theory/paradigms/self-supervised/contrastive-learning/index.md) |

## 強化學習

| 量 | 慣例 | 範例 | 出現位置 |
|---|---|---|---|
| 狀態、動作、觀測 | $s_t$ 表示狀態，$a_t$ 表示動作；當智能體只看得到部分狀態時使用 $o_t$ | $a_t \sim \pi(\cdot \mid s_t)$ | [強化學習](../../theory/paradigms/reinforcement-learning/index.md) |
| 獎勵 | 教科書慣例是 $r_{t+1}$ 為在 $s_t$ 採取動作後得到的獎勵。部分頁面改寫為 $r_t$ | $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ | [強化學習](../../theory/paradigms/reinforcement-learning/index.md)、[多巴胺](../../brain-mind/neuroscience/dopamine-reward-prediction-error/index.md) |
| 折扣與回報 | $\gamma$ 表示折扣因子；$G_t$ 表示折扣後的回報 | $G_t = \sum_{k\ge 0} \gamma^k r_{t+k+1}$ | [強化學習](../../theory/paradigms/reinforcement-learning/index.md) |
| 策略 | $\pi(a \mid s)$ 表示隨機策略；$\pi_\theta$ 表示參數化的策略；$\mu$ 表示確定性策略 | $\mu_i(o_i)$ | [策略梯度](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md)、[MADDPG](../../theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md) |
| 價值函數 | $V^\pi(s)$ 表示狀態價值；$Q^\pi(s,a)$ 表示動作價值；$Q^*$ 表示最佳動作價值 | $Q^*(s,a) = \mathbb{E}[r + \gamma \max_{a'} Q^*(s', a')]$ | [基於價值的方法](../../theory/paradigms/reinforcement-learning/value-based-methods/index.md) |
| 優勢 | $A_t$ 表示時間 $t$ 的優勢估計 | $\nabla_\theta J(\theta) = \mathbb{E}[\sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\, A_t]$ | [策略梯度](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md) |
| 轉移 | $P(s' \mid s, a)$ 表示轉移到 $s'$ 的機率 | $P(s' \mid s, \mathbf{a})$ | [多智能體強化學習](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md) |
| 聯合量 | 粗體 $\mathbf{a}$ 表示所有智能體的聯合動作；$\boldsymbol{\tau}$ 表示其聯合歷史 | $Q_{\text{tot}}(\boldsymbol{\tau}, \mathbf{a})$ | [QMIX](../../theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index.md) |

## 生成模型

| 量 | 慣例 | 範例 | 出現位置 |
|---|---|---|---|
| 資料與潛在變數 | $x$ 表示資料；$z$ 表示潛在變數，$p(z)$ 為其先驗 | $p_\theta(x \mid z)$ | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| 編碼器與解碼器 | $q_\phi(z \mid x)$ 表示編碼器；$p_\theta(x \mid z)$ 表示解碼器 | $\mathcal{L}(\theta, \phi; x)$ 表示證據下界 | [VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md) |
| 雜訊排程 | $\beta_t$ 表示第 $t$ 步加入的變異數；$\alpha_t = 1 - \beta_t$；$\bar\alpha_t = \prod_{s \le t} \alpha_s$ | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \epsilon$ | [DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md) |
| 去噪器 | $\epsilon_\theta(x_t, t)$ 預測加入 $x_t$ 的雜訊 | $\hat{x}_0 = \dfrac{x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta(x_t, t)}{\sqrt{\bar\alpha_t}}$ | [DDIM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddim.md) |
| 流匹配 | $x_0$ 表示雜訊樣本；$x_1$ 表示資料樣本；$t$ 表示時間，取自 $[0,1]$；$v_\theta$ 表示學到的速度場 | $x_t = (1-t)\,x_0 + t\,x_1$ | [流匹配](../../theory/paradigms/unsupervised/density-and-generative-models/flow-matching/index.md) |

## 同一符號的多種意義

下表列出英文頁面中承載不只一種意義的字母。讀者在依賴某個定義前，應先確認各頁面開頭的定義。

| 符號 | 本維基中的意義 | 出現位置 |
|---|---|---|
| $\sigma$ | 激活函數；標準差或變異數（$\sigma^2$）；雜訊水準；知識蒸餾中的 softmax；NeRF 中的密度；SVD 中的奇異值 | [深度學習](../../theory/deep-learning/index.md)、[知識蒸餾](../../theory/model-compression/knowledge-distillation/index.md)、[NeRF](../../theory/models/computer-vision/3d-and-neural-rendering/nerf/index.md)、[截斷奇異值分解](../../theory/math/linear-algebra/truncated-svd/index.md) |
| $\pi$ | 強化學習中的策略；EM 中的混合權重 $\pi_k$；最佳傳輸流匹配中的運輸計畫；MCMC 中的目標分布；餘弦排程中的圓周率 3.14 | [強化學習](../../theory/paradigms/reinforcement-learning/index.md)、[EM](../../theory/math/probability-statistics/expectation-maximisation/index.md)、[OT-CFM](../../theory/paradigms/unsupervised/density-and-generative-models/flow-matching/ot-cfm/index.md)、[MCMC](../../theory/paradigms/probabilistic/mcmc/index.md) |
| $\lambda$ | 特徵值；正規化或權重衰減的強度；泛指的超參數 | [線性代數](../../theory/math/linear-algebra/index.md)、[AdamW](../../theory/optimization/adaptive/adamw.md)、[超參數最佳化](../../theory/optimization/hyperparameter-optimisation.md) |
| $\tau$ | 對比學習中的 softmax 溫度；QMIX 中的聯合歷史；嶺迴歸中作為 MAP 的先驗尺度；連續時間發放率模型中的時間常數 | [對比學習](../../theory/paradigms/self-supervised/contrastive-learning/index.md)、[QMIX](../../theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index.md)、[最大似然](../../theory/math/probability-statistics/maximum-likelihood/index.md)、[工作記憶](../../brain-mind/working-memory-executive-function/funahashi-1989/index.md) |
| $\epsilon$ 與 $\varepsilon$ | Adam 中的小常數 $\epsilon$；擴散模型中的雜訊 $\epsilon$；VAE 與 FFJORD 中的雜訊 $\varepsilon$；前向模式微分中的對偶數單位 $\varepsilon$ | [Adam](../../theory/optimization/adaptive/adam.md)、[DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)、[VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md)、[前向模式](../../theory/math/automatic-differentiation/forward-mode/index.md) |
| $\Sigma$ 與 $C$ | SVD 中由奇異值構成的對角矩陣 $\Sigma$；EM 中某高斯成分的共變異數 $\Sigma_k$；PCA 中的資料共變異數 $C$ | [截斷奇異值分解](../../theory/math/linear-algebra/truncated-svd/index.md)、[EM](../../theory/math/probability-statistics/expectation-maximisation/index.md)、[PCA](../../theory/math/linear-algebra/pca/index.md) |
| $G_t$ | 強化學習中的折扣回報；Shampoo 中第 $t$ 步的梯度 | [強化學習](../../theory/paradigms/reinforcement-learning/index.md)、[Shampoo](../../theory/optimization/shampoo.md) |
| $\mathcal{L}$ | 損失，要被最小化；在 VAE 與變分推論中是要被最大化的證據下界 | [機器學習](../../theory/machine-learning/index.md)、[VAE](../../theory/paradigms/unsupervised/density-and-generative-models/vae/index.md)、[變分推論](../../theory/paradigms/probabilistic/variational-inference/index.md) |
| $D$ 與 $\mathcal{D}$ | 資料集；在 DSSM 檢索模型中，$D$ 為文件，$\mathcal{D}$ 為候選集合 | [最大似然](../../theory/math/probability-statistics/maximum-likelihood/index.md)、[DSSM](../../applications/search-and-information-retrieval/dssm/index.md) |
| $\theta$ | 模型參數；餘弦公式中的角度 | [線性代數](../../theory/math/linear-algebra/index.md) |
| $a$ 與 $\mathbf{a}$ | 單一智能體的動作；所有智能體的聯合動作 | [多智能體強化學習](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md) |
| $T$ | 步數（DDPM 中為 1000）；知識蒸餾與 [Glow](../../theory/paradigms/unsupervised/density-and-generative-models/normalising-flows/glow/index.md) 中的溫度 | [DDPM](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md)、[知識蒸餾](../../theory/model-compression/knowledge-distillation/index.md) |
| $\mu$ | 正規化層中的平均值；MADDPG 中的確定性策略 | [正規化](../../theory/deep-learning/normalisation/index.md)、[MADDPG](../../theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md) |

上表中有些慣例彼此也不一致。強化學習概覽中的獎勵索引為 $r_{t+1}$，但多巴胺頁面中的 TD 誤差寫作 $r_t$；雜訊符號在部分生成模型頁面為 $\epsilon$，在另一些頁面則為 $\varepsilon$。當某頁面偏離常見慣例時，值得確認該頁面定義的是哪一種。

## 關聯

[詞彙表](../glossary/index.md)提供本頁各概念的英文術語與繁體中文名稱。[線性代數](../../theory/math/linear-algebra/index.md)、[機率與統計](../../theory/math/probability-statistics/index.md)與[資訊理論](../../theory/information-theory/index.md)的概覽頁則定義了這些符號所代表的對象。

神經科學論文常使用自己的字母。[Funahashi（1989）的工作記憶頁面](../../brain-mind/working-memory-executive-function/funahashi-1989/index.md)將 $\tau$ 寫為連續時間發放率模型中的時間常數，而非溫度或先驗尺度。比較神經科學模型與機器學習模型時，應先將兩套符號對應起來。

## 參考文獻

### 開創性論文

- Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal. https://doi.org/10.1002/j.1538-7305.1948.tb01338.x — 將熵引入為資訊的度量，是資訊理論頁面使用 $H$ 符號的來源。
- Golub, G. & Kahan, W. (1965). *Calculating the Singular Values and Pseudo-Inverse of a Matrix*. Journal of the Society for Industrial and Applied Mathematics, Series B. https://doi.org/10.1137/0702016 — 提出計算矩陣奇異值的數值穩定演算法，這些奇異值即截斷奇異值分解頁面所依據的 $A = U\Sigma V^\top$ 分解中的量。
- Dempster, A. P., Laird, N. M. & Rubin, D. B. (1977). *Maximum Likelihood from Incomplete Data Via the EM Algorithm*. Journal of the Royal Statistical Society, Series B. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x — 提出 EM 演算法及其期望完整資料對數似然 $Q(\theta \mid \theta^t)$，即 EM 頁面使用的形式。
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — 提出變分自編碼器及其目標函數，使用 VAE 頁面所採用的 $q_\phi(z \mid x)$ 與 $p_\theta(x \mid z)$ 記號。
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — 定義變異數排程 $\beta_t$、$\alpha_t$ 與 $\bar\alpha_t$，以及擴散頁面所用的雜訊預測目標。
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — 提出 Adam 最佳化器，其學習率 $\eta$、一階與二階矩的衰減率 $\beta_1$ 與 $\beta_2$，以及小常數 $\epsilon$ 即 Adam 頁面的符號。
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — 深度 Q 網路論文，以參數 $\theta$ 將動作價值函數寫為 $Q(s, a; \theta)$。
- Rashid, T. et al. (2018). *QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning*. arXiv. https://arxiv.org/abs/1803.11485 — 提出將各智能體價值合併為 $Q_{\text{tot}}$ 的混合網路，即 QMIX 頁面所用的聯合價值。
- Lowe, R. et al. (2017). *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments*. arXiv. https://arxiv.org/abs/1706.02275 — 提出 MADDPG，各智能體具確定性策略 $\mu_i(o_i)$，並使用可見所有智能體動作的集中式評論家。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv. https://arxiv.org/abs/1503.02531 — 提出帶有 softmax 溫度 $T$ 的知識蒸餾，是蒸餾頁面溫度符號的來源。
