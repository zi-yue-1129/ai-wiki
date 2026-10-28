---
translation_reviewed: 2026-10-28
tags:
- neuroscience
- neural oscillations
- memory
aliases:
  - θ–γ 耦合
  - Theta-gamma coupling
  - Theta–gamma neural code
  - Phase-amplitude coupling
  - PAC
---

# θ–γ 耦合（Lisman & Jensen, 2013）

θ–γ 耦合是一種模式：慢速 theta 節律的相位調變快速 gamma 節律的振幅。在人類皮質記錄中，theta 通常取為約 4 至 8 Hz，高 gamma 約為 80 至 150 Hz。Lisman 與 Jensen（2013）主張，這種巢狀結構構成一種神經編碼：各個項目佔據每個 theta 週期內連續的 gamma 爆發。這個想法與記憶關係最為密切，尤其是海馬迴中的記憶。本頁是[神經振盪與同步](../index.md)的一部分。

## 問題

人在短期記憶中一次只能保留少量項目。心理物理學測量將這個數字定在約七個（Lisman & Idiart, 1995）。問題在於，一個神經網路如何在同一時間把數個項目彼此區分開來，而每個項目都由共享群體中的活動所表徵。若每個項目都以相同方式持續發放，它們就會彼此干擾。

## 核心想法

Lisman 與 Idiart（1995）主張，每個項目被指派到一個不同的快速 gamma 子週期。子週期在每個慢 theta 週期內重複出現，因此這些項目在每個 theta 週期內形成一個有順序的序列。這種模式在每個 theta 週期重複，而重複依賴的是神經元興奮性的改變，而非持續的迴路回響。

後來在人類身上的記錄直接顯示了這種耦合。Canolty et al.（2006）發現，在皮質電圖（ECoG）中，theta 的相位調變高 gamma 的功率，且在較高的 theta 振幅下調變較強。不同的行為任務會在皮質上產生不同的耦合模式。Lisman 與 Jensen（2013）把這個提議發展為更廣的 θ–γ 神經編碼：一個 theta 週期內的 gamma 子週期承載項目的有序序列。他們的回顧發現，這種編碼在海馬迴中最為清楚，其中不同的空間資訊佔據不同的 gamma 子週期。

## 方程式或演算法

測量耦合是一套程序。Tort et al.（2010）描述了一種常見的做法：

1. 把訊號濾波成慢頻段（theta）與快頻段（gamma）。
2. 在每個時間點，取出慢頻段的相位與快頻段的振幅包絡。
3. 依慢頻段的相位把振幅值分入各個區間（bin），並計算每個區間內振幅的平均。
4. 使用以 Kullback–Leibler 為基礎的指標，衡量所得的振幅分布偏離均勻分布的程度。分布平坦代表沒有耦合；分布有明顯的峰值則代表振幅取決於相位。
5. 將數值與經控制分析產生的替代資料（surrogate data）比較，以確認耦合強於隨機水準。

## 結果

- **模型（Lisman & Idiart, 1995）。** 在模擬網路中，模型產生了巢狀振盪：低頻節律為 5 至 12 Hz，高頻子週期接近 40 Hz。每個記憶儲存於不同的子週期中，而且模式在每個慢週期中重複。這是模型的結果，而非記錄的結果。
- **海馬迴的位置編碼（Lisman, 2005）。** Lisman 主張，theta 與 gamma 振盪構成一種編碼方式，用於讀取海馬迴中的位置序列。連續的位置被編碼在一個 theta 週期內連續的 gamma 子週期中，多種解碼分析顯示 theta 相位承載了關於動物位置的資訊。
- **人類記錄（Canolty et al., 2006）。** 在 ECoG 中，theta 相位調變高 gamma 功率。作者把這種耦合解釋為協調分散皮質區活動的方式。
- **測量方法（Tort et al., 2010）。** 作者把他們的指標與另外七種跨頻耦合測量比較，並報告它在部分效能基準上特別具有吸引力。

## 限制

