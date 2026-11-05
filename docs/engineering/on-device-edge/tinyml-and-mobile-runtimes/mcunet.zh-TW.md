---
translation_reviewed: 2026-11-04
last_reviewed: 2026-11-04
related:
  - engineering/on-device-edge
  - engineering/hardware
tags:
  - engineering
  - on-device
  - tinyml
aliases:
  - MCUNet
  - Tiny deep learning
  - 微控制器網路
---

# MCUNet

MCUNet 是在微控制器上執行影像分類的系統。微控制器只有數百 kB 的 SRAM 與約 1 MB 的快閃記憶體。它把網路與推論記憶體排程一起設計，並在特定裝置的限制下進行，而不是事後把大型網路縮小。論文報告在 STM32H743 微控制器（512 kB SRAM、2 MB 快閃記憶體）上達到 70.7% 的 ImageNet top-1 準確率。

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 MCUNet；上層頁面則比較各執行環境。

## 問題

標準的影像分類器有數十 MB 的權重與很大的激活張量。微控制器的記憶體兩者都放不下，因此常見的剪枝或量化大型模型的做法並不足夠：推論時的峰值激活記憶體也必須放得進去。事後縮小網路往往浪費預算，因為架構並不是依裝置的記憶體來選擇的。

## 核心想法

MCUNet 有兩個一起設計的部分。TinyNAS 是兩階段的神經架構搜尋：先縮小搜尋空間，使其符合目標的嚴格記憶體限制，再在該空間中搜尋模型。TinyEngine 是記憶體高效的推論引擎，它利用整個網路的結構來排程計算，使峰值記憶體維持在低水準。搜尋與引擎彼此為對方而設計，因此所選的網路，正是引擎能實際提供的記憶體所能承載的網路。

## 流程

1. 定義裝置預算：SRAM 與快閃記憶體大小，以及任務，此處為 ImageNet 等級的分類。
2. 執行 TinyNAS，找出符合預算的網路架構。
3. 為所選網路產生記憶體計畫，使每一層的激活重用一組固定的緩衝區。
4. 把網路編譯為依記憶體計畫執行的程式。
5. 在裝置上測量準確率與峰值記憶體。

## 結果

論文的主要結果是 70.7% 的 ImageNet top-1 準確率，報告於 STM32H743 微控制器（512 kB SRAM、2 MB 快閃記憶體）上。論文其他結果預設使用的板子是 STM32F746，其 SRAM 為 320 kB、快閃記憶體為 1 MB；摘要並報告，相較於量化的 MobileNetV2 與 ResNet-18，MCUNet 使用的 SRAM 少 3.5 倍、快閃記憶體少 5.7 倍。確切數字取決於板子與軟體版本，讀者應以論文的表格為準，而不要只看單一的主要數字。

## 限制

- **只針對一類裝置。** 網路是依固定的記憶體預算設計的。較大的裝置需要重新搜尋，而不是把網路等比放大。
- **準確率上限。** 即使經過協同設計，微控制器在同一任務上的準確率仍低於手機等級的模型。
- **任務範圍。** 結果針對影像分類。偵測、語音與語言模型的記憶體特性不同，本方法並未直接處理。
- **維護成本。** 每次新裝置、新任務或軟體更新，都可能需要各自的搜尋與測量。

## 後續工作

後續研究 [MCUNetV2](https://arxiv.org/abs/2110.15352) 以逐塊（patch-based）推論降低峰值記憶體，即一次只計算特徵圖的一部分。其摘要報告，對既有網路可降低 4 至 8 倍的峰值記憶體，並在微控制器上達到 71.8% 的 ImageNet top-1 準確率。本 wiki 目前尚未為它另設頁面。

## 相關連結

- 高效行動網路所用的深度可分離卷積，是 [MobileNets](https://arxiv.org/abs/1704.04861) 的基本構件，見 [CNN 家族](../../../theory/models/cnn/index.zh-TW.md)。
- 微控制器所用的整數運算，正是 [Jacob 等人（2017）](https://arxiv.org/abs/1712.05877) 的研究背景。
- 在手機上，執行環境會把模型對應到多種加速器，見 [LiteRT](litert.zh-TW.md) 與 [ExecuTorch](executorch.zh-TW.md)。

## 未解問題

- 搜尋能否同時涵蓋多種裝置預算，使一次搜尋服務一整個微控制器系列？
- 當記憶體排程還必須與韌體的其他部分共用 SRAM 時，準確率會損失多少？

## 參考文獻

### 開創性論文

- Lin, J., Chen, W.-M., Lin, Y., Cohn, J., Gan, C. & Han, S. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — 主要論文：為微控制器設計的協同架構搜尋（TinyNAS）與推論引擎（TinyEngine），並報告 STM32H743 上的 70.7% 結果。
- Lin, J., Chen, W.-M., Cai, H., Gan, C. & Han, S. (2021). *MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning*. arXiv:2110.15352. https://arxiv.org/abs/2110.15352 — MCUNet 的後續研究，以逐塊推論降低峰值記憶體，並在微控制器上報告 71.8% 的 ImageNet top-1 準確率。
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 提出用於高效視覺網路的深度可分離卷積，是許多微型網路的基本構件。
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 描述僅以整數運算的量化推論，即微控制器部署所依賴的運算方式。
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — MCUNet 的協同設計刻意不只依賴的壓縮方法。

### 文件與說明

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — 具 Arm Cortex-M 後端之執行環境的官方文件，可與協同設計的微控制器堆疊比較。
