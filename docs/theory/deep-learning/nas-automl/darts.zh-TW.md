---
translation_reviewed: 2026-10-28
---

# DARTS：可微分架構搜尋（Liu 等人，2019）

DARTS 把一個單元（cell）中運算的離散選擇放寬為加權和，使架構權重能與網路權重一起以梯度下降最佳化。搜尋結束後，保留最強的選擇，把架構離散化。本頁是[神經架構搜尋](index.md)的一部分。

## 概述

早期的 NAS 方法在離散選擇上搜尋，並需要控制器或演化迴圈來提出每個候選。Liu、Simonyan 與 Yang（2019）發現，運算之間的選擇可以是軟性的。單元中的每條邊都帶有候選運算的加權混合，混合權重則在驗證集上學習。

## 關鍵概念

- **單元**：由節點與帶有運算之邊組成的小型有向無環圖。完整網路會堆疊多份搜尋得到的單元。
- **混合運算**：一條邊上所有候選運算的加權和。
- **架構權重** \(\alpha\)：設定混合權重的對數值，以驗證損失的梯度下降學習。
- **網路權重** \(w\)：運算的一般參數，以訓練損失學習。
- **離散化**：最後一步，把每個混合運算替換為其最強的選擇。

## 問題

如何以梯度下降搜尋單元中的運算選擇，而不必訓練每個離散候選？又應如何把軟性選擇轉回固定的架構？

## 運作方式

在每條邊 \((i,j)\) 上，混合運算為

\[
\bar o^{(i,j)}(x) = \sum_{o\in\mathcal O} \frac{\exp\bigl(\alpha_o^{(i,j)}\bigr)}{\sum_{o'\in\mathcal O}\exp\bigl(\alpha_{o'}^{(i,j)}\bigr)}\, o(x),
\]

其中 \(\mathcal O\) 為候選運算的集合。搜尋是一個雙層問題：在使訓練損失最小的網路權重之下，架構權重使驗證損失最小，

\[
\min_{\alpha} \; \mathcal L_{\text{val}}\bigl(w^\ast(\alpha), \alpha\bigr) \quad \text{s.t.} \quad w^\ast(\alpha) = \arg\min_w \mathcal L_{\text{train}}(w, \alpha).
\]

內層問題以一步梯度近似，\(w' = w - \xi \nabla_w \mathcal L_{\text{train}}(w,\alpha)\)，由此得到對 \(\alpha\) 的一階或二階更新。搜尋結束後，每條邊保留 \(\alpha\) 最大的運算，每個節點保留兩條最強的入邊。

## 主要方法

本頁只涵蓋一種方法：在放寬後的單元上進行雙層梯度搜尋，最後再離散化。

1. 建立超網路：堆疊單元，其中每條邊都是混合運算。
2. 在網路權重（訓練切分）與架構權重（驗證切分）之間交替進行梯度步驟。
3. 把學到的 \(\alpha\) 離散化為固定的單元，保留最強的運算與邊。
4. 從頭訓練離散架構，並在保留資料上評估。

## 變體

- **一階 DARTS** 令 \(\xi = 0\)，去掉二階導數，因此較便宜。
- **二階 DARTS** 保留展開的一步，較準確，但需要更多記憶體與運算。
- **以單元為基礎的搜尋** 只搜尋一個單元並堆疊之；論文中在 CIFAR-10 找到的單元可遷移到 ImageNet。

## 結果與限制

- Liu 等人（2019）報告，此方法在 CIFAR-10 與 ImageNet 上找到高效能的卷積單元，並在語言建模基準上找到循環單元，且比非可微分方法快好幾個數量級。
- 超網路同時把所有候選運算放在記憶體中，限制了能放進單一裝置的搜尋空間大小。
- 搜尋可能朝向無參數運算（如跳接）崩潰，而這些運算在搜尋早期看起來表現良好。Zela 等人（2020）分析了這種崩潰，並提出可以防止它的正則化。
- 雙層梯度是一種近似，其品質取決於兩層的學習率，以及超網路對候選的排序能力（Yu 等人，2020）。

## 應用

- **為固定運算預算設計影像分類單元**，作為強化學習搜尋的較便宜替代方案。
- **序列模型的單元**，以相同的放寬方式在語言建模上搜尋。
- **後續搜尋方法的基準**。

## 開放問題

- 如何在不依賴人工調校正則化的情況下，防止向跳接的崩潰？
- 搜尋時使用的超網路排序，能否預測完整訓練後離散架構的準確率？

## 與其他頁面的連結

- 上層主題：[神經架構搜尋](index.md)
- 本主題的另一方法：[高效神經架構搜尋（ENAS）](efficient-neural-architecture-search.md)，同樣在候選之間共享權重，但以控制器取樣
- 相關的最佳化想法：[超參數最佳化](../../optimization/hyperparameter-optimisation/index.md)，調整固定架構的外部設定

## 參考文獻

### 奠基性論文

- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — 提出單元搜尋空間的連續放寬與雙層梯度搜尋。
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — 顯示候選之間的權重共享使搜尋便宜許多。
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — DARTS 以梯度下降取代的強化學習搜尋。

### 綜述與教科書

- Zela, A. et al. (2020). Understanding and Robustifying Differentiable Architecture Search. In *ICLR 2020*. arXiv:1909.09656. https://arxiv.org/abs/1909.09656 — 解釋可微分搜尋為何朝向跳接崩潰，以及如何加以正則化。
- Yu, K. et al. (2020). Evaluating the Search Phase of Neural Architecture Search. In *ICLR 2020*. arXiv:1902.08142. https://arxiv.org/abs/1902.08142 — 檢驗權重共享方法的搜尋階段對架構的排序能力。
- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — 把 DARTS 歸入搜尋策略之中的綜述。
