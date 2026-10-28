---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
---

# 隨機插值（Stochastic Interpolants）

隨機插值是 Albergo 與 Vanden-Eijnden（2023）提出的框架，用來在兩個分布之間建立時間相依的路徑，並沿此路徑學習速度場。此框架把流匹配與擴散模型涵蓋為同一家族中的兩個成員。Albergo、Boffi 與 Vanden-Eijnden 的後續工作把框架擴展到雜訊項，並與擴散模型更緊密地連結。家族總覽見[流匹配](index.md)頁。

## 概述

早期的流與擴散方法各自固定一種連接雜訊與資料的方式。隨機插值是一般函數 \(I_t(x_0, x_1)\)，輸入為雜訊樣本 \(x_0\) 與資料樣本 \(x_1\)，並滿足邊界條件使 \(x_0\) 位於 \(t=0\)、\(x_1\) 位於 \(t=1\)。任何插值的選擇都會給出一條機率路徑，並可為它學習速度場。如此便把路徑的選擇與訓練方法分開。

## 關鍵概念

- **插值** \(I_t(x_0, x_1) = a_t\,x_0 + b_t\,x_1\)，其中 \(a_0 = 1\)、\(a_1 = 0\)、\(b_0 = 0\)、\(b_1 = 1\)。論文的例子為 \(\cos(\tfrac{\pi}{2}t)\,x_0 + \sin(\tfrac{\pi}{2}t)\,x_1\)。
- **機率路徑**：當 \(x_0\) 與 \(x_1\) 分別獨立取自邊際分布 \(\rho_0\) 與 \(\rho_1\) 時，\(I_t\) 的分布。
- **速度**：時間導數 \(\partial_t I_t\)，其在 \(I_t = x\) 條件下的期望即定義邊際速度場。

## 運作方式

論文藉由最小化以下目標來學習速度估計 \(\hat v_t\)：

\[
G(\hat v) = \mathbb E\big[\lVert \hat v_t(I_t)\rVert^2 - 2\,\partial_t I_t \cdot \hat v_t(I_t)\big]
\]

論文指出，平方誤差形式 \(\mathbb E\lVert \hat v_t(I_t) - \partial_t I_t\rVert^2\) 具有相同的一階變分，因此也可以作為替代。它的最小值點是給定 \(I_t\) 時 \(\partial_t I_t\) 的條件期望，也就是邊際速度。抽樣時，方法沿學到的 ODE 從 \(t=0\) 積分到 \(t=1\)。

## 關鍵方法

### Building Normalizing Flows with Stochastic Interpolants（Albergo 與 Vanden-Eijnden，2023）

- **問題：** 流模型與擴散模型通常以各自獨立的構造來介紹，難以比較它們的路徑，也難以為新問題選擇其中之一。
- **核心想法：** 以兩個分布樣本之間的插值來定義路徑，並沿此路徑以回歸學習速度。只要滿足邊界條件，任何插值都可使用。
- **公式或演算法：** 上述回歸目標 \(G(\hat v)\)，插值由設計者選擇。每一步抽取 \(t\)、\(x_0\) 與 \(x_1\)，形成 \(I_t\)，並依目標更新 \(\hat v\)。
- **結果：** 論文的主要貢獻是框架與其目標函數，而非基準測試表格。
- **限制：** 論文的方法只使用機率流 ODE。論文也指出，重新取樣路徑的 SDE 係數在 \(t=0\) 與 \(t=1\) 處為奇異。插值的選擇留給設計者。

### Stochastic Interpolants: A Unifying Framework for Flows and Diffusions（Albergo、Boffi 與 Vanden-Eijnden，2023）

- **問題：** 2022 年的框架不允許插值中含有雜訊項，這限制了同一構造能涵蓋擴散模型的範圍。
- **核心想法：** 在插值中加入雜訊項。得到的隨機插值能在有限時間內精確連接兩個分布，並統一基於流與基於擴散的生成模型。
- **公式或演算法：** 含雜訊分量的一般插值，以同類型的回歸目標訓練。arXiv 摘要給出統一的主張，重用前應於論文中核對完整公式。
- **限制：** 框架本身是一般性的，實務表現取決於插值的選擇，以及搭配使用的訓練與抽樣程序。

## 關聯

- [條件流匹配](conditional-flow-matching.md)是此框架中的一個插值，即高斯最優傳輸路徑。
- [修正流](rectified-flow.md)使用線性插值 \(t\,x_1 + (1-t)\,x_0\)。
- [DDPM](../../diffusion/ddpm.md) 與[擴散模型](../../diffusion/index.md)頁涵蓋此框架的擴散面向。

## 開放問題

- 對於特定資料類型，哪一種插值能給出最佳的取樣效率。
- SDE 與 ODE 取樣器在品質與速度上如何比較。

## 參考文獻

### 開創性論文

- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 提出插值框架與本頁描述的回歸目標 \(G(\hat v)\)。
- Albergo, M. S., Boffi, N. M. & Vanden-Eijnden, E. (2023). *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*. arXiv. https://arxiv.org/abs/2303.08797 — 以雜訊項擴展框架，並連結流與擴散。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 條件流匹配目標，是插值框架的一個特例。

### 擴散背景

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). *Score-Based Generative Modeling through Stochastic Differential Equations*. ICLR. https://arxiv.org/abs/2011.13456 — 擴散模型的 SDE 觀點，隨機插值的 SDE 是它的推廣。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*. ICML. https://arxiv.org/abs/1503.03585 — 插值框架所推廣的早期擴散模型。
