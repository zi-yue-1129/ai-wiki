---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - theory/models/mixture-of-experts
  - engineering/inference-optimization
  - engineering/hardware
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - 混合專家模型服務
  - MoE 服務
  - 混合專家模型推論
---

# 混合專家模型的服務

!!! info "屬於推論最佳化"
    本頁隸屬於[推論最佳化](index.zh-TW.md)。它比較混合專家（MoE）模型帶來的服務問題；架構本身見[混合專家理論頁面](../../theory/models/mixture-of-experts/index.zh-TW.md)，每個具名方法各有自己的頁面。

混合專家（MoE）模型會把每個 token 路由到少數幾個專家子網路，因此對任一 token 而言，只有一部分參數是活躍的。這使得每個 token 的運算比同樣總大小的稠密模型便宜。但服務問題因此改變：所有專家仍必須儲存，而批次中的 token 會分散到可能位於不同裝置上的專家。

## 概述

MoE 模型把兩個數字分開看。總參數數量決定儲存模型所需的記憶體；活躍參數數量決定每個 token 的運算量。模型很大時，服務受記憶體限制；專家分散到許多裝置時，則受通訊限制。把所有專家放在一張 GPU 上的設計簡單，但限制了模型大小。把專家分散到多張 GPU 上，則需要把 token 送到專家所在處再送回，這會在每一層都增加通訊。

## 關鍵概念

- **專家平行化。** 把不同的專家放在不同的裝置上，每台裝置只保存部分專家，token 則送到持有其專家的裝置。
- **負載平衡。** 路由可能把大部分 token 送到少數幾個專家。過載的專家會拖慢整層，因為該層要等最慢的裝置完成。
- **記憶體佔用與活躍參數。** 模型必須能以總大小放進記憶體，而它的速度則取決於活躍的大小。
- **專家卸載。** 把不活躍的專家保存在主機記憶體或磁碟中，需要時再載入。

## 運作方式

對每一層 MoE，路由器會為每個 token 選擇專家。Token 依專家分組，送到持有這些專家的裝置。每個專家處理自己的 token，輸出再被送回並合併。

```mermaid
flowchart LR
  T[批次中的 token] --> R[路由器選擇專家]
  R --> A[全互連：把 token 送到專家所在裝置]
  A --> E[專家在各自的裝置上計算]
  E --> B[全互連：送回輸出]
  B --> C[為每個 token 合併輸出]
```

兩次全互連通訊，是專家平行化所增加的成本。它們的大小取決於批次，以及路由器把 token 分散得多均勻。

## 關鍵方法

每個具名方法各有自己的頁面。下表比較它們。

| 方法 | 處理的問題 | 核心想法 | 主要取捨 | 頁面 |
|---|---|---|---|---|
| GShard | 專家很多的模型必須手動分散到各裝置 | 為模型加上標註，讓編譯器把專家分片到各裝置 | 需要分片標註與能力足夠的編譯器 | [GShard](gshard.zh-TW.md) |
| DeepSpeed-MoE | MoE 模型在記憶體與延遲上服務成本都高 | 壓縮模型，並使用為 MoE 層設計的推論系統 | 增益取決於壓縮與所用的系統 | [DeepSpeed-MoE](deepspeed-moe.zh-TW.md) |
| 專家卸載 | 大型 MoE 模型放不進單一裝置的記憶體 | 把不活躍的專家移出裝置，需要時再載入 | 當路由器選到不在裝置上的專家時，載入會增加延遲 | [專家卸載](expert-offloading.zh-TW.md) |

## 結果

三種方法在不同的硬體與模型上報告，因此結果不能直接比較。GShard 報告以自動分片訓練超過 6000 億參數的稀疏閘控 MoE 模型。DeepSpeed-MoE 報告模型壓縮可使 MoE 模型大小縮小最多 3.7 倍，而其推論系統相較於現有 MoE 推論方案，延遲與成本改善 7.3 倍。專家卸載報告能在桌上型硬體上以混合量化執行 Mixtral-8x7B，其摘要未給出速度數字。

## 取捨

- **在地性與記憶體。** 把所有專家放在裝置上速度快，但限制了模型大小。卸載能放下較大的模型，但會增加載入延遲。
- **平衡與準確度。** 強制把 token 平均分散到各專家，可能改變模型的輸出，因此平衡與路由之間需要取捨。
- **通訊與運算。** 專家平行化會在每一層增加全互連流量。批次小時，流量的成本可能超過它節省的運算。
- **量化。** 量化專家權重可以減少記憶體，但對品質的影響取決於路由器與專家。

## 關聯

- 架構與路由見[混合專家理論頁面](../../theory/models/mixture-of-experts/index.zh-TW.md)，包括 [Mixtral](../../theory/models/mixture-of-experts/mixtral.zh-TW.md) 與 [Switch Transformer](../../theory/models/mixture-of-experts/switch-transformer.zh-TW.md)。
- 服務同一模型的注意力部分，沿用 [KV 快取壓縮與淘汰](kv-cache-compression.zh-TW.md)中的快取方法。
- 把預填充與解碼階段分到不同機器上的做法，見[預填充與解碼分離](disaggregated-serving.zh-TW.md)，它也可以套用於 MoE 模型。
- 承載全互連流量的硬體，見 [AI 硬體](../hardware/index.zh-TW.md)。

## 開放問題

- 在服務期間，要如何訓練或約束路由器，才能讓專家負載保持平衡，又不改變模型的輸出？
- 當專家被卸載時，考慮到每個提示的路由都不同，應該保留哪些專家在裝置上？

## 參考文獻

### 重要論文

- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. https://arxiv.org/abs/2006.16668 — 用於分片稀疏閘控 MoE 模型的標註 API 與 XLA 擴充，並有超過 6000 億參數的訓練結果。
- Rajbhandari, S. et al. (2022). *DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale*. arXiv:2201.05596. https://arxiv.org/abs/2201.05596 — MoE 模型壓縮與 MoE 推論系統，附有延遲、成本與大小的結果。
- Eliseev, A. & Mazur, D. (2023). *Fast Inference of Mixture-of-Experts Language Models with Offloading*. arXiv:2312.17238. https://arxiv.org/abs/2312.17238 — 用於 MoE 推論的參數卸載，能在桌上型硬體上執行 Mixtral-8x7B。
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research. arXiv:2101.03961. https://arxiv.org/abs/2101.03961 — Top-1 專家路由，減少每個 token 路由所增加的通訊。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — MoE 服務系統為模型注意力部分所依據的分頁式記憶體佈局。
