---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - AI feedback
aliases:
  - RLAIF
  - Reinforcement learning from AI feedback
  - 基於 AI 回饋的強化學習
  - 以 AI 回饋強化學習
---

# 基於 AI 回饋的強化學習（RLAIF）

基於 AI 回饋的強化學習（RLAIF）以語言模型產生的標註，取代 RLHF 所使用的人類偏好標註。學習程序維持不變：先以偏好配對訓練獎勵模型，再以強化學習對它最佳化策略。Lee et al.（2024）直接研究這個替換，並報告在他們測試的任務上，AI 標註訓練出的策略表現與人類標註相近。

## 問題

RLHF 需要大量的人類比較模型回應。每一次比較都耗費時間與金錢，而且評分者之間彼此不一致。問題在於：一個能力足夠的語言模型，能否給出足夠好的偏好標註來訓練獎勵模型，使人力投入得以減少，或轉移到較少的查核上。

## 核心想法

以現成的語言模型作為標註者。對每個提示與一對回應，詢問標註者哪一個較好，並以它對每個答案的機率作為軟標籤。以這些標籤訓練獎勵模型，然後像 RLHF 一樣進行強化學習。這個方法改變的是標籤的來源，而不是強化學習的步驟，因此可以與 RLHF 直接比較。

## 方程式或演算法

1. 從目前的策略取樣一個提示 $x$ 與兩個回應 $y_1, y_2$。
2. 詢問標註模型哪個回應較好，並讀出它偏好 $y_1$ 的機率 $p$。
3. 以軟標籤、依標準的 Bradley–Terry 損失訓練獎勵模型 $r_\phi$，

$$
\mathcal{L}(\phi) = -\mathbb{E}\left[p \log \sigma\big(r_\phi(x, y_1) - r_\phi(x, y_2)\big) + (1 - p)\log \sigma\big(r_\phi(x, y_2) - r_\phi(x, y_1)\big)\right]
$$

4. 以強化學習對 $r_\phi$ 最佳化策略，通常會加上一個懲罰，使策略保持接近起始模型。

Lee et al.（2024）還描述了一個直接的變體 d-RLAIF，它跳過第 3 步。標註模型在強化學習期間為回應評分，因此不需要另外訓練獎勵模型。

## 結果

Lee et al.（2024）比較 RLAIF 與 RLHF 在摘要以及有用與無害對話任務上的表現。摘要中報告，RLAIF 在這些任務上表現與 RLHF 大致相當。它也報告，即使標註者的大小與策略相同，或就是策略自己的起始檢查點，RLAIF 仍能勝過監督式微調的基準。摘要指出 d-RLAIF 勝過標準的 RLAIF。這些結果來自作者自己的評估協定，數字見論文本身，此處不重複。

## 限制

- **標註者偏誤。** 標註者的偏好成為訓練目標。如果它偏好某些風格或位置，獎勵模型也會學到這些偏好。
- **自我偏好。** 標註自己輸出或接近自己輸出的模型，可能因為與品質無關的理由偏好它們。
- **標註者的上限。** 策略被訓練朝向標註者能判斷的方向。在標註者無法良好評估的任務上，訊號很弱，這正是[可擴展監督](scalable-oversight.md)的核心困難。
- **證據範圍有限。** 報告的比較涵蓋少數任務。這些實驗並未確立在程式設計、長時程代理或開放式研究上的結果。
- **獎勵駭客。** 獎勵模型仍是代理，過度最佳化它可能降低真實品質，如[獎勵駭客](reward-hacking.md)所述。

## 相關連結

RLAIF 是[憲法式 AI](constitutional-ai.md)中標籤來源的部分，後者另外加入了書面原則與批判及修訂。與[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)中的框架相比，RLAIF 保持相同的目標，只改變誰給出比較。以書面規則而非直接經驗來判斷，在人類身上也有對應，例如人們如何套用成文標準，但這個類比是鬆散的。

## 應用

- 在建立聊天與摘要模型時，降低偏好資料的成本。
- 在人類專家稀少的任務上產生偏好資料，並由人類抽查。
- 比較不同的標註模型，選出在保留資料集上與人類評分者判斷一致的一個。

## 開放問題

- 當任務需要專家知識時，AI 標籤與人類偏好的吻合程度如何？
- 在標註者更強、訓練更長的情況下，d-RLAIF 相對標準 RLAIF 的優勢是否仍然存在？
- 在系統性偏誤寫入策略之前，需要什麼樣的檢查才足以偵測到它？

## 參考文獻

### 開創性論文

- Lee, H. et al. (2024). *RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2309.00267 — Compares AI-labelled and human-labelled preferences for training policies on summarisation and dialogue.
- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 — Introduces training from AI preference labels guided by written principles.
- Christiano, P. et al. (2017). *Deep Reinforcement Learning from Human Preferences*. arXiv:1706.03741. https://arxiv.org/abs/1706.03741 — Learns a reward model from human comparisons, the human-label baseline that RLAIF replaces.

### 綜述與教科書

- Casper, S., Davies, X. & Shi, C. (2023). *Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback*. arXiv:2307.15217. https://arxiv.org/abs/2307.15217 — Surveys open problems in preference-based training, many of which apply to AI-generated labels.
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. arXiv:2203.02155. https://arxiv.org/abs/2203.02155 — Applies reward-model RLHF to make a language model follow user instructions.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv:2305.18290. https://arxiv.org/abs/2305.18290 — Fits a policy directly to preference pairs, with no explicit reward model.
