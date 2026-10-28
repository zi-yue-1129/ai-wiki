---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/hardware
tags:
  - engineering
  - frameworks
  - compilers
aliases:
  - Triton 核心程式語言
  - OpenAI Triton
  - Triton 語言
---

# Triton

!!! info "屬於編譯器與核心程式"
    本方法頁隸屬於[編譯器與核心程式](index.zh-TW.md)。它詳細說明這個核心程式語言；上層頁面則比較它與各種編譯器系統。

Triton 是一種以 Python 撰寫 GPU 核心程式的語言與編譯器。官方文件把它描述為提供「基於 Python 的程式設計環境」，用來「高效率地撰寫自訂的 DNN 運算核心程式」，目標是在「現代 GPU 硬體上達到最大吞吐量」。它介於全自動編譯器與手寫裝置程式碼之間：程式設計者決定分塊方式，底層細節則由 Triton 處理。

## 問題

某些運算（例如注意力）只有在融合並分塊、使資料能放進晶片上記憶體時，才會快。若以 CUDA 撰寫這些核心程式，每個晶片、每種變體都需要專家花時間。自動編譯器不一定能找到最佳的分塊，因此較快的核心程式往往需要有人手寫。問題在於：如何讓這類核心程式容易撰寫，又不損失大部分的硬體速度。

## 核心想法

程式設計者以 Python 撰寫計算的一個區塊，編譯器再把它對應到晶片的執行緒與記憶體上。程式是以區塊（tile）組織的：把資料區塊從慢速記憶體載入、計算，再寫回。由於程式設計者能控制區塊大小與載入順序，核心程式就能把中間值留在晶片上，這正是融合注意力的記憶體論點。

## 程序

1. 工程師把核心程式寫成一個以資料區塊為單位運作的 Python 函式。
2. 程式設計者為每個區塊選定大小，以及載入與儲存的方式。
3. Triton 編譯器把函式降階，並為目標裝置產生 GPU 程式碼。
4. 核心程式像函式庫函式一樣，從 Python 呼叫。

Triton 也被用作後端。TorchInductor 會為 NVIDIA、AMD 與 Intel GPU 產生 Triton 程式碼，見 [torch.compile 頁面](torch-compile.zh-TW.md)。

## 結果

官方文件描述的是語言與其目標，並未報告基準測試結果，因此本頁不提供速度提升的數字。以 Triton 撰寫的核心程式，應在目標 GPU 上測量，並記錄 Triton 版本。

## 限制

- **程式設計負擔。** 較快的核心程式仍需要分塊與記憶體的知識。與 CUDA 相比，這種語言降低了負擔，但並未消除。
- **目標支援範圍。** 支援的硬體與功能取決於 Triton 版本與後端。
- **調校。** 最佳區塊大小因晶片與輸入形狀而異，因此核心程式需要自動調校或謹慎選擇。
- **較底層的層級。** 官方頁面提到一個較低階的程式設計模型 Gluon，它較不成熟，本頁不作詳述。

## 關聯

- 為 PyTorch 產生 Triton 程式碼的編譯器是 [torch.compile 與 TorchInductor](torch-compile.zh-TW.md)。
- 自動融合運算的線性代數編譯器是 [XLA](xla.zh-TW.md)。
- 融合核心程式對注意力為何重要，見 [FlashAttention](https://arxiv.org/abs/2205.14135) 論文與[推論最佳化](../../inference-optimization/index.zh-TW.md)。

## 開放問題

- 隨著編譯器進步，以較高階語言撰寫的手寫核心程式，是否仍能保有其優勢？
- 核心程式應如何在記憶體階層不同的晶片之間共用？

## 參考文獻

### 開創性論文

- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — 融合且分塊的注意力核心程式，展示了 Triton 式核心程式所追求的速度提升。
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — 自動的替代方案，它搜尋排程，而非要求程式設計者自行撰寫。

### 文章與文件

- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — 語言、其基於 Python 的環境與目標的官方文件。
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — 說明 TorchInductor 如何為 GPU 核心程式使用 Triton。
- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — 與手寫核心程式競爭的編譯器路徑的官方說明。

: Triton contributors，*Triton documentation*，見參考文獻。
