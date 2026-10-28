---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - AI debate
  - Debate
  - AI 辯論
  - 辯論
---

# AI 辯論

AI 辯論是一種監督協定，用來監督系統在人類評審無法直接查核的問題上的表現。兩個模型的複本為相反的答案辯論，由評審判斷哪一方的論證較有說服力。其想法是：評審只需評估簡短、可查核的主張，因為對立的辯者會指出錯誤。Irving、Christiano 與 Amodei（2018）提出這個方法，後續的實驗則檢驗它是否能幫助非專家的評審。

## 問題

當評審能分辨正確答案與錯誤答案時，以人類判斷監督模型是可行的。對於需要專家知識的問題，或輸出太長而難以查核的情況，評審無法單獨完成這件事。監督於是取決於能否找到一種程序，讓較弱的評審仍能得到正確答案，這正是[可擴展監督](scalable-oversight.md)所處理的問題。

## 核心想法

把問題視為零和遊戲。每一位辯者只有在評審接受其答案時才得分。如果一方提出錯誤的主張，另一方可以加以挑戰，而難以辯護的錯誤主張應該輸掉。Irving et al. 主張，在這種設定下，辯論可以向一位無法直接查核原問題的評審揭示真相。

## 協定

1. 提出問題 $q$。辯者 A 為答案 $a$ 辯護，辯者 B 為相反的答案辯護。
2. 辯者輪流發言，並可引用證據。回合數是固定的。
3. 評審（人類，或能力有限的模型）閱讀逐字稿，選出它接受其答案的辯者。
4. 兩位辯者以自我對弈訓練，因此各自都學習擊敗對方，勝者的陳述會被強化。

此提案假設誠實的一方總能以評審能理解的方式揭穿謊言。論文在此假設下給出理論論證，並在小型任務上示範這個設定。

## 結果

Irving et al.（2018）包含影像分類上的小型實驗。論文是包含理論與早期示範的提案，並非大規模的實證研究。

兩項較晚的研究以語言模型與人類評審檢驗這個想法：

- Khan et al.（2024）測試以非專家人類評審進行的辯論。摘要報告，當專家辯者被最佳化為更有說服力（而不使用真實標籤）時，非專家評審更常辨識出正確答案。換句話說，辯者的說服力幫助評審接近真相。
- Michael et al.（2023）測試兩位不可靠的專家辯者之間的辯論，並與由單一專家進行的諮詢基準比較。摘要報告，辯論幫助非專家人類評審更準確地回答困難的閱讀理解問題，評審準確率為 84%，諮詢基準為 74%。

這些結果來自特定的任務與評審群體，不應被解讀為辯論適用於所有問題的證據。

## 限制

- **說服力與真相。** 更具說服力的辯者可以在不正確的情況下獲勝。Khan et al. 的結果顯示，這在某些情境中可以被善用，但它也是最核心的風險。
- **隱藏的缺陷。** 太長或太技術性而無法查核的主張，即使是錯的，也可能在辯論中存活。
- **共謀。** 一起訓練的辯者可能同意一個誤導性的答案，然後分享獎勵。
- **評審的限制。** 評審可能被修辭所騙，其錯誤可能具有系統性。
- **假設的結構。** 理論依賴誠實的一方能夠獲勝，這對每一種問題類型未必成立。

## 相關連結

辯論借鑒了法律與科學實踐中的對抗式做法，這些實踐用對立的倡議者與交叉詰問來檢驗主張。這個類比有助於理解協定的結構，但人類的辯論並不是帶有習得策略的零和遊戲。此方法是[可擴展監督](scalable-oversight.md)中以分解為基礎的方法之一，並與 Christiano、Shlegeris 與 Amodei（2018）的放大方法相關。辯論實驗中的評審也面臨[獎勵駭客](reward-hacking.md)所討論的評估問題，因為辯者可能學會利用評審，而不是找出真相。

## 應用

- 在專家稀少的問答任務上，以實驗方式監督模型。
- 以人類受試者研究，檢驗模型的協助是否改善非專家的判斷。
- 設計能抵抗模型說服的評審與評估協定。

## 開放問題

- 當評審遠比辯者弱時，辯論能否找到真相？在什麼條件下會失敗？
- 應如何訓練評審，使其抵抗具說服力但錯誤的論證？
- 辯論能否推廣到無法單獨查核任一主張的任務？

## 參考文獻

### 開創性論文

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human as a way to supervise systems on questions beyond direct human judgement.
- Khan, A. et al. (2024). *Debating with More Persuasive LLMs Leads to More Truthful Answers*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2402.06782 — Shows that optimising debaters for persuasiveness, without ground truth, increases non-expert judge accuracy.
- Michael, J. et al. (2023). *Debate Helps Supervise Unreliable Experts*. arXiv:2311.08702. https://arxiv.org/abs/2311.08702 — Reports that debate between unreliable experts improves non-expert judges on hard reading-comprehension questions.

### 綜述與教科書

- Bowman, S. R. et al. (2022). *Measuring Progress on Scalable Oversight for Large Language Models*. arXiv:2211.03540. https://arxiv.org/abs/2211.03540 — Builds a benchmark for whether model assistance helps non-expert judges, including debate-style setups.
- Christiano, P., Shlegeris, B. & Amodei, D. (2018). *Supervising strong learners by amplifying weak experts*. arXiv:1810.08575. https://arxiv.org/abs/1810.08575 — Introduces iterated amplification, an alternative decomposition-based approach to supervising stronger models.
