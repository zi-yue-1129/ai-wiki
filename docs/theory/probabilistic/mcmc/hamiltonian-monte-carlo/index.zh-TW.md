---
translation_reviewed: 2026-10-28
---

# 哈密頓蒙地卡羅與 NUTS

哈密頓蒙地卡羅（Hamiltonian Monte Carlo, HMC）是一種 [MCMC](../index.md) 方法，它利用對數密度的梯度來提出較遠的移動。它模擬一個質點在負對數密度所定義的地形上的物理運動，然後以接受－拒絕步驟修正結果。不掉頭取樣器（No-U-Turn Sampler, NUTS）免去了手動設定模擬長度的需要，它也是 Stan 的預設取樣器。

## 概述

[Metropolis–Hastings](../metropolis-hastings/index.md) 等方法中的隨機漫步式提議，每次都是微小且近乎隨機的移動，因此探索分布的速度很慢。HMC 則改由物理模型來產生提議。質點在負對數密度所定義的地形上移動，因此能走得很遠，同時停留在機率高的區域。此方法由 Duane 等人（1987）為格點場論的模擬而提出，名為混合蒙地卡羅（hybrid Monte Carlo）。Neal（2012）以教學文章把它引入統計學，Betancourt（2017）則從幾何角度解釋它為何在困難的目標上表現良好。

HMC 需要可微的目標，梯度通常由[自動微分](../../../math/automatic-differentiation/index.md)提供。它的主要缺點是調校步長與模擬步數，而 NUTS 免除了後者。

## 核心概念

- **位置與動量**：取樣器為每個參數 $q$ 引入一個輔助的動量 $p$。位置 $q$ 是我們關心的變數，動量在每一步結束後就被丟棄。
- **哈密頓量**：總能量 $H(q, p) = U(q) + K(p)$，即位能 $U(q) = -\log\tilde\pi(q)$ 與動能 $K(p)$ 之和。
- **蛙跳積分器**：以步長 $\varepsilon$ 近似動力學的數值方法。它具有時間可逆與保體積的性質，而接受－拒絕步驟依賴這些性質。
- **質量矩陣** $M$：重新縮放動量的矩陣。當參數的尺度差異很大時，選擇適當的質量矩陣很重要。
- **軌跡長度**：蛙跳步數。太少會出現隨機漫步的行為，太多則浪費計算。

## 運作方式

哈密頓動力學為

$$
\frac{dq}{dt} = M^{-1}p, \qquad \frac{dp}{dt} = \nabla_q \log\tilde\pi(q).
$$

精確的動力學會保持能量守恆，因此軌跡終點的機率與起點相同。離散積分器造成的誤差，則由接受－拒絕步驟修正。一次 HMC 更新如下：

1. 抽取動量 $p \sim \mathcal{N}(0, M)$。
2. 從 $(q, p)$ 出發執行 $L$ 步蛙跳。每一步先以在 $q$ 處的梯度把 $p$ 更新半步，再把 $q$ 移動一整步，然後以在新 $q$ 處的梯度把 $p$ 再更新半步。
3. 以機率 $\min\!\big(1, \exp\{H(q,p) - H(q^*,p^*)\}\big)$ 接受終點 $(q^*, p^*)$，否則保留 $q$。

NUTS 以自適應規則取代固定的 $L$。從目前狀態出發，它沿隨機選擇的方向把軌跡倍增，並建立一棵由狀態組成的二元樹。當軌跡開始折回自身時停止，判斷依據是兩端動量上的 U 轉條件。步長在暖機期間以原始對偶平均（primal–dual averaging）調整（Hoffman & Gelman, 2011）。Stan 以此方案作為預設取樣器（Carpenter 等人，2017）。

## 實驗結果

Hoffman 與 Gelman（2011）在數個模型上比較 NUTS 與經過良好調校的標準 HMC。他們的主要主張是，NUTS 的效率至少與調校良好的 HMC 相當，有時更高，而且不需要使用者介入，也不需要昂貴的調校執行。論文同時引入了使其成為可能的步長適應方法。證據是在一組測試模型上的實證比較，論文並未宣稱普遍的加速。

## 限制

- **需要梯度**。含有離散變數、或密度無法微分的目標不在此方法的適用範圍內，除非經過重新參數化。
- **幾何**。HMC 的效率取決於目標的形狀。Betancourt（2017）解釋了它為何在形狀良好的目標上表現良好，而困難的幾何，例如階層模型中的狹窄漏斗，會使它吃力。
- **調校**。質量矩陣與步長仍須設定得當。黎曼變體可以自動適應幾何，但需要額外成本（Girolami & Calderhead, 2011）。
- **多峰性**。與其他局部取樣器一樣，HMC 一次只能探索一個模態。

## 開放問題

- 如何在執行中學習質量矩陣，這類方法在極高維中表現如何？
- 能否讓 HMC 型取樣器有效處理離散參數？許多模型都含有離散參數。

## 參考文獻

### 開創性論文

- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B*. https://doi.org/10.1016/0370-2693(87)91197-X — 提出結合哈密頓動力學與 Metropolis 修正的混合蒙地卡羅，用於格點場論模擬。
- Hoffman, M. D. & Gelman, A. (2011). The No-U-Turn Sampler: Adaptively Setting Path Lengths in Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1111.4246 — 提出 NUTS，能自動決定軌跡長度並即時調整步長。

### 綜述與教科書

- Neal, R. M. (2012). MCMC using Hamiltonian dynamics. arXiv. https://arxiv.org/abs/1206.1901 — 關於哈密頓動力學作為 MCMC 提議機制的教學文章，附有調校建議。

### 文章與文件

- Betancourt, M. (2017). A Conceptual Introduction to Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1701.02434 — 從幾何角度解釋 HMC 表現良好的原因，以及應如何調校。
- Girolami, M. & Calderhead, B. (2011). Riemann Manifold Langevin and Hamiltonian Monte Carlo Methods. *JRSS B*. https://doi.org/10.1111/j.1467-9868.2010.00765.x — 把朗之萬與哈密頓取樣器推廣到黎曼幾何，使提議無需試跑即可自動調整。
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., et al. (2017). Stan: A Probabilistic Programming Language. *Journal of Statistical Software*. https://doi.org/10.18637/jss.v076.i01 — 介紹 Stan 系統，它以 NUTS 作為預設取樣器，並被廣泛用於貝氏推論。
