---
translation_reviewed: 2026-10-28
---

# 混合精度訓練與梯度檢查點

混合精度訓練讓網路的大部分運算以 16 位元或 8 位元浮點格式進行，並在準確度依賴之處保留一份全精度的權重。梯度檢查點則在前向傳播中丟棄中間結果，改在反向傳播時重新計算，藉此降低激活值所佔用的記憶體。

## 概述

訓練受限於兩項資源：運算單元的速度，以及每個加速器上的記憶體。混合精度縮小每個數字的位元數，因此運算更快、儲存的張量也更小。檢查點則是少存一些、多算一些。大型訓練通常會同時使用兩者。它們都不是[訓練與微調總覽](index.zh-TW.md)中所說的「檢查點」，後者指將模型狀態存到磁碟，以便訓練在失敗後能夠續行。

## 關鍵概念

- **浮點格式**：由符號、指數與尾數組成。指數決定可表示的數值範圍，尾數決定精度。FP32 有 8 個指數位元與 23 個尾數位元，FP16 為 5 與 10，BF16 為 8 與 7。
- **主權重**：參數的全精度副本，由最佳化器更新。運算時使用的低精度副本便是由它四捨五入而來。
- **損失縮放**：反向傳播前將損失乘以一個常數，使小梯度不致下溢為零；更新前再將梯度除以同一個常數。
- **激活值**：每一層的中間輸出，反向傳播需要它們。在大批次與長序列的情況下，激活值往往是最大的記憶體成本。
- **重新計算**：在反向傳播時重新執行部分前向傳播，以重建未被儲存的激活值。

## 運作方式

### 混合精度

典型的做法是讓矩陣乘法以低精度輸入，並在 FP32 中累加。最佳化器更新 FP32 主權重，然後轉回低精度，供下一次前向傳播使用。Micikevicius 等人於 2017 年為 FP16 提出此流程，並加入主權重與損失縮放兩項設計。[^1]

FP16 的指數範圍較窄，會使小梯度變成零，因此需要損失縮放。BF16 保留了 FP32 的指數範圍，犧牲的是尾數位元，因此通常不需要損失縮放。Kalamkar 等人發現，在多個領域中，BF16 訓練都能與 FP32 的結果相當，且不需更動超參數。

FP8 每個值使用 8 位元，有兩種編碼：E4M3（4 個指數位元、3 個尾數位元）與 E5M2（5 與 2）。其範圍非常小，因此每個張量都要乘上一個尺度 $s$，使其最大值能落在格式範圍內：

$$
s = \frac{x^{\max}_{\text{FP8}}}{\max_i |x_i|}
$$

後續研究將 FP8 擴展到最佳化器狀態與整個 LLM 訓練流程，並指出不穩定性可能只會在長時間訓練後才出現。[^4]

### 記憶體計算

混合精度並不會縮減所有項目。對於以 Adam 訓練的參數，混合精度流程中的靜態狀態如下：

| 項目 | 格式 | 每個參數的位元組數 |
|---|---|---|
| 運算所用的權重 | FP16 或 BF16 | 2 |
| 梯度 | FP16 或 BF16 | 2 |
| 主權重 | FP32 | 4 |
| Adam 的一階與二階動量 | FP32 | 8 |
| **合計（不含激活值）** | | **16** |

純 FP32 的 Adam 每個參數同樣需要 16 位元組。因此節省的記憶體主要來自激活值（以低精度儲存）以及更快的運算。縮減靜態狀態則是另一個問題，其解法是把它分片到各個裝置上，[ZeRO](../distributed-training/zero.zh-TW.md) 便是如此處理。

### 梯度檢查點

標準的反向傳播會儲存每一層的激活值，因此記憶體隨深度 $n$ 增長。檢查點只保留選定段落的輸入，其餘丟棄。反向傳播時，每一段都會從其儲存的輸入重新執行前向傳播，然後再進行反向傳播。

