---
translation_reviewed: 2026-10-28
---

# TinyML 與行動端執行環境

TinyML 讓機器學習模型在只有幾 KB 記憶體的微控制器上執行。行動端執行環境則讓模型在手機與筆電上執行，並使用裝置的 CPU、GPU 與神經處理單元（NPU）。兩者都要把已訓練的模型放進固定的記憶體、運算與能源預算之中，而且都仰賴負責載入、排程與執行模型的執行環境。

## 概述

這個範圍的兩端相差好幾個數量級。微控制器是單一晶片，內含一顆小型處理器、數 KB 到數百 KB 的 SRAM 作為工作記憶體，而且常常沒有作業系統。手機則有數 GB 的記憶體、多核心 CPU、GPU 與 NPU，但記憶體要與作業系統及其他應用程式共用。MCUNet 論文指出，微控制器的記憶體比行動手機小兩到三個數量級。[^1]

執行環境是位於模型檔與硬體之間的軟體。它讀取裝置格式的模型，規劃中間結果存放的位置，為每個運算選擇實作方式，並在可能時把工作交給加速器。同一個網路在不同執行環境上的速度可能差很多，因此量測必須在目標裝置上進行，這也是[裝置端與邊緣 AI](index.zh-TW.md) 總覽所強調的。

## 關鍵概念

- **微控制器（MCU）**：包含處理器、用來存放程式碼與常數的晶片內快閃記憶體，以及作為工作記憶體的 SRAM 的晶片。許多微控制器執行裸機韌體或小型即時作業系統。
- **張量記憶區（tensor arena）**：一塊固定大小的 RAM，執行環境把中間激活值放在其中。由於它在推論開始前就已規劃完成，裝置執行時不需要再配置記憶體。
- **峰值記憶體**：執行過程中任一時刻佔用的最大記憶體量。它取決於中間激活值的大小，而不只是參數數量。MCUNetV2 論文發現，卷積網路的前幾個區塊通常決定了這個峰值。[^2]
- **核心函式庫（kernel library）**：針對某一類處理器最佳化過的卷積、矩陣乘法等運算實作。
- **委派模組（delegate）**：把模型計算圖的一部分交給 GPU 或 NPU 等加速器的外掛模組。委派模組不支援的運算子會在 CPU 上執行，而兩者之間頻繁切換所花的時間，可能超過加速器省下的時間。
- **事先轉換（ahead-of-time conversion）**：模型在送到裝置前就已完成轉換、量化與最佳化。相關的數值格式見[量化](../../theory/model-compression/quantisation/index.zh-TW.md)。

## 運作方式

部署分為四個階段：訓練、轉換、為目標執行環境打包，以及在裝置上執行。在裝置上量測則讓這個流程形成回饋。

```mermaid
flowchart LR
  T[已訓練的模型] --> C[轉換與量化]
  C --> P[為目標執行環境打包]
  P --> L[載入裝置]
  L --> A[規劃記憶體並分派運算子]
  A --> K[CPU 核心函式或 NPU 委派模組]
  K --> M[量測延遲、記憶體與能源]
```

在微控制器上，模型通常會以常數陣列的形式編譯進韌體，存放在快閃記憶體中。一個小型直譯器會走過計算圖，逐一執行運算子，並以張量記憶區作為工作記憶體。峰值記憶體由那些必須同時保存輸入與輸出的層決定。分塊排程（patch-based scheduling）的做法，是把較大的前段層切成小的空間區塊來計算，代價是在區塊重疊處重新計算部分數值，但能降低這個峰值。

行動端執行環境遵循同樣的模式，但機制更多：包括計算圖最佳化器、CPU 核心函式庫，以及 GPU 或 NPU 的委派模組。模型檔通常以記憶體映射（memory-mapped）的方式載入，因此作業系統只在讀取權重時才從儲存裝置載入。

## 關鍵方法

下面的執行環境以行內方式比較，因為它們目前都還沒有獨立頁面。

