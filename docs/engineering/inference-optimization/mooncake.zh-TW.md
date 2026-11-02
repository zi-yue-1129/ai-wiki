---
translation_reviewed: 2026-11-02
last_reviewed: 2026-11-02
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
    本方法頁隸屬於[預填充與解碼分離](disaggregated-serving.md)。上層頁面比較各個系統；本頁說明 Mooncake 的快取放置與過載政策。

Mooncake 結合獨立的預填充與解碼資源池，以及分散式鍵值（KV）快取。排程器考量可重用前綴存放的位置、搬移時間，以及請求能否在延遲目標內完成。以下依據 Qin 等人的論文，包括 2026 年 10 月修訂版。[^mooncake]

## 問題

預填充處理提示並建立注意力的 KV 快取；解碼利用這些狀態生成後續 token。長提示可能占用維持解碼回應速度所需的資源。分離兩個階段可減少干擾，卻帶來另一個決策：當可重用狀態位於別台機器時，請求應在哪裡執行？

兩項服務水準目標（SLO）尤其重要：從請求抵達開始計算的**首個 token 時間（TTFT）**，以及生成期間的 **token 間隔時間（TBT）**。快取命中雖可節省運算，仍可能因搬移或排隊而超出 TTFT 目標。同樣地，若解碼池隨後拒絕請求，已完成的預填充就成了浪費。[^workflow]

## 架構與請求路徑

Mooncake 整合 GPU 叢集周邊的 CPU、DRAM、SSD 與網路資源。**Conductor** 是全域排程器；**Messenger** 透過遠端直接記憶體存取（RDMA）搬移快取區塊。CPU 記憶體以分頁區塊存放 KV，並透過與前綴相關的雜湊識別可重用狀態。雜湊包含先前區塊，因此相同文字片段若接在不同前綴之後，並不足以構成命中。[^workflow]

概念上的請求路徑如下：

1. **比對前綴並選擇執行個體。** 選擇預填充與解碼資源時，比較快取可用性、預估預填充排隊時間與搬移成本。
2. **載入可重用狀態。** 將符合的前綴區塊取入預填充執行個體；未命中時省略此步驟。
3. **計算未快取的後綴。** 部分命中仍需增量預填充，並儲存新算出的狀態供重用。
4. **將狀態串流送往解碼端。** 逐層載入與儲存可讓搬移和運算重疊；整條路徑並非一連串完全阻塞的複製。
5. **重新檢查解碼容量並生成。** 本地解碼排程器會再次檢查延遲限制，才將請求納入連續批次。全域放置並不保證未來一定有可用名額。[^workflow]

### 部分命中不代表提示已處理完畢

以一個假設提示為例：總長 4,096 個 token，其中可重用前綴長 3,072 個 token：

| 數量 | 數值 |
|---|---|
| 提示總長 $N$ | 4,096 個 token |
| 可重用前綴長度 $H$ | 3,072 個 token |
| 未快取後綴 $N-H$ | 1,024 個 token |
| token 覆蓋率 $H/N$ | 75% |

這是自行設計的算例，不是論文的效能測試。後綴仍需對先前上下文執行注意力運算。因此，75% 的 token 覆蓋率不代表延遲減少 75%：排隊、資料搬移與後綴注意力仍然存在。

為建立直覺，可用一個忽略重疊的簡化成本比較兩個候選位置：

$$
\widehat T_i = Q_i + X_i + F(N,H_i),
$$

其中 $Q_i$ 是預估排隊時間，$X_i$ 是快取載入時間，而 $F$ 是前綴覆蓋長度為 $H_i$ 時的剩餘預填充時間。命中較長前綴的節點，仍可能輸給佇列較短或搬移較快的節點。此式用來說明排程取捨，並非延遲保證，也不是 Mooncake 逐層重疊執行的模型。論文的快取感知排程結合預估預填充、搬移與排隊成本，也考慮複製熱門區塊以平衡負載。[^scheduling]

## 過載與提早拒絕

**准入**決定是否接受請求，與尋找快取區塊是不同的決策。等到解碼才拒絕無法服務的請求，會浪費已執行的預填充。只在預填充前檢查解碼池的「目前」負載，也會出問題：一波已接受的預填充可能在檢查之後才抵達解碼池，使兩個資源池交替過載與缺乏工作。

Mooncake 改為預測這些預填充完成時的解碼負載。論文描述的實作採用**統一解碼時長的系統層級估計**，納入預期從預填充抵達的請求，以及從解碼離開的請求。它並未聲稱能準確預測每個請求的輸出長度；請求層級預測留待未來工作。[^overload]

評估這類政策時，應同時報告送入負載、拒絕數、完成數與延遲達標情況。例如，在追蹤至完成的一組假設請求中，1,000 個請求抵達、700 個獲准進入、650 個在兩項延遲目標內完成，則：

$$
\text{admission fraction}=700/1000=70\%,\qquad
\text{SLO completion fraction}=650/1000=65\%.
$$

