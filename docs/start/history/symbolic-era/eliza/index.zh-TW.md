---
translation_reviewed: 2026-10-28
---

# ELIZA

ELIZA 由 MIT 的 Joseph Weizenbaum 撰寫，並於 1966 年發表，是一個對話程式。它會把使用者句子中的關鍵字與分解模式比對，再從重組模板產生回覆。它沒有任何語意模型，卻顯示出人們多麼容易把理解歸於一台只是反映自己言語的機器。它是這個時期最知名的自然語言系統，也是[符號時代](../index.md)的重要里程碑。

## 概述

自然語言是早期 AI 程式設計者給自己設定的最困難問題之一，因為句子取決於句法、語意與脈絡。ELIZA 走了另一條路。它不去解析並理解句子，而是尋找觸發詞，把句子改寫成固定形式，再由該形式組出回覆。最有名的腳本模仿一位非指導型心理治療師，這讓程式有了一個很方便的理由：不斷提問，並把使用者的陳述反映回去。

這個程式顯示，一段對話只需要極少的東西，就能讓參與者覺得有意義。Weizenbaum 設計 ELIZA 是為了展示這類方法的限制，但他對有些使用者如此認真看待它感到不安。他的 1966 年論文描述了這套機制，並討論了這些心理層面的問題。

## 核心概念

- **關鍵字（keyword）**：輸入中會觸發特定規則組的詞。每個關鍵字可以帶有一個排序，用來決定多個關鍵字同時出現時使用哪一個。
- **分解規則（decomposition rule）**：把輸入句子切成片段的模式，例如關鍵字前後的詞語。
- **重組規則（reassembly rule）**：把片段放進回覆中的模板。通常會交換代名詞（例如「my」變成「your」），使回覆直接對著使用者說。
- **腳本（script）**：某一種對話角色的完整關鍵字與規則集合。改變腳本會改變程式的行為，而比對引擎不必改變。
- **ELIZA 效應（ELIZA effect）**：人們傾向於把理解、感受或意圖歸於一個只是反映其輸入的程式。

## 運作方式

ELIZA 的處理是一個簡短的模式比對循環：

1. 掃描輸入中的關鍵字，並選出排序最高的那一個。
2. 套用該關鍵字所附的分解規則，把輸入切成若干部分。
3. 為這種分解選擇一條重組規則，並輪流使用不同的替代規則，使回覆不會完全重複。
4. 把各部分填入模板，交換代名詞，然後回傳回覆。
5. 若輸入中沒有關鍵字，則退回一個通用回覆，例如請對方繼續說。

下面的順序是該方法的示意例子，並非論文中的對話紀錄。對於輸入「I am sad about my job」，一條針對「I am」的規則可能把句子分解為「sad about my job」，再重組為「How long have you been sad about your job?」。句子的任何部分都沒有被理解，程式只有一個模式和一個模板。

因此，這個引擎是一組作用於文字的小規則，沒有對世界的內部表示，也沒有對先前意義的記憶，更不會學習。它的輸出取決於給它的腳本。

## 結果

Weizenbaum 1966 年的論文描述了 ELIZA 的設計與示範中使用的腳本，並討論這種方法所引發的心理層面問題。這些證據是定性的：程式在示例對話中的運作被展示，其對使用者的影響也被報告與討論。論文並未提出基準分數，因此應把結果視為一種方法的示範，而非經過測量的效能水準。

## 限制

- **沒有理解。** 回覆可以很流暢，卻仍然誤解使用者說了什麼，因為程式從不表示句子的意義。
- **脆弱。** 沒有比對到任何關鍵字的句子，或以錯誤含義比對到關鍵字的句子，都會產生忽略內容的回覆。
- **手工撰寫的腳本。** 每個新的對話領域都需要由人撰寫新腳本，規則也無法移轉。
- **誤導性的印象。** ELIZA 效應意味著使用者的滿意度不能證明系統理解了什麼。這後來成為對話系統研究的核心關切。

## 開放問題

- 流暢的對話在哪裡結束，理解又在哪裡開始？同樣的問題在[大型語言模型](../../../../theory/models/llm/index.md)上再度出現，它們以截然不同的途徑產生能力強得多的回覆。
- 設計者應如何呈現對話系統，才不會讓使用者對它理解什麼產生誤解？這是[人機互動](../../../../society/human-ai-interaction/index.md)的問題。
- 人們是否以對待人的方式，把心理狀態歸於機器？[心理學](../../../../brain-mind/psychology/index.md)頁面討論了將心智歸於人工系統的相關證據。

## 參考文獻

### 開創性論文

- Weizenbaum, J. (1966). ELIZA: A computer program for the study of natural language communication between man and machine. *Communications of the ACM*. https://doi.org/10.1145/365153.365168 — 描述 ELIZA 的關鍵字、分解與重組規則，並討論它們所引發的心理層面問題。
- Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1956.1056813 — 比較有限狀態、短語結構與轉換式三種文法模型，是早期自然語言研究的形式背景。
- Winograd, T. (1972). Understanding natural language. *Cognitive Psychology*. https://doi.org/10.1016/0010-0285(72)90002-3 — 描述一個針對積木微世界的語言理解系統，是 ELIZA 以模式為基礎之做法的對照案例。

### 綜述與教科書

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — 一部 AI 史，把早期語言與對話研究放在該領域整體發展之中來描述。

### 文章與文件

- Haenlein, M. & Kaplan, A. (2019). A brief history of artificial intelligence: On the past, present, and future of artificial intelligence. *California Management Review*. https://doi.org/10.1177/0008125619864925 — 簡短的 AI 史與其主要觀點，寫作時為一期特刊的導論。
