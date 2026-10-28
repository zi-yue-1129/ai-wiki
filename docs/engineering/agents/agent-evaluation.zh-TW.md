---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - agents
  - evaluation
  - benchmarks
aliases:
  - Agent Evaluation
  - Agent Benchmarks
  - 代理評估
  - 代理基準測試
---

# 代理評估

評估代理，是判斷它在環境中一連串步驟上的表現，而不只是最後的文字。正確的答案可能來自糟糕的過程，健全的過程也可能因為小細節而失敗。因此代理評估會檢查軌跡與最終狀態，並在成功率之外，也計算成本與可靠度。

本頁是[代理工程](index.zh-TW.md)的一部分。

## 概述

問答基準評分的是單次回應。代理則會跨越多輪、呼叫工具並改變狀態，因此基準需要一個環境、一種在其中執行代理的方式，以及對結果的檢查。檢查可以是檢視最終狀態的程式、評分模型，或人類。每種選擇都在成本與準確性之間，以及結果能否重現之間取捨。

## 關鍵概念

- **任務成功率：**最終狀態符合目標的任務比例。
- **軌跡：**一次執行中完整的觀察、工具呼叫與輸出序列。
- **環境狀態：**任務所改變的資料，例如資料庫或網頁，成功與否就是對照它來檢查。
- **模擬使用者：**在對話中扮演使用者的語言模型，使代理能在對話中接受測試。
- **pass^k：**代理在同一任務的 k 次獨立嘗試中全部成功的機率。它衡量可靠度，這是單次執行無法顯示的。
- **每項任務成本：**完成一項任務所需的模型與工具成本。

## 運作方式

典型的評估遵循相同步驟。駕馭層設定任務與初始狀態。代理以固定的工具組執行。執行過程被記錄為軌跡。檢查器把最終狀態與目標比較。結果會依任務與重複執行彙總，因為單次執行會掩蓋變異。被比較的系統必須使用相同的駕馭層與工具。

## 基準

- **AgentBench**（Liu 等人，2023）在八個不同環境中評估語言模型作為代理的表現，並報告商用模型與開放模型之間有顯著差距。
- **WebArena**（Zhou 等人，2023）使用四個領域的寫實、可重現網站：電子商務、社群論壇、協作式軟體開發與內容管理。
- **OSWorld**（Xie 等人，2024）使用真實的電腦環境，因此任務不侷限於單一應用程式。
- **τ-bench**（Yao 等人，2024）以模擬使用者模擬對話，代理須使用領域工具並遵循政策指引。它把對話結束時的資料庫狀態與標註的目標狀態比較，並提出 pass^k 作為可靠度指標。
- **GAIA**（Mialon 等人，2023）測試需要工具與多步推理的一般助理任務。其專屬頁面見 [GAIA](../../theory/evaluation/benchmarks/reasoning-agents/gaia.zh-TW.md)。

## 對現行做法的批評

Kapoor 等人（2024）認為，代理基準過度偏重準確率，因而忽略成本。他們指出，部分準確率的提升來自昂貴的設計，並建議同時報告成本與準確率。他們的分析提醒我們，不應只憑成功率比較代理。

## 限制

- **評分錯誤。**過嚴或過寬的檢查器會改變分數。
- **資料污染。**公開任務可能出現在訓練資料中。
- **變異。**少數任務與單次執行，可能得出誤導性的排名。
- **環境簡化。**基準是真實任務的模型，兩者之間的差距會影響結果。

## 關聯

- 推理與代理基準，包括 [ARC-AGI](../../theory/evaluation/benchmarks/reasoning-agents/arc-agi.zh-TW.md) 與 [WebArena](../../theory/evaluation/benchmarks/reasoning-agents/webarena.zh-TW.md)，見[推理與代理基準](../../theory/evaluation/benchmarks/reasoning-agents/index.zh-TW.md)。
- 一般評估實務，包括以 LLM 為評審與資料污染，見[評估與基準](../evaluation/index.zh-TW.md)。
- 在正式運作中記錄的軌跡可以餵入評估，見[代理可觀測性](agent-observability.zh-TW.md)。

## 應用

- 每次發布前對代理進行**回歸測試**。
- 在固定工作流程中**比較模型或工具**，並把成本與成功率並列報告。
- **安全測試**：環境中包含應該被拒絕的任務。

## 開放問題

- 評估如何便宜到能經常執行，又仍能反映真實使用？
- 開放式輸出的評分者應如何驗證？
- 除了 pass^k，部署中的代理還需要哪些可靠度指標？

## 參考文獻

### 開創性論文

- Liu, X. 等人（2023）。*AgentBench: Evaluating LLMs as Agents*。arXiv。https://arxiv.org/abs/2308.03688 — 以八個互動環境評估 LLM 代理的多面向基準。
- Zhou, S. 等人（2023）。*WebArena: A Realistic Web Environment for Building Autonomous Agents*。arXiv。https://arxiv.org/abs/2307.13854 — 四個領域的可重現網站，用於評估網頁代理。
- Xie, T. 等人（2024）。*OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*。arXiv。https://arxiv.org/abs/2404.07972 — 用於評估多模態代理開放式任務的真實電腦環境。
- Yao, S. 等人（2024）。*τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*。arXiv。https://arxiv.org/abs/2406.12045 — 以模擬使用者的對話、領域工具與政策，並以資料庫狀態檢查，附 pass^k 可靠度指標。
- Mialon, G. 等人（2023）。*GAIA: a benchmark for General AI Assistants*。arXiv。https://arxiv.org/abs/2311.12983 — 需要推理、工具與瀏覽的一般助理任務基準。

### 調查與教科書

- Kapoor, S. 等人（2024）。*AI Agents That Matter*。arXiv。https://arxiv.org/abs/2407.01502 — 批評代理基準只重準確率，並主張同時評估成本與準確率。
