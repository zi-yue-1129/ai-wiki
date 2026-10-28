---
translation_reviewed: 2026-10-28
---

# 條件流匹配

條件流匹配（CFM）是 Lipman 等人（2022）以*流匹配*之名提出的迴歸目標。它把速度場擬合到條件機率路徑的已知速度上，以訓練連續正規化流，因此訓練時從不需要模擬這條流。它是[流匹配與整流流](../index.md)主題的基礎方法。

## 概述

連續正規化流以 ODE 定義生成模型：一個速度場把樣本從簡單的基底分布移動到資料分布。以最大概似訓練這類模型，每一步都需要 ODE 的解及其梯度，成本高昂。Lipman 等人（2022）提出以*固定條件路徑*上的迴歸來訓練速度場。每條路徑針對一個資料點定義，因此其速度有封閉形式。作者證明，對這些條件速度做迴歸，與對無法計算的邊際速度做迴歸，訓練出的是同一個模型。

此框架適用於任何高斯條件路徑族，而擴散路徑正是其中之一。論文特別指出，最佳傳輸位移路徑是一種有效率的選擇，並在 [OT-CFM](../ot-cfm/index.md) 中進一步發展。

## 核心概念

- **條件機率路徑** \(p_t(x \mid x_1)\)：一個分布，在 \(t=0\) 時是基底分布，在 \(t=1\) 時收斂到資料點 \(x_1\) 附近的窄分布。
- **條件速度** \(u_t(x \mid x_1)\)：生成該條件路徑的速度場。
- **邊際速度**：在給定目前位置時，對各資料點的條件速度取平均。它生成邊際路徑，但實務上無法計算。
- **高斯路徑**：每個時間的分布都是高斯的路徑，其平均數與標準差分別由排程 \(\mu_t\) 與 \(\sigma_t\) 決定。
- **免模擬訓練**：從不執行 ODE 求解器的訓練。

## 運作方式

考慮平均數為 \(\mu_t(x_1) = t\,x_1\)、標準差為 \(\sigma_t = 1-(1-\sigma_{\min})\,t\) 的高斯條件路徑，其中 \(\sigma_{\min} > 0\) 為一個小常數。時間 \(t\) 的樣本為 \(x = \mu_t(x_1) + \sigma_t\,x_0\)，其中 \(x_0 \sim \mathcal{N}(0, I)\)。生成這條路徑的流，其條件速度為

\[
u_t(x \mid x_1) = \frac{x_1 - (1-\sigma_{\min})\,x}{1-(1-\sigma_{\min})\,t}
\]

接著訓練依下列步驟進行：

1. 抽取一個資料點 \(x_1\)、一個時間 \(t \sim \mathcal{U}[0,1]\) 與雜訊 \(x_0 \sim \mathcal{N}(0, I)\)。
2. 形成路徑上的點 \(x = t\,x_1 + \sigma_t\,x_0\)。
3. 對 \(\|v_\theta(x, t) - u_t(x \mid x_1)\|^2\) 做一步梯度下降。

論文證明，這個條件損失的梯度與邊際損失的梯度只差一個常數。因此，即使迴歸目標是條件式的，訓練出的網路仍近似邊際速度場。

取樣時從 \(x(0) \sim \mathcal{N}(0, I)\) 開始，以任一 ODE 求解器積分 \(\frac{dx}{dt} = v_\theta(x, t)\) 到 \(t=1\)。每個求解器步驟需要一次網路求值。同一個 ODE 也能透過變數變換公式給出精確的概似值。

## 結果

論文在 ImageNet 上訓練模型，並與以擴散為基礎的方法比較。根據其摘要：

- 在 ImageNet 上訓練的流匹配，在概似與樣本品質兩方面，都持續優於其他以擴散為基礎的方法。
- 在流匹配中採用擴散路徑，是訓練擴散模型的一種更穩健、更穩定的替代方案。
- 最佳傳輸位移路徑比擴散路徑更有效率，訓練與取樣更快，並且泛化更好。

摘要未報告具體數值，因此這裡不引用數字。數值請見論文的表格。

## 限制

- 摘要所報告的是 ImageNet 實驗。它並未證明在其他資料類型上的表現，作者把這點視為此框架所開啟的方向，而不是已得出的結果。
- 高斯路徑的選擇是一項設計決定。無論採用哪條路徑，迴歸本身都是精確的，但哪條路徑最好仍是經驗問題。
- 路徑彎曲時，取樣仍需數個 ODE 步驟。要減少步數，需要更直的路徑，這正是[整流流](../rectified-flow/index.md)的動機。
- 透過 ODE 計算精確概似，需要積分散度項，會增加成本。

## 開放問題

- 哪一族條件路徑在大規模下品質最好？答案是否取決於資料類型？
- 排程 \(\mu_t\) 與 \(\sigma_t\)（包括 \(\sigma_{\min}\)）應如何選擇？
- 目標與取樣器如何與引導以及蒸餾到較少步數互動？

## 參考文獻

### 開創性論文

- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — 論文本身：條件迴歸目標、高斯路徑，以及此處所述的 ImageNet 實驗。
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. NeurIPS. https://arxiv.org/abs/1806.07366 — 定義透過 ODE 求解器訓練的連續深度網路，是流匹配所避開的高成本訓練設定的模型類別。
- Grathwohl, W. et al. (2018). *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*. arXiv. https://arxiv.org/abs/1810.01367 — 以最大概似訓練的連續正規化流，訓練時需要求解 ODE。
- Song, Y. et al. (2020). *Score-Based Generative Modeling through Stochastic Differential Equations*. arXiv. https://arxiv.org/abs/2011.13456 — 展示擴散模型的機率流 ODE，它與擴散模型具有相同的邊際密度，是流模型所依據的確定性觀點。

### 綜述與教科書

- Lipman, Y. et al. (2024). *Flow Matching Guide and Code*. arXiv. https://arxiv.org/abs/2412.06264 — 對流匹配的數學、設計選擇與延伸做了自成體系的回顧，並附有範例。
- Holderrieth, P. & Erives, E. (2025). *An Introduction to Flow Matching and Diffusion Models*. arXiv. https://arxiv.org/abs/2506.02070 — 一篇教學文章，從第一原理推導條件流匹配目標。
