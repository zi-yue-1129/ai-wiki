---
translation_reviewed: 2026-10-28
aliases:
  - 錯誤信念測驗
  - False-belief tests
---

# 語言模型的錯誤信念測驗（Kosinski，2023）

Kosinski 問：大型語言模型能否通過錯誤信念任務？這是兒童心智理論的標準測驗。論文測試了 11 個模型，並報告表現隨模型大小與世代大幅提升。本主題屬於[心理學與 AI](../index.md)。

## 問題

大型語言模型能否解決錯誤信念任務？成功是否取決於模型大小？兒童大約四歲起就能可靠地通過這些任務，因此它是一個不易靠運氣通過的基準。

## 核心想法

每個情境中，角色對某物件或位置的信念都與事實不符；接著模型被問到角色會怎麼想或怎麼做。正確回答需要追蹤角色的信念，而不是世界的真實狀態。每項任務寫成八種情境變體，共 16 個提示；只有模型 16 題全部答對，該任務才算通過。

## 程序

1. 寫出錯誤信念情境：主角持有一個已被現實推翻的信念。
2. 提出只能靠追蹤主角信念才能正確回答的問題。
3. 在八種變體中重複，每項任務共 16 個提示。
4. 為每個模型評分，只有 16 題全對才算通過，並比較不同大小與世代的模型。

## 結果

摘要指出測試了 11 個模型。較小與較舊的模型一題都沒通過。GPT-3-davinci-003 與 ChatGPT-3.5-turbo 各通過約 20%，ChatGPT-4 通過 75%。作者把這個水準與早期研究中六歲兒童的表現相比。

## 限制

- 通過測驗並不能證明模型擁有心理狀態。作者把心智理論自發出現視為一種可能，而非定論。
- 後續研究發現結果脆弱。微小的改寫就能推翻已報告的成功（Ullman, 2023），而對抗性測試顯示社會推理並不一致（Shapira et al., 2023）。
- Sap et al. (2022) 報告 GPT-3 在相關的社會任務上遠低於人類準確率，因此結論取決於所用的基準。

## 連結

- 定義這個術語的黑猩猩測驗見[黑猩猩心智理論測驗](../chimpanzee-theory-of-mind/index.md)。
- 關於這些模型是否具有心智理論的爭議，見母頁的[心智理論](../index.md)一節。

## 參考文獻

### 開創性論文

- Kosinski, M. (2023). Evaluating Large Language Models in Theory of Mind Tasks. arXiv. https://arxiv.org/abs/2302.02083 — 在錯誤信念任務上測試 11 個語言模型；ChatGPT-4 通過約 75%。
- Ullman, T. (2023). Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks. arXiv. https://arxiv.org/abs/2302.08399 — 保留相同原理的微小改動，會推翻 LLM 在心智理論任務上的成功。
- Sap, M. et al. (2022). Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs. arXiv. https://arxiv.org/abs/2210.13312 — 發現 GPT-3 在社會與心智理論問題上的準確率遠低於人類。
- Shapira, N. et al. (2023). Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large Language Models. arXiv. https://arxiv.org/abs/2305.14763 — 對抗性測試顯示，LLM 的社會推理並不一致，可能依賴淺層啟發式。
- Rabinowitz, N. C. et al. (2018). Machine Theory of Mind. arXiv. https://arxiv.org/abs/1802.07740 — ToMnet，一個以元學習建立的網路，能建模其他主體並在格子世界中通過 Sally–Anne 錯誤信念測驗。
