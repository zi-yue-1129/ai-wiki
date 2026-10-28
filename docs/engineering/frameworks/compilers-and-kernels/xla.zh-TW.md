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
  - XLA
  - 加速線性代數
  - Accelerated Linear Algebra
---

# XLA

!!! info "屬於編譯器與核心程式"
    本方法頁隸屬於[編譯器與核心程式](index.zh-TW.md)。它詳細說明 XLA；上層頁面則比較它與其他系統。

XLA（Accelerated Linear Algebra，加速線性代數）是一個開源的機器學習編譯器。它接收模型的計算圖、加以最佳化，並為特定裝置產生程式碼。它是 JAX 與 TensorFlow 加速路徑背後的編譯器，PyTorch 也能把它當作後端使用。官方說明指出，它由 Alibaba、AMD、Google、Intel、Meta 與 NVIDIA 等公司共同開發。

## 問題

框架會產生一張張量運算的圖。若逐一執行每個運算，每個中間結果都要先寫回慢速記憶體，下一個運算才能讀取。為每個晶片手工最佳化每個模型，難以擴展。XLA 的解法是為裝置編譯整張圖，由編譯器決定如何融合運算。

## 核心想法

把程式擷取為圖，降階為線性代數的中間表示，以一系列最佳化步驟處理該表示，再為目標後端產生程式碼。後端是可插拔的，因此同一個前端可以服務 GPU、CPU 與加速器。

## 程序

1. 框架（例如 JAX）追蹤模型，並把計算圖交給 XLA。
2. XLA 把計算圖降階為它的中間表示。
3. 一系列最佳化步驟在該表示上執行。官方頁面提到經過實際生產環境驗證的最佳化步驟，以及為模型平行化而做的自動分割。
4. 後端產生裝置程式碼，編譯後的程式在晶片上執行。

在 XLA 的文件中，中間表示稱為 HLO，官方頁面也連結到從 HLO 到可執行檔的導覽。該頁面說明 XLA 運用了 MLIR，一種共用的編譯器基礎架構。

## 結果

官方頁面是對系統的描述，並未報告基準測試結果，因此本頁不提供速度提升的數字。頁面所列的主張是關於覆蓋範圍：XLA 已整合進 PyTorch、JAX 與 TensorFlow，並支援 GPU、CPU 與 ML 加速器。

## 限制

- **編譯時間。** 事前編譯會增加第一次呼叫的延遲，而形狀經常改變的圖會反覆重新編譯。
- **控制力低於手寫核心程式。** 編譯器依自己的規則選擇融合方式。需要特定分塊的工程師，仍可能需要手寫核心程式，例如 [Triton](triton.zh-TW.md)。
- **後端品質不一。** 新後端只有在其最佳化步驟與核心程式成熟後，才能達到完整速度。
- **結果的可攜性。** 速度取決於編譯器版本與後端，因此測量結果無法乾淨地在不同的軟體環境之間轉移。

## 關聯

- PyTorch 使用者的替代方案是 [torch.compile 與 TorchInductor](torch-compile.zh-TW.md)。
- 晶片層級的融合，見[硬體與模型共同設計](../../hardware/co-design/index.zh-TW.md)頁面。
- 最常使用 XLA 的框架 JAX，列在[框架與工具](../index.zh-TW.md)中。

## 開放問題

- 自動編譯器能在新晶片上與手寫注意力核心程式相差多遠？
- 編譯器應如何處理動態形狀？動態形狀在服務中很常見，並會導致重複編譯。

## 參考文獻

### 開創性論文

- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — 同時期的編譯器，也為多種後端最佳化圖與運算子，可與 XLA 的設計比較。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — 說明融合核心程式的記憶體流量論點，而編譯器試圖自動重現這一點。

### 文章與文件

- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — XLA 的官方說明，包括其支援的框架、後端與最佳化步驟。
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — 官方的 torch.compile 文件，說明後端選項，可與 XLA 的做法比較。
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — 與 XLA 等編譯器互補的手寫核心程式語言的官方文件。

: OpenXLA，*XLA: Optimized compiler for machine learning*，見參考文獻。
