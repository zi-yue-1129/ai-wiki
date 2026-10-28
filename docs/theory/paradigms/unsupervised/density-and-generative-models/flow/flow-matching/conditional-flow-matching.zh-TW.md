---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md
---

# 條件流匹配（Conditional Flow Matching）

條件流匹配（CFM）是 Lipman 等人（2023）為連續正規化流提出的訓練目標。它把神經速度場回歸到一條簡單條件路徑的速度上，該路徑連接一個雜訊樣本與一個資料點，而且訓練時不需要模擬 ODE。家族總覽見[流匹配](index.md)頁，上層比較見[流模型](../index.md)頁。

## 概述

連續正規化流（Chen 等人，2018）透過 ODE 定義生成模型。以最大似然訓練它們時，每個梯度步驟都要解一次 ODE，成本很高。流匹配以單純的回歸來訓練速度場，避開了這個成本。論文指出，一個簡單的逐樣本目標，其梯度與一個難以計算的邊際目標的梯度相等，因此便宜的目標能訓練出同一個模型。論文也說明擴散路徑是其中一個特例，而最優傳輸路徑能給出較直的軌跡。

## 關鍵概念

- **條件路徑** \(p_t(x\mid x_1)\)：給定資料點 \(x_1\) 時，時間 \(t\) 的 \(x\) 之分布。在 \(t=0\) 時為雜訊，在 \(t=1\) 時集中於 \(x_1\)。
- **條件向量場** \(u_t(x\mid x_1)\)：產生條件路徑的速度。
- **邊際路徑與場**：條件路徑與場在 \(x_1\) 上的混合。邊際場在 \(t=1\) 時產生資料分布。
- **高斯條件路徑**：\(p_t(x\mid x_1) = \mathcal N\big(x \mid \mu_t(x_1), \sigma_t(x_1)^2 I\big)\)，均值與尺度函數由設計者選擇。

## 運作方式

流匹配損失 \(\mathcal L_{\text{FM}}(\theta) = \mathbb E_{t, x\sim p_t}\lVert v_\theta(t,x) - u_t(x)\rVert^2\) 使用邊際場 \(u_t(x)\)，而它是對所有資料點的積分，無法直接計算。Lipman 等人以條件損失取代

\[
\mathcal L_{\text{CFM}}(\theta) = \mathbb E_{t\sim\mathcal U[0,1],\; x_1\sim q(x_1),\; x\sim p_t(x\mid x_1)}\big\lVert v_\theta(t, x) - u_t(x\mid x_1)\big\rVert^2
\]

論文的定理 2 指出 \(\mathcal L_{\text{FM}}\) 與 \(\mathcal L_{\text{CFM}}\) 只相差一個與 \(\theta\) 無關的常數，因此梯度相同。最小化可計算的損失，就等於訓練同一個模型。抽樣時取 \(x_0\sim\mathcal N(0,I)\)，並以標準 ODE 解法從 \(t=0\) 積分 \(\mathrm{d}x/\mathrm{d}t = v_\theta(t,x)\) 到 \(t=1\)。

## 關鍵方法

### Flow Matching for Generative Modeling（Lipman 等人，2023）

- **問題：** 連續正規化流能給出精確似然，但每個訓練步驟都需要解 ODE。擴散模型訓練便宜，但受限於固定的隨機過程。
- **核心想法：** 把速度場回歸到所選機率路徑的條件速度上。逐樣本的目標對邊際場是無偏的，而且訓練時不需要模擬 ODE。
- **公式或演算法：** 論文的最優傳輸路徑（\(\sigma_{\min}\) 為小常數）其均值為 \(\mu_t(x_1)=t\,x_1\)、尺度為 \(\sigma_t = 1-(1-\sigma_{\min})t\)、流為 \(\psi_t(x)=(1-(1-\sigma_{\min})t)\,x + t\,x_1\)，條件場為 \(u_t(x\mid x_1) = \dfrac{x_1 - (1-\sigma_{\min})x}{1-(1-\sigma_{\min})t}\)。當 \(\sigma_{\min}\to 0\) 時，路徑是從雜訊到資料的等速直線。每一步訓練抽取 \(t\)、資料點 \(x_1\) 與雜訊點 \(x_0\sim\mathcal N(0,I)\)，形成 \(x_t=\psi_t(x_0)\)，並把 \(v_\theta(t, x_t)\) 回歸到 \(u_t(x_t\mid x_1)\)。當 \(\sigma_{\min}=0\) 時，目標即為 \(x_1 - x_0\)。
- **結果：** 論文表 1 報告無條件 ImageNet 的結果。在 32×32，最優傳輸路徑為 3.53 bits/dim、FID 5.02、122 次函數評估；擴散路徑為 3.54、FID 6.37、193 次。在 64×64，最優傳輸路徑為 3.31 bits/dim、FID 14.45；擴散路徑為 3.33、FID 16.88。在 128×128，論文只報告最優傳輸模型，為 2.90 bits/dim、FID 20.9。論文也指出，在 ImageNet 32×32 上，最優傳輸取樣器達到相同誤差門檻所需的函數評估約為擴散路徑的 60%。
- **限制：** 生成需要多次 ODE 評估（表 1 中為 122 到 193 次），因此取樣比單次網路前向傳遞慢。精確似然還需要再積分一次 ODE。論文以實證比較路徑，並未證明最優傳輸路徑在一般情況下最好。

## 關聯

- [修正流](rectified-flow.md)使用相同的直線目標，並以修正（reflow）程序讓軌跡更直。
- [小批次最優傳輸流匹配](minibatch-ot-flow-matching.md)保留此目標，但改變雜訊與資料點的配對方式。
- [隨機插值](stochastic-interpolants.md)把此目標中的內插選擇加以推廣。
- 擴散路徑是其特例，見 [DDPM](../../diffusion/ddpm.md)。
- 大型系統中的去噪器常為 Transformer，見 [DiT](../../../../../models/transformer/dit/index.md)。

## 開放問題

- 對於特定資料類型，哪一種條件路徑能在樣本品質與 ODE 步數之間取得最佳權衡。
- 回歸目標是否應使用比獨立抽樣更有資訊的雜訊與資料配對。

## 參考文獻

### 開創性論文

- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 提出條件流匹配與本頁使用的最優傳輸條件路徑。
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. arXiv. https://arxiv.org/abs/1806.07366 — 提出訓練時需要解 ODE 的連續深度模型，流匹配避開了這一步。
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — 回歸到相同的直線方向，並加入修正程序。
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 給出通用的內插框架與速度的回歸目標。
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. NeurIPS. https://arxiv.org/abs/2006.11239 — 擴散模型，其路徑為條件路徑家族的特例。

### 綜述與教科書

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 連續與離散流及其似然的背景。
