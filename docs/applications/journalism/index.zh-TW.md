---
translation_reviewed: 2026-10-28
related:
  - theory/models/llm
  - engineering/rag
  - society/safety-alignment
aliases:
  - 新聞與資訊生態
  - Journalism
  - Automated journalism
---

# 新聞與資訊生態

AI 在兩個方向影響新聞業。新聞編輯室用它撰寫、查核與發布報導；它也改變資訊的傳播方式，透過排序與推薦內容的平台。本頁涵蓋兩方面，從自動化報導到假新聞的散布。

## 概況

| 領域 | 例子 |
|---|---|
| 自動化報導 | 依結構化資料撰寫例行報導（例如財報或體育賽果）的軟體 |
| 研究與查核 | 搜尋文件與資料，並以來源查核主張 |
| 轉寫與檔案 | 把音訊與影片轉成可搜尋的文字 |
| 發布 | 排序並向讀者推薦文章 |
| 錯誤資訊 | 生成或散布假內容，以及偵測它們 |
| 受眾工具 | 摘要、翻譯與個人化電子報 |

## 自動化新聞

自動化新聞以軟體把結構化資料轉為新聞報導。Graefe（2016）回顧了這方面的研究，包括這些系統的運作方式及其在新聞編輯室中的應用，並以洛杉磯時報與美聯社的案例為例。Carlson（2015）則探討自動化新聞對勞動與新聞權威的更廣泛影響。

## 演算法的問責

新聞機構也會調查塑造公共生活的演算法。Diakopoulos（2014／2015）討論記者如何進行這類調查，其著作《Automating the News》（2019）則說明演算法如何重塑新聞的製作與發布。

## 假新聞的散布

Vosoughi、Roy 與 Aral（2018）比較了真假新聞在 Twitter 上的散布方式。偵測與限制錯誤資訊是重要的研究領域，部分取決於平台如何排序內容。

## 關鍵方法

有三種方法最為相關。每個都連結到解釋它的頁面。

- [大型語言模型](../../theory/models/llm/index.md)：起草報導與摘要，但需要編輯審查，因為它們可能流暢地陳述錯誤。
- [檢索增強生成](../../engineering/rag/index.md)：讓答案以文件檔案為依據，使每項主張都能追溯到來源。
- [安全與對齊](../../society/safety-alignment/index.md)：如何引導模型避免產生有害或錯誤的內容。

## 風險

- **大規模錯誤。**自動化報導可能同時在許多篇文章中重複同一個錯誤的資料來源。
- **信任。**讀者可能不知道報導是人還是機器寫的，而揭露的做法各有不同。
- **經濟。**自動化產出可能取代支撐在地新聞採訪的工作。

## 未解問題

- 新聞編輯室應如何揭露自動化寫作，讓讀者能夠判斷？
- 查核工具能否跟上生成式錯誤資訊的速度？
- 在地新聞編輯室需要什麼，才能使用這些工具而不失去編輯自主？

## 參考文獻

### 開創性論文

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science* 359(6380). https://doi.org/10.1126/science.aap9559 — 比較真假新聞在 Twitter 上的散布方式。
- Carlson, M. (2015). The Robotic Reporter: Automated journalism and the redefinition of labor, compositional forms, and journalistic authority. *Digital Journalism* 3(3). https://doi.org/10.1080/21670811.2014.976412 — 探討自動化新聞及其對勞動與新聞權威的影響。
- Diakopoulos, N. (2015). Algorithmic Accountability. *Digital Journalism* 3(3). https://doi.org/10.1080/21670811.2014.976411 — 討論記者如何調查塑造公共資訊的演算法。

### 教科書與綜述

- Diakopoulos, N. (2019). *Automating the News: How Algorithms Are Rewriting the Media*. Harvard University Press. https://doi.org/10.4159/9780674239302 — 一本關於演算法如何塑造新聞製作與發布的書。

### 文章與文件

- Graefe, A. (2016). *Guide to Automated Journalism*. Tow Center for Digital Journalism, Columbia University. https://data.journalism.columbia.edu/sites/data.journalism.columbia.edu/files/content/guide-to-automated-journalism.pdf — 回顧自動化新聞的研究，並以洛杉磯時報與美聯社的案例為例。
