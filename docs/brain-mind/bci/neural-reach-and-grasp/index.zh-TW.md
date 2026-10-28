---
translation_reviewed: 2026-10-28
---

# 以神經控制的手臂進行伸手與抓取（Hochberg 等人，2012）

解碼器把運動皮質的脈衝活動轉為機械手臂的動作。

## 問題

四肢癱瘓的人能否用自己運動皮質的訊號，控制機械手臂去伸手與抓取物體？

## 核心想法

皮質內微電極陣列記錄運動皮質的放電活動。解碼器把這些活動對應到手臂的運動，而受試者能依視覺回饋，以閉環方式修正動作。

## 方程式或演算法


  1. 在受試者嘗試動作時記錄運動皮質神經元的放電活動。
  2. 由這些活動擬合出手臂速度或位置的解碼器。
  3. 以閉環方式執行解碼器，讓受試者能依所見修正手臂。

## 結果

四肢癱瘓的受試者能用機械手臂伸手並抓取物體，顯示解碼後的神經訊號能控制多關節的肢體。

## 限制

研究的受試者人數少。手臂的動作比自然肢體慢，植入物多年的穩定性與需要重新校正的問題仍未解決。

## 連結

- 母頁：[腦機介面與神經解碼](../index.md)
- 同一主題的另一方法：[言語神經義肢](../speech-neuroprosthesis/index.md)

## 參考文獻

### 開創性論文

- Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G. & Vaughan, T. M.（2002）。Brain–computer interfaces for communication and control. *Clinical Neurophysiology*. https://doi.org/10.1016/S1388-2457(02)00057-3 — 早期綜述，將 BCI 定義為把腦訊號轉為指令的系統，重點在為嚴重失能者提供溝通。
- Hochberg, L. R., 等人（2006）。Neuronal ensemble control of prosthetic devices by a human with tetraplegia. *Nature*. https://doi.org/10.1038/nature04970 — 顯示四肢癱瘓者能以皮質內陣列控制游標與其他裝置。
- Hochberg, L. R., 等人（2012）。Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — 顯示受試者能以機械手臂伸手並抓取物體。
- Willett, F. R., 等人（2023）。A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — 以遞迴網路與語言模型，從言語運動皮質高速解碼嘗試說話的內容。
- Moses, D. A., 等人（2021）。Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria. *New England Journal of Medicine*. https://doi.org/10.1056/NEJMoa2027540 — 以皮質腦電圖記錄，解碼一位無法說話者的句子。
