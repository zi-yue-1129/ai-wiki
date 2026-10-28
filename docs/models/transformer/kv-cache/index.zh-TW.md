---
related:
- models/llm
- engineering/mlops
aliases:
  - KV Cache
  - Key-Value Cache
  - KV Cache Compression
  - KV 快取
  - 鍵值快取
tags:
  - KV cache
  - inference efficiency
  - LLM serving
translation_reviewed: 2026-10-28
---

# KV 快取管理

自回歸生成時，解碼器會儲存之前每個 token 的鍵與值，因此每個新 token 每層只需計算一組新的鍵與值。這個鍵值（KV）快取省下了重複的計算，但它的大小會隨序列長度、層數與頭數增長。對於長上下文與大量同時進行的請求，快取的記憶體用量常常超過模型權重本身。因此管理快取是[大型語言模型服務](../../llm/index.md)的核心問題。方法大致分為四類：記憶體如何配置、保留哪些 token、儲存的值如何壓縮，以及架構如何從一開始就減少需要儲存的量。

## 概觀

| 策略 | 回答的問題 | 例子 |
|---|---|---|
| 記憶體管理 | 快取區塊如何配置與共享？ | PagedAttention、前綴共享 |
| 淘汰 | 哪些 token 可以丟棄？ | H2O、Scissorhands、StreamingLLM、SnapKV |
| 量化 | 值可以用多少位元儲存？ | KIVI、KVQuant |
| 架構縮減 | 能否從一開始就儲存較少的值？ | MQA 與 GQA、多頭潛在注意力 |
| 卸載 | 快取可以放在哪裡？ | FlexGen |

## 做法

### 記憶體管理

vLLM 的 PagedAttention 把快取存成固定大小的區塊，並透過表格對映，類似虛擬記憶體。如此一來，請求不再需要一整塊連續的記憶體，大幅減少碎片，並讓共享同一提示前綴的請求可以共用區塊。Kwon et al.（2023）回報的服務吞吐量，明顯高於為每個請求預留記憶體的系統。

### 淘汰

淘汰會保留固定預算的 token，其餘丟棄。H2O 保留「重擊者」（heavy hitters），也就是累積獲得最多注意力的 token，外加最近的 token。Scissorhands 則保留重要性隨時間持續存在的 token。StreamingLLM 觀察到，前幾個 token 不論內容為何都會得到大量注意力；保留這些注意力沉點（attention sinks）加上最近的窗口，就能讓模型在很長的串流上運作，不需重新訓練。但它不保留遠處的內容，因此是穩定化方法，不是記憶方法。SnapKV 則利用提示末段的注意力，為每個頭決定要保留哪些較早的位置。

### 量化

量化快取是把每個值以較少位元儲存。困難在於鍵與值的統計特性不同。KIVI 不經調校，就把鍵以通道為單位、值以 token 為單位量化為兩位元。KVQuant 在套用旋轉嵌入之前量化鍵，使用非均勻的量化層級，並另外儲存少數離群值，因此能支援非常長的上下文。

### 架構縮減

[注意力變體](../attention-variants/index.md)中介紹的共享頭，可以減少儲存的頭數。DeepSeek-V2 引入的多頭潛在注意力則更進一步：鍵與值被壓縮成低維的潛在向量，只快取這個潛在向量，計算注意力時再重建鍵與值。這種縮減內建於訓練中，因此無法在訓練後任意套用到既有模型上。

### 卸載

FlexGen 把權重與快取在 GPU 記憶體、CPU 記憶體與磁碟之間移動，並安排傳輸來隱藏其成本。它的目標是單張 GPU 上的吞吐量而非延遲，因此適合批次推論。

## 取捨

- **品質與記憶體。** 淘汰與激進的量化都可能遺失後面 token 需要的資訊。平均來看損失通常很小，但在特定的檢索任務上可能很大。
- **架構與事後方法。** 架構縮減的節省可預測，但需要訓練新模型。淘汰與量化則可以套用在既有模型上。
- **延遲。** 卸載與某些壓縮方案每個 token 都會增加計算或傳輸，因此即使記憶體下降，生成仍可能變慢。
- **評估。** 結果取決於基準。保留摘要品質的方法，可能在「大海撈針」式的檢索上失敗。

## 相關連結

快取是[注意力](../attention-variants/index.md)的成本與硬體相遇之處。淘汰會與[位置編碼](../positional-encodings/index.md)互動，因為移除 token 會改變剩餘 token 的位置。使用這些方法的服務系統，在[MLOps 與部署](../../../engineering/mlops/index.md)中討論。

## 未解問題與更多變體

- **需要遠距細節的任務。** 淘汰方法保留近期與重要的 token，因此可能遺失長輸入中早先只提過一次的事實。依需求取回被淘汰項目的方法是一種回應，但會增加延遲。
- **查詢感知的選擇。** 大多數淘汰決策是在知道問題之前，或只依據短的觀察窗口做出的。根據查詢來選擇 token 是一個開放方向。
- **離群值與低位元。** 量化到四位元以下，仍對離群通道敏感；鍵與值的離群值處理方式也不同。
- **跨請求共享。** 當提示重複時，前綴快取有效。如何在不同使用者之間共享並壓縮快取、又不洩漏資訊，發展較少。
- **學習式壓縮。** MLA 這類潛在壓縮是在訓練中學成的。如何用很少的運算，為既有模型學習一個壓縮器，仍是開放問題。
- **推測解碼與多 token 解碼。** 這些解碼方法如何與快取淘汰與壓縮互動，大多尚未研究。

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv:1706.03762 — 定義多頭注意力，其鍵與值在生成時被快取。
- Kwon, W., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention". SOSP 2023. arXiv:2309.06180 — KV 快取的分頁配置，是 vLLM 的基礎。
- Zhang, Z., et al. (2023). "H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models". arXiv:2306.14048 — 保留累積注意力最大 token 的淘汰方法。
- Xiao, G., et al. (2024). "Efficient Streaming Language Models with Attention Sinks". ICLR 2024. arXiv:2309.17453 — 以注意力沉點加上近期窗口，達成穩定的串流生成。
- Liu, Z., et al. (2024). "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache". arXiv:2402.02750 — 兩位元快取量化，鍵與值採用不同方案。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2023). "Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time". arXiv:2305.17118 — 依重要性持續存在的 token 進行淘汰。
- Li, Y., et al. (2024). "SnapKV: LLM Knows What You are Looking for Before Generation". arXiv:2404.14469 — 利用提示末段的觀察窗口，為每個頭選擇要保留的前綴 token。
- Hooper, C., et al. (2024). "KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization". arXiv:2401.18079 — 在旋轉嵌入之前量化鍵，使用非均勻層級並處理離群值。
- DeepSeek-AI (2024). "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model". arXiv:2405.04434 — 多頭潛在注意力，快取壓縮後的潛在向量而非完整的鍵與值。
- Sheng, Y., et al. (2023). "FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU". arXiv:2303.06865 — 以排程的傳輸，把權重與快取卸載到 GPU、CPU 與磁碟之間。
