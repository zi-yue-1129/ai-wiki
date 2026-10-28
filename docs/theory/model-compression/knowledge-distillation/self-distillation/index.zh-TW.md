---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - 自我蒸餾
  - 自蒸餾
  - Self-distillation
---

# 自我蒸餾

自我蒸餾（self-distillation）訓練網路從自己的輸出或特徵學習，學習對象可以是自己較早的副本，也可以是自己較深的層。與[師生式蒸餾](../index.zh-TW.md)不同，它不需要更大的模型。這個家族最值得注意的結果是：學生往往比產生目標的模型更準確。

## 概觀

在經典蒸餾中，教師是另一個較大或訓練較好的模型。自我蒸餾則省去這項要求。一種常見做法是：以相同架構，讓第 \(t\) 代在第 \(t-1\) 代經過軟化的預測上訓練。另一種做法是把一個網路分成數段，在同一次訓練中，把最深一段的知識傳給較淺的各段。兩者使用的損失與經典蒸餾相近，只是把教師換成網路本身。

## 關鍵概念

- **再生網路（born-again network）。** 與教師架構相同的學生，在教師的預測上訓練。
- **世代（generation）。** 一輪自我蒸餾。可以串接多個世代。
- **深層教師（deep-layer teacher）。** 在同一次訓練中，網路較深的部分監督較淺的部分。
- **為何有效。** 軟性目標可以作為正則化項。其機制仍有爭議，各篇論文提出不同的解釋。

## 主要方法

以下兩個代表性方法都讓網路擔任自己的教師，但所需的訓練次數不同。

- [再生網路（Furlanello 等人，2018）](born-again-networks/index.zh-TW.md)：依序訓練多個世代，每一代與教師架構相同，因此每個新學生都由前一個模型蒸餾而來。
- [自己當老師（Zhang 等人，2019）](be-your-own-teacher/index.zh-TW.md)：在單一網路內，把最深部分的知識蒸餾到較淺的部分，全部在一次訓練中完成。

再生網路以額外的訓練次數換取乾淨的師生結構，而且效果可能隨世代重複出現。自己當老師則在一次訓練內達到類似效果，代價是輔助分類器與額外的損失項。

## 取捨

- **成本與免教師設計。** 再生網路訓練需要重複多次。深層自我蒸餾在一次訓練中加入輔助分類頭，但回報的效果取決於架構。
- **評估。** 自我蒸餾的模型可能在準確率上與教師相當，但在校準或穩健性上有所不同，僅看準確率無法發現這些差異。

## 更多變體與未解問題

- **變體：**[特徵式蒸餾](../feature-based/index.zh-TW.md)，也可用於同一網路的各層之間。
- **未解問題：**為何網路從自己的副本學到的東西，比只從標籤學到的還多。正則化的解釋頗為合理，但尚無定論。
- **未解問題：**對大型模型而言，重複的世代是否持續改進，還是會趨於飽和。
- **相關：**[教師助手](../response-based/teacher-assistant/index.zh-TW.md)的概念處理師生之間的大落差，這與自我蒸餾沒有獨立教師的問題是不同的問題。

## 關聯

自我蒸餾類似學習者複習並鞏固自己先前的理解。系統透過重新學習自己的預測而改進，這個想法也在[持續學習](../../../../theory/paradigms/continual/index.zh-TW.md)中被研究，其中模型較早的狀態用來引導後續訓練。

## 參考文獻

### 開創性論文

- Furlanello, T., Lipton, Z. C., Tschannen, M., Itti, L. & Anandkumar, A. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — 訓練與教師架構相同的學生；摘要報告這些學生在視覺與語言任務上都勝過其教師。
- Zhang, L., Song, J., Gao, A., Chen, J., Bao, C. & Ma, K. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — 把網路較深部分的知識蒸餾到較淺部分；摘要報告平均準確率提升 2.65%。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 自我蒸餾沿用、並以網路本身作為教師的蒸餾目標。
- Mirzadeh, S.-I., Farajtabar, M., Li, A., Levine, N., Matsukawa, A. & Ghasemzadeh, H. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 指出師生差距過大時學生表現會下降，並提出中介的教師助手來縮小差距。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — 回顧蒸餾方法，包括本頁討論的自我蒸餾變體。

### 講座與影片

（本頁未查核）

### 文章與文件

（本頁未查核）
