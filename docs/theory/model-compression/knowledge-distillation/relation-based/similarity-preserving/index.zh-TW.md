---
translation_reviewed: 2026-10-28
---

# 相似度保持知識蒸餾

相似度保持蒸餾訓練學生，使教師中產生相似激活值的樣本，在學生中也產生相似的激活值。它匹配的是一個批次上的成對相似度矩陣，而不是特徵本身。學生在自己的表示空間中保留教師的相似度，因此兩個網路不必共用特徵空間。它是比 [RKD](../rkd/index.zh-TW.md) 更簡單的[以關係為基礎](../index.zh-TW.md)方法。

## 問題

整個批次上的關係損失可能很昂貴，而且不清楚哪些關係最能轉移知識。

## 核心想法

語意相近的輸入在訓練好的網路中，傾向於引發相似的激活模式。以此作為目標：計算教師在一個批次上激活值的成對相似度，並訓練學生產生相同的相似度模式。

## 公式或演算法

對一個批次，教師與學生的相似度矩陣都由其激活值計算，每一對樣本都以正規化的內積計算。學生被訓練去匹配兩個矩陣，這項損失再加到一般的任務損失上。

## 結果

摘要以一個觀察為依據：語意相近的輸入在訓練好的網路中傾向引發相似的激活模式。實驗數字見論文。

## 限制

相似度矩陣的大小隨批次大小的平方增長，而且此方法是在分類任務上評估的。

## 開放問題與相關變體

- **批次大小。** 如何在大批次下維持相似度矩陣的成本低，是實務上的問題。
- **相關：** [RKD](../rkd/index.zh-TW.md)加入三元組的角度關係，承載的結構更多。

## 相關連結

成對相似度是度量學習的基礎，而「相似的輸入共用一種編碼」的想法，與[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)中的群體編碼相關。

## 參考文獻

### 開創性論文

- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 訓練學生在自己的激活值中保留教師的成對相似度。
- Park, W., Kim, D., Lu, Y., Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — 匹配距離與角度，是較豐富的關係集合。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 特徵層級的蒸餾，需要共用的特徵空間，是此方法的替代方案。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 依知識類型綜述蒸餾，包括關係知識。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 輸出層級的基準，相似度匹配是對它的補充。
