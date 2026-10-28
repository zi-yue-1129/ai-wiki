---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/human-ai-interaction
  - society/interpretability
  - brain-mind/psychology
tags:
  - automation bias
  - overreliance
  - human-AI interaction
  - skill erosion
aliases:
  - 自動化偏誤
  - 過度依賴
  - Automation bias
  - Overreliance
---

# 自動化偏誤與過度依賴

自動化偏誤是指人們過於輕易地依賴自動化輔助工具的輸出，以致錯過輔助工具未標示的問題，並接受其錯誤的建議。過度依賴是當輔助工具是 AI 系統時，同樣模式的較廣義用語，包括語言模型。這種效應在航空與醫療中已有大量記錄，現在也是使用生成式 AI 工作的人們所關切的核心問題。

## 概述

使用自動化輔助工具的人面臨一種取捨。檢查輔助工具的輸出需要花費心力，而如果工具通常是正確的，檢查似乎就不必要。隨著時間推移，信任的習慣可能超過工具的可靠度，錯誤因而未被察覺。自動化偏誤描述由此產生的兩類錯誤：遺漏錯誤，即人因為輔助工具未發出警示而沒有採取行動；誤作為錯誤，即人依據輔助工具的錯誤建議採取行動。過度依賴則是在日常工作中，同一模式在 AI 系統所提供建議上的表現。

## 核心概念

- **遺漏錯誤**：因為自動化輔助工具沒有標示問題，而未能注意到或回應問題。
- **誤作為錯誤**：儘管有其他資訊，仍依據自動化輔助工具的錯誤建議行事。
- **自滿（complacency）**：當自動系統過去表現可靠時，對它的監控減少。
- **認知卸載（cognitive offloading）**：將心智工作交給外部工具，可能減少人在該工作上投入的心力。
- **技能退化（deskilling）**：因缺乏練習而失去技能，長期自動化可能導致此結果。

## 運作方式

Parasuraman 與 Manzey（2010）回顧自滿與自動化偏誤的研究，並依其標題所示，將其整合為注意力的說明。依此觀點，關鍵在於人如何在監控與自動系統之間分配注意力。當系統可靠時，監控變得較不頻繁、也較不周全，因而降低了發現系統偶發錯誤的機會。結果取決於輔助工具的可靠度、人的工作負荷，以及錯誤被查核的難易程度。

Skitka、Mosier 與 Burdick（1999）研究自動決策輔助是否使人的判斷產生偏誤，論文標題即為〈Does automation bias decision-making?〉。

## 主要方法

實驗研究在嘗試降低此效應時採取的方式各有不同：

- **解釋。** Bansal 等人（2021）檢驗 AI 解釋是否能提升互補的團隊表現，即團隊的表現優於人或 AI 單獨作業時。
- **關於檢查的成本效益推理。** Vasconcelos 等人（2023）報告，一般而言 AI 提供解釋時過度依賴並不會下降；他們以成本效益架構主張，人們會策略性地選擇是否參與解釋，因此在某些情境中解釋確實能降低過度依賴。
- **認知強制功能。** Buçinca、Malaya 與 Gajos（2021）設計三種認知強制介入，促使人更認真地思考 AI 解釋。在一項有 199 名參與者的實驗中，他們將其與兩種可解釋 AI 設計及無 AI 的基線相比。

## 實務中的證據

航空與醫療的研究早於生成式 AI，而其發現已被應用於 AI 決策支援。語言模型的過度依賴是活躍的研究領域，在這些情況中，看似合理卻錯誤的答案可能在未檢查的情況下被接受。Lee 等人（2025）以調查報告，人們使用生成式 AI 時，自述的認知投入與信心有所降低。自述測量的是人們對自己思考的說法，而非其表現的實際變化。

## 技能退化與認知卸載

Bainbridge（1983）討論自動化的「諷刺」（ironies of automation）。生成式 AI 是否也造成類似的技能流失，是尚未定論的問題，本頁不將其視為已確立。

## 關聯

自動化偏誤是[可解釋性](../interpretability/index.md)中解釋問題的行為面：解釋改變的是人們信任什麼，而不只是他們理解什麼。它也與[心理學](../../brain-mind/psychology/index.md)中啟發式與偏誤的研究相連，因為注意力與信任的同一套機制也是這些錯誤的基礎。總覽頁 [人機互動與信任](index.md) 將自動化偏誤與 AI 陪伴、AI 素養並列。

## 應用

- 臨床決策支援，模型的建議可能改變診斷。
- 使用程式設計助手的軟體開發，其生成的程式碼可能在未仔細閱讀的情況下通過審查。
- 使用自動評分的公部門決策。
- 教育領域，學生可能在未學習教材的情況下接受生成的答案。

## 未解問題

- **哪些設計能在不降低人們採納有用建議的情況下，減少過度依賴？** 有效的強制功能也會降低人們對系統的喜好。
- **長期效應。** 多數研究為短期；反覆使用是否在數月內改變技能或信任，尚未有良好的量測。
- **跨任務的推廣。** 航空與實驗室任務的結果，未必能套用到開放式的生成任務。

## 參考文獻

### 開創性論文

- Skitka, L. J., Mosier, K. L. & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5), 991–1006. https://doi.org/10.1006/ijhc.1999.0252 — 研究自動決策輔助是否使人的判斷產生偏誤，如其標題所示。
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — 討論自動化的諷刺，如其標題所示。
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — 發現解釋並未提升互補的團隊表現，但會提高人接受 AI 建議的機率。
- Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1). https://doi.org/10.1145/3449287 — 設計三種認知強制介入，並與僅有解釋的設計及無 AI 基線相比。
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — 以成本效益架構主張，解釋在某些情境中能降低過度依賴。
- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — 以知識工作者的調查，報告生成式 AI 使用時自述的認知投入與信心降低。

### 綜述與教科書

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — 回顧自滿與自動化偏誤，並將其整合為注意力分配的說明。

## 延伸學習

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — 語言模型運作方式的背景知識，有助於判斷何時需要檢查其輸出。
