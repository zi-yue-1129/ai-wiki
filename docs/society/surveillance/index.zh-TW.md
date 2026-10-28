---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - society/privacy
  - society/governance
tags:
  - surveillance
  - facial recognition
  - human rights
aliases:
  - 監控
  - 臉部辨識
  - 人臉辨識
  - Facial recognition
---

# 監控、臉部辨識與人權

AI 讓比對人臉、追蹤移動與分析大量影像和文字的成本大幅降低。這些能力可以服務公共安全與便利性，也可能侵蝕隱私、讓人不敢集會，並且對特定群體造成不成比例的影響。本頁說明臉部辨識的準確度問題、預測性警務的使用，以及法律上的回應。

## 概述

**臉部辨識**是把一張臉的影像與儲存的影像庫比對，以驗證身分（一對一），或找出候選人（一對多）。這裡的**監控**指的是利用攝影機、資料庫與自動化分析，系統性地觀察人。人權上的擔憂在於，這些系統可能在人們不知情或未同意的情況下使用，而且其錯誤並不平均分布在所有人身上。

## 關鍵概念

- **偽陽性**：系統宣稱某人與影像庫相符，但其實不在庫中。在警務中，這可能導致錯誤的盤查或逮捕。
- **偽陰性**：系統未能比對出確實在庫中的人。
- **人口統計差異**：依性別、年齡、膚色或原籍國等群體，錯誤率出現的差異。
- **預測性警務**：以過去的犯罪紀錄進行統計建模，決定警察應該在哪裡巡邏。

## 運作方式

臉部辨識流程先偵測人臉，把它轉換為數值樣板，再與儲存的樣板比對。每個步驟都可能失敗。準確度取決於影像品質、訓練資料，以及比對門檻的設定；門檻決定了偽陽性與偽陰性之間的取捨。

準確度差異最早是在商用性別分類系統中被記錄下來的。Buolamwini 與 Gebru 測試了三套商用系統，發現深膚色女性的錯誤率最高，達 34.7%，而淺膚色男性的最高錯誤率為 0.8% [(Buolamwini and Gebru, 2018)](https://proceedings.mlr.press/v81/buolamwini18a.html)。美國國家標準與技術研究院（NIST）隨後測試了大量臉部辨識演算法，發現偽陽性率在不同人口群體間常相差 10 倍到 100 倍以上；在技術摘要中，女性的偽陽性是男性的 2 到 5 倍；而偽陰性的差異較小，且因演算法而異 [(Grother, Ngan and Hanaoka, 2019)](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8280.pdf)。偽陽性問題在監控中特別重要，因為一次錯誤比對就可能導致盤查、搜查或逮捕。

預測性警務也呈現相關問題。當模型以反映過去執法模式、而非潛在犯罪的紀錄來訓練時，可能重複並放大既有偏見 [(Lum and Isaac, 2016)](https://doi.org/10.1111/j.1740-9713.2016.00960.x)。

## 部署規模

喬治城大學法律中心隱私與科技中心在 2016 年的一項研究指出，執法單位的臉部辨識網路涵蓋逾 1.17 億名美國成年人，約每兩位美國成年人就有一位在這樣的網路之中 [(Garvie, Bedoya and Frankle, 2016)](https://www.perpetuallineup.org/)。這些數字已有十年之久，系統此後也持續成長，因此它們反映的是趨勢方向，而非當前的規模。

## 法律回應

歐盟 AI 法規禁止數種用途，包括未經挑選地從網路或閉路電視爬取臉部影像以建立辨識資料庫，以及在公共場所由執法機關進行即時遠端生物辨識，但有少數例外 [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)。部分城市與美國州政府限制警方使用臉部辨識，另有些地方則擴大使用。爭論的焦點在於：準確度改進是否足以支持更廣泛的使用，或某些用途無論準確度如何都應該禁止。

## 與其他頁面的關聯

監控帶出的隱私問題見[隱私與資料保護](../privacy/index.md)，公平性問題見[倫理與公平](../ethics/index.md)。人口統計差異的評估方法，與[評估](../../theory/evaluation/index.md)中討論的指標密切相關。

## 應用

臉部辨識用於解鎖手機、邊境旅客查驗、尋找失蹤人口與辨識嫌疑人。自動化影像分析則用於零售、交通與公共空間監控。每種應用都需要在效益、同意與錯誤成本之間取得不同的平衡。

## 開放問題

- 準確度差異能否降低到足以公平部署的程度？誰來在真實環境中驗證這項主張？
- 當人臉比對只是證據的一部分時，應該採用什麼樣的監督機制？
- 某些用途，例如對公共空間進行大規模監控，應該直接禁止，還是逐案管理？
- 因錯誤比對受害的人，要如何取得救濟？

## 參考文獻

### 重要論文

- Buolamwini 與 Gebru，*Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification*，Proceedings of Machine Learning Research 81（2018）。https://proceedings.mlr.press/v81/buolamwini18a.html — 顯示三套商用分類器在膚色與性別上的準確度差距很大。
- Lum 與 Isaac，*To Predict and Serve?*，Significance（2016）。https://doi.org/10.1111/j.1740-9713.2016.00960.x — 說明以有偏見的紀錄訓練的預測性警務模型，如何重現該偏見。

### 綜述與教科書

- Grother、Ngan 與 Hanaoka，*Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects*，NIST Interagency Report 8280（2019）。https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8280.pdf — 大規模評估臉部辨識演算法的人口統計差異。

### 文章與文件

- Garvie、Bedoya 與 Frankle，*The Perpetual Line-Up: Unregulated Police Face Recognition in America*，Center on Privacy & Technology at Georgetown Law（2016）。https://www.perpetuallineup.org/ — 記錄警方臉部辨識網路的規模，以及其對駕照照片的取用。
- 歐盟，*Regulation (EU) 2024/1689 (Artificial Intelligence Act)*，歐盟官方公報（2024）。https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 設定禁止行為與遠端生物辨識的限制。
