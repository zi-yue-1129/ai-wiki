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
  - DistServe
  - 預填充解碼分離服務
---

# DistServe

!!! info "屬於預填充與解碼分離"
    本方法頁隸屬於[預填充與解碼分離](disaggregated-serving.zh-TW.md)。它詳細說明 DistServe；上層頁面則比較它與其他系統。

DistServe 是一套服務系統，把 LLM 推論的預填充與解碼階段指派給不同的 GPU。作者主張，若兩個階段在同一顆 GPU 上執行，會彼此干擾；把它們分開，就能達成共用部署所無法達成的延遲目標。論文報告有效吞吐（goodput）的增益，也就是在延遲目標內完成的請求速率。

## 問題

服務系統的好壞，不只看每秒的總 token 數，還要看有多少請求能達到延遲目標。在共用的 GPU 上，一個很長的預填充會拖慢同一批次中請求的解碼，使 token 與 token 之間的時間拉長。為了保護延遲而調低批次大小，又會降低吞吐量，因此營運者必須在兩者之間取捨。問題在於：如何在不做這種取捨的情況下，於延遲目標內服務更多請求。

## 核心想法

DistServe 把預填充與解碼放在不同的 GPU 上，以消除干擾。如此每個階段都有自己的批次，每個資源池也能依自己的瓶頸來配置大小與平行化方式。系統透過搜尋，找出在目標延遲下能最大化有效吞吐的配置，從而決定每個階段的位置與平行度。提示處理完後，KV 快取會從預填充 GPU 搬到解碼 GPU。

## 程序

1. 在目標硬體上對模型進行剖析，估計不同批次大小與平行度下的預填充與解碼延遲。
2. 在延遲目標下搜尋位置配置，決定每個階段取得哪些 GPU 與何種平行度。
3. 把每個請求送到預填充 GPU，由它計算 KV 快取。
4. 把快取傳到解碼 GPU，由它以自己的批次產生輸出 token。
5. 監控兩個階段的延遲，並在工作負載改變時調整配置。

## 結果

論文報告，相較於它所評估的最先進系統，DistServe 能服務 7.4 倍的請求，或達成 12.6 倍更嚴格的 SLO，而且超過 90% 的請求都在延遲上限內完成。這些是有效吞吐的結果，只計入達到目標的請求，因此不應解讀為原始吞吐量的增益。比較結果取決於所評估的系統與選定的工作負載。

## 限制

- **配置搜尋。** 最佳配置取決於模型、硬體與工作負載，任何一項改變都要重新搜尋。
- **傳輸成本。** 每次預填充後，KV 快取都必須在 GPU 之間搬移，這會增加延遲，並佔用互連頻寬。
- **工作負載改變。** 當提示長度分布改變時，兩個資源池之間的固定分配可能失衡。
- **有效吞吐是人為選定的指標。** 增益是相對於某個延遲目標報告的，不同的目標可能改變排名。

## 關聯

- 以分塊長提示的方式讓兩個階段留在同一台機器上，是另一種做法，見[上層頁面](disaggregated-serving.zh-TW.md)。
- 其他跨機器分離階段的系統是 [Splitwise](splitwise.zh-TW.md) 與 [Mooncake](mooncake.zh-TW.md)。
- 每個資源池內部的批次處理，沿用 [Orca](orca.zh-TW.md) 的迭代層級概念。

## 開放問題

- 配置搜尋能否線上執行，使系統不需要長時間的剖析步驟，就能適應突發流量？
- 系統應如何判斷搬移快取比在解碼 GPU 上重新計算預填充更便宜？

## 參考文獻

### 重要論文

- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — 主要論文：階段分離、以有效吞吐為基礎的配置，以及 SLO 的結果。
- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — 獨立的設計，把階段分到不同機器上，供比較。
- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079. https://arxiv.org/abs/2407.00079 — 以快取為中心的同一種分離，在過載下供比較。
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 每個資源池內部使用的迭代層級排程。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — 傳輸過來的快取所儲存的分頁式快取佈局。
