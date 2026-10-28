---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/neuroai
tags:
- neuroscience
- attention
- computer-vision
aliases:
  - Itti 等人 1998
  - 顯著性圖
  - 基於顯著性的視覺注意力
---

# 基於顯著性的視覺注意力（Itti、Koch 與 Niebur，1998）

Itti、Koch 與 Niebur（1998）建立了一個由下而上注意力的模型，它只靠特徵對比就能從場景中選出位置。顏色、亮度與方向在數個尺度上被計算，中心-周邊差異會凸顯與周圍不同的區域，最後結合成單一的顯著性圖。勝者全取的階段挑出最顯著的位置，而返回抑制（inhibition of return）則防止模型一直停在同一處。這個模型成為電腦視覺中基於顯著性注意力的參考實作。

本頁是[大腦與機器中的注意力](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

人類觀察者會把眼睛移到場景中的少數幾個位置，而這些位置往往並非隨機。有些區域即使觀察者並未在搜尋，也會因為與周圍不同而吸引注意力。問題在於：一個簡單、由下而上的計算，能否預測注意力在自然影像中會去哪裡。

## 方法

此模型是一條由下而上的影像運算管線，沒有從眼動資料中學習。它接收一張影像，計算特徵圖，並把它們結合成顯著性的圖。接著它依顯著性高低依序選取位置，並在每個位置被注意後加以抑制。

步驟如下：

1. 把影像分解為數個空間尺度上的顏色、亮度與方向通道。
2. 在每個通道內計算中心-周邊差異，使與周圍不同的區域產生強烈反應。
3. 把特徵圖正規化並結合為單一的顯著性圖。
4. 以勝者全取階段選出最顯著的位置，接著套用返回抑制，使注意力移到別處。

第 4 步是把靜態的圖轉變為一連串注視點的關鍵。如果沒有返回抑制，模型會不斷回到同一位置。

## 結果

論文指出，模型在合成影像與自然影像上的選取，在定性上會跟隨那些突出的區域，而選取的順序與人們觀看此類場景的順序相似。在本頁所用的摘要中，這些結果是定性的。引用具體數字前，請查閱全文。

## 限制

- 此模型只有由下而上的部分，沒有任務目標，因此無法解釋對特定目標的搜尋。
- 顯著性不等於相關性。突出的區域可能與觀察者正在做的事無關。
- 特徵是人工設計的，模型並未從資料中學習這些特徵。

## 與其他主題的關聯

- **由上而下的解釋**：目標驅動的對應面，即選擇受任務需求偏向，見[偏向競爭](../biased-competition/index.md)。
- **視覺特徵**：顏色與方向通道與[知覺與視覺系統](../../visual-perception/index.md)中的感受野研究相關。
- **神經科學背景**：計算對比的皮質區域摘要於[神經科學基礎](../../neuroscience/index.md)。

## 開放問題

- **顯著性在複雜場景中是否能捕捉人類注意力？** 簡單的特徵模型能預測部分注視點，但不是全部，這個落差正以更細緻的場景模型加以研究。
- **由下而上與由上而下的訊號應如何結合？** 此模型把兩者分開處理，合併的解釋仍是開放問題。

## 參考文獻

### 開創性論文

- Itti, L., Koch, C. & Niebur, E.（1998）。A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*。https://doi.org/10.1109/34.730558 — 以中心-周邊特徵對比建立的由下而上注意力顯著性圖模型。
- Desimone, R. & Duncan, J.（1995）。Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.ne.18.030195.001205 — 本顯著性模型所補足的由上而下偏向競爭解釋。
- Mnih, V., Heess, N., 等人（2014）。Recurrent Models of Visual Attention. *NeurIPS*。https://arxiv.org/abs/1406.6247 — 學習而得的注視點選取模型，是目標導向選擇的機器版本。
- Bahdanau, D., Cho, K. & Bengio, Y.（2014）。Neural Machine Translation by Jointly Learning to Align and Translate. arXiv 預印本。https://arxiv.org/abs/1409.0473 — 提出學習式對齊，是神經網路中注意力的早期形式。

### 綜述與回顧

- Corbetta, M. & Shulman, G. L.（2002）。Control of goal-directed and stimulus-driven attention in the brain. *Nature Reviews Neuroscience*。https://doi.org/10.1038/nrn755 — 負責由下而上的刺激驅動注意力的腹側網路，正是顯著性解釋所建模的對象。
