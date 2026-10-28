---
translation_reviewed: 2026-10-28
---

# 從皮質解碼被注意的說話者（Mesgarani 與 Chang 2012）

Mesgarani 與 Chang（2012）在聽者同時聽到兩位說話者時記錄皮質活動，並報告皮質對被注意說話者的表徵，比對被忽略說話者的表徵來得更強。他們的方法從神經訊號重建聽者所注意的語音，使混合語音中的選擇性注意變得可以測量。本頁是[聽覺與聽覺系統](../index.md)的子頁，上層頁面提供概述，本頁說明方法與證據。

## 概述

在人群中跟隨一位說話者，就是雞尾酒會問題。Cherry（1953）以兩段同時出現的語音進行早期實驗，使這個問題成為可以受控研究的主題。[^1] 神經科學的問題是：大腦對被注意說話者的表徵，是否與對另一位說話者的表徵不同。

Mesgarani 與 Chang 的做法是直接記錄皮質。他們在接受癲癇手術監測的病人身上，把電極放在顳上回（一個已知處理語音的區域）的表面。參與者聽到兩位說話者的混合語音，並被告知要注意哪一位。接著分析這些紀錄，以判斷神經訊號反映的是哪位說話者。

## 核心概念

- **選擇性注意**：把處理資源集中在多個來源中的某一個來源上的能力。
- **皮質腦電圖（ECoG）**：從暴露於皮質表面的電極記錄的活動。它的訊號比頭皮記錄更具局部性。
- **解碼器**：把神經活動對應到刺激特徵的模型。線性解碼器是最簡單的形式。
- **語音混合**：兩位說話者的語音加在一起，因此它們的頻譜圖在時間與頻率上相互重疊。

## 運作方式

1. 在參與者聽單一位說話者時，記錄顳上回上方的 ECoG。使用神經訊號中的高頻部分，它能追蹤局部神經群體的活動。
2. 擬合一個線性解碼器，把帶有延遲的神經活動映射到語音頻譜圖。若 $r_k(t)$ 是電極 $k$ 的活動、$S_f(t)$ 是頻率 $f$ 的頻譜圖，模型為 $\hat{S}_f(t) = \sum_{k,\tau} w_{k,\tau,f}\, r_k(t-\tau)$，權重以迴歸擬合。
3. 同時呈現兩位說話者，參與者注意其中一位。
4. 把解碼器套用到混合語音期間記錄的神經活動上，產生重建的頻譜圖。
5. 比較重建結果與被注意及被忽略說話者的頻譜圖。哪一位說話者的頻譜圖與重建結果較為接近，就表示它在皮質表徵中佔主導地位。

解碼器是在單一說話者的語音上訓練的，因此對被注意說話者的偏好，必須來自混合語音期間的神經訊號。

## 結果

論文報告，混合語音期間的重建結果比被忽略的說話者更貼近被注意的說話者，因此皮質對混合語音的表徵由被注意的說話者主導。圖表與統計數字見於論文原文，本頁以文字描述此結果。

這項結果把行為上的想法轉化為可測量的皮質變化，也提供了直接的方式來探問選擇發生在路徑的哪個位置。

## 限制

- **樣本小。** 紀錄來自少數病人，電極位置是基於臨床原因而設定，並非依研究問題而定。
- **受控條件。** 解碼器是在單一說話者上訓練的，混合語音是固定的，注意的線索也是明確給出的。對其他聲音、音量與自然聆聽情境的推廣，尚未在此檢驗。
- **讀出而非機制。** 這個方法顯示哪位說話者被表徵，卻沒有說明注意如何改變這種表徵。

## 開放問題

- **注意是增強被注意的說話者、抑制另一位，還是兩者兼具？** 要回答這個問題，需要一個中性的基線，而本研究的設計並未提供。
- **選擇發生在路徑的哪個位置？** 紀錄來自皮質，位於腦幹之後。選擇是否更早就已發生，仍待確定。
- **這種讀出能否適用於自然情境？** 多位說話者、不同的噪音與日常聆聽，仍有待檢驗。

[^1]: Cherry 的實驗同時呈現兩段語音，並把不同的訊號分別送到兩耳，並以統計方式詮釋聽者的反應。

## 參考文獻

### 開創性論文

- Mesgarani, N. & Chang, E. F.（2012）。Selective cortical representation of attended speaker in multi-talker speech perception。*Nature*。https://doi.org/10.1038/nature11020 — 記錄說話者混合期間的皮質活動，並顯示被注意的說話者在表徵中佔主導地位。
- Cherry, E. C.（1953）。Some Experiments on the Recognition of Speech, with One and with Two Ears。*The Journal of the Acoustical Society of America*。https://doi.org/10.1121/1.1907229 — 早期關於在兩段語音同時出現時如何辨識語音的實驗。
- Mesgarani, N., Cheung, C., Johnson, K. & Chang, E. F.（2014）。Phonetic Feature Encoding in Human Superior Temporal Gyrus。*Science*。https://doi.org/10.1126/science.1245994 — 記錄顳上回的語音反應，並顯示它們如何編碼語音特徵。

### 綜述與教科書

- Mattys, S. L., Davis, M. H., Bradlow, A. R. & Scott, S. K.（2012）。Speech recognition in adverse conditions: A review。*Language and Cognitive Processes*。https://doi.org/10.1080/01690965.2012.705006 — 回顧聽者如何在噪音中辨識語音，以及哪些過程能加以補償。
- Rauschecker, J. P. & Scott, S. K.（2009）。Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing。*Nature Neuroscience*。https://doi.org/10.1038/nn.2331 — 根據靈長類研究主張，聽覺皮質具有前側與後側串流。

### 文章與文件

- Wang, D. & Chen, J.（2018）。Supervised Speech Separation Based on Deep Learning: An Overview。arXiv。https://arxiv.org/abs/1708.07524 — 綜述以深度學習方法從背景干擾中選出目標說話者。
