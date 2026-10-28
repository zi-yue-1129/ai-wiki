---
translation_reviewed: 2026-10-28
---

# 梯度下降及其收斂

梯度下降法沿著可微分函數的梯度反方向反覆前進，以求得其極小值。它的保證來自微積分：泰勒界限說明一步之後函數最多能升高多少，而凸性則把很小的梯度與極小值的距離聯繫起來。它是[微積分與最佳化基礎](../index.md)一頁中的一階方法。

## 概述

給定損失 $f$ 與起點 $x_0$，此方法反覆計算 $x_{k+1}=x_k-\eta\nabla f(x_k)$，其中 $\eta$ 為步長，也就是學習率。[隨機梯度下降](../../../optimization/sgd-and-momentum/index.md)則以小批次估計的雜訊梯度取代精確梯度。

Polyak（1963）給出一個簡單的條件，在此條件下梯度方法線性收斂。Nesterov（2004）給出光滑凸函數的收斂速率，以及能改進這些速率的加速變體。Karimi、Nutini 與 Schmidt（2016）指出，Polyak 條件在沒有凸性的情況下仍可得到線性收斂。

## 核心概念

- **步長** $\eta$：步長太大會越過極小值；步長太小則進展緩慢。
- **$L$-光滑性**：梯度是 $L$-Lipschitz 的，即 $\lVert\nabla f(x)-\nabla f(y)\rVert\le L\lVert x-y\rVert$。
- **凸性**：$f(y)\ge f(x)+\nabla f(x)^\top(y-x)$ 對所有 $x, y$ 成立。任一點的切平面都位於函數圖形之下。
- **強凸性**，模數為 $\mu>0$，會在右側加上項 $\tfrac{\mu}{2}\lVert y-x\rVert^2$。比值 $\kappa=L/\mu$ 稱為條件數，衡量函數在不同方向上彎曲的不均勻程度。
- **Polyak–Łojasiewicz（PL）條件**：$\tfrac12\lVert\nabla f(x)\rVert^2\ge\mu\,(f(x)-f^*)$，其中 $f^*$ 為最小值。它不需要凸性。

## 運作方式

分析的基礎是[概述](../index.md)中的二次上界。對 $L$-光滑函數，

$$
f(y)\le f(x)+\nabla f(x)^\top(y-x)+\tfrac{L}{2}\lVert y-x\rVert^2 .
$$

令 $y=x-\eta\nabla f(x)$ 並取 $\eta=1/L$，此界限給出

$$
f(x_{k+1})\le f(x_k)-\frac{1}{2L}\lVert\nabla f(x_k)\rVert^2 .
$$

每一步使損失下降的量與梯度平方成正比。即使在簡單的二次函數上，步長超過 $2/L$ 也可能使損失增加，所以在已知 $L$ 時，$1/L$ 是安全的選擇。

**凸情形。** 凸性把差距 $f(x_k)-f^*$ 與梯度範數聯繫起來。結合上面的下降量，$T$ 步後的差距以常數乘上 $L\lVert x_0-x^*\rVert^2/T$ 為上界，速率為 $O(1/T)$。Nesterov 的加速方法對同一類函數將其改進為 $O(1/T^2)$。

**強凸情形。** 差距以幾何速率縮小，每步至多乘上 $1-1/\kappa$。

**PL 條件下。** 同樣的論證給出每步乘上 $1-\mu/L$ 的線性速率。Karimi 等人（2016）將此應用於最小平方法、羅吉斯迴歸與支援向量機等問題。

## 結果

證據是理論性的。上述界限已在所引用的專著中證明，不需要基準表；其實際適用範圍受到假設的限制：

- 對光滑凸損失，$O(1/T)$ 速率與幾何速率如 Nesterov（2004）與 Bubeck（2014）所述成立。
- Karimi 等人（2016）指出，強凸性蘊含 PL 條件，而 PL 條件已足以達成線性收斂；他們並將其應用於多種機器學習問題。
- 深度網路的損失既非凸的，也非全域光滑的。因此，這些保證描述的是較簡單的類別，無法直接保證網路的訓練結果。

## 限制

- **假設。** 這些保證需要 $L$，而它通常未知，或在參數空間中變化。Boyd 與 Vandenberghe（2004）介紹的回溯線搜尋可以在不知道 $L$ 的情況下選擇步長。
- **病態。** 大的 $\kappa$ 使普通梯度下降在狹窄的谷底之間來回震盪。[二階方法](../../../optimization/second-order.md)一頁所述的前處理可以處理這個問題。
- **鞍點。** 梯度下降可能在梯度很小的鞍點附近停滯。Dauphin 等人（2014）主張，這類點在高維度中佔優勢。
- **只使用一階資訊。** 此方法忽略曲率，而[牛頓法](../newton-method/index.md)正是利用曲率。
- **泛化。** 最小化訓練損失的速率，並不能說明測試表現。

## 開放問題

- **非凸訓練。** 為何固定步長的梯度下降在非凸的訓練損失上常常表現良好，而經典的步長上界 $1/L$ 事先並不知道，目前尚未被完全解釋。
- **PL 條件的適用範圍。** PL 條件或類似條件是否在深度網路訓練的軌跡上成立，仍是開放問題。
- **實務中的加速。** 加速方法在最壞情況下改進了凸問題的速率。這項優勢能否延續到深度網路的隨機訓練，仍有爭議。

## 參考文獻

### 開創性論文

- Polyak, B. T. (1963). Gradient methods for the minimisation of functionals. *USSR Computational Mathematics and Mathematical Physics*. https://doi.org/10.1016/0041-5553(63)90382-3 — 分析梯度方法，並給出線性收斂的簡單條件。
- Karimi, H., Nutini, J. & Schmidt, M. (2016). Linear Convergence of Gradient and Proximal-Gradient Methods Under the Polyak-Łojasiewicz Condition. arXiv. https://arxiv.org/abs/1608.04636 — 在 PL 不等式下證明線性收斂，且不需要凸性。
- Dauphin, Y. et al. (2014). Identifying and attacking the saddle point problem in high-dimensional non-convex optimization. arXiv. https://arxiv.org/abs/1406.2572 — 主張在高維度中，鞍點會拖慢訓練。

### 綜述與教科書

- Nesterov, Y. (2004). *Introductory Lectures on Convex Optimization*. Springer. https://doi.org/10.1007/978-1-4419-8853-9 — 光滑凸函數上梯度方法的分析，包括加速方法。
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://doi.org/10.1017/CBO9780511804441 — 搭配線搜尋的梯度下降，以及凸函數理論。
- Bubeck, S. (2014). Convex Optimization: Algorithms and Complexity. arXiv. https://arxiv.org/abs/1405.4980 — 凸問題複雜度的專著，包括梯度法與加速梯度法。
