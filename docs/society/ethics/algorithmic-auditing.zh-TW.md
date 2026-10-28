---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - society/human-ai-interaction
tags:
  - auditing
  - documentation
  - accountability
  - regulation
aliases:
  - 演算法稽核
  - 演算法審計
  - 影響評估
  - Algorithmic auditing
  - Model cards
  - Datasheets
---

# 演算法稽核與影響評估

演算法稽核是依據定義好的標準（例如各群體間的準確率、安全性或法律遵循）對 AI 系統，或對開發與部署該系統的組織，進行的系統性評估。影響評估則是相關的做法，在部署之前或過程中預先評估系統會影響哪些人、如何影響。兩者都仰賴文件紀錄，因為稽核者只能測試被描述的內容，也只能檢查能取得的資料。本頁涵蓋主要的稽核類型、支持稽核的文件工具，以及目前要求部分稽核的法規。

## 概述

在基準測試上表現良好的模型，仍可能對特定使用者、在特定情境下，或被用於新的用途時失敗。稽核試圖回答：系統是否如提供者所述般運作、對誰運作，以及可能出什麼問題。影響評估則較早提出同樣的問題，視野也較寬，包括受影響的人與使用輸出的機構。

## 核心概念

- **內部稽核**：由開發組織進行的評估，通常由與產品團隊分開的人員執行。
- **外部稽核**：由組織外部的一方進行的評估，可以是監管機關、研究人員或經認可的機構。外部稽核取決於稽核者獲得的存取權限。
- **黑箱與白箱存取**：黑箱稽核只測試輸入與輸出；白箱稽核則可檢視資料、程式碼或權重。
- **模型卡（model card）**：描述模型預定用途、各群體評估結果與限制的標準化文件。
- **資料表（datasheet）**：描述資料集的蒐集方式、組成、用途與已知缺口的文件。
- **影響評估**：對系統可能帶給受影響人群的效益與傷害所做的結構化審查。

## 運作方式

### 稽核階段

Raji 等人（2020）提出一套內部演算法稽核框架，支援 AI 系統從開發到部署的端到端流程，並套用於組織內部的整個開發生命週期。其目標是在部署前找出危害，並將部署後出現的問題追溯到其來源。實務中的稽核在範圍與嚴謹程度上差異極大。

### 文件工具

- **模型卡。** Mitchell 等人（2019）提出模型卡：附隨於訓練好模型的簡短文件，提供跨文化與人口群體等條件下的基準評估。目的是讓未參與訓練的人也能看見模型的預定用途與限制。
- **資料集資料表。** Gebru 等人（2021）主張每個資料集都應附上資料表，記錄其建立動機、組成、蒐集過程與建議用途。

這兩種文件都是自我申報的。它們使稽核成為可能，但無法取代稽核。

### 影響評估

影響評估會辨識受影響的群體、系統所影響的決策、可能的失敗模式，以及計畫中的緩解措施。部分法規框架要求此類評估，其程序因法域而異。

## 法規背景

歐盟《人工智慧法》（Artificial Intelligence Act），即 Regulation (EU) 2024/1689，為聯盟內的 AI 制定統一規則。它對被歸類為高風險的系統課以義務。分類與符合性規則見該法條文，應直接閱讀條文，其解釋與執法指引仍在持續發展。

其他法域採取不同路徑，例如依賴各行業監管機關、公部門採購規則或自願性標準。法律與政策見[法律、政策與治理](../governance/index.md)。

## 稽核大型語言模型

稽核通用模型比稽核狹義的分類器困難，因為任務與使用者的範圍是開放的。常見做法包括跨群體的基準評估、對抗性測試或紅隊測試以找出有害輸出，以及記錄訓練資料與安全措施。Metaxa 等人（2021）綜述從外部由外而內稽核演算法系統的方法，這也是黑箱存取所帶來的處境。

## 關聯

稽核是實踐[公平性定義](fairness-definitions.md)中公平性準則的方式，也是[偏見案例研究](bias-case-studies.md)中的失敗如何被發現與查證的途徑。稽核的人的一面，包括人們如何使用被稽核系統的輸出，見[人機互動](../human-ai-interaction/index.md)。

## 應用

- 在部署前測試招募、信貸與醫療工具。
- 公部門採購，要求機關在採用系統前取得文件與評估結果。
- 透過受控帳號對平台推薦與搜尋系統進行研究性稽核。

## 未解問題

- **存取權限。** 外部稽核者常需要開發者不願分享的資料、程式碼或模型存取權。如何安全地提供這些存取仍未解決。
- **標準。** 若缺乏共通的指標與程序，對同一系統的兩次稽核可能得出相反結論。
- **失敗時的責任。** 稽核通過但系統日後傷害了某人時，責任如何分配尚未定論。
- **通用模型的稽核。** 要在其所有用途上測試開放式系統目前並不可行，這類系統的稽核範圍仍在界定中。

## 參考文獻

### 開創性論文

- Raji, I. D. et al. (2020). Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing. *Proceedings of FAT\* 2020*. https://doi.org/10.1145/3351095.3372873 — 提出套用於整個開發生命週期的內部稽核框架。
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. *Proceedings of FAT\* 2019*. https://doi.org/10.1145/3287560.3287596 — 提出模型卡：附帶跨文化與人口群體等條件基準評估的文件。
- Gebru, T. et al. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92. https://doi.org/10.1145/3458723 — 提出資料表，記錄每個資料集的建立動機、組成、蒐集過程與建議用途。

### 綜述與教科書

- Metaxa, D. et al. (2021). Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. *Foundations and Trends in Human–Computer Interaction*, 14(4), 272–344. https://doi.org/10.1561/1100000083 — 綜述從外部由外而內稽核演算法系統的方法。
- Regulation (EU) 2024/1689 of the European Parliament and of the Council (Artificial Intelligence Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — AI 法義務（包括高風險系統）的主要法律文本。
