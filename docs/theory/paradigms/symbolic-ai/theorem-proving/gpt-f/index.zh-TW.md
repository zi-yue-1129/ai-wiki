---
translation_reviewed: 2026-10-28
---

# GPT-f（Polu 與 Sutskever 2020）

GPT-f 是一個 Transformer 語言模型，為自動證明器提出證明步驟，最初用於 Metamath 形式語言。它是學習式策略預測的早期代表：模型寫出下一步，形式檢查器則接受或拒絕它。它也是上層頁面[自動定理證明與形式化數學](../index.zh-TW.md)所列三個代表性方法之一。

## 概述

當時的自動證明器大多依賴人工設計的搜尋規則。Polu 與 Sutskever 試問：語言模型的生成能否改善自動證明器的一個弱點，也就是難以產生新的數學項。他們建立了 GPT-f，作為 Metamath 的證明器與證明助理。[^1] 它的證明被收入 Metamath 主函式庫，作者報告這是深度學習系統貢獻的證明首次被形式數學社群所採納。

## 核心概念

- **證明狀態**：仍待證明的目標，連同可用於此目標的假設。
- **證明步驟（策略）**：轉換某個目標的下一個指令，例如一個 Metamath 步驟，或一個 Lean 或 Coq 的策略。
- **策略預測**：從當前狀態生成合理下一步的學習任務。
- **最佳優先搜尋**：先展開分數最高的部分證明，使有希望的分支先於較弱的分支被探索。
- **驗證器**：接受或拒絕每個生成步驟的形式系統。模型可以提出任何東西，但只有通過驗證的步驟會留下來。

## 運作方式

模型以形式證明訓練，這些證明被寫成狀態與步驟的序列，使模型學會預測下一步。證明時，證明器執行最佳優先搜尋：

1. 把目標放入前沿，分數為零。
2. 取出分數最高的節點。
3. 請模型針對該節點的證明狀態，提出數個候選的下一步。
4. 把每個候選送交驗證器，丟棄被拒絕的候選。
5. 把每個通過的步驟加入為子節點。其分數為父節點的分數，加上模型給該步驟的對數機率。
6. 所有目標都已關閉時停止，或搜尋預算用完時停止。

對於一個 $k$ 步的證明 $a_1, \dots, a_k$，它依序經過狀態 $x_0, \dots, x_{k-1}$，其分數為

$$
s = \sum_{i=1}^{k} \log p_\theta(a_i \mid x_{i-1}),
$$

其中 $\theta$ 表示模型參數。把對數機率加總，會偏好模型在每一步都認為合理的證明。確切的搜尋設定在各次實驗中有所不同，並見於論文。

## 結果

- **Metamath。** GPT-f 被接受的證明是主要結果，由 Polu 與 Sutskever 在 Metamath 函式庫上報告。[^1]
- **miniF2F。** Zheng 等人提出 miniF2F 基準，並以 GPT-f 作為其基線，其表現分析見於論文。[^2] 數字在該論文中，本頁不重述。
- **後續比較。** Lample 等人報告，GPT-f 在一組留出的 Metamath 定理上解決了 56.5%，而他們的搜尋方法在同一組上達到 65.4%，加上對未證明定理進行線上訓練後提升到 82.6%。[^3]
- **Lean。** Han 等人報告，將策略預測與證明產物資料共同訓練後，留出的 Lean 測試定理上的成功率從 32% 提升到 48%。[^4]

這些數字來自不同的基準、語言與訓練設定，因此彼此不能直接比較。

## 限制

- **依賴資料。** 模型從一個函式庫中由人撰寫的證明學習。這類函式庫相較於一般文字很小，屬於容易過擬合的資料稀缺情境。[^4]
- **失敗的步驟。** 許多被提出的步驟會被拒絕，而搜尋成本會隨候選數量增加。
- **保證有限。** 一個經過驗證的證明只說明形式陳述成立，不說明它是否捕捉到了原本想解的問題。

## 開放問題

- **遷移。** 在一個函式庫上訓練的模型，能否遷移到其他函式庫，以及研究級的數學？
- **前提選擇。** 策略預測與前提選擇處理搜尋的不同部分。[^5] 如何最好地結合兩者，仍是開放的。
- **人類風格。** 生成的證明是否像人類的證明，還是利用了數學家會避開的函式庫規律？

## 關聯

GPT-f 的模式是模型提出、檢查器裁決，這與[推理模型](../../../../models/reasoning/index.zh-TW.md)中的測試時搜尋相似。其後繼方法加入了受 AlphaZero 啟發的搜尋。[^3] [AlphaProof](../../../../../applications/mathematics/alphaproof/index.zh-TW.md) 則在奧林匹亞規模上應用了強化學習。

## 應用

- **證明輔助。** 提出策略的模型可以向正在 Lean 或 Coq 中撰寫證明的人建議步驟，而證明助理會檢查每一步。GPT-f 被接受的 Metamath 證明顯示，此類結果能進入社群函式庫。[^1]
- **基準測試。** 像 miniF2F 這樣的形式化基準，讓系統能被自動比較。[^2]

[^1]: Polu 與 Sutskever（2020），見上方參考文獻。
[^2]: Zheng 等人（2021），見上方參考文獻。
[^3]: Lample 等人（2022），見上方參考文獻。Metamath 的數字以其摘要所報告者為準。
[^4]: Han 等人（2021），見上方參考文獻。資料稀缺的說法出自其摘要。
[^5]: Alemi 等人（2016），見上層頁面所引用者。

## 參考文獻

### 開創性論文

- Polu, S. & Sutskever, I. (2020). *Generative Language Modeling for Automated Theorem Proving*. arXiv. https://arxiv.org/abs/2009.03393 — 提出 GPT-f，一個用於 Metamath 的 Transformer 證明器，其證明被收入主函式庫。
- Zheng, K., Han, J. M. & Polu, S. (2021). *MiniF2F: a cross-system benchmark for formal Olympiad-level mathematics*. arXiv. https://arxiv.org/abs/2109.00110 — 提出 miniF2F 基準，並以 GPT-f 作為基線。
- Han, J. M. et al. (2021). *Proof Artifact Co-training for Theorem Proving with Language Models*. arXiv. https://arxiv.org/abs/2102.06203 — 以證明項取得的自監督資料，改善 Lean 中的策略預測。
- Lample, G. et al. (2022). *HyperTree Proof Search for Neural Theorem Proving*. arXiv. https://arxiv.org/abs/2205.11491 — 在 Metamath 上將一種搜尋方法與 GPT-f 比較，並加入線上訓練。

### 綜述與教科書

- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — 形式定理證明的綜述，涵蓋學習式策略預測及其開放挑戰。
