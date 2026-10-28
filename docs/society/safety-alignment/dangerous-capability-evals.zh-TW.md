---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/governance
tags:
  - alignment
  - evaluation
  - safety policy
aliases:
  - Dangerous capability evaluations
  - Frontier safety frameworks
  - 危險能力評估
  - 前沿安全框架
---

# 危險能力評估與前沿安全框架

危險能力評估測試 AI 模型是否具備可能造成嚴重危害的能力，例如對生物或化學武器提供實質協助、進行攻擊性網路行動，或自主複製。前沿安全框架則是把這些測試結果連結到各種承諾的政策：哪些能力等級觸發哪些防護措施，以及何時不得部署模型。兩者合起來，是開發者決定一個模型是否可以發布的主要方式之一。

## 概覽

通用模型可以用於許多任務，因此某種能力在多數人手中無害，對少數誤用仍可能很重要。評估者因此測試那些若存在就會很嚴重的特定能力，而不只是測量平均表現。Shevlane et al.（2023）主張，這類評估應成為負責任開發的標準部分，並列出此類測試應涵蓋的風險類別。

目前出現了兩種結構。第一種是評估套件：一組從問答到多步驟代理工作的任務，以門檻來評分。第二種是把分數與行動連結起來的政策。Anthropic 的負責任擴展政策定義了 AI 安全等級，其防護措施隨能力提高；Google DeepMind 的前沿安全框架則為網路與自主性等領域命名了關鍵能力等級。其他開發者也以不同名稱發布類似的框架。

## 核心概念

- **能力門檻（capability threshold）**：預先在測試前設定的表現水準，達到時該模型被視為需要更強的防護措施。
- **部署前評估（pre-deployment evaluation）**：發布前的測試，通常由開發者進行，有時由外部機構進行。
- **能力誘發（elicitation）**：為了顯現模型能力所付出的努力，例如提示、工具與微調。誘發不足的評估會低估風險。
- **防護措施（safeguard）**：降低能力可被用於傷害的風險的措施，例如拒絕政策、分類器或存取控管。

## 運作方式

典型的循環包含四個步驟。開發者在訓練模型之前，先定義風險領域與門檻。他們對候選模型進行評估，包括給模型工具與多步驟任務的測試。若達到門檻，框架要求在部署前採取特定的防護措施，若無法達成，則可能要求暫停開發。結果記錄在模型卡或系統卡中。

Phuong et al.（2024）在 Google DeepMind 工作，描述了數種危險能力的評估，包括說服、網路安全任務與自我擴散，並報告數個前沿模型在這些任務上的結果。Kinniment et al.（2023）在實際的自主任務上評估語言模型代理，例如多步驟的軟體與研究工作，以了解模型能多大程度完成對自主複製有意義的任務。生物風險則以 WMDP 等基準評估。Li et al.（2024）建立該基準，用來衡量生物安全、網路安全與化學安全中的危險知識，並用它來測試遺忘方法。

## 主要方法

評估的實務仍在形成中，因此關鍵項目較適合被描述為方法，而非單一演算法：

- **能力基準**（Li et al., 2024；Phuong et al., 2024）：固定的問題集或任務，依門檻評分。它們容易重複執行，但可能被鑽漏洞，也可能過時。
- **代理任務評估**（Kinniment et al., 2023）：給模型工具與開放式任務。它們更能反映真實能力，但成本較高，也較難標準化。
- **前沿安全框架**（Anthropic, 2024；Google DeepMind, 2024）：把結果連結到必要防護措施與部署決策的政策。
- **第三方評估**：外部機構獨立進行測試。Shevlane et al.（2023）支持這種做法，因為開發者有動機只報告有利的結果。

## 限制

- **誘發不足。** 測試可能漏掉一個更有決心的使用者能找出的能力。部署前的結果是下界。
- **基準的效度。** 測量知識的測試，未必能測量模型能否應用這些知識；測量某項任務的測試，也未必能預測其他任務。
- **存取權限。** 外部評估者對模型與其工具的存取，通常少於開發者。
- **時機。** 評估在發布前進行，但在微調、部署與新工具之後，能力可能改變。
- **自我評估。** 由開發者撰寫的框架，取決於開發者對門檻的判斷，這也是外部審查常被提出的原因。

## 相關連結

風險評估在工程與公共衛生中有悠久的歷史，其中門檻與獨立測試是常態。飛機適航認證與藥物試驗是常見的類比。這些類比對門檻與分階段核准的邏輯很有用，但 AI 能力與實體產品不同，它在發布後仍可能改變。什麼算是危險能力，也取決於誰會受害、以何種方式受害，這與[治理](../governance/index.md)相關。偵測模型內部的危險知識或行為，是[可解釋性](../interpretability/index.md)的一部分；而會使評估產生誤導的欺騙行為，則在[欺騙性對齊](deceptive-alignment.md)中討論。

## 應用

- 發布前的評估，並記錄在模型卡與系統卡中。
- 由政府主導的測試，例如英國與美國等國家的 AI 安全研究機構所進行的測試。
- 如 WMDP 這類基準，讓研究者比較防護措施與遺忘方法。

## 開放問題

- 當危害不確定，而某項能力的好處也很大時，該如何設定門檻？
- 當模型能隱藏能力時（如[欺騙性對齊](deceptive-alignment.md)所討論），評估能否可靠地偵測到這些能力？
- 誰應該能看到完整結果？哪些內容應該公開？

## 參考文獻

### 開創性論文

- Shevlane, T. et al. (2023). *Model evaluation for extreme risks*. arXiv:2305.15324. https://arxiv.org/abs/2305.15324 — Argues that developers should evaluate models for dangerous capabilities and sets out the risk categories such tests should cover.
- Phuong, M. et al. (2024). *Evaluating Frontier Models for Dangerous Capabilities*. arXiv:2403.13793. https://arxiv.org/abs/2403.13793 — Reports evaluations of frontier models across several dangerous-capability domains.
- Kinniment, M. et al. (2023). *Evaluating Language-Model Agents on Realistic Autonomous Tasks*. arXiv:2312.11671. https://arxiv.org/abs/2312.11671 — Evaluates language-model agents on multi-step autonomous tasks relevant to autonomous replication.
- Li, N. et al. (2024). *The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning*. arXiv:2403.03218. https://arxiv.org/abs/2403.03218 — A benchmark of hazardous knowledge in biosecurity, cybersecurity and chemical security, used to test unlearning.

### 文章與文件

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — The developer's policy defining AI Safety Levels and the safeguards required at each.
- Google DeepMind, *Introducing the Frontier Safety Framework*, 17 May 2024. https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/ — Describes critical capability levels and the procedure for responding when a model reaches them.
