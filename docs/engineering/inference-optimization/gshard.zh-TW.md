---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - theory/models/mixture-of-experts
  - engineering/inference-optimization
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - GShard
  - 自動分片
---

# GShard

!!! info "屬於混合專家模型的服務"
    本方法頁隸屬於[混合專家模型的服務](moe-serving.zh-TW.md)。它詳細說明 GShard；上層頁面則比較它與其他方法。

GShard 是一組標註 API 與 XLA 編譯器的擴充，用來把稀疏閘控的混合專家模型分片到許多裝置上。作者以它訓練超過 6000 億參數的模型：程式設計者為張量該如何切分加上標註，再由編譯器產生分割後的程式。它主要是訓練系統，但其分片方法是推論時專家平行化的基礎。

## 問題

專家很多的模型對單一裝置來說太大，因此專家必須分散到多台裝置上。針對每個模型與每種配置手動撰寫裝置間的通訊，容易出錯，也無法擴展到許多種配置。問題在於：如何以一小組標註描述平行配置，並讓編譯器產生裝置上的程式。

## 核心想法

GShard 要求程式設計者標註哪些張量維度要跨裝置切分（例如專家維度），以及模型應在何處複製。接著，GShard 所擴充的編譯器會分割運算，並插入所需的通訊。對稀疏閘控的混合專家層而言，專家維度會跨裝置切分，token 則被路由到持有其專家的裝置。

## 程序

1. 撰寫模型，並標註要跨裝置切分的張量維度。
2. 為專家層加上標註，使每個專家或每組專家位於某台裝置上。
3. 以擴充後的 XLA 編譯器編譯已標註的模型，由它分割程式。
4. 執行分割後的程式，由編譯器插入路由所需的通訊。
5. 對照裝置檢查配置，若通訊佔主導，則調整標註。

## 結果

論文報告，以自動分片訓練超過 6000 億參數的稀疏閘控混合專家模型。論文也報告，在 2048 顆 TPU v3 加速器上，於 4 天內訓練了一個從 100 種語言翻譯成英文的模型。這些是訓練結果，論文的重點也在訓練，因此推論的影響應從設計推論，而非從論文中報告的推論基準得出。

## 限制

- **以訓練為主。** 論文談的是訓練模型。推論的批次大小與延遲需求不同，因此為訓練選擇的配置未必是推論的最佳配置。
- **依賴編譯器。** 此方法依賴 XLA 擴充，因此其效益取決於編譯器對目標硬體的支援。
- **路由的通訊。** 路由在每一層都需要全互連流量，而流量取決於 token 在專家之間分散的均勻程度。

## 關聯

- GShard 所擴充的編譯器是 [XLA](../frameworks/compilers-and-kernels/xla.zh-TW.md)，見框架與工具的編譯器與核心程式一節。
- 架構與路由見[混合專家理論頁面](../../theory/models/mixture-of-experts/index.zh-TW.md)。
- 其他服務方法為 [DeepSpeed-MoE](deepspeed-moe.zh-TW.md) 與[專家卸載](expert-offloading.zh-TW.md)。

## 開放問題

- 當批次小、延遲比吞吐量更重要時，推論最好的專家配置是什麼？
- 分片標註能否依服務工作負載自動推導，而不需要程式設計者手動撰寫？

## 參考文獻

### 重要論文

- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. https://arxiv.org/abs/2006.16668 — 主要論文：用於分片稀疏閘控 MoE 模型的標註 API 與 XLA 擴充，附有訓練結果。
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — GShard 所分片的稀疏閘控混合專家層。
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research. arXiv:2101.03961. https://arxiv.org/abs/2101.03961 — Top-1 路由，簡化了 GShard 配置所需支援的通訊。
- Rajbhandari, S. et al. (2022). *DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale*. arXiv:2201.05596. https://arxiv.org/abs/2201.05596 — 以推論為主的 MoE 系統，與以訓練為主的設計比較。
- Eliseev, A. & Mazur, D. (2023). *Fast Inference of Mixture-of-Experts Language Models with Offloading*. arXiv:2312.17238. https://arxiv.org/abs/2312.17238 — 以卸載在記憶體較少的硬體上服務 MoE 模型的另一種做法。
