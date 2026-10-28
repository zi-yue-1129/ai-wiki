---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
- theory/paradigms/self-supervised
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - 特徵式蒸餾
  - Feature-based distillation
  - Hint-based distillation
---

# 特徵式蒸餾

特徵式蒸餾（feature-based distillation）訓練學生模型去匹配教師模型的中間表徵，而不只是輸出。學生因此學會教師如何計算特徵，在每一層都得到訓練訊號，而不是只在最後一層。它是[知識蒸餾](../index.zh-TW.md)的第二大類，與匹配輸出分布並列。

## 概觀

像[回應式蒸餾](../response-based/index.zh-TW.md)那樣，學生只能從輸出得到每個樣本的一個目標，也就是教師經過軟化的預測。然而，深層教師會建立許多有用的中間特徵，最後一層只承載其中一部分知識。特徵式方法因此加入一項損失，比較隱藏層的啟動值，通常要先經過一個可學習的投影（回歸器），把學生的特徵維度對到教師的維度。當學生又薄又深時，這些中間提示有時是訓練得以成功的關鍵。

## 關鍵概念

- **提示層（hint layer）。** 教師的某一層，其啟動值作為學生某一層的目標。
- **回歸器（regressor）。** 把學生特徵投影到教師維度的可學習映射，使兩者可以比較。
- **注意力圖（attention maps）。** 網路對空間位置反應強弱的摘要，可以用來取代完整啟動值進行匹配。
- **層的選擇。** 要匹配哪些教師層與學生層是設計決策，最佳選擇取決於架構。

## 主要方法

以下兩個代表性方法都監督中間層，差別在於複製特徵的程度。

- [FitNets（Romero 等人，2015）](fitnets/index.zh-TW.md)：在兩階段排程中，透過可學習的回歸器匹配教師某一層的完整隱藏啟動值。
- [注意力轉移（Zagoruyko 與 Komodakis，2016）](attention-transfer/index.zh-TW.md)：匹配空間注意力圖，這是啟動值較便宜的摘要；當解析度相符時不需要回歸器。

FitNets 轉移的特徵比較完整，但需要相容的特徵空間。注意力轉移放寬了這項限制，但只適用於具有空間結構的架構。

## 取捨

- **資訊量與彈性。** 特徵匹配比輸出匹配轉移更多資訊，但它限制學生必須產生相容的特徵。
- **成本。** 教師必須對每個輸入執行一次，額外的損失也增加需要調整的超參數。
- **不匹配。** 當學生與教師的設計不同時，最佳的提示層可能沒有明確的對應層。

## 更多變體與未解問題

- **變體：**[關係式蒸餾](../relation-based/index.zh-TW.md)，匹配樣本之間的關係，而不是單一特徵。
- **變體：**[自我蒸餾](../self-distillation/index.zh-TW.md)，提示來自同一網路的較深層。
- **未解問題：**對於沒有明顯對應關係的架構（例如深度不同的 Transformer），如何自動選擇提示層。
- **未解問題：**匹配特徵是否能轉移教師的推理過程，還是只轉移其表徵。

## 關聯

特徵匹配是[自監督學習](../../../../theory/paradigms/self-supervised/index.zh-TW.md)中表徵學習在蒸餾中的對應概念。學習者吸收的是教師的內部方法，而不只是答案，這與人如何從範例中學習有鬆散的類比；見[認知科學](../../../../brain-mind/cognitive-science/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Romero, A., Ballas, N., Ebrahimi Kahou, S., Chassang, A., Gatta, C. & Bengio, Y. (2015). *FitNets: Hints for Thin Deep Nets*. ICLR 2015. https://arxiv.org/abs/1412.6550 — 以提示層訓練又薄又深的學生；摘要報告一個參數約少 10.4 倍、卻勝過較大教師的學生。
- Zagoruyko, S. & Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 提出注意力轉移，讓學生匹配教師的注意力圖，摘要報告在多個資料集與 CNN 架構上都有提升。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 把整體模型（ensemble）壓縮成單一模型；是特徵式方法所延伸的輸出層基準。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — 廣泛回顧蒸餾方法，依轉移的知識種類分類，包括特徵式知識。預印本可免費閱讀：https://arxiv.org/abs/2006.05525。

### 講座與影片

（本頁未查核）

### 文章與文件

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 將 BERT 蒸餾為約小 40% 的模型，同時保留 97% 的語言理解能力；是語言模型蒸餾的標準參考。
