---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/llm/instructgpt-rlhf
tags:
  - alignment
  - policy
aliases:
  - Model specifications
  - Model spec
  - Instruction hierarchy
  - 模型規範
  - 指令層級
---

# 模型規範與行為政策

模型規範（model spec）是一份說明 AI 系統預期行為的文件：它預設應該做什麼、應該拒絕什麼、如何衡量來自不同當事人的指令，以及衝突時如何解決。開發者會公開這類文件，或其中的部分，讓外部人士能比較預期行為與實際觀察到的行為。它是以原則為基礎的對齊中最明顯的形式之一，與[憲法式 AI](constitutional-ai.md)並列。

## 概覽

語言模型會同時收到來自多個來源的指令：打造產品的開發者、部署模型的企業，以及輸入文字的使用者。模型自身也有預設行為。模型規範定義當這些指令衝突時，哪一方應該優先。例如，開發者可以把模型限制在某個主題，但使用者仍應被告知某個請求超出範圍；某些對使用者的保護，則無論開發者如何指定都不能被覆寫。

這既是政策問題，也是技術問題。規範會對模型應該與不應該做什麼做出選擇，而這些選擇會影響許多使用者。公開規範讓人們可以對這些選擇提出異議。沒有規範時，行為仍然可以被塑造，但塑造的過程較不透明。

## 核心概念

- **指令層級（instruction hierarchy）**：對指令來源（例如系統、開發者、使用者與工具輸出）的排序，決定哪一個指令優先。
- **預設行為（default behaviour）**：當沒有指令涵蓋某種情況時，模型的做法。
- **硬性限制（hard constraints）**：任何指令都無法改變的行為。
- **稽核（auditing）**：把觀察到的行為與宣告的規範做比對。

## 行為如何被規定

規範在三個層面運作。有些規則以原則的形式陳述，例如尊重使用者的自主權，或避免對模型本身的性質撒謊。有些則以期望與不期望回應的範例來陳述，這能使意圖具體化，但可能留下缺口。第三個層面是訓練方法，它決定規範如何被轉化為行為。

有兩種訓練方法把規範直接與模型連結。Wallace et al.（2024）訓練模型嚴格遵守指令層級，使得來自較低優先級來源（例如工具輸出）的指令，在與較高優先級指令衝突時不會被遵從。他們報告這改善了對提示注入的穩健性，同時指出這並未完全消除問題。Guan et al.（2024）提出審慎對齊（deliberative alignment），訓練模型在回應前先回想安全規範中的相關部分並加以推理。模型會拿到規範的文字，因此行為是依據書面規則，而不只是依據範例。

Askell et al.（2021）描述了同一方向上更早的一步。他們使用一個經過訓練、具備有用、誠實與無害特質的通用語言助理，作為對齊方法的測試平台，並主張明確的行為目標使進展可以被衡量。

## 稽核

書面規範使稽核成為可能。評估者可以針對每條規則撰寫測試提示，並檢查模型是否遵從。規範與觀察到的行為之間的落差，就是訓練缺口、規範缺口或兩者並存的證據。稽核面臨與其他評估相同的困難：有限的測試無法涵蓋所有情況，而在測試中表現良好的模型，在部署時可能不同（參見[危險能力評估](dangerous-capability-evals.md)）。

## 關於誰來決定的爭議

規範會引發一些並非純技術性的問題：

- **權威。** 規範由開發者撰寫，但受模型行為影響的人並未參與。有些提案主張應納入公眾意見，或提供使用者可以選擇的相互競爭的規範。
- **價值。** 規範說明當價值衝突時哪個優先，例如安全與使用者自主。合理的人對此有不同的權衡，而規範本身無法解決這個問題。
- **透明度。** 公開規範有助於外部人士檢查行為，但規範可能描述意圖，卻未描述實現它的訓練資料或程序。
- **在地規範。** 單一的全球規範，未必符合每個部署地點的法律或文化期待。

這些爭議與更廣泛的[治理](../governance/index.md)和[倫理](../ethics/index.md)辯論相連。

## 相關連結

規範類似專業團體所發布的行為準則，例如醫療守則規定醫師對病人的義務，以及執業的界線。這個類比顯示，透過訓練與審查落實的明文規範，可以以可預測的方式塑造行為，不過模型並不是會受專業懲戒約束的從業者。遵循指令層級的模型也引出一個問題：系統如何區分指令與資訊，這在[語言模型](../../theory/models/llm/index.md)的研究中有所探討。

## 應用

- 開發者公開的模型規範，用來向使用者、部署者與研究者說明預期行為。
- 以指令層級訓練，以減少處理不可信內容的代理中的提示注入。
- 依書面規則自動稽核模型行為。

## 開放問題

- 規範能有多完整？遇到未涵蓋的情況時應該怎麼做？
- 誰應該決定規範所編碼的優先順序？受影響的群體如何參與？
- 以書面規範為推理依據的訓練方法，能否推廣到規範未預料的情況？

## 參考文獻

### 開創性論文

- Askell, A. et al. (2021). *A General Language Assistant as a Laboratory for Alignment*. arXiv:2112.00861. https://arxiv.org/abs/2112.00861 — Uses a helpful, honest and harmless assistant as a testbed for measuring progress on alignment.
- Wallace, E. et al. (2024). *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. arXiv:2404.13208. https://arxiv.org/abs/2404.13208 — Trains models to prioritise system and developer instructions over conflicting user or tool instructions, improving resistance to prompt injection.
- Guan, M. Y. et al. (2024). *Deliberative Alignment: Reasoning Enables Safer Language Models*. arXiv:2412.16339. https://arxiv.org/abs/2412.16339 — Trains models to reason over a written safety specification before responding.

### 綜述與教科書

- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 — Uses a written set of principles to guide training, the approach that stated specifications build on.

### 文章與文件

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — Developer policy that connects stated commitments to required safeguards, an example of a published behaviour and safety commitment.
