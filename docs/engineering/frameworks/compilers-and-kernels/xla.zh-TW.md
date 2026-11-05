---
translation_reviewed: 2026-11-04
last_reviewed: 2026-11-04
related:
  - engineering/hardware
tags:
  - engineering
  - frameworks
  - compilers
aliases:
  - XLA
  - Accelerated Linear Algebra
  - 加速線性代數
---

# XLA

XLA（Accelerated Linear Algebra，加速線性代數）是一個開源的機器學習編譯器。它接收模型的圖，加以最佳化，並為特定裝置產生程式碼。官方專案說明它可從 PyTorch、TensorFlow 與 JAX 使用，並由包括 Alibaba、Amazon Web Services、AMD、Apple、Arm、Google、Intel、Meta 與 NVIDIA 在內的硬體與軟體公司共同建立。

!!! info "屬於編譯器與核心程式"
    本方法頁屬於[編譯器與核心程式](index.zh-TW.md)。它詳細說明 XLA；上層頁面則比較它與其他系統。

## 問題

框架會產生一張張量運算的圖。若一次執行一個運算，每個中間結果都要先回到慢速記憶體，下一個運算才能讀取。為每個晶片手動最佳化每個模型無法擴展。XLA 同時處理這兩點：它為裝置編譯整張圖，因此由編譯器決定如何融合。

## 核心想法

把程式擷取為圖，降階到線性代數的中間表示，以一系列遍歷（pass）最佳化該表示，然後為目標後端產生程式碼。官方頁面表示，XLA「運用 MLIR 的能力」，把這些功能整合進單一編譯器工具鏈。後端可以替換，因此同一個前端可以服務 GPU、CPU 與機器學習加速器。

## 流程

1. 框架（例如 JAX）追蹤模型，並把圖交給 XLA。
2. XLA 把圖降階到其中間表示，XLA 文件稱之為 HLO。
3. 一系列最佳化遍歷在該表示上執行。官方頁面描述這些遍歷經過生產環境驗證，並提到模型平行化的自動分割。
4. 後端產生裝置程式碼，編譯後的程式在晶片上執行。

官方頁面連結到一份從 HLO 到可執行檔的流程說明，要了解這些步驟的細節，可以參考該說明。

## 結果

官方頁面描述的是系統本身，並未報告基準測試結果，因此本頁不提供加速倍數。它所作的主張著重於涵蓋範圍：XLA 已與 PyTorch、JAX 及 TensorFlow 整合，並支援 GPU、CPU 與機器學習加速器。

## 限制

- **編譯時間。** 事先編譯會在第一次呼叫時增加延遲，而形狀經常改變的圖會反覆重新編譯。
- **控制力低於手寫核心程式。** 編譯器依自己的規則選擇融合。需要特定分塊的工程師，仍可能需要手寫核心程式，如 [Triton](triton.zh-TW.md) 所示。
- **後端品質不一。** 新後端只有在其遍歷與核心程式成熟後才能達到全速。
- **結果的可攜性。** 速度取決於編譯器版本與後端，因此測量結果無法乾淨地跨堆疊轉移。

## 相關連結

- PyTorch 使用者的替代方案是 [torch.compile 與 TorchInductor](torch-compile.zh-TW.md)，它可以使用 Triton 核心程式。
- 晶片層級的融合討論，見[硬體協同設計](../../hardware/co-design/index.zh-TW.md)頁。
- 最常使用 XLA 的框架 JAX，列於[框架與工具](../index.zh-TW.md)。

## 未解問題

- 自動編譯器在新晶片上，能多接近手寫的注意力核心程式？
- 編譯器應如何處理動態形狀？它在服務中很常見，並會造成反覆編譯。

## 參考文獻

### 開創性論文

- Lattner, C. et al. (2020). *MLIR: A Compiler Infrastructure for the End of Moore's Law*. arXiv:2002.11054. https://arxiv.org/abs/2002.11054 — 描述 MLIR，即 XLA 官方頁面所說其所建立於其上的共用編譯器基礎架構。
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv:1802.04799. https://arxiv.org/abs/1802.04799 — 同樣為多種後端最佳化圖與運算的同期編譯器，可與 XLA 的設計比較。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — 說明融合核心程式的記憶體搬移論點，編譯器試圖自動重現它。

### 文件與說明

- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — XLA 的官方說明，包括其支援的框架、後端與最佳化遍歷。
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — torch.compile 及其後端選項的官方 PyTorch 文件，可與 XLA 的做法比較。
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — 與 XLA 等編譯器互補的手寫核心程式語言之官方文件。
