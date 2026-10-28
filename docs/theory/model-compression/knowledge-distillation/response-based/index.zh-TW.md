---
translation_reviewed: 2026-10-28
---

# 以回應為基礎的蒸餾

以回應為基礎的蒸餾訓練學生去匹配教師的輸出分布，通常是每個樣本經溫度軟化的 logits。它是[知識蒸餾](../index.zh-TW.md)的原始形式，此家族中各方法的差異主要在於教師的輸出如何被使用：分類器的軟預測、語言模型的遮罩 token 預測，或序列中教師自己的答案。

## 概述

標準做法是在任務損失之外，加上教師與學生經軟化後分布之間的 KL 散度。教師是凍結的，因此其輸出可以預先算好。以回應為基礎的方法不需要存取教師的內部層，因此是最容易套用在只能透過輸出存取的模型上的蒸餾形式。

## 方法比較

| 方法 | 設定 | 超出軟輸出的額外訊號 | 頁面 |
| --- | --- | --- | --- |
| Hinton 蒸餾 | 分類 | 無；經溫度軟化的目標與真實標籤並用 | [Hinton 蒸餾](hinton-distillation/index.zh-TW.md) |
| DistilBERT | 語言模型預訓練 | 遮罩語言建模損失，以及隱藏狀態對齊損失 | [DistilBERT](distilbert/index.zh-TW.md) |
| 助教蒸餾（TAKD） | 任何情況，差距很大時 | 大小居中的教師助教，用來縮小差距 | [助教蒸餾](teacher-assistant/index.zh-TW.md) |

第一個方法是基準。第二個方法加入語言模型的目標與隱藏狀態對齊，使預訓練更便宜。第三個方法改變教師，使大差距更容易跨越。

## 取捨

- **簡單與訊號量。** 只匹配輸出很簡單，但每個樣本只有一個目標，轉移的資訊比以特徵為基礎的方法少。
- **溫度。** 溫度決定學生能看到多少教師的相對機率，最佳值取決於任務。
- **教師的存取。** 只需要輸出，適合透過介面提供的模型，但須遵守供應商的條款。

## 開放問題

- **差距大小。** 教師相對於學生應該多大，以及是否總是需要中間教師，目前尚無定論。
- **輸出多樣性。** 當教師的輸出幾乎是 one-hot 時，軟目標攜帶的資訊很少，最佳的補救方法仍有爭論。

## 相關連結

以回應為基礎的蒸餾是實務上最廣泛使用的形式，而[大型語言模型蒸餾](../llm-distillation/index.zh-TW.md)的方法也以同一目標為基礎。每個輸入都要執行教師的硬體成本，見 [AI 硬體](../../../../engineering/hardware/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 介紹以溫度軟化的輸出作為蒸餾目標。
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 以輸出匹配加上隱藏狀態對齊來蒸餾 BERT。
- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 加入中間的教師助教，以縮小大型教師與小型學生之間的差距。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 依知識類型綜述蒸餾，從輸出匹配開始。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 特徵層級的替代方法，在輸出匹配之外加入中間目標。
