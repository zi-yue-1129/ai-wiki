---
translation_reviewed: 2026-10-28
---

# 機器學習編譯器與核函式語言

機器學習編譯器與核函式語言，會把模型的數學描述轉換成能在特定硬體上高效執行的程式碼。它們決定哪些運算會被合併、資料在記憶體中如何排列，以及工作如何分配給各個處理器，因此在很大程度上決定了模型在加速器上能跑多快。

## 概述

深度學習框架把模型描述為一連串張量運算。若每個運算各自執行，加速器就要從主記憶體讀入輸入、計算，再把結果寫回。對許多運算而言，計算本身遠比這些記憶體搬運快，因此程式受限於記憶體，而不是運算能力。編譯器會檢視整張計算圖，把運算合併成較少的核函式，並為目標晶片產生程式碼，藉此降低成本。核函式語言則更進一步，讓工程師直接撰寫最內層的迴圈。

硬體的多樣性讓這個需求更加迫切。同一個模型可能要在 GPU、TPU、手機的神經網路引擎與 CPU 上執行，而每一種硬體都有自己的記憶體階層與指令集。TVM 的作者指出，若沒有編譯器，把工作負載部署到新平台就需要大量人工投入。[^tvm] 關於這些編譯器所針對的晶片，見 [AI 硬體](../hardware/index.zh-TW.md)。

## 關鍵概念

- **計算圖擷取（graph capture）**：在運算執行之前記錄張量運算，方式可以是追蹤一次執行，也可以是分析 Python 程式碼。
- **中間表示（intermediate representation, IR）**：編譯器會改寫的程式表示形式。現代編譯器多半使用多個層級，從圖層級的運算一直降到迴圈與機器指令。
- **運算子融合（operator fusion）**：把數個運算合併成一個核函式，使中間結果能留在暫存器或晶片上的快取中。偏置加法接著一個啟動函數，就是典型例子。
- **核函式（kernel）**：在加速器上以大量平行執行緒執行的函式。
- **分塊（tiling）**：把一個計算切成能放進快速晶片內記憶體的區塊，並在移到下一塊之前重複使用目前的區塊。
- **排程（schedule）**：對某個運算選擇分塊大小、迴圈順序與平行化對應方式。Halide 將演算法與排程分開，使同一個計算能針對不同機器調校。[^halide]
- **算術強度（arithmetic intensity）**：每搬運一個位元組的記憶體所執行的浮點運算數。屋頂線模型（roofline model）把可達到的效能上限定為峰值運算能力，與算術強度乘以記憶體頻寬兩者中的較小者。[^roofline]

## 運作方式

典型的編譯器流程是：擷取計算圖，透過融合運算與選擇資料配置來改寫它，降低為迴圈，產生程式碼，以啟發式方法或搜尋選出排程，最後在裝置上執行結果。

```mermaid
flowchart LR
  M["模型程式碼"] --> C["計算圖擷取"]
  C --> R["計算圖改寫：融合、配置"]
  R --> L["降低為迴圈與 IR"]
  L --> G["程式碼產生"]
  G --> A["排程自動調校"]
  A --> X["在加速器上執行"]
```

融合說明了這一點為何重要。若分開執行，偏置加法與啟動函數各自都要把完整輸出寫入主記憶體，再讀回來。融合後，兩者都在每個數值仍位於快速記憶體時套用，結果只需寫入一次。數學內容不變，但捨入結果可能略有不同。

注意力機制是手工設計核函式最明顯的例子。標準注意力會實體化一個分數矩陣，其大小隨序列長度的平方成長。FlashAttention 則以分塊方式逐塊計算完全相同的結果，因此大型矩陣不必存入較慢的記憶體。[^flashattention] 它的收益來自減少讀寫次數，而不是減少運算次數。

## 關鍵方法

下表比較主要做法。

| 做法 | 誰撰寫核函式 | 最佳化的對象 | 主要取捨 |
|---|---|---|---|
| XLA（TensorFlow、JAX） | 編譯器，依整張計算圖工作 | 整個編譯程式中的融合與配置 | 依輸入形狀編譯，形狀改變就會重新編譯 |
| TorchInductor（`torch.compile`） | 編譯器，依從 Python 擷取的計算圖工作 | 融合；GPU 上產生 Triton 程式碼，CPU 上產生 C++ | 無法擷取的程式碼會造成計算圖斷裂，改回逐步執行 |
| Triton | 程式設計師，以資料區塊為單位 | 每個區塊內的記憶體存取與排程 | 控制力不如 CUDA，而且需要學習新語言 |
| TVM 與 Ansor | 編譯器，排程由搜尋找出 | 跨多種後端的效能，由學習式成本模型引導 | 每個運算都需要花費搜尋的計算時間 |
| 手寫 CUDA | 工程師 | 對執行緒、共享記憶體與指令的完整控制 | 每個核函式、每一代硬體都要投入大量心力 |

**XLA** 會把整個線性代數運算程式編譯成目標裝置的程式碼，也是 JAX 與 TensorFlow 大量加速器支援背後的編譯器。

**TorchInductor** 是 PyTorch 2 中 `torch.compile` 的後端。TorchDynamo 從一般的 Python 程式擷取計算圖，TorchInductor 再把它降低為 GPU 上的 Triton 核函式，或 CPU 上的 C++ 程式碼。[^pt2] 無法擷取的程式碼則以逐步執行的方式運行。

**Triton** 讓程式設計師以資料區塊為單位思考，編譯器負責處理每個區塊內部的細節。[^triton]