- **模型與資料。** 「項目位於 gamma 子週期」的理論來自網路模型。最清楚的海馬迴證據（Lisman & Jensen, 2013）主要涉及空間資訊，因此把這種編碼推廣到其他類型的記憶內容，是一種推論。
- **耦合尚不等於編碼。** 顯示 gamma 振幅取決於 theta 相位，並不表示該相位攜帶特定項目的資訊。要解碼每個子週期的內容，需要進一步的分析。
- **測量的選擇。** 耦合估計取決於濾波設定、時段長度與所用的控制。Tort et al.（2010）討論了時段長度與替代資料控制分析等技術面向。
- **樣本。** 這裡引用的人類證據來自 ECoG，它記錄的是皮質表面，只涵蓋電極放置的部位，這限制了結果在不同腦區間的推廣程度。

## 連結

- **記憶。** 海馬迴是 θ–γ 編碼最清楚被證明的部位（Lisman & Jensen, 2013），見[記憶與學習](../../memory-learning/index.md)。
- **溝通。** [透過相干性的通訊](../communication-through-coherence/index.md)是本章另一個以節律為基礎的說法。相干性關注群體之間的溝通，θ–γ 耦合關注單一迴路如何組織自己的項目。
- **記錄。** 人類研究中使用的 ECoG 與局部場電位訊號，說明見[神經影像與記錄方法](../../neuroimaging-methods/index.md)。
- **人工網路。** 基於相位的編碼已在脈衝神經網路中研究，其中每個脈衝相對於振盪的時間攜帶資訊。見[脈衝神經網路與神經形態運算](../../snn-neuromorphic/index.md)。標準人工網路使用連續的激活值而非脈衝，因此沒有與子週期編碼直接對應的部分。兩者的連結是概念上的：兩者都利用一個週期內活動的順序，把項目彼此分開。

## 應用

- **人類任務研究。** 顱內記錄可以顯示 θ–γ 耦合如何隨行為任務改變，正如 Canolty et al.（2006）所做的。
- **耦合測量。** Tort et al.（2010）的指標是量化不同腦區記錄中相位–振幅耦合的可用測量之一。

## 開放問題

- θ–γ 編碼是否攜帶特定內容？下游腦區如何讀取每個子週期的相位？
- 一個 theta 週期內可容納多少個 gamma 子週期？這個數字是否因物種與腦區而異？
- 能否以因果方式檢驗耦合，亦即操控 theta 節律並檢查其對記憶的影響？

## 參考文獻

### 開創性論文

- Lisman, J. E. & Idiart, M. A. P.（1995）。Storage of 7 ± 2 short-term memories in oscillatory subcycles. *Science*。https://doi.org/10.1126/science.7878473 — 最初的 θ–γ 記憶模型：慢週期內連續的 gamma 子週期中各自儲存不同的項目。
- Lisman, J.（2005）。The theta/gamma discrete phase code occurring during the hippocampal phase precession may be a more general brain coding scheme. *Hippocampus*。https://doi.org/10.1002/hipo.20121 — 主張 theta 與 gamma 構成海馬迴中位置序列的相位編碼，並有相位進動與解碼分析的支持。
- Canolty, R. T. et al.（2006）。High gamma power is phase-locked to theta oscillations in human neocortex. *Science*。https://doi.org/10.1126/science.1128115 — 人類 ECoG 證據，顯示 theta 相位調變高 gamma 功率。
- Tort, A. B. L., Komorowski, R., Eichenbaum, H. & Kopell, N.（2010）。Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. *Journal of Neurophysiology*。https://doi.org/10.1152/jn.00106.2010 — 以 Kullback–Leibler 為基礎的相位–振幅耦合指標，並與另外七種測量比較。

### 綜述與教科書

- Lisman, J. E. & Jensen, O.（2013）。The theta–gamma neural code. *Neuron*。https://doi.org/10.1016/j.neuron.2013.03.007 — 發展 θ–γ 編碼假說並回顧其證據的綜述。
- Lisman, J. & Buzsáki, G.（2008）。A neural coding scheme formed by the combined function of gamma and theta oscillations. *Schizophrenia Bulletin*。https://doi.org/10.1093/schbul/sbn060 — 回顧 theta 與 gamma 振盪共同作為神經編碼的證據，並討論其與精神分裂症可能的關聯。
