---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/on-device-edge
  - engineering/hardware
tags:
  - engineering
  - on-device
  - tinyml
aliases:
  - MCUNet
  - 微型深度學習
  - 微控制器網路
---

# MCUNet

!!! info "屬於 TinyML 與行動執行環境"
    本方法頁隸屬於[TinyML 與行動執行環境](index.zh-TW.md)。它詳細說明 MCUNet；上層頁面則把它與各種執行環境比較。

MCUNet 是一套在微控制器上執行影像分類的系統。微控制器只有幾百 KB 的 SRAM 與約 1 MB 的快閃記憶體。它不是事後縮小大型網路，而是在某一款裝置的限制下，同時設計網路與推論的記憶體排程。論文報告，在一顆具有 320 kB SRAM 與 1 MB 快閃記憶體的微控制器上，ImageNet 分類的 top-1 準確度超過 70%。

## 問題

標準的影像分類器有數十 MB 的權重，以及很大的啟動值張量。微控制器的記憶體兩者都放不下，因此常見的做法，也就是剪枝或量化大型模型，並不足夠：推論過程中的峰值啟動值記憶體也必須放得下。若在設計完成後才縮小網路，常常浪費了預算，因為架構並不是依照裝置實際擁有的記憶體來選擇的。

## 核心想法

MCUNet 有兩個共同設計的部分。TinyNAS 在小型網路的空間中搜尋，找出最符合目標裝置記憶體與運算預算的網路。TinyEngine 是一個推論函式庫，它為該網路安排運算，以降低峰值記憶體，並避免一般執行環境所需的動態配置。搜尋與排程器共用同一個目標，因此網路是依照排程器真正能提供的記憶體來選擇的。

## 程序

1. 定義裝置預算，即 SRAM 與快閃記憶體的大小，以及目標準確度任務。
2. 在網路架構空間中搜尋，並以預算作為限制條件。
3. 為選定的網路產生記憶體規劃，使每一層的啟動值重複使用固定的緩衝區。
4. 把網路編譯成不需動態配置記憶體的程式。
5. 在裝置上量測準確度與峰值記憶體。

## 結果

論文報告，在一顆具有 320 kB SRAM 與 1 MB 快閃記憶體的微控制器上，ImageNet top-1 準確度超過 70%。同一研究也報告了其他預算與任務的結果，並把設計出的網路與無法放進該裝置的標準架構做比較。數字取決於裝置與軟體版本，因此讀者應以論文的表格為準，不應把單一的主要結果當成一般的速度或準確度主張。

## 限制

- **只適用一類裝置。** 網路是為固定的記憶體預算設計的。較大的裝置需要重新搜尋，而不是把舊模型等比放大。
- **準確度上限。** 即使經過共同設計，微控制器在同一任務上的準確度仍低於手機等級的模型。
- **任務範圍。** 結果針對影像分類。偵測、語音與語言模型的記憶體特性不同，本方法並未直接處理。
- **維護成本。** 每一款新裝置、新任務或每次軟體更新，都可能需要重新搜尋與量測。

## 關聯

- 高效行動網路所用的深度可分離卷積，是 [MobileNets](https://arxiv.org/abs/1704.04861) 的基本單元，見 [CNN 家族](../../../theory/models/cnn/index.zh-TW.md)。
- 微控制器所用的整數運算，是 [Jacob 等人（2017）](https://arxiv.org/abs/1712.05877) 的主題。
- 手機上需要把模型對應到多種加速器的執行環境，見 [LiteRT](litert.zh-TW.md) 與 [ExecuTorch](executorch.zh-TW.md)。

## 開放問題

- 搜尋能否一次涵蓋多種裝置預算，使一次搜尋服務一整個微控制器系列？
- 當記憶體排程還必須與韌體的其他部分共用 SRAM 時，準確度會損失多少？

## 參考文獻

### 重要論文

- Lin, J. et al. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. NeurIPS 2020. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — 主要論文：為微控制器設計的共同架構搜尋與推論函式庫，並提供 320 kB SRAM 上的 ImageNet 結果。
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — 高效的卷積基準，其深度可分離區塊使小型網路得以實用。
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — 僅使用整數的推論，是微控制器運算單元所需的基礎。
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — MCUNet 的設計避免單獨依賴的壓縮方法。

### 文章與文件

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — 具有 Cortex-M 後端之執行環境的官方文件，可與共同設計的微控制器技術堆疊比較。
