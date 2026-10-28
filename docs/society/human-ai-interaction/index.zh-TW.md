---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society
  - society/interpretability
  - society/ethics
  - brain-mind/psychology
tags:
  - human-AI interaction
  - trust
  - overreliance
aliases:
  - 人機互動與信任
  - 人機互動
  - Human-AI interaction
  - Human-AI trust
---

# 人機互動與信任

人機互動研究人們如何使用、信任、過度信任 AI 系統，以及 AI 系統如何改變人。一個系統是否準確，其重要性往往不及使用者如何對它產生依賴、如何理解它，以及如何據此調整自己的工作。本節涵蓋這種關係，從信任的認知機制到解釋的設計、人在迴路中的角色，以及對技能的長期影響。

## 概述

系統可能大部分時候都正確，但仍被不當使用。人們可能過度信任它而停止檢查，也可能信任不足而忽略有用的建議，或與它形成某種改變其行為的關係，而這些改變並非任何人的本意。人機互動結合心理學、人機介面與技術社會科學，來解釋這些模式，並設計能支持更好使用方式的系統。

## 主題

| 頁面 | 重點 |
|---|---|
| [自動化偏誤與過度依賴](automation-bias.md) | 遺漏與誤作為錯誤、解釋的效果、認知強制功能、技能退化 |
| [AI 陪伴](ai-companionship.md) | 對對話式系統的情感依附及其對福祉的影響 |
| [AI 素養與大眾理解](ai-literacy.md) | 人們為了判斷 AI 輸出、參與治理所需具備的知識 |

## 核心概念

- **信任校準**：人對系統的依賴程度，與系統實際可靠度之間的吻合程度。
- **過度依賴**：依賴程度超過系統的可靠度，可能導致未被察覺的錯誤。
- **解釋設計**：系統如何呈現其理由，以及這些理由是否真的幫助人做出更好的決定。
- **人在迴路中（human-in-the-loop）**：人能審查、批准或推翻自動化決策的設計。
- **技能退化（deskilling）**：因長期依賴替自己執行某項技能的工具，而失去該技能。

## 運作方式

人們會從介面、流暢度與系統過去的表現，形成對系統的期待。當期待與系統的可靠度相符時，依賴是恰當的；不相符時，錯誤便隨之而來。解釋、信心顯示與資訊呈現的順序，都會改變這些期待，有時會在未提升準確率的情況下增加依賴。

人在迴路中的設計假設人能發現系統的錯誤。這個假設只在人有時間、資訊與技能去檢查時才成立。缺少這些條件時，形式上的人工審查可能對安全幾乎沒有幫助。同樣的疑慮也適用於那些以 AI 產出作為決策依據的組織。

## 關聯

解釋問題連結到[可解釋性](../interpretability/index.md)，該頁描述產生解釋的方法。當人們依賴自動化決策時所產生的公平性與問責問題，見[倫理與公平](../ethics/index.md)。注意力與信任的心理機制見[心理學](../../brain-mind/psychology/index.md)。

## 應用

- 臨床決策支援，臨床人員必須決定何時採納模型的建議。
- 寫作與程式設計工具，其草稿可能在未仔細閱讀的情況下被採納。
- 公部門的評分系統，官員必須為依賴自動評分的決定提出理由。
- 教育領域，AI 助教與助理會影響學生練習與學習的方式。

## 未解問題

- **哪些設計選擇能在不同使用者與任務中產生校準的信任？**
- **長期改變。** 反覆使用如何在數月與數年間塑造技能、期待與關係。
- **責任歸屬。** 當人接受了一個後來被證明錯誤的 AI 建議時，誰應負責。

## 參考文獻

### 開創性論文

- Parasuraman, R. & Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors*, 52(3), 381–410. https://doi.org/10.1177/0018720810376055 — 回顧自滿與偏誤如何影響自動化系統的使用。
- Bansal, G. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717 — 發現解釋並未提升互補的團隊表現，但會提高人接受 AI 建議的機率。
- Vasconcelos, H. et al. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*, 7(CSCW1). https://doi.org/10.1145/3579605 — 以成本效益架構主張，解釋在某些情境中能降低過度依賴。
- Bainbridge, L. (1983). Ironies of automation. *Automatica*, 19(6), 775–779. https://doi.org/10.1016/0005-1098(83)90046-8 — 討論自動化的諷刺，如其標題所示。

### 綜述與教科書

- Lee, H.-P. et al. (2025). The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers. *Proceedings of CHI 2025*. https://doi.org/10.1145/3706598.3713778 — 以知識工作者的調查，報告生成式 AI 使用時自述的認知投入與信心降低。

## 延伸學習

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — 語言模型運作方式的背景知識，有助於判斷何時需要檢查其輸出。
