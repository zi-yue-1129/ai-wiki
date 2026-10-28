---
translation_reviewed: 2026-10-28
---

# 預填充與解碼分離

預填充與解碼分離是一種服務設計，把大型語言模型推論的兩個階段，分別放在不同的 GPU 池上執行。預填充池處理提示並建立其 [KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)；接著這份快取被移到解碼池，由解碼池產生輸出。把兩個階段分開，可以避免長提示與逐 token 生成共用同一張 GPU 時的互相干擾，也讓每個池都能依自己的延遲目標調整規模與設定。

## 概述

一次請求的服務包含兩個階段，見[推論最佳化](index.zh-TW.md)。預填充以一次平行處理讀完整段提示，並產生第一個輸出 token。接著解碼一次產生其餘的 token，每一步都要讀取模型權重與該請求的快取。

多數引擎會把兩個階段放在同一批 GPU 上。[連續批次處理](orca.zh-TW.md)能讓這個共用批次保持滿載，但一個大型預填充加入後，會拖慢批次中每一步解碼，使用者會感覺到 token 之間停頓。分離式設計則讓每個階段使用各自的機器，以避開這個衝突。研究系統在 2023 與 2024 年提出這個想法，而 Mooncake 報告它已用於正式營運的服務。

## 關鍵概念

- **預填充實例（prefill instance）**：處理提示並寫入其 KV 快取的工作單元。
- **解碼實例（decode instance）**：接收快取並產生輸出 token 的工作單元。
- **首 token 時間（TTFT）**與**每個輸出 token 的時間（TPOT）**：前者是第一個 token 出現前的延遲，主要由預填充決定；後者是之後各 token 之間的平均間隔，主要由解碼決定。
- **服務等級目標（SLO）**：服務所承諾的延遲目標，通常是對 TTFT 與 TPOT 的上限。
- **良好吞吐量（goodput）**：在滿足 SLO 的前提下完成的請求速率。DistServe 以它作為主要指標，取代單純的吞吐量。
- **KV 傳輸**：把一個請求的快取，從預填充實例透過網路或互連移到解碼實例。

## 運作方式

對一個請求而言，路徑會經過一個路由器與兩個池：

```mermaid
flowchart LR
  R[請求] --> G[全域排程器]
  G --> P[預填充池：計算提示的 KV]
  P --> T[KV 傳輸]
  T --> D[解碼池：產生 token]
  D --> O[串流輸出]
```

排程器先把請求送到某個預填充實例。傳輸開始之前，解碼實例必須先為即將到來的快取保留記憶體。預填充完成後，快取經由網路移動，之後由解碼實例接手，直到輸出結束。

兩個階段能如此乾淨地分開，是因為它們的瓶頸不同。在預填充中，權重只讀取一次，就能服務所有提示 token，因此算術強度高，速度受算力限制（參考文獻中的屋線模型可說明這種取捨）。在解碼中，每一步都要讀取權重，以及每個序列的快取，才能為每個序列產生一個 token，因此速度受記憶體頻寬限制。於是每個池都能採用適合其階段的平行方式與 GPU 數量，而預填充與解碼 GPU 的比例也能依負載調整。

**KV 傳輸成本。** 每個請求要移動的快取大小，依循[KV 快取壓縮](kv-cache-compression.zh-TW.md)中的公式 $2 \cdot L \cdot H_{kv} \cdot d_h \cdot T \cdot b$，其中 $T$ 為提示長度。作為粗略估算，假設模型有 32 層、32 個 key-value 頭，每個頭的維度為 128，數值以 16 位元儲存。這樣每個 token 需要 $2 \cdot 32 \cdot 32 \cdot 128 \cdot 2$ 位元組，也就是 512 KiB。一個 2048 token 的提示會產生 1 GiB 的快取。若連結的頻寬為 25 GB/s，搬移它約需 40 毫秒，對於以數百毫秒計的 TTFT 目標而言，這是相當可觀的一部分。分組查詢注意力、量化快取與快速互連都能降低這項成本；另外，設計上也可以讓傳輸與預填充運算重疊，例如每一層的快取一準備好就先送出。此處的數字只是示意，並非量測結果。

## 關鍵方法

主要變體的差異，在於它們最佳化的目標，以及除了分離本身之外還改了什麼。最後一列是不移動快取的共置替代方案。結果欄位為各論文摘要中的數字，所用的模型與硬體各不相同，因此彼此不能直接比較。

