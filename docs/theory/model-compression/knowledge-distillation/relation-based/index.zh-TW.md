---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
- theory/models/transformer
tags:
- model compression
- knowledge distillation
- relation-based distillation
aliases:
  - 關係式蒸餾
  - Relation-based distillation
  - Relational knowledge distillation
---

# 關係式蒸餾

關係式蒸餾（relation-based distillation）轉移的是樣本之間的關係，而不是單一樣本的輸出或特徵。學生學到某些輸入對在教師的表徵空間中是接近還是遙遠，而這類結構是單一輸出與特徵所不具備的。

## 概觀

輸出匹配要求學生重現教師對每個輸入的答案。特徵匹配要求它重現教師的內部向量。關係匹配則要求它重現一個批次的幾何結構：成對的距離、三元組的角度，或樣本之間的相似度。這種幾何結構常對檢索或分群等下游任務很重要，因此即使個別輸出已經相符，轉移它仍有幫助。

## 關鍵概念

- **成對關係（pairwise relation）。** 由兩個樣本計算的量，例如它們在表徵空間中的距離或相似度。
- **高階關係（higher-order relation）。** 由三個或更多樣本計算的量，例如一個三元組形成的角度。
- **批次層級損失。** 關係損失在一個批次上計算，因此批次的組成與大小會影響訓練訊號。
- **幾何結構。** 表徵的排列方式。即使教師與學生的座標系不同，也能匹配這種結構。

## 主要方法

以下兩個代表性方法都在批次內匹配關係，差別在於保留哪些關係。

- [RKD（Park 等人，2019）](rkd/index.zh-TW.md)：匹配樣本之間的距離關係與角度關係，因此同時捕捉成對與高階結構。
- [保留相似度的蒸餾（Tung 與 Mori，2019）](similarity-preserving/index.zh-TW.md)：要求學生保留教師啟動值的成對相似度，目標較窄，也較容易說明。

RKD 使用較豐富的關係集合，包括三元組上的角度。保留相似度的蒸餾只保留成對相似度，使目標更容易解釋。

## 取捨

- **彈性與資訊量。** 關係讓學生可以使用不同的表徵幾何，但與輸出或特徵匹配相比，每個樣本攜帶的資訊較少。
- **對批次的依賴。** 損失取決於哪些樣本同批，因此批次大小與抽樣方式需要小心選擇。
- **成本。** 成對項的數量隨批次大小的平方增長，增加記憶體與時間成本。

## 更多變體與未解問題

- **變體：**[特徵式蒸餾](../feature-based/index.zh-TW.md)，直接匹配向量本身。
- **未解問題：**對於語言模型，哪些關係最能轉移知識，因為其表徵維度高，而且批次常由長序列組成。
- **未解問題：**當教師與學生在不同資料上訓練時，關係如何轉移。

## 關聯

樣本之間的關係是度量學習的核心對象，也是[Transformer 模型](../../../../theory/models/transformer/index.zh-TW.md)中嵌入幾何的研究重點。相似度結構承載意義的想法，也是[神經科學](../../../../brain-mind/neuroscience/index.zh-TW.md)的組織原則之一，該領域透過幾何來研究群體編碼。

## 參考文獻

### 開創性論文

- Park, W., Kim, D., Lu, Y. & Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — 提出距離關係與角度關係的蒸餾損失，轉移樣本之間的相互關係；摘要報告學生有明顯提升，並且在度量學習上，學生可以達到或超過教師。
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — 訓練學生，使教師啟動值中相似（或不相似）的輸入對，在學生的啟動值中也相似（或不相似）。
- Romero, A., Ballas, N., Ebrahimi Kahou, S., Chassang, A., Gatta, C. & Bengio, Y. (2015). *FitNets: Hints for Thin Deep Nets*. ICLR 2015. https://arxiv.org/abs/1412.6550 — 特徵層級的蒸餾，是關係匹配的對照。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — 依知識種類回顧蒸餾，包括關係式知識。

### 講座與影片

（本頁未查核）

### 文章與文件

- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 輸出層級的蒸餾基準，關係式方法即是延伸它。
