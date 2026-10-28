---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/symbolic-ai
tags:
  - evolutionary
  - program-synthesis
aliases:
  - Genetic programming
  - GP
  - 遺傳規劃
---

# 遺傳規劃

遺傳規劃把遺傳演算法的運算子應用於電腦程式（通常以樹狀結構表示），以演化出程式。Koza（1992）提出此方法，用來自動產生解決指定任務的程式。候選解是運算式而非固定長度的字串，因此搜尋能同時找到解的結構與常數。上層概述見[演化與群體智慧](index.zh-TW.md)。

## 概述

遺傳演算法在固定的編碼上搜尋。遺傳規劃則讓編碼可以成長：每個候選解是由函數與終端節點組成的樹，其大小與形狀在搜尋過程中都可以改變。這使它適合符號迴歸，即目標是一個能擬合資料的運算式。

## 問題

撰寫解決某任務的程式，通常需要人預先選定其結構。遺傳規劃則問：結構能否透過搜尋找到？它以測試案例為候選程式評分。

## 核心想法

程式是一棵樹。內部節點是函數，例如加法或條件判斷；葉節點是終端，例如輸入變數或常數。交叉會在兩個親代之間交換隨機選取的子樹，突變則以新產生的子樹取代某個子樹。適應度透過在測試案例上執行程式來衡量。

## 演算法

1. 從函數集與終端集中隨機建立一個由樹組成的族群。
2. 在測試案例上執行每棵樹，並計算其適應度，例如資料上的誤差。
3. 依適應度選出親代，可用錦標賽或與適應度成比例的選擇。
4. 以子樹交叉與子樹突變產生子代。
5. 取代族群並重複，直到某個程式達到成功標準或耗盡預算。

兩個對集合的條件使搜尋有良好定義。封閉性（closure）要求每個函數都能接受任何終端或其他函數可能產生的值。充分性（sufficiency）要求終端集與函數集合起來足以表示一個解。Koza（1992）詳細討論了這兩個條件，並舉了符號迴歸與布林函數學習等例子。

## 主要結果

Koza（1992）與 Koza（1994）描述了此方法及其在由測試案例定義的問題上的應用。本次檢查未能取得全文，因此本頁不引用任何結果，演算法一節中的例子也需要對照原書核實。引用效能主張前，請先查閱論文。

## 限制

- 樹往往會在沒有適應度對應提升的情況下不斷變大，這種現象稱為膨脹（bloat），它浪費評估次數，也使程式難以閱讀。
- 交叉可能破壞有用的子樹，因此搜尋可能需要很多世代。
- 以有限測試案例為基礎的適應度，可能獎勵只擬合案例、卻無法泛化的程式。
- 演化出的程式難以驗證，因此其在未見輸入上的正確性需要另外測試。

## 關聯

- [演化與群體智慧](index.zh-TW.md)是上層概述，遺傳規劃與其他群體方法並列於其中。
- [遺傳演算法](genetic-algorithms.zh-TW.md)是以固定編碼為基礎的方法，遺傳規劃把其運算子延伸到樹狀結構。
- [符號人工智慧](../symbolic-ai/index.zh-TW.md)以明確方式表示知識與程式，這正是遺傳規劃所搜尋的表徵。
- [NEAT](neat.zh-TW.md)演化的是網路結構而非運算式樹，使用相同的群體框架。

## 應用

- 符號迴歸，其輸出是擬合資料的可解釋公式。
- 以測試案例指定任務的控制器、濾波器與電路自動設計。

## 未解問題

- 如何在不限制可找到的程式的前提下控制膨脹？
- 遺傳規劃能否與學習模型結合，使搜尋產生能超越測試案例而泛化的程式？

## 參考文獻

### 開創性論文

- Koza, J. R.（1992）。*Genetic Programming: On the Programming of Computers by Means of Natural Selection*。MIT Press。https://openlibrary.org/isbn/0262111705 — 提出以樹為基礎的遺傳規劃，包含封閉性與充分性條件以及子樹運算子。
- Koza, J. R.（1994）。Genetic programming as a means for programming computers by natural selection。*Statistics and Computing*，4(2)。https://doi.org/10.1007/bf00175355 — 配套論文，闡述此方法及其在自動程式設計中的應用。
- Holland, J. H.（1975）。*Adaptation in Natural and Artificial Systems*。University of Michigan Press。https://doi.org/10.1145/1216504.1216510 — 遺傳規劃所延伸的遺傳演算法框架。此 DOI 連到該書 1975 年的一篇書評。

### 綜述與教科書

- Eiben, A. E. & Smith, J. E.（2015）。*Introduction to Evolutionary Computing*。Springer。https://doi.org/10.1007/978-3-662-44874-8 — 教科書，涵蓋遺傳規劃所用的表徵與運算子。
- Bäck, T.（1996）。*Evolutionary Algorithms in Theory and Practice*。Oxford University Press。https://doi.org/10.1093/oso/9780195099713.001.0001 — 教科書，分析群體搜尋，包括驅動膨脹的選擇壓力。

## 延伸學習

供想進一步探索的讀者參考，這些不是參考文獻。

- [DEAP](https://github.com/DEAP/deap) 包含遺傳規劃模組，附有以樹為基礎的範例。
