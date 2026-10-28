---
translation_reviewed: 2026-10-28
---

# 最佳化

訓練模型就是選擇參數，使損失函數變小。最佳化是執行這項搜尋的演算法集合。本 wiki 中幾乎每種方法，從線性迴歸到大型語言模型，最後都要靠最佳化器完成。

## 概述

把模型寫成 \(f_\theta\)，參數為 \(\theta\)，訓練損失是資料上的平均：\(L(\theta)=\frac{1}{N}\sum_i \ell(f_\theta(x_i), y_i)\)。學習就是尋找 \(\theta^\* = \arg\min_\theta L(\theta)\)。因為搜尋的對象是數百萬到數十億個數字，我們依賴指向「上坡」方向的梯度 \(\nabla_\theta L\)，並朝反方向移動。這套方法的效果取決於損失曲面的形狀：是否為凸函數、曲率多大，以及我們對梯度的估計有多雜訊。

這些搜尋所用的數學在[數學](../math/index.md)中，使用它的訓練流程在[深度學習](../deep-learning/index.md)中。損失與正則化的監督式學習觀點在[損失函數與最佳化](../paradigms/supervised/loss-functions-and-optimization/index.md)中。本資料夾討論最佳化器本身。

## 核心概念

- **梯度下降**：反覆更新 \(\theta \leftarrow \theta - \eta \nabla L(\theta)\)，其中 \(\eta\) 是學習率。
- **隨機梯度下降（SGD）**：用隨機抽出的小批次估計梯度，而不是用整個資料集。每一步便宜但有雜訊。
- **凸性**：凸函數沒有虛假的局部極小值，因此任何局部極小值都是全域極小值。神經網路的損失通常是非凸的。
- **平滑性**：梯度變化速度的上界 \(L\)。它決定最大的安全步長 \(\eta \le 1/L\)。
- **條件數**：當各方向的曲率差異很大時，普通梯度下降會來回震盪。依參數逐一縮放有助於改善。
- **損失地形**：\(L(\theta)\) 在高維空間中的曲面，包含鞍點、平坦區域，以及寬窄不一的極小值。

## 方法家族

下列最佳化器依其使用的資訊分組。每個子頁說明機制、變體與關鍵論文。

| 家族 | 使用的資訊 | 子頁 | 狀態 |
|---|---|---|---|
| 一階、SGD 家族 | 梯度與動量 | [SGD 與動量](sgd-and-momentum/index.md) | 草稿 |
| 自適應方法 | 由梯度平方得出的逐參數尺度 | [自適應方法](adaptive/index.md) | 草稿（Adam 與 AdamW 各有獨立頁） |
| 二階與擬牛頓 | 曲率（Hessian 或其近似） | [二階方法](second-order.md)，並有 [L-BFGS](lbfgs.md)、[K-FAC](kfac.md) 與 [Shampoo](shampoo.md) 等方法頁 | 草稿 |
| 學習率排程與預熱 | 學習率如何隨時間變化 | [學習率排程](learning-rate-schedules.md)，並有[漸進式預熱](gradual-warm-up.md)、[附暖重啟的餘弦退火](cosine-annealing-warm-restarts.md)與[循環學習率](cyclical-learning-rates.md)等方法頁 | 草稿 |
| 正則化與權重衰減 | 最佳化器必須遵守的懲罰項 | [正則化與權重衰減](regularisation-and-weight-decay.md)，並有[尖銳極小值](sharp-minima.md)與 [SGD 雜訊尺度](sgd-noise-scale.md) 等方法頁；解耦衰減見 [AdamW](adaptive/adamw.md) 頁 | 草稿 |
| 梯度裁剪與正規化 | 對梯度大小的限制 | [梯度裁剪與正規化](gradient-clipping-and-normalisation.md)，並有[範數裁剪](norm-clipping.md)、[LARS](lars.md) 與 [LAMB](lamb.md) 等方法頁 | 草稿 |
| 大批次與分散式 | 跨多個裝置的訓練 | [大批次與分散式](large-batch-and-distributed.md) | 草稿 |
| 零階與演化 | 完全不使用梯度 | [零階與演化](zeroth-order-and-evolutionary.md)，並有 [SPSA](spsa.md)、[演化策略](evolution-strategies.md) 與 [CMA-ES](cma-es.md) 等方法頁 | 草稿 |
| 理論 | 收斂、地形、銳度 | [理論與損失地形](theory-and-landscapes.md) | 規劃中 |

## 運作方式

對於凸且 \(L\)-平滑的損失，取 \(\eta = 1/L\) 的梯度下降在 \(T\) 步後以 \(O(1/T)\) 的速率降低損失；若損失是強凸的，則為線性速率。隨機梯度會增加雜訊，而步長的 Robbins–Monro 條件保證收斂。上述每個家族都改變了這幅圖景的一部分：方向（動量）、尺度（自適應方法）、使用的曲率（二階）、步長的排程，或假設的正則性。

## 關聯

- **數學：** 凸性、泰勒展開與 Hessian 解釋了方法為何有效。見[數學](../math/index.md)。
- **深度學習：** 反向傳播計算 \(\nabla L\)，而最佳化器決定如何使用它。見[深度學習](../deep-learning/index.md)。
- **正則化：** 權重衰減與提早停止作用在同一個目標上，可視為對最佳化的隱含改變。
- **大腦與心智：** 生物學習無法精確跟隨梯度，因為精確的反向傳播需要對稱的回饋權重，而生物電路並不明顯具有這種結構。尋找局部、合理的學習規則是 [NeuroAI](../../brain-mind/neuroai/index.md) 的主要主題。

## 開放問題

- 隨機與自適應方法為何能找到泛化良好的解，即使損失曲面有許多極小值？
- 學習率的預熱與排程，在極大批次下會如何互動？
- 二階資訊能否在數十億參數的模型規模上，以可接受的成本使用？
- 生物系統中，哪些局部學習規則近似這些最佳化器？

## 參考文獻

### 開創性論文

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:10.1214/aoms/1177729586 — 提出使用遞減步長的隨機逼近，是隨機梯度下降的基礎。
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:10.1016/0041-5553(64)90137-5 — 提出重球動量，並分析其在二次問題上的加速效果。
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — 提出 Adam，一種利用梯度偏差校正矩估計的自適應方法。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — 針對大型資料集的隨機梯度方法綜述，並包含收斂分析。
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 凸分析與演算法的標準教科書，作者提供免費 PDF。

### 講座與影片

- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T. (2018). Visualizing the Loss Landscape of Neural Nets. NeurIPS. https://arxiv.org/abs/1712.09913 — 損失曲面的視覺化方法，說明網路設計如何改變地形幾何。

### 文章與文件

- Stanford CS231n, *Optimization* 講義。https://cs231n.github.io/optimization-1/ — 針對初學者、內容清楚且附圖的梯度下降、學習率與動量筆記。
