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
  - torch.compile
  - TorchInductor
  - TorchDynamo
  - 編譯 PyTorch 模型
---

# torch.compile 與 TorchInductor

!!! info "屬於編譯器與核心程式"
    本方法頁隸屬於[編譯器與核心程式](index.zh-TW.md)。它詳細說明 PyTorch 的編譯器堆疊；上層頁面則比較它與其他系統。

`torch.compile` 是 PyTorch 用來編譯模型的入口，同時保留即時執行的 Python 程式設計風格。它用 TorchDynamo 擷取程式，用 AOTAutograd 事先擷取反向傳播，再把圖交給後端。預設後端是 TorchInductor，它能為多種加速器產生快速程式碼；對 NVIDIA、AMD 與 Intel GPU，則使用 OpenAI Triton 核心程式。

## 問題

PyTorch 的即時執行模式容易除錯，但它一次只執行一個運算，因此運算之間的中間結果要寫入慢速記憶體。編譯器可以融合運算，但必須擷取可能包含分支、呼叫外部程式碼並改變形狀的 Python 程式。問題在於：如何可靠地擷取程式，而不要求使用者改寫。

## 核心想法

追蹤執行模型的 Python 框架（frame），把張量運算記錄為圖，再編譯這張圖。遇到無法擷取的程式碼時，圖會在該處切開，其餘部分仍以 Python 執行。TorchDynamo 負責擷取，官方頁面說它「使用 CPython 的 Frame Evaluation API，安全地擷取 PyTorch 圖」。

## 程序

1. 使用者對模型或函式呼叫 `torch.compile`。
2. TorchDynamo 從 Python 位元組碼擷取前向圖。
3. AOTAutograd 事先擷取反向圖，使編譯器能同時最佳化兩個方向。
4. 後端編譯這些圖。預設為 TorchInductor，它產生程式碼，並為 GPU 呼叫 Triton 核心程式。
5. 可以改選其他後端，頁面列出的例子包括 cudagraphs、TensorRT、TVM 與 OpenVINO。

若擷取失敗，圖會被切成幾段。官方頁面把讀者導向其關於圖中斷（graph break）的指南，而非自行說明。

## 結果

官方文件說明了各組成部分與預設後端，並未報告基準測試結果。本頁不提供速度提升的數字。需要數據的讀者，應測量自己的模型並記錄 PyTorch 版本，因為結果會隨版本改變。

## 限制

- **圖中斷。** 無法擷取的程式碼會切開圖。許多中斷會降低效益，而找出它們需要花費心力。
- **編譯時間與重新編譯。** 輸入形狀改變可能觸發新的編譯。
- **依賴後端。** 速度取決於 TorchInductor 與目標 GPU 所用的 Triton 版本。
- **除錯。** 錯誤可能來自編譯器堆疊而非模型本身，比即時執行的錯誤更難追蹤。

## 關聯

- TorchInductor 為 GPU 產生程式碼所用的語言是 [Triton](triton.zh-TW.md)。
- JAX 使用者依賴的編譯器是 [XLA](xla.zh-TW.md)。
- 編譯器試圖重現的融合注意力核心程式，見[推論最佳化](../../inference-optimization/index.zh-TW.md)。

## 開放問題

- 實際模型有多常退回即時執行？每次中斷的代價是多少？
- 通用編譯器能否在最新的注意力變體上，與手工調校的核心程式相當？

## 參考文獻

### 開創性論文

- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — 能為多種後端最佳化圖與運算子的編譯器，也是 TorchInductor 後端清單中列出的系統之一。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — 核心程式層級的論點：減少記憶體流量能加速注意力，而編譯器試圖重現這一點。

### 文章與文件

- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — 官方說明 TorchDynamo、AOTAutograd、TorchInductor 與預設後端。
- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — 與 JAX 和 TensorFlow 使用的編譯器相比，供參考。
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — TorchInductor 用來產生 GPU 程式碼的核心程式語言官方文件。

: PyTorch，*torch.compiler: Compiling PyTorch models*，見參考文獻。
