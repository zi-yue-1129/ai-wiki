---
translation_reviewed: 2026-10-28
---

# 自我蒸餾

自我蒸餾訓練一個網路從它自己的輸出或特徵學習，可以是從它的早期副本，也可以是從它自己較深的層。與[教師-學生蒸餾](../index.zh-TW.md)不同，不需要更大的模型。這一家族令人驚訝的結果是，學生往往比產生目標的模型更準確。

## 概述

在傳統蒸餾中，教師是獨立的模型，通常更大或訓練得更好。自我蒸餾不需要這個條件。一種常見設定是讓第 \(t\) 代在第 \(t-1\) 代的軟化預測上訓練，每一代的架構都相同。另一種設定則在一個網路的淺層加上輔助分類器，並以最深的分類器作為其他分類器的教師。兩者都使用與傳統蒸餾相同的損失，只是把教師換成網路本身。

## 關鍵概念

- **重生網路（born-again network）。** 與教師架構相同的學生，在教師的預測上訓練。
- **世代。** 一輪自我蒸餾。可以串接多個世代。
- **深層教師。** 一種變體，在同一次訓練中，網路最深的分類器監督較淺的分類器。
- **為何有幫助。** 軟目標起正則化作用，並降低最終模型的變異，但確切機制仍有爭議。

## 方法比較

| 方法 | 教師 | 訓練次數 | 頁面 |
| --- | --- | --- | --- |
| 重生網路 | 同架構的前一代 | 每一代一次完整訓練 | [重生網路](born-again-networks/index.zh-TW.md) |
| 做你自己的老師 | 同一網路最深的分類器 | 總共一次訓練 | [做你自己的老師](be-your-own-teacher/index.zh-TW.md) |

重生網路以額外的訓練次數換取乾淨的教師-學生設定，而且效果可以跨世代重複。做你自己的老師在單次訓練中達到相似的效果，代價是輔助分類器與訓練項。

## 取捨

- **成本與免教師設計。** 重生訓練需要重複執行。深層自我蒸餾只增加輔助頭，但改善較小。
- **評估。** 自我蒸餾的模型可能在基準上與教師相當，但在校準或穩健性上有所不同。

## 更多變體與開放問題

- **變體。** [特徵式蒸餾](../feature-based/index.zh-TW.md)，也可以用在同一網路的各層之間。
- **開放問題。** 為什麼網路從自己的副本學到的，比從標籤學到的更多。正則化的解釋合理，但尚未定論。
- **開放問題。** 重複的世代會持續改善，還是對大型模型會飽和。
- **相關。** [助教](../response-based/teacher-assistant/index.zh-TW.md)的想法用來跨越教師與學生之間的大差距，顯示教師的大小也很重要。

## 相關連結

自我蒸餾類似學習者複習並鞏固自己早先的理解。系統透過重新學習自己的預測而改進，也是[持續學習](../../../../theory/paradigms/continual/index.zh-TW.md)研究的題目，其中模型的早期狀態用來引導後續訓練。

## 參考文獻

### 開創性論文

- Furlanello, T., 等人 (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — 與教師架構相同的學生，表現優於其教師。
- Zhang, L., 等人 (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — 深層自我蒸餾，平均準確度比基準高 2.65%。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 自我蒸餾所重用的蒸餾損失，網路本身即為其教師。

### 綜述與教科書

- Gou, J., 等人 (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾，包括自我蒸餾的變體。
- Mirzadeh, S.-I., 等人 (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 顯示教師與學生的差距大時，學生的表現會下降。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

（本頁尚未查核任何項目）
