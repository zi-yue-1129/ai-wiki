---
translation_reviewed: 2026-10-28
---

# 言語神經義肢（Willett 等人，2023）

循環網路從言語運動皮質解碼音素機率，產生文字。

## 問題

無法說話的人能否透過解碼與言語相關的神經活動，快速溝通？

## 核心想法

皮質內陣列記錄言語運動皮質。遞迴神經網路從每個時間窗口的活動中解碼音素機率，語言模型再把這些機率轉成最可能的詞語序列。

## 方程式或演算法


  1. 在受試者嘗試說話時記錄神經活動。
  2. 以遞迴網路解碼音素機率。
  3. 以語言模型選出最可能的詞語序列。

## 結果

論文報告，在大詞彙量下，嘗試說話的解碼速度可達每分鐘數十個詞。

## 限制

結果來自人數很少的受試者，需要更長時間的重複驗證。解碼器需以每位受試者的記錄進行訓練。

## 連結

- 母頁：[腦機介面與神經解碼](../index.md)
- 同一主題的另一方法：[神經控制的伸手與抓取](../neural-reach-and-grasp/index.md)

## 參考文獻

### 開創性論文

- Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G. & Vaughan, T. M.（2002）。Brain–computer interfaces for communication and control. *Clinical Neurophysiology*. https://doi.org/10.1016/S1388-2457(02)00057-3 — 早期綜述，將 BCI 定義為把腦訊號轉為指令的系統，重點在為嚴重失能者提供溝通。
- Hochberg, L. R., 等人（2006）。Neuronal ensemble control of prosthetic devices by a human with tetraplegia. *Nature*. https://doi.org/10.1038/nature04970 — 顯示四肢癱瘓者能以皮質內陣列控制游標與其他裝置。
- Hochberg, L. R., 等人（2012）。Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — 顯示受試者能以機械手臂伸手並抓取物體。
- Willett, F. R., 等人（2023）。A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — 以遞迴網路與語言模型，從言語運動皮質高速解碼嘗試說話的內容。
- Moses, D. A., 等人（2021）。Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria. *New England Journal of Medicine*. https://doi.org/10.1056/NEJMoa2027540 — 以皮質腦電圖記錄，解碼一位無法說話者的句子。
