---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- perception
- speech
aliases:
  - 多解析度頻譜時間模型
  - 頻譜時間感受野
  - Spectrotemporal Model
  - Chi et al. 2005
---

# 多解析度頻譜時間模型（Chi 等人，2005）

一種中央聽覺處理的計算模型，同時依頻譜與時間結構表示聲音，並在數種解析度下進行。

本頁是[聽覺系統](../index.md)的一個方法。它是[任務最佳化神經網路（Kell 等人，2018）](../kell-2018/index.md)中受訓練網路的人工設計對應。

## 概述

聲音在頻率與時間上都會變化，聽覺系統兩者都需要。頻譜圖顯示頻率隨時間的變化，但它沒有直接顯示皮層所關注的模式，例如聲音響度變化的快慢，或其頻譜結構的精細程度。Chi、Ru 與 Shamma（2005）提出一個同時表示這兩種結構的模型。

## 問題

問題在於：是否能有一個原則明確的表示，同時捕捉複雜聲音（例如語音與音樂）的頻譜與時間兩個面向，並且仍接近聽覺路徑已知的特性。

## 核心想法

模型先從類似耳蝸的頻譜圖出發，接著套用一組多解析度的濾波器。每個濾波器是一種理想化的頻譜時間感受野，對特定的頻譜尺度（模式在頻率上的精細程度）與特定的時間速率（模式隨時間變化的快慢）作出反應。輸出即是統一的多解析度表示。這個模型建立在早期與中央聽覺階段的心理聲學與神經生理發現之上。它的保真度則以從表示重建聲音來檢驗，藉此顯示特徵保留了多少訊號。

## 方程式或演算法

1. **周邊分析。** 計算聲音的時間－頻率頻譜圖，使用一組重疊的恆 Q 頻率濾波器。
2. **中央分析。** 以一組濾波器與頻譜圖做卷積。每個濾波器調諧於一個頻譜尺度與一個時間速率，且濾波器涵蓋數種解析度。
3. **表示。** 濾波器輸出構成一個四維的表示，維度為時間、頻率、尺度與速率。論文沿時間積分後得到三維的形式。
4. **重建。** 將表示反向轉換以重新合成聲音，並與原聲比較，以評估特徵保留了多少資訊。

論文給出複雜訊號通過每個階段的完整數學形式，並把這些階段與其他聽覺處理模型相連。

## 結果

論文的結果針對表示本身。重建測試顯示，部分重新合成的語音完全可懂，失去頻譜上尖銳的特徵會逐漸降低可懂度，而某些重建演算法仍會產生失真。較早、較簡單的版本曾經以語音可懂度與單耳相位敏感度檢驗。摘要沒有給出數值基準，因此本頁不引用任何數字。

## 限制

- **設計固定。** 濾波器是人工設計的，而非從資料中學得，因此無法適應它所聽到的聲音的統計特性。
- **描述性，而非對皮層的預測。** 模型描述的是表示，本身並不說明一群神經元會如何反應。
- **與資料的比較。** 在後續的研究中，頻譜時間濾波器模型解釋的跨聽覺皮層 fMRI 變異少於受訓練的網路（55.1% 對 69.9%）。人工設計的特徵因此可能遺漏學習所能捕捉的部分反應結構（Kell 等人，2018）。
- **範圍。** 摘要沒有對皮層作出明確主張，論文也說模型「不以生物物理為本」。因此任何與特定皮層神經元的連結都是一種推論。

## 連結

- **耳蝸前端**：模型從類似耳蝸所產生的頻譜圖出發。見[聽覺系統](../index.md)。
- **受訓練的替代方案**：同樣的問題，即什麼特徵最能描述聽覺皮層，在[任務最佳化網路](../kell-2018/index.md)中由學得的特徵回答。
- **感受野**：對特定頻率與時間模式的調諧，與[視覺皮層的感受野](../../neuroscience/receptive-fields-hubel-wiesel/index.md)的概念相呼應。
- **稀疏編碼**：對自然訊號的高效且具選擇性的表示，見[稀疏編碼](../../computational-neuroscience/sparse-coding/index.md)。

## 應用

- **模型比較**：Kell 等人（2018）以這類頻譜時間濾波器模型作為基準，比較受訓練的網路與皮層的 fMRI 反應。

## 開放問題

- **皮層使用哪些解析度？** 要符合皮層調諧所需的頻譜尺度與時間速率集合，仍在研究之中。
- **學得的或固定的？** 學習得來的前端是否會比人工設計的前端更符合皮層，如 Kell 等人（2018）所示，目前尚無定論。
- **噪音中的語音。** 此表示能否分開重疊的說話者，而不只是描述單一聲音，仍是開放問題。

## 參考文獻

### 開創性論文

- Chi, T., Ru, P. & Shamma, S. A.（2005）。Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*。https://doi.org/10.1121/1.1945807 — 原始論文。提出頻譜與時間特徵的統一多解析度表示，並以重建測試檢驗。
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H.（2018）。A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*。https://doi.org/10.1016/j.neuron.2018.03.044 — 將受訓練的網路與頻譜濾波器模型，在聽覺皮層 fMRI 上做比較。
- Theunissen, F. E., Sen, K. & Doupe, A. J.（2000）。Spectral-Temporal Receptive Fields of Nonlinear Auditory Neurons Obtained Using Natural Sounds. *The Journal of Neuroscience*。https://doi.org/10.1523/jneurosci.20-06-02315.2000 — 顯示由鳥鳴估得的頻譜時間感受野，比由隨機純音估得者更能預測聽覺神經元的反應。

### 綜述與教科書

- Robles, L. & Ruggero, M. A.（2001）。Mechanics of the mammalian cochlea. *Physiological Reviews*。https://doi.org/10.1152/physrev.2001.81.3.1305 — 綜述耳蝸力學：行進波、音調的位置編碼與外毛細胞放大。
- Rauschecker, J. P. & Scott, S. K.（2009）。Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*。https://doi.org/10.1038/nn.2331 — 綜述聽覺皮層中的圖與路徑，參照靈長類研究，並討論其對人類語音處理的意義。
