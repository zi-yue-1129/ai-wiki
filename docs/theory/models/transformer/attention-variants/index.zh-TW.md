---
related:
- theory/models/llm
aliases:
  - Attention Variants
  - Efficient Attention
  - 注意力變體
  - 高效注意力
tags:
  - attention
  - efficient inference
  - long context
translation_reviewed: 2026-10-28
---

# 注意力變體

標準的縮放點積注意力，其時間與記憶體成本都是序列長度 \(n\) 的 \(O(n^2)\)。訓練時，這會限制上下文長度；生成時，每個新 token 都要讀取龐大的[鍵值快取](../kv-cache/index.md)。多數注意力變體針對三種成本之一：需要儲存的鍵值頭數、需要計算的查詢–鍵配對數，或精確計算所需的記憶體傳輸量。本頁介紹會改變注意力計算本身的變體；位置編碼的選擇見[位置編碼](../positional-encodings/index.md)。

## 概觀

| 家族 | 減少的項目 | 例子 | 改變後的成本 |
|---|---|---|---|
| 共享頭 | 鍵值快取大小 | MQA、GQA | 計算相同，記憶體較少 |
| 稀疏或局部模式 | 查詢–鍵配對數 | Sparse Transformer、Longformer、滑動窗口 | 約 \(O(n\sqrt{n})\) 或 \(O(nw)\) |
| 線性注意力 | softmax 的使用 | 線性 Transformer、Performers | \(O(n)\)，為近似 |
| IO 感知的精確注意力 | 記憶體傳輸 | FlashAttention | 結果相同，記憶體與時間較少 |

## 做法

### 共享的鍵與值頭

在多頭注意力中，每個頭都有自己的鍵與值。多查詢注意力（MQA）讓所有查詢頭共用一組鍵與值，因此鍵值快取會縮小為頭數的倒數。分組查詢注意力（GQA）則是在查詢頭的群組內共享鍵與值，介於完整多頭與多查詢之間。GQA 可以透過一段短暫的額外訓練，把既有的多頭檢查點轉換而成，這也是許多開源模型採用它的原因。

### 稀疏與局部模式

稀疏注意力不讓每個查詢都看所有較早的 token，而是限制在固定模式內。Sparse Transformer 使用跨步與固定模式，能看得很遠，同時讓成本接近 \(O(n\sqrt{n})\)。Longformer 結合滑動窗口與少數全域 token，成本與 \(n\) 呈線性。Mistral 7B 使用固定窗口的滑動窗口注意力，資訊仍能隨層數擴散，因為每一層都把資訊向前傳遞一個窗口。局部模式很快，但除非有其他機制，否則無法檢索任意的遠距 token。

### 線性注意力

線性注意力以核特徵映射 \(\phi\) 取代 softmax，使乘積可以重排為 \(\phi(Q)\,(\phi(K)^\top V)\)。項 \(\phi(K)^\top V\) 可以累積成一個遞迴狀態，讓注意力變成每個 token 成本固定的循環更新。Katharopoulos et al.（2020）展示了這個等價關係及其自回歸形式。Performers 則用隨機特徵（FAVOR+）近似 softmax 核，使用的特徵越多，近似就越準確。

### IO 感知的精確注意力

FlashAttention 計算的結果與標準注意力完全相同，同時減少記憶體流量。它有獨立的頁面，見 [FlashAttention](flash-attention/index.zh-TW.md)，內容包括其演算法、結果與後續版本。這一類是精確的注意力，與上面的近似方法相對。

## 取捨

- **精確與近似。** 共享頭與 FlashAttention 保留精確的注意力計算。稀疏、線性與隨機特徵方法改變了計算的內容，其品質取決於任務。
- **檢索能力。** 壓縮或限制上下文的方法可能遺失特定的遠距 token。需要從長輸入中檢索單一事實的任務，最能暴露這種損失。
- **硬體。** 速度取決於核心實作與記憶體佈局。省下運算量的變體，在某些加速器上不一定省時間。
- **訓練與推論。** 有些變體可以在訓練與推論中都使用，有些只能在推論時轉換後使用，這會影響實驗的成本。

## 相關連結

這些變體是長上下文[大型語言模型](../../llm/index.md)背後的主要工具。共享頭與潛在注意力所減少的快取，在[KV 快取管理](../kv-cache/index.md)中討論。完全不用注意力的替代架構（例如狀態空間模型）則在 [Transformers & Attention](../index.md) 總覽頁中介紹。

## 未解問題與更多變體

- **檢索差距。** 線性與狀態空間模型效率高，但在從長輸入中精確回想細節時，通常不如注意力。混合架構（少數完整注意力層搭配高效層）是一種回應，但最佳比例尚無定論。
- **學習式稀疏。** 大多數稀疏模式是人工固定的。學習該關注哪些 token（例如透過路由或 top-k 選擇）很有潛力，但比較難訓練。
- **頭的配置。** GQA 中鍵值群組的數量通常靠試驗決定。缺少一個能依品質與記憶體預算來設定的原則性方法。
- **核設計。** 線性注意力的特徵映射大多是人工設計的，其對 softmax 的近似誤差只在簡單情況下被充分理解。
- **長上下文評估。** 用來測試注意力變體能否在極長輸入中保留資訊的基準仍不一致。

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv:1706.03762 — 提出縮放點積與多頭注意力，是本頁所有變體的基準。
- Shazeer, N. (2019). "Fast Transformer Decoding: One Write-Head is All You Need". arXiv:1911.02150 — 多查詢注意力，所有查詢共用一個鍵值頭。
- Ainslie, J., et al. (2023). "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints". arXiv:2305.13245 — 分組查詢注意力，從多頭檢查點轉換而來。
- Child, R., et al. (2019). "Generating Long Sequences with Sparse Transformers". arXiv:1904.10509 — 因式分解的稀疏注意力模式，成本接近 \(O(n\sqrt{n})\)。
- Beltagy, I., Peters, M. E. & Cohan, A. (2020). "Longformer: The Long-Document Transformer". arXiv:2004.05150 — 結合全域 token 的滑動窗口注意力，用於長文件。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Katharopoulos, A., et al. (2020). "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention". ICML 2020. arXiv:2006.16236 — 線性注意力，並具有快速自回歸解碼的循環形式。
- Choromanski, K., et al. (2020). "Rethinking Attention with Performers". arXiv:2009.14794 — 以隨機特徵近似 softmax 注意力（FAVOR+）。
- Dao, T., et al. (2022). "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness". arXiv:2205.14135 — 分塊、IO 感知的精確注意力。
- Dao, T. (2023). "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning". arXiv:2307.08691 — 改善 FlashAttention 的平行性與工作分配。
- Jiang, A. Q., et al. (2023). "Mistral 7B". arXiv:2310.06825 — 在廣泛使用的開源模型中採用滑動窗口注意力。
