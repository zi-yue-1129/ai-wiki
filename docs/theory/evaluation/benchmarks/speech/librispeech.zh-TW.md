---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
---

# LibriSpeech

LibriSpeech 是約 1,000 小時的英文朗讀語音語料庫，取材自公共領域的有聲書，也是自動語音辨識的標準基準（Panayotov et al., 2015）。許多語音論文在改用其他資料前都會先報告它。

## 任務與資料

輸入是一段錄製的語音，輸出是其逐字稿。音訊來自與書籍文字對齊的 LibriVox 錄音。語料庫分為訓練資料，以及各自再分為乾淨與其他子集的開發集與測試集。其他子集是挑選來讓辨識器較難處理的，因此包含較困難的錄音（Panayotov et al., 2015）。

## 協定與指標

主要指標是詞錯誤率：替換、刪除與插入的總數除以參考詞數。分數取決於文字正規化，以及解碼時是否使用語言模型，因此論文必須說明兩者。此處常見系統所用的訓練目標連接時序分類，見 Graves et al. (2006)。

## 它能說明什麼

它顯示辨識器在朗讀、相對乾淨的語音上的表現。乾淨與其他子集之間的落差，則說明系統處理較困難錄音的能力。

## 限制

- **朗讀語音。** 有聲書的朗讀比對話規律，因此分數在實務上可能高估表現。
- **條件有限。** 語料庫涵蓋的說話者與錄音條件範圍固定。
- **差異很小。** 強系統在乾淨集上的錯誤率已很低，因此小差距需要信賴區間。

## 相關

- [語音概述](index.md) 比較語音基準。
- [基準測試概述](../index.md) 列出所有家族。

## 參考文獻

### 開創性論文

- Panayotov, V. et al. (2015). *Librispeech: An ASR corpus based on public domain audio books*. ICASSP 2015. https://doi.org/10.1109/ICASSP.2015.7178964 — 描述語料庫、切分方式與乾淨及其他子集。

### 文章與文件

- Graves, A. et al. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — 介紹許多在此語料庫上評估的辨識器所用的 CTC 損失。
- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — 在多個語音測試集上評估大型辨識器，而非只有一個。

### 補充來源

- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — 展示在大量語音上訓練的端到端辨識。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
