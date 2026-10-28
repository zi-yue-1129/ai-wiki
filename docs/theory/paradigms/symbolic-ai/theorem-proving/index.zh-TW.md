---
translation_reviewed: 2026-10-28
---

# 自動定理證明與形式數學

自動定理證明建立能判定一個邏輯陳述是否可由一組公理推出的程式，並可產生可檢查的證明。形式數學則更進一步，以精確的語言書寫數學，使電腦能逐步驗證。本頁是[符號 AI、搜尋與規劃](../index.md)的一部分。

## 概述

定理證明器在形式系統中判定或搜尋證明。自動證明器在沒有人工指引的情況下處理固定的問題，互動式證明器則讓人引導證明，由電腦檢查每一步。兩者都用於數學、軟體與硬體驗證，也可作為 AI 系統可檢驗推理的來源。

## 關鍵概念

- **證明**：有限的步驟序列，每一步都由公理或推理規則證明其合理性，並導出該陳述。
- **反駁**：透過證明該陳述的否定加上公理不可滿足來證明陳述。多數自動證明器採用此方式。
- **可滿足性（SAT）**：判定一個命題公式是否存在使其為真的指派。許多證明問題都可化為 SAT。
- **證明助手**：互動式系統，檢查由人或程式寫成的形式證明，並保存已驗證結果的函式庫。

## 運作方式

最常用的是兩大類。基於歸結的證明器透過反覆結合子句來推導新子句，以反駁一組子句，直到出現空子句為止。[歸結](resolution.md)是此類方法的基本推理規則（Robinson，1965）。對於命題問題，[DPLL](dpll.md)程序透過搜尋、單位傳播與回溯來判定可滿足性（Davis、Logemann 與 Loveland，1962）。Lean 與 Coq 等證明助手以依賴型別論或相關邏輯來表述陳述，並以一個小型、受信任的核心檢查證明（de Moura 等人，2015）。

## 主要方法

- [歸結](resolution.md)：許多一階證明器背後的推理規則。
- [DPLL](dpll.md)：SAT 的回溯搜尋，是現代 SAT 求解器的核心。

Lean 等證明助手在此僅作為系統提及，不以方法的形式介紹。

## 與其他頁面的連結

- [搜尋演算法](../search/index.md)說明證明器所用的證明狀態搜尋。
- [神經符號 AI](../neuro-symbolic/index.md)把邏輯推理與學習模型結合，包括以學得的元件引導證明搜尋的嘗試。
- [知識圖譜與知識表示](../knowledge-graphs/index.md)與本頁共用陳述事實所用的邏輯形式。

## 應用

- **軟體與硬體驗證**：證明程式或電路符合其規格。
- **形式數學**：在證明助手中驗證重要定理。Hales 等人（2017）報告了開普勒猜想的完整形式證明。
- **AI 推理**：為邏輯推論提供可檢查的紀錄，並以已驗證的任務測試學習系統。

## 開放問題

- 自動證明器對於需要長推理鏈或大量引理函式庫的問題仍然吃力。
- 以學得的模型引導證明搜尋很有希望，但學得的引導必須經由證明器檢查，因此能得到的好處有限。
- 把大範圍的數學形式化需要持續投入，從非形式文字到形式文字的翻譯成本仍然很高。

## 參考文獻

### 奠基性論文

- Robinson, J. A. (1965). A machine-oriented logic based on the resolution principle. *Journal of the ACM* 12(1), 23–41. https://doi.org/10.1145/321250.321253 — 提出含合一的歸結推理規則。
- Davis, M., Logemann, G. & Loveland, D. (1962). A machine program for theorem-proving. *Communications of the ACM* 5(7), 394–397. https://doi.org/10.1145/368273.368557 — 給出帶回溯的程序，即 DPLL 演算法。
- Davis, M. & Putnam, H. (1960). A computing procedure for quantification theory. *Journal of the ACM* 7(3), 201–215. https://doi.org/10.1145/321033.321034 — 提出 DPLL 所改進的早期程序。
- de Moura, L. et al. (2015). The Lean theorem prover (system description). In *Automated Deduction — CADE-25*, Lecture Notes in Computer Science, 378–388. https://doi.org/10.1007/978-3-319-21401-6_26 — 描述 Lean 證明助手。

### 綜述與教科書

- Hales, T. et al. (2017). A formal proof of the Kepler conjecture. *Forum of Mathematics, Pi* 5. https://doi.org/10.1017/fmp.2017.1 — 報告一個重要定理在證明助手中的完整形式證明。
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — 歸結與邏輯推論的教科書背景。
