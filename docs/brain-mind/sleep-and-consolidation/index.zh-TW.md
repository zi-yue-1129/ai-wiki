---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- memory
- sleep
- reinforcement learning
aliases:
  - 睡眠、重播與記憶鞏固
  - Sleep and Memory
  - Memory Consolidation
  - Hippocampal Replay
  - 記憶鞏固
  - 海馬迴重播
  - SWR
---

# 睡眠、重播與記憶鞏固

新的記憶並不會在經驗結束的那一刻就定型。在休息與睡眠時，大腦會重播最近的活動，而這種重播被認為有助於把脆弱的記憶轉為穩定的記憶。同樣的原理，也就是從重播的經驗中學習，在人工智慧中是標準工具，這使得本主題成為神經科學與深度強化學習之間最清楚的橋樑之一。

## 概述

學會一條路線、一項任務或一串項目，會在數分鐘內改變大腦，但改變並不會在那一刻就完成。齧齒類動物的記錄顯示，經驗期間活躍的神經元，在動物休息或睡眠時會以壓縮的形式再次放電。這些重新活化很短暫，與特定的網路節律同步，而且可以順向或逆向地進行。綜合來看，這些證據顯示海馬迴會重播最近的經驗，而重播有助於記憶逐步轉移到新皮質。
## 核心概念

**海馬迴重播。** 大鼠海馬迴中的位置細胞（在特定位置放電的神經元）會依序放電，描繪動物穿越空間的路徑。動物跑完後休息時，同一序列會再度出現，有時是反向的。睡眠中的重播最先被報告，清醒時的重播隨後被發現。[方法頁](hippocampal-replay/index.zh-TW.md)說明相關證據。

**尖波漣波。** 重播由特定的網路事件承載。在 CA1 區，局部場電位出現一個大而緩慢的偏轉，稱為尖波，伴隨一個接近 200 Hz 的快速振盪，稱為漣波。這些事件發生在靜止不動、進食與飲水以及慢波睡眠期間。抑制它們會損害齧齒類動物的空間記憶，因此這個事件與記憶功能有關，而不只是時間上的巧合。[方法頁](sharp-wave-ripples/index.zh-TW.md)提供細節。

**系統鞏固。** 學習初期，許多記憶依賴海馬迴。隨著時間推移，新皮質會逐漸能夠在沒有海馬迴的情況下支持回憶。反覆的重新活化是提出的途徑之一。Frankland 與 Bontempi（2005）回顧近期與遠期記憶如何在這些結構之間組織。這種安排為何有用，見[互補學習系統](../memory-learning/complementary-learning-systems/index.zh-TW.md)，此處不重複。

**睡眠階段與學習。** 睡眠並非單一狀態。慢波睡眠是非快速眼動睡眠中最深的階段，Diekelmann 與 Born（2010）以及 Rasch 與 Born（2013）的綜述中，它與陳述性記憶（如事實與事件）的鞏固關聯最為一致。快速眼動睡眠的角色則較無定論。慢振盪、睡眠紡錘波與漣波，被認為會在睡眠中協調海馬迴與皮質之間的對話。

**經驗回放作為 AI 的類比。** 深度強化學習直接採用了重播。Lin（1992）重複使用儲存的經驗以加速學習；Mnih 等人（2015）則在深度 Q 網路中保留最近畫面的記憶，並隨機抽樣用於更新。重播能打破連續步驟之間的相關性，也讓學習者能重複利用罕見的經驗。大腦與演算法共享同一原理，但兩者的對應只是啟發式的，尚未獲得證實。Mattar 與 Daw（2018）提出一個規範性模型，依照重播對未來選擇的影響程度排序，這讓兩者之間有了可檢驗的連結。[方法頁](experience-replay/index.zh-TW.md)說明演算法，[經驗回放的理論頁](../../theory/paradigms/reinforcement-learning/experience-replay/index.zh-TW.md)則涵蓋其各種變體。

## 主要方法

兩個方法頁描述生物機制，一個方法頁描述演算法。以下簡要比較各頁。

- [海馬迴重播（Foster & Wilson, 2006）](hippocampal-replay/index.zh-TW.md)：它還原重播的序列本身，涵蓋清醒與睡眠中的動物，並顯示序列可以反向播放。
- [尖波漣波（Buzsáki 等人, 1992）](sharp-wave-ripples/index.zh-TW.md)：它涵蓋承載重播的網路事件，以及關閉該事件以檢驗其對記憶是否重要的實驗。
- [經驗回放（Lin, 1992；Mnih 等人, 2015）](experience-replay/index.zh-TW.md)：它是一種工程方法，即重複使用儲存轉移的緩衝區，也是以程式碼檢驗大腦類比的地方。

## 關聯

