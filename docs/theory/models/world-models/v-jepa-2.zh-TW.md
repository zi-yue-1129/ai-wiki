---
translation_reviewed: 2026-10-28
tags:
  - world models
  - self-supervised
  - robotics
aliases:
  - V-JEPA 2
  - V-JEPA 2-AC
---

# V-JEPA 2

V-JEPA 2 是一種自監督影片模型，它在表徵空間中預測被遮住的內容，而不是預測像素。這篇論文把它擴展為世界模型 V-JEPA 2-AC：在少量未標註的機器人影片上對一個以動作為條件的預測器做後訓練。作者接著用這個預測器來規劃機器人動作。

## 問題

影片模型學到很多外觀與動態，但只預測影片的模型無法告訴機器人，它的動作會造成什麼結果。論文探討：沒有標籤學到的影片表徵，能否在少量機器人資料下轉換成以動作為條件的預測器，並用於真實機械臂的規劃。

## 核心想法

編碼器以聯合嵌入預測目標，在大量影片上訓練，這種目標是預測輸入中被遮住部分的表徵。為了控制，作者在機器人軌跡上後訓練一個以執行動作為條件的預測器。接著在規劃迴圈中使用它，搜尋能讓結果接近目標影像的動作。

## 運作方式

1. 以預測被遮住影片區域表徵的方式預訓練影片編碼器，風格與 [I-JEPA](../../paradigms/self-supervised/index.md) 的聯合嵌入預測一致。
2. 在機器人影片上後訓練以動作為條件的預測器，其中動作即為記錄到的機器人運動。
3. 控制時，取樣候選動作序列，在表徵空間中預測其結果，並挑選預測狀態最接近目標影像的那一組。

確切的訓練目標與權重見論文的方法章節，重用前應先閱讀。

## 關鍵方法

V-JEPA 2 是為預先訓練好的影片預測器加入動作的其中一種方式。與其他方法相比：

- 相對於 [DINO-WM](dino-wm.md)，後者在目標環境自己的軌跡上，以凍結的影像編碼器訓練預測器；V-JEPA 2 則從在大量一般影片上訓練的編碼器出發，再用機器人影片做後訓練。
- 相對於 [Genie](genie.md)，後者生成可互動的影片；V-JEPA 2 在表徵空間中預測，用於規劃，而不是生成像素。

## 結果

根據摘要，V-JEPA 2-AC 在不到 62 小時、未標註的 DROID 資料集機器人影片上完成後訓練。接著，它在兩個實驗室的 Franka 機械臂上零樣本部署，透過規劃朝向目標影像，完成物件抓取與放置。摘要中的主要數字應直接從論文取得，而非從二手摘要取得。

## 限制

- 報告的機器人評估使用特定的機械臂與特定任務組合。論文並未說明能否推廣到其他機器人本體。
- 在表徵空間中規劃，取決於編碼器是否保留了分辨目標所需的特徵。

## 與其他主題的連結

V-JEPA 2 把[自監督](../../paradigms/self-supervised/index.md)的聯合嵌入預測研究，連結到以模型為基礎的控制。它的動作條件化引出與 [動作可控性](action-controllability.md) 相同的問題：預測器是否真的依賴它所獲得的動作。世界模型的更廣家族，見[總覽頁](index.md)。

## 應用

以學到的預測器做零樣本抓取與放置，以及在不同機器人的實驗室中用影片目標做規劃。

## 開放問題

- 新的機器人本體需要多少機器人資料，以及 62 小時是否只是下限。
- 在表徵空間中規劃，是否保留了精確抓取所需的細緻空間資訊。

## 參考文獻

### 奠基性論文

- Assran, M.、Bardes, A.、Fan, D. 等人 (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv 預印本. https://arxiv.org/abs/2506.09985 — 提出 V-JEPA 2 及其以動作為條件的變體 V-JEPA 2-AC，後者在機器人影片上做後訓練，用於零樣本規劃。

### 文章與預印本

- Zhou, G. 等人 (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — 在凍結影像特徵上的預測器，是從影片預訓練特徵做規劃的比較對象。
- Bruce, J. 等人 (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — 生成式的對應方法：在未標註影片上訓練的潛在動作模型。
- Assran, M. 等人 (2023). *Self-Supervised Learning From Images With a Joint-Embedding Predictive Architecture*. CVPR 2023. https://openaccess.thecvf.com/content/CVPR2023/html/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.html — V-JEPA 2 所延伸的影像版本聯合嵌入預測方法。
