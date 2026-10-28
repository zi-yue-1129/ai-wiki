---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - applications/education
  - society/privacy
  - society/governance
tags:
  - children
  - education
  - child rights
  - policy
aliases:
  - Children and AI
  - AI and children
  - AI education policy
  - 兒童與 AI
  - 兒童教育政策
---

# 兒童、教育政策與 AI

兒童在學校、家中與消費型平台上使用 AI，往往在為他們的年齡層制定規則之前就已經開始。本頁說明隨之而來的政策問題：哪些保護適用、年齡限制與同意如何運作，以及 AI 工具的設計如何影響孩子的學習。

## 概述

兒童與 AI 的政策位於三個架構的交會處：兒童權利、資料保護與教育。近年的指引多半要求 AI 從一開始就以兒童的最佳利益與發展為設計目標，而不是在成人產品上市後再加以改編。這些指引大多屬於建議性質。具約束力的規則範圍較窄，而且在許多地方仍在制定中。

## 關鍵概念

- **兒童**：法律給予特別保護的年齡界線。在美國《兒童線上隱私保護法》（Children's Online Privacy Protection Act）中，兒童指未滿 13 歲的個人（15 U.S.C. §6501）。其他法律採用不同的年齡。
- **可驗證的家長同意**：同一法律下，在現有技術條件下合理努力，確保家長在蒐集前收到營運者作法的通知，並授權蒐集兒童的個人資訊。
- **防護機制（guardrails）**：影響 AI 工具回應方式的設計，例如提示學生自己推理問題，而不是直接給出答案。

## 運作方式

政策透過三個槓桿影響兒童。

1. **使用權限與年齡限制。** UNESCO 2023 年的指引建議，為兒童獨自與生成式 AI 平台對話設定年齡限制，但未說明應是幾歲。
2. **資料保護。** 同一份指引建議強制實施資料隱私保護。UNICEF 2025 年的指引則把保護兒童的資料與隱私列為十項要求之一。在美國，《兒童線上隱私保護法》要求，在以兒童為對象的服務上蒐集未滿 13 歲兒童的個人資訊前，必須取得可驗證的家長同意。
3. **設計與教學法。** 工具是直接給答案，還是引導推理，會改變學生學到的東西。Bastani 等人（2025）在一項針對高中數學學生的實地研究中發現，未設防護機制的生成式 AI 會損害學習；而具有鼓勵推理之防護機制的家教工具，則保護了學生的學習與表現。

## 因應措施

| 做法 | 作用 | 限制 |
|---|---|---|
| 獨自使用的年齡限制 | 限制兒童獨自使用生成式 AI 平台的時機 | UNESCO 未給出年齡；確認年齡可能需要蒐集更多兒童的個人資料 |
| 家長同意與資料規則 | 要求同意，並限制向年幼兒童蒐集的資料 | 美國規則涵蓋未滿 13 歲的兒童；其他國家的門檻與規則不同 |
| 以兒童為中心的設計要求 | 為尊重兒童權利的 AI 訂定十項要求，涵蓋安全到 AI 素養 | 屬於指引，而非具約束力的法律 |
| 具防護機制的家教設計 | 引導推理，而不是直接給答案 | 證據來自特定研究，效果可能因科目與年齡而異 |

## 與其他主題的連結

- 課堂上使用的工具，例如家教與回饋系統，見[教育](../../applications/education/index.zh-TW.md)。
- 在隱私法下如何保護兒童的資料，包括以個人資料訓練的模型，見[隱私與資料保護](../privacy/index.zh-TW.md)。
- 制定這些責任的法律與標準，見[法律、政策與治理](../governance/index.zh-TW.md)。

## 應用

- **學校**決定課堂可以使用哪些 AI 工具，以及適用的年齡。
- **家長**決定孩子是否可以獨自使用 AI 服務。
- **產品團隊**為兒童打造 AI，必須符合同意與設計要求。
- **政策制定者**為 AI 服務訂定年齡限制與同意規則。

## 開放問題

- 獨自使用 AI 應適用什麼年齡限制？如何在不蒐集更多個人資料的情況下確認年齡？
- 具防護機制的家教，能否在更長的時間與數學以外的科目中保有其效益？
- 兒童應如何學習 AI 素養？UNICEF 的指引將其列為一項要求。

## 參考資料

### 奠基性論文

- Seßler, K. et al. (2023). ChatGPT for good? On opportunities and challenges of large language models for education. *Learning and Individual Differences*, 103, 102274. https://doi.org/10.1016/j.lindif.2023.102274 — 由多領域作者群撰寫，概述大型語言模型在教育中的機會與挑戰。
- Bastani, H. et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. https://doi.org/10.1073/pnas.2422633122 — 針對高中數學學生使用生成式 AI 家教的實地研究，比較有與沒有鼓勵推理之防護機制的家教。

### 文章與官方文件

- UNICEF Office of Strategy and Evidence – Innocenti（2025）。*Guidance on AI and children*, version 3.0。https://www.unicef.org/innocenti/reports/policy-guidance-ai-children — 為尊重兒童權利的 AI 政策與系統訂定十項要求，涵蓋安全、資料保護、公平、透明、包容與 AI 素養。
- Miao, F. & Holmes, W.（2023）。*Guidance for generative AI in education and research*。UNESCO。https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research — 建議強制實施資料隱私保護，並為獨自使用生成式 AI 平台設定年齡限制，且以適合年齡的方式設計教學。
- *Children's Online Privacy Protection Act*，15 U.S.C. §6501（定義）。https://www.law.cornell.edu/uscode/text/15/6501 — 定義「兒童」為未滿 13 歲的個人，並規定可驗證的家長同意。營運者的義務見 §6502。
