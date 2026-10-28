---
translation_reviewed: 2026-10-28
related:
  - theory/models/computer-vision
  - theory/models/multimodal
  - society/ethics
aliases:
  - 無障礙與輔助科技
  - Accessibility
  - Assistive technology
---

# 無障礙與輔助科技

許多 AI 工具本質上是輔助性的：為盲人描述影像、為聽障者加上字幕，並為有認知或語言困難的人簡化文字。若未與身心障礙者一起設計與測試，相同的技術也可能讓產品更難使用。本頁說明 AI 如何提供協助，以及維持其責任的設計標準。

## 概況

| 領域 | 例子 |
|---|---|
| 影像描述 | 為螢幕閱讀器使用者描述照片與物體 |
| 視覺問答 | 回答有關攝影機所見內容的問題 |
| 字幕與轉寫 | 語音即時字幕，以及錄音的文字稿 |
| 社群與內容 | 為動態消息中的圖片自動產生替代文字 |
| 動態內容 | 為無法看見的使用者描述 GIF 與影片 |
| 語言與閱讀 | 簡化文字，以及為閱讀困難者提供語音合成 |

## 影像描述與視覺問題

VizWiz（Bigham 等人，2010）讓盲人拍下照片、以語音提問，並由遠端工作者回覆，通常幾分鐘內就能得到答案。以 11 位盲人參與者進行的實地部署，回報平均約兩分鐘得到答覆。自動替代文字則更進一步：Wu 等人（2017）描述一套為社群網路上的螢幕閱讀器使用者產生影像描述的系統，並以約 9,000 位 VoiceOver 使用者進行實地測試。Ga11y（Zhang 等人，2022）結合自動化與人工標註來描述 GIF 動畫。

## 標準

Web 內容無障礙指南 2.2（W3C，2024）為使網頁內容能被各類身心障礙者使用，訂定了可測試的標準。AI 功能與其他介面功能受同樣的標準檢驗，因此描述錯誤或缺漏的自動替代文字，仍算作不合格。世界衛生組織（2019）報告有多少人生活在視力喪失中，以及如何加強眼科照護，從而界定了需求的規模。

## 關鍵方法

多數輔助視覺工具的基礎是兩種方法。每個都連結到解釋它的頁面。

- [電腦視覺](../../theory/models/computer-vision/index.md)：辨識影像中的物體、文字與場景，影像描述工具仰賴此技術。
- [多模態模型](../../theory/models/multimodal/index.md)：結合影像與語言，回答有關場景的問題，如視覺問答。

## 風險

- **錯誤的描述**可能誤導無法檢查影像的使用者，因此錯誤需要明確的提示，以及容易更正的方式。
- **未與身心障礙者測試**，可能產生在基準測試中表現良好、實際上卻失敗的工具。
- **隱私。**描述周遭環境的攝影機可能拍到旁人。

公平與包容的議題見[倫理與公平性](../../society/ethics/index.md)。

## 未解問題

- 輔助工具應如何向無法看見影像的使用者說明自身的不確定性？
- 自動描述能否在各類內容上匹配人工撰寫的替代文字品質？
- 設計標準應如何擴充，以涵蓋 AI 生成的內容？

## 參考文獻

### 開創性論文

- Bigham, J. P. et al. (2010). VizWiz: nearly real-time answers to visual questions. *UIST '10*. https://doi.org/10.1145/1866029.1866080 — 盲人拍下場景並提問，由遠端工作者回覆，實地部署有 11 位參與者。
- Wu, S. et al. (2017). Automatic Alt-text: Computer-generated Image Descriptions for Blind Users on a Social Network Service. *CSCW '17*. https://doi.org/10.1145/2998181.2998364 — Facebook 為螢幕閱讀器使用者提供的自動影像描述，並進行為期兩週、約 9,000 位 VoiceOver 使用者的實地測試。
- Zhang, M. R., Zhong, M. & Wobbrock, J. O. (2022). Ga11y: An Automated GIF Annotation System for Visually Impaired Users. *CHI '22*. https://doi.org/10.1145/3491102.3502092 — 為盲人與低視力使用者標註 GIF 動畫，並比較三種標註介面風格。

### 教科書與綜述

- 世界衛生組織（2019）。*World report on vision*。WHO。https://www.who.int/publications/i/item/9789241516570 — 報告有多少人生活在視力喪失中，以及如何加強眼科服務。

### 文章與文件

- W3C（2024）。*Web Content Accessibility Guidelines (WCAG) 2.2*。W3C Recommendation。https://www.w3.org/TR/WCAG22/ — 使網頁內容能被各類身心障礙者使用的可測試標準。
