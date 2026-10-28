---
translation_reviewed: 2026-10-28
---

# SGD 與動量

隨機梯度下降（SGD）及其動量變體，是深度學習中最簡單、也最廣泛使用的最佳化器。它們對每個參數使用同一個學習率，且只依賴梯度。它們至今仍是常見的基準方法；Wilson 等人（2017）發現，在某些任務上，它們的泛化效果優於自適應方法。家族層級的位置見[最佳化總覽](../index.md)。

## 概述

梯度下降會沿著訓練損失的梯度反方向移動參數，即 \(\theta \leftarrow \theta - \eta\, \nabla L(\theta)\)。在整個資料集上計算梯度的成本很高，因此實際訓練會使用小批次 \(B\)，梯度為 \(g_t = \nabla_\theta \frac{1}{|B|}\sum_{i\in B} \ell_i(\theta)\)。每一步的計算成本低，方向帶有雜訊，但平均而言仍指向正確的方向。

![參數點沿二次損失曲線，經八次小批次梯度更新。](../../../assets/concept-animations/sgd-minibatch-updates.gif)

*原創動畫；AI Wiki，CC BY-SA 4.0。*

橘線連接相鄰的參數值，藍點在更新位置之間移動。這個一維例子的完整資料損失為 \(L(\theta)=\theta^2/2\)，每一步則使用小批次梯度 \(g_t=\theta_t+\epsilon_t\)，學習率固定為 0.35。預設的示意雜訊可使更新不同於完整梯度，但不能證明估計無偏或代表一般訓練表現。曲線上的移動呈現插值參數的損失，並非連續訓練軌跡。數值和時間均為示意，並非模型實測；循環時回到起點。

## 關鍵概念

- **小批次**：用來在某一步估計梯度的隨機資料子集。
- **學習率 \(\eta\)**：步長。太大會使損失發散，太小則使訓練緩慢。
- **動量**：過去梯度的滑動平均，使方向更平滑，並加速沿著一致斜坡的前進。
- **Nesterov 動量**：在前瞻點計算梯度的變體。
- **學習率排程**：在訓練過程中改變 \(\eta\) 的規則，見[學習率排程](../learning-rate-schedules.md)。

## 運作方式

### 純 SGD

對於強凸目標，搭配適當遞減步長的 SGD，在 \(k\) 步後以 \(O(1/k)\) 的速率收斂。在同一問題上，全批次梯度下降則線性收斂，因此隨機方法在每一步上較慢（Bottou、Curtis 與 Nocedal，2018）。隨機梯度是完整梯度的不偏估計，因此期望更新是正確的，但會增加變異。這類隨機逼近收斂的經典條件是 \(\sum_t \eta_t = \infty\) 與 \(\sum_t \eta_t^2 < \infty\)（Robbins 與 Monro，1951）。

雜訊不只是成本。在梯度步中加入雜訊，有助於最佳化器逃離鞍點（Ge 等人，2015）。Keskar 等人（2017）指出，大批次的泛化效果較差，且收斂到較尖銳的極小值，這顯示小批次的雜訊有助於泛化。平坦性是否能解釋泛化，目前仍有爭議。

### 重球動量

完整的方法與其分析，見[重球動量](heavy-ball.md)頁面。

Polyak（1964）提出了重球方法。在深度學習軟體中常見的形式中，它維護一個速度：

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + g_t \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

重複的方向會累積，符號來回翻轉的方向會相互抵消。這能抑制損失曲面狹窄谷地中的振盪，而純梯度下降在那裡會之字形前進。

### Nesterov 動量

完整的方法與其保證，見 [Nesterov 動量](nesterov.md)頁面。

Nesterov 的變體在前瞻點 \(\theta_{t-1} - \eta\beta v_{t-1}\) 計算梯度，而不是在 \(\theta_{t-1}\) 計算。它在套用速度之前先加以修正。Sutskever 等人（2013）研究了這兩種方法在深層網路訓練上的表現，並指出搭配動量排程的 Nesterov 形式訓練效果良好。

## 比較

