# 數學與形式證明

AI 在數學中有兩種不同的用法。語言模型以自然語言解題與寫證明，答案可能錯誤且難以檢查。形式系統則以電腦可驗證的語言表達證明，因此模型的嘗試不是通過檢查，就是失敗。最新的進展結合了兩者。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 形式定理證明 | Lean 等證明助手；對證明步驟進行搜尋與強化學習 | 通過檢查的證明是可靠的獎勵訊號 |
| 奧林匹亞幾何 | 提出輔助構造的語言模型，搭配符號演繹引擎 | AlphaGeometry（Trinh et al., 2024） |
| 奧林匹亞解題 | 以形式化題目做強化學習，以證明檢查器作為獎勵 | AlphaProof（Hubert et al., 2025） |
| 用於發現的程式搜尋 | 語言模型提出程式，評估器在迴圈中保留好的程式 | FunSearch（Romera-Paredes et al., 2024） |
| 語言模型的競賽數學 | 思維鏈推理、取樣與投票 | 以 MATH 與 GSM8K 基準衡量 |
| 猜想引導 | 學習模型提出規律，再由數學家證明 | Davies et al.（2021） |
| 符號計算 | 用於積分與微分方程的序列到序列模型 | Lample & Charton（2019） |

## 為什麼困難

- **驗證**：自然語言證明看起來可能很有說服力，實際上卻可能錯誤。形式證明可由機器檢查，但撰寫時需要形式語言與定義函式庫。
- **資料稀少**：形式證明語料遠少於網路文本，因此模型只能從合成題目與自己成功的證明中學習。
- **稀疏獎勵**：大多數證明嘗試都會失敗，學習訊號因此很少。
- **錯誤形式化**：形式證明可能正確地證明了與原意不同的命題。

## 關鍵方法

- [思維鏈推理](../../theory/models/reasoning/chain-of-thought.md)：逐步的自然語言推理，是語言模型處理競賽數學的常用途徑。
- [測試時擴展](../../theory/models/reasoning/test-time-scaling.md)：推論時投入更多運算，對許多解法進行取樣或搜尋。
- [符號 AI、搜尋與規劃](../../theory/paradigms/symbolic-ai/index.md)：形式演繹與證明搜尋，是定理證明的古典一側，AlphaGeometry 把它與神經模型結合。
- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：從證明檢查器的判定中學習證明策略，AlphaProof 一類系統即是如此。

## 相關連結

- 機器學習所用的數學基礎見[數學](../../theory/math/index.md)頁。
- 形式證明與符號搜尋是本頁的理論面。見[符號 AI](../../theory/paradigms/symbolic-ai/index.md)。
- 人們如何建構證明、直覺從何而來，是[認知科學](../../brain-mind/cognitive-science/index.md)的研究對象。數學直覺也是 AI 引導發現所嘗試建模的問題之一。
- 競賽數學同時也是推理模型的基準，見[推理模型](../../theory/models/reasoning/index.md)。

## 應用

- 在 Lean 等證明助手中檢查與撰寫形式證明
- 協助數學家找出規律、檢驗猜想
- 軟體與硬體的自動驗證，使用的正是同一套證明技術
- 數學推理的教學與評量（見[教育](../education/index.md)）

## 風險與限制

- **基準污染**：公開競賽的題目可能已出現在訓練資料中，使分數被高估。
- **錯誤形式化**：對錯誤命題做出的機器檢查證明，是一種容易被忽略的失敗。
- **誇大宣稱**：奧林匹亞等級表現的報告，涵蓋的是經挑選的題目與特定的形式環境。
- **歸屬**：當發現來自程式搜尋時，結果的信用與理解需要分開處理。

## 開放問題

- 形式證明搜尋能否擴展到研究等級的數學，而那裡的形式函式庫仍然稀少。
- 數學家應如何引用、檢驗與信任有 AI 協助產生的結果。

## 參考文獻

### 開創性論文

- Hendrycks, D. et al. (2021). Measuring Mathematical Problem Solving With the MATH Dataset. arXiv. https://arxiv.org/abs/2103.03874 — 含逐步解答的競賽等級數學題基準，用於衡量語言模型的推理能力。
- Cobbe, K. et al. (2021). Training Verifiers to Solve Math Word Problems. arXiv. https://arxiv.org/abs/2110.14168 — 提出 GSM8K 基準，並訓練驗證器對取樣得到的解答排序。
- de Moura, L. & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. *CADE 2021, Lecture Notes in Computer Science*. https://doi.org/10.1007/978-3-030-79876-5_37 — 介紹 Lean 4，是多數現行形式數學 AI 系統所用的證明助手。
- Trinh, T. H. et al. (2024). Solving olympiad geometry without human demonstrations. *Nature*. https://doi.org/10.1038/s41586-023-06747-5 — 以語言模型搭配符號演繹引擎，解決奧林匹亞幾何題。
- Romera-Paredes, B. et al. (2024). Mathematical discoveries from program search with large language models. *Nature*. https://doi.org/10.1038/s41586-023-06924-6 — 以語言模型提出程式、由評估器評分，產生新的數學構造。
- Hubert, T. et al. (2025). Olympiad-level formal mathematical reasoning with reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-025-09833-y — 介紹 AlphaProof，以強化學習在 Lean 中學習證明形式化的奧林匹亞題。

### 綜述與教科書

- Davies, A. et al. (2021). Advancing mathematics by guiding human intuition with AI. *Nature*. https://doi.org/10.1038/s41586-021-04086-x — 展示學習模型如何提出猜想，再由數學家證明，涵蓋紐結理論與表示論。
- Lample, G. & Charton, F. (2019). Deep Learning for Symbolic Mathematics. arXiv. https://arxiv.org/abs/1912.01412 — 訓練序列到序列模型求解積分與微分方程。
