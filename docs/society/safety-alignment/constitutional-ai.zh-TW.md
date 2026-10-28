---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
  - theory/models/llm/instructgpt-rlhf
tags:
  - alignment
  - AI feedback
aliases:
  - Constitutional AI
  - CAI
  - RLAIF
  - 憲法式 AI
  - 以 AI 回饋強化學習
---

# 憲法式 AI 與 RLAIF

憲法式 AI（Constitutional AI, CAI）讓語言模型依照一份簡短的書面原則，也就是「憲法」，來批判並修訂自己的輸出，藉此學會無害。在基於人類回饋的強化學習（RLHF）中，大部分的人類偏好標註會被 AI 模型產生的標註取代。Bai et al.（2022）在 Anthropic 提出這個方法。以 AI 標註取代人類偏好標註的一般想法，通常稱為基於 AI 回饋的強化學習（RLAIF），由 Lee et al.（2024）獨立研究。

## 概覽

RLHF 會先根據人類對兩個回應的比較訓練獎勵模型，再針對它最佳化策略（參見[從人類回饋中學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)）。這種設定會帶來三個問題：

- 人類標註者必須閱讀並判斷大量有害文字，既緩慢又昂貴。
- 不同標註者的標註彼此不一致，背後的價值也是隱含的。
- 最後的行為難以檢視，因為價值分散在數千筆標註之中。

憲法式 AI 把價值寫成明文，以解決第二與第三個問題。這些原則是簡短的陳述，例如偏好最不可能協助危險行為的回應。模型再把它們套用到自己的輸出上。

## 核心概念

- **憲法（constitution）**：訓練程序會從中取樣的自然語言原則清單。
- **批判與修訂（critique and revision）**：模型依據某條取樣到的原則，對自己的一則回應寫出批判，再重寫該回應以回應批判。
- **AI 偏好標註（AI preference label）**：由語言模型判斷兩則回應哪一則更符合某條原則。
- **偏好模型（preference model）**：以 AI 偏好標註訓練出的獎勵模型。

## 運作方式

此方法分為兩個階段。

1. **監督階段（SL-CAI）。** 初始模型回答設計來誘發有害輸出的提示。對每則回答，模型依據取樣到的原則產生批判與修訂。這些修訂成為微調的訓練資料，使模型直接學會產生修訂後風格的回答。
2. **強化學習階段（RL-CAI）。** 經過微調的模型對每個提示產生成對的回答。模型被要求判斷哪一則較符合某條原則，這些 AI 標註用來訓練偏好模型。接著與 RLHF 相同，以強化學習對偏好模型最佳化策略。

```mermaid
flowchart LR
    A[有害提示] --> B[初始回應]
    B --> C[依據原則批判]
    C --> D[修訂後的回應]
    D --> E[監督式微調]
    E --> F[成對回應]
    F --> G[AI 判斷何者符合原則]
    G --> H[偏好模型]
    H --> I[對偏好模型做強化學習]
```

Bai et al.（2022）仍保留少量人類的有用性標註，使模型在無害之外也能保持實用。

## 主要方法

以下方法共享偏好學習的概念。這裡簡要比較，細節請見連結的頁面。

- [RLHF](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)（Christiano et al., 2017；Ouyang et al., 2022）：人類比較訓練獎勵模型，再引導強化學習。
- **RLAIF**（Lee et al., 2024）：在相同的流程中以 AI 標註取代人類標註。改變的是標註來源，學習程序不變。
- **憲法式 AI**（Bai et al., 2022）：RLAIF 加上由書面憲法引導的批判與修訂。
- [DPO](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index.md)（Rafailov et al., 2023）：移除明確的獎勵模型，直接以偏好配對擬合策略。由 AI 產生的配對同樣可以用於 DPO。

## 結果

Bai et al.（2022）報告，依照憲法程序訓練的模型，在作者自己的評估中被判定比 RLHF 基準更無害，同時在有用性上有作者所討論的取捨。Lee et al.（2024）比較 AI 標註與人類標註的偏好，用於摘要與對話任務，並報告 AI 標註訓練出的策略，被偏好的比例與人類標註訓練者相近。兩項結果都來自開發者自己的評估流程，因此最適當的解讀是：此方法在所測試的任務上有效，而非普遍保證。

## 限制與批評

- **誰的價值？** 憲法由開發者撰寫。批評者認為，一份簡短的原則清單編碼了特定的文化與政治選擇，而選擇原則的過程並不透明。
- **標註者偏誤。** AI 標註者會承襲訓練資料的偏誤，也可能偏好與自己風格相近的回應。這類自我偏好會讓回饋看起來比實際更一致。
- **較弱的評審。** 批判的品質取決於撰寫批判的模型。對於模型能力低於被訓練策略的任務，AI 回饋可能漏掉錯誤，這使此方法與[可擴展的監督](scalable-oversight.md)相連。
- **迴避式拒絕。** 針對危害的訓練可能使模型傾向於無益的拒絕。有用性的取捨是這個文獻中反覆出現的發現。
- **規格缺口。** 原則是一般性的，模型必須加以詮釋，而詮釋可能與開發者的本意不同。這是[獎勵駭客與規格博弈](reward-hacking.md)所討論問題的一個版本。

## 相關連結

憲法式 AI 是一套工程程序，不是道德認知的模型，因此它與人類倫理的類比是鬆散的。它的批判步驟類似自我監控，而憲法所扮演的角色類似一個人內化的規範，但兩種比擬都未經檢驗。道德推理的哲學，包括規則與判斷之間的爭論，在[AI 哲學](../philosophy/index.md)與[倫理](../ethics/index.md)中討論。此方法也位於更廣泛的[安全與對齊](index.md)工具箱之中，與[模型規範](model-specs.md)並列。

## 開放問題

- 當模型能力超越評判它們的標註者時，AI 回饋是否仍然可靠？
- 憲法應該包含哪些原則？由誰來決定？
- AI 撰寫的批判有多常能抓出真正的錯誤，而非回應表面的特徵？
- 以原則為基礎的訓練所獲得的進步，能否轉移到憲法未列出的新型危害？

## 參考文獻

### 開創性論文

- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 — Introduces critique-and-revision followed by reinforcement learning from AI preference labels, guided by a written constitution.
- Lee, H. et al. (2024). *RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2309.00267 — Compares AI-labelled and human-labelled preferences as training signals for summarisation and dialogue.
- Christiano, P. et al. (2017). *Deep Reinforcement Learning from Human Preferences*. arXiv:1706.03741. https://arxiv.org/abs/1706.03741 — Learns a reward model from human pairwise comparisons, the template that RLAIF and CAI modify.
- Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback*. arXiv:2203.02155. https://arxiv.org/abs/2203.02155 — Applies reward-model RLHF to make a language model follow user instructions.
- Rafailov, R. et al. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. arXiv:2305.18290. https://arxiv.org/abs/2305.18290 — Fits a policy directly to preference pairs, with no explicit reward model.

### 綜述與教科書

- Casper, S., Davies, X. & Shi, C. (2023). *Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback*. arXiv:2307.15217. https://arxiv.org/abs/2307.15217 — Surveys the open technical and sociotechnical problems in RLHF, many of which carry over to AI-feedback methods.