```mermaid
flowchart LR
    f1[前向：第 1 段] --> k1[(第 2 段的已儲存輸入)]
    k1 --> f2[前向：第 2 段] --> k2[(第 3 段的已儲存輸入)]
    k2 --> f3[前向：第 3 段] --> loss[損失]
    loss --> b3[重新計算第 3 段，再反向傳播]
    k2 -.-> b3
    b3 --> b2[重新計算第 2 段，再反向傳播]
    k1 -.-> b2
```

若每隔約 $\sqrt{n}$ 層設置一個檢查點，便約只需儲存 $\sqrt{n}$ 個激活值，代價是每個小批次多一次前向傳播。[^5] Griewank 與 Walther 更早就為反向模式自動微分推導出排程，其最佳性是可證明的，但取決於所列出的準則。

重新計算整層會重複執行昂貴的矩陣乘法。Korthikanti 等人則只重新計算每個 Transformer 層中較便宜的部分，並結合序列平行化。在他們的設定中，這使激活值記憶體降為約五分之一，並大幅降低重新計算的額外開銷。[^7]

## 主要方法

| 方法 | 節省什麼 | 代價 | 來源 |
|---|---|---|---|
| 搭配損失縮放的 FP16 混合精度 | 激活值與梯度的記憶體；矩陣乘法更快 | 損失縮放；指數範圍窄 | Micikevicius 等人（2017） |
| BF16 混合精度 | 同 FP16，通常不需損失縮放 | 尾數位元比 FP16 少 | Kalamkar 等人（2019） |
| FP8 訓練 | 進一步節省儲存與頻寬 | 逐張量縮放；長時間訓練的不穩定性 | Micikevicius 等人（2022）；Peng 等人（2023）；Fishman 等人（2024） |
| 梯度檢查點 | 激活值記憶體，降至約 $\sqrt{n}$ | 多一次前向傳播 | Chen 等人（2016） |
| 選擇性重新計算 | 激活值記憶體，在其設定中約為五分之一 | 需決定要重新計算哪些運算 | Korthikanti 等人（2022） |

## 相關連結

[LoRA](peft-lora.zh-TW.md) 凍結了大部分權重，因此只有小型適配器需要梯度與最佳化器狀態。關於訓練後的精度，請見[訓練後量化](../../theory/model-compression/quantisation/post-training/index.zh-TW.md)；[混合精度量化](../../theory/model-compression/quantisation/mixed-precision/index.zh-TW.md)頁面使用相同的詞來指為每一層選擇位元寬度，那是另一個問題。晶片支援哪些格式，請見 [AI 硬體](../hardware/index.zh-TW.md)。Dao 等人的 FlashAttention 則在注意力核心內部，以分塊計算的方式套用相同的記憶體流量邏輯。

大腦的連結比較寬鬆。生物神經元並不使用 16 位元浮點數進行運算，它們的訊號稀疏且由事件驅動，[脈衝神經網路](../../brain-mind/snn-neuromorphic/index.zh-TW.md)正是利用這個概念來追求能源效率。一個脈衝是時間上的二元事件，而不是某種格式中的數字。大腦在學習時是否保存類似完整的激活歷史，目前並不清楚；許多受生物啟發的學習規則則不需要這樣的記錄。

## 應用

- 大型語言模型通常以 BF16 混合精度進行預訓練，部分近期的訓練則使用 FP8。[^4]
- 長序列訓練中激活值佔主導地位，依賴檢查點與選擇性重新計算。

## 開放問題

- **長時間訓練的穩定性。** Fishman 等人將 FP8 的不穩定性追溯到 SwiGLU，並提出 Smooth-SwiGLU 加以處理。這類修正能否推廣到其他架構，目前並不清楚。
- **最佳的檢查點位置。** Jain 等人使用現成的 MILP 求解器來解決重新計算的排程問題，並回報可訓練的輸入大小最多可放大 5.1 倍。[^8] 最佳排程是否值得其規劃成本，是工程上的判斷。
- **最佳化器狀態的更低精度。** Peng 等人與 Fishman 等人在特定設定下，將梯度與 Adam 動量量化為 FP8。這種做法能否延伸到各種規模與任務，尚待研究。

