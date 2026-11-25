---
translation_reviewed: 2026-11-25
---

# DPM-Solver：擴散取樣的快速 ODE 求解器

DPM-Solver（Lu 等人，2022）是一種免訓練的求解器，用來求解已訓練擴散模型所定義的常微分方程（ODE）。它使用慢速取樣器所用的同一個模型，約 10 至 20 次網路評估即可得到良好樣本。家族層級的概觀請見[擴散模型](index.md)頁面。它所推廣的取樣器是 [DDIM](ddim.md)，論文顯示 DDIM 是 DPM-Solver 的一階特例。

## 概述

擴散模型可以透過把 ODE 從雜訊積分到資料來取樣。這個 ODE 是確定性的，因此數值求解器可以走大步，取樣成本等於步數乘以每次網路評估的成本。一般的 ODE 求解器把整個右側視為黑箱。DPM-Solver 則利用擴散 ODE 的形式：解的一部分可以精確計算，只需要近似其餘部分，因此少數大步仍能保持準確。

## 問題

以標準數值求解器取樣擴散模型，通常需要數百到數千步才能達到高品質。Lu 等人（2022）提出的問題是：一個專為擴散 ODE 設計、且不需要重新訓練的求解器，能否在約 10 步內達到該品質。論文把這視為「快速且免訓練的擴散機率模型取樣」問題。

## 核心想法

擴散 ODE 的形式為 \( \frac{dx_t}{dt} = f(t)\,x_t + \frac{g^2(t)}{2\sigma_t}\,\epsilon_\theta(x_t, t) \)，其中 \(f\) 與 \(g\) 定義前向加噪過程，\(\epsilon_\theta\) 是噪聲預測網路。論文的關鍵步驟如下：

1. **改變時間變數。** 定義半對數信噪比 \( \lambda_t = \log(\alpha_t / \sigma_t) \)。此量隨 \(t\) 嚴格遞減，因此可以取代 \(t\) 作為積分變數。
2. **精確積分線性部分。** 因為 ODE 是半線性的，從時間 \(s\) 到時間 \(t\) 的解，是前一狀態的精確線性縮放，加上網路輸出的一個積分：

\[
x_t = \frac{\alpha_t}{\alpha_s}\,x_s - \alpha_t \int_{\lambda_s}^{\lambda_t} e^{-\lambda}\,\hat\epsilon_\theta(\hat x_\lambda, \lambda)\,d\lambda .
\]

3. **只近似積分。** 在每一步開始處，對網路輸出做關於 \(\lambda\) 的泰勒展開。保留 \(k\) 項即得到 \(k\) 階求解器，而每一項的積分都有封閉形式。論文把所得求解器命名為 DPM-Solver-1、-2 與 -3。

對於手工設計的時間表，論文在 \(\lambda\) 上而非 \(t\) 上均勻放置時間步。論文也提出自適應步長時間表，並同時報告兩者的結果。

## 演算法

令 \(h_i = \lambda_{t_i} - \lambda_{t_{i-1}}\)，一階更新（DPM-Solver-1）為

\[
\tilde x_{t_i} = \frac{\alpha_{t_i}}{\alpha_{t_{i-1}}}\,\tilde x_{t_{i-1}} - \sigma_{t_i}\left(e^{h_i} - 1\right)\epsilon_\theta(\tilde x_{t_{i-1}}, t_{i-1}).
\]

二階與三階求解器在每一步內部，於一或兩個中間時間評估網路，再把結果組合起來。論文提出的固定評估次數快速變體，會盡可能使用 DPM-Solver-3 步；若評估次數不能被三整除，則加入一步 DPM-Solver-1 或 DPM-Solver-2，以剛好用完預算。

一階更新與 DDIM 的一步相同。論文把 DDIM 的更新式改寫在 \(\lambda\) 變數下，得到完全相同的公式。因此 DPM-Solver 包含 DDIM 作為其最低階成員，並在其上加入更高階。

## 結果

摘要報告，在 CIFAR-10 上 10 次函數評估得到 4.70 FID，20 次得到 2.87 FID；在數個資料集上，相較於先前最好的免訓練取樣器，速度提升 4 至 16 倍。

