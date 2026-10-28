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
  - Splitwise
  - 階段分割
---

# Splitwise

!!! info "屬於預填充與解碼分離"
    本方法頁隸屬於[預填充與解碼分離](disaggregated-serving.zh-TW.md)。它詳細說明 Splitwise；上層頁面則比較它與其他系統。

Splitwise 是一種叢集層級的設計，把 LLM 請求的兩個階段（提示計算與 token 生成）分到不同的機器上。作者的論點是，兩個階段需要不同的硬體，因此若叢集只配置一種機器類型來服務兩者，就會浪費資源。Splitwise 分別為每個階段配置資源，並透過快速連線在機器之間搬移狀態。論文報告在相同成本下有更高的吞吐量，或在相同成本與功耗預算下有更多的吞吐量。

## 問題

提示階段會平行處理許多 token，計算量大。Token 階段每一步只產生一個 token，受記憶體限制。適合某一階段的機器，往往不適合另一階段；而以單一機器類型建構的叢集，必須為不需要的那個階段過度配置。問題在於：如何讓每個階段使用合適的硬體，又不必為每個請求專門保留一台機器。

## 核心想法

Splitwise 讓一個請求的提示階段在一台機器上執行，token 階段在另一台機器上執行，使每一個階段都能使用適合它的硬體。叢集依階段分別配置，因此提示機器與 token 機器的數量可依工作負載來設定。Token 階段所需的狀態，主要是 KV 快取，會透過互連在機器之間傳輸，而這個傳輸的設計是與每一側的運算重疊進行。

## 程序

1. 接收請求，並把它的提示送到提示資源池中的一台機器。
2. 在該機器上計算提示的 KV 快取。
3. 透過叢集的快速互連，把快取傳到 token 資源池中的一台機器。
4. 在 token 機器上逐步生成 token，並在資源池內進行批次處理。
5. 依工作負載配置兩個資源池的大小，並隨負載改變調整比例。

## 結果

論文報告，相較於它所比較的現行設計，此設計能在成本低 20% 的情況下達到 1.4 倍的吞吐量。論文也報告，在相同成本與功耗預算下，此設計能達到 2.35 倍的吞吐量。這些是論文中的工作負載與硬體上的叢集層級結果，比較的基準是當時的設計，因此讀數字時應連同這些設定一起考慮。

## 限制

- **互連上的傳輸。** 增益取決於機器之間有快速連線。若沒有，搬移快取的成本可能抵銷增益。
- **硬體假設。** 此設計假設不同的硬體適合不同的階段，而這取決於可用的加速器。
- **資源配置。** 兩個資源池之間的比例必須符合工作負載中提示與輸出長度的組合，而這個組合會隨時間改變。
- **營運複雜度。** 路由、故障處理與快取狀態現在會跨越多台機器。

## 關聯

- 以 GPU 為單位分離階段，並搭配配置搜尋的做法，見 [DistServe](distserve.zh-TW.md)。
- 以快取為中心、在過載下分開叢集的架構，見 [Mooncake](mooncake.zh-TW.md)。
- 每個資源池內部的迭代層級批次處理，沿用 [Orca](orca.zh-TW.md)。

## 開放問題

- 能否依提示與輸出組合的變化，自動調整兩個資源池的大小？
- 當加速器本身就能同時把兩個階段都做好時，依階段的硬體優勢是否仍然成立？

## 參考文獻

### 重要論文

- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — 主要論文：把階段分到不同機器上、依階段配置，並報告吞吐與成本結果。
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — 以 GPU 為單位的階段分離與配置搜尋，供比較。
- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079. https://arxiv.org/abs/2407.00079 — 以快取為中心的分離式架構，在過載下供比較。
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 資源池內部使用的迭代層級排程。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — 搬移過來的狀態所儲存的分頁式快取佈局。