[^1]: Micikevicius 等人（2017）回報，這些技術使深度學習模型的記憶體用量降低近兩倍。
[^4]: Peng 等人（2023）回報，在 H100 GPU 上訓練 GPT-175B 時，相較於 BF16 的 Megatron-LM 基準，記憶體用量降低 39%、速度提高 75%；此數字為作者所測得。Fishman 等人（2024）則以最多兩兆 token 進行訓練。
[^5]: Chen 等人（2016）回報，對一個 1,000 層的殘差網路，記憶體由 48 GB 降至 7 GB，而運行時間約增加 30%。
[^7]: Korthikanti 等人（2022）回報，激活值記憶體減少為五分之一，重新計算的額外開銷減少逾 90%。
[^8]: Jain 等人（2019）回報，Checkmate 可使實際網路的輸入大小放大至多 5.1 倍。

## 參考文獻

### 開創性論文

- Micikevicius, P. 等人 (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — 提出以半精度訓練深度網路時所用的 FP32 主權重與損失縮放。
- Kalamkar, D. 等人 (2019). *A Study of BFLOAT16 for Deep Learning Training*. arXiv:1905.12322. https://arxiv.org/abs/1905.12322 — 實證研究，顯示 BF16 訓練在多個領域都與 FP32 結果相當。
- Micikevicius, P. 等人 (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — 定義 E4M3 與 E5M2 兩種 FP8 格式，並在訓練任務上進行測試。
- Chen, T. 等人 (2016). *Training Deep Nets with Sublinear Memory Cost*. arXiv:1604.06174. https://arxiv.org/abs/1604.06174 — 以重新計算被丟棄的激活值，換取記憶體隨網路深度呈次線性增長。
- Griewank, A. & Walther, A. (2000). *Algorithm 799: revolve*. ACM Transactions on Mathematical Software. https://doi.org/10.1145/347837.347846 — 提出反向模式微分的檢查點排程，在所列準則下可證明為最佳。
- Rajbhandari, S. 等人 (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — 將最佳化器狀態、梯度與參數分片到各個裝置上。
- Korthikanti, V. 等人 (2022). *Reducing Activation Recomputation in Large Transformer Models*. arXiv:2205.05198. https://arxiv.org/abs/2205.05198 — 為大型 Transformer 提出選擇性激活重新計算，並結合序列平行化。
- Jain, P. 等人 (2019). *Checkmate: Breaking the Memory Wall with Optimal Tensor Rematerialization*. arXiv:1910.02653. https://arxiv.org/abs/1910.02653 — 將重新計算表述為最佳化問題，並以 MILP 求解器求解訓練排程。
- Peng, H. 等人 (2023). *FP8-LM: Training FP8 Large Language Models*. arXiv:2310.18313. https://arxiv.org/abs/2310.18313 — 將 FP8 擴展到 LLM 訓練中的梯度與最佳化器狀態，並回報相對於 BF16 的記憶體與速度收益。
- Fishman, M. 等人 (2024). *Scaling FP8 training to trillion-token LLMs*. arXiv:2409.12517. https://arxiv.org/abs/2409.12517 — 以 FP8 訓練 LLM，資料量最多達兩兆 token，並分析長時間訓練中的不穩定性。
- Dao, T. 等人 (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — 以分塊方式計算精確注意力，減少對 GPU 高頻寬記憶體的讀寫。

### 綜述與教科書

- Griewank, A. & Walther, A. (2008). *Evaluating Derivatives*. SIAM. https://doi.org/10.1137/1.9780898717761 — 自動微分的標準參考書，涵蓋反向模式，而檢查點正是用來降低其儲存成本。
