---
translation_reviewed: 2026-11-01
last_reviewed: 2026-11-01
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
    本方法隸屬於[預填充與解碼分離](disaggregated-serving.md)，該頁比較不同系統。

Splitwise 將提示處理與後續 token 生成分配到不同機器，並為兩階段獨立配置資源。[^splitwise] 分離也可使用同質硬體；不同加速器類型是選項，而非必要條件。論文的工作負載呈現不同的運算與記憶體需求，因此採用按階段配置資源。

## 排程與交接

設計包含提示池、token 池，以及大小可動態調整的**混合池**。叢集排程器依待處理 token 數衡量佇列，選出提示／token 機器配對；機器排程器管理本機佇列與批次。[^splitwise]

提示機器產生第一個 token 與 KV 快取，token 機器接續生成。逐層非同步傳輸可以與後續提示運算重疊；較短提示則可使用序列式傳輸。混合池機器在高負載時可服務兩個階段。[^splitwise]

因此，兩個方塊的圖示適合入門，卻不足以完整描述排程器。資源池管理也不同於為每個請求保留一台專用機器：每台機器可隨時間服務多個請求。

## 為何快取傳輸重要

狀態包含已處理上下文的注意力鍵和值。PagedAttention 處理快取配置與共享，並不會讓網路傳輸免費。[^paged] 查詢頭數也不一定等於鍵／值頭數：分組查詢注意力讓多組查詢共用鍵／值頭。[^gqa]

對具有一致各層配置的單一假設序列，未壓縮的**邏輯**資料量為

$$
B_{\mathrm{KV}}=2LSH_{\mathrm{KV}}d_hb.
$$

其中 $L$ 為層數、$S$ 為快取序列長度、$H_{\mathrm{KV}}$ 為鍵／值頭數、$d_h$ 為每個頭的元素數、$b$ 為每個元素的位元組數。係數二同時計入鍵與值。

這計算的是張量元素，而非特定實作的配置量；不包含中繼資料、填補、複製、壓縮與傳輸協定開銷。分散式分片可分攤邏輯資料量，但頭的複製也可能增加實體總量；不應假定每個 GPU 都持有完整資料量。

### 資料量算例

假設 $L=32$、$S=4096$、$H_{\mathrm{KV}}=8$、$d_h=128$、$b=2$，則邏輯快取為 **536,870,912 位元組 = 512 MiB**。若有效酬載頻寬為 **25 GB/s**，其中 GB 使用十進位，完全序列式的傳輸至少需要

$$
t_{\mathrm{transfer}}\geq
\frac{B_{\mathrm{KV}}}{\beta_{\mathrm{effective}}}
=\frac{536{,}870{,}912}{25\times10^9}
\approx21.5\ \mathrm{ms}.
$$

這些參數僅供說明，並非 Splitwise 或特定模型的測量值。若 $H_{\mathrm{KV}}$ 改為 32，資料量就會變成四倍。連線標示的位元速率、有效位元組吞吐量，以及二進位 MiB，不能互相直接代換。

這個界限衡量的是簡化單一傳輸流模型中的搬移工作。重疊可以從端到端延遲中隱藏部分工作，卻不會消除位元組或同步。共享網路容量與同時傳輸，也可能降低每個請求的有效頻寬。

## 第一個 token 與交接間隔

因為提示機器可在序列式傳輸完成前回傳第一個 token，只測量**首 token 時間（TTFT）**，可能漏掉之後的停頓。[^splitwise]

考慮一個刻意採序列方式的示意時間線：傳輸達到上述頻寬界限，最初等待與提示處理合計 40 ms，一次解碼需要 8 ms：

| 事件 | 距抵達時間，約略值 |
|---|---|
| 回傳第一個 token | 40.0 ms |
| 快取傳輸完成 | 61.5 ms |
| 回傳第二個 token | 69.5 ms |

TTFT 為 40 ms，但第一與第二個 token 的間隔約為 29.5 ms。這是依假設時間線計算的結果，而非實測排程。佇列、傳輸重疊，或不同的 token 交付時點，都會改變它。

除了 TTFT，還應報告 token 間延遲及其尾端分布。DistServe 在資源分配與放置時，同樣分別考量預填充與解碼的延遲目標。[^distserve]

