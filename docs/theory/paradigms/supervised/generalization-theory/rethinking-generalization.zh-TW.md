---
related:
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/evaluation-and-validation
  - theory/optimization
tags:
  - generalization
  - implicit regularisation
  - deep learning theory
aliases:
  - Rethinking generalization
  - Zhang et al. 2017
  - 重新思考泛化
translation_reviewed: 2026-11-01
---

# 理解深度學習需要重新思考泛化

Zhang 等人（2017）顯示，大型影像分類器能擬合完全隨機的標籤，而在標籤具有真實訊號時仍能泛化。這個結果打破了一種常見的泛化解釋，即複雜度量與顯式正則化能讓模型足夠簡單而得以泛化。論文是這個謎題的標準參考，家族層級的介紹見[泛化理論](index.md)頁面。

## 概述

經典學習理論把泛化與函數類別的複雜度連結起來。依此觀點，一個有足夠容量記住任意標籤的模型應該無法泛化。Zhang 等人在現代網路上檢驗這個觀點，發現容量確實存在，而常用的正則化器並不是讓網路能泛化的原因。

## 問題

作者問：既然經典理論與顯式正則化都無法清楚解釋，為什麼大型神經網路在實務上能很好地泛化？實驗把兩個問題分開：當標籤不含訊號時，網路能否擬合訓練資料？而當標籤是真實的時，顯式正則化對測試準確率有多少貢獻？

## 實驗

- **隨機標籤。** 在 CIFAR-10 與 ImageNet 上，以真實標籤與隨機標籤訓練網路。論文的摘要是：深度網路能輕易擬合隨機標籤。以隨機像素或高斯輸入時，CIFAR-10 的訓練誤差也能降到零。
- **正則化消融。** 關閉資料增強、權重衰減與 dropout，並測量它們對測試準確率的影響。也檢驗了提早停止與批次正規化。
- **有限樣本表示力。** 一個構造顯示，只要參數數量超過資料點數，雙層 ReLU 網路就能擬合 \(n\) 個點的任意標籤。

在 CIFAR-10（表 1）上，Inception 以真實標籤達到 100.0% 的訓練準確率，測試準確率為 85.75%。以隨機標籤，它同樣達到 100.0% 的訓練準確率，但測試準確率只有 9.78%，接近 10% 的機會水準。在 ImageNet（表 2）上，Inception v3 以隨機標籤達到 95.20% 的 top-1 訓練準確率，而 top-1 測試準確率只有 0.11%。

## 隱式正則化

論文的結論是，顯式正則化對控制泛化誤差既非必要，單獨也不充分。接著它尋找隱式正則化。對線性模型，作者指出，從零開始的隨機梯度下降會收斂到範數較小的解；在核實驗中，內插解等於最小範數解。作者補充，最小範數只是故事的一小部分，因為範數上升的同時測試誤差下降。

## 理論

定理 1 指出，一個具有 \(2n + d\) 個權重的雙層 ReLU 網路，能表示 \(d\) 維中 \(n\) 個點的樣本上的任意函數。推論 1 給出深度 \(k \ge 2\) 時寬度為 \(O(n/k)\) 的構造。作者把它與一個需要 \(O(dn)\) 參數的早期構造比較。這個結果是關於擬合樣本，而非泛化。

## 限制

- 作者表示，他們尚未找到一個精確的形式化度量，使這些大型模型在其下是簡單的。
- 對這些模型，Rademacher 複雜度的界接近一，而均勻穩定性忽略了標籤，因此經典界太弱，無法解釋結果。
- 隱式正則化無法解釋為什麼某些架構比其他架構泛化得更好。
- 隨機標籤的實驗沒有調整超參數，因此論文關於擬合的結論僅限於那些實驗。
- 提早停止的發現仍屬暫時性，要使其嚴謹，需要獨立的測試集。

## 關聯

- 論文引用的隨機梯度下降穩定性分析來自 [Hardt 等人（2015）](https://arxiv.org/abs/1509.01240)，它從穩定性的角度說明 SGD 為何能泛化。
- 試圖回應此謎題的範數型界，見[泛化理論](index.md)頁面，包括 [Bartlett 等人（2017）](https://arxiv.org/abs/1706.08498)。
- 最佳化的一面，包括 SGD 的角色，見[最佳化](../../../optimization/index.md)章節。

## 未解問題

- 哪一種模型與 SGD 的性質，能解釋隨機標籤擬合所無法解釋的泛化？
- 能否找到一種複雜度度量，使訓練後的網路在其下是簡單的？
- 哪些因素區分了泛化較好的架構與較差的架構？

## 參考文獻

### 奠基論文

- Zhang, C., Bengio, S., Hardt, M., Recht, B. & Vinyals, O.（2017）。Understanding Deep Learning Requires Rethinking Generalization. ICLR. [arXiv:1611.03530](https://arxiv.org/abs/1611.03530) — 本頁討論的隨機化實驗與表示力構造。
- Neyshabur, B., Tomioka, R. & Srebro, N.（2014）。In Search of the Real Inductive Bias: On the Role of Implicit Regularization in Deep Learning. [arXiv:1412.6614](https://arxiv.org/abs/1412.6614) — 研究隱式正則化，以及梯度方法所找到解的範數。
- Hardt, M., Recht, B. & Singer, Y.（2015）。Train faster, generalize better: Stability of stochastic gradient descent. [arXiv:1509.01240](https://arxiv.org/abs/1509.01240) — 對 SGD 的穩定性分析，給出已訓練模型的泛化界。
- Bartlett, P., Foster, D. J. & Telgarsky, M.（2017）。Spectrally-normalized margin bounds for neural networks. [arXiv:1706.08498](https://arxiv.org/abs/1706.08498) — 神經網路的範數型間隔界，是論文認為仍然過弱的複雜度度量之一。

### 綜述與教科書

- Ioffe, S. & Szegedy, C.（2015）。Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. [arXiv:1502.03167](https://arxiv.org/abs/1502.03167) — 論文測量其對泛化影響的批次正規化層。

### 講座與影片

（本頁未核對）

### 文章與文件

- Szegedy, C. 等人（2015）。Rethinking the Inception Architecture for Computer Vision. [arXiv:1512.00567](https://arxiv.org/abs/1512.00567) — ImageNet 實驗所用的 Inception v3 架構。
