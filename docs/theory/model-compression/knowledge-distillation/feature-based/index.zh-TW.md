---
translation_reviewed: 2026-10-28
---

# 特徵式蒸餾

特徵式蒸餾訓練學生去匹配教師的中間表徵，而不只是輸出。學生因此學到教師如何計算特徵，在每個深度都有訓練訊號，而不是只在最後一層。它是[知識蒸餾](../index.zh-TW.md)的第二大家族，與匹配輸出分布的方法並列。

## 概述

以輸出為基礎的蒸餾，例如[以回應為基礎的蒸餾](../response-based/index.zh-TW.md)，每個樣本只給學生一個目標：教師軟化後的預測。然而，深層教師會建立有用的中間特徵，最後一層只承載它所知道的一部分。特徵式方法加入一個比較隱藏激活值的損失，通常會先經過一個學習得到的投影，把學生的特徵維度映射到教師的維度。當學生又薄又深時，這些中間提示正是讓訓練得以進行的關鍵。

## 關鍵概念

- **提示層。** 教師的某一層，其激活值作為學生所選層的目標。
- **回歸器。** 學習得到的投影，把學生特徵映射到教師的維度，使兩者可以比較。
- **注意力圖。** 網路反應位置的空間摘要，可以用來匹配，而不必匹配完整的激活值。
- **層的選擇。** 要匹配的教師與學生層是設計決定，最佳選擇取決於架構。

## 方法比較

| 方法 | 匹配的內容 | 設定 | 額外需求 | 頁面 |
| --- | --- | --- | --- | --- |
| FitNets | 經學習回歸器映射的完整隱藏激活值 | 又薄又深的卷積學生 | 兩階段訓練：先提示，再輸出 | [FitNets](fitnets/index.zh-TW.md) |
| 注意力轉移 | 沿通道加總的空間注意力圖 | 具空間結構的卷積網路 | 各層需有解析度相符的空間圖 | [注意力轉移](attention-transfer/index.zh-TW.md) |

FitNets 匹配特徵本身，轉移的資訊最多，但需要共同的特徵空間。注意力轉移匹配較便宜的摘要，放寬了匹配的限制，但只適用於架構具有空間結構的情況。

## 取捨

- **資訊與彈性。** 特徵匹配比輸出匹配轉移更多資訊，但它限制學生必須產生相容的特徵。
- **成本。** 教師必須對每個輸入執行，額外的損失也增加調參工作。
- **不匹配。** 當學生與教師的設計不同時，最佳的提示層可能沒有明確的對應。

## 更多變體與開放問題

- **變體。** [關係式蒸餾](../relation-based/index.zh-TW.md)，匹配樣本之間的關係，而不是個別特徵。
- **開放問題。** 對於沒有明顯對應關係的架構（例如深度不同的 Transformer），如何自動選擇提示層。
- **開放問題。** 匹配特徵是否轉移了教師的推理，還是只轉移了它的表徵。

## 相關連結

特徵匹配是[自監督學習](../../../../theory/paradigms/self-supervised/index.zh-TW.md)中表徵學習的蒸餾對應。學生從教師的內部狀態學習，而不是從它的答案學習，與學習者吸收老師的方法之間有類比，見[認知科學](../../../../brain-mind/cognitive-science/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Romero, A., 等人 (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 以教師的中間提示訓練又薄又深的學生，在 CIFAR-10 上參數約少 10.4 倍。
- Zagoruyko, S., Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — 匹配教師與學生之間的注意力圖，改善較小的 CNN。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 輸出層級的蒸餾，是特徵方法所延伸的基準。

### 綜述與教科書

- Gou, J., 等人 (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 依知識類型綜述蒸餾，包括特徵式知識。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Sanh, V., 等人 (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 以隱藏狀態對齊加上輸出匹配來蒸餾 BERT。
