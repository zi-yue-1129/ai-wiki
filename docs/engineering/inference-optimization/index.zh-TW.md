# 推論最佳化

推論最佳化是一組讓已訓練模型回答更快、每張 GPU 能服務更多使用者、且每個 token 成本更低的技術。對大型語言模型而言，瓶頸通常不在運算，而在記憶體：每生成一個 token，都要讀取模型權重，以及之前所有 token 已快取的 key 與 value。

## 概述

模型只訓練一次，卻會被服務數百萬次，因此服務效率的小幅提升會不斷累積。推論分成兩個階段，硬體需求差異很大：

- **預填充（prefill）** 會平行處理整段提示。它受算力限制，因為許多 token 共用同一次權重讀取。
- **解碼（decoding）** 一次只產生一個 token。它受記憶體頻寬限制，因為每一步都要讀取完整權重，以及該 token 之前整個 [KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)。

多數技術針對其中一個階段，而且許多技術需要在延遲與吞吐量之間取捨。

## 關鍵概念

- **延遲與吞吐量**：對聊天服務而言，首 token 時間與每個輸出 token 的時間很重要；對成本而言，每張 GPU 每秒產生的 token 數很重要。批次處理能提高吞吐量，但可能拖慢個別請求。
- **算術強度與屋線模型（roofline）**：浮點運算量與搬移位元組數的比值。一個核心函式的效能上限，取決於峰值算力或記憶體頻寬哪一個先到達。參見[記憶體階層與頻寬](../hardware/index.md)。
- **KV 快取**：儲存 key 與 value，避免重新計算提示上的注意力。其大小隨序列長度、批次大小與層數成長，因此常是單一裝置能容納多少請求的限制。
- **連續（逐迭代）批次處理**：某個請求結束後，新請求會立刻加入執行中的批次，而不是等整批結束。
- **量化**：以較少位元儲存權重或激活值，以減少記憶體流量。方法見 [MLOps 與部署](../mlops/index.zh-TW.md)，以及[工程總覽](../index.zh-TW.md)連結的模型壓縮內容。

## 運作方式

典型的服務系統會疊加數個層次：

```mermaid
flowchart TD
  R[請求] --> S[排程器：連續批次處理]
  S --> M[記憶體管理：分頁式 KV 快取]
  M --> K[核心函式：融合注意力、量化矩陣乘法]
  K --> D[解碼：取樣或推測式驗證]
  D --> O[串流輸出 token]
```

排程器決定每一步執行哪些請求。記憶體管理器決定它們的 KV 快取放在哪裡。核心函式決定每一步在硬體上跑多快。解碼階段則決定每一步產生多少 token。

## 關鍵方法

### Orca：逐迭代排程（Yu et al., 2022）

- **問題**：靜態批次處理要等批次中最長的請求結束，短請求完成後 GPU 會閒置。
- **核心想法**：以單次模型迭代為排程單位。結束的請求在迭代之間離開，等待中的請求則加入。
- **方程式或演算法**：每次迭代對目前活躍的請求集合執行一次模型；選擇性批次處理會把可共用的計算合併，並對每個請求個別處理注意力。
- **結果**：論文指出，在相近延遲下，相較於以請求為單位的批次處理，生成式 GPT 類模型的吞吐量大幅提升。
- **限制**：排程器必須處理長短不一的序列，記憶體碎片問題仍然存在，這是下一個方法要解決的。

### PagedAttention 與 vLLM（Kwon et al., 2023）

- **問題**：KV 快取以為最大序列長度預留的連續緩衝區儲存，大部分記憶體因碎片與過度預留而浪費。
- **核心想法**：把 KV 快取切成固定大小的區塊，類似虛擬記憶體的分頁，並依需求把每個請求的邏輯區塊對應到實體區塊。具有共同前綴的請求可以共用區塊。
- **方程式或演算法**：注意力核心透過區塊表讀取 key 與 value，因此一個序列的區塊在記憶體中不需要連續。
- **結果**：論文指出，在相近延遲下，吞吐量高於既有服務系統，記憶體浪費也降到很小的比例。
- **限制**：區塊查找會增加核心複雜度，效益也取決於工作負載有多少前綴共用。

### 推測式解碼（Leviathan et al., 2023）

