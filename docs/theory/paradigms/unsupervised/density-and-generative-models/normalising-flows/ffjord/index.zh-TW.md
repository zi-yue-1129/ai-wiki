---
translation_reviewed: 2026-10-28
---

# FFJORD

FFJORD（Grathwohl 等人，2018）是一種[正規化流](../index.md)，其變換是一個常微分方程（ODE）的解，而其動力學則是不受限制的神經網路。它的對數密度以 Hutchinson 跡估計器估計，因此從不需要計算完整的雅可比矩陣之跡。結果是一個具有無偏密度估計、且對網路結構沒有限制的連續模型。

## 概述

離散的流需要結構化的映射，才能讓雅可比行列式容易計算，耦合與自回歸的設計正是如此。連續流則可以避開這個限制。資料隨時間由一個 ODE 推進，而對數密度的變化由動力學雅可比矩陣之跡決定，跡比行列式更容易處理。Chen 等人（2018）以這種形式引入了連續正規化流（CNF），並以 ODE 求解器進行最大似然訓練。

精確計算跡的成本大約相當於對動力學做 \(D\) 次求值，在高維時相當昂貴。FFJORD 保留連續的形式，並以隨機估計器估計跡。

## 核心概念

- **連續正規化流**：由動力學 \(f\) 定義的映射 \(z(t_1) = z(t_0) + \int_{t_0}^{t_1} f(z(t), t)\,dt\)。因為 ODE 可以沿時間反向求解，這個映射是可逆的。
- **瞬時變數變換**：沿一條軌跡，對數密度的變化率等於動力學雅可比矩陣之跡的負值。
- **Hutchinson 跡估計器**：對於均值為零、共變異數為單位矩陣的隨機向量 \(\varepsilon\)，有 \(\operatorname{Tr}(A) = \mathbb{E}_\varepsilon[\varepsilon^\top A \varepsilon]\)。常用的選擇是高斯或 Rademacher 雜訊。
- **向量–雅可比乘積**：乘積 \(\varepsilon^\top \partial f / \partial z\)。反向模式自動微分計算它的成本，大約與計算 \(f\) 本身相當。

## 運作方式

令資料 \(x\) 為時間 \(t_0\) 的狀態，基底樣本為時間 \(t_1\) 的狀態。論文形式的瞬時變數變換公式給出

\[
\log p(x) = \log \mathcal{N}\big(z(t_1); 0, I\big) + \int_{t_0}^{t_1} \operatorname{Tr}\!\left(\frac{\partial f}{\partial z(t)}\right) dt
\]

跡被其無偏估計 \(\mathbb{E}_\varepsilon[\varepsilon^\top (\partial f / \partial z)\,\varepsilon]\) 取代。雜訊向量在每次 ODE 求解期間固定，使動力學在一次求解內保持確定性。

訓練步驟如下：

1. 為每次 ODE 求解抽取一個雜訊向量 \(\varepsilon\)。
2. 把狀態與累加的跡項，從資料積分到基底。跡項以 \(\varepsilon^\top (\partial f/\partial z)\varepsilon\) 的速率增長，由一次向量–雅可比乘積算得。
3. 計算基底樣本在標準常態下的對數密度加上累加項，並對小批次取平均。
4. 以伴隨方法（adjoint method）透過求解器做反向傳播，其記憶體用量不隨求解器步數增加，然後更新參數。

取樣時，抽取一個基底樣本，並沿時間反向積分同一組動力學至 \(t_0\)。

## 結果

論文評估了五個表格資料集，以及影像資料集 MNIST 與 CIFAR-10。對於影像，報告數值為每維位元數，越低越好：

| 模型 | MNIST | CIFAR-10 |
|---|---|---|
| RealNVP | 1.06 | 3.49 |
| Glow | 1.05 | 3.35 |
| FFJORD（多尺度） | 0.99 | 3.40 |
| FFJORD（單一流，使用卷積編碼器–解碼器） | 1.05 | — |

在 MNIST 上，單一的 FFJORD 流與 Glow 和 RealNVP 相當，後兩者需要組合許多流才能達到類似的效能。在 CIFAR-10 上，多尺度的 FFJORD 接近 Glow，而論文表示它所用的參數不到 Glow 的 2%。在表格資料上，FFJORD 是可逆模型中表現最好的，優勢很大，但自回歸模型表現更好；論文指出，FFJORD 在除一個資料集之外的所有資料集上都優於 MAF。

## 限制

- **速度。**每一次似然計算與取樣都需要求解 ODE，論文指出此方法比其他競爭方法慢。
- **估計器的變異。**論文指出，跡估計器的變異隨矩陣的 Frobenius 範數平方增長。
- **訓練時需要模擬。**最大似然訓練需要 ODE 求解器參與迴圈。Tong 等人（2023）指出，這種以模擬為基礎的訓練是限制連續流的瓶頸，也因此促成了免模擬的目標函數。

## 未解問題

- 能否在不模擬 ODE 的情況下訓練連續流，而密度品質又會付出什麼代價？[流匹配](../../flow-matching/index.md)與隨機插值（Albergo 與 Vanden-Eijnden，2022）已在生成任務上回答了這個問題，但在精確似然上的取捨仍在評估。
- 每次求解需要多少個雜訊樣本，才能得到穩定的似然？

## 參考文獻

### 開創性論文

- Grathwohl, W., Chen, R. T. Q., Bettencourt, J., Sutskever, I. & Duvenaud, D. (2018). *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*. arXiv. https://arxiv.org/abs/1810.01367 — 論文本身：無偏跡估計器、自由形式的動力學，以及本頁討論的密度結果。
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. NeurIPS. https://arxiv.org/abs/1806.07366 — 以 ODE 定義連續正規化流，並以伴隨方法進行最大似然訓練。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — 以迴歸已知的向量場來訓練連續正規化流，訓練時避免模擬。
- Tong, A. et al. (2023). *Improving and generalizing flow-based generative models with minibatch optimal transport*. arXiv. https://arxiv.org/abs/2302.00482 — 把條件流匹配推廣為連續正規化流，並討論以模擬為基礎的最大似然訓練之限制。
- Albergo, M. S. & Vanden-Eijnden, E. (2022). *Building Normalizing Flows with Stochastic Interpolants*. arXiv. https://arxiv.org/abs/2209.15571 — 以二次損失學習連續流，避免對 ODE 求解器做反向傳播。

### 綜述與教科書

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 綜述正規化流，包括連續時間的設計，以及密度計算與取樣之間的取捨。