系統鞏固的說明依賴[互補學習系統](../memory-learning/complementary-learning-systems/index.zh-TW.md)中描述的快速與慢速學習系統，記憶系統的整體圖景則見[大腦中的記憶與學習](../memory-learning/index.zh-TW.md)。

重播也與規劃有關。Mattar 與 Daw 的模型提出，重播透過在需要之前更新價值，幫助選擇行動，這與[有模型與無模型控制](../decision-reward/model-based-vs-model-free/index.zh-TW.md)中討論的以模型為基礎的控制相關。逆向重播會把結果連回導致結果的各個狀態，與時序差分學習的價值傳遞相似，這個訊號見[多巴胺的獎勵預測誤差](../neuroscience/dopamine-reward-prediction-error/index.zh-TW.md)。

在 AI 方面，重播是[強化學習](../../theory/paradigms/reinforcement-learning/index.zh-TW.md)的標準工具之一；而重新排練舊資料，則是[持續學習](../../theory/paradigms/continual/replay-and-memory/index.md)中防止遺忘的標準做法。

## 應用

- **強化學習。** 深度 Q 網路等基於價值的代理人，以及許多離策略方法，都會使用重播緩衝區，以提高資料效率。
- **持續學習。** 訓練時交錯舊資料與新資料，受互補學習系統理論啟發，是對抗災難性遺忘的常用基準。
- **神經科學方法。** 能即時偵測漣波並加以關閉的閉環系統，用於檢驗重播是否具有因果作用。這些是研究工具，並非任何疾病已確立的治療。

## 未解問題

- **重播是因果作用，還是只是讀數？** 抑制漣波會損害記憶，但哪些內容與時機對鞏固是必要的，仍不清楚。
- **哪些記憶會被重播？** Mattar 與 Daw 的效用模型提出一條選擇規則。大腦在多種情境下是否遵循此規則，尚待確認。
- **睡眠中的重播與清醒時的重播功能相同嗎？** 兩者可能支持不同功能，例如鞏固與規劃。
- **哪些記憶會從睡眠中獲益？** 陳述性記憶的證據比其他記憶類型更強，其界線仍有爭議。
- **哪些能轉移到機器上？** 哪些重播規則能改善大型學習系統，哪些只是類比，仍是開放問題。

## 參考文獻

### 奠基性論文

- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of hippocampal ensemble memories during sleep. *Science* 265, 676–679. https://doi.org/10.1126/science.8036517 — 報告清醒時海馬迴位置細胞的活動模式，在睡眠中重新活化。
- Skaggs, W. E. & McNaughton, B. L. (1996). Replay of neuronal firing sequences in rat hippocampus during sleep following spatial experience. *Science* 271, 1870–1873. https://doi.org/10.1126/science.271.5257.1870 — 報告空間經驗之後，睡眠期間位置細胞放電序列的重播。
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — 顯示清醒大鼠在跑動後的休息期間，位置細胞序列會以反向順序重播，並提出與強化學習評估相關的解釋。
- Buzsáki, G. 等人（1992）。High-frequency network oscillation in the hippocampus. *Science* 256, 1025–1027. https://doi.org/10.1126/science.1589772 — 描述靜止不動、進食與慢波睡眠期間 CA1 約 200 Hz 的振盪，即承載重播的漣波事件。
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — 提出依效用排序重播的假說，可同時解釋向前的規劃與逆向重播。
- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning* 8, 293–321. https://doi.org/10.1007/BF00992699 — 為強化學習代理人提出經驗回放，重複利用儲存的經驗以加速學習。
- Mnih, V. 等人（2015）。Human-level control through deep reinforcement learning. *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — 深度 Q 網路，從重播記憶中均勻抽樣近期經驗。

### 綜述與教科書

- Buzsáki, G. (2015). Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus* 25, 1073–1188. https://doi.org/10.1002/hipo.22488 — 關於尖波漣波、其迴路起源，以及其在重播、記憶鞏固與規劃中角色的長篇綜述。
- Wittkuhn, L. 等人（2021）。Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — 回顧神經科學與機器學習中重播的計算功能，並比較兩個領域。
- Frankland, P. W. & Bontempi, B. (2005). The organization of recent and remote memories. *Nature Reviews Neuroscience* 6, 119–130. https://doi.org/10.1038/nrn1607 — 回顧近期與遠期記憶如何隨時間在海馬迴與皮質之間組織。
- Diekelmann, S. & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience* 11, 114–126. https://doi.org/10.1038/nrn2762 — 回顧睡眠，特別是慢波睡眠，如何支持記憶鞏固。
- Rasch, B. & Born, J. (2013). About sleep's role in memory. *Physiological Reviews* 93, 681–766. https://doi.org/10.1152/physrev.00032.2012 — 關於睡眠在記憶中角色的長篇綜述，涵蓋睡眠階段與機制。
