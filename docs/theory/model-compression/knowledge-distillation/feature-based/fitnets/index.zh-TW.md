---
translation_reviewed: 2026-10-28
aliases:
  - FitNets
  - Hints for thin deep nets
  - 提示式蒸餾
---

# FitNets

FitNets 以提示訓練一個又薄又深的學生：提示就是教師的中間特徵。教師中的提示層，透過學習得到的回歸器，由學生中的引導層去匹配；學生分兩階段訓練，先學提示，再學輸出。它是[特徵式蒸餾](../index.zh-TW.md)的參考方法。

## 問題

只用輸出訓練一個又深又薄的學生很難，而大型教師的準確度也無法完全轉移給它。輸出匹配每個樣本只給一個目標，對深層網路的前幾層來說，這個訊號太弱。論文顯示，以提示訓練的又深又薄學生，可以在參數少得多的情況下，匹配或超過較大的教師網路。

## 核心想法

以教師的某一層作為提示，學生的某一層作為引導層。先訓練學生，使其引導層透過學習得到的回歸器預測提示，回歸器把學生的特徵映射到教師的大小。然後再以輸出訓練整個學生。回歸器只在第一階段使用，之後即丟棄。

## 方程式或演算法

提示損失為

$$
\mathcal{L}_{\text{HT}} = \tfrac{1}{2}\, \lVert f_T(x) - r(f_S(x)) \rVert^2
$$

其中 $f_T$ 與 $f_S$ 分別是教師與學生在所選層的特徵，$r$ 是學習得到的回歸器。第一階段對引導層以前的學生層與回歸器最小化此損失。第二階段則對整個學生套用 [Hinton 蒸餾](../../response-based/hinton-distillation/index.zh-TW.md)的標準輸出蒸餾目標。

為了讓回歸器的參數量保持較小，論文以卷積回歸器取代全連接回歸器，使其輸出與提示具有相同的空間大小。

## 結果

摘要報告，在 CIFAR-10 上，參數少了將近 10.4 倍的深層學生，表現優於較大、較深的教師網路。論文也在 MNIST、CIFAR-100、SVHN 與 AFLW 上評估，並回報此方法在這些基準上與標準蒸餾相當或更好。

## 限制

- 兩階段的排程增加了設計選擇，提示層的選擇也很重要。
- 回歸器是額外的訓練機制，第一階段之後即被丟棄。
- 所報告的增益來自卷積影像基準，以及固定的一族又薄又深的架構。

## 關鍵方法

- [注意力轉移](../attention-transfer/index.zh-TW.md)匹配教師激活值的空間摘要，比 FitNets 的完整特徵提示便宜，也不需要回歸器。
- [Hinton 蒸餾](../../response-based/hinton-distillation/index.zh-TW.md)是 FitNets 第二階段所用的輸出層級目標。

## 開放問題與相關變體

- **提示的選擇。** 對於沒有明顯對應關係的架構（例如深度不同的 Transformer），如何選擇提示層仍是開放問題。
- **回歸器設計。** 比卷積回歸器更簡單的映射，是否會丟失教師特徵的資訊，尚無定論。

## 相關連結

FitNets 是[自監督學習](../../../../../theory/paradigms/self-supervised/index.zh-TW.md)中逐層表徵學習的蒸餾對應。它所針對的又薄又深的學生，是[邊緣硬體](../../../../../engineering/hardware/index.zh-TW.md)上常見的形式。

## 參考文獻

### 開創性論文

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 以中間提示訓練又薄又深的學生，在 CIFAR-10 上參數約少 10.4 倍。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 第二階段所使用的輸出層級目標。
- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 為相同目的而設計的較便宜特徵目標。
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 提出另一種中間目標，供與提示比較。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述特徵式知識與其他類型。
