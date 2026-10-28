---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/neuroai
tags:
- neuroscience
- attention
aliases:
  - Desimone 與 Duncan 1995
  - 偏向競爭
  - 偏向競爭模型
---

# 偏向競爭（Desimone 與 Duncan，1995）

Desimone 與 Duncan（1995）提出，同一感受野內的刺激會在視覺皮質中競爭表徵，而注意力透過把競爭偏向被注意的刺激來解決這場競爭。這個想法解釋了為何兩個刺激同時出現時，反應看起來像兩者的加權平均，也解釋了由上而下的訊號如何改變這個平均。這篇論文是綜述，匯集了神經生理學的證據，並成為視覺皮質注意力的標準解釋。

本頁是[大腦與機器中的注意力](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

視覺皮質的延伸區域有很大的感受野，因此不只一個物體可能同時落在其中。當兩個刺激存在時，神經元的反應並不只是各自反應的總和。問題在於大腦如何決定哪一個刺激驅動該反應，以及注意力如何改變這個決定。

## 方法

這篇論文是神經生理學證據的綜述，而非單一實驗。它彙整了視覺區域的記錄，這些記錄來自猴子注意兩個刺激之一的情境，並比較有注意與無注意時的反應。接著它提出一個單一機制，來解釋跨區域的這種模式。

所提出之解釋的步驟如下：

1. 感受野內的刺激競爭神經元有限的反應。
2. 沒有注意時，對一對刺激的反應會被拉向兩者的某種組合。
3. 來自較高區域的由上而下訊號，把競爭偏向符合當前目標的刺激。
4. 偏向後的反應向後傳遞，因此被注意的刺激在整個階層中得到更強的表徵。

第 3 步是注意力與由下而上訊號的區別所在。這個偏向可以依位置設定、依顏色之類的特徵設定，也可以依學到的目標設定。

## 結果

綜述指出，當兩個刺激位於同一感受野時，對這一對的反應相對於只有被注意刺激時會降低，而注意力會把反應拉向被注意的刺激。此效應在數個視覺區域中都有發現。本文以定性方式總結這些發現；引用具體數值前，請查閱全文。

## 限制

- 這個解釋是視覺系統的框架，並未說明實作此偏向的迴路。
- 偏向競爭解釋的是感受野內刺激之間的選擇，對於注意力如何在整個視野中分配，解釋較少。
- 證據主要來自靈長類視覺皮質，其在人類與其他感覺系統中的普遍性是另一個問題。

## 與其他主題的關聯

- **顯著性解釋**：不靠由上而下偏向、而是透過特徵對比運作的由下而上選擇路徑，見 [Itti、Koch 與 Niebur（1998）](../saliency-map/index.md)。
- **機器中的注意力模型**：與由上而下偏向相似的 Transformer 注意力加權，見 [Transformer](../../../theory/models/transformer/index.md)。
- **神經科學背景**：會彼此競爭的感受野與皮質區域，見[神經科學基礎](../../neuroscience/index.md)。
- **知覺**：注意力如何改變腹側路徑的反應，見[知覺與視覺系統](../../visual-perception/index.md)。

## 開放問題

- **什麼設定由上而下的偏向？** 綜述指出了來源，但選出目標訊號並把它送到正確神經元的機制，仍在研究中。
- **競爭發生在早期還是晚期？** 競爭在各區域間的時間點仍有爭議。

## 參考文獻

### 開創性論文

- Desimone, R. & Duncan, J.（1995）。Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.ne.18.030195.001205 — 提出偏向競爭，即由上而下的訊號解決同一感受野內刺激之間的競爭。
- Itti, L., Koch, C. & Niebur, E.（1998）。A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*。https://doi.org/10.1109/34.730558 — 以特徵對比為基礎的由下而上注意力模型，是偏向競爭的對應面。
- Mnih, V., Heess, N., 等人（2014）。Recurrent Models of Visual Attention. *NeurIPS*。https://arxiv.org/abs/1406.6247 — 學習而得的由上而下注意力選取模型，是目標導向選擇的機器版本。

### 綜述與回顧

- Corbetta, M. & Shulman, G. L.（2002）。Control of goal-directed and stimulus-driven attention in the brain. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn755 — 提供由上而下與由下而上訊號的背側與腹側注意力網路。

### 文章與原始研究

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I.（2017）。Attention Is All You Need. *NeurIPS*。https://arxiv.org/abs/1706.03762 — Transformer 的注意力加權，是由上而下偏向的機器類比。
