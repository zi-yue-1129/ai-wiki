---
translation_reviewed: 2026-10-28
---

# 歸結（Robinson 1965）

歸結是一條作用於子句的推論規則，由 John Alan Robinson 於 1965 年提出。證明器把待證猜想的否定加入一組子句，並反覆合併子句，直到推出矛盾為止。它是自動一階定理證明的經典方法。它也是上層頁面[自動定理證明與形式化數學](../index.zh-TW.md)所描述的三個代表性方法之一。

## 概述

數學陳述可以寫成許多不同的邏輯形式。歸結作用於一種標準形式，也就是子句，並且只使用一條推論規則，因此程式不必理解陳述的含義就能套用它。Robinson 的貢獻在於把這條規則與合一結合起來，使一般的模式能在搜尋過程中配對到特定的項。

Davis 與 Putnam 早先建立了一個以電腦測試有效性的程序，它對公式的實例使用歸結。後來的工作以分裂取代了其中大部分的歸結，這一改變導向了現代的 SAT 求解器。[^1]

## 核心概念

- **文字**：原子公式或其否定，例如 $P(x)$ 或 $\neg P(f(y))$。
- **子句**：文字的析取。一組子句代表一個合取，若沒有任何指派能同時滿足其中所有子句，該集合即為矛盾。
- **合一子**：使兩個項相同的代換 $\sigma$。最一般合一子（記為 mgu）是施加限制最少的那一個。
- **歸結式**：由兩個含有互補文字的子句，在套用合一子之後所產生的子句。
- **空子句**：不含任何文字的子句，它永遠為假。推出空子句即表示該子句集合不可滿足。

## 運作方式

歸結規則取兩個子句，其中分別含有文字 $L$ 與 $\neg M$，且其原子可以合一，並產生它們的歸結式：

$$
\frac{C \lor L \qquad D \lor \neg M}{(C \lor D)\sigma}, \qquad \sigma = \mathrm{mgu}(L, M).
$$

要證明猜想 $\varphi$，證明器需檢查：$\neg\varphi$ 的子句集合連同背景公理是否不可滿足。標準程序是一個飽和迴圈：

1. 將公理與待證猜想的否定轉換為子句標準形式，並以 Skolem 化去除量詞。
2. 選出一對含有互補文字、且可以合一的子句。
3. 把它們的歸結式加入集合，除非它明顯是冗餘的。
4. 若出現空子句，即停止：猜想已被證明。
5. 若不能再產生新的子句，則該集合可滿足，猜想不是有效的。否則在資源上限內，從第 2 步重複。

細化策略用來限制組合爆炸。支持集策略要求每一步的父子句中，至少一個源自待證猜想的否定；排序限制則限定哪些文字可以被歸結。反駁完備性，即不可滿足的集合總能推出空子句的保證，在規則的標準形式中仍然保留。

## 結果

Robinson 1965 年的論文以證明而非基準測試，確立了該規則及其完備性。因此它的意義是理論性的：它為自動一階證明搜尋提供了既可靠又完備的基礎。Davis、Logemann 與 Loveland 1962 年的論文討論了其程序的程式設計、試運行與可能的改進。他們的程序以分裂取代了歸結，並成為[CDCL 專頁](../cdcl-sat/index.zh-TW.md)所討論求解器的祖先。各程式的具體表現數字載於這些論文中，本頁不再重述。

## 限制

- **組合成長。** 不加限制的歸結會產生大量冗餘子句。每一步都可能使集合變大，因此記憶體與時間迅速成長。
- **不終止。** 對一階邏輯而言，飽和迴圈在可滿足的集合上可能永遠不停。這個問題只是半可判定的，因此證明器有時無法給出答案。
- **沒有內建算術。** 數字與其他理論必須編碼為子句，效率低。

## 開放問題

- **應保留哪些子句？** 現代一階證明器在子句選擇上仍依賴啟發式方法。學習式選擇已有研究：Kaliszyk 等人以強化學習引導連接式證明器的證明搜尋。[^2]
- **與 SAT 和 SMT 結合。** 問題中的基礎（ground）部分，通常由 SAT 或 SMT 求解器處理得更好。如何在兩者之間分配工作，是一個沒有固定答案的工程問題。
- **人類的證明風格。** 歸結證明很少能以數學的方式被人讀懂。機器證明能否轉譯為人類式的論證，仍是開放問題。

[^1]: Davis 與 Putnam（1960），以及 Davis、Logemann 與 Loveland（1962），見上方參考文獻。
[^2]: Kaliszyk 等人（2018），見上方參考文獻。

## 參考文獻

### 開創性論文

- Robinson, J. A. (1965). *A Machine-Oriented Logic Based on the Resolution Principle*. Journal of the ACM. https://doi.org/10.1145/321250.321253 — 提出含合一的歸結原理，並證明其反駁完備性。
- Davis, M. & Putnam, H. (1960). *A Computing Procedure for Quantification Theory*. Journal of the ACM. https://doi.org/10.1145/321033.321034 — 提出早期的電腦程序，用來測試邏輯中的有效性。
- Davis, M., Logemann, G. & Loveland, D. (1962). *A machine program for theorem-proving*. Communications of the ACM. https://doi.org/10.1145/368273.368557 — 描述以分裂取代後來證明器中大部分歸結的程序。

### 綜述與教科書

- Marques-Silva, J., Lynce, I. & Malik, S. (2021). *Conflict-Driven Clause Learning SAT Solvers*, chapter 4 of the *Handbook of Satisfiability*. IOS Press. https://doi.org/10.3233/FAIA200987 — 追溯從 DPLL 程序發展而來的求解器脈絡。
- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — 一篇綜述，將基於歸結的方法與後來的證明方法置於形式推理的脈絡中。

### 文章與文件

- Kaliszyk, C., Urban, J., Michalewski, H. & Olšák, M. (2018). *Reinforcement Learning of Theorem Proving*. arXiv. https://arxiv.org/abs/1805.07563 — 以強化學習引導連接式證明器的證明搜尋。
- Fikes, R. E. & Nilsson, N. J. (1971). *STRIPS: A new approach to the application of theorem proving to problem solving*. Artificial Intelligence. https://doi.org/10.1016/0004-3702(71)90010-5 — 展示定理證明如何被應用於規劃，是 STRIPS 形式化的起源。
