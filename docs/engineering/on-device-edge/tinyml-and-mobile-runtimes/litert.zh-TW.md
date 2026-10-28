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
  - LiteRT
  - TensorFlow Lite
  - TFLite
  - 輕量執行環境
---

# LiteRT

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁隸屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 LiteRT；上層頁面則比較它與其他執行環境。

LiteRT 是 Google 的裝置端機器學習執行環境，前身為 TensorFlow Lite。它以精簡的 flatbuffer 格式載入模型，並在裝置上執行，運算時可使用 CPU，或透過硬體委派使用 GPU 與神經處理單元（NPU）。官方頁面表示，它能在具有 CPU、GPU 與 NPU 加速的多種裝置上執行模型，並列出從 PyTorch、TensorFlow 與 JAX 匯出的路徑。

## 問題

在資料中心框架中訓練的模型體積大、使用 32 位元浮點數，而且依賴手機執行效率不佳的運算子。要把它出貨到裝置上，必須轉換為較小的格式，在因手機而異的硬體上執行，並讓應用程式符合裝置的記憶體與電池限制。每支手機的 CPU、GPU 與 NPU 組合不同，因此執行環境必須為每個運算子選出最合適的單元，而開發者不需要為每種晶片撰寫不同的程式。

## 核心想法

把訓練好的模型一次轉換為 flatbuffer 檔案，執行環境可以直接對映到記憶體，無需長時間解析。執行時，直譯器執行計算圖；對每個運算子，它會詢問委派加速器能否執行。支援的運算子送到 GPU 或 NPU，其餘在 CPU 上執行。開發者只需撰寫一個應用程式，對映則由執行環境處理。

## 程序

1. 以 PyTorch、TensorFlow 或 JAX 訓練模型，並匯出為執行環境的格式。
2. 量化模型，通常為 8 位元整數，必要時使用校準資料。
3. 在應用程式中載入檔案並建立直譯器。
4. 若裝置有 GPU 或 NPU，則附加對應的委派。
5. 執行推論，並在每一款目標裝置上量測延遲與記憶體。

## 結果

官方頁面描述了此執行環境在 CPU、GPU 與 NPU 上的加速，以及其匯出路徑。本頁所依據的資料未公布基準測試數字，因此本頁不提供速度提升的數據。需要具體數字的讀者，應在要出貨的手機上，以即將使用的委派量測模型。

## 限制

- **運算子覆蓋範圍。** 委派只支援部分運算子。模型若使用不支援的運算子，計算圖會被切分，每個切分點都會在 CPU 與加速器之間增加一次資料複製。
- **量化的工作量。** 整數模型需要校準，部分層量化後會損失準確度，因此轉換不一定只是一個步驟。
- **裝置差異。** 同一個模型在某支手機上快，在另一支上卻可能慢，取決於該裝置支援哪種委派。
- **大型語言模型。** 此執行環境是為能放進裝置記憶體的模型設計的。大型語言模型需要[裝置端與邊緣 AI](../index.zh-TW.md)頁面所述的快取與量化選擇。

## 關聯

- 量化步驟依賴 [Jacob 等人（2017）](https://arxiv.org/abs/1712.05877) 的整數運算方法。
- 適合此執行環境的高效架構，見 [CNN 家族](../../../theory/models/cnn/index.zh-TW.md)，其中 MobileNets 是標準範例。
- 以 PyTorch 為優先的替代方案，見 [ExecuTorch](executorch.zh-TW.md)。
- 最小的裝置，見 [MCUNet](mcunet.zh-TW.md)。

## 開放問題

- 執行環境應如何在「NPU 快但支援的運算子少」與「GPU 慢但覆蓋較廣」之間做選擇？
- 轉換步驟能否在出貨前，先檢查所選委派是否能執行整個模型？

## 參考文獻

### 重要論文

- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 此執行環境所要執行的高效架構，使用深度可分離卷積。
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 行動端 8 位元部署所依據的整數量化方案。
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — 在轉換為裝置格式之前，用來縮減模型的壓縮方法。

### 文章與文件

- Google. *LiteRT: On-device AI runtime*. https://developers.google.com/edge/litert — 此執行環境的官方頁面，涵蓋 CPU、GPU 與 NPU 加速，以及匯出路徑。
- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — PyTorch 的邊緣執行環境，從 PyTorch 匯出路徑處理同一個部署問題。
