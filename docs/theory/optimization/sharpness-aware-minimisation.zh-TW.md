---
translation_reviewed: 2026-10-28
---

# 銳度感知最小化（SAM）

SAM 讓模型朝向整個鄰域都具有低損失的參數訓練，而不只是最佳化器所在的那一點損失低。Foret 等人（2021）提出此方法，並在影像基準上報告泛化改善。上層概述見[收斂、損失地形與銳度](theory-and-landscapes.md)。

## 概述

SAM 是包在基礎最佳化器（如 SGD）外的一層包裝。它改變基礎最佳化器所用的梯度，代價是每一步多一次前向與反向傳播。

## 問題

兩組參數可以有相同的訓練損失，卻有很不同的銳度，也就是附近損失上升的速度。尖銳的極小值對權重的小擾動敏感，而訓練損失看不出這種差異。目標是找到在擾動下仍保持低損失的極小值，這預期能帶來較好的泛化。

## 核心想法

把訓練損失換成半徑為 \(\rho\) 的球內最壞的損失。這使訓練成為一個最小最大問題：找出在施加最壞的小擾動之後，損失仍然最小的參數。

## 演算法

SAM 目標為

\[
\min_w \max_{\|\varepsilon\|_2 \le \rho} L_S(w + \varepsilon),
\]

其中 \(L_S\) 是訓練損失。內層的最大化以 \(L_S\) 在 \(w\) 附近的一階泰勒展開來近似。對歐幾里得範數而言，近似的最壞擾動為

\[
\hat\varepsilon(w) = \rho\,\frac{\nabla_w L_S(w)}{\|\nabla_w L_S(w)\|_2}.
\]

也就是沿最陡上升方向、長度為 \(\rho\) 的一步。更新用的梯度則在擾動後的點上計算：

\[
g = \nabla_w L_B\big(w + \hat\varepsilon(w)\big).
\]

以 SGD 為基礎最佳化器時，更新式為 \(w_{t+1} = w_t - \eta\, g\)，其中 \(g\) 在小批次 \(B\) 上計算。因此每一步需要兩次梯度評估，一次在 \(w\)，一次在 \(w + \hat\varepsilon(w)\)。

論文建議預設值 \(\rho = 0.05\)，並在主要實驗中直接使用，未另外調校。

## 主要結果

摘要報告，SAM 在包括 CIFAR-10、CIFAR-100 與 ImageNet 在內的基準資料集上改善泛化，並在微調任務上取得數個設定下的最佳結果。摘要未給出準確率數字，因此本頁不引用任何數值。

## 限制

- 每一步需要兩次梯度評估，因此除非第二次評估能被降低成本，否則每步的訓練成本約為基礎最佳化器的兩倍。
- 半徑 \(\rho\) 是額外的超參數，其最佳值取決於模型與資料。
- 銳度並非不變量：Dinh 等人（2017）顯示，重新參數化可以在不改變函數的情況下改變銳度。因此 SAM 的效益既是對極小值的陳述，也取決於所選的參數化方式。

## 關聯

- [收斂、損失地形與銳度](theory-and-landscapes.md)是上層概述，SAM 與收斂理論及地形文獻並列於其中。
- [尖銳極小值](sharp-minima.md)提供 SAM 所要檢驗的平坦性與泛化假說。
- [SGD 雜訊尺度](sgd-noise-scale.md)說明了為何大批次傾向找到較尖銳的極小值。
- [正則化與權重衰減](regularisation-and-weight-decay.md)以懲罰項直接改變損失地形，而不是透過最壞情況的鄰域。

## 應用

- 在 CIFAR 與 ImageNet 上訓練影像分類器，論文報告泛化有改善。
- 微調預訓練模型，論文同樣報告改善。

## 開放問題

- 最壞情況的鄰域是否為正確的平坦性定義，還是它主要扮演梯度上的正則化？
- \(\rho\) 應如何隨模型大小或批次大小調整？能否在不搜尋的情況下設定？

## 參考文獻

### 開創性論文

- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B.（2021）。*Sharpness-Aware Minimization for Efficiently Improving Generalization*。arXiv。https://arxiv.org/abs/2010.01412 — 提出 SAM，以參數鄰域上的最小最大目標取代單點損失，並報告影像基準上的泛化改善。
- Keskar, N. S., 等人（2017）。*On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*。ICLR。https://arxiv.org/abs/1609.04836 — SAM 所設計來檢驗的尖銳極小值假說。
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y.（2017）。*Sharp Minima Can Generalize For Deep Nets*。arXiv。https://arxiv.org/abs/1703.04933 — 顯示銳度可以透過重新參數化改變而不改變函數，這限制了銳度度量能解釋的範圍。
- Dauphin, Y., 等人（2014）。*Identifying and attacking the saddle point problem in high-dimensional non-convex optimization*。arXiv。https://arxiv.org/abs/1406.2572 — 高維地形中平坦與尖銳區域的背景。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 隨機梯度方法綜述，SAM 所包裝的基礎最佳化器正屬於這一類。
