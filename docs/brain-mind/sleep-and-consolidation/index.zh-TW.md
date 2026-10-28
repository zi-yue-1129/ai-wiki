---
translation_reviewed: 2026-10-28
---

# 睡眠、重播與記憶鞏固

記憶鞏固是把剛形成的經驗轉變為持久記憶的過程。睡眠期間，大腦似乎會重播最近的經驗，最明顯的是慢波睡眠時海馬迴中的重播，而這種重播有助於把記憶移入新皮質的儲存處。同樣的想法，也就是透過重播既有經驗來保護先前學到的內容，如今已是人工智慧中的標準工具。

## 概述

人們在一夜睡眠後，通常比同樣時間保持清醒後記得更好（Diekelmann & Born, 2010）。因此睡眠對記憶而言，不只是休息。早期的失憶症研究顯示，形成新的情節記憶需要海馬迴，這部分見於[記憶與學習的神經機制](../memory-learning/index.md)。之後的損傷與記錄研究則顯示，許多記憶會隨時間而不再依賴海馬迴，這個過程稱為系統鞏固（Squire & Alvarez, 1995；Frankland & Bontempi, 2005）。

未解的問題是：是什麼把記憶從一個儲存處移到另一個？一個主流的提議是，近期經驗會在睡眠中離線地被再活化，而這種再活化會訓練新皮質。Wilson 與 McNaughton（1994）以生理層次給出這個想法的具體形式：清醒任務中出現過的海馬迴位置細胞放電模式，會在隨後的睡眠中重新出現。說明為何需要兩個儲存系統的理論，是[互補學習系統](../memory-learning/complementary-learning-systems/index.md)：海馬迴快速學習，並透過重播把經驗餵給慢速學習的皮質。

本頁最後以人工智慧的對應概念作結，也就是經驗回放。

## 核心概念

- **鞏固**：記憶在編碼之後隨時間穩定下來的過程。
- **系統鞏固**：記憶逐漸減少依賴海馬迴、更多依賴分散式新皮質迴路的重組過程。
- **重播**：清醒經驗中出現的神經序列，在休息或睡眠時再次出現。
- **尖波漣波**：海馬迴中短暫的高頻活動爆發，常見於安靜休息與慢波睡眠，重播即在此時表現出來。
- **慢波睡眠（SWS）**：最深的非 REM 睡眠階段，以大而慢的皮質振盪為特徵。
- **REM 睡眠**：快速眼動與類似夢境活動的階段。其在記憶中的角色，不如慢波睡眠那樣確定。

## 運作方式

睡眠會在非 REM 各階段（包括慢波睡眠）與 REM 睡眠之間循環。慢波睡眠多集中在夜晚前半段。一個廣被討論的兩階段說法認為，慢波睡眠中的再活化會轉化並整合近期記憶，之後 REM 睡眠可能穩定經過轉化的記憶（Rasch & Born, 2013）。

在慢波睡眠期間，海馬迴會產生尖波漣波，而重播就在這些漣波中表現。在人類中，睡眠時於海馬迴記錄到的漣波，巢狀地位於睡眠紡錘波之中，而紡錘波又巢狀地位於慢振盪之中（Staresina 等人，2015）。這種巢狀結構，是對鞏固期間海馬迴與皮質如何協調的一種解釋。

```mermaid
flowchart LR
  W[清醒經驗] --> E[海馬迴中編碼]
  E --> SWS[慢波睡眠：漣波重播近期序列]
  SWS --> CTX[皮質：慢振盪與紡錘波協調轉移]
  CTX --> REM[REM 睡眠：可能穩定轉化後的記憶]
  REM --> L[長期皮質儲存]
```

重播在時間上是壓縮的：一段行為序列可能以濃縮的形式再次出現（Buzsáki, 2015）。重播也可以反向進行（Foster & Wilson, 2006）。在同一批漣波中，有些重播是正向的，有些則是反向的（Diba & Buzsáki, 2007）。

並非所有關於睡眠的解釋，都讓重播居於中心。突觸穩態假說提出，睡眠會降低整體突觸強度，從而避免學習使網路飽和。[^1] 兩種想法不一定互斥，但學界尚未決定它們如何互相配合。

## 關鍵方法

每個方法都有自己的頁面，此處只作比較。

