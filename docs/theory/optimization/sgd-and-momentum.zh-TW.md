---
translation_reviewed: 2026-10-28
---

# SGD 與動量

隨機梯度下降（SGD）及其動量變體是深度學習中最簡單的最佳化器。它們對每個參數使用同一個學習率，只依賴梯度。許多視覺模型仍以它們為預設，也是比較自適應方法時的基準。[概述](index.md)說明它們在各個家族中的位置。

## 概述

梯度下降沿著訓練損失梯度的反方向移動參數，\(\theta \leftarrow \theta - \eta\, \nabla L(\theta)\)。在整個資料集上計算梯度代價太高，因此實務訓練會使用小批次 \(B\)，梯度為 \(g_t = \nabla_\theta \frac{1}{|B|}\sum_{i\in B} \ell_i(\theta)\)。每一步很便宜，方向有雜訊，但平均而言指向正確的方向。

## 核心概念

- **小批次**：在某一步用來估計梯度的隨機資料子集。
- **學習率 \(\eta\)**：步長。太大會使損失發散，太小則訓練緩慢。
- **動量**：過去梯度的移動平均，能平滑方向，並加速沿著一致斜率的前進。
- **Nesterov 動量**：在前瞻點計算梯度的變體。
- **學習率排程**：在訓練過程中改變 \(\eta\) 的規則，詳見[學習率排程](learning-rate-schedules.md)。

## 運作方式

### 普通 SGD

對於凸且 \(L\)-平滑的損失，取 \(\eta = 1/L\) 的梯度下降在 \(T\) 步後以 \(O(1/T)\) 的速率降低損失；若損失是強凸的，則為線性速率。隨機梯度是完整梯度的無偏估計，因此期望更新是正確的，但會增加變異。若步長遞減，Robbins–Monro 條件 \(\sum_t \eta_t = \infty\) 與 \(\sum_t \eta_t^2 < \infty\) 保證收斂。

雜訊不只是代價。它能幫助最佳化器離開鞍點，且常被認為與收斂到較平坦的極小值有關，這個連結仍有爭議。

### 重球動量

Polyak 的重球方法保留一個速度：

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + g_t \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

重複出現的方向會累積，反覆翻轉的方向則會互相抵消。這能抑制損失曲面狹窄山谷中的震盪，而普通梯度下降在那裡會來回折返。

### Nesterov 動量

Nesterov 的變體在前瞻點 \(\theta_{t-1} - \eta\beta v_{t-1}\) 計算梯度，而不是在 \(\theta_{t-1}\)。這會在套用速度前先修正它，訓練卷積網路時使用 SGD 相當普遍。

## 實務注意事項

- 動量值 \(\beta = 0.9\) 附近是常見的預設。
- 批次大小與學習率會互相影響。較大的批次通常允許較大的學習率，但有上限。
- 使用 SGD 加動量在影像分類上通常泛化良好，但比自適應方法更需要仔細調校。

## 關聯

- [自適應方法](adaptive/index.md)對同一個更新的每個座標重新縮放。
- [深度學習](../deep-learning/index.md)說明產生 \(g_t\) 的反向傳播步驟。
- [NeuroAI](../../brain-mind/neuroai/index.md) 討論為何精確的梯度步驟難以對應到生物學習。

## 應用

- 以 SGD 與 Nesterov 動量訓練卷積網路與分類網路。
- 比較新方法時常用的基準最佳化器。

## 開放問題

- SGD 的雜訊為何傾向找到泛化良好的解？這種效應在不同架構中有多強？
- 批次非常大時，動量應如何調校？

## 參考文獻

### 開創性論文

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:10.1214/aoms/1177729586 — 提出使用遞減步長的隨機逼近，是 SGD 的基礎。
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:10.1016/0041-5553(64)90137-5 — 提出重球動量，並分析其在二次問題上的加速效果。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — 隨機梯度方法綜述，說明其在大型資料集上的收斂行為。
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, 第 8 章。MIT Press。https://www.deeplearningbook.org/ — 教科書對 SGD、動量與實務訓練的完整說明，可線上免費閱讀。

### 文章與文件

- Stanford CS231n, *Optimization* 講義。https://cs231n.github.io/optimization-1/ — 梯度下降、學習率與動量的清楚附圖筆記。
