---
tags:
- engineering
- systems
aliases:
- 完全分片資料平行
---

# PyTorch FSDP

完全分片資料平行（Fully Sharded Data Parallel, FSDP）是 PyTorch 對 ZeRO 式分片的實作。它把模型包成分片單元，將每個單元的參數分散在各個資料平行裝置上，在使用前收集，用完後釋放，使模型能以資料平行訓練，而模型狀態分散在各裝置上。

## 概述

分片模型狀態只有在容易使用時才有價值。FSDP 把它做成框架功能：使用者只要包裝模型，函式庫會處理參數收集、梯度歸約與通訊排程。每個分片單元只保留自己那一份展平參數的分片，因此峰值記憶體由最大的單元決定，而不是整個模型。

## 關鍵概念

- **分片單元（sharded unit）**：一組模組，其參數會一起展平並分片。單元的邊界決定參數何時被收集。
- **All-gather**：在前向或反向傳播之前，收集該單元在每個裝置上的完整參數。
- **Reduce-scatter**：跨裝置加總梯度，並讓每個裝置只保留自己負責的分片。
- **預先取得（prefetching）**：在目前單元計算時，提早開始下一個單元的 all-gather，使通訊與計算重疊。

## 運作方式

對每個分片單元，FSDP 在前向傳播前 all-gather 其參數，進行計算後釋放收集到的副本。在反向傳播時，它再次 all-gather，計算梯度，然後對梯度做 reduce-scatter，使每個裝置只保留梯度分片。最佳化器接著更新每個裝置自己的分片。

```mermaid
flowchart LR
  A[All-gather 單元參數] --> F[前向計算]
  F --> X[釋放收集到的參數]
  X --> B[反向前再次 all-gather]
  B --> G[反向計算]
  G --> R[Reduce-scatter 梯度]
  R --> O[最佳化器更新本地分片]
```

## 關鍵方法

這個方法是每個單元的收集、計算、釋放循環，加上梯度的 reduce-scatter。論文的證據是：在大量 GPU 上訓練大型 Transformer 模型時所量測到的記憶體與吞吐量，以及論文記錄的設計取捨。

## 結果

論文報告了在多顆 GPU 上以 FSDP 訓練大型 Transformer 模型的記憶體與吞吐量結果，並說明單元邊界與預先取得如何影響效能。確切數字取決於模型與叢集，讀者應參考論文中的實驗。

## 限制

- **單元邊界很重要**：選擇不當的單元，不是一次收集太多，就是產生許多小而慢的通訊。
- **每個模型都要調校**：預先取得與分片設定必須針對每種架構調整。
- **通訊**：參數分片會增加通訊，必須與計算重疊，才能維持吞吐量。

## 開放問題

- 對於結構不規則的模型，應如何自動選擇分片單元？
- FSDP 如何與同一次訓練中的張量平行與管線平行交互作用？

## 參考文獻

### 重要論文

- Zhao, Y. et al. (2023). *PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel*. VLDB 2023. https://arxiv.org/abs/2304.11277 — 說明 PyTorch 中完全分片資料平行的設計，以及其單元與預先取得的效能取捨。

### 相關工作

- Rajbhandari, S. et al. (2020). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. SC 2020. https://arxiv.org/abs/1910.02054 — FSDP 對參數、梯度與最佳化器狀態的分片所遵循的演算法。
- Li, S. et al. (2020). *PyTorch Distributed: Experiences on Accelerating Data Parallel Training*. VLDB 2020. https://arxiv.org/abs/2006.15704 — FSDP 所擴充的複製式資料平行設計，FSDP 在其上加入了分片。
- Shoeybi, M. et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. https://arxiv.org/abs/1909.08053 — 層內切分。FSDP 不做這件事，兩者可以組合。
- Narayanan, D. et al. (2021). *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM*. SC 2021. https://arxiv.org/abs/2104.04473 — 展示在叢集規模下，如何把分片資料平行與張量平行、管線平行結合。
