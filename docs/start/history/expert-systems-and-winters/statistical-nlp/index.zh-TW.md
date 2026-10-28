---
translation_reviewed: 2026-10-28
---

# 統計語言處理（1976–1993）

統計語言處理以從資料估計出的機率模型，取代手寫的文法與規則。它始於 1970 年代的語音辨識。到了 1990 年代初，同樣的方法也用於機器翻譯與詞性標註，並受惠於大型的人工標註語料庫，例如賓州樹庫（Penn Treebank）。

## 概述

到了 1970 年代，語音辨識已是單靠規則不足的最明顯例子。聲學訊號本身含糊不清，而能與之相符的詞序列多得無法用手列舉。IBM 的 Frederick Jelinek 與同事把辨識框定為一個統計決策：給定聲音，找出在語言模型與「每個詞如何發音」的模型下最可能的詞序列（Jelinek, 1976）。這種從規則轉向估計機率的做法，後來被稱為統計轉向。

1980 年代與 1990 年代初，同樣的思路擴散到其他問題。法英之間的翻譯，被建模為以平行文本中句子對學得的機率（Brown 等人，1990、1993）。詞性標註則以在標註文本上訓練的隱馬可夫模型來處理（Kupiec, 1992）。大型語料庫提供了這些方法所需的資料。這轉向並非一步到位，基於規則與統計的系統並存了多年，而統計方法主要以涵蓋範圍與穩健性勝出。

## 核心概念

- **語料庫**：大量的文字或語音，常由人工標註，用來估計模型參數並加以測試。
- **隱馬可夫模型（HMM）**：一種模型，其中一串隱藏狀態（例如詞性標記）產生觀察到的詞。它包含狀態之間轉移的機率，以及在某狀態下每個詞出現的機率。
- **源頭－通道模型**：從觀察到的輸出反推最可能的原始文字的方法，結合語言模型與「原始文字如何變成輸出」的模型。
- **參數估計**：從資料擬合模型的機率，可以透過計數，或以 EM 等迭代方法進行。

## 運作方式

語音辨識與翻譯共用同一個決策規則。給定觀察 $x$，選出使下式最大的來源句子 $w$：

$$
\hat{w} = \arg\max_{w}\; P(w)\, P(x \mid w).
$$

第一項是語言模型，偏好流暢的詞序列。第二項是通道模型：在語音中它描述聲學訊號，在翻譯中則是從對齊句子學得的機率翻譯模型。

對於詞性標註，對詞 $w_i$ 最可能的標記序列 $t_i$ 使下式最大：

$$
\hat{t} = \arg\max_{t}\; \prod_i P(w_i \mid t_i)\, P(t_i \mid t_{i-1}).
$$

每個因子都透過在已標記語料中計數來估計。解碼使用動態規劃，也就是維特比演算法，因此不必列舉所有可能就能找到最佳標記序列。Kupiec（1992）研究了如何使這類標註器更穩健，包括對訓練中很少出現的詞。

## 結果

這一時期的結果是以人工標註的資料來衡量的。例如，標註正確率是以人工標註的文本為準（Kupiec, 1992）。1990 與 1993 年的翻譯論文使用的是平行的法文與英文文本。Penn Treebank（Marcus 等人，1993）提供了一個共享的、人工標註的英文語料庫，使各研究團隊的結果得以比較。

## 限制

- **依賴資料。** 機率的好壞取決於語料庫。罕見事件估計不準，而在某一類文本上訓練的模型，可能在另一類文本上表現很差。
- **標註成本高。** 標記語料需要人力，而且只能部分涵蓋一種語言。
- **較難解釋。** 一張機率表可能預測得很準，卻無法說明一個句子為何合乎文法。統計轉向以明確規則換取了涵蓋範圍，這個取捨也是 [MYCIN](../mycin/index.md) 頁面所討論的。

## 連結

統計語言處理是今日語言模型的直接前身。它的機率框架延續到[語言模型](../../../../theory/models/nlp/index.md)，以及之後的[大型語言模型](../../../../theory/models/llm/index.md)，後者從規模大得多的語料庫估計詞元的機率。隱馬可夫模型屬於更廣的[機率圖模型](../../../../theory/probabilistic/graphical-models/index.md)家族。

這個方法也與心智與大腦的問題有交會。嬰兒在還不知道詞義之前，就能從音節的統計規律中，在連續語音裡找出類似詞的單位。這項發現在[嬰兒的統計學習](../../../../brain-mind/developmental-cognition/statistical-learning/index.md)頁面中討論。

## 應用

- **語音辨識**，用於聽寫與電話系統，是最早也最普及的應用之一。
- **機器翻譯**，以平行文本訓練的機率翻譯模型，成為後來統計系統的基礎。

## 開放問題

- 只靠文字上的統計，能學到多少語言的結構？這個問題把語言學家與計算研究者分成了不同陣營。
- 機率模型描述的是人如何理解語言，還是只說明機器能多好地處理語言？

## 參考文獻

### 開創性論文

- Jelinek, F. (1976). Continuous speech recognition by statistical methods. *Proceedings of the IEEE*. https://doi.org/10.1109/PROC.1976.10159 — 把連續語音辨識框定為以資料估計的機率模型所做的統計解碼。
- Brown, P. F. et al. (1990). A statistical approach to machine translation. *Computational Linguistics*. https://aclanthology.org/J90-2002/ — 把從法英平行文本學得的統計翻譯模型應用於機器翻譯。
- Brown, P. F., Della Pietra, S. A., Della Pietra, V. J. & Mercer, R. L. (1993). The mathematics of statistical machine translation: Parameter estimation. *Computational Linguistics*. https://aclanthology.org/J93-2003/ — 提出 IBM 翻譯模型，以及把它們擬合到平行文本的估計方法。

### 文章與文件

- Kupiec, J. (1992). Robust part-of-speech tagging using a hidden Markov model. *Computer Speech & Language*. https://doi.org/10.1016/0885-2308(92)90019-Z — 把隱馬可夫模型應用於詞性標註，並研究如何使標註器在實務中更穩健。
- Marcus, M., Santorini, B. & Marcinkiewicz, M. A. (1993). Building a large annotated corpus of English: The Penn Treebank. *Computational Linguistics*. https://aclanthology.org/J93-2004/ — 描述賓州樹庫，一個大型的人工標註英文語料庫，成為標準的訓練與測試資源。

### 綜述與教科書

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — 一部 AI 史，把轉向統計方法放進整個領域的發展脈絡中。
