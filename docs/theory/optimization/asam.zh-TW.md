---
translation_reviewed: 2026-10-28
---

# 自適應銳度感知最小化（ASAM）

ASAM 是 [SAM](sharpness-aware-minimisation.md) 的變體，其鄰域依每個權重的大小縮放。由於這種縮放，當網路的權重在不改變所計算函數的情況下被重新縮放時，它的銳度度量不會改變。Kwon 等人（2021）在 ICML 2021 提出此方法。

## 概述

與 SAM 相同，ASAM 包在基礎最佳化器之外，每一步需要兩次梯度評估。改變的是擾動可以到達的鄰域形狀，而不是外層的訓練迴圈。

## 問題

SAM 在權重空間中使用固定半徑 \(\rho\) 的球。許多網路的層（例如 ReLU 網路後接批次正規化）允許權重被重新縮放，而函數保持不變。在這種重新縮放下，固定半徑的銳度會改變，因此量測到的銳度可能無法很好地指示泛化。論文指出，SAM 適當的 \(\rho\) 取決於訓練軌跡上權重的尺度。

## 核心想法

以權重來定義鄰域：權重大的地方允許較大的擾動，權重小的地方則允許較小的擾動。如此，銳度就以尺度不變的方式量測，而訓練目標也遵循同一個鄰域。

## 演算法

ASAM 以正規化運算子 \(T_w\) 定義自適應銳度。論文採用的逐元素選擇為 \(T_w = \mathrm{diag}(|w_1|, \ldots, |w_k|)\)，自適應銳度為

\[
\max_{\|T_w^{-1}\varepsilon\|_p \le \rho} L_S(w + \varepsilon) - L_S(w),
\]

其中 \(1 \le p \le \infty\)。在 \(p = 2\) 時，其一階近似給出的擾動為

\[
\hat\varepsilon(w) = \rho\,\frac{T_w^2 \nabla_w L_S(w)}{\|T_w \nabla_w L_S(w)\|_2}.
\]

訓練步驟接著在擾動後的點上取梯度，\(g = \nabla_w L_B\big(w + \hat\varepsilon(w)\big)\)，與 SAM 完全相同。論文也為卷積層提供逐濾波器的 \(T_w\) 選擇：某個濾波器的對角元素使用該濾波器的 \(\ell_2\) 範數，其餘權重則使用絕對值。

## 主要結果

論文以最高測試準確率回報多次執行的平均值與標準差：

- **CIFAR-10，DenseNet-121**：SAM 92.00 ± 0.17；ASAM 93.33 ± 0.04（5 次執行）。
- **CIFAR-10，WideResNet-28-10**：SAM 96.98 ± 0.04；ASAM 97.28 ± 0.07（5 次執行）。
- **ImageNet，ResNet-50**，top-1 準確率：SAM 76.39 ± 0.03；ASAM 76.63 ± 0.18（3 次執行）。

論文指出 ASAM「整體上優於 SGD 與 SAM」。這些表中相對 SAM 的進步很小，多半只有零點幾個百分點。

## 限制

- 在論文自己的表中，相對 SAM 的進步很小。在 ImageNet 上，差異落在執行結果的幾個標準差之內。
- \(T_w\) 的選擇是設計決定。逐元素與逐濾波器兩種版本定義了不同的鄰域，論文並未宣稱其中任一種為最佳。
- 論文指出，ASAM 適當的 \(\rho\) 不像 SAM 那樣依權重尺度而定，但並未給出共通的預設值。因此 SAM 與 ASAM 的 \(\rho\) 數值不能直接比較。
- 論文沒有明確給出 ASAM 每步的計算成本。由於其更新與 SAM 具有相同的兩次梯度結構，依此推論成本與 SAM 相同，再加上套用 \(T_w\) 的成本。

## 關聯

- [SAM](sharpness-aware-minimisation.md)是 ASAM 所修改的固定半徑方法，請先閱讀。
- [收斂、損失地形與銳度](theory-and-landscapes.md)是上層概述，將這兩種方法置於地形研究的結果之中。
- [尖銳極小值](sharp-minima.md)是尺度不變性論證所精煉的平坦性假說。
- [自適應方法](adaptive/index.md)同樣以與權重相關的量來縮放更新，不過 Adam 等方法使用的是梯度統計量，而非權重本身。

## 應用

- 在 CIFAR-10 與 ImageNet 上訓練卷積影像分類器，即論文回報的基準。

## 開放問題

- 尺度不變性能否解釋泛化的增益，還是增益來自有效鄰域大小的改變？
- 對於論文未測試的架構，應如何選擇 \(T_w\)？

## 參考文獻

### 開創性論文

- Kwon, J., Kim, J., Park, H. & Choi, I. K.（2021）。*ASAM: Adaptive Sharpness-Aware Minimization for Scale-Invariant Learning of Deep Neural Networks*。ICML 2021，PMLR 139。https://arxiv.org/abs/2102.11600 — 定義尺度不變的自適應銳度與 ASAM 目標，並在 CIFAR-10 與 ImageNet 上回報相對 SAM 的小幅增益。查核：arXiv metadata 與論文中的 PMLR 139 標頭。
- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B.（2021）。*Sharpness-Aware Minimization for Efficiently Improving Generalization*。ICLR 2021。https://arxiv.org/abs/2010.01412 — ASAM 所修改的固定半徑方法。查核：ICLR 2021 海報頁 https://iclr.cc/virtual/2021/poster/2782 列出相同標題。
- Keskar, N. S., 等人（2017）。*On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*。ICLR 2017。https://arxiv.org/abs/1609.04836 — 自適應度量所要檢驗的尖銳極小值假說。查核：ICLR 2017 條目 https://mlanthology.org/iclr/2017/keskar2017iclr-large 列出相同標題。
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y.（2017）。*Sharp Minima Can Generalize For Deep Nets*。ICML 2017，PMLR 70。https://proceedings.mlr.press/v70/dinh17b.html — 顯示重新參數化會改變銳度而不改變函數，這正是 ASAM 所處理的問題。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — SAM 與 ASAM 所包裝的隨機梯度方法綜述。
