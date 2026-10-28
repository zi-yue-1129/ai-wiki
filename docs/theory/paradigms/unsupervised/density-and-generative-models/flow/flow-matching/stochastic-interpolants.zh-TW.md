---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
---

# 隨機插值（Stochastic Interpolants）

隨機插值是 Albergo 與 Vanden-Eijnden（2023）提出的框架，用來在兩個分布之間建立時間相依的路徑，並沿此路徑學習速度場。此框架把流匹配與擴散模型涵蓋為同一家族中的兩個成員。Albergo、Boffi 與 Vanden-Eijnden 的後續工作在插值中加入雜訊項，並使此構造與擴散模型更緊密地連結。家族總覽見[流匹配](index.md)頁。

## 概述

早期的流與擴散方法各自固定一種連接雜訊與資料的方式。隨機插值是一般函數 \(I(t, x_0, x_1)\)，輸入為雜訊樣本 \(x_0\) 與資料樣本 \(x_1\)，並滿足邊界條件使 \(x_0\) 位於 \(t=0\)、\(x_1\) 位於 \(t=1\)。任何插值的選擇都會給出一條機率路徑，並可為它學習速度場。如此便把路徑的選擇與訓練方法分開。

## 關鍵概念

- **插值** \(I(t, x_0, x_1)\)：滿足 \(I(0, x_0, x_1) = x_0\) 與 \(I(1, x_0, x_1) = x_1\)，並且 \(|\partial_t I| \le C_1 |x_0 - x_1|\)。論文的例子是三角插值 \(\cos(\tfrac{\pi}{2}t)\,x_0 + \sin(\tfrac{\pi}{2}t)\,x_1\)。
- **機率路徑**：當 \(x_0\) 與 \(x_1\) 分別獨立取自邊際分布 \(\rho_0\) 與 \(\rho_1\) 時，\(I_t = I(t, x_0, x_1)\) 的分布。
- **速度**：時間導數 \(\partial_t I_t\)。其在 \(I_t = x\) 條件下的期望即為邊際速度場 \(v(t, x)\)。

## 運作方式

論文藉由最小化以下目標來學習速度估計 \(\hat v_t\)：

\[
G(\hat v) = \mathbb E\big[\lVert \hat v_t(I_t)\rVert^2 - 2\,\partial_t I_t \cdot \hat v_t(I_t)\big]
\]

其唯一的最小值點是邊際速度 \(v(t, x) = \mathbb E[\partial_t I_t \mid I_t = x]\)。論文指出，平方誤差形式 \(\mathbb E\lVert \hat v_t(I_t) - \partial_t I_t\rVert^2\) 與 \(G\) 具有相同的一階變分，因此可用以取代 \(G\)。但一般而言，它在最佳點的值並不為零，所以它是一個不同的目標，只是具有相同的駐點方向。抽樣時，方法沿學到的 ODE 從 \(t=0\) 積分到 \(t=1\)。

## 關鍵方法

### Building Normalizing Flows with Stochastic Interpolants（Albergo 與 Vanden-Eijnden，2023）

- **問題：** 流模型與擴散模型通常以各自獨立的構造來介紹，難以比較它們的路徑，也難以為新問題選擇其中之一。
- **核心想法：** 以兩個分布樣本之間的插值來定義路徑，並沿此路徑以回歸學習速度。只要滿足邊界條件，任何插值都可使用。
- **公式或演算法：** 上述回歸目標 \(G(\hat v)\)，插值由設計者選擇。每一步抽取 \(t\)、\(x_0\) 與 \(x_1\)，形成 \(I_t\)，並依目標更新 \(\hat v\)。抽樣使用機率流 ODE。
- **結果：** 論文報告的是密度估計與影像生成實驗，而非單一基準。在其表格中的五個表格式資料集上，此方法在四個上勝過 FFJORD，而在 BSDS300 上 FFJORD 略勝。在 CIFAR-10 與 ImageNet 32×32 上，FID 數值依論文的說法「接近擴散模型，但略遜於最佳結果」。論文也報告了 128×128 的影像實驗。
- **限制：** 論文指出，對應 SDE 的漂移項與擴散係數在 \(t=0\) 與 \(t=1\) 處為奇異，因此實務上以 ODE 為抽樣器。插值的選擇留給設計者。

