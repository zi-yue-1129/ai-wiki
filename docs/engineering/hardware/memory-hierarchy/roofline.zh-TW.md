---
translation_reviewed: 2026-10-28
---

# 屋頂線模型

屋頂線模型是一張用來界定某程式在特定機器上能達到的效能上限的圖表。它以可達效能對運算強度作圖，其中運算強度是程式每從記憶體搬移一個位元組所執行的運算次數。圖上有兩條界線：一條水平線代表峰值浮點運算速率，另一條斜線代表峰值記憶體頻寬。Williams、Waterman 與 Patterson 於 2008 年與 2009 年為多核心處理器提出這個模型。[記憶體階層](index.zh-TW.md)頁面用它來說明，為什麼許多工作負載受限於頻寬。

## 問題

若程式核心的實測效能只有每秒幾十億次浮點運算，單看這個數字，無法判斷它受限於記憶體、受限於算術，還是因為程式碼不佳，也無法得知它還能快多少。Williams 等人希望有一張圖，同時對程式設計師與架構師提供洞見，並顯示在特定機器上，是哪一種資源限制了浮點核心的效能。

## 關鍵概念

- **運算強度：** 每位元組 DRAM 流量所執行的運算次數，量測的是快取與主記憶體之間的流量。它是圖表的橫軸。
- **運算上限：** 機器的峰值浮點效能。它是一條水平線，任何核心都不能超過它。論文從硬體規格或微基準測試取得這個數值。
- **記憶體上限：** 峰值記憶體頻寬，在對數座標上畫成斜線。論文將它描述為記憶體能持續維持的穩態頻寬，而非 DRAM 晶片標示的接腳頻寬。
- **屋脊點：** 兩條上限相交的運算強度。它等於峰值效能除以峰值頻寬。

## 運作方式

上界為

\[
P_{\text{attainable}} = \min\left(P_{\text{peak}},\; B \cdot I\right)
\]

其中 \(P_{\text{peak}}\) 是運算上限，\(B\) 是記憶體頻寬，\(I\) 是運算強度。運算強度低於屋脊點的核心受記憶體限制；高於屋脊點的核心則受運算限制。

使用這張圖時，先量測核心，並把它標成一個點：

- 點位於屋頂下方越遠，表示更好的程式碼越有機會縮小這段差距。
- 要把點往右移，需要重複使用每個位元組的資料，例如透過分塊或融合運算。要把點往上移，則需要更好地利用同一套硬體。

上限針對每台機器計算一次，而非針對每個核心。同一台機器上的所有核心，都以同樣的兩條線來衡量。

## 階層式 Roofline

原始模型只計算到主記憶體的流量，並假設工作集無法完全放入晶片上的快取。當快取服務了大部分流量時，單一記憶體上限會給出誤導性的上界。Yang 等人（2020）將模型延伸到 NVIDIA GPU 記憶體階層的每一層，各層各有一條上限。每一層都有自己的運算強度，也就是該層每位元組搬移所對應的運算次數，因此一個核心可能受某一層限制，卻不受另一層限制。他們也把 Empirical Roofline Toolkit 延伸到更多數值精度與 Tensor Core 運算，並以一個以 TensorFlow 與 PyTorch 撰寫的深度學習氣候影像分割應用進行分析。

## 套用於 LLM 推論

Yuan 等人（2024）使用 屋頂線框架分析 LLM 推論的效率。他們的分析說明了 LLM 在解碼階段為何受記憶體限制、各種方法需要多少記憶體與運算，以及如何選擇硬體。[記憶體階層](index.zh-TW.md)頁面也說明了相同的算術：模型為一個序列生成一個詞元時，每個權重只讀取一次，並僅用於約一次運算，因此運算強度約為 1，遠在屋脊點的左側。把多個序列批次化，可以讓每個權重在整個批次中重複使用，使該點往右移。

## 結果

屋頂線模型已被延伸到 GPU，並應用於深度學習工作負載。Yang 等人（2020）以逐層的圖表，顯示一個應用如何使用 GPU 的運算與記憶體資源，以及它以 TensorFlow 與 PyTorch 實作時的表現有何不同。Yuan 等人（2024）則使用 屋頂線框架，依高效 LLM 推論技術對記憶體存取與運算的影響，來分析這些技術。

## 限制

- **原始界線假設記憶體是主要限制。** 記憶體上限把主記憶體的頻寬視為限制資源，因此當快取有效時，單層圖表的說服力較弱。
- **上限都是峰值數值。** 實際達到的頻寬與運算吞吐量通常低於上限，因此屋頂是上界，而非預測。
- **忽略延遲與重疊。** 模型不描述核心等待資料的時間，也不描述其運算與記憶體流量的重疊程度。
- **運算強度取決於實作。** 計算位元組數需要真實程式碼的快取行為，必須實際量測。融合後的核心，其運算強度可能遠高於同樣運算分開執行的版本。
- **晶片之間的通訊不在基本圖表內。** 模型描述的是單一機器，因此晶片之間連線的成本需要另外分析，見[互連](../interconnects/index.zh-TW.md)。

## 開放問題

- **多晶片 Roofline。** 加入晶片間連線上限的圖表，能否為大型模型的訓練與服務提供有用的界線，仍是擴展性討論中的開放問題。
- **形狀會改變的工作負載。** LLM 推論的運算強度取決於批次大小與上下文長度，因此每個模型只有一個點並不足夠。如何在同一張圖上呈現這些形狀的完整範圍，仍在研究中。

## 相關連結

屋頂線模型是[記憶體階層](index.zh-TW.md)頁面中頻寬論述所依據的分析工具，也解釋了為什麼減少每個數值的位元數會有幫助，例如[混合精度訓練](../co-design/mixed-precision.zh-TW.md)與[量化](../../../theory/model-compression/quantisation/index.zh-TW.md)。對於相同的運算，搬移較少位元組的核心具有較高的運算強度，這正是 [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.zh-TW.md) 所依賴的效果。[推論最佳化](../../inference-optimization/index.zh-TW.md)章節則把同樣的想法應用於服務端。

## 參考文獻

### 開創性論文

- Williams, S., Waterman, A. 與 Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM 52(4), 65–76. https://doi.org/10.1145/1498765.1498785 — 提出這張圖，以峰值運算能力與峰值記憶體頻寬乘以運算強度，界定可達到的效能。
- Williams, S., Waterman, A. 與 Patterson, D. (2008). *Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures*. Technical Report UCB/EECS-2008-134, UC Berkeley. https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf — 原始技術報告，定義了各項上限，並說明上限是針對每台機器計算一次。

### 綜述與教科書

- Yang, C., Wang, Y., Farrell, S., Kurth, T. 與 Williams, S. (2020). *Hierarchical Roofline Performance Analysis for Deep Learning Applications*. arXiv:2009.05257. https://arxiv.org/abs/2009.05257 — 將模型延伸到 NVIDIA GPU 記憶體階層的每一層，並應用於一個深度學習應用。
- Yuan, Z., 等人 (2024). *LLM Inference Unveiled: Survey and Roofline Model Insights*. arXiv:2402.16363. https://arxiv.org/abs/2402.16363 — 以 屋頂線框架綜述高效的 LLM 推論，並說明 LLM 為何受記憶體限制。

### 文章與文件

- Gholami, A., 等人 (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — 主張對 AI 服務而言，主要瓶頸是記憶體頻寬而非運算，而這正是記憶體上限所描述的情境。
