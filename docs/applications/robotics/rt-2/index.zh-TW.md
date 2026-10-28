---
translation_reviewed: 2026-10-28
related:
  - theory/models/multimodal
  - theory/models/llm
aliases:
  - RT-2
  - Vision-language-action model
  - 視覺語言動作模型
---

# RT-2：視覺語言動作模型（Brohan 等人，2023）

Brohan 等人想知道：在網路資料上預訓練的視覺語言模型，能否直接控制機器人。他們的答案是 RT-2，它把機器人動作寫成文字 token，因此同一個模型同時處理語言與控制。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

只用機器人資料訓練的機器人，對日常任務所需的物件、概念與推理所知有限。大型視覺語言模型知識豐富，但輸出的是文字，而不是馬達指令。

## 核心想法

RT-2 把網路預訓練的視覺語言模型，與機器人軌跡以及一般的視覺語言任務（例如視覺問答）一起共同微調（co-fine-tuning）。機器人動作寫成文字 token，因此與語言共用同一種格式。作者把這類模型稱為視覺語言動作（VLA）模型。

## 程序

1. 從大量網路影像與文字資料上預訓練的視覺語言模型開始。論文使用 PaLI-X 與 PaLM-E。
2. **動作表示**：每個動作由 8 個整數組成，分別是終止旗標、6 自由度的末端執行器位移，以及夾爪伸展量。每個連續維度均勻離散為 256 個區間，再把整數寫成文字 token。
3. **共同微調**：把機器人資料與網路視覺語言資料一起訓練。機器人資料在混合資料中的比例，RT-2-PaLI-X 約為 50%，RT-2-PaLM-E 約為 66%（附錄 B）。
4. 執行時，依相機影像與指令生成動作 token，再解碼成機器人指令。在機器人動作提示下，解碼只限於有效的動作 token。

## 結果

主要的泛化結果是作者機器人上的成功率（表 4，附錄 H.1）。平均值取自未見過的物件、背景與環境設定。

| 模型 | 已見任務 | 未見設定平均 |
|---|---|---|
| R3M | 45 | 12 |
| VC-1 | 63 | 10 |
| RT-1 | 92 | 32 |
| MOO | 75 | 35 |
| RT-2-PaLI-X-55B | 91 | 62 |
| RT-2-PaLM-E-12B | 93 | 62 |

論文文字稱，在未見設定上 RT-2 約為 RT-1 與 MOO 的 2 倍，約為其他基線的 6 倍（第 4.1 節）。在湧現技能方面，55B 的 PaLI-X 模型整體平均為 60%，RT-1 為 17%，作者稱其為次佳基線的 3 倍以上（表 5，第 4.2 節）。在模擬的 Language-Table 基準上，RT-2-PaLI-3B 得分為 90 ± 10，RT-1 為 74 ± 13（表 1）。

RT-2-PaLM-E 的思維鏈變體在動作 token 之前加入一個簡短的計畫步驟，論文只以定性範例呈現（第 4.4 節），未報告其成功率。

論文的消融實驗顯示，共同微調在最大規模時最為重要。55B 模型共同微調平均為 63，僅微調則為 52（表 6）。表 4 對同一模型給出 62，兩表相差一個百分點。

## 限制

- **沒有新動作**：機器人無法從網路資料中獲得新的實體動作，技能仍限於機器人資料的分布之內（第 5 節）。
- **運算與速度**：作者指出運算成本很高。55B 模型的執行頻率為 1–3 Hz，5B 模型約為 5 Hz（第 3.3 節）。對高頻控制而言，即時推論「可能成為主要瓶頸」（第 5 節；附錄 G）。
- **可用的基礎模型少**：能用來建構 RT-2 的通用視覺語言模型只有少數（第 5 節；附錄 G）。
- **失敗案例**：對把手等特定部位抓取不佳、擦拭等新動作、折毛巾等靈巧動作，以及多步驟的長推理（附錄 G）。
- **評估範圍**：實驗只在作者的機器人與任務類型上進行。

## 連結

- 視覺語言模型見[多模態模型](../../../theory/models/multimodal/index.md)。
- 語言模型的部分見[大型語言模型](../../../theory/models/llm/index.md)。
- 同一想法也出現在開放模型中：[OpenVLA](../openvla/index.md)。

## 參考文獻

### 開創性論文

- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — 以機器人軌跡與網路資料共同微調網路預訓練的視覺語言模型，並把動作寫成文字 token。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — RT-2 所比較的 transformer 機器人策略，以大量真實機器人資料訓練。
- Open X-Embodiment Collaboration (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — 涵蓋 22 種機器人本體的共享資料集，以及在其上訓練的 RT-X 模型（包括 RT-2-X）。
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — 較晚的通用機器人策略，建立在視覺語言模型上，論文稱之為視覺語言動作流模型。

### 教科書與綜述

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 關於基礎模型能力、技術原理與風險的報告，機器人是其中的應用領域之一。