| 執行環境 | 目標裝置 | 模型格式 | 區別在哪裡 |
|---|---|---|---|
| TensorFlow Lite Micro | 沒有作業系統的微控制器 | TFLite flatbuffer | 直譯器設計成能在數 KB 記憶體中執行，並使用張量記憶區配置 |
| CMSIS-NN | Arm Cortex-M 處理器 | 微控制器執行環境使用的核心函式庫 | 手工最佳化的核心，可降低記憶體佔用並提高吞吐量 |
| LiteRT（原名 TensorFlow Lite） | Android、iOS 與嵌入式 Linux | `.tflite` | 跨平台執行環境，GPU 與 NPU 的委派模組由硬體廠商提供 |
| Core ML | iPhone、iPad、Mac 等 Apple 平台 | 轉換後的模型套件 | 平台專屬：框架會為每個模型在 CPU、GPU 與 Neural Engine 之間選擇 |
| ExecuTorch | 手機與嵌入式裝置 | 事先匯出的 PyTorch 程式 | 執行從 PyTorch 匯出的模型，並提供廠商加速器的後端 |
| ONNX Runtime Mobile | Android 與 iOS | 運算子集合縮減的 ONNX | ONNX Runtime 的精簡版本，提供加速器的執行提供者（execution provider） |

主要的選擇，在於平台專屬的執行環境與跨平台的執行環境之間。前者能充分發揮每種裝置的硬體，後者讓同一個模型檔可用於多種裝置，但通常會犧牲一些峰值速度。委派模組的涵蓋範圍，往往比峰值速度更重要。一個支援大多數運算子的 NPU 可能比 CPU 快很多，但如果計算圖中間出現一個不支援的運算子，模型就會被切成兩段，分別在不同的處理器上執行。

### 裝置端語言模型

語言模型讓問題變得不同，因為它們的權重很大，而且 [KV 快取](../../theory/models/transformer/kv-cache/index.zh-TW.md)會隨上下文增長。粗略估計，參數量為 N、以 b 位元儲存的模型，其權重約佔 N × b / 8 個位元組。因此一個 30 億參數的模型，以 4 位元儲存約需 1.5 GB，以 16 位元則約需 6 GB；這還沒有計入快取、激活值與作業系統。

有三種做法可以應對：

- **較小的架構**。MobileLLM 研究參數量在 10 億以下、適合行動端使用的語言模型，採用深而窄的設計、嵌入層共享與分組查詢注意力。[^3] Phi-3-mini 有 38 億參數，被描述為小到能部署在手機上。[^4]
- **低位元權重**。AWQ 是一種只量化權重的方法。它觀察到，大約 1% 的權重比其他權重重要得多，並以激活感知縮放（activation-aware scaling）保護它們。[^5]
- **從快閃記憶體串流載入**。「LLM in a flash」的做法是把參數存放在快閃儲存裝置中，需要時再載入 DRAM，因此參數量超過可用 DRAM 的模型仍可執行。

## 相關連結

生物神經系統在嚴格的能源預算內運算，記憶體與運算彼此緊密相鄰。[脈衝神經網路與神經形態硬體](../../brain-mind/snn-neuromorphic/index.zh-TW.md)走的是相近的路線：它們只在出現脈衝時運算，因此適合耗電很少、持續運作的感測。今日的 TinyML 系統使用傳統網路，但同樣要面對資料與運算應放在哪裡的問題。

壓縮提供模型。[模型壓縮](../../theory/model-compression/index.zh-TW.md)涵蓋量化、剪枝與蒸餾，而[知識蒸餾](knowledge-distillation.zh-TW.md)頁面提供部署時的筆記。大型模型的服務端技術見[推論最佳化](../inference-optimization/index.zh-TW.md)，行動 NPU 則列於 [AI 硬體](../hardware/index.zh-TW.md)。為小預算而設計的架構，例如 MobileNets，則見 [CNN 家族](../../theory/models/cnn/index.zh-TW.md)。

裝置端處理也改變了隱私：原始輸入留在裝置上，見[隱私與資料保護](../../society/privacy/index.zh-TW.md)。讓大量裝置保持模型更新，則是 [MLOps](../mlops/index.zh-TW.md) 所涵蓋的營運問題。

## 應用

- **持續感測**。關鍵字偵測、手勢偵測與異常偵測，在穿戴裝置與家電中的微控制器上執行。MLPerf Tiny 基準測試套件衡量這類超低功耗系統的準確度、延遲與能源消耗。[^6]
- **手機功能**。相機、文字與語音功能愈來愈多在裝置上執行，有 NPU 時就使用 NPU。Apple 關於其基礎模型的報告，描述了一個約 30 億參數的裝置端模型。
- **裝置端調適**。在裝置上訓練已在 256 KB 記憶體內示範成功，讓感測器能在不把資料送到伺服器的情況下，適應自身的資料。

## 開放問題

- 面對數千台、NPU 與執行環境版本各不相同的裝置，如何更新模型，並確認每台裝置的行為一致？
- 跨平台執行環境會縮小與平台專屬執行環境的差距嗎？還是為了速度，仍必須依賴廠商的委派模組？
- 隨著上下文視窗變長，KV 快取會不會超過裝置的記憶體？從快閃記憶體串流權重，是長久的解法嗎？

