---
translation_reviewed: 2026-10-28
---

# 零樣本思維鏈

零樣本思維鏈要求語言模型在沒有任何已寫好範例的情況下逐步推理。它在問題後加上一句簡短的引導語「Let's think step by step」，模型便會在作答前自行寫出推理過程。此方法是需要範例的[思維鏈](chain-of-thought.md)的變體，並與[推理模型](index.md)頁中的其他方法並列。

## 概述

思維鏈提示透過給予寫好步驟的範例，向模型展示如何推理。這需要有人為每項任務撰寫這些範例。Kojima 等人（2022）提問：能否只靠在問題後加上引導語，就讓模型在沒有任何範例的情況下推理？

## 關鍵概念

- **零樣本提示（zero-shot prompting）**：不含任何已寫好範例的提示，只有任務本身。
- **引導語（trigger phrase）**：改變模型回應方式的簡短指令，此處為「Let's think step by step」。
- **推理鏈（reasoning chain）**：模型在最終答案之前寫出的中間步驟。

## 問題

標準的思維鏈提示需要幾個範例，其推理步驟都是手寫的。範例的品質會影響結果，而且為每項新任務撰寫範例成本很高。問題在於：一句簡單的指令能否在沒有範例的情況下引出逐步推理？

## 核心想法

在問題後加上引導語。模型接著會在答案之前產生推理鏈，與有範例時的做法相同。此方法只改變提示本身。

## 運作方式

最簡單的形式有兩個步驟：以問題加上引導語提示模型，然後從它寫出的文字中讀取最終答案。提示中不含範例，權重也不會改變。

## 演算法

1. 取得問題。
2. 在問題後加上「Let's think step by step」。
3. 解碼模型的續寫，並從生成的推理末尾讀出最終答案。

## 核心方法

零樣本思維鏈是單一方法，即在不變的模型上加一句引導語。其主要比較對象是少樣本思維鏈（加入寫好步驟的範例），以及沒有引導語的一般零樣本提示。

## 結果

- 摘要報告，使用 InstructGPT（text-davinci-002）並加上引導語時，MultiArith 的準確率從 17.7% 提升到 78.7%，GSM8K 則從 10.4% 提升到 40.7%。
- 摘要把這些結果呈現為零樣本結果，提示中沒有任何範例。

## 限制

- 摘要中報告的增益，是針對一個模型系列（InstructGPT text-davinci-002）。摘要並未確立其他模型也會有同樣的增益。
- 在困難任務上的準確率仍然偏低，因此引導語無法縮小與 [自洽性](self-consistency.md)等更強方法之間的差距。
- 與思維鏈相同，寫出的推理是一種輸出，而不是模型內部運算的直接記錄。

## 變體與更多變體

- **少樣本思維鏈**：[思維鏈](chain-of-thought.md)頁所述、以範例為基礎的方法；在沒有範例時，引導語便可取代它。
- **自洽性**：取樣多條零樣本推理鏈並投票，見[自洽性](self-consistency.md)。

## 關聯

- [思維鏈](chain-of-thought.md)是本頁所簡化的、以範例為基礎的方法。
- [自洽性](self-consistency.md)可以疊加在零樣本推理鏈之上。
- [大型語言模型](../llm/index.md)描述了使用此引導語的提示情境。

## 應用

- 在撰寫範例不切實際的任務上，快速的推理提示。
- 在新基準上比較推理方法時，作為基線提示。

## 開放問題

- 哪些引導語效果最好，它們能否在不同模型之間通用？
- 增益有多少來自推理本身，又有多少來自引導語所鼓勵的輸出格式？

## 參考文獻

### 開創性論文

- Kojima, T., et al.（2022）。*Large Language Models are Zero-Shot Reasoners*. arXiv. https://arxiv.org/abs/2205.11916 — 提出引導語「Let's think step by step」，並報告本頁使用的 MultiArith 與 GSM8K 結果。
- Wei, J., et al.（2022）。*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 零樣本變體所比較的、以範例為基礎的方法。
- Brown, T. B., et al.（2020）。*Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 本方法所對照的零樣本與少樣本提示設定。

### 綜述與教科書

- Huang, J. & Chang, K. C.-C.（2023）。*Towards Reasoning in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2212.10403 — 綜述以提示為基礎的推理方法，包括零樣本變體。
