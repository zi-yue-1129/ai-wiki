---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/kv-cache
  - engineering/inference-optimization
  - engineering/on-device-edge
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - KIVI
  - KV 快取 2 位元量化
---

# KIVI

!!! info "屬於 KV 快取壓縮與淘汰"
    本方法頁隸屬於[KV 快取壓縮與淘汰](kv-cache-compression.zh-TW.md)。它詳細說明 KIVI；上層頁面則比較它與其他方法。

KIVI 是一種無需調校的方法，把 KV 快取量化為 2 位元。它保留每一個 token，但以少得多的位元儲存每一個 token，並且因為 key 與 value 的統計特性不同，會沿不同的軸進行量化。作者報告，包含模型權重在內，它把峰值記憶體降低為 2.6 倍，並允許多達 4 倍的批次大小，使真實 LLM 推論工作負載的吞吐量達到 2.35 至 3.47 倍。

## 問題

淘汰會丟棄 token 來縮小快取，但可能移除後續 token 需要的內容。量化每一個 token 可以避免這種損失，但單純把快取量化為 2 位元會嚴重損害準確度。原因在於 key 與 value 的分布不同：某些 key 通道含有很大的離群值，而 value 則在各 token 之間變化較平緩。同一套方案無法同時適用於兩者。

## 核心想法

作者分析 key 與 value 後發現，key 的離群值集中在某些通道，value 則沒有。因此 KIVI 依通道量化 key，讓每個通道使用自己的縮放係數，使離群值不會擴散到其他通道。它依 token 量化 value。這個方案是非對稱的，每組都有零點，而且無需調校，因此可以直接套用到既有模型上。

## 程序

1. 以全精度保留最近的一小段 token 殘差，因為它們被讀取最頻繁。
2. 以 2 位元依通道量化 key，每組附帶縮放係數與零點。
3. 以 2 位元依 token 量化 value，每個 token 附帶縮放係數與零點。
4. 儲存量化後的快取，並在讀取時於注意力核心中反量化各區塊。
5. 對反量化後的值計算注意力，並把新 token 寫入殘差。

## 結果

摘要報告，在測試的模型上，KIVI 包含權重在內的峰值記憶體降低為 2.6 倍，允許多達 4 倍的批次大小，並在真實 LLM 推論工作負載上達到 2.35 至 3.47 倍的吞吐量。論文報告，在它所用的基準上準確度損失很小。記憶體與吞吐量的數字取決於硬體、批次大小與基準，因此應連同論文的實驗設定一起閱讀。

## 限制

- **量化的額外開銷。** 在注意力中反量化會增加工作量，因此吞吐量增益取決於核心實作，以及工作負載是否受記憶體頻寬限制。
- **分組大小。** 準確度取決於分組大小與離群值的分布方式，而這在不同模型之間各不相同。
- **長上下文的品質。** 平均上的小損失，在長上下文檢索任務上可能放大，因此使用前需要長上下文評估。
- **不是檢索方法。** 量化保留每一個 token，但並未改變模型能注意的範圍，快取仍會隨長度增長。

## 關聯

- 丟棄 token 而非降低其精度的替代方案，見 [H2O](h2o.zh-TW.md)。
- 若要把視窗方法與量化結合，匯聚 token 應始終保持全精度，這點在 [StreamingLLM](streamingllm.zh-TW.md) 中有說明。
- 權重量化使用的是相同的位元寬度概念，在邊緣裝置上的應用見[裝置端與邊緣 AI](../on-device-edge/index.zh-TW.md)。

## 開放問題

- 能否在量化之前預測 key 的離群值通道，使每個模型只需設定一次縮放係數，而不是每組各設定一次？
- 殘差的全精度大小，是否應依請求的長度與任務來選擇？

## 參考文獻

### 重要論文

- Liu, Z. et al. (2024). *KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache*. arXiv:2402.02750. https://arxiv.org/abs/2402.02750 — 主要論文：2 位元 KV 快取量化，key 依通道、value 依 token，且無需調校。
- Zhang, Z. et al. (2023). *H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models*. arXiv:2306.14048. https://arxiv.org/abs/2306.14048 — 淘汰的替代方案，以丟棄 token 換取較小的快取。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — 分頁式快取佈局，量化後的區塊在其中儲存與讀取。
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — 架構上的快取縮減，需要訓練，並與事後量化進行比較。
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need*. arXiv:1911.02150. https://arxiv.org/abs/1911.02150 — 最早的共享頭快取縮減，用來與量化既有快取比較。
