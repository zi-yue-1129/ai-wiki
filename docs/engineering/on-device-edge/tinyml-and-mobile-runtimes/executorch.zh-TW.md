---
translation_reviewed: 2026-11-04
last_reviewed: 2026-11-04
related:
  - engineering/on-device-edge
  - engineering/frameworks
  - engineering/hardware
tags:
  - engineering
  - on-device
  - runtimes
aliases:
  - ExecuTorch
  - PyTorch edge runtime
  - 邊緣端執行環境
---

# ExecuTorch

ExecuTorch 是 PyTorch 的裝置端推論執行環境。PyTorch 模型會事先匯出為緊湊的程式，由小型執行環境在裝置上載入，並透過可插拔的後端執行。官方文件列出三個設計目標：可攜性、效能與生產力。它把可攜性描述為能在「從高階行動裝置到受限的微控制器」上執行。

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 ExecuTorch；上層頁面則比較各執行環境。

## 問題

以 PyTorch 訓練的團隊需要把同一個模型出貨到手機、筆電與微控制器。每個目標都有自己的加速器與執行環境，因此每一個都要獨立的匯出路徑，會使工作量加倍，而且匯出的模型可能與測試過的模型不同。執行環境必須讓模型忠於訓練圖，同時讓每個裝置使用自己的硬體。

## 核心想法

用 PyTorch 的事先匯出工具，把模型匯出為執行環境能在沒有 Python 直譯器的情況下執行的圖。把圖降階到目標裝置的後端，後端保留它支援的部分，其餘部分交給可攜的預設實作。執行環境很小，不依賴大型框架，適合記憶體有限的裝置。官方文件描述此執行環境在 CPU、GPU、NPU 與 DSP 目標上提供硬體加速。

## 流程

1. 在 PyTorch 中撰寫並訓練模型。
2. 用事先匯出工具匯出模型，使圖固定下來。匯出建立於 [torch.compile 與 TorchInductor](../../frameworks/compilers-and-kernels/torch-compile.zh-TW.md) 所述的圖擷取之上。
3. 把匯出的圖降階到一個或多個目標裝置的後端。
4. 把程式序列化為裝置執行環境載入的檔案。
5. 在裝置上執行程式，並將其輸出與 PyTorch 模型比對。

## 後端

官方文件列出了一組後端，名稱包括 XNNPACK、Core ML、Vulkan、Qualcomm AI Engine、MediaTek、OpenVINO、Arm Ethos-U 與 Arm Cortex-M。官方文件並未為每個後端說明目標硬體，因此部署前應先查閱該後端的頁面。

## 結果

官方文件描述了設計目標、後端與部署步驟。本頁所依據的資料並未報告基準測試數字，因此本頁不提供速度或記憶體數字。對專案真正重要的比較，是在目標裝置上以相同輸入測量各後端。

## 限制

- **後端支援不一。** 支援的運算子與硬體取決於後端與版本，因此同一個模型可能在某裝置上完整執行，在另一裝置上只能部分執行。
- **匯出的嚴格性。** 事先匯出需要能被擷取的圖，因此動態控制流必須改寫或受限制。
- **較新的堆疊。** 與 LiteRT 相比，PyTorch 邊緣堆疊較新，介面變動也較頻繁。
- **驗證。** 應在每個後端上，把匯出程式的輸出與原始模型比對，因為降階可能改變數值結果。

## 相關連結

- 與此層相關的編譯器層，見 [torch.compile 與 TorchInductor](../../frameworks/compilers-and-kernels/torch-compile.zh-TW.md)。
- 以轉換器與委派為基礎的行動替代方案是 [LiteRT](litert.zh-TW.md)。
- 最小的裝置需要協同設計的模型，見 [MCUNet](mcunet.zh-TW.md)。

## 未解問題

- 同一個匯出的圖，能否同時服務手機 NPU 與微控制器，而不必為每種裝置各自做降階？
- 團隊應如何在許多後端上測試，確認匯出的程式與訓練模型一致？

## 參考文獻

### 開創性論文

- Ansel, J. et al. (2024). *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*. ASPLOS 2024. https://doi.org/10.1145/3620665.3640366 — 描述 PyTorch 匯出工具所建立於其上的圖擷取與編譯設計。
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 整數量化，部分 ExecuTorch 後端用於 NPU 與微控制器。
- Lin, J. et al. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — 微控制器的案例，Arm Cortex-M 後端從執行環境端處理這個問題。

### 文件與說明

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — 執行環境的官方文件，包括其設計目標、後端與部署步驟。
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — PyTorch 編譯器文件，涵蓋匯出所建立於其上的圖擷取。
- Google. *LiteRT: High-Performance On-Device Machine Learning Framework*. https://developers.google.com/edge/litert — 替代的行動執行環境，可與 ExecuTorch 的後端模型比較。
