---
translation_reviewed: 2026-10-28
---

# 衝突驅動子句學習（GRASP 1999）

衝突驅動子句學習（CDCL）是現代 SAT 求解器的核心搜尋方法。它擴充了較早的 DPLL 程序：把每個死路都轉化為一個新子句，使同樣的錯誤不會重複發生。加上理論求解器後，同一架構（DPLL(T)）也成為 SMT 求解器的基礎。它是上層頁面[自動定理證明與形式化數學](../index.zh-TW.md)所列三個代表性方法之一。

## 概述

SAT 問題詢問一個合取範式的命題公式是否可滿足。這個問題是 NP 完全的，但實用的求解器能處理許多來自硬體驗證與規劃的結構化實例。

DPLL 於 1962 年提出，它在部分指派上搜尋，並在某個子句被違反時回溯。它的弱點是可能在許多分支中重新發現同一個衝突。Marques-Silva 與 Sakallah 的 GRASP 加上了兩個想法：分析每一次衝突，找出應負責的決策，並把其原因儲存為新子句，然後回到該子句開始發揮作用的層級。[^1]

## 核心概念

- **決策與傳播**：求解器為某個變數指定一個值，稱為決策，接著以單元傳播把所有被子句強制的文字設為真，這些子句的其他文字皆為假。
- **決策層級**：目前為止所做的決策數。被傳播的指派屬於造成它的那個決策所在的層級。
- **衝突**：在目前指派下，所有文字皆為假的子句。
- **第一個唯一蘊涵點（1UIP）**：蘊涵圖中的一個點，在該點上，衝突的成因可以由當前決策層級上的單一文字來捕捉。求解器通常在此點學習子句。
- **非時序回跳**：學習之後，求解器回到學得子句中第二高的決策層級，而不是只退回上一個決策。
- **重新啟動**：捨棄目前的指派重新搜尋，並保留已學得的子句。

## 運作方式

CDCL 求解器的核心迴圈如下：

1. 執行單元傳播。若出現衝突，跳到第 3 步。
2. 若所有變數都已指派，回報公式可滿足。否則以啟發式選出一個未指派的變數，對它做決策，然後回到第 1 步。
3. 若決策層級為零，公式不可滿足。否則沿蘊涵圖回溯分析衝突，直到第一個唯一蘊涵點，並推導出學得的子句。
4. 把學得的子句加入公式，回跳到該子句指定的層級，並在那裡指派其唯一的文字。回到第 1 步。
5. 偶爾重新啟動，並刪除已證明無用的學得子句。

學得的子句本身是公式的推論，並可沿蘊涵圖以一連串歸結步驟推導出來。[^2] 因此，CDCL 可以理解為由搜尋所引導的歸結。[歸結專頁](../resolution/index.zh-TW.md)給出了該規則。

**SMT。** SMT 求解器把公式中的每個原子抽象為一個命題變數。理論求解器（例如線性算術的求解器）檢查所選的文字是否一致，不一致時回傳一個衝突子句。Nieuwenhuis、Oliveras 與 Tinelli 為這種惰性方法給出了一個抽象的 DPLL 框架。[^3] Z3 是一個廣泛使用的 SMT 求解器。[^4]

## 結果

最強的近期證據來自 Heule、Kullmann 與 Marek，他們以 cube-and-conquer（一種結合前瞻與 CDCL 求解器的混合方法）解決了布林畢氏三元組問題。這次運算使用了 800 個核心的叢集，耗時約兩天，並產生了經過驗證的證明。[^5] GRASP 自己的實驗記錄於其論文中；本頁不重複其數字。

## 限制

- **最壞情況。** 除非 P 等於 NP，否則任何求解器在某些實例族上都需要指數時間。學得的子句也會不斷累積，必須加以管理。
- **依賴啟發式。** 效能取決於決策啟發式、重新啟動與子句刪除，而且良好的設定會因實例類別而異。
- **證書。** 不可滿足性的證明可能非常龐大，畢氏三元組的結果即是例證。
- **理論的限制。** SMT 求解的能力受限於其理論求解器，而量化公式需要不同的機制。

## 開放問題

- **學習式啟發式。** 學習模型能否在工業實例上勝過調校過的分支啟發式，是一個開放問題。
- **擴展 cube-and-conquer。** 把困難問題切分為許多子問題，在某些實例上有效。如何一般性地選出好的切分方式，仍是開放的。
- **信任求解器。** 經認證的證明（例如 DRAT 證明）能把信任轉移到一個小型檢查器上。

[^1]: Marques-Silva 與 Sakallah（1999），見上方參考文獻。
[^2]: Marques-Silva、Lynce 與 Malik（2021），見上方參考文獻。
[^3]: Nieuwenhuis、Oliveras 與 Tinelli（2006），見上方參考文獻。
[^4]: de Moura 與 Bjørner（2008），見上方參考文獻。
[^5]: Heule、Kullmann 與 Marek（2016），見上方參考文獻。叢集規模與運算時間以其摘要所述為準。

## 參考文獻

### 開創性論文

- Marques-Silva, J. P. & Sakallah, K. A. (1999). *GRASP: a search algorithm for propositional satisfiability*. IEEE Transactions on Computers. https://doi.org/10.1109/12.769433 — 引入子句學習與非時序回溯，是 CDCL 的核心。
- Davis, M., Logemann, G. & Loveland, D. (1962). *A machine program for theorem-proving*. Communications of the ACM. https://doi.org/10.1145/368273.368557 — 描述 CDCL 所擴充的分裂程序。
- Nieuwenhuis, R., Oliveras, A. & Tinelli, C. (2006). *Solving SAT and SAT Modulo Theories*. Journal of the ACM. https://doi.org/10.1145/1217856.1217859 — 給出抽象的 DPLL 框架，並將其延伸到 SMT。
- de Moura, L. & Bjørner, N. (2008). *Z3: An Efficient SMT Solver*. TACAS 2008. https://doi.org/10.1007/978-3-540-78800-3_24 — 提出 Z3，一個為效率設計、在驗證中被廣泛使用的 SMT 求解器。

### 綜述與教科書

- Marques-Silva, J., Lynce, I. & Malik, S. (2021). *Conflict-Driven Clause Learning SAT Solvers*, chapter 4 of the *Handbook of Satisfiability*. IOS Press. https://doi.org/10.3233/FAIA200987 — 《可滿足性手冊》中的一章，說明 CDCL 求解器如何學習子句並管理其搜尋。

### 文章與文件

- Heule, M. J. H., Kullmann, O. & Marek, V. W. (2016). *Solving and Verifying the boolean Pythagorean Triples problem via Cube-and-Conquer*. arXiv. https://arxiv.org/abs/1605.00723 — 描述一種在大型叢集上運行的混合式 SAT 方法，解決了一個開放的拉姆齊理論問題並附上經驗證的證明。
