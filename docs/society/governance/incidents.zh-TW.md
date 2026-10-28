---
translation_reviewed: 2026-10-28
---

# AI 事故資料庫與案例研究

AI 事故資料庫記錄 AI 系統造成傷害或失效的真實案例，讓設計者、研究者與監管機關能從已經發生的失敗中學習。主要工具包括：描述事故的共通詞彙、AI 事故資料庫與 OECD AI 事件監測器等公開蒐集的資料，以及部分法律現已對開發者施加的通報義務。

!!! info "屬於法律、政策與治理"
    本頁隸屬於[法律、政策與治理](index.md)。它詳細說明一種治理工具；上層頁面則涵蓋更廣的法律情勢。

## 概述

成熟的安全領域都會保存失敗的紀錄，例如航空業的事故調查報告。McGregor（2020）對 AI 作了同樣的比較：智慧系統會在現實世界造成傷害，卻沒有對其失敗的集體記憶，因此企業會在設計、開發與部署中一再犯下相同錯誤。AI 事故資料庫的建立，就是為了建立這種記憶，作為一個公開、可搜尋的已通報失敗紀錄。

基準測試檢驗的是建構者預先設想的條件；事故則顯示系統在面對真實使用者時發生了什麼。關於事前的一面，請見[危險能力評估](../safety-alignment/dangerous-capability-evals.md)。

## 關鍵概念

- **AI 事故（AI incident）**：已經發生、且 AI 系統扮演某種角色的傷害。OECD（2024）將其與 **AI 危害（AI hazard）** 區分開來，後者指尚未造成傷害、但有可能發生的風險。
- **分類體系（taxonomy）**：描述事故的一組類別，例如傷害類型、產業領域、系統種類或可能的成因。
- **認知不確定性（epistemic uncertainty）**：對某一事故已知的內容，與完整分類所需資訊之間的落差，例如其真正成因或系統的內部運作。Paeth 等人（2024）主張，這種不確定性在事故通報中無法避免，必須加以管理。

## 運作方式

事故資料會經過一連串步驟，每一步都會篩選最後留存的紀錄。

```mermaid
flowchart LR
    A[已部署系統中的失敗] --> B[由受害者、媒體或營運者通報]
    B --> C[以分類體系歸類]
    C --> D[寫入事故資料庫]
    D --> E[模式分析]
    E --> F[設計修正、稽核與規範]
```

1. **發生與通報。** 事故只有在有人注意到並通報時才會進入紀錄，因此安靜發生的傷害會被低估。
2. **歸類。** 編審者套用分類體系。Paeth 等人（2024）將兩套獨立的分類體系套用於相同事故，並指出結構性的模糊之處，例如成因不明或嚴重程度難以判定，使歸類變得困難。
3. **分析。** 計數與模式是主要產出。Wei 與 Zhou（2022）以內容分析檢視 AI 事故資料庫，發現有 13 個應用領域出現不道德的 AI 使用，其中以服務型機器人、語言與視覺模型，以及自動駕駛最為突出。

因此，資料庫是已通報失敗的樣本，而不是 AI 失敗頻率的測量。[^1]

## 關鍵方法

下表比較四種整理 AI 失敗的取徑。它們回答的問題不同。

| 取徑 | 記錄內容 | 主要優點 | 主要限制 |
|---|---|---|---|
| AI 事故資料庫（McGregor，2020） | 公開的真實 AI 失敗報告，可依面向與全文搜尋 | 涵蓋真實案例廣泛，且開放取用 | 依賴通報與媒體關注；歸類本身不確定 |
| OECD AI 事件監測器（OECD，2024） | 來自公開來源的事件，採用 OECD 對事件與危害的定義 | 定義共通，可跨司法管轄區使用 | 各司法管轄區自行決定納入範圍，因此數量不能直接比較 |
| 社會技術危害分類體系（Shelby 等人，2022） | 演算法系統的危害類型，源自 172 篇論文的範疇性回顧 | 協助實務工作者在危害發生前預先辨識 | 來自研究文獻，而非實際觀察到的案例 |
| 語言模型風險分類體系（Weidinger 等人，2021） | 大型語言模型在六個領域的 21 項風險 | 系統化地描繪語言模型可能造成傷害的方式 | 聚焦於單一類模型，且寫於許多後續部署失敗出現之前 |

另一項規模更大的工作，AI 風險儲存庫（Slattery 等人，2024），發現在其所收錄的 1,725 項風險中，人為決策造成的風險幾乎與 AI 系統本身造成的一樣多（分別為 38% 與 42%）。

## 與其他主題的連結

- **評估與安全。** 部署前的測試試圖預見失敗，事故則顯示哪些失敗被遺漏。請見[安全與對齊](../safety-alignment/index.md)。
- **偏見。** 許多已記錄的失敗屬於分組拆解後才看得出的錯誤，整體準確率掩蓋了群體之間的巨大落差。請見[演算法偏見案例研究](../ethics/bias-case-studies.md)。
- **回饋。** 有些失敗會擴大，因為系統自身的輸出會改變它所學習的資料。請見[預測性警務中的失控回饋迴圈](../surveillance/runaway-feedback-loops/index.md)。
- **腦與心智。** 事故集合可能因心理因素而產生誤導：引人注目、廣受報導的失敗，比常見而安靜的失敗更容易被想起，這正是[啟發法與偏誤](../../brain-mind/cognitive-science/heuristics-and-biases/index.md)所描述的判斷偏誤。把資料庫當成頻率統計來讀，正是落入這個陷阱。