- **問題**：每次完整前向傳播只產生一個 token，會讓大模型受記憶體限制且利用率偏低。
- **核心想法**：一個小而便宜的草稿模型先提出數個 token，再由大型目標模型一次平行檢查全部。被接受的 token 保留，第一個被拒絕的 token 則以修正後的取樣替換。
- **方程式或演算法**：草稿 token $x$ 的草稿機率為 $q(x)$，以機率 $\min\!\left(1, \frac{p(x)}{q(x)}\right)$ 被接受，其中 $p$ 為目標分布。被拒絕時，從 $\mathrm{norm}\big(\max(0, p - q)\big)$ 取樣。如此輸出分布與目標模型完全相同。
- **結果**：論文指出，在 T5-XXL 的翻譯與摘要任務上，解碼速度快 2 至 3 倍，且輸出分布不變。
- **限制**：加速幅度取決於草稿與目標相符的頻率。Medusa 與 EAGLE 等不需獨立草稿模型的變體，則以額外訓練換取這項效益。

### 多查詢與分組查詢注意力（Shazeer, 2019；Ainslie et al., 2023）

- **問題**：多頭注意力中每個頭各自保存 key 與 value，KV 快取很大，每一步解碼都要讀取大量記憶體。
- **核心想法**：讓多個查詢頭共用 key 與 value。多查詢注意力只用一組 key-value 頭；分組查詢注意力則使用少量分組，在品質與記憶體之間取得平衡。
- **方程式或演算法**：若有 $H$ 個查詢頭與 $G$ 個 key-value 分組，快取大小隨 $G$ 而非 $H$ 成長。
- **結果**：Ainslie et al. 指出，多頭檢查點可以用原始預訓練算力的一小部分轉換為分組查詢模型，品質接近多頭注意力。
- **限制**：key-value 頭變少會降低模型容量，在需要多樣注意力模式的任務上，品質可能下降。

## 相關連結

- KV 快取本身的說明見 [Transformer KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)；本頁說明服務系統如何管理它。
- 硬體限制，例如記憶體頻寬與互連，決定了這裡每項技術的上限，見 [AI 硬體](../hardware/index.md)。
- 部署相關議題，包括監控、成本與上線，見 [MLOps 與部署](../mlops/index.zh-TW.md)。
- 權重量化與剪枝會改變模型本身，其與服務端方法的比較見模型壓縮相關內容。

## 應用

- **聊天服務**：連續批次處理與分頁記憶體，讓單張 GPU 能同時服務大量使用者。
- **程式碼補全**：延遲最重要，因此推測式解碼與小型草稿模型很常見。
- **長文件問答**：KV 快取記憶體佔主導，因此促成分組查詢注意力與快取淘汰策略。
- **裝置端助理**：量化權重與小型模型能符合嚴格的記憶體預算，此時頻寬與功耗限制比吞吐量更關鍵。

## 開放問題

- **長上下文**：快取隨長度線性成長。H2O 與 StreamingLLM 等淘汰策略會丟棄 token，可能損害需要被丟棄內容的任務。
- **混合工作負載**：把預填充與解碼一起排程，可能拖慢解碼。分塊預填充是一種解法，但最佳策略取決於服務的延遲目標。
- **更多變體**：硬體專用核心、預填充與解碼分離的伺服器、稀疏或檢索式注意力，各自在準確度、記憶體與工程成本之間有不同取捨。
- **量測**：吞吐量與延遲高度依賴批次形狀與提示組合，因此已發表的數字難以直接比較。

## 參考文獻

### 奠基性論文

- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 提出逐迭代排程，是現代服務系統連續批次處理的基礎。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 說明分頁式 KV 快取管理與 vLLM 服務系統。
- Leviathan, Y., Kalman, M. & Matias, Y. (2023). *Fast Inference from Transformers via Speculative Decoding*. ICML 2023. https://arxiv.org/abs/2211.17192 — 證明草稿與驗證式解碼能在降低延遲的同時，保留目標模型的輸出分布。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — 以分塊計算精確注意力，減少對 GPU 慢速記憶體的讀寫。
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need*. https://arxiv.org/abs/1911.02150 — 提出多查詢注意力，讓所有查詢共用一組 key 與 value 頭，以縮小解碼時的快取。

### 綜述與擴展相關論文

- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023. https://arxiv.org/abs/2305.13245 — 說明如何以少量額外訓練，把多頭檢查點轉換為分組查詢注意力。
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — 分析如何把模型切分到多顆晶片上，以平衡延遲敏感與吞吐導向推論的計算與記憶體。

### 文章與文件

- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — 定義屋線模型，把算術強度與記憶體頻寬、峰值算力關聯起來。
- vLLM project. *vLLM documentation*. https://docs.vllm.ai/ — 開源引擎中分頁注意力、連續批次處理與量化服務的實務參考。
