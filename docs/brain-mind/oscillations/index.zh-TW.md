---
translation_reviewed: 2026-10-28
related:
- theory/models/rnn
tags:
- neuroscience
- neural oscillations
- synchrony
aliases:
  - 神經振盪與同步
  - 神經振盪
  - 腦波振盪
  - Neural Oscillations
  - Brain Oscillations
  - Neural Synchrony
---

# 神經振盪與同步

大腦中的神經元群常會產生節律：它們的集體活動以規律的頻率起伏。同步（synchrony）指的是神經元或腦區之間時間上的對齊。兩者被提出作為大腦組織時序、溝通與記憶的一種方式。它們在人工網路中的對應物，遠不如其他神經科學與 AI 的連結那樣直接。

## 概述

神經振盪是一群神經元活動的節律性變化。研究者在群體層級的訊號中觀察到它，例如反映許多細胞突觸活動的[局部場電位](../neuroimaging-methods/index.md)，以及頭皮腦電圖（EEG）。單一神經元的脈衝本身並不是節律，但當許多神經元在相近的相位發放時，群體訊號就會振盪。

振盪出現的頻率範圍非常寬廣。Buzsáki 與 Draguhn（2004）描述它們橫跨五個數量級，並主張它們在不同物種間被保留下來，顯示其具有功能，而非網路活動的副產品。他們把近期的發現連結到三種作用：決定哪些輸入被選取、把神經元在時間上串連成集合（assembly），以及促進突觸可塑性。

## 核心概念

- **頻段。** 振盪通常依頻段分類。常用的名稱有 delta、theta、alpha、beta 與 gamma，但各研究對邊界的定義不同。本章使用的兩個範圍來自特定研究：在人類皮質記錄中，theta 為 4 至 8 Hz，高 gamma 為 80 至 150 Hz（Canolty et al., 2006）。
- **相位。** 相位是訊號在其週期中所處的位置。資訊可以由脈衝在週期中出現的時刻來攜帶，而不只是由脈衝的數量。Lisman 與 Idiart（1995）提出，短期記憶中的各個項目各自佔據巢狀於慢週期之中的不同快速子週期，因此快節律的相位能將它們區分開來。
- **相干性。** 相干性描述兩個節律之間隨時間保持穩定的相位關係。Womelsdorf et al.（2007）發現，兩個神經元群彼此影響的強度取決於它們節律之間的相位關係，而且這些相位關係比互動早了數毫秒出現。
- **跨頻耦合。** 快節律的振幅可以取決於慢節律的相位。這是 theta–gamma 耦合的基礎，而後者與記憶有關。

## 關鍵方法

- [透過相干性的通訊（Fries, 2005）](communication-through-coherence/index.md)：主張各腦區之間的相干性控制它們訊號溝通的效力。它關注的是腦區之間的溝通。
- [θ–γ 耦合（Lisman & Jensen, 2013）](theta-gamma-coupling/index.md)：主張慢 theta 節律的相位組織快速 gamma 爆發，形成迴路內部的編碼方式。它關注的是單一迴路如何組織項目，主要應用於記憶。

## 連結

- **記憶。** [記憶與學習](../memory-learning/index.md)中與記憶相關的想法，核心在於海馬迴中的 theta 與 gamma 節律。該頁提到的睡眠節律，如慢振盪、紡錘波與漣波，也屬於同一類想法。
- **記錄。** 群體節律以 [LFP、ECoG 與 EEG](../neuroimaging-methods/index.md) 測量，它們看見的是神經元群而非單一細胞。解讀時需要謹慎，因為加總訊號中的節律無法揭示是哪些神經元產生的。
- **計算模型。** 耦合振盪器與脈衝神經網路模型研究這類節律如何產生。參見[計算神經科學](../computational-neuroscience/index.md)與[脈衝神經網路與神經形態運算](../snn-neuromorphic/index.md)，後者把相位編碼列為其中一種編碼方式。
- **人工網路。** 標準人工網路沒有膜電位、脈衝或自身的節律，因此振盪在其中沒有直接對應物。有一種架構直接採用了這個想法：耦合振盪循環神經網路（coRNN）把其隱藏狀態視為一組耦合非線性振盪器的輸出，並在時間上離散化（Rusch & Mishra, 2020）。作者證明了隱藏狀態梯度的界限，從而緩解梯度爆炸與消失的問題，並報告其在多項基準測試上的表現與當前最佳方法相當。這個類比屬於架構層面：它說明振盪器動力學可以作為循環式運算，但並不表示經過訓練的網路會發展出類似大腦的 theta 或 gamma 節律，也不表示兩個系統中的這些節律做的是同一件事。參見[循環神經網路](../../theory/models/rnn/index.md)。

