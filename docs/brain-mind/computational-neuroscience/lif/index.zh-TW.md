---
translation_reviewed: 2026-10-28
related:
- brain-mind/snn-neuromorphic
- brain-mind/neuroscience
tags:
- neuroscience
- spiking neural networks
- neuron models
aliases:
  - 漏電積分發放模型
  - Leaky integrate-and-fire
  - LIF
---

# 漏電積分發放模型（LIF）

漏電積分發放（leaky integrate-and-fire，LIF）神經元，是最簡單、仍能捕捉神經元放電核心的脈衝模型。膜電位累積輸入電流、緩慢地向靜息電位洩漏，並在達到閾值時發出脈衝、隨後重設。它是脈衝網路的主力模型：夠簡單，能大規模模擬，同時仍能重現脈衝的時間。

本頁屬於[計算神經科學](../index.md)。它詳細說明一種神經元模型。

## 概述

真實神經元透過離子通道的動力學產生動作電位，[Hodgkin–Huxley 模型](../hodgkin-huxley/index.md)詳細描述了這個過程。多數網路研究並不需要這麼細的層次。LIF 模型只保留電位、洩漏與閾值，並把脈衝視為事件。這使它能快速用於大型網路與神經形態硬體，代價是失去脈衝的形狀。

## 核心概念

- **膜電位（membrane voltage）**：神經元膜兩側的電位，隨輸入上升，並朝靜息值衰減。
- **洩漏（leak）**：在兩次輸入之間，電位朝靜息值的衰減。
- **閾值（threshold）**：神經元發出脈衝的電位。
- **重設（reset）**：脈衝後電位回到較低的值，之後神經元才能再度放電。
- **不應期（refractory period）**：脈衝後的一小段時間，神經元在此期間不會反應，基本模型中常會加入此項。

## 問題

神經元以放電回應輸入，而脈衝的時間攜帶資訊。描述此過程的模型，需要捕捉閾值與洩漏，又不能付出完整離子通道模型的代價，才能模擬大量神經元組成的網路。

## 核心想法

把神經元視為漏電電容器。輸入電流為它充電，洩漏使它放電；當電位達到閾值時，模型記錄一次脈衝，並把電位重設。此模型是 Hodgkin–Huxley 圖像的簡化：它省略了塑造脈衝形狀的離子電流，只保留決定脈衝何時發生的積分與閾值。

## 方程式或演算法

膜電位 \(V\) 遵循

\[
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R\,I(t), \qquad V \geq V_{th} \;\Rightarrow\; \text{spike},\; V \leftarrow V_{reset}
\]

其中 \(\tau_m\) 為膜時間常數，\(R\) 為膜電阻，\(I(t)\) 為輸入電流，\(V_{rest}\)、\(V_{th}\) 與 \(V_{reset}\) 分別為靜息、閾值與重設電位。模擬時，此方程以小的時間步長積分，每當跨越閾值就記錄一次脈衝。

## 結果

此模型的放電行為已有充分建立。在恆定輸入下，它的放電率隨高於閾值的輸入強度而上升，這捕捉了神經元的基本放電率行為。它的脈衝時間，是神經元如何以時間編碼輸入的一個有用（雖然簡化的）描述。其優點在於計算：LIF 網路可以大規模模擬，這也是多數脈衝網路研究的基礎。

## 限制

- **沒有脈衝形狀。**脈衝是事件，因此模型不描述離子通道、脈衝寬度或後超極化。
- **樹突被簡化。**每個神經元都是一個點，因此模型無法表示詳細模型中的非線性樹突運算。
- **參數固定。**標準 LIF 神經元不會調整閾值或洩漏，因此某些任務需要適應性變體，如適應性 LIF。

## 與其他主題的關聯

- **Hodgkin–Huxley 模型**：LIF 所簡化的詳細模型。見 [Hodgkin–Huxley](../hodgkin-huxley/index.md)。
- **脈衝神經網路**：LIF 神經元是脈衝網路常用的單元；訓練它們的學習規則見[脈衝神經網路與神經形態運算](../../snn-neuromorphic/index.md)，包括[脈衝時序依賴可塑性](../../snn-neuromorphic/stdp/index.md)。
- **母主題**：[計算神經科學](../index.md)。

## 應用

- **神經形態硬體**：許多晶片實作 LIF 類神經元，因為此模型計算成本低，且天生為事件驅動。
- **網路模型**：大型皮質迴路模擬通常以 LIF 神經元作為單元。

## 開放問題

- **網路需要多少細節？**詳細神經元的哪些特徵對網路功能重要，仍是開放問題，而這決定了 LIF 何時足夠。
- **如何加入適應性？**適應性變體改善了時間處理，但如何把適應性與學習結合，仍在探索中。

## 參考文獻

### 開創性論文

- Abbott, L. F.（1999）。Lapicque's introduction of the integrate-and-fire model neuron (1907). *Brain Research Bulletin*。https://doi.org/10.1016/S0361-9230(99)00161-6 — Lapicque 1907 年積分發放模型的歷史回顧，是 LIF 神經元的起源。
- Burkitt, A. N.（2006）。A review of the integrate-and-fire neuron model: I. Homogeneous synaptic input. *Biological Cybernetics*。https://doi.org/10.1007/s00422-006-0082-8 — 回顧積分發放模型在恆定與波動突觸輸入下的行為。
- Izhikevich, E. M.（2003）。Simple model of spiking neurons. *IEEE Transactions on Neural Networks*。https://doi.org/10.1109/TNN.2003.820440 — 比較簡單的脈衝模型，包括積分發放族，並說明哪些能重現皮質神經元的放電型態。

### 綜述與教科書

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*。Cambridge University Press。https://neuronaldynamics.epfl.ch/ — 免費線上教科書，其中有關於積分發放神經元及其變體的章節。
- Hodgkin, A. L. & Huxley, A. F.（1952）。A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*。https://doi.org/10.1113/jphysiol.1952.sp004764 — LIF 神經元所簡化的詳細電導模型。
