---
translation_reviewed: 2026-10-28
aliases:
  - EKFAC
  - 特徵值修正的 Kronecker 分解
---

# EKFAC

EKFAC（特徵值修正的 Kronecker 分解）保留 [K-FAC](index.zh-TW.md) 的克羅內克分解特徵基底，但在該基底中追蹤對角變異數，而不是使用各因子特徵值的乘積作為縮放。George 等人（2018）提出了此方法。他們主張，它是比 K-FAC 更好的費雪矩陣近似，而且一旦特徵基底可用，每次迭代的成本仍然很低。

## 問題

K-FAC 以克羅內克積 $A \otimes G$ 近似費雪矩陣。其預處理器在該乘積的特徵基底中重新縮放梯度，但它所用的縮放（各因子特徵值的乘積）不一定等於梯度沿每個特徵向量的真實二階矩。計算特徵基底也很昂貴，因此 K-FAC 必須低頻率地更新它，而基底可能落後於局部曲率。

## 核心想法

取兩個 K-FAC 因子 $A$、$B$ 的特徵向量 $U_A$、$U_B$，並以它們的克羅內克積 $U = U_A \otimes U_B$ 作為基底。在此基底中，追蹤每個旋轉後梯度座標的二階矩的滾動估計。預處理時，先把梯度旋轉到此基底，再把每個座標除以其追蹤值，最後旋轉回去。對角項可以每次迭代更新，而特徵基底只偶爾重新計算。

## 公式或演算法

設 $\nabla\theta$ 為梯度，$\epsilon$ 為阻尼常數，每一步為

1. 旋轉：$\tilde{g} = U^\top \nabla\theta$。
2. 重新縮放：$\tilde{g}_i \leftarrow \tilde{g}_i / (s_i + \epsilon)$，其中 $s_i$ 是 $\tilde{g}_i^{\,2}$ 的滾動平均。
3. 旋轉回去：$\Delta\theta = U\,\tilde{g}$。

論文的關鍵在第 2 步。縮放值是沿特徵向量本身量得的二階矩，而不是由因子特徵值推算出的縮放。

## 結果

在一個深度自編碼器任務，以及在 CIFAR-10 上訓練的卷積網路上，論文回報 EKFAC 隨著訓練週期進行，降低訓練損失的速度比 K-FAC 快。論文稱為 EKFAC-ra 的變體，在相同的實際時間內，降低訓練損失的速度也比 K-FAC 快。兩種方法的驗證表現相近。

## 限制

- 特徵基底的計算成本很高，因此在兩次更新之間，它可能落後於真實曲率。更新頻率是額外的超參數。
- 「更好的費雪近似」這項主張，是依據論文自身的標準。實證上的改善來自少數幾種架構。
- EKFAC 繼承了底層克羅內克近似的獨立性假設。

## 關鍵方法

- [K-FAC](index.zh-TW.md)是預處理器，EKFAC 重用其特徵基底。
- [KFC](kfc.zh-TW.md)把克羅內克分解擴展到卷積層，而論文的實驗包含卷積網路。
- [Adam](../adaptive/adam.zh-TW.md)在參數基底中追蹤對角二階矩。EKFAC 保留這個對角的想法，但把它套用在旋轉後的基底上。

## 開放問題與相關變體

- **更新排程。** 考慮到計算成本，應多久重新計算一次特徵基底，論文只研究了其中一部分。
- **其他基底。** 其他旋轉基底能否比克羅內克分解的特徵基底給出更好的對角近似，仍是開放問題。

## 相關連結

- [二階與擬牛頓方法](../second-order.zh-TW.md)是 K-FAC 家族所在的上層概述。
- [自適應方法](../adaptive/index.zh-TW.md)與本方法共享逐座標縮放的想法。

## 參考文獻

### 開創性論文

- George, T., Laurent, C., Bouthillier, X., Ballas, N. & Vincent, P. (2018). *Fast Approximate Natural Gradient Descent in a Kronecker-factored Eigenbasis*. arXiv:1806.03884. https://arxiv.org/abs/1806.03884 — 在克羅內克分解特徵基底中追蹤對角變異數，論文主張這是比 K-FAC 更好的費雪近似。
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. arXiv:1503.05671. https://arxiv.org/abs/1503.05671 — 提出 EKFAC 所使用之特徵基底的 K-FAC 因子。
- Grosse, R. & Martens, J. (2016). *A Kronecker-factored approximate Fisher matrix for convolution layers*. ICML, PMLR 48:573–582. https://proceedings.mlr.press/v48/grosse16.html — K-FAC 的卷積擴展，供卷積網路上的比較之用。
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — EKFAC 所近似的自然梯度方法。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — 大規模最佳化者的綜述，把自然梯度方法置於脈絡中。