| 方法 | 梯度計算位置 | 一行更新式 | 詳細內容 |
|---|---|---|---|
| 純 SGD | 目前的參數 | \(\theta \leftarrow \theta - \eta g\) | 本頁 |
| 重球法 | 目前的參數 | 累積速度，再前進 | [重球動量](heavy-ball.md) |
| Nesterov | 前瞻點 | 在前進前修正速度 | [Nesterov 動量](nesterov.md) |

## 實務注意事項

- 約 \(\beta = 0.9\) 的動量是常見的預設值。Goyal 等人（2017）以 SGD 訓練 ImageNet 模型時即使用此值。
- 批次大小與學習率會互相影響。Goyal 等人（2017）在其實驗中顯示，把學習率與批次大小成線性比例放大，在一定範圍內有效，且需搭配暖身階段。
- 在某些任務上，帶動量的 SGD 的泛化可能優於自適應方法，但自適應方法可能更快達到較低的訓練損失。Wilson 等人（2017）顯示，在簡單的過參數化問題上，兩類方法會找到不同的解。

## 關聯

- [自適應方法](../adaptive/index.md)會為同一個更新的每個座標重新縮放。
- [深度學習](../../deep-learning/index.md)說明產生 \(g_t\) 的反向傳播步驟。
- [NeuroAI](../../../brain-mind/neuroai/index.md)比較基於梯度的訓練與大腦中的學習。

## 應用

- 以 SGD 與動量訓練影像分類網路（Goyal 等人，2017）。
- 在比較新方法與 SGD 的研究中作為基準最佳化器（Wilson 等人，2017）。

## 未解問題

- 為什麼 SGD 的雜訊傾向於找到泛化良好的解？這個效應在不同架構間有多強？
- 批次大小非常大時，應如何調整動量？

## 參考文獻

### 開創性論文

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*, 22, 400–407。doi:[10.1214/aoms/1177729586](https://doi.org/10.1214/aoms/1177729586) — 提出遞減步長的隨機逼近，是 SGD 的基礎。
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*, 4, 1–17。doi:[10.1016/0041-5553(64)90137-5](https://doi.org/10.1016/0041-5553(64)90137-5) — 提出重球動量，並分析它在二次問題上的加速效果。
- Ge, R., Huang, F., Jin, C. & Yuan, Y. (2015). Escaping From Saddle Points: Online Stochastic Gradient for Tensor Decomposition. COLT。https://arxiv.org/abs/1503.02101 — 顯示在隨機梯度步中加入雜訊，能讓最佳化器逃離鞍點。
- Sutskever, I., Martens, J., Dahl, G. & Hinton, G. (2013). On the importance of initialization and momentum in deep learning. ICML。https://proceedings.mlr.press/v28/sutskever13.html — 研究動量與 Nesterov 方法在深層與循環網路訓練上的表現。
- Keskar, N. S., Mudigere, D., Nocedal, J., Smelyanskiy, M. & Tang, P. T. P. (2017). On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima. ICLR。https://arxiv.org/abs/1609.04836 — 指出大批次訓練的泛化較差，且收斂到較尖銳的極小值。
- Goyal, P. 等人（2017）。Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour. arXiv。https://arxiv.org/abs/1706.02677 — 以帶動量的 SGD、線性學習率縮放與暖身階段，進行大批次訓練。
- Wilson, A. C., Roelofs, R., Stern, M., Srebro, N. & Recht, B. (2017). The Marginal Value of Adaptive Gradient Methods in Machine Learning. NeurIPS。https://arxiv.org/abs/1705.08292 — 顯示在簡單的過參數化問題上，自適應方法找到的解，泛化可能比 SGD 差。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*。https://arxiv.org/abs/1606.04838 — 對隨機梯度方法及其在大型資料集上收斂行為的綜述。
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*，第 8 章。MIT Press。https://www.deeplearningbook.org/ — 教科書對 SGD、動量與實務訓練的完整說明，可免費線上閱讀。

### 文章與文件

- Stanford CS231n，*Optimization* 講義。https://cs231n.github.io/optimization-1/ — 關於梯度下降、學習率與動量的清晰圖解講義。