**TVM 與 Ansor** 在圖層級與運算子層級為多種後端進行最佳化。TVM 的作者報告其效能足以與手工調校的函式庫競爭。[^tvm] Ansor 的作者報告，相較於當時較早的最先進方法，它在 Intel CPU 上最多可加速 3.8 倍。[^ansor]

**手寫 CUDA** 仍然是取得最後一段效能的方式。FlashAttention 就是以這種方式建構的。代價是工程投入，而且每一代硬體都得重做一次。

## 相關連結

- 呼叫這些編譯器的框架列在[框架與工具](index.zh-TW.md)總覽中。編譯器還必須把通訊與運算安排在一起，這部分見[分散式訓練](../distributed-training/index.zh-TW.md)。
- 服務部署依賴核函式。[推論最佳化](../inference-optimization/index.zh-TW.md)涵蓋的演算法，例如 [PagedAttention](../inference-optimization/paged-attention.zh-TW.md)，其速度取決於客製化的記憶體存取程式碼。
- 注意力是編譯器與核函式撰寫者最常最佳化的運算，見 [Transformer](../../theory/models/transformer/index.zh-TW.md)。經編譯的計算圖仍必須產生正確的梯度，相關規則見[自動微分](../../theory/math/automatic-differentiation/index.zh-TW.md)。
- 編譯器對新架構很重要。某個新運算在框架中可能結果正確，但在沒有融合核函式之前仍然很慢。這也是狀態空間模型 [Mamba](../../theory/models/ssm/selective-state-spaces/mamba/index.zh-TW.md) 依賴硬體感知掃描的原因。
- 腦與心智的角度：[尖峰神經網路](../../brain-mind/snn-neuromorphic/index.zh-TW.md)所描述的神經形態晶片是事件驅動的，記憶體與通訊方式都和 GPU 差異很大。把網路映射到這類晶片，是同一類型的編譯問題。

## 應用

- **訓練大型模型**：融合 Transformer 區塊中的許多小運算，可減少前向與反向傳播中的記憶體搬運。
- **服務部署**：開源服務引擎中的注意力與取樣核函式通常都是客製化撰寫的。
- **可攜式部署**：當編譯器支援各個後端時，同一個模型可以部署到加速器、手機與 CPU。
- **新架構**：撰寫快速核函式，往往決定一個提出的架構是否可行。

## 開放問題

- **自動化與手工設計的取捨**：基於搜尋的編譯器在常見運算上表現良好，但最快的注意力核函式仍是手工設計的。搜尋能否在硬體改變時縮小這段差距，目前並不清楚。
- **動態形狀與控制流程**：擷取到的計算圖假設結構固定，而可變長度的輸入與依資料決定的分支，會迫使系統重新編譯或退回逐步執行。
- **數值行為**：融合會改變浮點數結果，因此測試必須以編譯後的程式碼為準，而不只是原始模型。

[^tvm]: TVM 論文指出，若沒有編譯器，把工作負載部署到新平台就需要大量人工投入。參見參考文獻中的 Chen et al. (2018)。
[^halide]: 演算法與排程的分離，正是 Ragan-Kelley et al. (2013) 的核心想法。
[^roofline]: 參見 Williams, Waterman and Patterson (2009)。上限為峰值運算能力與算術強度乘以頻寬兩者中的較小者。
[^flashattention]: Dao et al. (2022) 主張，注意力演算法必須考慮 GPU 高頻寬記憶體與晶片上 SRAM 之間的讀寫。
[^pt2]: Ansel et al. (2024) 說明了經編譯的執行路徑，以及退回逐步執行的情況。
[^triton]: Tillet, Kung and Cox (2019) 說明編譯器如何處理每個分塊內部的細節。
[^ansor]: 此數字是 Zheng et al. (2020) 摘要中報告的結果。

## 參考文獻

### 開創性論文

- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. OSDI 2018. https://arxiv.org/abs/1802.04799 — 結合圖層級與運算子層級最佳化，並以學習式成本模型服務多種硬體的編譯器。
- Ragan-Kelley, J. et al. (2013). *Halide: A Language and Compiler for Optimizing Parallelism, Locality, and Recomputation in Image Processing Pipelines*. PLDI 2013. https://doi.org/10.1145/2491956.2462176 — 將演算法與排程分開，這個想法後來被張量編譯器採用。
- Tillet, P., Kung, H. T. & Cox, D. (2019). *Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations*. MAPL 2019. https://doi.org/10.1145/3315508.3329973 — 為分塊神經網路計算撰寫 GPU 核函式的區塊層級語言與編譯器。
- Ansel, J. et al. (2024). *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*. ASPLOS 2024. https://doi.org/10.1145/3620665.3640366 — 說明 PyTorch 2 如何把 Python 程式擷取成計算圖，並以 TorchInductor 編譯。
- Zheng, L. et al. (2020). *Ansor: Generating High-Performance Tensor Programs for Deep Learning*. OSDI 2020. https://arxiv.org/abs/2006.06762 — 透過對階層式搜尋空間取樣，再以演化搜尋精煉，產生張量程式。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — 以分塊方式計算精確注意力，減少對較慢 GPU 記憶體的讀寫。
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline*. Communications of the ACM. https://doi.org/10.1145/1498765.1498785 — 屋頂線模型，把效能與算術強度及記憶體頻寬聯繫起來。

### 綜述與教科書

- Li, M. et al. (2020). *The Deep Learning Compiler: A Comprehensive Survey*. arXiv:2002.03794. https://arxiv.org/abs/2002.03794 — 深度學習編譯器的綜述，包含 XLA 與 TVM，聚焦於其多層級中間表示。
