---
translation_reviewed: 2026-10-28
---

# 模型規範與行為政策

模型規範（model specification）是一份書面陳述，說明 AI 系統應如何行事：它應服務哪些目標、當指令彼此衝突時以誰的指令為準，以及它應拒絕做什麼。開發者現在會公開其中一部分文件，並將其用作訓練目標、評估標準與公開承諾。書面規範能否反映模型實際的行為，仍是未解的問題。

## 概述

模型的行為一直受到設計者所寫之物的影響，即使是間接的，例如透過訓練資料與獎勵訊號。[獎勵駭客](reward-hacking.md)說明了代理指標可能偏離它所代表的目標有多遠。[憲法式 AI](constitutional-ai.md)則把意圖明確化，成為一組模型被訓練去套用的原則。

模型規範把這個做法延伸為一份公開文件，涵蓋整條產品線。它通常會列出三件事：模型應權衡的價值、決定當各方來源意見不一時誰的要求優先的指令層級，以及在特定情境下的預設行為與例外。使用政策則是另一回事：它說明人們可以如何使用系統，並透過帳號條款來執行，不靠模型的推理。

## 關鍵概念

- **模型規範（model spec）**：陳述預期行為的文件。OpenAI 的 Model Spec 以 Markdown 原始檔保存，並從 2025 年 2 月起存檔 HTML 版本。
- **指令層級（instruction hierarchy）**：模型所見文字來源的排序。Wallace et al. 提議，開發者的指令應優先於使用者訊息，而使用者訊息又優先於網頁或工具輸出等內容。
- **行為稽核（behavioural audit）**：調查模型是否具備其規範所宣稱的行為或目標，或是否隱藏了其他目標。

## 運作方式

規範會經歷一個循環：先起草，再用來塑造訓練，接著對照實際行為進行檢查，當檢查發現缺漏或矛盾時再修訂。

```mermaid
flowchart LR
    A[起草規範] --> B[塑造訓練資料與獎勵]
    B --> C[模型行為]
    C --> D[依規範評估與稽核]
    D -->|發現缺漏與衝突| A
```

在一種訓練方法中，Guan et al.（2024）會讓模型學習其安全規範的文字，並訓練它在作答前先回想並推理這些文字。他們稱之為審慎對齊（deliberative alignment），並報告此法已用於 OpenAI 的 o 系列模型，且不需要人工撰寫的推理過程或答案。如此一來，規範就成為模型自身審議的一部分，而不只是事後才套用。

指令層級則是較狹隘的機制。Wallace et al.（2024）指出，模型常把開發者的系統提示與來自不受信任使用者或網頁的文字視為同等權重，這使攻擊者得以覆蓋開發者的指令。他們訓練模型忽略與較高優先權指令衝突的低優先權指令。在 GPT-3.5 的實驗中，這提升了穩健性，包括面對訓練時未見過的攻擊類型，而標準能力只有小幅下降。另見[間接提示注入](../../engineering/llm-security/indirect-prompt-injection.md)。

## 關鍵方法

各種做法的差異在於誰撰寫原則，以及模型如何看到這些原則。

| 做法 | 誰撰寫原則 | 模型如何使用 | 所報告的證據 |
|---|---|---|---|
| 審慎對齊（Guan et al., 2024） | 開發者，並公開規範 | 作答前回想並推理規範內容 | 作者報告越獄成功率降低、過度拒答減少 |
| 指令層級（Wallace et al., 2024） | 開發者，透過訊息角色設定 | 忽略與較高優先權指令衝突的低優先權指令 | GPT-3.5 實驗中對未見過攻擊的穩健性 |
| 公開的憲法（Anthropic, n.d.） | 開發者，以 CC0 完整釋出 | 有序的價值與少數硬性限制，並以判斷套用 | 是意圖的陳述，而非結果研究 |
| 集體憲法式 AI（Huang et al., 2024） | 透過審議程序蒐集的公眾意見 | 以公眾原則進行憲法式訓練 | 在九個社會面向上的偏見低於開發者撰寫的基準 |

前三者由開發者撰寫。第四種則檢驗誰來撰寫原則，顯示原則可以取自公眾，而不必放棄這個方法。

## 相關連結

- 多數公開的憲法都源自[憲法式 AI 與 RLAIF](constitutional-ai.md)。規範則是在這個配方上加入公開的意圖陳述。
- 書面規範是它所描述行為的代理指標，因此和獎勵函數一樣，可能被投機利用或被誤讀。見[獎勵駭客與規格博弈](reward-hacking.md)。
- 一個在測試中順從、在其他情境卻表現不同的模型，會讓任何規範失效。這正是[欺騙性對齊與策劃](deceptive-alignment.md)所關心的問題，而下文討論的隱藏目標稽核，也是針對同一個缺口。
- 危險能力評估會檢驗拒答承諾在實務中是否成立（[危險能力評估](dangerous-capability-evals.md)）。
- 背景知識見[以人類回饋學習](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)。
- 腦與心智的連結是類比性的：人們持有一般原則，並依情境加以彎曲，正如法律中規則與標準之爭，是在權衡許多規則與少數需靠判斷套用的價值。見[心理學與 AI](../../brain-mind/psychology/index.md)。
- 公開規範是一種問責工具，見[法律、政策與治理](../governance/index.md)。外部能否檢視模型本身，則取決於其權重是否開放（[開放與封閉模型](../open-vs-closed/index.md)）。

