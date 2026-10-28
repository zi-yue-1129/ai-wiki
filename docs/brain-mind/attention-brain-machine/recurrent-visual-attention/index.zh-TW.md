---
translation_reviewed: 2026-10-28
related:
- theory/models/transformer
- brain-mind/attention-brain-machine
tags:
- attention
- vision
- reinforcement learning
aliases:
  - 循環視覺注意力
  - Recurrent Models of Visual Attention
  - RAM
---

# 循環視覺注意力模型（Mnih et al., 2014）

循環注意力模型（recurrent attention model，RAM）是一種一次只看影像一個注視點（glimpse）的網路。每一步它選擇下一個要看的位置、把所見累積在循環記憶中，並決定輸出什麼。位置的選擇不可微分，因此模型以強化學習訓練，這使它成為學習型、有目標導向的視覺注意力的早期例子。

本頁屬於[大腦與機器中的注意力](../index.md)。它詳細說明一個模型。

## 概述

生物視覺不會一次處理整個場景。眼睛會移動，注意力會挑選少數位置做細緻處理。Mnih 等人問的是：網路能否只靠分類訊號，自己學會這種選擇，而不必處理每一個像素。答案是一個能為任務學習該看哪裡的模型。

## 核心概念

- **注意力視窗（glimpse）**：影像中一小塊高解析度的區域，以選定位置為中心，離中心越遠解析度越低。
- **位置策略（location policy）**：網路中負責選擇下一個注視位置的部分。
- **循環核心（recurrent core）**：在多次注視之間累積資訊的隱藏狀態，使模型能整合所見。
- **位置的強化學習**：位置選擇從分布中取樣出一個隨機動作，因此需要以獎勵訊號訓練，不能只靠反向傳播。

## 問題

處理完整的高解析度影像成本高昂，而一次看全部的模型並不會挑選重要的部分。硬注意力（hard attention）選擇離散的位置，無法用一般梯度下降訓練，因為取樣位置會阻斷梯度。問題在於：如何訓練一個只注意少數位置、仍能學會任務的模型。

## 核心想法

網路在每一步於目前位置取一個注視點、更新循環狀態，並輸出下一個注視點的位置；最後再輸出分類。位置選擇從分布中取樣，模型以 REINFORCE 策略梯度方法訓練，並以最終分類是否正確作為獎勵。網路的其他部分則以一般反向傳播訓練。

## 方法

1. 在目前位置取一個低解析度、廣視野的注視點，並編碼。
2. 由注視點與前一狀態，更新循環狀態。
3. 依狀態由策略取樣下一個位置。
4. 重複固定次數的注視，然後輸出分類。
5. 分類器以反向傳播訓練，位置策略以 REINFORCE 訓練，獎勵來自最終判斷。

## 結果

論文報告，此模型學會注意影像中的相關部分，並在其測試的任務上分類準確，包括平移過的 MNIST 任務與動態控制任務。它的效率來自只處理少數注視點，而非整張影像。論文中的數字應以原論文為準；本頁不引用這些數字。

## 限制

- **訓練的變異大。**位置策略的強化學習梯度有雜訊，因此訓練比標準監督式學習慢且較不穩定。
- **任務簡單。**主要實驗使用小型、受控的資料集，因此推廣到自然影像的能力有限。
- **注視次數固定。**模型取固定次數的注視，與人類以停止為基礎、彈性的注意力不同。

## 與其他主題的關聯

- **偏向競爭與顯著性**：選擇的生物與自下而上的解釋，見[偏向競爭](../biased-competition/index.md)與[顯著性圖](../saliency-map/index.md)。
- **Transformer 注意力**：軟注意力會加權所有輸入，而不是選擇一個位置，這是 [Transformer](../../../theory/models/transformer/index.md) 的機制。
- **強化學習**：位置策略以本頁所屬之策略梯度家族訓練，見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。
- **母主題**：[大腦與機器中的注意力](../index.md)。

## 應用

- **高效率視覺**：學習該看哪裡，可以減少處理大型影像所需的計算。
- **機器人與主動視覺**：選擇看哪裡，是移動感測器以收集資訊的機器人的核心。

## 開放問題

- **硬注意力能否擴展？**訓練穩定性是在大型模型中使用位置選擇的主要障礙。
- **學到的注視與人類眼動如何比較？**與人類掃視路徑的吻合，是研究問題，而非原論文的結果。

## 參考文獻

### 開創性論文

- Mnih, V., Heess, N., Graves, A. & Kavukcuoglu, K.（2014）。Recurrent Models of Visual Attention. *Advances in Neural Information Processing Systems 27*。https://arxiv.org/abs/1406.6247 — 提出循環注意力模型，以強化學習訓練的學習型策略選擇注視位置。
- Ba, J., Mnih, V. & Kavukcuoglu, K.（2015）。Multiple Object Recognition with Visual Attention. *International Conference on Learning Representations*。https://arxiv.org/abs/1412.7755 — 把注視式注意力延伸到辨識一張影像中的多個物件。
- Vaswani, A., 等人（2017）。Attention Is All You Need. *Advances in Neural Information Processing Systems 30*。https://arxiv.org/abs/1706.03762 — 提出 Transformer 的軟注意力，是選擇位置的可微分替代方案。

### 綜述與回顧

- Desimone, R. & Duncan, J.（1995）。Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.ne.18.030195.001205 — 回顧視覺系統中注意力如何在競爭的刺激之間做選擇，這是本模型所處理問題的生物面向。
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M.（2017）。Neuroscience-Inspired Artificial Intelligence. *Neuron*。https://doi.org/10.1016/j.neuron.2017.06.011 — 回顧神經科學如何啟發 AI，包括注意力與選擇性處理。
- Itti, L., Koch, C. & Niebur, E.（1998）。A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*。https://doi.org/10.1109/34.730558 — 自下而上的顯著性模型，依特徵對比而非學到的策略來選擇位置。
