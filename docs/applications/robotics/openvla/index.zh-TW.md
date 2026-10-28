---
translation_reviewed: 2026-10-28
related:
  - theory/models/multimodal
  - theory/models/llm
aliases:
  - OpenVLA
  - 開放視覺語言動作模型
---

# OpenVLA（Kim 等人，2024）

Kim 等人發表了 OpenVLA，這是一個擁有 70 億參數、開源的視覺語言動作模型。目標是讓研究者能檢視、微調與執行的模型，而不只是封閉的系統。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

最強的機器人視覺語言動作模型是封閉的，多數實驗室無法研究、調整或部署。問題在於：開放模型能否與大得多的封閉模型匹敵。

## 核心想法

OpenVLA 結合 Llama 2 語言骨幹，以及由 DINOv2 與 SigLIP 特徵構成的視覺編碼器。它以 97 萬筆真實機器人示範訓練。RT-2-X 有 550 億參數，論文報告 OpenVLA 在 29 項任務上比它高出 16.5% 的絕對成功率，參數量約少八倍。

## 程序

1. 以 97 萬筆真實機器人示範訓練語言與視覺骨幹。
2. 為新的機器人或任務微調。論文報告秩為 32 的低秩適應（LoRA）可達到與完整微調相近的成功率，而只訓練約 1.4% 的參數，不過其實驗在 A100 GPU 上執行。
3. 以量化部署模型：4 位元權重的表現與 bfloat16 相當，記憶體需求為 7.0 GB，而非 16.8 GB。

## 結果

論文報告，OpenVLA 在 29 項任務上比 RT-2-X 高出 16.5% 的絕對成功率，在 BridgeData V2 上有明顯提升（數字見圖 3）。RT-2-X 在語意泛化上仍較強，兩者在 Google 機器人上表現相當。LoRA 與量化結果見論文表 1 與表 2。

## 限制

- 結果限於作者測試過的基準與機器人。
- RT-2-X 在語意泛化上較強，因此優勢取決於任務。
- 論文的微調實驗在 A100 GPU 上執行，而非消費級硬體。
- 微調與部署比訓練便宜，但仍需要工程投入。

## 連結

- 作為比較對象的封閉模型是 [RT-2](../rt-2/index.md)。
- 視覺語言的部分見[多模態模型](../../../theory/models/multimodal/index.md)。
- 語言模型骨幹見[大型語言模型](../../../theory/models/llm/index.md)。

## 參考文獻

### 開創性論文

- Kim, M. J. et al. (2024). OpenVLA: An Open-Source Vision-Language-Action Model. arXiv. https://arxiv.org/abs/2406.09246 — 70 億參數的開放機器人控制模型，附檢查點與程式碼一併釋出。
- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — OpenVLA 所比較的封閉視覺語言動作模型。
- Padalkar, A. et al. (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — 來自 22 種機器人的共享資料集，即跨機器人訓練所用的資料。
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — 較晚的機器人基礎模型，供與開放替代方案比較。

### 教科書與綜述

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 基礎模型的報告，以及共享基礎模型的理由。