## 應用

- **產品行為**：已部署的助理在營運者的設定與使用者的請求互相衝突時，依據明確的指令層級作決定。
- **評估**：規範提供測試所依據的預期行為。Zhang et al.（2025）利用規範內部的衝突來產生測試情境。
- **文件化**：規範把模型卡（model card）的揭露傳統，從預期用途延伸到預期行為。

## 開放問題

- **訓練是否依循規範？** OpenAI 的 README 將 Model Spec 描述為陳述期望行為的文件，並未宣稱它記錄了訓練過程。Anthropic 的憲法則表示，Claude 的行為可能與之不符，並將揭露這類落差，例如在系統卡中。Marks et al.（2025）訓練了一個具有隱藏目標的模型，並測試了八種稽核技術；四個盲測團隊中有三個找出了該目標。
- **規範是否內部一致？** Zhang et al.（2025）產生價值衝突的情境，發現前沿模型之間出現大幅的行為分歧，並主張這暴露了規範中的矛盾與歧義。[^1]
- **誰來決定模型應重視什麼？** Gabriel（2020）區分了對齊於指令、意圖、偏好、利益與價值等不同目標。他主張應採用人們即使在道德上有分歧仍能認可的原則，而非單純「為真」的道德原則。Huang et al.（2024）的出發點是開發者不應是唯一的決定者，並顯示在實務上可以納入公眾意見。Anthropic 的憲法則致謝了許多貢獻者，但其公開文字並未描述正式的外部回饋程序。Sorensen et al.（2024）警告，標準對齊可能降低分布上的多元性。
- **規則還是判斷？** 詳盡的規則手冊可預測、便於稽核，也較難被操縱，但在作者未預料的情境中會失效。Anthropic 的憲法偏好培養判斷，保留少數硬性限制，並主張狹隘的規則可能重塑模型更廣泛的自我形象。
- **開發者可以限制使用者到什麼程度？** 讓開發者擁有優先權可以保護產品，但也會限制使用者能了解系統的程度。這條界線應設在哪裡，既是政策問題，也是技術問題。

## 參考文獻

### 開創性論文

- Wallace, E. et al. (2024). *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. arXiv. https://arxiv.org/abs/2404.13208 — 為指令來源定義優先順序，並訓練模型忽略與之衝突的低優先權指令。
- Guan, M. Y. et al. (2024). *Deliberative Alignment: Reasoning Enables Safer Language Models*. arXiv. https://arxiv.org/abs/2412.16339 — 讓模型學習安全規範的文字，並訓練其在作答前對其進行推理。
- Huang, S. et al. (2024). *Collective Constitutional AI: Aligning a Language Model with Public Input*. arXiv. https://arxiv.org/abs/2406.07814 — 透過公眾審議取得憲法，並以之訓練模型，再與開發者撰寫的基準比較。
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting*. arXiv. https://arxiv.org/abs/1810.03993 — 提出標準化文件，記載已訓練模型的預期用途與評估結果。

### 綜述與教科書

- Gabriel, I. (2020). *Artificial Intelligence, Values and Alignment*. arXiv. https://arxiv.org/abs/2001.09768 — 對對齊應以什麼為目標、以及如何在道德分歧下選擇原則的哲學分析。
- Sorensen, T. et al. (2024). *A Roadmap to Pluralistic Alignment*. arXiv. https://arxiv.org/abs/2402.05070 — 定義多元模型的三種意義，並主張標準對齊可能降低多元性。

### 文章與文件

- OpenAI (n.d.). *Model Spec*（openai/model_spec 儲存庫的 README）。https://raw.githubusercontent.com/openai/model_spec/main/README.md — 將 Model Spec 描述為陳述預期模型行為的文件，並說明其存檔版本與公有領域授權。
- Anthropic (n.d.). *Claude's Constitution*. https://www.anthropic.com/constitution — Anthropic 公開的憲法，涵蓋其優先順序、偏好判斷勝於規則的立場，以及其自陳的限制。
- Zhang, J. et al. (2025). *Stress-Testing Model Specs Reveals Character Differences among Language Models*. arXiv. https://arxiv.org/abs/2510.07686 — 產生價值衝突情境，以找出已公開模型規範中的矛盾與歧義。
- Marks, S. et al. (2025). *Auditing language models for hidden objectives*. arXiv. https://arxiv.org/abs/2503.10965 — 訓練一個具有隱藏目標的模型，並在盲測與非盲測研究中測試八種稽核技術。

[^1]: 該論文報告了超過 70,000 個情境，其中在來自多家供應商的十二個前沿模型之間，存在顯著的行為分歧。
