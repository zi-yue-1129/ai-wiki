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
  - LiteRT
  - TensorFlow Lite
  - TFLite
  - 輕量執行環境
---

# LiteRT

LiteRT 是 Google 的裝置端機器學習執行環境，是 TensorFlow Lite 的後繼者。它載入緊湊的 `.tflite` 格式模型並在裝置上執行，可使用 CPU，或 GPU 與神經處理單元（NPU）上的硬體加速。官方頁面列出 CPU、GPU 與 NPU 加速，以及從 PyTorch、TensorFlow 與 JAX 的匯出路徑，三者都會把模型轉為 `.tflite` 格式。

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 LiteRT；上層頁面則比較各執行環境。

## 問題

在資料中心框架中訓練的模型很大，使用 32 位元浮點數，並依賴手機執行效率不佳的運算子。要把它出貨到裝置上，就得轉為較小的格式、在各手機差異很大的硬體上執行，並讓應用程式維持在裝置的記憶體與電量範圍內。每部手機的 CPU、GPU 與 NPU 組合不同，因此執行環境必須為每個運算子選擇最佳單元，而開發者不必為每種晶片撰寫不同的程式碼。

## 核心想法

把訓練好的模型一次性轉為 `.tflite` 檔案，使執行環境能有效地載入。執行時，直譯器執行圖。對每個運算子，它詢問加速器委派（delegate）能否執行：支援的運算子交給 GPU 或 NPU，其餘在 CPU 上執行。開發者只需撰寫一個應用程式，映射工作由執行環境處理。

## 流程

1. 在 PyTorch、TensorFlow 或 JAX 中訓練模型，並匯出為 `.tflite` 格式。
2. 將模型量化，通常為 8 位元整數；必要時使用校準資料。
3. 在應用程式中載入檔案並建立直譯器。
4. 若裝置有 GPU 或 NPU，則掛載對應的委派。
5. 執行推論，並在每個目標裝置上測量延遲與記憶體。

## 結果

官方頁面描述了執行環境在 CPU、GPU 與 NPU 上的加速，以及它的匯出路徑。本頁所依據的資料並未發表基準測試數字，因此本頁不提供加速倍數。需要數字的讀者，應以出貨時所用的委派，在目標手機上測量模型。

## 限制

- **運算子涵蓋範圍。** 委派只支援部分運算子。模型若使用不支援的運算子，圖就會被切開，每個切口都會在 CPU 與加速器之間增加一次複製。
- **量化的工作量。** 整數模型需要校準，有些層量化後會損失準確率，因此轉換不一定只是一個步驟。
- **裝置差異。** 同一個模型在不同手機上速度可能差很多，取決於裝置支援哪種委派。
- **大型語言模型。** 此執行環境是為能放進裝置記憶體的模型設計的。大型語言模型需要[裝置端與邊緣 AI](../index.zh-TW.md)頁所涵蓋的快取與量化選擇。

## 相關連結

- 量化步驟依賴 [Jacob 等人（2017）](https://arxiv.org/abs/1712.05877) 的整數運算。
- 適合此執行環境的高效架構，見 [CNN 家族](../../../theory/models/cnn/index.zh-TW.md)，其中 MobileNets 是標準範例。
- 以 PyTorch 為優先的替代方案，見 [ExecuTorch](executorch.zh-TW.md)。
- 最小的裝置，見 [MCUNet](mcunet.zh-TW.md)。

## 未解問題

- 當快速的 NPU 委派只支援較少運算子，而較慢的 GPU 委派涵蓋較多時，執行環境應如何選擇？
- 轉換步驟能否在出貨前檢查，所選委派是否能執行整個模型？

## 參考文獻

### 開創性論文

- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 本執行環境所設計執行的高效架構，使用深度可分離卷積。
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 8 位元行動部署背後的整數量化方案。
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — 在模型轉為裝置格式之前縮小模型的壓縮方法。

### 文件與說明

- Google. *LiteRT: High-Performance On-Device Machine Learning Framework*. https://developers.google.com/edge/litert — 此執行環境的官方頁面，包括其 CPU、GPU 與 NPU 加速，以及從 PyTorch、TensorFlow 與 JAX 的匯出路徑。
- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — PyTorch 邊緣執行環境，從 PyTorch 匯出路徑處理同一個部署問題。