| 方法 | 區別所在 | 頁面 |
|---|---|---|
| 海馬迴重播（Wilson 與 McNaughton，1994） | 在任務與睡眠期間記錄位置細胞的神經元集合，發現清醒時的共同放電模式會在睡眠中重現 | [海馬迴重播](hippocampal-replay/index.md) |
| 目標式記憶再活化（Rasch 等人，2007） | 在學習期間出現的線索，於睡眠中再次呈現，以檢驗再活化是否導致鞏固 | [目標式記憶再活化](targeted-memory-reactivation/index.md) |

## 與其他主題的關聯

- **記憶與學習**：失憶症的證據、突觸可塑性，以及海馬迴與皮質的分工，見於[記憶與學習的神經機制](../memory-learning/index.md)；系統層次的理論見於[互補學習系統](../memory-learning/complementary-learning-systems/index.md)。本頁建立在這兩者之上，不重複其內容。
- **規劃與決策**：Mattar 與 Daw（2018）把重播與規劃連結起來，因此重播也是決策的一部分。見[決策、多巴胺與獎勵](../decision-reward/index.md)。
- **AI 的對應概念**：在深度強化學習中，會重播儲存的過去轉移以訓練代理人。這就是[經驗回放](../../theory/paradigms/reinforcement-learning/experience-replay/index.md)所描述的 AI 對應概念；持續學習的觀點見[基於重播與記憶的持續學習](../../theory/paradigms/continual/replay-and-memory/index.md)。

## 應用

- **強化學習**：重播儲存的轉移，可以穩定以價值為基礎的代理人的訓練。Mnih 等人（2015）以帶有重播記憶的深度 Q 網路學習 Atari 遊戲；Fedus 等人（2020）則研究重播容量與重播比例如何影響效能。
- **持續學習**：災難性干擾（McCloskey & Cohen, 1989）是重播所針對之問題的人工版本。Shin 等人（2017）借鏡海馬迴，提出生成式重播，由生成模型提供早期任務的樣本。Kirkpatrick 等人（2016）則減緩對早期任務重要權重的學習，這是受突觸鞏固啟發的正則化方法。見[持續學習](../../theory/paradigms/continual/index.md)。
- **研究工具**：目標式記憶再活化讓實驗者能檢驗某段記憶是否在睡眠中被再活化，這是一種因果檢驗（Rasch 等人，2007）。
- **臨床神經科學**：Buzsáki（2015）指出，稱為 p 型漣波的病理性漣波，被視為癲癇組織的標記。

## 開放問題

- **重播是否具有因果作用？** 線索實驗與漣波干擾實驗都顯示重播對記憶有影響，但某一特定重播模式與某段特定儲存記憶之間的連結，仍在檢驗中。
- **什麼決定哪些經驗會被重播？** Mattar 與 Daw（2018）主張，與規劃相關的優先記憶存取，可以解釋海馬迴重播的模式。優先順序的規則仍是懸而未決的問題。
- **突觸縮減的角色為何？** 突觸穩態假說與鞏固說做出不同的預測，目前不清楚兩者是否都描述睡眠的功能。
- **AI 的類比能走多遠？** Kumaran 等人（2016）主張，重播與互補系統對代理人而言是有用的概念。深度強化學習中的重播通常採用固定排程，缺少大腦那種類似睡眠的結構。
- **多少證據來自人類？** 最詳細的重播證據來自齧齒類動物，人類的記錄較為稀少。見 Staresina 等人（2015）。

[^1]: Tononi 與 Cirelli（2006）提出，清醒時突觸強度平均上升，睡眠時則再次降低。此假說只是關於睡眠功能的數種解釋之一，其證據仍有爭議。

## 參考文獻

### 開創性論文

- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of Hippocampal Ensemble Memories During Sleep. *Science*. https://doi.org/10.1126/science.8036517 — 記錄空間任務與睡眠期間的位置細胞神經元集合，並顯示清醒時的共同放電模式會在之後的睡眠中重現。
- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature*. https://doi.org/10.1038/nature04587 — 報告跑步時的位置細胞序列，在清醒狀態下以反向順序重播，使重播超越睡眠的範圍。
- Diba, K. & Buzsáki, G. (2007). Forward and reverse hippocampal place-cell sequences during ripples. *Nature Neuroscience*. https://doi.org/10.1038/nn1961 — 報告在尖波漣波期間重播的位置細胞序列，同時有正向與反向兩種。
- Ji, D. & Wilson, M. A. (2006). Coordinated memory replay in the visual cortex and hippocampus during sleep. *Nature Neuroscience*. https://doi.org/10.1038/nn1825 — 報告睡眠期間的重播，在視覺皮質與海馬迴之間是協調進行的。
- Rasch, B., Büchel, C., Gais, S. & Born, J. (2007). Odor Cues During Slow-Wave Sleep Prompt Declarative Memory Consolidation. *Science*. https://doi.org/10.1126/science.1138581 — 顯示在慢波睡眠時再次呈現學習時的氣味，能改善陳述性記憶的保留。
- McCloskey, M. & Cohen, N. J. (1989). Catastrophic Interference in Connectionist Networks: The Sequential Learning Problem. *Psychology of Learning and Motivation*. https://doi.org/10.1016/S0079-7421(08)60536-8 — 指出災難性干擾：在連結主義網路中，學習新項目會覆寫先前的學習。
- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement learning, planning and teaching. *Machine Learning*. https://doi.org/10.1007/BF00992699 — 早期結合強化學習與儲存經驗重播的研究，是經驗回放的先驅。
- Mnih, V. 等人 (2015). Human-level control through deep reinforcement learning. *Nature*. https://doi.org/10.1038/nature14236 — 提出深度 Q 網路，以重播過去轉移的記憶，從像素學習 Atari 遊戲。
- Staresina, B. P. 等人 (2015). Hierarchical nesting of slow oscillations, spindles and ripples in the human hippocampus during sleep. *Nature Neuroscience*. https://doi.org/10.1038/nn.4119 — 報告人類睡眠時在海馬迴記錄到的漣波，巢狀地位於紡錘波與慢振盪之中。
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience*. https://doi.org/10.1038/s41593-018-0232-z — 提出與規劃相關的優先記憶存取，可以解釋海馬迴重播的模式。
- Shin, H. 等人 (2017). Continual Learning with Deep Generative Replay. arXiv. https://arxiv.org/abs/1705.08690 — 提出生成式重播：由生成模型提供早期任務的樣本，與新的訓練交錯進行。
- Kirkpatrick, J. 等人 (2016). Overcoming catastrophic forgetting in neural networks. arXiv. https://arxiv.org/abs/1612.00796 — 提出彈性權重鞏固，減緩對早期任務重要權重的學習。
- Fedus, W. 等人 (2020). Revisiting Fundamentals of Experience Replay. arXiv. https://arxiv.org/abs/2007.06700 — 研究重播容量與重播比例如何影響 Q 學習方法。

### 綜述與教科書

- Diekelmann, S. & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2762 — 綜述睡眠對記憶處理有所貢獻的證據，以及不同睡眠階段如何發揮作用。
- Walker, M. P. & Stickgold, R. (2004). Sleep-Dependent Learning and Memory Consolidation. *Neuron*. https://doi.org/10.1016/j.neuron.2004.08.031 — 綜述學習後的睡眠如何支持人類的記憶鞏固。
- Born, J. & Wilhelm, I. (2011). System consolidation of memory during sleep. *Psychological Research*. https://doi.org/10.1007/s00426-011-0335-6 — 綜述睡眠如何推動系統鞏固，即記憶在不同腦系統之間的逐步轉移。
- Rasch, B. & Born, J. (2013). About Sleep's Role in Memory. *Physiological Reviews*. https://doi.org/10.1152/physrev.00032.2012 — 綜述慢波睡眠的再活化如何推動鞏固，以及 REM 睡眠可能如何穩定記憶。
- Buzsáki, G. (2015). Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus*. https://doi.org/10.1002/hipo.22488 — 綜述尖波漣波作為壓縮重播的場域，以及干擾漣波會損害記憶的證據。
- Kumaran, D., Hassabis, D. & McClelland, J. L. (2016). What learning systems do intelligent agents need? Complementary learning systems theory updated. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2016.05.004 — 在深度學習與重播的脈絡下重新檢視互補學習系統理論。
- Squire, L. R. & Alvarez, P. (1995). Retrograde amnesia and memory consolidation: a neurobiological perspective. *Current Opinion in Neurobiology*. https://doi.org/10.1016/0959-4388(95)80023-9 — 綜述逆行性失憶，作為記憶會經歷隨時間逐步鞏固的證據。
- Frankland, P. W. & Bontempi, B. (2005). The organization of recent and remote memories. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1607 — 綜述近期與遠期記憶在腦中如何組織，以及它們的儲存如何隨時間改變。
- Tononi, G. & Cirelli, C. (2006). Sleep function and synaptic homeostasis. *Sleep Medicine Reviews*. https://doi.org/10.1016/j.smrv.2005.05.002 — 提出睡眠會降低整體突觸強度，這是關於睡眠功能的假說，至今仍有爭議。
