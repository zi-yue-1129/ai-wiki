---
translation_reviewed: 2026-10-28
tags:
- neuroscience
- neural oscillations
- synchrony
aliases:
  - 透過相干性的通訊
  - Communication through Coherence
  - CTC
  - Neuronal coherence
---

# 透過相干性的通訊（Fries, 2005）

透過相干性的通訊是 Pascal Fries 於 2005 年提出的假說。它主張，從一群神經元送往另一群神經元的訊號是否有效，取決於兩者的節律活動是否相干，也就是兩個節律之間的相位關係是否隨時間保持穩定。這是把神經振盪與認知連結起來的主要提議之一。本頁是[神經振盪與同步](../index.md)的一部分。

## 問題

兩個腦區之間可以有高度密集的連結，但接收端的腦區同時受到許多輸入的驅動。哪些訊號能通過、哪些被忽略，是由什麼決定的？解剖上的連接在學習的時間尺度上是固定的，但選擇必須能隨時間變化。問題在於，什麼樣的動態機制能讓既有連結的效果開啟或關閉。

## 核心想法

Fries（2005）主張神經元之間的溝通是經由神經元的相干性進行的，因此相干性的彈性模式定義了彈性的溝通結構。同一作者後來的綜述（Fries, 2015）更具體地描述 gamma 頻段的同步如何塑造一個群體到下一個群體的訊號傳遞，以及注意力如何作用於它。由於相位關係會改變，同一條解剖連結在不同時間可以攜帶不同的訊號。

## 方程式或演算法

這個方法是一套測量程序，而不是單一的方程式：

1. 記錄兩個訊號，例如兩個位點或兩個電極上的局部場電位。
2. 把兩個訊號濾波到感興趣的頻段，並在每個時間點取出各自的相位。
3. 由相位差計算相干性：一個經過正規化的量，當相位差在時間或重複試驗中保持一致時，數值較大。
4. 比較不同條件下的相干性，例如受注意與未受注意的刺激，以檢驗耦合是否隨任務改變。

## 結果

Womelsdorf et al.（2007）提供神經記錄，直接檢驗這套說法，考察神經元群之間的互動是否取決於其節律活動的同步。標題陳述了此主張：神經元互動是透過神經元同步來調變的。完整結果見原文，本頁不引用其圖表數字。

Bosman et al.（2012）在猴子的視覺皮質上檢驗了注意的面向，測試視覺區域之間的選擇性同步。標題陳述了此主張：猴子視覺區域之間的選擇性同步實現注意的刺激選擇。本頁不引用論文的數值結果。

這些證據大多屬於相關性的，因此支持了這個假說，但尚未完全確立它。

## 限制

- **相關不等於因果。** 兩個群體可能因為共享同一輸入而變得相干，而兩者之間並無直接影響。要證明相干性會改變溝通，必須操控節律本身。
- **分析的選擇很重要。** 相干性取決於頻段、視窗長度與參考訊號的選擇。報告的效果可能因這些決定而不同，因此比較不同研究時需要謹慎。
- **哪個頻段？** 這個假說是一個框架，而不是針對某個固定頻率的主張。gamma 是否為腦區之間溝通的正確頻段，以及它在不同腦區與任務中是否不同，仍有爭議。

## 連結

- **θ–γ 耦合。** [θ–γ 耦合](../theta-gamma-coupling/index.md)是本章另一個以節律為基礎的方法。兩者的範圍不同：相干性關注群體之間的溝通，θ–γ 耦合關注單一迴路如何組織自己的項目。
- **注意力。** 相干性被提出作為選擇性注意的機制（Fries, 2015）。這個主題也是 wiki 中[注意力：腦與機器](../../attention-brain-machine/index.md)頁的主要內容之一。
- **記錄。** 相干性由局部場電位、ECoG 與 EEG 訊號計算，這些訊號的說明見[神經影像與記錄方法](../../neuroimaging-methods/index.md)。
- **人工網路。** 標準人工網路沒有相位，因此這個想法沒有直接的對應物。最接近的類比是注意力機制中的閘控，它依學得的權重而非時間來選擇資訊。這只是概念上的粗略連結，並不表示兩者的運作方式相同。

## 應用

- **研究神經溝通。** 這個框架提出可檢驗的預測：改變兩個腦區之間的相位關係，應當會改變它們的互動。因此它是研究注意力與知覺的研究工具，使用上述的訊號。

## 開放問題

- 相位對齊是溝通的機制，還是與溝通一同出現的讀數？
- 哪些頻段在哪些腦區之間承載溝通，並且如何隨任務改變？
- 相干性能否從有雜訊的人類記錄中可靠地估計，而估計值對分析選擇的依賴程度又有多大？

## 參考文獻

### 開創性論文

- Fries, P.（2005）。A mechanism for cognitive dynamics: neuronal communication through neuronal coherence. *Trends in Cognitive Sciences*, 9(10), 474–480。https://doi.org/10.1016/j.tics.2005.08.011 — 最初的提議，把神經元群之間的相干性命名為溝通的機制。
- Womelsdorf, T., Schoffelen, J.-M., Oostenveld, R., Singer, W., et al.（2007）。Modulation of neuronal interactions through neuronal synchronization. *Science*, 316(5831), 1609–1612。https://doi.org/10.1126/science.1139597 — 神經記錄，檢驗神經元群之間的互動是否取決於其節律的同步。
- Bosman, C., Schoffelen, J.-M., Brunet, N., Oostenveld, R., et al.（2012）。Attentional stimulus selection through selective synchronization between monkey visual areas. *Neuron*, 75(5), 875–888。https://doi.org/10.1016/j.neuron.2012.06.037 — 猴子的記錄，檢驗視覺區域之間的選擇性同步作為注意刺激選擇的機制。

### 綜述與教科書

- Fries, P.（2015）。Rhythms for cognition: communication through coherence. *Neuron*。https://doi.org/10.1016/j.neuron.2015.09.034 — 由該假說的提出者撰寫的回顧，論述 gamma 頻段的同步如何塑造群體之間的溝通，以及注意力如何作用於其上。
- Fries, P.（2009）。Neuronal gamma-band synchronization as a fundamental process in cortical computation. *Annual Review of Neuroscience*, 32, 209–224。https://doi.org/10.1146/annurev.neuro.051508.135603 — 主張 gamma 頻段的同步是皮質運算的基本過程。
