---
translation_reviewed: 2026-10-28
---

# 關係式知識蒸餾

關係式知識蒸餾（RKD）訓練學生重現教師表示在一個批次上的幾何：樣本對之間的距離，以及三元組之間的角度。學生不需要與教師共用座標，只需要共用結構。它是一種[以關係為基礎](../index.zh-TW.md)的方法，論文顯示它能改善學生模型，並在度量學習中讓學生有機會超越教師。

## 問題

匹配個別特徵迫使學生的表示與教師共用座標。若只在意結構，例如在檢索或分群中，這樣做並不必要。

## 核心想法

比較教師與學生中樣本之間的關係，而不是樣本本身。成對關係使用距離，高階關係使用三元組的角度，因此學生重現的是教師的幾何。

## 公式或演算法

距離損失比較教師與學生空間中，一個批次內樣本之間正規化後的成對距離。角度損失比較三元組形成的角度。兩者都加到一般的任務損失上，並以平均值正規化距離，使兩個空間的尺度差異不影響結果。

## 結果

摘要表示，此方法以顯著的幅度改善學生模型，並且在度量學習中學生可以超越教師。摘要沒有給出單一的主要數字。

## 限制

批次層級的計算增加成本，而關係的選擇會影響結果。結果取決於批次大小，因為關係是在每個批次內計算的。

## 開放問題與相關變體

- **使用哪些關係。** 對特定任務而言，最佳的關係組合事先並不知道。
- **相關：** [相似度保持蒸餾](../similarity-preserving/index.zh-TW.md)匹配較簡單的成對相似度矩陣。

## 相關連結

樣本之間的關係是度量學習的核心對象，也是[Transformer](../../../../../theory/models/transformer/index.zh-TW.md)嵌入幾何的核心。相似結構承載意義的想法，也在[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)中透過群體編碼的幾何來研究。

## 參考文獻

### 開創性論文

- Park, W., Kim, D., Lu, Y., Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — 匹配樣本之間的距離與角度，以顯著幅度改善學生模型。
- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 匹配激活值的成對相似度，是較簡單的關係損失。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 特徵層級的蒸餾，是關係匹配的對照。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 依知識類型綜述蒸餾，包括關係。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 輸出層級的蒸餾，是關係方法所延伸的基準。
