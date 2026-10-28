---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
aliases:
  - Speech benchmarks
  - 語音基準
---

# 語音基準

語音基準測試自動語音辨識，也就是把音訊轉成文字的能力。分數通常是固定測試集上的詞錯誤率，因此只有在切分、文字標準化與解碼設定都相同時，結果才可以比較。

## 概述

早期的端到端語音系統以大量已轉錄的語音訓練，並在少數標準測試集上評判。例如 Deep Speech 是比傳統語音系統更簡單的端到端系統，傳統系統依賴人工建構的處理階段。作者報告，它在 Switchboard Hub5'00 測試集上的錯誤率為 16.0%，並指出該系統在嘈雜環境中的表現優於當時廣泛使用的商用系統（Hannun et al., 2014）。連接時序分類（CTC）是一種把未分段的音訊與文字對齊的訓練目標，使這類模型不需要逐幀標籤也能訓練（Graves et al., 2006）。

LibriSpeech 提供了一個公開的測試集，取材自公有領域的有聲書錄音，使不同系統能在相同的語音上比較（Panayotov et al., 2015）。之後的研究則問這些分數能否轉移。Whisper 以 68 萬小時的多語言與多任務監督資料訓練，作者報告它無需微調即可在標準基準上達到良好的泛化，並接近人類的準確率與穩健性（Radford et al., 2022）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [LibriSpeech](librispeech.md) | 轉錄朗讀的英文有聲書語音 | 乾淨與較難（other）測試集上的詞錯誤率 |

LibriSpeech 是此家族的主要基準。它的乾淨測試集與較難的 other 測試集，可區分系統在較容易與較困難語音上的表現，因此兩個數字應該一起報告。

## 關鍵概念

- **詞錯誤率（WER）**：使辨識結果與參考文字一致所需的詞替換、刪除與插入數，除以參考文字的詞數。
- **標準化**：在計分前，對參考文字與辨識結果都套用的大小寫、標點與數字規則。
- **零樣本轉移**：在未用該基準的資料訓練的情況下測試模型。大型網路訓練的模型可以做到這一點（Radford et al., 2022）。

## 運作方式

辨識器為測試集中的每個音訊檔產生轉錄文字。轉錄文字與參考文字以相同方式標準化、對齊，並在所有測試語句上計算 WER。解碼的選擇，例如解碼時使用的語言模型與束搜尋寬度，都會改變分數，因此屬於協定的一部分。

## 常見問題

- **標準化。** 詞錯誤率取決於比對前如何標準化標點、大小寫與數字，因此標準化規則必須報告。
- **領域轉移。** 朗讀的有聲書語音與對話、口音和嘈雜錄音不同，因此在一個測試集上的低錯誤率不會自動轉移到其他測試集（Radford et al., 2022）。
- **訓練重疊。** 大規模網路訓練資料可能包含與測試內容相近的錄音，因此測試集的來源歷史很重要。
- **測試集雜訊。** 單一測試集的變異可能就足以掩蓋詞錯誤率的小差異，因此接近的系統之間需要顯著性檢定。

## 相關連結

- [語言](../language/index.md) 涵蓋純文字的對應基準，其中也出現相同的標準化與資料污染問題。
- [語音模型](../../../models/speech/index.md) 說明這些基準所評估的系統。
- [聽覺系統](../../../../brain-mind/auditory-system/index.md) 說明人如何辨識語音，這是神經基準有時用來比較聽覺模型的對象。

## 開放問題

- 如何以不獎勵記憶單一測試集的基準，衡量語音系統在口音、語言與各種條件下的穩健性。
- 詞錯誤率是否能捕捉聽者所重視的內容，例如意義，或只是與參考文字的表面吻合。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [協定](../../protocols/index.md) 涵蓋切分與報告方式。

## 參考文獻

### 開創性論文

- Graves, A., Fernández, S., Gomez, F. & Schmidhuber, J. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — 介紹 CTC 損失函數，許多語音辨識器所使用的訓練目標。
- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — 展示以大量語音訓練的端到端辨識，在 Switchboard Hub5'00 上錯誤率為 16.0%。
- Panayotov, V., Chen, G., Povey, D. & Khudanpur, S. (2015). *Librispeech: An ASR corpus based on public domain audio books*. ICASSP 2015. https://doi.org/10.1109/ICASSP.2015.7178964 — 介紹公有領域有聲書語料庫及其測試集。

### 文章與文件

- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — 以 68 萬小時的多語言與多任務監督資料訓練，並報告跨基準的零樣本結果。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 檢視基準的建構效度，以及廣泛宣稱的限制。
