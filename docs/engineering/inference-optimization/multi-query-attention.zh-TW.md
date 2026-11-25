# 多查詢注意力

多查詢注意力讓一個注意力層中的所有查詢頭，共用同一組 key 頭與 value 頭。KV 快取大約縮小為頭數的倍數，使解碼受記憶體限制的程度大幅降低。

## 概述

在標準的多頭注意力中，每個頭各自保存 key 與 value。推論時，KV 快取隨頭數增加，而每次解碼都要讀取全部快取。Shazeer 在 2019 年提出的多查詢注意力，保留所有查詢頭，但讓它們共用一個 key-value 頭，因此快取以及讀取快取所需的頻寬，都縮小為頭數的倍數。

## 關鍵概念

- **查詢頭**：各自計算注意力模式的獨立投影。多查詢注意力保留全部查詢頭。
- **共用的 key-value 頭**：所有查詢頭使用的單一 key 與 value 投影。
- **快取大小**：若有 $H$ 個頭，每個 token 的快取從 $H$ 組 key-value 縮減為一組。

## 運作方式

對每個 token，該層計算 $H$ 個查詢向量，但只計算一個 key 向量與一個 value 向量。解碼時，快取每個 token 只存一組 key 與 value。每個查詢頭都對這份共用快取做注意力，因此注意力計算的形式不變，但每一步的記憶體流量下降。

```mermaid
flowchart LR
  X[token 隱藏狀態] --> Q1[查詢頭 1]
  X --> Q2[查詢頭 2]
  X --> QH[查詢頭 H]
  X --> K[一個共用的 key]
  X --> V[一個共用的 value]
  K --> C[KV 快取：每個 token 一組]
  V --> C
```

### 算例：共用 Value 不代表輸出相同

<div tabindex="0" role="region" aria-label="可水平捲動的概念動畫；使用左右方向鍵" style="max-width:100%;overflow-x:auto">
<img data-source-asset-urls src="../../assets/concept-animations/mqa-shared-values-output-still.svg" data-motion-src="../../assets/concept-animations/mqa-shared-values-output-motion.svg" data-still-src="../../assets/concept-animations/mqa-shared-values-output-still.svg" alt="兩個查詢頭以不同權重對共用快取的數值 1、2、4 加權，分別累積出 1.8 與 3.0。" width="640" height="360" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 靜態預覽](../../assets/concept-animations/mqa-shared-values-output-still.svg) · 在 MkDocs 網站使用可鍵盤操作的播放／暫停控制（Enter 或空白鍵）；減少動態效果偏好預設顯示靜態圖。

跨頭共用 K 與 V 並不代表共用查詢或注意力分布。考慮兩個查詢頭及三個快取 token，共用純量 Value $v=(1,2,4)$。假設兩個頭的 Softmax 後權重分別為 $p_1=(0.6,0.2,0.2)$ 與 $p_2=(0.2,0.2,0.6)$。加權貢獻與輸出如下：

| 查詢頭 | Token 1 | Token 2 | Token 3 | 輸出 |
|---|---:|---:|---:|---:|
| Q1 | 0.6 | 0.4 | 0.8 | 1.8 |
| Q2 | 0.2 | 0.4 | 2.4 | 3.0 |

移動的外框標示目前正在累積貢獻的共用 token；兩條輸出長條使用相同尺度。兩個頭的注意力權重總和皆為 1，但加權輸出不同。逐欄累積僅用於解釋規約運算，並非融合注意力運算核心的實際執行順序。這些純量及機率是人工構造的教學數值，並非模型實測啟動值。共用 KV 的設計見 [Shazeer（2019）](https://arxiv.org/abs/1911.02150)，數值算例為原創，與[分組查詢注意力的頭共享及快取成長算例](grouped-query-attention.md)不同。

*原創教學動畫，CC BY-SA 4.0。*

## 關鍵方法

這個方法是對注意力層投影的修改，而非新的核心。它的證據是：在模型大小相同的情況下，解碼速度提升，代價是些許品質損失。

## 結果

Shazeer（2019）報告，在翻譯任務上，增量解碼速度較快，品質損失很小，這正是此方法設計要做的取捨。後續研究（包括分組查詢注意力）發現，增加 key-value 頭的數量可以補回品質差距。

## 限制

- **品質損失**：單一 key-value 頭的容量低於獨立的多個頭，可能傷害需要多樣注意力模式的任務。
- **訓練成本**：模型必須以這種結構訓練，既有的多頭檢查點無法直接轉換。
- **效益遞減**：快取變小後，權重與運算等其他成本會成為主導。

## 開放問題

- 大型語言模型要多少個 key-value 頭，品質才會與標準多頭注意力相當？
- 從頭訓練與轉換既有模型，這個取捨是否不同？

## 參考文獻

### 奠基性論文

- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need*. https://arxiv.org/abs/1911.02150 — 提出讓所有查詢頭共用單一 key 與 value 頭，以加速增量解碼。

### 相關研究

- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023. https://arxiv.org/abs/2305.13245 — 把這個概念推廣為一組 key-value 頭，在保留大部分記憶體節省的同時恢復品質。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — 以不同機制處理注意力的記憶體流量，這也是多查詢注意力所減少的部分。
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — 解釋為什麼減少每個 token 讀取的位元組，能加速受記憶體限制的解碼。
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — 說明當推論被分割到多顆晶片時，注意力佈局如何影響成本。
