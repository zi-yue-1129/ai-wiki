---
translation_reviewed: 2026-10-28
---

# 遮罩自回歸流

遮罩自回歸流（MAF）由 Papamakarios、Pavlakou 與 Murray（2017）提出，是一種由自回歸仿射變換構成的[正規化流](../index.md)。每個變數只使用前面的變數進行變換，因此資料點的密度可以在一次平行計算中算出，而取樣則必須一次生成一個變數。MAF 推廣了 [RealNVP](../realnvp/index.md)，並與逆自回歸流密切相關。

## 概述

自回歸模型把聯合密度分解為條件分布，\(p(x) = \prod_i p(x_i \mid x_{1:i-1})\)，並給出精確的似然。MADE 架構（Germain 等人，2015）以遮罩讓所有條件分布都可以在一次計算中得到，遮罩確保輸出 \(i\) 只依賴輸入 \(1, \ldots, i-1\)。然而，從 MADE 取樣仍需要 \(D\) 次依序計算。

MAF 注意到，自回歸模型也定義了一個從隨機數 \(u\) 到資料 \(x\) 的映射。每個資料變數是對應雜訊變數的仿射函數，其縮放與平移取決於前面的資料變數。這個映射是可逆的，而它的逆，也就是由 \(x\) 還原 \(u\)，只需要一次遮罩計算。MAF 用這個逆映射計算密度，並堆疊數個這樣的映射來構成一個流。

## 核心概念

- **自回歸條件分布**：\(x_i\) 的高斯分布，其平均 \(\mu_i\) 與對數尺度 \(\alpha_i\) 只依賴於 \(x_{1:i-1}\)。
- **隨機數觀點**：模型是獨立同分布高斯雜訊 \(u\) 的變換。從 \(u\) 到 \(x\) 的映射是生成方向，而它的逆給出密度。
- **遮罩（MADE）**：前饋網路權重上的二元遮罩，用來強制變數的排序。
- **排序**：自回歸模型對變數的順序敏感。MAF 可以在每一層使用不同的順序，從而避免只依賴單一排序。
- **逆自回歸流（IAF）**：以相同的建構模塊，但方向相反。Kingma 等人（2016）用它來加速取樣，代價是密度計算必須依序進行。

## 運作方式

每個條件分布都是高斯分布，其參數由前面的變數決定：

\[
p(x_i \mid x_{1:i-1}) = \mathcal{N}\big(x_i \mid \mu_i, (\exp\alpha_i)^2\big), \qquad \mu_i = f_{\mu_i}(x_{1:i-1}), \quad \alpha_i = f_{\alpha_i}(x_{1:i-1})
\]

取樣執行 \(x_i = u_i \exp\alpha_i + \mu_i\)，\(i = 1, \ldots, D\)，其中 \(u_i \sim \mathcal{N}(0,1)\)。每個 \(\mu_i\) 與 \(\alpha_i\) 都依賴於已經產生的值，因此遞迴是依序的。其逆映射為

\[
u_i = (x_i - \mu_i)\exp(-\alpha_i)
\]

所有 \(\mu_i\) 與 \(\alpha_i\) 都可以同時由資料算出。其雅可比矩陣是三角的，行列式為 \(\exp(-\sum_i \alpha_i)\)，因此

\[
\log p(x) = \log \mathcal{N}(u; 0, I) - \sum_{i=1}^{D} \alpha_i
\]

堆疊 \(K\) 個這樣的變換，每一層都會增加一項對數行列式。訓練時，每一層以一次遮罩計算得到一個小批次的 \(u\)，並最大化平均對數似然。取樣時抽取 \(u\) 並執行遞迴，論文指出這需要 \(D\) 次依序計算。

## 結果

論文在四個 UCI 資料集與 BSDS300 的 8 × 8 自然影像切片上進行無條件密度估計。分數是測試集上的平均對數似然，單位為奈特（nats），數值越高越好。兩個模型都是十層：

| 資料集 | RealNVP（10 層） | MAF（10 層） |
|---|---|---|
| POWER | 0.17 | 0.24 |
| GAS | 8.33 | 10.08 |
| HEPMASS | −18.71 | −17.73 |
| MINIBOONE | −13.84 | −12.24 |
| BSDS300 | 153.28 | 154.93 |

論文報告，MAF 在每個資料集上都優於 RealNVP。在 BSDS300 上，其最佳的單一模型是條件分布為高斯混合的 MAF，達到 156.36 奈特。

## 限制

- **取樣緩慢。**取樣需要 \(D\) 次依序計算。對於高維資料，這遠比密度計算慢。
- **高斯條件分布。**仿射變換假設條件分布為高斯。高斯混合的變體在 BSDS300 上得到最佳結果，顯示更豐富的條件分布確實有幫助。
- **排序。**固定的排序可能無法表示一個簡單的密度，論文的例子說明了這一點。在各層使用不同的順序可以減輕這個問題，但無法消除對排序的選擇。

## 未解問題

- 能否讓一個流同時具有快速的密度計算與快速的取樣？Parallel WaveNet（van den Oord 等人，2017）把依序的 WaveNet 蒸餾為前饋的逆自回歸流，是通往此目標的一條路。
- 學習得到的排序，或依資料結構選擇的排序，是否比論文所用的固定反轉更好？

## 參考文獻

### 開創性論文

- Papamakarios, G., Pavlakou, T. & Murray, I. (2017). *Masked Autoregressive Flow for Density Estimation*. NeurIPS. https://arxiv.org/abs/1705.07057 — 論文本身：自回歸仿射變換、平行的密度計算，以及本頁討論的基準結果。
- Germain, M., Gregor, K., Murray, I. & Larochelle, H. (2015). *MADE: Masked Autoencoder for Distribution Estimation*. ICML. https://arxiv.org/abs/1502.03509 — 在自編碼器中使用二元遮罩，使一次計算就能得到所有的自回歸條件分布。
- Kingma, D. P., Salimans, T., Jozefowicz, R., Chen, X., Sutskever, I. & Welling, M. (2016). *Improving Variational Inference with Inverse Autoregressive Flow*. NeurIPS. https://arxiv.org/abs/1606.04934 — 提出自回歸流的逆方向，可以平行取樣，並能擴展到高維的潛在空間。
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — 提出 MAF 所推廣的耦合流，也是 MAF 比較的基準。
- van den Oord, A. et al. (2017). *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*. arXiv. https://arxiv.org/abs/1711.10433 — 把依序的 WaveNet 蒸餾為前饋的逆自回歸流，生成速度快於實時。

### 綜述與教科書

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 綜述正規化流，包括自回歸設計，以及密度計算與取樣之間的取捨。
