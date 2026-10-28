---
translation_reviewed: 2026-10-28
---

# FitNets

FitNets 以提示訓練一個又薄又深的學生：提示就是教師的中間特徵。教師中的提示層，透過學習得到的回歸器，由學生中的引導層去匹配；學生分兩階段訓練，先學提示，再學輸出。它是[特徵式蒸餾](../index.zh-TW.md)的參考方法。

## 問題

只用輸出訓練一個又深又薄的學生很難，而大型教師的準確度也無法完全轉移給它。輸出匹配每個樣本只給一個目標，對深層網路的前幾層來說，這個訊號太弱。

## 核心想法

以教師的某一層作為提示，學生的某一層作為引導層。先訓練學生，使其引導層透過學習得到的回歸器預測提示，回歸器把學生的特徵映射到教師的大小。然後再以輸出訓練整個學生。

## 公式或演算法

提示損失為 \(\lVert f_T(x) - r(f_S(x)) \rVert^2\)，其中 \(f_T\) 與 \(f_S\) 分別是教師與學生在所選層的特徵，\(r\) 是學習得到的回歸器。第一階段之後，接著是 [Hinton 蒸餾](../../response-based/hinton-distillation/index.zh-TW.md)的標準輸出蒸餾損失。

## 結果

摘要報告，在 CIFAR-10 上，參數少了將近 10.4 倍的深層學生表現優於較大的教師網路。

## 限制

兩階段的排程增加了設計選擇，提示層的選擇也很重要。回歸器是額外的訓練機制，訓練後會被丟棄。

## 開放問題與相關變體

- **提示的選擇。** 對於沒有明顯對應關係的架構（例如深度不同的 Transformer），如何選擇提示層仍是開放問題。
- **相關：** [注意力轉移](../attention-transfer/index.zh-TW.md)匹配教師特徵較便宜的摘要。

## 相關連結

FitNets 是[自監督學習](../../../../../theory/paradigms/self-supervised/index.zh-TW.md)中逐層表徵學習的蒸餾對應。它所針對的又薄又深的學生，是[邊緣硬體](../../../../../engineering/hardware/index.zh-TW.md)上常見的形式。

## 參考文獻

### 開創性論文

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 以中間提示訓練又薄又深的學生，在 CIFAR-10 上參數約少 10.4 倍。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 第二階段所使用的輸出層級目標。
- Zagoruyko, S., Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 為相同目的而設計的較便宜特徵目標。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述特徵式知識與其他類型。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 在語言模型蒸餾中使用隱藏狀態對齊。
