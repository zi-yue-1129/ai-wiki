---
translation_reviewed: 2026-10-28
---

# 注意力轉移

注意力轉移訓練學生去匹配教師的注意力圖，也就是摘要卷積網路在空間上反應位置的圖，而不是完整的特徵張量。Zagoruyko 與 Komodakis 表明，這個較便宜的目標能讓較小的 CNN 從較強的教師獲得準確度。它是[特徵式](../index.zh-TW.md)方法，以資訊換取較簡單的目標。

## 問題

匹配完整激活值會迫使學生複製它可能沒有能力表示的特徵。需要一個較便宜、仍能承載教師結構的目標。

## 核心想法

匹配教師的注意力圖。注意力圖是激活值的空間摘要，因此學生學到的是在哪裡反應，而不需要複製每個通道。

## 公式或演算法

注意力圖在每個空間位置上，由沿通道加總的激活值平方計算而得。學生被訓練使其注意力圖接近教師的，並在一般損失之外加上一個懲罰項。比較前會先正規化。

## 結果

作者主張，較小的學生 CNN 透過模仿較強教師的注意力圖而獲得準確度。數字見論文的表格。

## 限制

注意力圖只存在於架構具有空間結構的地方，因此此方法是為卷積網路開發的。摘要會丟棄完整特徵匹配所保留的通道資訊。

## 開放問題與相關變體

- **Transformer。** 注意力圖對 Transformer 而言是自然的目標，但在那裡轉移的效果如何，仍需研究。
- **相關：** [FitNets](../fitnets/index.zh-TW.md)匹配完整特徵，承載的資訊較多，成本也較高。

## 相關連結

注意力圖是網路在看哪裡的空間摘要，這使此方法與[Transformer](../../../../../theory/models/transformer/index.zh-TW.md)中的注意力機制相連。對反應位置的關注，在[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)中也有對應的研究。

## 參考文獻

### 開創性論文

- Zagoruyko, S., Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 匹配教師與學生之間的空間注意力圖，以改善較小的 CNN。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 完整特徵提示，是此方法所簡化的替代方案。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 注意力轉移所加入的輸出損失。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述特徵式知識，包括注意力類型的目標。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 另一種中間目標，匹配成對相似度，供比較。
