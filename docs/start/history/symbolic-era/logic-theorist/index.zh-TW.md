---
translation_reviewed: 2026-10-28
---

# Logic Theorist 與通用問題求解器

Logic Theorist 由 Allen Newell、J. C. Shaw 與 Herbert Simon 於 1956 年撰寫，它以啟發式搜尋來證明符號邏輯的定理。它的後繼者通用問題求解器（General Problem Solver）則把類似的目標導向搜尋思路套用到一般問題上。兩者都是[符號時代](../index.md)以及更廣泛的[符號 AI](../../../../theory/paradigms/symbolic-ai/index.md)傳統中的里程碑方法。

## 概述

到了 1950 年代中期，電腦能操作符號這件事已不新鮮，但很少有程式做出接近推理的事情。Newell 與 Simon 想要一個步驟可以被讀成解題過程的程式，他們選擇邏輯，是因為證明是一個毫不含糊的目標。Logic Theorist 以一組公理和先前已證明的定理為起點，嘗試推導出新的運算式。

它的核心做法是避免嘗試所有可能的組合。它依啟發式為能產生的運算式排序，只展開最有希望的那些。這套方法大約在 1956 年達特茅斯研討會前後被提出。通用問題求解器則把這個想法推廣到任何能以目標、一組運算子與目前狀態描述的問題。

## 核心概念

- **啟發式（heuristic）**：估計候選項有多大希望的經驗法則。啟發式能引導搜尋，但不保證一定成功。
- **狀態空間（state space）**：一個問題可達到的所有狀態，以及在其間移動的運算子。證明就是從公理到目標運算式的一條路徑。
- **差異（difference）**：目前狀態與目標不同之處。
- **手段－目的分析（means–ends analysis）**：規則是，給定一個差異，求解者挑選一個已知能縮小該類差異的運算子，然後處理該運算子所需的前提條件。
- **子目標（subgoal）**：為了讓某個運算子可以套用而設定的目標。子目標本身還可能產生更多子目標。

## 運作方式

Logic Theorist 處理命題邏輯的運算式。它從公理與已建立的定理出發，套用代換與分離等運算子產生新的運算式。候選項依啟發式排序，啟發式會檢查它們與目標的接近程度。通往目標的那串運算就是證明。

通用問題求解器背後的一般方法是一個迴圈：

1. 若目前狀態符合目標，停止。
2. 找出目前狀態與目標之間的一個差異 $D$。
3. 選出一個已知能縮小 $D$ 這類差異的運算子 $O$。
4. 若 $O$ 無法套用，把它的前提條件設為子目標並先求解。
5. 套用 $O$，回到第 1 步。

每次套用都會縮小剩餘的差異。這個程序不保證最短路徑，但只要存在合適的運算子，它就會持續取得進展。

## 結果

1956 年的論文報告了 Logic Theorist 在符號邏輯定理上的執行結果，1957 年的論文則以同一程式與其啟發式進行了進一步實驗。主要主張是：啟發式選擇讓程式能為許多給定的定理找到證明，而不需要窮舉搜尋。這裡不重述確切的數字，讀者應直接參考原論文。

至於通用問題求解器，1958 年的論文主要透過理論與人類解題方式的吻合來論證，而不是依靠基準分數。

## 限制

- **組合式成長。** 啟發式能修剪搜尋，但候選狀態的數量仍會隨證明長度迅速增加。這些程式在小型領域中運作，超出後便吃力。
- **手工撰寫的知識。** 運算子與啟發式由程式設計者提供，程式本身不會學習，因此每個新領域都需要新的工程。
- **通用性。** 手段－目的分析在形式上與領域無關，但真實問題需要領域知識來選擇好的運算子，因此通用問題求解器在實務上比其名稱所示的範圍更窄。
- **心理學上的忠實度。** 聲稱程式能模擬人類思考的主張有爭議，而且吻合程度視任務而定。

## 開放問題

- 能否從資料學習過去引導這些程式的啟發式，同時保留讓搜尋可靠的性質？[A\* 搜尋](../../../../theory/paradigms/symbolic-ai/search/a-star/index.md)頁面討論了可容許啟發式的這項張力。
- 人類解題中有多少是手段－目的搜尋，又有多少依賴辨識或既有經驗？[認知架構](../../../../brain-mind/cognitive-architectures/index.md)頁面對此有所討論。
- 像 [Tree of Thoughts](../../../../theory/paradigms/symbolic-ai/search/tree-of-thoughts/index.md) 這樣在語言模型輸出上進行搜尋的系統，重新提出了生成器與搜尋程序該如何結合的問題。

## 參考文獻

### 開創性論文

- Newell, A. & Simon, H. A. (1956). The logic theory machine: A complex information processing system. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1956.1056797 — Logic Theorist 的原始描述，它透過對符號運算式進行啟發式搜尋來證明定理。
- Newell, A., Shaw, J. C. & Simon, H. A. (1957). Empirical explorations of the logic theory machine. *Papers presented at the Western Joint Computer Conference*. https://doi.org/10.1145/1455567.1455605 — 針對執行 Logic Theorist 及其啟發式效果所做的後續實驗。
- Newell, A., Shaw, J. C. & Simon, H. A. (1958). Elements of a theory of human problem solving. *Psychological Review*. https://doi.org/10.1037/h0048495 — 以一般性的方式提出把問題求解視為啟發式搜尋，這是通用問題求解器背後的理論。
- Simon, H. A. & Newell, A. (1958). Heuristic problem solving: The next advance in operations research. *Operations Research*. https://doi.org/10.1287/opre.6.1.1 — 一篇立場論文，主張啟發式解題程式應擴展作業研究的方法。
- Newell, A. & Simon, H. A. (1976). Computer science as empirical inquiry: Symbols and search. *Communications of the ACM*. https://doi.org/10.1145/360018.360022 — 物理符號系統假說，把 Logic Theorist 框定為符號處理系統。

### 綜述與教科書

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — 涵蓋早期符號程式及其所引入搜尋方法的 AI 史。
