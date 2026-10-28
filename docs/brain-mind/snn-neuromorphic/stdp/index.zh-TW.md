---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/computational-neuroscience
tags:
- neuroscience
- learning rules
- spiking neural networks
aliases:
  - 脈衝時序依賴可塑性
  - Spike-timing-dependent plasticity
  - STDP
---

# 脈衝時序依賴可塑性（STDP）

脈衝時序依賴可塑性（STDP）是一種學習規則：突觸的改變取決於突觸兩側脈衝的相對時間。若突觸前神經元在突觸後神經元之前不久放電，突觸便增強；順序相反，則突觸減弱。它是目前最為人所知、在生物中觀察到的此類規則，也是脈衝網路中許多學習規則的基礎。

本頁屬於[脈衝神經網路與神經形態運算](../index.md)。它詳細說明一種學習規則。

## 概述

Donald Hebb 提出「一起放電的神經元，會連結在一起」。STDP 把這個想法精確到時間上：重要的不只是兩個神經元是否活躍，還包括輸入脈衝是否早於輸出脈衝到達。幫助觸發突觸後脈衝的突觸會被強化；太晚到達、無助於觸發的突觸則會減弱。

## 核心概念

- **突觸前與突觸後脈衝**：到達突觸的脈衝，以及接收神經元所發出的脈衝。
- **時間窗（timing window）**：突觸會改變的脈衝時間差範圍，通常為數十毫秒。
- **增強與減弱（potentiation and depression）**：突觸前脈衝先到時增強，後到時減弱。
- **Hebb 學習（Hebbian learning）**：相關的活動會強化連結的更廣泛原則，STDP 是其中針對時間的特定形式。

## 問題

Hebb 原則沒有說明，在短時間內突觸何時應該改變。對皮質與海馬神經元的實驗顯示，改變的正負與大小取決於脈衝的順序與間隔。脈衝網路中的學習模型，需要一條能捕捉這種依賴關係的規則。

## 核心想法

突觸權重的改變，是突觸前與突觸後脈衝之間時間差 \(\Delta t = t_{post} - t_{pre}\) 的函數。\(\Delta t > 0\)（突觸前先於突觸後）的配對產生增強，\(\Delta t < 0\) 的配對產生減弱。效果隨 \(|\Delta t|\) 增大而減弱，因此只有近乎同時的脈衝會大幅改變突觸。

## 方程式或演算法

常見形式對時間差的兩種符號各使用一個指數窗：

\[
\Delta w = \begin{cases} A_+ \, e^{-\Delta t / \tau_+} & \Delta t > 0 \\ -A_- \, e^{\Delta t / \tau_-} & \Delta t < 0 \end{cases}
\]

其中 \(A_+\) 與 \(A_-\) 設定增強與減弱的大小，\(\tau_+\) 與 \(\tau_-\) 設定時間窗，通常在數十毫秒的範圍內。每次出現一對脈衝時就套用此規則。

## 結果

Bi 與 Poo（1998）對培養的海馬神經元所做的原始實驗，量測了突觸強度的改變如何隨配對脈衝的時間而變，並發現上述不對稱的時間窗。Markram 等人（1997）則報告，在皮質錐狀神經元中，突觸效能取決於突觸後動作電位與突觸輸入之間的時間關係。此規則的形式即取自這些量測，而數值上的時間窗因標本而異。

## 限制

- **成對規則。**基本形式只考慮脈衝對。三重與其他高階規則，在某些標本中擬合資料較好。
- **單獨時不穩定。**若沒有上限或競爭機制，STDP 可能把權重推向極端，因此實用模型會加入正規化或恆定性機制。
- **不足以單獨完成任務學習。**STDP 單獨只能做非監督的特徵學習。要學習任務，需要獎勵等訊號，這正是獎勵調節 STDP 的基礎。

## 與其他主題的關聯

- **脈衝神經網路**：STDP 是脈衝網路的局部學習規則之一，另一個是 [e-prop](../eprop/index.md)，它使用資格跡與學習訊號。
- **神經形態硬體**：局部、以時間為基礎的規則適合晶片上學習，因為每個突觸只需要其兩個神經元的脈衝時間。
- **多巴胺與獎勵**：獎勵調節 STDP 把時間規則與獎勵訊號連結起來，見[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.md)。
- **母主題**：[脈衝神經網路與神經形態運算](../index.md)。

## 應用

- **非監督特徵學習**：以 STDP 訓練的網路，可以在沒有標籤的情況下，從輸入脈衝序列學到特徵。
- **神經形態晶片**：以局部時間規則進行晶片上學習，是硬體設計中的活躍領域。

## 開放問題

- **成對規則是否捕捉了生物機制？**脈衝之間的高階交互作用，以及它們對樹突位置的依賴，並未被簡單形式完全捕捉。
- **STDP 如何與其他可塑性結合？**恆定性與神經調節機制與 STDP 互動的方式，基本規則並未顯示。
- **STDP 能否在規模上學習複雜任務？**大多數示範都在小型問題上進行，因此推廣到深層網路仍未解決。

## 參考文獻

### 開創性論文

- Bi, G.-Q. & Poo, M.-M.（1998）。Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *Journal of Neuroscience*。https://doi.org/10.1523/JNEUROSCI.18-24-10464.1998 — 量測突觸改變的正負與大小，如何取決於突觸前與突觸後脈衝的時間。
- Markram, H., Lübke, J., Frotscher, M. & Sakmann, B.（1997）。Regulation of Synaptic Efficacy by Coincidence of Postsynaptic APs and EPSPs. *Science*。https://doi.org/10.1126/science.275.5297.213 — 顯示皮質突觸的效能取決於突觸後動作電位相對於突觸輸入的時間。
- Song, S., Miller, K. D. & Abbott, L. F.（2000）。Competitive Hebbian learning through spike-timing-dependent synaptic plasticity. *Nature Neuroscience*。https://doi.org/10.1038/78829 — 顯示基於時間的規則，能在網路模型中產生輸入結構的競爭式 Hebb 學習。

### 綜述與教科書

- Caporale, N. & Dan, Y.（2008）。Spike timing-dependent plasticity: a Hebbian learning rule. *Annual Review of Neuroscience*。https://doi.org/10.1146/annurev.neuro.31.060407.125639 — 把 STDP 作為 Hebb 規則的綜述，涵蓋其實驗基礎與在迴路學習中的角色。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*。Cambridge University Press。https://neuronaldynamics.epfl.ch/ — 免費線上教科書，其中有關於脈衝網路中突觸可塑性與學習規則的章節。
