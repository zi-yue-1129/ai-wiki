---
translation_reviewed: 2026-10-28
---

# 硬體感知的模型與軟體協同設計

模型的成本不只由參數數量或 FLOPs 決定。它的速度還取決於使用的數值格式、運算是否融合成能讓資料留在晶片上的核心，以及它所執行的晶片。硬體感知的設計，是從一開始就把這些因素納入模型與軟體堆疊，而不是等模型完成後再量測它快不快。本頁是 [AI 硬體](../index.zh-TW.md)章節的子章節。它涵蓋三個主要槓桿：數值格式、核心與編譯器，以及在目標硬體上量測的架構選擇，並連結到各自的頁面。

## 問題

只計算 FLOPs 並不能很好地預測延遲。兩個 FLOPs 相同的網路，速度可能相差數倍，因為其中一個讀取的記憶體多得多、使用較慢的運算，或無法有效地對應到晶片上。硬體的更新速度快於模型，因此為某一世代調校的設計，對下一世代可能不太合適。

## 核心想法

有三個槓桿可以改變運算與記憶體之間的平衡，每個都在 wiki 的其他地方有專門的頁面：

- **數值格式。** 每個數值使用的位元越少，每次運算的記憶體流量就越少。混合精度訓練與 8 位元推論都依賴這一點，而準確度的代價由訓練方法來控制。
- **核心與編譯器。** 融合的核心在一次掃過資料時完成多個運算，中間結果不必寫回晶片外的記憶體。以 CUDA 與 Triton 語言撰寫的手工核心，以及 XLA 等編譯路徑，是讓這件事成為可能的軟體層。
- **在目標上的架構。** 某個設計選擇，例如鍵與值頭的數量，或模型的專家結構，應依據它在實際執行的晶片上的量測速度來判斷，而不是依 FLOPs 判斷。

## 公式或演算法

[記憶體階層與頻寬](../memory-hierarchy/index.zh-TW.md)中的屋頂線模型，可以給出一個核心所需時間的初步估計：

\[
t \approx \max\left(\frac{\text{FLOPs}}{P_{\text{peak}}},\; \frac{\text{搬移的位元組數}}{B}\right)
\]

改變數值格式會直接改變位元組數這一項：把權重儲存為一半的位元，對於受記憶體限制的層而言，每個 token 讀取的位元組數減半，因此算術強度大約加倍。融合也會改變位元組數，因為留在晶片上的中間結果不計入流量。架構選擇會同時影響兩項，哪一項佔主導，只能靠在目標上的量測來確定。

## 結果

Micikevicius 等人（2017）顯示，以 16 位元浮點數訓練，在多種架構上大約可把記憶體用量減半，前提是保留一份全精度的權重副本，並進行損失縮放。

Micikevicius 等人（2022）提出兩種 8 位元浮點編碼，他們報告以此可以訓練 CNN、RNN 與 Transformer，包括參數多達 1750 億的模型，其品質與 16 位元訓練相當，且不需更改超參數。

Krishnamoorthi（2018）報告，訓練後以逐通道權重進行的 8 位元整數量化，可讓許多 CNN 的準確度維持在浮點數的約 2% 以內，並在 CPU 上達到約 2 至 3 倍的加速，在定點硬體上最多可達 10 倍。

Dao 等人（2022）顯示，一個避免把中間結果寫入高頻寬記憶體的注意力核心，比標準實作更快，且計算的是完全相同的精確結果。

Tan 等人（2018）把手機上量測到的推論速度納入 MnasNet 的搜尋目標，使搜尋偏好在裝置上兼顧準確度與延遲的網路，而非以 FLOPs 作為代理。

## 限制

協同設計會把模型與晶片綁在一起。為某一加速器調校的網路，在另一顆晶片上可能失去大部分速度，因此可移植性會受損。所報告的加速倍數取決於編譯器版本、批次大小與軟體堆疊，因此在不同環境中很難重現。較低精度的格式需要謹慎處理：它們可能以只在大型或特殊工作負載上才出現的方式改變準確度。

## 開放問題與相關變體

- **哪些格式能通用。** 目前尚不清楚哪些 8 位元或 4 位元格式能在晶片世代之間持續使用，或它們的準確度在長推理鏈上能維持多久。
- **手工核心與編譯器。** 手寫的 CUDA 核心控制力最強，而編譯器與高階語言能以較少的努力支援更多硬體。兩者之間的平衡正在改變。
- **混合專家。** Shazeer 等人（2017）顯示，條件式計算可以在相近的運算成本下大幅提高模型容量。成本會轉移到記憶體與晶片之間的通訊上，因此專家的配置必須配合[互連](../interconnects/index.zh-TW.md)。
- **注意力的記憶體。** [分組查詢注意力](../../inference-optimization/grouped-query-attention.zh-TW.md)設計減少了長上下文解碼必須讀取的 [KV 快取](../../../theory/models/transformer/kv-cache/index.zh-TW.md)，而 [PagedAttention](../../inference-optimization/paged-attention.zh-TW.md) 則減少了該記憶體中被浪費的部分。
- **相關：** [量化](../../../theory/model-compression/quantisation/index.zh-TW.md)是數值格式槓桿在模型端的一半，而[模型壓縮](../../../theory/model-compression/index.zh-TW.md)的各種方法，決定模型能使用哪些格式。

## 相關連結

本頁假設的硬體，已在 [AI 加速器](../accelerators/index.zh-TW.md)中說明，其中 [TPU](../accelerators/tpu/index.zh-TW.md) 是固定功能矩陣硬體的例子。這些取捨在訓練端的版本，見[分散式訓練](../../distributed-training/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Dao, T., 等人 (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — 一種具 IO 感知能力的注意力核心，比標準方法更快，且計算的是完全相同的精確結果。
- Micikevicius, P., 等人 (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — 顯示 16 位元訓練在多種架構上大約可將記憶體用量減半，並需搭配主權重副本與損失縮放。
- Micikevicius, P., 等人 (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — 提出兩種 8 位元浮點編碼，可將大型模型訓練到與 16 位元相當的品質。
- Shazeer, N., 等人 (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — 提出條件式計算，能在相近的運算成本下大幅提高模型容量。
- Tan, M., 等人 (2018). *MnasNet: Platform-Aware Neural Architecture Search for Mobile*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — 把量測到的裝置端延遲納入架構搜尋的目標。

### 綜述與教科書

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — 綜述資料流與數值格式的選擇如何影響 DNN 硬體的效率。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — 報告逐通道的 8 位元整數量化能讓許多 CNN 維持接近浮點數的準確度，並加速 CPU 與定點硬體上的推論。