| 變體 | 與其他方法的區別 | 報告的結果（取自摘要） |
|---|---|---|
| Splitwise | 先分析兩個階段，再把它們分到不同機器上，解碼機器則選用較低功耗與成本的硬體 | 吞吐量為目前設計的 1.4 倍，成本低 20% |
| DistServe | 依良好吞吐量目標，分別為每個階段規劃資源與平行方式，並依叢集頻寬安排兩個階段的位置 | 可服務最多 7.4 倍的請求，或在 SLO 收緊 12.6 倍的情況下仍能服務，優於最先進系統 |
| TetriInfer | 把提示切成固定大小的區塊，分離兩個階段，並依預測的資源用量排程 | 平均 TTFT 降低 97%，平均工作完成時間降低 47%，且少用 38% 的資源 |
| Mooncake | 面向正式營運服務的 KV 快取中心架構，在 CPU 記憶體與 SSD 之間建立快取池，並在過載時提早拒絕請求 | 在部分模擬情境中吞吐量最多提高 525%；真實工作負載下多服務 75% 的請求 |
| Sarathi-Serve（共置） | 分塊預填充把提示區塊加入解碼批次，且不暫停解碼，因此不需移動快取 | 在單張 A100 上服務 Mistral-7B，於尾部延遲限制下，服務容量為 vLLM 的 2.6 倍 |

Splitwise 把分離視為硬體與成本的決策，DistServe 則把它視為由 SLO 所決定的規劃問題；TetriInfer 與 Mooncake 則在分離之外加上排程與快取的設計。Sarathi-Serve 則說明，不需要任何傳輸，也能移除大部分的干擾。

## 相關連結

快取本身的說明見 [Transformer KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)。每個實例管理記憶體的方式見 [PagedAttention 與 vLLM](paged-attention.zh-TW.md)，而 [KV 快取壓縮](kv-cache-compression.zh-TW.md)則能減少實例之間搬移的位元組數。

分離式設計把 [Orca](orca.zh-TW.md) 的排程概念，從一個池延伸到兩個池。傳輸是否划算，取決於互連與記憶體頻寬，見 [AI 硬體](../hardware/index.zh-TW.md)。維持兩個必須保持平衡的池，並加上監控與自動擴縮，則是另一個營運問題，見 [MLOps 與部署](../mlops/index.zh-TW.md)。

腦科學的類比在這裡很薄弱：專門化的模組彼此傳遞工作，充其量只是粗略的比擬，因此本頁不依賴這個類比。

## 應用

- **長提示的聊天服務**：使用者同時感受得到首 token 的延遲與穩定的輸出速度。Mooncake 描述了 Kimi 服務的這種情境。
- **長文件任務**：長輸入搭配短答案時，預填充佔主導地位，因此預填充池可以獨立於解碼池擴充規模，DistServe 與 Splitwise 在分別規劃各階段規模時，都是這樣做的。
- **混合工作負載**：TetriInfer 以混合的下游工作負載為目標，這類請求的提示與輸出長度差異很大，而一個長提示若不加處理，可能會拖慢許多解碼步驟。

## 開放問題

- **上下文增長時的傳輸**：快取大小隨提示長度線性成長，因此要傳輸、重新計算或壓縮它，取決於工作負載與連結。
- **池的規模**：預填充與解碼 GPU 的最佳比例，會隨提示與輸出長度改變。為兩個池擴充規模，比擴充單一池困難。
- **故障與重用**：若解碼實例在生成中途故障，它的快取可能必須重建。像 Mooncake 那樣的共用快取池，能帶來跨請求的重用，但也帶來新的故障模式。
- **分離或共置**：分塊預填充縮小了兩者的差距，哪一種設計較好，取決於硬體、網路與延遲目標。

## 參考文獻

### 奠基性論文

- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. OSDI 2024. https://arxiv.org/abs/2401.09670 — 把兩個階段放在不同 GPU 上，並為每個階段分別規劃資源與平行方式。
- Patel, P. et al. (2024). *Splitwise: Efficient generative LLM inference using phase splitting*. ISCA 2024. https://arxiv.org/abs/2311.18677 — 分析提示計算與 token 生成的特性，再把兩者分到不同機器上。
- Hu, C. et al. (2024). *Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads*. arXiv preprint. https://arxiv.org/abs/2401.11181 — 結合分塊提示、獨立的預填充與解碼實例，以及針對混合工作負載的兩層排程器。
- Agrawal, A. et al. (2024). *Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve*. OSDI 2024. https://arxiv.org/abs/2403.02310 — 在單張 GPU 上使用分塊預填充與無停頓批次處理，作為在機器之間移動快取的替代方案。
- Qin, R. et al. (2024). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv preprint. https://arxiv.org/abs/2407.00079 — 描述一個分離預填充與解碼叢集、並以 CPU 記憶體與 SSD 共用快取的正式營運平台。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 介紹 vLLM 中的分頁式 KV 快取記憶體管理，分離式系統中的每個實例仍需要它。

### 綜述與教科書

- Zhou, Z. et al. (2024). *A Survey on Efficient Inference for Large Language Models*. arXiv preprint. https://arxiv.org/abs/2404.14294 — 綜述文章，把服務層級的系統性最佳化放進高效 LLM 推論的分類架構中。

### 文章與文件

- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://doi.org/10.1145/1498765.1498785 — 定義屋線模型，說明為何預填充受算力限制、解碼受記憶體頻寬限制。
