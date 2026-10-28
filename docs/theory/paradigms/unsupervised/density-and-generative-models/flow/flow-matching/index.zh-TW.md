---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/transformer
tags:
  - 流匹配
  - 生成模型
  - 連續正規化流
aliases:
  - 流匹配
  - Flow matching
  - 條件流匹配
---

# 流匹配（Flow Matching）

流匹配透過把速度場回歸到沿著雜訊到資料路徑的已知速度，來訓練連續時間的生成模型。與早期的連續正規化流不同，它在訓練時不需要模擬 ODE，因此能擴展到大型影像。抽樣時則對 ODE 從雜訊積分到資料。包含離散正規化流在內的家族總覽見[流模型](../index.md)頁，擴散的對應方法見[擴散模型](../../diffusion/index.md)頁。

## 概覽

Lipman 等人（2023）提出流匹配來訓練連續正規化流。關鍵觀察是：速度場可以透過回歸每個資料點的條件路徑速度來學習，之後便能恢復邊際速度場。作者指出，擴散模型使用的擴散路徑也是此類路徑的一個家族，因此流匹配推廣了擴散的訓練方式。他們也強調最優傳輸路徑，在其實驗中它給出較直的軌跡與較快的抽樣。

後續工作保留相同的回歸想法，但改變三者之一：雜訊與資料之間的插值、雜訊與資料點的配對方式，或拉直軌跡的方式。

## 關鍵概念

- **機率路徑** \(p_t\)：一族分布，在 \(t=0\) 時為簡單的雜訊分布，在 \(t=1\) 時為資料分布。
- **條件路徑** \(p_t(x\mid x_1)\)：從雜訊出發、終點為單一資料點 \(x_1\) 的路徑。
- **速度場** \(v_\theta(x,t)\)：定義 ODE \(\mathrm{d}x/\mathrm{d}t = v_\theta(x,t)\) 的網路。
- **最優傳輸路徑**：內插為雜訊與資料之間直線的條件路徑，速度形式簡單。

## 運作方式

取雜訊樣本 \(x_0\sim\mathcal N(0,I)\) 與資料點 \(x_1\)。使用論文採用的最優傳輸路徑，路徑上時間 \(t\) 的點為 \(x_t = (1-t)\,x_0 + t\,x_1\)，其速度為 \(u_t = x_1 - x_0\)。訓練最小化

\[
\mathcal L_{\text{CFM}}(\theta) = \mathbb E_{t,\,x_0,\,x_1}\big\lVert v_\theta(x_t, t) - (x_1 - x_0)\big\rVert^2
\]

由於條件速度有閉合形式，這個回歸不需要解 ODE。最小化的解即為產生資料分布的邊際速度場。抽樣時從雜訊抽出 \(x_0\)，並以標準數值解法從 \(t=0\) 積分到 \(t=1\)。

## 關鍵方法

- [條件流匹配（Lipman 等人，2023）](conditional-flow-matching.md)：以高斯最優傳輸路徑為基礎的回歸目標，是基礎方法，並把擴散路徑涵蓋為特例。
- [修正流（Liu 等人，2022）](rectified-flow.md)：回歸到直線內插，並以修正程序拉直軌跡，供少步數抽樣使用。
- [隨機插值（Albergo 與 Vanden-Eijnden，2023）](stochastic-interpolants.md)：統一流與擴散的通用插值框架，插值的選擇保持開放。
- [小批次最優傳輸流匹配（Tong 等人，2024）](minibatch-ot-flow-matching.md)：依每個小批次上計算的最優傳輸計畫來配對雜訊與資料點。

## 關聯

- 流匹配與擴散共享連續時間的觀點，擴散路徑是其特例，見 [DDPM](../../diffusion/ddpm.md) 與 [DDIM](../../diffusion/ddim.md)。
- 其去噪器通常是作用於潛在圖塊上的 Transformer，見 [DiT](../../../../../models/transformer/dit/index.md)。
- ODE 抽樣器是數值積分問題，與[最佳化](../../../../../optimization/index.md)中的方法相關。

## 應用

以潛在流模型進行文字到影像與影片生成，以及分子構形等連續資料的生成；在這些情境中，速度場是自然的參數化方式。

## 開放問題

- 哪一種機率路徑能在樣本品質與 ODE 步數之間取得最佳的權衡。
- 實務上需要多少步驟，而蒸餾能把步數減少多少。
- 流匹配能否在非常大的模型上完全取代擴散訓練，以及兩者在條件生成上的比較。

## 參考文獻

### 開創性論文

- Lipman, Y., et al. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 提出條件流匹配，無需模擬即可訓練連續正規化流。
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — 學習沿較直路徑的速度場，使抽樣所需的步數更少。
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 以隨機內插橋接流與擴散，並給出速度的回歸目標。
- Tong, A., et al. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — 以小批次最優傳輸配對雜訊與資料，使條件流匹配的路徑更直。

### 綜述與教科書

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 連續與離散流的背景，對方法的似然面向有所助益。
