---
translation_reviewed: 2026-10-28
---

# MetaGPT

MetaGPT（Hong 等人，2023）是一個多代理人框架，其中的語言模型代理人各自承擔固定的專業角色，例如產品經理、架構師、專案經理與工程師，並依照標準作業程序所規範的裝配線，傳遞結構化的文件。它是[多代理人編排](../index.md)概述頁中以角色為基礎的方法。

## 概述

沒有結構的連續模型呼叫，會把每一步的錯誤傳給下一步，最後的輸出也可能前後矛盾。Hong 等人認為，人類組織能避免這個問題，是因為把工作分給專家，並規定其產出如何交接。MetaGPT 採用了相同的安排：角色告訴代理人要產出什麼，程序則告訴它會收到什麼、必須檢查什麼。

先前以角色為基礎的系統，例如 CAMEL（Li 等人，2023）與 ChatDev（Qian 等人，2023），讓代理人自由對話。MetaGPT 則以文件與檢查點取代自由對話。

## 關鍵概念

- **角色（role）**：單一代理人的設定檔、目標與允許產出的內容集合。產品經理撰寫需求，架構師撰寫設計，工程師撰寫程式碼。
- **標準作業程序（SOP）**：角色所遵循、以提示寫成的步驟與文件序列。作者從人類的軟體實務中編寫 SOP。
- **裝配線（assembly line）**：每個角色的產出即是下一個角色的輸入的流程。
- **結構化訊息（structured message）**：有明確型別的文件，例如需求檔案或介面說明，用來取代自由格式的聊天。

## 運作方式

軟體任務的流程大致如下：

1. 產品經理代理人把使用者的請求轉為需求文件。
2. 架構師代理人把需求轉為系統設計，包含資料結構與介面。
3. 專案經理代理人把設計拆成任務並加以指派。
4. 工程師代理人為其任務撰寫程式檔案。
5. 每一步都可以把輸入與先前的文件對照檢查，而執行步驟可以實際運行程式碼，並把錯誤回饋。

作者把這個流程描述為元程式設計（meta-programming）框架：SOP 以提示序列寫成，因此工作流程本身就是代理人所執行的程式。

## 關鍵方法

與讓對等代理人互相辯論的[多代理人辯論](../debate/index.md)不同，MetaGPT 預先固定每個代理人的角色。若要由單一規劃者委派任務，請見 [HuggingGPT](../hugginggpt/index.md)。

## 結果

在作者使用的 SoftwareDev 基準上，MetaGPT 與 ChatDev 進行比較。論文表 1 顯示，完整的 MetaGPT 系統相對於 ChatDev 的表現如下。[^1]

- **可執行性**（以 1 至 4 分評分）：3.75 對 ChatDev 的 2.25。
- **程式碼總行數**：251.4 對 77.5。
- **人工修訂成本**：0.83 對 2.5，數值越低越好。
- **每行程式碼的 token 數**：124.3 對 248.9。

MetaGPT 的總 token 用量也較多，為 31,255，ChatDev 為 19,292，因此它的效益並非沒有代價。在沒有可執行回饋迴圈的版本中，分數為 3.67，因此大部分的效益來自角色與文件。

## 限制

- **成本。** 文件、審查與重試都會倍增 token 用量。每行程式碼的效率可能提升，但總成本仍會上升。
- **固定的工作流程。** SOP 由人預先撰寫，因此系統的彈性受限於它所編碼的程序。沒有已知工作流程的任務，適用性較差。
- **評估範圍狹窄。** 主要結果來自軟體開發。論文並未顯示相同的效益是否適用於研究、寫作或分析。
- **失敗模式仍然存在。** 一項對多個多代理人框架失敗情況的研究發現，許多失敗來自規格不清與代理人之間的錯位；結構化文件能減少這些問題，但無法完全消除（Cemri 等人，2025）。[^2]

## 開放問題

- **角色設計。** 角色、數量以及職責的劃分目前都由人工決定，而測試這些設計的方法仍不成熟。
- **通用性。** 由 SOP 驅動的流程能否轉移到結構不確定或會改變的任務，尚不清楚。

## 相關連結

把工作分成角色，類似於古典認知架構中的專門模組。在 [ACT-R](../../../../brain-mind/cognitive-architectures/act-r/index.md) 中，視覺、動作控制與記憶等獨立模組，透過有限容量的緩衝區彼此溝通；以角色為基礎的模式，可以看作是代理人層級上這種設計的鬆散類比。更完整的介紹請見[認知架構](../../../../brain-mind/cognitive-architectures/index.md)。

## 參考文獻

### 奠基性論文

- Hong, S. et al. (2023). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. arXiv. https://arxiv.org/abs/2308.00352 — 提出以角色為基礎的代理人，遵循標準作業程序，並沿裝配線傳遞結構化文件。
- Li, G. et al. (2023). *CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society*. arXiv. https://arxiv.org/abs/2303.17760 — 以起始提示引導的角色扮演代理人，用來研究彼此溝通的代理人之間的合作。
- Qian, C. et al. (2023). *ChatDev: Communicative Agents for Software Development*. arXiv. https://arxiv.org/abs/2307.07924 — 一個由代理人組成、以聊天進行設計、編碼與測試的軟體公司，是 MetaGPT 比較的主要基準。

### 綜述與教科書

- Guo, T. et al. (2024). *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. arXiv. https://arxiv.org/abs/2402.01680 — 綜述以 LLM 為基礎的多代理人系統，包括代理人設定檔與溝通方式的設計。

### 文章與文件

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv. https://arxiv.org/abs/2503.13657 — 對多代理人系統 14 種失敗模式的分類，分為系統設計、代理人之間的錯位與任務驗證三類。
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv. https://arxiv.org/abs/2308.08155 — 開源框架，用來建構以對話完成任務的代理人，是角色式設計常用的平台。

[^1]: Hong et al. (2023)，表 1（SoftwareDev 的統計分析），https://arxiv.org/abs/2308.00352 — ChatDev 與 MetaGPT 的可執行性、程式碼規模、修訂成本、token 用量以及每行程式碼的 token 數。
[^2]: Cemri et al. (2025)，分類摘要，https://arxiv.org/abs/2503.13657 — 三類失敗的來源，作為此限制的依據。