## 評估能確立什麼

原型在 vLLM 上擴充快取傳輸；較大規模的叢集設計則使用以效能量測為基礎的事件驅動模擬器。[^splitwise] 應區分硬體測量與模擬的資源配置結果。

兩個具體的論文操作點為：

- **圖 18(a)，對話工作負載：**Splitwise-AA 在相同成本與預配置功率下，達到 Baseline-A100 的 2.15 倍吞吐量。
- **圖 18(b)，固定成本：**Splitwise-AA 達到 Baseline-H100 的 1.4 倍吞吐量，但功率增加 25%，空間為兩倍。[^splitwise]

它們使用不同基準與限制條件，並非同一部署同時具有的屬性。預配置功率是容量預算，不會自動等於每個請求實際消耗的能量。

## 相關技術

- [Orca](orca.md) 提出迭代層級排程；它是排程的參考，而非 Splitwise 原型執行 Orca 實作的證據。[^orca]
- [PagedAttention 與 vLLM](paged-attention.md) 處理快取記憶體管理，與跨機器路由是不同問題。[^paged]
- [DistServe](distserve.md) 在延遲限制下最佳化各階段的資源與平行策略。[^distserve]
- [Mooncake](mooncake.md) 採用以 KV 快取為中心的架構，包含分散式快取資源與過載處理。[^mooncake]

## 重現與營運限制

比較時應記錄：

1. 模型與權重版本、注意力頭配置、快取精度及平行策略。
2. 加速器類型、機器數、功率上限與成本計算期間。
3. 提示／輸出長度分布、到達過程、批次政策與資源池大小政策。
4. 有效網路頻寬、傳輸策略與同時進行的傳輸數。
5. 延遲目標與百分位數、接受的請求速率、逐筆 token 間隔與資源使用率。
6. 哪些結果來自硬體測量，哪些由模型或模擬器估計。

應清楚保留無損交接的假設。改變快取精度或表徵，會引入額外近似，其準確性須另外評估。排程改善本身，並不能證明有損快取表徵會保留輸出。

故障與重試需要明確的狀態擁有權政策：哪個機器負責請求、何時完成傳輸，以及客戶端已收到什麼。這些是部署問題，而非可由吞吐量數字推導出的保證。在輸出一部分後重播請求，也須避免串流 token 重複。

長提示工作負載與長輸出工作負載會對不同資源造成壓力。因此，固定資源池比例應在需求改變時接受評估，而非假定對所有軌跡都最佳。

[^splitwise]: Patel et al.，arXiv v2（2024），第 IV–VI 節與圖 18；詳見參考文獻。
[^paged]: Kwon et al.（2023），摘要；詳見參考文獻。
[^gqa]: Ainslie et al.（2023），摘要；詳見參考文獻。
[^distserve]: Zhong et al.（2024），摘要；詳見參考文獻。
[^orca]: Yu et al.（2022），出版者摘要；詳見參考文獻。
[^mooncake]: Qin et al.，arXiv v5（2026），摘要；詳見參考文獻。

## 參考文獻

- Patel, P. et al. (2023; revised 2024). *Splitwise: Efficient Generative LLM Inference Using Phase Splitting*. https://arxiv.org/abs/2311.18677 — 描述按階段劃分的資源池、排程、快取傳輸，以及以硬體效能量測為基礎的叢集設計評估。
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. https://arxiv.org/abs/2401.09670 — 在首 token 與每個輸出 token 的延遲需求下，最佳化階段分配與放置。
- Qin, R. et al. (2024; revised 2026). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. https://arxiv.org/abs/2407.00079 — 描述分散式快取資源、分離的服務階段與過載排程。
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI. https://www.usenix.org/conference/osdi22/presentation/yu — 提出自迴歸生成的迭代層級排程與選擇性批次處理。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP. https://arxiv.org/abs/2309.06180 — 處理 KV 快取的碎片與共享，支援更大的服務批次。
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP. https://aclanthology.org/2023.emnlp-main.298/ — 說明分組查詢注意力中，鍵／值頭數為何可能不同於查詢頭數。