## 應用

- **政府的監測。** OECD AI 事件監測器依共通定義蒐集公開報導。
- **法律中的通報義務。** Anderljung 等人（2023）主張，前沿模型開發者應承擔註冊與通報義務，並在部署後監測並回應關於能力與用途的新資訊。歐盟 AI 法對具系統性風險的通用模型設定事故通報義務，加州 SB 53（2025）則要求前沿開發者通報安全事故。目前的時程與細節請見[上層頁面](index.md)。

### 重大失敗的教訓

- **集中。** 具有實體後果的系統，例如自動駕駛車輛，在紀錄中經常出現。
- **回饋迴圈。** Ensign 等人（2017）顯示，預測性警務系統會不斷把警力派回同一地區，因為系統自身的部署產生了它所學習的資料。通報的事故只能減輕這種效應；要消除它，必須改變系統的輸入。
- **未經驗證的輸出。** Dahl 等人（2024）發現，語言模型在針對法院案件的具體、可核對問題上經常出現幻覺。[^2]這正是那些被通報、引用了不存在判決的法院文件背後的失敗（請見[法律中的 AI](../../applications/law/index.md)）。對專業使用而言，教訓是把每一條引用都對照原始來源檢查。
- **隱藏的差異。** 許多案例是由外部人員發現的，他們在整體準確率看似可接受之後，才依群體拆解結果。

## 開放問題

- **涵蓋範圍。** 哪些傷害會被通報，又由誰通報？以新聞報導為基礎的資料庫，會高估受關注的失敗。
- **定義。** OECD 對事件與危害的區分，能否在不同國家與產業間以相同方式應用？
- **不確定的事實。** 當事故的成因未知或有爭議時，紀錄應如何撰寫？Paeth 等人（2024）提出了緩解方法，但尚未形成定論的實務。
- **門檻。** 哪種嚴重程度應觸發通報義務，又由誰決定？這些問題與[運算治理與出口管制](compute-governance.md)中關於運算門檻的辯論相連。
- **私下的失敗。** 嚴重的失敗往往留在企業內部。通報要如何觸及它們，又不洩露商業機密？

[^1]: McGregor（2020）報告，在預印本發表時已存檔超過 1,000 份事故報告。此後資料庫持續成長，引用數字前請查核其最新總數。
[^2]: Dahl 等人（2024）的比率適用於關於聯邦法院案件、可核對的具體問題，且在不同模型之間差異很大。不應將其視為法律工作的一般失敗率。

## 參考資料

### 開創性論文

- McGregor, S. (2020). *Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database*. arXiv preprint. https://arxiv.org/abs/2011.08512 — 介紹 AI 事故資料庫，作為真實 AI 失敗的共同紀錄。
- Weidinger, L. et al. (2021). *Ethical and social risks of harm from Language Models*. arXiv preprint. https://arxiv.org/abs/2112.04359 — 將大型語言模型的 21 項風險歸納於六個領域，並附上緩解方法。
- Shelby, R. et al. (2022). *Sociotechnical Harms of Algorithmic Systems: Scoping a Taxonomy for Harm Reduction*. arXiv preprint. https://arxiv.org/abs/2210.05791 — 對 172 篇論文進行範疇性回顧，產出五個主題的危害分類體系。
- Ensign, D. et al. (2017). *Runaway Feedback Loops in Predictive Policing*. arXiv preprint. https://arxiv.org/abs/1706.09847 — 說明預測性警務如何陷入回饋迴圈，以及如何阻止。
- Anderljung, M. et al. (2023). *Frontier AI Regulation: Managing Emerging Risks to Public Safety*. arXiv preprint. https://arxiv.org/abs/2307.03718 — 提出針對前沿 AI 開發者的註冊、通報與監測義務。

### 文章與官方文件

- OECD (2024). *Defining AI incidents and related terms*. OECD Artificial Intelligence Papers, No. 16. https://doi.org/10.1787/d1a8d965-en — 將 AI 事故定義為已發生的傷害，將 AI 危害定義為可能發生的傷害。
- Slattery, P. et al. (2024). *The AI risk repository: A meta-review, database, and taxonomy of risks from artificial intelligence*. arXiv preprint. https://arxiv.org/abs/2408.12622 — 將 74 個框架中的 1,725 項風險整理為單一分類體系。
- Paeth, K. et al. (2024). *Lessons for Editors of AI Incidents from the AI Incident Database*. arXiv preprint. https://arxiv.org/abs/2409.16425 — 檢視 750 件以上的事故，找出使事故索引變得複雜的模糊之處。
- Wei, M. & Zhou, Z. (2022). *AI Ethics Issues in Real World: Evidence from AI Incident Database*. arXiv preprint. https://arxiv.org/abs/2206.07635 — 對該資料庫進行內容分析，找出 13 個應用領域與八種倫理問題形式。
- Dahl, M. et al. (2024). *Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models*. arXiv preprint. https://arxiv.org/abs/2401.01301 — 以可核對的法律案件問題，衡量大型語言模型的法律幻覺。
