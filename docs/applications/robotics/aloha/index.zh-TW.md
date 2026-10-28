---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/models/transformer
aliases:
  - ALOHA
  - Action Chunking with Transformers
  - ACT
  - 低成本雙臂操作
---

# ALOHA 與 ACT（Zhao 等人，2023）

Zhao 等人想知道：便宜、精度不高的機器人硬體，能否從少量真實示範學會精細的雙手任務。他們建置了一套低成本的雙臂系統 ALOHA，並提出學習方法 Action Chunking with Transformers（ACT）。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

精細的雙臂操作，例如打開容器或插入電池，很難只靠模仿學會。誤差會在許多步驟中累積，人類示範也不一致。精密的機器人硬體昂貴，限制了能收集示範的人。

## 核心想法

ALOHA 把低成本手臂與遙控裝置配對，讓人能直接示範任務。ACT 一次預測一段未來的動作（一個 chunk），而不是每一步預測一個動作，因此減少了誤差累積的影響。這個策略以基於 transformer 的生成模型來建模這些動作序列。

## 程序

1. 用遙控系統收集示範，論文報告每個任務約 10 分鐘的資料。
2. 訓練 ACT，預測每個觀察之後的動作 chunk。
3. 執行時，執行預測出的 chunk，再依最新觀察預測下一段。

## 結果

論文報告六個真實世界的雙臂任務，包括打開透明的調味料容器與插入電池，成功率為 80–90%。這些數字來自論文摘要；詳細的比較需要查閱全文。

## 限制

- 結果來自作者自己的硬體與少數任務。
- chunk 會讓機器人一次承諾好幾步，因此依過時視角規劃的 chunk 可能出錯。這在實務上多重要，需要查閱全文。
- 每個新任務仍需要人來示範。

## 連結

- 模仿學習的設定見[模仿學習](../../../theory/paradigms/imitation/index.md)。
- 針對類似任務的擴散式策略，見[Diffusion Policy](../diffusion-policy/index.md)。
- Transformer 架構見[Transformer](../../../theory/models/transformer/index.md)。

## 參考文獻

### 開創性論文

- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — 提出 ALOHA 硬體與預測動作 chunk 的 ACT 策略。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — 以大量真實機器人資料訓練的 transformer 策略，研究泛化能力如何隨資料與模型規模改變。
- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — 以條件去噪擴散模型生成機器人動作，是針對同類任務、與 ACT 並列的替代方案。

### 教科書與綜述

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — 模仿學習方法的綜述，涵蓋 ACT 所用的設定。
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — 機器人強化學習的綜述，是示範之外的主要替代方法。
