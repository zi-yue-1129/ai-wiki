---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
aliases:
  - Diffusion Policy
  - 擴散策略
---

# Diffusion Policy（Chi 等人，2023）

Chi 等人提出以去噪擴散模型生成機器人行為。策略不是從觀察直接預測一個動作，而是從雜訊出發，在觀察的引導下逐步生成一段動作序列。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

在同一情境中有多種正確動作時，模仿式策略常常表現不佳。一般的迴歸模型會把這些選擇平均起來，而平均結果可能是很差的動作。機器人的動作空間又是高維的，使問題更嚴重。

## 核心想法

論文把視覺運動策略建模為條件式去噪擴散過程。模型從隨機雜訊開始，反覆去除雜訊，每一步都以當前觀察為條件。結果是一段貼近某個示範模式、而不是平均值的動作序列。作者主張，擴散模型能很好地處理多模態動作與高維空間，而且訓練穩定。

## 程序

1. 收集任務的示範，把每個觀察與當時採取的動作配對。
2. 訓練一個網路，在觀察的條件下預測加入示範動作序列中的雜訊。基礎方法是[去噪擴散模型](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md)。
3. 執行時，從雜訊出發，經過去噪步驟取樣出一段動作序列，再執行其中一部分。論文描述的是接收視界控制（receding-horizon control）：策略先執行預測序列的一部分，再重新預測。

## 結果

論文報告，相較於先前最先進的方法，平均提升 46.9%。摘要描述了四個操作基準上的 15 項任務；主要比較表列出其中 12 項（8 項模擬與 4 項真實世界）。也報告了真實機器人的實驗。各任務的細節需要查閱全文。

## 限制

- 生成一段動作序列需要多次去噪步驟，相較於單次前向計算，推論時間較長。
- 報告的進步是在作者自己的基準與機器人設定上測得的。
- 論文的比較對象是當時的方法，之後已有變化。

## 連結

- 模仿學習的設定見[模仿學習](../../../theory/paradigms/imitation/index.md)。
- 本方法所依據的方法是[擴散模型](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md)。
- 針對類似任務、以 transformer 為基礎的策略見[ALOHA 與 ACT](../aloha/index.md)。

## 參考文獻

### 開創性論文

- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — 把視覺運動策略建模為條件去噪擴散，並報告四個基準上 15 項任務的結果。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — 本策略的訓練與取樣流程所依據的擴散模型。
- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — ACT 策略，是針對同類任務的競爭方法。

### 教科書與綜述

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — 模仿學習方法的綜述。
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — 機器人強化學習的綜述。
