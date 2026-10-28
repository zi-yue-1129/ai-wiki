---
translation_reviewed: 2026-10-28
---

# FlashAttention

FlashAttention 計算精確的縮放點積注意力，並大幅減少與高頻寬記憶體之間的資料流量。它不近似注意力矩陣。它把計算切分成區塊，使查詢、鍵與值的區塊留在快速的晶片上記憶體中，並且從不把完整的 \(n \times n\) 分數矩陣寫到較慢的記憶體。Dao 等人（2022）提出此方法，後續版本改善了平行性，並更善用新世代的 GPU。它是 [IO 感知](../index.zh-TW.md)精確注意力的標準例子，與[注意力變體](../index.zh-TW.md)總覽中的其他家族並列。

## 問題

標準注意力計算分數矩陣 \(S = QK^\top / \sqrt{d}\)，對每一列套用 softmax，再乘上 \(V\)。對長度為 \(n\) 的序列，這個矩陣有 \(n^2\) 個元素。在 GPU 上，把它寫入與讀出高頻寬記憶體的時間，超過運算本身，因此注意力受記憶體流量限制，而非受 FLOPs 限制，正如[記憶體階層](../../../../../engineering/hardware/memory-hierarchy/index.zh-TW.md)頁所說明的。

## 核心想法

把 \(Q\)、\(K\) 與 \(V\) 切成能放進晶片上 SRAM 的區塊。對每一個查詢區塊，串流掃過各個鍵與值的區塊，計算部分分數，並在每個區塊到達時更新輸出。softmax 以增量方式計算，因此完整的分數列從未同時存在於記憶體中。在反向傳播時，此方法會重算它沒有儲存的分數，以少量額外運算換取大幅減少的記憶體流量。

## 公式或演算法

對一個查詢列，令執行中的最大值為 \(m\)，執行中的正規化項為 \(\ell\)。當一個新的分數區塊 \(s\) 到達時，更新為

\[
m' = \max(m, \max(s)), \qquad
\ell' = e^{m - m'}\,\ell + \sum e^{s - m'}
\]

部分輸出在加入新區塊的貢獻前，以同一個因子 \(e^{m - m'}\) 重新縮放。最終輸出與標準的 softmax 注意力完全相等，因為縮放使每一項都相對於最終的最大值。softmax 的增量形式沿用 Milakov 與 Gimelshein（2018）所描述的執行正規化技巧。

注意力輸出與統計量所需的記憶體為 \(O(n)\)，而非 \(O(n^2)\)；運算量仍為 \(O(n^2 d)\)。

## 結果

Dao 等人（2022）報告，此方法比標準的精確注意力更快，且使用較少記憶體，輸出相同。FlashAttention-2（Dao，2023）報告其速度約為原版的兩倍，並達到 A100 理論峰值 FLOPs 每秒的約 50% 至 73%。FlashAttention-3（Shah 等人，2024）報告在 H100 GPU 上注意力快 1.5 至 2 倍，FP16 約達每秒 740 TFLOPs，FP8 則接近每秒 1.2 PFLOPs。

## 限制

此方法是精確的，因此其時間複雜度仍為 \(O(n^2)\)。Rabe 與 Staats（2021）顯示精確注意力可以用 \(O(\log n)\) 的記憶體計算，但該界限仍需要二次方的時間，因此長序列仍然昂貴。核心程式是為特定的 GPU 架構撰寫的，每一世代都需要新的工作。收益也取決於序列長度、頭維度與批次大小，因此某一組設定下的基準數字無法直接套用到另一組。

## 開放問題與相關變體

- **長上下文成本。** 精確注意力的時間仍是二次方。稀疏或線性變體能否在序列變長時維持品質，取決於任務，見[注意力變體](../index.zh-TW.md)總覽。
- **低精度。** FlashAttention-3 在新硬體上使用 FP8。低精度在各類任務上的準確度代價仍是開放問題，這也與[協同設計](../../../../../engineering/hardware/co-design/index.zh-TW.md)的取捨有關。
- **解碼。** 生成時，每一步讀取的是整個 [KV 快取](../../kv-cache/index.zh-TW.md)，而非計算大型分數矩陣，因此 FlashAttention 對預填階段的幫助大於對單一 token 解碼的幫助。
- **相關：** [KV 快取](../../kv-cache/index.zh-TW.md)與共享頭的設計處理的是另一種成本，即鍵與值的記憶體，而非分數矩陣的流量。

## 相關連結

FlashAttention 是對[記憶體階層](../../../../../engineering/hardware/memory-hierarchy/index.zh-TW.md)頁中分析的記憶體受限行為的軟體解法。它展示了核心程式如何在不改變模型的情況下改變屋頂線模型中的位元組項，這與[協同設計](../../../../../engineering/hardware/co-design/index.zh-TW.md)頁的邏輯相同。

## 參考文獻

### 開創性論文

- Dao, T., 等人 (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — 具分塊與 IO 感知能力的精確注意力，避免把分數矩陣寫入高頻寬記憶體。
- Dao, T. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. arXiv:2307.08691. https://arxiv.org/abs/2307.08691 — 透過更好的 GPU 執行緒平行性，報告速度約為原版的兩倍。
- Shah, J., 等人 (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision*. arXiv:2407.08608. https://arxiv.org/abs/2407.08608 — 報告在 H100 GPU 上注意力快 1.5 至 2 倍，包括 FP8 核心。

### 綜述與教科書

（本頁尚未查核任何項目）

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Rabe, M. N., Staats, C. (2021). *Self-attention Does Not Need O(n²) Memory*. arXiv:2112.05682. https://arxiv.org/abs/2112.05682 — 顯示精確的自注意力可以用對數記憶體計算，但時間仍為二次方。
- Milakov, M., Gimelshein, N. (2018). *Online normalizer calculation for softmax*. arXiv:1805.02867. https://arxiv.org/abs/1805.02867 — 以更新執行中的最大值與正規化項的方式，以較少的記憶體存取計算 softmax。
