---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/misinformation
  - society/governance
  - society/ethics
tags:
  - elections
  - democracy
  - persuasion
aliases:
  - 選舉與民主
  - 人工智慧與選舉
  - 政治廣告
  - Political persuasion
---

# AI、選舉與民主

生成式 AI 可以寫出具說服力的政治訊息、製作逼真的合成媒體，並協助競選團隊大規模地對選民進行精準投放。這些能力引發了幾個問題：選舉是否公平、選民能否形成自己的判斷，以及當競選使用 AI 時誰該負責。本頁討論民主層面的風險。虛假內容的運作機制，見[錯誤資訊與深偽](../misinformation/index.md)。

## 概述

民主仰賴選民能夠了解候選人、辯論議題，並相信收到的資訊是誠實的。AI 帶來三項改變。它降低了製作政治文字與圖像的成本；它讓個人化訊息變得便宜；它也讓選民更難分辨真實內容與偽造內容。目前的研究顯示這些疑慮確有根據，但尚未證明 AI 能穩定地改變選舉結果。

## 關鍵概念

- **精準投放（microtargeting）**：依據個人資料，為特定個人或小群體量身打造政治訊息。
- **說服**：訊息造成的人的態度或自述意向的改變。
- **騙子紅利（liar's dividend）**：因為假貨存在，公眾人物得以把真實證據說成是假的。
- **政治廣告規範**：對競選與平台的法律義務，例如揭露與對投放的限制。

## 運作方式

競選團隊可以用 AI 系統起草多個版本的訊息、測試效果，並推送表現最好的版本。個人化內容則更進一步，系統可以依據選民表達的立場或人口特徵調整訊息。合成影片與聲音可以用來誤導，但研究顯示更常見的效果是不確定感。Vaccari 與 Chadwick 發現，人們面對深偽影片時，比較可能感到不確定，而不是被誤導；而這種不確定感會降低對社群媒體上新聞的信任 [(Vaccari and Chadwick, 2020)](https://doi.org/10.1177/2056305120903408)。

文字則是另一個問題。Kreps、McCain 與 Brundage 以三項實驗探討 AI 生成的新聞文字是否可信，以及它們能否影響人們的意見，包括對外交政策的意見 [(Kreps, McCain and Brundage, 2020)](https://doi.org/10.1017/XPS.2020.37)。

## 說服效果的證據

一項事前登記的實驗最直接地檢驗了精準投放的疑慮。Hackenburg 與 Margetts 建置了一個網路應用程式，把每位參與者的人口與政治資料輸入 GPT-4 的提示中。在一項有 8,587 名參與者的隨機實驗中，這些訊息普遍具有說服力，在某些情況下把對某項政策立場的支持提高了多達 12 個百分點。然而，精準投放訊息的說服效果，與非精準投放訊息相比並無統計上的顯著差異（4.83 對 6.20 個百分點，P = 0.226）。作者的結論是，現有 LLM 的影響力可能來自其通用文字的說服力，而非其為每個人量身打造的能力 [(Hackenburg and Margetts, 2024)](https://doi.org/10.1073/pnas.2403116121)。

公眾對 AI 標籤的反應也很重要。Altay 與 Gilardi 發現，人們對標示為 AI 生成的新聞標題抱持懷疑，即使內容屬實或是人寫的，因為他們假設這篇文章是完全由自動化產生的 [(Altay and Gilardi, 2024)](https://doi.org/10.1093/pnasnexus/pgae403)。因此，標籤可能同時影響對準確內容與不準確內容的信任。

## 規範回應

歐盟 AI 法規要求，部署生成或操縱深偽內容的 AI 系統的部署者，揭露該內容是人工生成的；但對部分創作與藝術性作品設有例外 [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)。平台對政治內容的政策，也會施加進一步的限制，而各服務與國家的規則差異很大。

## 與其他頁面的關聯

說服的研究與本維基中心理學與認知科學的部分相連，信念改變與來源信任一直是這些領域長期關注的主題。治理層面的問題見[法律、政策與治理](index.md)。虛假內容的運作機制見[錯誤資訊與深偽](../misinformation/index.md)。

## 應用

競選團隊使用 AI 撰寫內容、翻譯、進行志工接觸，以及分析選民資料。選務機關與事實查核者使用偵測工具與即時監測。平台則對政治內容套用標示與廣告透明度規則。

## 開放問題

- AI 生成的訊息是否真的會改變投票，而不只是態度或自述意向？在真實競選中，這種效果有多大？
- 對真實性的不確定感，會不會成為比欺騙更主要的民主危害？
- 當競選使用 AI 製作誤導內容時，誰應負責：競選團隊、工具提供者，還是平台？
- 如何要求競選揭露 AI 的使用，又不讓正當用途受到寒蟬效應的影響？

## 參考文獻

### 重要論文

- Kreps、McCain 與 Brundage，*All the News That's Fit to Fabricate: AI-Generated Text as a Tool of Media Misinformation*，Journal of Experimental Political Science（2020）。https://doi.org/10.1017/XPS.2020.37 — 三項實驗，探討 AI 生成新聞文字的可信度及其對意見的影響。
- Vaccari 與 Chadwick，*Deepfakes and Disinformation: Exploring the Impact of Synthetic Political Video on Deception, Uncertainty, and Trust in News*，Social Media + Society（2020）。https://doi.org/10.1177/2056305120903408 — 實驗證據顯示，深偽主要造成不確定感，並降低對新聞的信任。
- Hackenburg 與 Margetts，*Evaluating the persuasive influence of political microtargeting with large language models*，Proceedings of the National Academy of Sciences（2024）。https://doi.org/10.1073/pnas.2403116121 — 一項有 8,587 名參與者的事前登記實驗，發現 GPT-4 訊息具說服力，而精準投放並未帶來顯著的額外效果。
- Altay 與 Gilardi，*People are skeptical of headlines labeled as AI-generated, even if true or human-made, because they assume full AI automation*，PNAS Nexus（2024）。https://doi.org/10.1093/pnasnexus/pgae403 — 顯示 AI 標籤會降低人們對新聞標題的信任，包括準確的標題。

### 文章與文件

- 歐盟，*Regulation (EU) 2024/1689 (Artificial Intelligence Act)*，歐盟官方公報（2024）。https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 為深偽內容的部署者設定揭露義務。
