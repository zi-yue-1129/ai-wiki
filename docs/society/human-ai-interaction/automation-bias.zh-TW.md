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

Parasuraman 與 Manzey（2010）回顧自滿與自動化偏誤的研究，並將其與注意力模型整合。他們的說明是：人會在監控工作與自動系統之間分配注意力。當系統可靠時，監控變得較不頻繁、也較不周全，因而降低了發現系統偶發錯誤的機會。結果取決於輔助工具的可靠度、人的工作負荷，以及錯誤被查核的難易程度。

Skitka、Mosier 與 Burdick（1999）在飛行模擬的情境中，以自動監控輔助工具測試這一點。他們發現，當輔助工具未標示問題時，人們會犯遺漏錯誤；當他們遵循錯誤的建議時，則會犯誤作為錯誤。他們的結論是，這些錯誤是依賴輔助工具的可量測代價，而不只是粗心所致。

## 主要方法

實驗研究在嘗試降低此效應時採取的方式各有不同：

- **解釋。** Bansal 等人（2021）研究 AI 解釋是否有助於人機團隊。他們報告，解釋往往增加人們採納 AI 建議的頻率，包括錯誤的建議，因此團隊表現的提升在不同任務間並不一致。
- **關於檢查的成本效益推理。** Vasconcelos 等人（2023）主張並檢驗：當檢查解釋的努力相對於發現錯誤的效益來說較低時，解釋能降低過度依賴。
- **認知強制功能。** Buçinca、Malaya 與 Gajos（2021）引入一些設計，延遲或結構化 AI 的回答，讓人在接受之前先思考。這些設計降低了過度依賴，但參與者常認為它們較不有幫助，顯示有用之處與人們的偏好之間存在落差。

## 實務中的證據

航空與醫療的研究早於生成式 AI，而其發現已被應用於 AI 決策支援。語言模型的過度依賴已在寫作、程式設計與資訊搜尋任務中被研究，在這些任務中，看似合理卻錯誤的答案可能在未檢查的情況下被接受。Lee 等人（2025）對知識工作者進行調查，報告對生成式 AI 工具的信心較高，與自述的批判性思考較少相關；而對自身技能的自信較高，則與批判性思考較多相關。該研究以自述為依據且屬橫斷面設計，因此顯示的是關聯，而非因果。

## 技能退化與認知卸載

Bainbridge（1983）描述了自動化的「諷刺」：將任務自動化，會移除維持操作人員技能所需的練習，而剩下的人工任務，例如處理罕見的故障，正是最需要技能的部分。同樣的論點也被用於生成式 AI：一個從不起草或檢查解答的工作者，可能會失去做這些事的能力。這方面的證據仍然有限，研究者區分了兩種卸載：一種釋放注意力、讓人做更好的工作；另一種則侵蝕人所需的技能。

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

- Skitka, L. J., Mosier, K. L. & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5), 991–1006. https://doi.org/10.1006/ijhc.1999.0252 — 實驗研究人們在監控任務中使用自動輔助工具時的遺漏與誤作為錯誤。
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — 主張將流程自動化會移除操作人員處理故障所需的練習。
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — 檢驗 AI 解釋是否提升互補的人機團隊表現，並發現效果取決於任務。
- Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1). https://doi.org/10.1145/3449287 — 顯示認知強制功能能降低過度依賴，而參與者較不喜歡這類功能。
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — 主張並檢驗：當檢查成本相對於效益較低時，解釋能降低過度依賴。
- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — 以知識工作者的調查，將對生成式 AI 的信心與批判性思考建立關聯。

### 綜述與教科書

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — 回顧自滿與自動化偏誤，並將其整合為注意力分配的說明。

## 延伸學習

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — 語言模型運作方式的背景知識，有助於判斷何時需要檢查其輸出。
