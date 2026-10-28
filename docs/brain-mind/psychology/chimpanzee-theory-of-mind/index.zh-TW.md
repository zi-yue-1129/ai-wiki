---
translation_reviewed: 2026-10-28
aliases:
  - 黑猩猩心智理論測驗
  - Chimpanzee theory of mind
---

# 黑猩猩心智理論測驗（Premack 與 Woodruff，1978）

Premack 與 Woodruff 問：黑猩猩能否把目標歸因給人類演員？黑猩猩先觀看一段影片，內容是一個人努力解決問題，然後在可能解法的照片之間做選擇。這篇論文提出了「心智理論」一詞來稱呼這種能力。它是本主題的第一個代表性方法；見[心理學與 AI](../index.md)。

## 問題

動物能否推斷另一個主體想做什麼，還是只會回應眼前看到的動作？測驗必須把目標歸因與單純對所見做出反應區分開來。

## 核心想法

若黑猩猩穩定地選中能解決演員問題的照片，作者便主張牠理解的是演員的目標，而不只是看到的動作。影片中的演員被呈現為陷入困境，因此黑猩猩選擇的解法，反映了牠認為演員想要什麼。

## 程序

1. 讓一隻成年黑猩猩觀看一系列影片，內容是人類演員努力解決各種問題。
2. 呈現幾張可能解法的照片，其中一張能解決影片中的問題。
3. 記錄黑猩猩選了哪張照片。
4. 若牠穩定地選中正確照片，便推論牠把目標歸因給演員。

## 結果

摘要報告黑猩猩穩定地選中正確照片。摘要沒有給出試驗次數或統計數字，因此數字需要查閱全文核對。

## 限制

- 研究只測試一隻成年黑猩猩，無法說明這個結果有多典型。
- 在接受目標歸因之前，必須先排除較單純的解釋，例如場景與圖片之間習得的關聯。設計是否做到這點，至今仍有爭議。
- 測驗只涉及一個狹窄情境中的目標，並未另外測試對世界的信念。後來針對錯誤信念的研究處理的正是這個缺口。

## 連結

- 機器上的同類問題，見[語言模型的錯誤信念測驗](../false-belief-llms/index.md)。
- 測驗背後的心智狀態概念，連到母頁的[心智理論](../index.md)一節。

## 參考文獻

### 開創性論文

- Premack, D. & Woodruff, G. (1978). Does the chimpanzee have a theory of mind? *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X00076512 — 首次提出「心智理論」一詞，並以錄影與照片的測驗檢驗黑猩猩是否把目標歸因給人類演員。
- Rabinowitz, N. C. et al. (2018). Machine Theory of Mind. arXiv. https://arxiv.org/abs/1802.07740 — ToMnet，一個以元學習建立的網路，能建模其他主體的行為，並在格子世界中通過 Sally–Anne 錯誤信念測驗。
- Sap, M. et al. (2022). Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs. arXiv. https://arxiv.org/abs/2210.13312 — 發現 GPT-3 在社會與心智理論問題上的準確率遠低於人類。
- Ullman, T. (2023). Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks. arXiv. https://arxiv.org/abs/2302.08399 — 保留相同原理的微小改動，會推翻 LLM 在心智理論任務上的成功。
- Shapira, N. et al. (2023). Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large Language Models. arXiv. https://arxiv.org/abs/2305.14763 — 對抗性測試顯示，LLM 的社會推理並不一致，可能依賴淺層啟發式。
