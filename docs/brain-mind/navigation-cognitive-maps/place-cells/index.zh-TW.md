---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- navigation
- memory
aliases:
  - 位置細胞
  - Place cells
  - Place cell
  - 認知地圖假說
---

# 位置細胞與認知地圖假說（O'Keefe 與 Dostrovsky，1971）

位置細胞是海馬迴中的神經元，當動物位於環境中某個特定部分時會強烈放電。O'Keefe 與 Dostrovsky（1971）在自由移動的大鼠身上做了單一單元記錄，並提出海馬迴保有一張空間地圖。這為 Tolman 的認知地圖概念提供了神經層面的一種對應。

本頁屬於[空間導航與認知地圖](../index.md)。它詳細說明一種方法。更廣的圖像，包括頭部方向細胞與格狀單元，見該頁。

## 概述

想像你走過一個房間。有些海馬迴神經元只有在你站在某個位置時才活躍，而每個神經元的位置都不同。這些神經元合起來，就能告訴大腦動物在哪裡，而這些資訊可用來規劃路線。1971 年的論文報告了一隻自由移動的大鼠在環境中的單元活動，其標題提出海馬迴是一張空間地圖。

## 關鍵概念

- **位置場**：位置細胞放電的環境區域。
- **空間地圖**：群體活動追蹤動物所在位置的表徵。
- **認知地圖**：Tolman（1948）用來描述環境類地圖表徵的詞，用於彈性行為，例如找到新路線。
- **重映射**：環境改變時，哪些位置細胞放電、以及在何處放電的改變。

## 問題

到 1970 年代初，海馬迴已與記憶和行為相連，但問題在於它的活動是否攜帶空間資訊。若是，海馬迴就可能是認知地圖的神經基礎。1971 年的論文以自由移動大鼠的單一單元記錄來探討此問題。

## 核心想法

1971 年論文的標題點出了這個主張：海馬迴是一張空間地圖，並以自由移動大鼠的初步單元活動為依據。這個主張與 Tolman（1948）的認知地圖概念相連。若許多單元各自對不同位置有調諧，它們合起來就能編碼動物的位置並支持導航。這個想法談的是群體編碼：一整組神經元，各自與自己的位置相連，共同承載空間資訊。

## 方程式或演算法

一個常見的簡化模型，把位置細胞的放電率描述為以偏好位置 \(c\) 為中心的高斯峰：

\(f(x) = r_{\max} \exp\left(-\frac{\lVert x - c \rVert^{2}}{2\sigma^{2}}\right)\)

其中 \(x\) 為動物的位置，\(r_{\max}\) 為峰值放電率，\(\sigma\) 決定位置場的寬度。這是建模中使用的簡化描述。真實的位置場形狀與大小各不相同，而原始觀察應以論文本身為準。

## 結果

O'Keefe 與 Dostrovsky（1971）在自由移動的大鼠身上提出初步證據，來自單一單元的活動，以支持海馬迴是空間地圖的主張。此報告屬初步性質，其主張僅限於作者所研究的細胞與環境。

後來的研究為地圖概念加入兩點。位置細胞是一個更廣迴路的一部分，此迴路還包括內嗅皮質中的第二群體，即格狀單元（Moser 等人，2008）。格狀單元見[格狀單元頁面](../../neuroai/grid-like-units/index.md)。此外，海馬迴可能把空間表徵為預測地圖，而非單純的位置編碼（Stachenfeld 等人，2017）。

## 限制

- **初步報告。** 1971 年的論文是早期的初步報告，其主張僅限於它所描述的動物與環境。後來的研究更廣泛地檢驗這些主張。
- **位置不是全部。** 位置細胞可能攜帶位置以外的資訊，後來的模型也納入了類地標與其他非空間訊號。[Tolman–Eichenbaum 機器](../tolman-eichenbaum-machine/index.md)提出了這樣的模型（Whittington 等人，2020）。
- **穩定性與重映射。** 位置場為何穩定或改變，是模型比較的一部分。TEM 模型預測重映射是有結構的，而非隨機。

## 關聯

- **認知地圖**：位置細胞是認知地圖最知名的神經候選。見[空間導航與認知地圖](../index.md)。
- **後繼表徵**：海馬迴中的預測地圖可被讀為空間上的 SR。見[後繼表徵](../successor-representation/index.md)。
- **記憶**：位置細胞在休息與睡眠時重播近期經驗，把空間編碼與記憶連在一起。見[記憶與學習的神經機制](../../memory-learning/index.md)。
- **AI**：位置細胞式的地圖啟發了關於智慧體學習得來的世界模型的討論。見[世界模型與具身智慧](../../../theory/models/world-models/index.md)。

## 應用

- **導航的神經科學**：位置細胞是研究海馬迴如何表徵空間的參考點。
- **預測地圖**：Stachenfeld 等人（2017）以預測地圖的觀點，把位置細胞與強化學習連在一起。與規劃以及[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)的連結，也在該處討論。

## 未解問題

- **什麼驅動位置場？** 位置場有多少來自地標、自身移動或內部狀態，仍有爭議。
- **地圖還是預測地圖？** 位置細胞編碼的是位置本身，還是由此預期的未來狀態，仍是開放問題（Stachenfeld 等人，2017）。
- **地圖如何被使用？** 位置細胞提供空間編碼，但這個編碼如何支持規劃與新路線，仍在研究中（Behrens 等人，2018）。

## 參考文獻

### 開創性論文

- O'Keefe, J. 與 Dostrovsky, J.（1971）。The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat。*Brain Research*。https://doi.org/10.1016/0006-8993(71)90358-1 — 以自由移動大鼠的單元活動提供初步證據，其標題提出海馬迴是一張空間地圖。
- Tolman, E. C.（1948）。Cognitive maps in rats and men。*Psychological Review*。https://doi.org/10.1037/h0061626 — 在一篇關於大鼠與人的論文中提出「認知地圖」一詞，是後來位置細胞研究所承接的想法。
- Stachenfeld, K. L.、Botvinick, M. M. 與 Gershman, S. J.（2017）。The hippocampus as a predictive map。*Nature Neuroscience*。https://doi.org/10.1038/nn.4650 — 借鏡強化學習，提出海馬迴位置細胞攜帶的是預測地圖，而非純粹的空間地圖。

### 綜述與教科書

- Behrens, T. E. J. 等人（2018）。What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior。*Neuron*。https://doi.org/10.1016/j.neuron.2018.10.002 — 回顧認知地圖的證據，認為空間中看到的類地圖表徵，可能是組織各種知識的一般機制的一例。
- Moser, E. I.、Kropff, E. 與 Moser, M.-B.（2008）。Place Cells, Grid Cells, and the Brain's Spatial Representation System。*Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.neuro.31.061307.090723 — 回顧位置細胞與格狀細胞作為同一迴路的一部分，如何在行為與記憶中表徵地點與路線。
