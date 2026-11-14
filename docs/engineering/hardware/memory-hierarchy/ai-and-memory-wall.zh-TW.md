---
related:
  - engineering/hardware/co-design
  - theory/model-compression/quantisation
  - theory/models/transformer
tags:
  - hardware
  - memory bandwidth
  - scaling
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - AI and Memory Wall
  - Memory wall
  - 記憶體牆
---

# AI 與記憶體牆（Gholami et al., 2024）

Gholami 與同事（2024）主張，大型 AI 模型的主要效能瓶頸正從運算轉向記憶體頻寬。過去二十年，伺服器的峰值 FLOPS 成長速度遠快於 DRAM 與互連頻寬，因此現在限制模型訓練與服務速度的，是資料搬移，而非算術運算（Gholami et al., 2024）。

## 概觀

論文從推動模型規模的擴展趨勢談起。神經網路的擴展定律與大量無監督資料的取得，使 LLM 在訓練與服務時所需的運算與記憶體大幅增加。作者的論點是，硬體的趨勢並不均衡：運算的成長遠快於餵給它的頻寬，這個落差就是記憶體牆（Gholami et al., 2024）。

## 關鍵概念

- **峰值 FLOPS**：處理器每秒可達到的最大浮點運算次數。
- **記憶體頻寬**：資料在記憶體與處理器之間搬移的速率，以每秒位元組數計。
- **算術強度**：每從記憶體載入一個位元組所執行的浮點運算數。論文以 FLOPs 除以記憶體運算數來定義（第 II-A 節）。
- **記憶體受限**：執行速度由頻寬而非算術決定的工作負載，通常出現在算術強度低的情況。

## 擴展落差

摘要指出，過去二十年伺服器峰值 FLOPS 大約每兩年成長 3.0 倍，而 DRAM 與互連頻寬分別每兩年成長 1.6 倍與 1.4 倍（Gholami et al., 2024）。這些比率是對資料做線性迴歸的結果，論文的註腳 3 有此說明（圖 1）。同一期間，論文給出的整體成長約為：峰值 FLOPS 約 60,000 倍，DRAM 頻寬約 100 倍，互連頻寬約 30 倍。

由於運算的成長快於頻寬，處理器能執行的運算數可能超過記憶體能供應的量。因此，若設計希望充分利用運算能力，就必須減少每次運算所搬移的位元組數。

## 為何解碼是記憶體受限

論文主張，自迴歸解碼是記憶體受限工作負載最明顯的例子。生成每個 token 都需要把一個大型權重矩陣乘上單一的活化向量，因此每個權重只用於極少的運算。作者把這種矩陣向量運算的低算術強度歸因於自迴歸推論，並報告在他們的剖析中，GPT-2 的算術強度小了好幾個數量級（第 II-B 節，圖 3）。結果是，在低批次大小下，記憶體牆可能成為解碼器模型的主要瓶頸，而非運算（第 II-B 節）。

這份剖析假設使用 8 位元精度與批次大小為 1。作者指出，結論未必適用於所有解碼器應用，例如很長的輸入提示或大批次推論（註腳 5 與 6）。

## 提出的因應方式

論文第 III 節討論了數種因應方式，並主張架構本身也需要重新思考，因為許多大型 Transformer 只是近似相同基礎架構的放大版本：

- **高效訓練。** 二階方法、ZeRO 框架、只保存部分活化值的重新物化，以及低精度訓練（第 III-A 節）。
- **高效部署。** 量化（論文表示要降到 INT4 相對容易，且對準確率影響很小）、剪枝，以及小型語言模型（第 III-B 節）。
- **加速器設計。** 以峰值運算換取更好的運算與頻寬比、更有效率的快取，以及容量更大的 DRAM，可能形成不同頻寬的 DRAM 階層（第 III-C 節）。

## 相關連結

- [屋頂線模型](roofline.md) 提供判斷核心是受運算還是頻寬限制的標準方法，記憶體牆的論證正依賴這項判斷。
- [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) 是具體的因應方式：它減少精確注意力的記憶體流量，而非其算術量。
- [量化](../../../theory/model-compression/quantisation/quantisation-survey.md) 減少每個數值的位元組數，而 [硬體協同設計](../co-design/index.md) 同時改變模型與硬體。
- [擴展定律](../../../theory/models/llm/scaling-laws/kaplan-scaling-laws.md) 說明為何模型規模與記憶體需求持續上升。

## 應用

這項論證適用於服務大型語言模型（每生成一個 token 都要讀取權重），也適用於訓練極大模型（晶片之間的通訊成為瓶頸）。論文的結論是，晶片內與晶片間的記憶體搬移，很快就會成為服務大型 AI 模型的主要限制因素（第 IV 節）。

## 未解問題

- 頻寬相對運算能成長到多快，以及記憶體技術能否改變論文擬合的趨勢。
- 能否設計出在不損失準確率的前提下提高算術強度的架構。

## 參考文獻

### 開創性論文

- Gholami, A., Yao, Z., Kim, S. et al. (2024). *AI and Memory Wall*. arXiv. https://arxiv.org/abs/2403.14123 — 主張記憶體頻寬而非運算正成為大型模型的主要瓶頸，本頁討論的擴展比率即出自此文。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — 透過在快速記憶體中分塊計算，減少精確注意力的記憶體流量。
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 推動模型規模與記憶體需求成長的擴展定律。
- Frantar, E. et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv. https://arxiv.org/abs/2210.17323 — 低位元權重量化，減少解碼時讀取的位元組數。

### 綜述

- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline*. Communications of the ACM, 52(4), 65–76. https://doi.org/10.1145/1498765.1498785 — 屋頂線模型，將算術強度與可達到的效能聯繫起來。