只看獲准請求的成功比例，則為 $650/700\approx92.9\%$；它回答的問題不同於所有抵達請求的成功比例。若要報告速率，還需說明測量期間及未完成請求的處理方式。這些比例不是 Mooncake 的結果，而是用來解釋：僅有已接受請求的高成功百分比，無法證明服務容量更大。

## 結果與解讀方式

論文將 Mooncake 與實驗使用的 vLLM 基準比較。端到端評估採用具有 LLaMA2-70B 架構的替代模型；每個節點搭載八張 A800 80-GB GPU，並使用高頻寬 RDMA 網路。[^evaluation]

| 論文報告的比較 | 範圍與解讀 |
|---|---|
| 吞吐量最多增加 525% | 特定模擬長上下文情境，且受 TTFT/TBT 限制；增加 525% 代表基準的 $1+5.25=6.25$ 倍。 |
| 符合 SLO 的請求約多 75% | 以真實請求軌跡重播，10 個預填充加 10 個解碼執行個體，對比 20 個 vLLM 執行個體；限制為 TTFT 30 秒與 TBT 0.1 秒。 |

摘要將後者描述為讓 Kimi 處理更多請求。第 8.1.3 節提供的是重播實驗，不應將其理解為獨立測得、可普遍套用的線上正式環境加速倍數。這兩個數字都沒有把前綴重用的效果，與階段分離、排程及特定基準的效果隔離。第 8.2 節另以過載實驗比較准入策略，並非產生 525% 主要數字的實驗。[^evaluation]

## 限制與實務檢查

- **重用隨工作負載而變。** 測量前綴覆蓋、淘汰與冷啟動行為。共享較少會減少重用機會，但不代表分離架構的所有潛在好處都消失。
- **搬移可能成為主因。** 同時分析快取傳輸頻寬、競爭與預填充時間。儲存更多前綴不保證 TTFT 更低。
- **預測可能出錯。** 輸出長度分布改變時，統一時長估計可能失準。除了資源池利用率，也應檢視延後拒絕與浪費的預填充。
- **快取身分與隔離需謹慎處理。** 部署時，應將重用限定於相容的模型狀態與執行設定，並落實租戶權限。前綴雜湊相符本身不是存取控制政策。

這些是評估與部署時的檢查項目，並非聲稱論文已證明所有這類條件都安全。

## 關聯

[Splitwise](splitwise.md) 研究階段分離與硬體配置；[DistServe](distserve.md) 針對延遲受限的有效吞吐量，最佳化資源分配、平行策略與放置。[^splitwise][^distserve] Mooncake 在此設計空間中加入分散式前綴狀態管理與過載准入。

[PagedAttention 與 vLLM](paged-attention.md) 處理 KV 記憶體分配與共享；分頁本身不決定分散式快取放置政策。[^paged] Orca 的迭代層級排程說明批次如何在生成迭代之間改變，與決定是否接受整個請求是不同層面的問題。[^orca]

[^mooncake]: Qin 等人（2024，2026 年修訂），《Mooncake》，摘要及第 1–3 節；下方連結指向第 5 版。
[^workflow]: Qin 等人，《Mooncake》，第 2–3 節與第 5.2 節：延遲指標、與前綴相關的區塊雜湊、增量預填充、逐層搬移及解碼准入複查。
[^scheduling]: Qin 等人，《Mooncake》，第 6 節：快取感知放置與熱點平衡。
[^overload]: Qin 等人，《Mooncake》，第 7.2–7.4 節：延遲的負載回饋與系統層級預測。
[^evaluation]: Qin 等人，《Mooncake》，第 8.1–8.2 節：測試環境、模擬工作負載、真實軌跡重播及獨立的准入策略實驗。
[^splitwise]: Patel 等人（2023），《Splitwise》，摘要；連結見下方。
[^distserve]: Zhong 等人（2024），《DistServe》，摘要；連結見下方。
[^paged]: Kwon 等人（2023），《PagedAttention》，摘要；連結見下方。
[^orca]: Yu 等人（2022），《Orca》，摘要；連結見下方。

## 參考文獻

### 重要論文

- Qin, R. et al. (2024; revised 2026). *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. arXiv:2407.00079v5. https://arxiv.org/html/2407.00079v5 — 主要架構論文，詳述分散式前綴重用、排程、過載預測與評估條件。
- Zhong, Y. et al. (2024). *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*. arXiv:2401.09670. https://arxiv.org/abs/2401.09670 — 說明在延遲限制下，針對各階段進行資源分配與放置。
- Patel, P. et al. (2023). *Splitwise: Efficient generative LLM inference using phase splitting*. arXiv:2311.18677. https://arxiv.org/abs/2311.18677 — 研究提示與生成使用獨立機器，以及硬體配置的取捨。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 說明分頁式 KV 分配，以及請求內和請求間的共享。
- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 提出用於自回歸生成的迭代層級排程與選擇性批次。
