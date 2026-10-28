---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
- neuroscience
- memory
- sleep
aliases:
  - Hippocampal Replay
  - Reverse Replay
  - 海馬迴重播
  - 反向重播
  - 序列重播
---

# 海馬迴重播（Foster & Wilson, 2006）

海馬迴重播是指，經驗期間記錄到的神經元放電序列，在動物休息或睡眠時再次被重新活化。Foster 與 Wilson（2006）顯示，清醒的大鼠在跑動後會以反向順序重播這些序列。

本頁是[睡眠、重播與記憶鞏固](../index.zh-TW.md)的一部分。承載重播的網路事件，見[尖波漣波](../sharp-wave-ripples/index.zh-TW.md)。

## 概述

位置細胞是海馬迴中，在動物位於特定位置時放電的神經元。動物跑過一條路線時，位置細胞會依固定順序放電，因此其放電序列描繪出路徑。重播是指，同樣的順序在經驗之後的時間再次出現，通常速度更快。因此，重播以壓縮的形式承載過去的資訊。若大腦需要儲存或評估過去，又不必真的重跑一次，這就很有用。

## 問題

海馬迴是形成新情節記憶所必需的，病人 H.M. 即為例證（見[大腦中的記憶與學習](../../memory-learning/index.zh-TW.md)）。當時未解的問題是，資訊如何離開海馬迴。重播提供了一種解答：若海馬迴重複近期的序列，新皮質便能從中學習。這個答案取決於重播是否確實發生，以及它是否也發生在清醒時，而不只是睡眠時。

## 核心想法

Wilson 與 McNaughton（1994）同時記錄多個位置細胞。他們發現，大鼠跑動時代表其路徑的活動模式，會在之後的睡眠中重新活化。Skaggs 與 McNaughton（1996）報告，空間經驗之後的睡眠期間，會重播位置細胞的放電序列。Foster 與 Wilson（2006）接著記錄清醒大鼠的活動。跑完之後，位置細胞的序列以跑動時相反的順序播放。Diba 與 Buzsáki（2007）發現，在[尖波漣波](../sharp-wave-ripples/index.zh-TW.md)頁所述的漣波事件中，序列既會順向播放，也會反向播放。

反向順序之所以重要，是因為它把結果連回導致結果的各個狀態。Foster 與 Wilson 認為，這可能支持對事件序列的評估，類似強化學習模型中的做法。

## 方程式或演算法

重播沒有單一的方程式。量測它的方法是一套偵測程序：

1. 記錄跑動期間許多位置細胞的放電，並估計每個細胞最常放電的位置。
2. 在之後的休息或睡眠期間，找出群體活動的爆發。
3. 對每個爆發，解碼各個活躍細胞所代表的位置，並依其放電時間排序。
4. 將此順序與跑動的順序比較。順向或反向的高度吻合，是重播的證據；這須與打亂序列的對照組比較後才能判定。

## 結果

- 清醒時位置細胞的活動模式，已在睡眠中觀察到重播（Wilson & McNaughton, 1994；Skaggs & McNaughton, 1996）。
- 已觀察到跑動後的清醒重播，在 Foster 與 Wilson（2006）的研究中，序列以反向順序播放。
- 在尖波漣波期間，序列會順向與反向播放（Diba & Buzsáki, 2007）。
- Mattar 與 Daw（2018）建立了一個規範性模型，依效用為每個候選記憶排序，效用定義為更新該記憶所帶來的未來獎勵增益，乘以代理人預期會造訪該狀態的折扣後次數。此模型可同時解釋有助於規劃的順向重播，以及把結果連回先前行動的逆向重播。

## 限制

- **觀察不等於因果。** 重播顯示序列被重新活化，但不表示這種重新活化就是記憶得以持久的原因。因果性的檢驗主要來自干擾承載重播的漣波（見[尖波漣波](../sharp-wave-ripples/index.zh-TW.md)）。
- **解碼依賴各種選擇。** 重建細胞順序取決於位置場的估計方式與所用的統計對照。結論受這些選擇影響。
- **證據主要來自齧齒類動物的空間任務。** 其他物種與任務中的重播，特徵較不清楚。
- **逆向重播的功能仍有爭議。** Foster 與 Wilson 將其與事件序列的評估連結，Mattar 與 Daw 則將其與規劃連結。後續研究尚未確定哪種解釋正確。

## 關聯

- **大腦。** 重播由[尖波漣波](../sharp-wave-ripples/index.zh-TW.md)承載。重播能訓練新皮質的想法，是[互補學習系統](../../memory-learning/complementary-learning-systems/index.zh-TW.md)的核心；更廣的記憶圖景見[大腦中的記憶與學習](../../memory-learning/index.zh-TW.md)。
- **獎勵與價值。** 評估的想法，將重播與[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.zh-TW.md)中的預測誤差訊號連結起來。
- **規劃。** 若重播是在模擬未來的路線或結果，它便與[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.zh-TW.md)中所述的以模型為基礎的控制相關。
- **AI。** 機器上的對應是[經驗回放](../experience-replay/index.zh-TW.md)。兩者都以不同於經驗發生時的順序，重複利用儲存的經驗。

## 應用

- **神經科學研究。** 在休息與睡眠期間，從位置細胞的記錄中讀出重播，並作為改變睡眠或休息的實驗中記憶處理的量測。這些是研究工具。

## 未解問題

- **哪些事件會被重播，原因為何？** Mattar 與 Daw 的效用解釋是其中一個候選，其對特定事件的預測仍在檢驗中。
- **睡眠中的重播與清醒時的重播功能相同嗎？** 兩者在鞏固與規劃中的角色可能不同。
- **重播如何改變皮質？** 從海馬迴重播到皮質持久改變的路徑，仍在研究中。
- **人類的重播與齧齒類動物的重播是否相似？** 證據正在增加，但較難取得。

## 參考文獻

### 奠基性論文

- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — 顯示清醒大鼠跑動後的休息期間，位置細胞序列會以反向順序重播，並提出與強化學習評估的關聯。
- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of hippocampal ensemble memories during sleep. *Science* 265, 676–679. https://doi.org/10.1126/science.8036517 — 報告清醒時海馬迴位置細胞的活動模式，在睡眠中重新活化。
- Skaggs, W. E. & McNaughton, B. L. (1996). Replay of neuronal firing sequences in rat hippocampus during sleep following spatial experience. *Science* 271, 1870–1873. https://doi.org/10.1126/science.271.5257.1870 — 報告空間經驗之後，睡眠期間位置細胞放電序列的重播。
- Diba, K. & Buzsáki, G. (2007). Forward and reverse hippocampal place-cell sequences during ripples. *Nature Neuroscience* 10, 1241–1242. https://doi.org/10.1038/nn1961 — 報告在尖波漣波期間，位置細胞序列同時順向與反向播放。
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — 提出依效用排序重播的假說，在模擬導航中同時解釋向前規劃與逆向重播。

### 綜述與教科書

- Davidson, T. J., Kloosterman, F. & Wilson, M. A. (2009). Hippocampal replay of extended experience. *Neuron* 63, 497–507. https://doi.org/10.1016/j.neuron.2009.07.027 — 報告海馬迴對較長段空間經驗的重播，超越早期研究中的短序列。
- Wittkuhn, L. 等人（2021）。Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — 回顧神經科學與機器學習中重播的計算功能，並比較兩個領域。
