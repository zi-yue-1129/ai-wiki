---
translation_reviewed: 2026-10-28
---

# 期望最大化（EM）演算法

期望最大化（EM）演算法用於在部分變數未被觀察到時求最大概似估計。它交替進行兩件事：先在目前參數下估計隱藏變數，再把這些估計當作已知，重新估計參數。它是擬合混合模型與許多其他潛在變數模型的標準工具。本頁所屬的主題是[AI 的機率與統計](../index.md)，而它所服務的估計量則見[最大概似估計](../maximum-likelihood/index.md)一頁。

## 概述

許多模型有從未被觀察到的變數：混合模型中產生每個點的成分、隱馬可夫鏈的狀態，或資料表中缺失的一格。令 $x$ 為觀察到的資料，$z$ 為隱藏變數，$\theta$ 為參數。觀察資料的概似要對未觀察到的值求和，

$$
\log p(x\mid\theta)=\log\sum_z p(x,z\mid\theta).
$$

對數無法移到和號之內，因此即使完整資料的概似 $p(x,z\mid\theta)$ 很簡單，其最大值點通常也沒有閉式解。Dempster、Laird 與 Rubin（1977）以 EM 之名提出解決此問題的一般迭代方法，並證明每一次迭代都不會使觀察資料的概似下降。

## 核心概念

- **責任（responsibility）**：在目前參數下，每個隱藏值的後驗機率 $p(z\mid x,\theta^{t})$。在混合模型中，它是某個點來自某個成分的機率。

## 運作方式

從參數 $\theta^{t}$ 開始，每次迭代有兩個步驟。

1. **E 步。** 在目前參數下計算隱藏變數的後驗，並形成
   $$Q(\theta\mid\theta^{t})=\mathbb{E}_{p(z\mid x,\theta^{t})}\big[\log p(x,z\mid\theta)\big].$$
2. **M 步。** 令 $\theta^{t+1}=\arg\max_\theta Q(\theta\mid\theta^{t})$。

M 步通常很容易，因為 $Q$ 是完整資料對數概似的期望值，其最大值點常有閉式解。

**例子：高斯混合。** 設成分權重為 $\pi_k$、均值為 $\mu_k$、共變異數為 $\Sigma_k$。E 步計算責任 $r_{ik}=p(z_i=k\mid x_i,\theta^t)$。M 步則把每個均值更新為以責任加權的平均，

$$
\mu_k=\frac{\sum_i r_{ik}\,x_i}{\sum_i r_{ik}},
$$

共變異數與權重也以相同方式更新。每個點會按責任比例分給各成分。

**下界的觀點。** 對隱藏變數上的任何分布 $q(z)$，由 Jensen 不等式可得

$$
\log p(x\mid\theta)\ \ge\ \mathbb{E}_{q}\big[\log p(x,z\mid\theta)\big]-\mathbb{E}_{q}\big[\log q(z)\big].
$$

當 $q(z)=p(z\mid x,\theta)$ 時，右側等於概似。Neal 與 Hinton（1998）以此觀點說明：E 步把 $q$ 設為後驗，M 步則對 $\theta$ 最大化此下界。這個下界就是[變分推論](../../../probabilistic/variational-inference/index.md)中的證據下界（ELBO），因此 EM 是對它做座標上升。

```mermaid
flowchart LR
  T["參數 θ(t)"] --> E["E 步：給定 x 與 θ(t) 的 z 後驗"]
  E --> Q["期望完整資料對數概似 Q"]
  Q --> M["M 步：對 θ 最大化 Q"]
  M --> T2["參數 θ(t+1)"]
  T2 -. 重複直到概似不再改變 .-> E
```

## 結果

Dempster、Laird 與 Rubin（1977）在缺失、設限與混合模型資料上展示此方法，其證據是分析性的，而非基準測量。Wu（1983）指出，在涵蓋許多實務模型的條件下，EM 收斂到概似的一個駐點，但不一定是最大值。Neal 與 Hinton（1998）指出，同樣的論證也支持漸進式與稀疏等變體，這些變體每一步只更新部分資料。

## 限制

- **局部最優。** 結果取決於初始參數，因此實務上會從多個起點執行 EM。
- **收斂緩慢。** 收斂通常是線性的，且可能很慢。
- **E 步難以計算。** 在許多模型中，$z$ 的後驗無法精確計算。變分或蒙地卡羅變體會近似它，但代價是失去單調性的保證。
- **標準誤。** EM 給出點估計，其標準誤需要額外工作。

## 開放問題

- 高維混合模型的全域收斂保證目前只有部分結果。
- 變分自編碼器學習一個編碼器，一次為所有資料近似 E 步。與精確 EM 相比，這會犧牲多少精確度，仍在研究中。

## 關聯

- **最大概似估計。** EM 是資料不完整時的最大概似方法；參見[最大概似估計](../maximum-likelihood/index.md)一頁。
- **變分推論。** EM 是對 ELBO 做座標上升的特例。[變分推論](../../../probabilistic/variational-inference/index.md)章節發展了一般情形。
- **大腦與心智。** 目前尚未建立 EM 與神經計算之間的直接關聯。[上層頁面](../index.md)中的「貝氏大腦」觀點是最接近的想法。

## 應用

- **分群。** 高斯混合模型以 EM 擬合，責任值提供軟性的分群指派。
- **隱馬可夫模型。** 訓練它的 Baum–Welch 演算法是 EM 的一個實例，隱藏狀態即為潛在變數。
- **因子分析。** 以少數隱藏因子解釋觀察變數的模型，以 EM 擬合。

## 參考文獻

### 開創性論文

- Dempster, A. P., Laird, N. M. & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society B*. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x — 提出 EM 演算法，並證明它不會使觀察資料的概似下降。
- Wu, C. F. J. (1983). On the convergence properties of the EM algorithm. *The Annals of Statistics*. https://doi.org/10.1214/aos/1176346060 — EM 收斂到概似駐點的條件。
- Neal, R. M. & Hinton, G. E. (1998). A view of the EM algorithm that justifies incremental, sparse, and other variants. In *Learning in Graphical Models*. https://doi.org/10.1007/978-94-011-5014-9_12 — 把 EM 視為對自由能下界的最大化，並由此推導漸進式變體。
- Kingma, D. P. & Welling, M. (2013). Auto-encoding variational Bayes. arXiv. https://arxiv.org/abs/1312.6114 — 以攤銷編碼器最大化下界來訓練潛在變數模型，是 E 步的神經網路版本。

### 綜述與教科書

- McLachlan, G. J. & Krishnan, T. (2008). *The EM Algorithm and Extensions*, 2nd ed. Wiley. https://doi.org/10.1002/9780470191613 — 關於 EM 理論、延伸與應用的專書。