## 應用

- **腦機介面。** 解碼大腦訊號以控制裝置的內容，見[腦機介面](../bci/index.md)頁。上述的群體層級記錄，是其輸入訊號之一。
- **睡眠與記憶。** 上文「連結」中提到的睡眠節律（慢振盪、紡錘波與漣波），在[記憶與學習](../memory-learning/index.md)頁中作為記憶的脈絡加以討論。
- **序列建模。** coRNN 架構是以振盪器方程式建構序列模型的例子，其論文報告了基準測試結果。

## 開放問題

- **因果性。** 振盪是造成腦區之間的溝通，還是只是伴隨溝通而出現？要回答這個問題，需要直接操控節律的實驗，而這在人類身上較為困難。
- **頻段的專一性。** 各頻段在功能上是否有明確區分，還是形成連續的譜？許多研究中，頻段的邊界是依慣例劃定的。
- **解讀編碼。** 相位編碼已在模型以及部分記錄中被觀察到。下游腦區是否真的解碼相位，目前仍不清楚。
- **在 AI 中的應用。** 振盪器架構除了其測試過的基準之外，是否還有其他好處，仍有待研究。

## 參考文獻

### 開創性論文

- Singer, W. & Gray, C. M.（1995）。Visual feature integration and the temporal correlation hypothesis. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.ne.18.030195.003011 — 關於視覺特徵如何被整合的時間相關性假說的回顧。
- Lisman, J. E. & Idiart, M. A. P.（1995）。Storage of 7 ± 2 short-term memories in oscillatory subcycles. *Science*。https://doi.org/10.1126/science.7878473 — 一個網路模型，其中記憶項目佔據慢 theta 週期內連續的 gamma 子週期。
- Fries, P.（2005）。A mechanism for cognitive dynamics: neuronal communication through neuronal coherence. *Trends in Cognitive Sciences*。https://doi.org/10.1016/j.tics.2005.08.011 — 最初提出神經元相干性是神經元群之間溝通機制的論文。

### 綜述與教科書

- Buzsáki, G. & Draguhn, A.（2004）。Neuronal oscillations in cortical networks. *Science*。https://doi.org/10.1126/science.1099745 — 皮質網路中振盪的綜述，涵蓋其頻率範圍與所被提出的功能。
- Fries, P.（2015）。Rhythms for cognition: communication through coherence. *Neuron*。https://doi.org/10.1016/j.neuron.2015.09.034 — 由該假說的提出者撰寫的回顧，論述 gamma 頻段的同步如何塑造群體之間的溝通，以及注意力如何作用於其上。
- Buzsáki, G.（2006）。*Rhythms of the Brain*。Oxford University Press。https://doi.org/10.1093/acprof:oso/9780195301069.001.0001 — 關於腦節律的專書，內容比上述綜述更深入。

### 文章與文件

- Rusch, T. K. & Mishra, S.（2020）。Coupled Oscillatory Recurrent Neural Network (coRNN): An accurate and (gradient) stable architecture for learning long time dependencies. arXiv:2010.00951。https://arxiv.org/abs/2010.00951 — 由耦合非線性振盪器建構的循環架構，隱藏狀態的梯度有界，並有基準測試結果。
