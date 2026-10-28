---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - Debate cross-examination
  - Cross-examination
  - 辯論交叉詰問
  - 交叉詰問
---

# 辯論交叉詰問

交叉詰問（cross-examination）是加在 [AI 辯論](debate.md)上的機制，目的是讓辯者在陳述被質疑後，無法改變該陳述的意思。在機器學習的版本中，對手可以質問辯者的一個已存檔副本，而該副本只知道到那一點為止說過的內容。這個想法來自 Barnes 與 Christiano（2020）的一篇非正式文章，它針對辯論的一個特定弱點：歧義。

## 問題

辯論假設，錯誤的主張會被對手的辯者揭露。不誠實的辯者可以利用這一點：先做出一個含糊的陳述，之後再挑選最適合當前論證段落的意思。只看最後幾輪交鋒的評審，可能不會注意到這種轉換。Barnes 與 Christiano 把這種歧義視為交叉詰問所要解決的問題。

## 關鍵概念

- **存檔副本**：對機器辯者而言，是它做出某個陳述時的快照。副本不知道之後辯論走了哪一條分支。
- **釐清問題**：對手向副本提出的、關於該陳述用語與細節的問題。
- **承諾**：辯者必須事先把細節講定，或給出之後可以彼此對照檢查的回答。

## 運作方式

1. 辯者 A 在辯論中做出陳述 $s$。
2. 若是機器辯者，系統會保存 A 當時狀態的副本。
3. 之後，辯者 B 可以就 $s$ 質問該副本。副本只根據到 $s$ 為止的紀錄作答。
4. 任一辯者都可以引用這些回答。若 A 之後的主張與副本所說相矛盾，矛盾會對 A 不利。
5. 評審再像一般辯論一樣作出判斷。

對於無法被複製的人類辯者，文章建議回溯到某個術語被引入的地方，或請一位只看過該陳述之前辯論內容的隊友加入。這個版本依賴善意的遊戲，因為辯者必須誠實回答先前說過的內容。

## 證據

正式的辯論研究測試的是相關特徵，但並未測試這種基於副本的機制。以下每一項都是有用的比較點：

- Khan et al.（2024）測試互動式辯論，評審在每一輪之後可以發表意見，例如提出釐清問題。在 LLM 評審的情況下，互動式辯論並未比靜態辯論提高準確率；在人類評審的情況下，兩者相當。
- Michael et al.（2023）允許評審提問，並對辯者設定舉證負擔。在人類評審的情況下，辯論達到 84% 的準確率，諮詢則為 74%。在 AI 辯者的情況下，辯論為 78%，諮詢為 80%，差異不顯著。
- Kenton et al.（2024）明確選擇不評估互動式辯論，也就是評審在每一輪提問的設定。
- Brown-Cohen et al.（2025）提出一個正式的協定：證明者（prover）分解一個主張，估計者（estimator）為各子主張指定機率。它的結構在精神上接近交叉詰問，但論文沒有使用這個詞。論文給出理論上的可靠性與完備性結果，沒有實驗。

綜合來看，這些結果顯示互動式提問可以幫助部分評審，但並未確立交叉詰問機制本身的效果。

## 限制

- **只針對歧義。** 文章表示，此機制無法解決混淆論證（obfuscated arguments）的問題，而作者對此沒有解法。
- **依賴善意。** 人類版本只有在辯者回溯時誠實作答，才會有效。
- **副本的忠實度。** 此機制假設存檔副本能反映辯者在做出陳述時的推理。正式文獻並未檢驗這個假設。
- **證據間接。** 目前沒有正式實驗測試基於副本的交叉詰問協定。

## 相關連結

交叉詰問的名稱借自法庭實務，在法庭上，一方的主張會經由對方的提問接受檢驗。這個類比有助於理解設計，但辯者的副本並不是證人，類比也不能保證機制會奏效。此方法屬於[可擴展監督](scalable-oversight.md)中的辯論一脈，與[AI 辯論](debate.md)及分解式方法並列。這些協定中的評審，也面臨[獎勵駭客](reward-hacking.md)所討論的被利用風險。

## 應用

以下是研究上的用途，而非已部署的系統。

- 為必須承諾其主張細節的機器辯者設計辯論協定。
- 訓練人類辯者與評審，檢查一個主張在提問下是否保持一致。
- 建立評估設定，測試模型的解釋在追問下是否站得住。

## 開放問題

- 存檔副本反映的是原辯者的推理，還是只有它的字句？
- 交叉詰問在實務上能否減少基於歧義的欺騙，它對混淆論證有幫助嗎？
- 基於副本的機制，如何與證明者－估計者結構等正式協定結合？

## 參考文獻

### 開創性論文

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human, the protocol that cross-examination modifies.
- Khan, A. et al. (2024). *Debating with More Persuasive LLMs Leads to More Truthful Answers*. Proceedings of ICML 2024 (PMLR 235). https://arxiv.org/abs/2402.06782 — Compares static and interactive debate with human and LLM judges on QuALITY.
- Michael, J. et al. (2023). *Debate Helps Supervise Unreliable Experts*. arXiv:2311.08702. https://arxiv.org/abs/2311.08702 — Tests debate with judges who can ask questions, against a consultancy baseline.

### 綜述與教科書

- Kenton, Z. et al. (2024). *On scalable oversight with weak LLMs judging strong LLMs*. arXiv:2407.04622. https://arxiv.org/abs/2407.04622 — Compares debate and consultancy with weak LLM judges, and states that interactive debate is not evaluated.
- Brown-Cohen, J. et al. (2025). *Avoiding Obfuscation with Prover-Estimator Debate*. arXiv:2506.13609. https://arxiv.org/abs/2506.13609 — Proposes a prover-estimator debate protocol, with theoretical soundness and completeness results.

## 延伸學習

- Barnes, E. & Christiano, P. (2020). [Debate update: Obfuscated arguments problem](https://www.alignmentforum.org/posts/PJLABqQ962hZEqhdB/debate-update-obfuscated-arguments-problem). AI Alignment Forum. 交叉詰問的原始描述，見於這篇非正式文章。