[^1]: Lin et al. (2020)，*MCUNet*。摘要指出，微控制器的記憶體比行動手機小「2 到 3 個數量級」。
[^2]: Lin et al. (2021)，*MCUNetV2*。摘要指出，CNN 前幾個區塊使用的記憶體，可能比網路其餘部分多一個數量級。
[^3]: Liu et al. (2024)，*MobileLLM*。摘要稱這個次十億參數的規模是「行動端部署的實用選擇」。
[^4]: Abdin et al. (2024)，*Phi-3 Technical Report*。摘要將 phi-3-mini 描述為參數量 38 億、「小到能部署在手機上」的模型。
[^5]: Lin et al. (2023)，*AWQ*。摘要指出，只保護 1% 的關鍵權重，就能大幅降低量化誤差。
[^6]: Banbury et al. (2021)，*MLPerf Tiny*。摘要將這套基準測試描述為衡量超低功耗 TinyML 系統的準確度、延遲與能源消耗。

## 參考文獻

### 重要論文

- Lin, J., Chen, W.-M., Lin, Y., Cohn, J., Gan, C. & Han, S. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. NeurIPS 2020. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — 把神經架構搜尋與輕量推論引擎一起設計，使 ImageNet 規模的模型能在微控制器上執行。
- Lin, J., Chen, W.-M., Cai, H., Gan, C. & Han, S. (2021). *MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning*. NeurIPS 2021. arXiv:2110.15352. https://arxiv.org/abs/2110.15352 — 指出 CNN 的前段區塊主導峰值記憶體，並提出逐塊推論以降低它。
- David, R. et al. (2021). *TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems*. MLSys 2021. arXiv:2010.08678. https://arxiv.org/abs/2010.08678 — 描述一個以直譯器為基礎、可在數 KB 記憶體內執行的微控制器推論框架。
- Lai, L., Suda, N. & Chandra, V. (2018). *CMSIS-NN: Efficient Neural Network Kernels for Arm Cortex-M CPUs*. arXiv:1801.06601. https://arxiv.org/abs/1801.06601 — 為 Arm Cortex-M 處理器設計的核心函式庫，可降低記憶體佔用並改善執行時間與能源使用。
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 為行動視覺設計的高效卷積架構，以深度可分離卷積為核心。
- Lin, J. et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. MLSys 2024. arXiv:2306.00978. https://arxiv.org/abs/2306.00978 — 針對大型語言模型的低位元僅權重量化，保護關鍵權重，目標是裝置端使用。
- Alizadeh, K. et al. (2023). *LLM in a flash: Efficient Large Language Model Inference with Limited Memory*. arXiv:2312.11514. https://arxiv.org/abs/2312.11514 — 把參數存放在快閃記憶體並按需載入，使執行超過 DRAM 容量的模型成為可能。
- Lin, J. et al. (2022). *On-Device Training Under 256KB Memory*. NeurIPS 2022. arXiv:2206.15472. https://arxiv.org/abs/2206.15472 — 以共同設計的演算法與系統，使微調能在 256 KB 記憶體內完成。

### 綜述與教科書

- Gholami, A. et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 綜述高效推論的量化方法，是上文轉換步驟的背景知識。

### 文章與文件

- Apple. *Core ML*. Apple Developer Documentation. https://developer.apple.com/documentation/coreml — Apple 官方參考文件，說明在其裝置上執行轉換後模型的框架。
- Banbury, C. et al. (2021). *MLPerf Tiny Benchmark*. arXiv:2106.07597. https://arxiv.org/abs/2106.07597 — 基準測試套件，衡量超低功耗機器學習系統的準確度、延遲與能源消耗。
- Abdin, M. et al. (2024). *Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone*. arXiv:2404.14219. https://arxiv.org/abs/2404.14219 — 介紹一個可在手機上執行、參數量為 38 億的模型的技術報告。
- Gunter, T. et al. (2024). *Apple Intelligence Foundation Language Models*. arXiv:2407.21075. https://arxiv.org/abs/2407.21075 — 描述一個約 30 億參數的裝置端模型，以及它如何針對推論最佳化。
- Liu, Z. et al. (2024). *MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases*. ICML 2024. arXiv:2402.14905. https://arxiv.org/abs/2402.14905 — 針對參數量在 10 億以下語言模型的架構研究，供行動端使用。