論文中針對 CIFAR-10 離散時間模型（線性雜訊時間表）的比較表，給出 DPM-Solver 與 DDIM 在相同評估次數下的對照。表中的 ε 是取樣時使用的最小時間步，論文將其設為 10⁻³ 或 10⁻⁴：

| 取樣器（CIFAR-10，離散時間模型） | 10 次評估的 FID | 20 次評估的 FID |
|---|---|---|
| [DDIM](ddim.md) | 13.58 | 6.94 |
| DPM-Solver，第 1 型，ε = 10⁻³ | 6.37 | 4.28 |
| DPM-Solver，第 2 型，ε = 10⁻⁴ | 10.16 | 3.72 |

在 10 次評估時，此表中第 1 型明顯優於第 2 型；在 20 次評估時，則是第 2 型較好。論文指出，這一模式更一般地成立：評估次數少時，第 1 型搭配 ε = 10⁻³ 可能較好；評估次數多時，第 2 型搭配 ε = 10⁻⁴ 可能較好。

## 限制

- **為取樣而設計，而非為似然計算。** 論文指出，此求解器是為快速取樣而設計，「可能不適合加速擴散機率模型的似然評估」。
- **仍非即時。** 論文表示，搭配 DPM-Solver 的擴散模型仍不夠快，無法用於即時應用；相較之下，GAN 仍快得多。
- **設定很重要。** 最佳的時間下限與求解器階數，取決於評估次數，如上表所示。不存在對整個範圍都最好的單一設定。
- **實驗使用作者自己的模型。** 報告的結果使用預訓練模型與作者選定的資料集。要判斷這些增益能否延伸，還需要其他後續研究在不同模型上檢驗。

## 關聯

- DDIM 是 DPM-Solver 的一階成員。[DDIM](ddim.md) 頁面說明其取樣器與結果。
- 蒸餾是另一條少步取樣的路線，它透過訓練改變模型，而 DPM-Solver 只改變取樣器。請見[漸進式蒸餾](progressive-distillation.md)與[一致性模型與快速取樣器](consistency-models.md)。
- DPM-Solver 所積分的機率流 ODE，來自擴散的隨機微分方程觀點，由 Song 等人（2021）描述，並在 [Score SDE](score-sde.md) 頁面中摘要。

## 開放問題

- 當模型有強條件控制（例如無分類器引導）時，免訓練求解器能走多遠？
- 在 \(\lambda\) 上均勻取點，是否對每個模型都是最佳時間表，還是只是一個好的預設值？
- 在 10 次評估時，與多步取樣器仍有多少差距？這個差距是靠更好的求解器縮小，還是靠更好的模型縮小？

## 參考文獻

### 開創性論文

- Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C. 與 Zhu, J.（2022）。*DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps*。發表於 *NeurIPS 2022*。https://arxiv.org/abs/2206.00927 — 提出擴散 ODE 的精確半線性解，以及階數 1 至 3 的 DPM-Solver 系列，並給出 10 至 20 次評估的結果。
- Song, J., Meng, C. 與 Ermon, S.（2021）。*Denoising Diffusion Implicit Models*。發表於 *ICLR 2021*。https://arxiv.org/abs/2010.02502 — DPM-Solver-1 所重現的確定性、非馬可夫取樣器。
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. 與 Poole, B.（2021）。*Score-Based Generative Modeling through Stochastic Differential Equations*。發表於 *ICLR 2021*。https://arxiv.org/abs/2011.13456 — 定義 DPM-Solver 所積分的機率流 ODE。
- Ho, J., Jain, A. 與 Abbeel, P.（2020）。*Denoising Diffusion Probabilistic Models*。發表於 *NeurIPS 2020*。https://arxiv.org/abs/2006.11239 — DPM-Solver 取樣所用的已訓練模型與噪聲預測目標。

### 綜述與教科書

- Yang, L., Zhang, Z., Song, Y., Hong, S., Xu, R., Zhao, Y., Zhang, W., Cui, B. 與 Yang, M.-H.（2022）。*Diffusion Models: A Comprehensive Survey of Methods and Applications*。arXiv。https://arxiv.org/abs/2209.00796 — 擴散模型綜述，涵蓋快速取樣器與訓練方法。
