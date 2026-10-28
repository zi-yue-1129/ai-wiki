---
translation_reviewed: 2026-10-28
---

# 收斂、損失地形與銳度

最佳化器表現如何，取決於兩個問題。第一，它多快能到達損失較低的點？第二，在許多低損失點中，它會到達哪一個？第一個問題由收斂理論回答，其結論依賴凸性與平滑性。第二個問題由損失地形的幾何回答，而它對泛化很重要。本子章同時討論這兩者，以及作用於第二個問題的銳度感知方法。

## 概述

本子章屬於[最佳化](index.md)資料夾。方法頁為[銳度感知最小化](sharpness-aware-minimisation.md)，至於平坦性與泛化的關係，見[尖銳極小值](sharp-minima.md)。

## 核心概念

- **凸性**：凸函數沒有虛假的局部極小值，因此每個局部極小值都是全域極小值。
- **平滑性**：梯度是 \(L\)-Lipschitz 的，它決定最大的安全步長 \(\eta \le 1/L\)。
- **駐點**：梯度為零的點。在非凸問題中，梯度方法會到達這些點，但並非所有駐點都是極小值。
- **鞍點**：曲率有正有負的駐點。在高維中，鞍點遠比局部極小值常見。
- **銳度**：參數離開極小值時，損失上升的速度。平坦極小值的銳度較低。

## 運作方式

對於凸且 \(L\)-平滑的損失，取步長 \(1/L\) 的梯度下降在 \(T\) 步後以 \(O(1/T)\) 的速率降低損失；若損失是強凸的，則為線性速率。隨機梯度會增加雜訊，為了收斂，步長必須遞減（Bottou 等人，2018）。這些結果不能直接套用於深度網路，因為其損失是非凸的。

對非凸損失而言，實務上的問題是最佳化器會到達哪些駐點。Dauphin 等人（2014）主張，高維中的主要困難來自鞍點的大量存在，鞍點周圍是高誤差的平原。他們提出的無鞍牛頓法利用曲率資訊來處理這個問題。

地形幾何也和泛化有關。Keskar 等人（2017）觀察到，大批次訓練傾向找到較尖銳的極小值，而平坦性與泛化之間的關係正是[尖銳極小值](sharp-minima.md)的核心。Dinh 等人（2017）顯示，透過重新參數化，可以在不改變網路所計算函數的情況下改變銳度，因此單靠銳度無法解釋泛化。

## 關鍵方法

| 主題 | 處理的問題 | 頁面 |
|---|---|---|
| 凸與平滑損失的收斂 | 損失下降的速率 | 本頁（Bottou 等人，2018） |
| 鞍點 | 逃離高誤差平原 | Dauphin 等人（2014） |
| 銳度感知最小化（Foret 等人，2021） | 朝向平坦鄰域訓練 | [SAM](sharpness-aware-minimisation.md) |
| 自適應銳度感知最小化（Kwon 等人，2021） | 依權重大小縮放的鄰域，對重新縮放具不變性 | [ASAM](asam.md) |
| 尖銳極小值與泛化 | 以平坦性預測泛化 | [尖銳極小值](sharp-minima.md) |

## 關聯

- [正則化與權重衰減](regularisation-and-weight-decay.md)會直接改變損失地形，它帶來的平坦性是正則化幫助泛化的一種方式。
- [大批次與分散式](large-batch-and-distributed.md)把批次大小與所找到極小值的銳度連結起來。
- [二階方法](second-order.md)使用曲率來處理鞍點與病態問題。

## 應用

- 依所得極小值的銳度，來選擇批次大小與學習率。
- 以 SAM 訓練影像分類器，已應用於 CIFAR 與 ImageNet 基準。

## 開放問題

- 平坦性是泛化的成因，還是取決於模型參數化方式的相關現象？
- 凸問題的哪些實務收斂保證能延伸到深度網路？

## 參考文獻

### 開創性論文

- Dauphin, Y., Pascanu, R., Gulcehre, C., Cho, K., Ganguli, S. & Bengio, Y.（2014）。*Identifying and attacking the saddle point problem in high-dimensional non-convex optimization*。arXiv。https://arxiv.org/abs/1406.2572 — 主張高維非凸最佳化的主要困難來自鞍點，而非局部極小值，並提出無鞍牛頓法。
- Keskar, N. S., 等人（2017）。*On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*。ICLR。https://arxiv.org/abs/1609.04836 — 報告大批次訓練找到較尖銳的極小值，而這些極小值的泛化較差。
- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B.（2021）。*Sharpness-Aware Minimization for Efficiently Improving Generalization*。arXiv。https://arxiv.org/abs/2010.01412 — 提出 SAM，在參數的鄰域上最小化損失，而不是只在單一點上。
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y.（2017）。*Sharp Minima Can Generalize For Deep Nets*。arXiv。https://arxiv.org/abs/1703.04933 — 顯示重新參數化可以改變極小值的銳度，而不改變函數或其泛化，因此銳度不是不變量。
- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T.（2018）。*Visualizing the Loss Landscape of Neural Nets*。NeurIPS。https://arxiv.org/abs/1712.09913 — 視覺化損失地形，說明網路設計如何改變其幾何。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 隨機梯度方法綜述，包含凸與非凸問題的收斂分析。