### Stochastic Interpolants: A Unifying Framework for Flows and Diffusions（Albergo、Boffi 與 Vanden-Eijnden，2023）

- **問題：** 2022 年的框架使用確定性插值，因此無法在同一構造中涵蓋隨機取樣器的家族，也無法與流統一。
- **核心想法：** 在插值中加入雜訊項。一般隨機插值為 \(x_t = I(t, x_0, x_1) + \gamma(t)\,z\)，其中 \(z\sim\mathcal N(0, I)\) 與 \((x_0, x_1)\) 獨立，\(\gamma(0)=\gamma(1)=0\)，且在 \((0,1)\) 上 \(\gamma(t)>0\)。\(x_t\) 的分布在 \(t=0\) 與 \(t=1\) 精確符合目標分布，這正是論文所說在有限時間內連接兩個分布的意思。
- **公式或演算法：** 漂移項以二次速度目標 \(\mathcal L_b[\hat b] = \int_0^1 \mathbb E\big[\tfrac12\lvert\hat b(t, x_t)\rvert^2 - (\partial_t I + \dot\gamma(t)\,z)\cdot\hat b(t, x_t)\big]\,\mathrm dt\) 學習，其最小值點為 \(b(t, x) = \mathbb E[\dot x_t \mid x_t = x]\)。分數函數以 \(\mathcal L_s[\hat s] = \int_0^1 \mathbb E\big[\tfrac12\lvert\hat s(t, x_t)\rvert^2 + \gamma^{-1}(t)\,z\cdot\hat s(t, x_t)\big]\,\mathrm dt\) 學習，最小值點為 \(s = -\gamma^{-1}\eta_z\)，其中 \(\eta_z(t, x) = \mathbb E[z \mid x_t = x]\)。擴散係數為 \(\varepsilon(t)\) 的前向與後向 SDE 具有相同的邊際分布，論文並指出，分數擴散模型可在時間重新參數化後改寫為單邊插值。
- **結果：** 論文主要是框架與證明性的工作。其實驗部分涵蓋二維與 128 維的高斯混合，以及影像生成。本頁未完整核對數值結果，因此不引用數字。
- **限制：** 與 2022 年的論文相同，SDE 的係數在端點為奇異。論文也指出，對插值做最佳化可恢復薛丁格橋，但它表示實務上不需要此最佳化，因為任何固定插值都能給出無偏差的模型。

## 關聯

- [條件流匹配](conditional-flow-matching.md)是此框架中的一個插值，即高斯最優傳輸路徑。
- [修正流](rectified-flow.md)使用線性插值 \(t\,x_1 + (1-t)\,x_0\)。
- [DDPM](../../diffusion/ddpm.md) 與[擴散模型](../../diffusion/index.md)頁涵蓋此框架的擴散面向。

## 開放問題

- 對於特定資料類型，哪一種插值能給出最佳的取樣效率。
- 考慮到 SDE 係數在端點為奇異，SDE 與 ODE 取樣器在品質與速度上如何比較。

## 參考文獻

### 開創性論文

- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 提出插值框架、回歸目標 \(G(\hat v)\)，以及本頁所述的表格式與影像實驗。
- Albergo, M. S., Boffi, N. M. & Vanden-Eijnden, E. (2023). *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*. arXiv. https://arxiv.org/abs/2303.08797 — 加入雜訊項 \(\gamma(t) z\)、前向與後向 SDE，以及本頁所述的二次漂移與分數目標。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 條件流匹配目標，是插值框架的一個特例。

### 擴散背景

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). *Score-Based Generative Modeling through Stochastic Differential Equations*. ICLR. https://arxiv.org/abs/2011.13456 — 擴散模型的 SDE 觀點，隨機插值的 SDE 是它的推廣。
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*. ICML. https://arxiv.org/abs/1503.03585 — 插值框架所推廣的早期擴散模型。
