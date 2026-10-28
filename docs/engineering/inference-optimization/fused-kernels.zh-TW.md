---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - inference
  - GPU
  - kernels
aliases:
  - Fused Kernels
  - FlashAttention
  - IO-Aware Attention
  - 融合核心
  - 融合運算核心
  - 感知輸入輸出的注意力
---

# 融合核心與感知輸入輸出的注意力

融合核心（fused kernel）在一次掃描資料的過程中完成多個運算，使中間結果留在快速的晶片上記憶體中，而不必寫回較慢的記憶體再讀取。對大型語言模型而言，許多運算受限於記憶體流量而非算術速度，因此融合是推論時降低延遲、提高吞吐量的主要方法之一。

本頁是[推論最佳化](index.zh-TW.md)的一部分。

## 概述

在現代加速器上，算術單元往往比通往主記憶體的路徑快。若一個運算每讀寫一個位元組所做的算術很少，它的速度就受限於記憶體頻寬，而其速度取決於它要往返記憶體幾次。注意力機制是明顯的例子。樸素的計算會把一個很大的分數矩陣寫入記憶體，並在每一步讀回，因此其時間與記憶體成本都隨序列長度成長。

## 關鍵概念

- **核心（kernel）：**在加速器上執行的函式。模型的前向傳播就是一連串核心。
- **融合（fusion）：**把數個核心合併為一個，使中間值不必儲存在主記憶體中。
- **感知輸入輸出（IO-awareness）：**圍繞快速與慢速記憶體之間的讀寫次數來設計演算法，而不只考慮算術運算次數。
- **受記憶體限制的運算：**速度由記憶體流量決定的運算。

## 運作方式

融合的注意力核心會把查詢、鍵與值矩陣切成能放進快速記憶體的區塊。它載入一個區塊，計算該區塊的注意力分數，更新一個累積的正規化量，最後只寫出最終輸出。完整的分數矩陣從未被寫出。結果與標準注意力相同，因此此方法被描述為精確的。把偏置、啟動函式與正規化等小運算融合，也遵循相同原則，只是規模較小。

## 關鍵方法

- [FlashAttention（Dao 等人，2022）](../../theory/models/transformer/attention-variants/flash-attention/index.zh-TW.md)：以區塊計算的精確注意力，不儲存完整的分數矩陣。其專屬頁面位於模型章節。
- 融合的逐元素與正規化核心：把偏置、啟動函式與正規化層合併為一個核心，去掉它們額外的記憶體往返。
- 手寫核心與編譯器產生的核心：專家會為最熱門的運算手寫融合核心，其餘部分則由編譯器產生融合核心。這些選擇所針對的記憶體系統，見[硬體](../hardware/index.zh-TW.md)。

## 關聯

- 降低數值精度同樣能減少記憶體流量，見[混合精度訓練與推論](../hardware/co-design/mixed-precision.zh-TW.md)。
- 服務階段的注意力快取記憶體管理，見 [PagedAttention](paged-attention.zh-TW.md)。
- FlashAttention 所加速的注意力變體，見[Transformer 注意力變體](../../theory/models/transformer/attention-variants/index.zh-TW.md)。

## 應用

- 注意力成本佔主導的長上下文服務。
- 在 GPU 伺服器上降低聊天與程式補全的延遲。
- 加快訓練，因為同一批核心也能加速反向傳播。

## 限制

- **依賴硬體。**針對某一代加速器調校的核心，在另一代上未必快；隨著硬體變動，它也需要持續維護。
- **工程成本。**手寫核心難以撰寫與除錯，融合後的核心也比分開的運算更難修改。
- **效益取決於工作負載。**受算術限制的運算，幾乎無法從減少的記憶體流量中獲益。

## 開放問題

- 編譯器產生的融合核心，能在多大程度上比得上手寫核心？
- 核心的修改，應如何檢查其數值差異？

## 參考文獻

### 開創性論文

- Dao, T. 等人（2022）。*FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*。NeurIPS。https://arxiv.org/abs/2205.14135 — 提出感知輸入輸出的精確注意力，避免把完整的注意力矩陣存入記憶體。
- Dao, T.（2023）。*FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*。arXiv。https://arxiv.org/abs/2307.08691 — 同一核心家族的後續修訂，改進平行化與工作分配。
- Micikevicius, P. 等人（2018）。*Mixed Precision Training*。ICLR。https://arxiv.org/abs/1710.03740 — 顯示使用降低精度的算術訓練，可以達到與全精度相當的準確率，因而減少記憶體流量。
- Kwon, W. 等人（2023）。*Efficient Memory Management for Large Language Model Serving with PagedAttention*。SOSP。https://arxiv.org/abs/2309.06180 — 以分頁方式管理注意力快取，是服務端的記憶體系統做法。
- Chen, T. 等人（2018）。*TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*。OSDI。https://arxiv.org/abs/1802.04799 — 為多種硬體目標產生最佳化核心的編譯器，是手寫核心的自動化對應。
