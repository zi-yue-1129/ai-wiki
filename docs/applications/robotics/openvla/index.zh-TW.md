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

OpenVLA 建立在 Prismatic-7B 視覺語言模型上。它的視覺編碼器把 DINOv2 與 SigLIP 特徵依通道串接，由兩層 MLP 投影到語言模型中，再由 70 億參數的 Llama 2 骨幹生成動作 token（第 3.1 節）。論文拿它與擁有 550 億參數的封閉模型 RT-2-X 比較，報告 OpenVLA 在 29 項任務上的絕對成功率高出 16.5%（摘要）。

## 程序

1. **資料**：從 Open X-Embodiment 篩選 97 萬筆真實機器人示範。該資料集在撰寫時有超過 200 萬條軌跡、70 多個資料集。只保留具有第三人稱相機與單臂末端執行器控制的操作資料集。最終混合資料使用 27 個資料集（第 3.3 節，表 3）。DROID 以 10% 權重納入，並在訓練的最後三分之一移除。
2. **動作表示**：7 個動作維度各自離散為 256 個區間，均勻分布在第 1 與第 99 百分位數之間。Llama 分詞器的保留 token 太少，因此把 256 個最少使用的 token 覆寫為動作 token。訓練只對動作 token 使用下一個 token 的交叉熵損失（第 3.2 節）。
3. **訓練**：27 個 epoch，學習率固定為 2e-5 且不做 warmup，批次大小 2048，使用 64 顆 A100 GPU 訓練 14 天，約 21,500 A100 小時（第 3.4、3.5 節）。
4. **微調與部署**：為新的機器人或任務，秩為 32 的 LoRA 可達到與完整微調相近的成功率，同時只訓練約 1.4% 的參數。量化後的權重則可用較少記憶體部署（第 5.2、5.4 節）。

## 結果

在 BridgeData V2 WidowX 上（17 項任務，170 次執行），平均成功率分別為：RT-1-X 18.5 ± 2.7%、Octo 20.0 ± 2.6%、RT-2-X（55B）50.6 ± 3.5%，OpenVLA 為 70.6 ± 3.2%（表 4，圖 3）。在 29 項任務上（WidowX 17 項、Google 機器人 12 項），OpenVLA 的絕對成功率領先 RT-2-X 16.5 個百分點（摘要，第 1 節）。在 Google 機器人上，文字稱兩者表現相當（圖 4，表 6）。

RT-2-X 只在語意泛化上較高，作者將其歸因於與網路資料的共同訓練（第 5.1 節）。在微調任務上，摘要報告 OpenVLA 比 Diffusion Policy 高出 20.4%（第 5.2 節）。

Franka-Tabletop 任務上的微調結果（表 1 與表 2）：

| 策略 | 成功率 |
|---|---|
| 完整微調（約 71.9 億個可訓練參數） | 69.7 ± 7.2% |
| LoRA，秩 32（9,760 萬個可訓練參數，1.4%） | 68.2 ± 7.5% |
| Sandwich | 62.1 ± 7.9% |
| 凍結視覺 | 47.0 ± 6.9% |
| 只訓練最後一層 | 30.3 ± 6.1% |

LoRA 在單顆 A100 上訓練需要 10 至 15 小時，作者稱其運算量比完整微調少 8 倍（第 5.3 節）。在 8 項 BridgeData 任務（80 次執行，表 2）的量化測試中，bfloat16 為 71.3 ± 4.8%，記憶體 16.8 GB；int8 為 58.1 ± 5.1%，記憶體 10.2 GB；int4 為 71.9 ± 4.7%，記憶體 7.0 GB。

## 限制

- **輸入**：模型只接受單張影像。多張影像、本體感受與觀察歷史留待未來工作（第 6 節）。
- **速度**：在 RTX 4090 上以 bfloat16 執行約為 6 Hz，未使用編譯或推測解碼（第 3.5 節）。這對 ALOHA 這類 50 Hz 的高頻雙臂系統而言太慢（第 6 節）。在 A5000 上，8 位元推論只有 1.2 Hz 且會傷害表現；4 位元約為 3 Hz（第 5.4 節）。
- **可靠度**：作者表示，模型在所測任務上通常只達到「<90% 的成功率」（第 6 節）。
- **行為**：在狹窄、需要靈巧操作的任務上，Diffusion Policy 產生較平滑、較精確的軌跡（第 5.2 節）。RT-2-X 在語意泛化上領先（第 5.1 節）。
- **範圍**：結果限於作者測試過的基準與機器人；論文也指出仍有許多設計問題未被探討（第 6 節）。

## 連結

- 作為比較對象的封閉模型是 [RT-2](../rt-2/index.md)。
- 作為比較對象的擴散式策略是 [Diffusion Policy](../diffusion-policy/index.md)。
- 視覺語言的部分見[多模態模型](../../../theory/models/multimodal/index.md)。
- 語言模型骨幹見[大型語言模型](../../../theory/models/llm/index.md)。

## 參考文獻

### 開創性論文

- Kim, M. J. et al. (2024). OpenVLA: An Open-Source Vision-Language-Action Model. arXiv. https://arxiv.org/abs/2406.09246 — 70 億參數的開放視覺語言動作模型，與封閉的 550 億參數 RT-2-X 相比。
- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — OpenVLA 所比較的封閉視覺語言動作模型。
- Open X-Embodiment Collaboration (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — 涵蓋 22 種機器人本體的共享機器人資料集，是 OpenVLA 篩選訓練資料的來源。
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — 較晚的通用機器人策略，建立在視覺語言模型上，論文稱之為視覺語言動作流模型。

### 教科書與綜述

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 關於基礎模型能力、技術原理與風險的報告，機器人是其中的應用領域之一。
