---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
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
  - PyTorch 邊緣執行環境
  - 邊緣端執行環境
---

# ExecuTorch

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁隸屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 ExecuTorch；上層頁面則比較它與其他執行環境。

ExecuTorch 是 PyTorch 的裝置端推論執行環境。PyTorch 模型會先預先匯出為精簡的程式，再由一個小型執行環境透過可插拔的後端在裝置上載入與執行。官方文件列出三個設計目標：可攜性、效能與生產力。它的後端包括用於 CPU 的 XNNPACK、用於 GPU 的 Core ML 與 Vulkan、用於 Qualcomm 與 MediaTek NPU 的後端，以及用於微控制器的 Arm Ethos-U 與 Cortex-M 目標。

## 問題

以 PyTorch 訓練的團隊，需要把同一個模型出貨到手機、筆電與微控制器上。每個目標都有自己的加速器與執行環境，若為每一個目標各建一條匯出路徑，工作量就會翻倍，而且匯出後的模型可能與測試過的模型不同。執行環境必須讓模型忠於訓練時的計算圖，同時讓每個裝置使用自己的硬體。

## 核心想法

使用 PyTorch 的預先匯出工具，把模型匯出為執行環境能在沒有 Python 直譯器的情況下執行的計算圖。接著把計算圖降階到目標裝置的後端，後端保留它支援的部分，其餘則留給可攜的預設路徑執行。執行環境很小，不依賴大型框架，適合記憶體有限的裝置。

## 程序

1. 以 PyTorch 撰寫並訓練模型。
2. 使用預先匯出工具匯出模型，使計算圖固定下來。
3. 把匯出的計算圖降階到一個或多個適用於目標裝置的後端。
4. 把程式序列化為裝置執行環境可以載入的檔案。
5. 在裝置上執行程式，並把輸出與 PyTorch 模型比對。

## 結果

官方文件描述了設計目標、後端與部署步驟。本頁所依據的資料未報告基準測試數字，因此本頁不提供速度或記憶體的數據。對專案而言，真正重要的比較是在目標裝置上、以相同輸入量測各後端的表現。

## 限制

- **後端支援不一。** 支援的運算子與硬體取決於後端與發行版本，因此模型可能在某一裝置上完整執行，在另一裝置上只能部分執行。
- **匯出的嚴格性。** 預先匯出需要能被擷取的計算圖，因此動態的控制流程必須改寫或加以限制。
- **較新的技術堆疊。** 與 LiteRT 相比，PyTorch 的邊緣堆疊較新，介面變動也較頻繁。
- **驗證。** 降階可能改變數值結果，因此每個後端上匯出程式的輸出，都應與原始模型比對。

## 關聯

- 匯出與計算圖擷取步驟，與[torch.compile 與 TorchInductor](../../frameworks/compilers-and-kernels/torch-compile.zh-TW.md)所述的編譯器層有關。
- 以轉換器與委派為核心的行動替代方案，見 [LiteRT](litert.zh-TW.md)。
- 最小的裝置，需要共同設計的模型，見 [MCUNet](mcunet.zh-TW.md)。

## 開放問題

- 單一匯出的計算圖，能否同時服務手機 NPU 與微控制器，而不需要為每一種裝置另建降階路徑？
- 團隊應如何測試，確認匯出程式在多個後端上與訓練模型的結果一致？

## 參考文獻

### 重要論文

- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 整數量化，多個 ExecuTorch 後端在 NPU 與微控制器上使用它。
- Lin, J. et al. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. NeurIPS 2020. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — 微控制器的案例，Cortex-M 與 Ethos-U 後端從執行環境端處理這個問題。

### 文章與文件

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — 此執行環境的官方文件，包括其設計目標、後端與部署步驟。
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — PyTorch 編譯器的文件，涵蓋匯出所依據的計算圖擷取。
- Google. *LiteRT: On-device AI runtime*. https://developers.google.com/edge/litert — 另一種行動執行環境，可與 ExecuTorch 的後端模型比較。
