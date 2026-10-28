---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/video
  - theory/models/transformer
tags:
  - ViViT
  - video Transformer
  - attention
aliases:
  - 影片視覺 Transformer
  - ViViT
  - Video Vision Transformer
---

# ViViT：影片視覺 Transformer

ViViT 是只由 Transformer 層構成的影片分類模型。它把一段片段轉換為時空詞元，並在其上套用自注意力，同時有多種分解空間與時間注意力的方式。它是視覺 Transformer 的影片對應版本，顯示影片分類不一定需要卷積。

## 概觀

[影片章節](index.zh-TW.md)提供了更廣的脈絡。本頁說明模型。影像用的 Transformer 會把圖片切成區塊，並把每個區塊視為一個詞元。ViViT 對影片做同樣的事，使用橫跨數個影格的管狀區塊（tubelet）作為詞元，然後對所有詞元做注意力。

## 問題

對每個時空詞元做完整注意力非常昂貴，因為詞元數量隨空間與時間大小的乘積成長。問題在於如何在降低成本的同時，保留注意力的表達能力，並在標註影片稀少時訓練這樣的模型。

## 核心想法

片段被切成互不重疊的時空管狀區塊，每一塊嵌入為一個詞元。作者提出多種分解式編碼器，把注意力拆開。其中一種變體先在每個影格內做空間注意力，再在每個位置跨影格做時間注意力。另一種變體依序套用空間與時間 Transformer。分解版本降低了成本，作者報告它們在實驗中與完整注意力相當。

## 方程式

對於 $T$ 個影格、每格 $N$ 個空間詞元的影片，完整自注意力的成本約為 $(TN)^2$ 次運算。先做空間注意力再做時間注意力的分解編碼器，成本約為 $T N^2 + N T^2$，當 $T$ 與 $N$ 都很大時，遠小於完整注意力。注意力本身採用 Transformer 論文中標準的縮放點積形式。

## 結果

論文報告，在當時的數個動作辨識基準上達到最佳結果，數字見其結果表。此處不重述數值，它們也取決於模型是否在大型影像或影片資料集上預訓練。

## 限制

- 注意力的成本仍隨片段長度與解析度快速成長。
- 效能依賴預訓練；僅在小型影片資料集上訓練的模型，可能不如卷積基準。
- 與其他影片分類器一樣，ViViT 可能會在基準片段中學到外觀捷徑。

[VideoMAE](index.zh-TW.md) 等遮蔽預訓練方法解決了資料問題。

## 關聯

ViViT 直接使用[Transformer](../../transformer/index.zh-TW.md)所述的架構，並把視覺 Transformer 的方法延伸到時間軸。它的注意力是同一章中與 [I3D](i3d.zh-TW.md) 一併討論的分解形式之一。

## 應用

動作辨識、影片檢索，以及為字幕生成等下游任務提供影片表徵學習。

## 開放問題

- 隨著片段變長，哪一種空間與時間的分解最好？
- 影片 Transformer 的優勢有多少來自預訓練，而非架構本身？

## 參考文獻

### 奠基性論文

- Arnab、Dehghani、Heigold、Sun、Lučić 與 Schmid，*ViViT: A Video Vision Transformer*（2021）。https://arxiv.org/abs/2103.15691 — ViViT 模型及其分解式編碼器。
- Vaswani 等人，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — ViViT 應用於影片的 Transformer 架構。
- Dosovitskiy 等人，*An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*（2020）。https://arxiv.org/abs/2010.11929 — ViViT 延伸至影片的視覺 Transformer。
- Bertasius、Wang 與 Torresani，*Is Space-Time Attention All You Need for Video Understanding?*（2021）。https://arxiv.org/abs/2102.05095 — 不使用卷積的時空注意力影片模型，並比較了分解式注意力的設計。
- Tong、Song、Wang 與 Wang，*VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training*（2022）。https://arxiv.org/abs/2203.12602 — 遮蔽預訓練，減少影片 Transformer 所需的標註資料。
