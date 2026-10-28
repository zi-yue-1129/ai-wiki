---
translation_reviewed: 2026-10-28
aliases:
  - Attention transfer
  - Attention maps distillation
  - 注意力轉移
---

# 注意力轉移

注意力轉移訓練學生卷積網路去匹配教師的空間注意力圖。注意力圖摘要網路在哪裡反應，而不是匹配完整的特徵張量。Zagoruyko 與 Komodakis（2016）表明，這個較便宜的目標能在多個資料集與架構上改善學生 CNN。它是[特徵式](../index.zh-TW.md)方法，以部分資訊換取較簡單的目標。

## 問題

匹配完整激活值會迫使學生複製教師特徵的每個通道，包括學生可能沒有能力表示的特徵。需要一個較便宜、仍能承載教師結構的目標。

## 核心想法

匹配教師的注意力圖。注意力圖是某一層激活值的空間摘要，因此學生學到的是在哪裡反應，而不需要複製每個通道。論文定義兩種圖：以激活值計算的激活式圖，以及以輸出對激活值的梯度計算的梯度式圖。論文回報，激活式的形式效果較好，勝過匹配完整激活值。

## 方程式或演算法

對於具有 $C$ 個通道、激活張量為 $A$ 的層，激活式映射是把絕對激活值以冪次 $p > 1$ 沿通道加總，每個樣本得到一張空間圖：

$$
F^{p}_{\text{sum}}(A) = \sum_{i=1}^{C} |A_i|^{p}
$$

學生的損失在一般任務損失之外加上一個懲罰項。對每一對被匹配的層 $j$，學生與教師的圖先展平並做 $\ell_2$ 正規化，再進行比較：

$$
\mathcal{L}_{AT} = \mathcal{L}(W_S, x) + \frac{\beta}{2} \sum_{j \in \mathcal{I}} \left\| \frac{Q_S^{j}}{\lVert Q_S^{j} \rVert_2} - \frac{Q_T^{j}}{\lVert Q_T^{j} \rVert_2} \right\|_p
$$

其中 $Q^j$ 是第 $j$ 層的向量化注意力圖，$\mathcal{I}$ 是被匹配的層集合，$\beta$ 是懲罰的權重，$p$ 是範數類型，論文設為 2。正規化使比較不受圖的整體尺度影響。

## 結果

論文回報，在多個資料集與 CNN 架構上都有一致的改善，包括有殘差與無殘差的網路，以及不同種類的分類任務。論文也回報，激活式轉移比匹配完整激活值改善更多，而且注意力懲罰可以與標準蒸餾損失合併使用。數值表格見論文。

## 限制

- 注意力圖只存在於架構具有空間結構的地方，因此此方法是為卷積網路開發的。
- 摘要會丟棄完整特徵匹配所保留的通道資訊。
- 懲罰權重 $\beta$ 與被匹配的層的選擇，是學生表現所依賴的額外設定。

## 關鍵方法

- [FitNets](../fitnets/index.zh-TW.md)透過學得的回歸器匹配完整的中間特徵。它承載的資訊比注意力轉移多，成本也較高。
- [Hinton 蒸餾](../../response-based/hinton-distillation/index.zh-TW.md)是注意力轉移加入其懲罰項的輸出層級目標。

## 開放問題與相關變體

- **Transformer。** 注意力圖對 Transformer 而言是自然的目標，但在那裡轉移的效果如何，仍需研究。
- **其他中間目標。** 保留相似度的蒸餾（Tung 與 Mori，2019）匹配另一種中間摘要，在相同任務上與注意力圖比較，仍是開放問題。

## 相關連結

注意力圖是網路在看哪裡的空間摘要，這使此方法與[Transformer](../../../../../theory/models/transformer/index.zh-TW.md)中的注意力機制相連。對反應位置的關注，在[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)中也有對應的研究，不過此方法是工程手段，並未對神經機制作任何主張。

## 參考文獻

### 開創性論文

- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 匹配教師與學生之間基於激活值的空間注意力圖，以改善較小的 CNN。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 完整特徵提示，是注意力轉移所簡化的替代方案。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 注意力轉移所加入的輸出損失。
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 提出另一種中間目標，供與注意力圖比較。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾，包括特徵式目標。
