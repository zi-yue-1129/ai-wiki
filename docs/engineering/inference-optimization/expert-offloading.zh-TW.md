---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - theory/models/mixture-of-experts
  - engineering/inference-optimization
  - engineering/on-device-edge
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - 專家卸載
  - MoE 卸載
---

# 專家卸載

!!! info "屬於混合專家模型的服務"
    本方法頁隸屬於[混合專家模型的服務](moe-serving.zh-TW.md)。它詳細說明專家卸載；上層頁面則比較它與其他方法。

專家卸載讓 MoE 模型能在無法保存所有專家的裝置上服務。不活躍的專家保存在主機記憶體或磁碟中，路由器需要時才把它們載入裝置。Eliseev 與 Mazur 以參數卸載演算法為基礎，提出一種加速卸載的策略，並報告能在桌上型硬體上以混合量化執行 Mixtral-8x7B。

## 問題

每層有八個大型專家的 MoE 模型，可能大到一張 GPU 的記憶體放不下，即使每個 token 只用到其中兩個專家。把每個專家都保留在裝置上，會浪費記憶體在目前 token 不使用的專家上。把所有專家都卸載到主機，則每次取用專家都很慢。問題在於：如何讓模型實際使用的專家靠近運算，同時載入其餘的專家，又不讓生成停頓。

## 核心想法

此方法在裝置上保留模型的非專家部分，以及一份專家快取；其餘專家則存放在主機記憶體中。當路由器選到不在裝置上的專家時，該專家會被傳到裝置。作者以參數卸載演算法為基礎，提出一種加速卸載的策略。摘要並未詳細描述該策略，因此本頁也不描述。模型以混合量化執行，可減少必須儲存與搬移的資料大小。

## 程序

1. 以混合位元寬度的方案量化專家權重，以縮小其大小。
2. 把專家保存在主機記憶體中，並在裝置上保留共享層與一份專家快取。
3. 對每一層，由路由器為目前的 token 選擇專家。
4. 載入所有被選中、但不在裝置上的專家。
5. 依該方法定義的快取策略淘汰一個已快取的專家以騰出空間，然後繼續生成。

## 結果

摘要報告，此策略可讓 Mixtral-8x7B 以混合量化在桌上型硬體上執行。摘要也指出，MoE 模型生成 token 比同等大小的稠密模型快，因為對任一輸入只有部分層是活躍的。摘要未給出具體的速度數字，因此本頁不報告速度。需要這些數字的讀者，應在目標硬體上，以所用的快取大小與量化方式進行量測。

## 限制

- **載入延遲。** 當路由器選到不在裝置上的專家時，該 token 必須等待傳輸完成，因此增加了延遲。
- **快取命中率。** 增益取決於路由器選到已快取專家的頻率，而這會因提示與模型而異。
- **量化的影響。** 為了放進記憶體而量化專家，可能降低輸出品質，因此量化後必須檢查品質。
- **批次的行為。** 同時服務許多請求，會把路由器的選擇分散到更多專家上，降低快取命中率。

## 關聯

- 在所有裝置上保留專家並加以分片的替代做法，是 [GShard](gshard.zh-TW.md)。
- 壓縮模型並使用專用推論系統的替代做法，是 [DeepSpeed-MoE](deepspeed-moe.zh-TW.md)。
- 為較小裝置量化權重的說明，見[裝置端與邊緣 AI](../on-device-edge/index.zh-TW.md)頁面。
- Mixtral 的架構見[混合專家理論頁面](../../theory/models/mixture-of-experts/mixtral.zh-TW.md)。

## 開放問題

- 快取策略能否利用路由器的機率，在專家被選中之前預先載入？
- 隨著批次變大，快取命中率會下降多少？到什麼時候卸載就不再值得？

## 參考文獻

### 重要論文

- Eliseev, A. & Mazur, D. (2023). *Fast Inference of Mixture-of-Experts Language Models with Offloading*. arXiv:2312.17238. https://arxiv.org/abs/2312.17238 — 主要論文：用於 MoE 推論的卸載策略，能在桌上型硬體上以混合量化執行 Mixtral-8x7B。
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — 稀疏閘控層，卸載方法讓其中未使用的專家離開裝置。
- Rajbhandari, S. et al. (2022). *DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale*. arXiv:2201.05596. https://arxiv.org/abs/2201.05596 — 壓縮加系統的替代服務方法。
- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. https://arxiv.org/abs/2006.16668 — 把專家保留在多台裝置上的分片替代做法。
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research. arXiv:2101.03961. https://arxiv.org/abs/2101.03961 — Top-1 路由，限制了每個 token 需要的專家數。
