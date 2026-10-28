---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# GAIA

GAIA（General AI Assistants）是一組真實世界的問題，需要推理、多模態理解、網路瀏覽與工具使用。這些問題對人來說很簡單，但對多數 AI 系統卻很困難。作者報告人類受試者得分 92%，而裝上外掛的 GPT-4 只有 15%（Mialon et al., 2023）。

## 任務與資料

每題都需要同時運用數種能力，例如在網路上找到事實、讀取附加的檔案或影像，再把結果整合成一個答案。這個基準的設計避開了模型已經勝過人類的任務，例如專業考試，改為測試助理能否處理需要多個步驟的一般請求（Mialon et al., 2023）。

## 協定與指標

答案簡短且可檢查，因此指標是正規化後的**完全相符準確率**。測試答案不公開，結果須提交而非在本地計算。分數取決於系統被允許使用的工具，因此必須連同分數一起報告工具組。

## 它能說明什麼

發表時，人類與最佳系統之間的差距是主要發現。這顯示系統在專業考試上的能力，並不會自動轉移到需要例行工具使用與網頁導覽的任務（Mialon et al., 2023）。

## 限制

- **即時網路。** 網頁會隨時間改變，因此同一題在之後可能得到不同答案。結果需要附上執行日期。
- **公開的部分小。** 公開的題目不多，多數報告的結果來自團隊無法檢視的保留測試集。
- **工具存取。** 有搜尋引擎與瀏覽器的系統，與沒有它們的系統不能比較，即使模型相同。

## 相關

- [WebArena](webarena.md) 在受控的網頁環境中測試代理，而非開放的網路。
- [ARC-AGI](arc-agi.md) 測試從範例中獲得規則的能力。
- [推理與代理家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — 介紹真實世界的問題，以及人類與系統的比較。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張基準應衡量技能獲取，而非任務表現。

### 文章與文件

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 上下文提示，是評估工具使用問題時的常見設定。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 多步驟問題常依賴的中間推理步驟。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 討論基準設計應如何區分學到的知識與能力。
