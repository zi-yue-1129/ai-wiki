---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/inference-optimization
  - engineering/hardware
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - Mooncake
  - 以 KV 快取為中心的架構
---

# Mooncake

!!! info "屬於預填充與解碼分離"
    本方法頁隸屬於[預填充與解碼分離](disaggregated-serving.zh-TW.md)。它詳細說明 Mooncake；上層頁面則比較它與其他系統。

Mooncake 是一套圍繞 KV 快取建構的服務架構。它把預填充與解碼叢集分開，並把提示的快取當成共享資源，可以在請求之間儲存、搬移與重用。論文描述它是為高度過載的情境設計的，並報告在模擬情境中的吞吐量增益，以及在一個實際部署中能處理的請求數增加。

## 問題

大規模服務同時面臨兩種壓力。提示很長的請求在預填充需要大量運算，而許多請求共享相同的前綴，因此它們的 KV 快取是重複的工作。當系統過載時，把每個請求視為獨立的排程器無法重用這些工作，也無法在尖峰期間為新到的請求維持低延遲。問題在於：如何透過把快取視為一等資源，在過載下服務更多請求。

## 核心想法

Mooncake 把預填充與解碼叢集分開，並圍繞 KV 快取組織整個系統。提示的快取保存在分散式儲存中，因此與先前請求共享前綴的新請求，可以重用已儲存的快取，而不必重新計算。排程器在放置預填充與解碼工作時會考慮快取，而且當搬移快取區塊比重新計算更便宜時，系統可以在機器之間移動它們。

## 程序

1. 接收請求，並在分散式快取儲存中查詢與其提示相符的已儲存前綴。
2. 若找到相符的前綴，載入已快取的區塊；否則在預填充節點上執行預填充。
3. 儲存新的快取區塊，使之後的請求能重用它們。
4. 把快取送到解碼節點，並在該節點上生成 token。
5. 在過載時，讓排程器拒絕、延後或重新路由請求，以使其餘請求維持在延遲目標內。

## 結果

論文報告，在某些模擬情境中，Mooncake 的吞吐量最多可提升 525%。它也報告，在真實工作負載下，此架構使已部署的服務能處理多 75% 的請求。模擬與部署的結果來自不同的設定，而部署情境中的增益取決於工作負載包含多少前綴共享。

## 限制

- **依賴前綴共享。** 大部分增益來自已快取前綴的重用。前綴共享少的工作負載受益要少得多。
- **儲存容量與放置。** 分散式快取儲存有自己的記憶體限制，而放置策略決定哪些區塊能保留下來。
- **模擬結果。** 最大的吞吐量數字來自模擬，因此只是所模擬情境的估計。
- **工程範圍。** 此架構橫跨儲存、排程與傳輸，建構與營運的規模都很大。

## 關聯

- 以 GPU 為單位分離階段、並搭配配置搜尋的替代設計，見 [DistServe](distserve.zh-TW.md)。
- Mooncake 也採用的跨機器階段分割，見 [Splitwise](splitwise.zh-TW.md)。
- 讓區塊層級重用可行的分頁式記憶體佈局，是 [PagedAttention 與 vLLM](paged-attention.zh-TW.md)。

## 開放問題

- 當前綴共享因使用者與時間而異時，應如何設定快取儲存的大小與放置？
- 重用策略能否在含有私人資料的提示上保證安全，使這些資料不會透過共享快取外洩？

## 參考文獻

### 重要論文

- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079. https://arxiv.org/abs/2407.00079 — 主要論文：以快取為中心、分開預填充與解碼叢集的架構，並提供模擬與部署的結果。
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — 以有效吞吐為基礎配置的 GPU 層級分離，供比較。
- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — 機器層級的階段分割，供比較。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — 讓區塊層級重用可行的分頁式快取佈局。
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 此類服務系統所依據的迭代層級排程。
