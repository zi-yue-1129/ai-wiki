---
translation_reviewed: 2026-10-28
related:
- theory/paradigms/meta-learning
- theory/optimization
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- learning
- neuromodulation
aliases:
  - 多巴胺之外的神經調節物質
  - 神經調節物質
  - Neuromodulation
  - Neuromodulators beyond dopamine
  - Acetylcholine
  - 乙醯膽鹼
  - Noradrenaline
  - Norepinephrine
  - 正腎上腺素
  - Serotonin
  - 血清素
  - ACh
  - NE
  - 5-HT
---

# 多巴胺之外的神經調節物質

多巴胺是與 AI 關係最常被提及的神經調節物質，因為它的獎勵預測誤差與強化學習的學習訊號相符。大腦還有其他神經調節物質。乙醯膽鹼、正腎上腺素與血清素各自來自一個小型核團，並廣泛投射到大腦各處；理論上它們分別負責不確定性、覺醒程度與學習速度的調節。這些角色是 AI 中適應性學習想法的來源之一。

本頁涵蓋這三個系統。多巴胺的訊號見[多巴胺的獎勵預測誤差](../neuroscience/dopamine-reward-prediction-error/index.md)，多巴胺在選擇中的角色見[決策、多巴胺與獎勵](../decision-reward/index.md)。神經調節的基本概念見[神經科學基礎](../neuroscience/index.md)。

## 概要

麩胺酸之類的神經傳導物質會把特定訊息從一個神經元傳到下一個。神經調節物質則是擴散式釋放，作用時間較長，因此會改變整個迴路的反應強度與學習方式。它比較像一組設定，而不是一則訊息。

這提示了一種分工。每個系統可能回報世界狀態的某些面向，而大腦的學習會隨這個狀態調整。主要的提議是：乙醯膽鹼訊號預期中的不確定性，正腎上腺素訊號突然且未被預期的改變，血清素設定大腦往前看多遠，覺醒程度則決定利用已知與探索之間的平衡。

## 核心概念

- **神經調節物質**：會在大範圍內改變神經元與迴路運作方式的化學物質。
- **預期不確定性（expected uncertainty）**：已知存在的不確定性，例如某個線索在特定情境下不可靠。
- **非預期不確定性（unexpected uncertainty）**：突然的改變，使既有預期變得不可靠。
- **學習率**：一次新結果更新估計值的幅度。它是多數學習演算法的元參數，也就是演算法本身的設定，而不是從資料學到的數值。

## 關鍵方法

- [基於不確定性的神經調節（Yu & Dayan, 2005）](yu-dayan-2005/index.md)：乙醯膽鹼與正腎上腺素分別訊號兩種不確定性，兩者都會降低對自上而下預期的依賴。
- [以神經調節實現的元學習（Doya, 2002）](doya-2002/index.md)：四種神經調節物質分別對應強化學習演算法的各部分，一個預測誤差與三個元參數。

兩種理論解釋的重點不同。Yu 與 Dayan 關心大腦在不確定下應如何權衡信念，並主要把乙醯膽鹼與正腎上腺素連到注意力。Doya 關心學習演算法本身的設定如何被控制，並把每種神經調節物質對應到其中一個組成部分。

## 核心想法

**不確定性作為訊號。** 如果某個線索已知有雜訊，一次出乎意料的結果不應大幅改變信念。如果環境剛剛改變，信念就應迅速調整。Yu 與 Dayan 主張乙醯膽鹼與正腎上腺素分別編碼這兩種情況。

**覺醒與探索的權衡。** 藍斑核是大腦正腎上腺素的主要來源，據描述它會在支持廣泛探索的緊張性模式與支持專注利用的相位模式之間切換（Aston-Jones & Cohen, 2005）。在人類身上，瞳孔相關的覺醒程度會追蹤雜訊過程中可評估的不穩定性，並預測新資料會如何改變信念（Nassar et al., 2012）。

**神經調節物質作為元參數。** Doya（2002）把多巴胺對應到預測誤差，血清素對應到折扣因子，正腎上腺素對應到動作選擇的隨機程度，乙醯膽鹼對應到學習率。這個對應是一項假說，但它讓每種神經調節物質都有精確的計算角色。

**AI 中的相同想法。** Adam 之類的適應性最佳化器會根據梯度的滑動估計來控制每個參數的步長（Kingma & Ba, 2015）。學習型最佳化器更進一步，直接學習更新規則。Andrychowicz et al.（2016）訓練遞迴網路作為最佳化器，在其訓練的任務上勝過人工設計的最佳化器。

## 連結

- **強化學習。** 學習率、折扣因子與 softmax 溫度是 Doya 連到神經調節物質的元參數。見[強化學習](../../theory/paradigms/reinforcement-learning/index.md)及其[探索](../../theory/paradigms/reinforcement-learning/exploration/index.md)頁。
- **元學習。** 神經調節提供了「學會學習」的生物學觀點：大腦不只學習內容，也調整學習方式。見[元學習](../../theory/paradigms/meta-learning/index.md)。
- **預測編碼。** 兩種理論都把不確定性視為控制新證據改變信念多少的機制。見[預測編碼與自由能](../predictive-coding/index.md)。
- **注意力。** 不確定性訊號會塑造注意力。見[大腦與機器中的注意力](../attention-brain-machine/index.md)。
- **記憶與以模型為基礎的控制。** 乙醯膽鹼在記憶更新速度上的假定角色與[記憶與學習](../memory-learning/index.md)相關。神經調節物質也可能改變代理人對習得模型的依賴程度，見[以模型為基礎與無模型控制](../decision-reward/model-based-vs-model-free/index.md)。

## 應用

- **AI 中的適應性學習率。** [Adam](../../theory/optimization/adaptive/adam.md) 等適應性最佳化器執行的功能與 Doya 對乙醯膽鹼的對應相同，但它們本身不是神經調節模型。
- **學會學習。** 學習型最佳化器以訓練出的規則取代人工設計的更新規則，是「學習規則本身可以被學習」這個想法在工程上的對應。
- **人類實驗。** 瞳孔直徑是認知實驗中測量覺醒與不確定性的非侵入性指標，例如 Nassar et al.（2012）。

## 開放問題

- **哪個訊號對應哪個角色？** 把乙醯膽鹼與正腎上腺素分成預期與非預期不確定性有一定支持，但兩種訊號在許多任務中會重疊。
- **這些對應是因果的嗎？** 要驗證操弄某一種神經調節物質是否恰好改變一個參數，很困難，因為各系統彼此交互作用。
- **神經調節物質如何影響學習規則？** 改變學習率的分子與迴路路徑仍在描繪中。
- **人工元學習器像大腦嗎？** 兩者目標相同，但大腦是否實作了類似 AI 中學得的更新規則，目前並不清楚。

## 參考文獻

### Seminal papers

- Yu, A. J. & Dayan, P. (2005). Uncertainty, Neuromodulation, and Attention. *Neuron*. https://doi.org/10.1016/j.neuron.2005.04.026 — 提出乙醯膽鹼與正腎上腺素分別訊號預期與非預期不確定性。詳見[Yu & Dayan 2005](yu-dayan-2005/index.md)。
- Doya, K. (2002). Metalearning and neuromodulation. *Neural Networks*, 15(4–6), 495–506. https://doi.org/10.1016/s0893-6080(02)00044-8 — 提出四種神經調節物質分別對應強化學習的元參數。詳見[Doya 2002](doya-2002/index.md)。
- Dayan, P. & Yu, A. J. (2006). Phasic norepinephrine: a neural interrupt signal for unexpected events. *Network: Computation in Neural Systems*, 17(4), 335–350. https://doi.org/10.1080/09548980601004024 — 提出相位正腎上腺素是非預期事件的神經中斷訊號。
- Nassar, M. R., Rumsey, K. M., Wilson, R. C., Parikh, K., Heasly, B. & Gold, J. I. (2012). Rational regulation of learning dynamics by pupil-linked arousal systems. *Nature Neuroscience*, 15(7), 1040–1046. https://doi.org/10.1038/nn.3130 — 人類實驗顯示瞳孔相關的覺醒追蹤雜訊過程中可評估的不穩定性，並預測新資料會多大程度地影響信念。
- Andrychowicz, M. et al. (2016). Learning to learn by gradient descent by gradient descent. *NeurIPS*. https://arxiv.org/abs/1606.04474 — 訓練遞迴網路作為最佳化器，在其訓練任務上勝過人工設計的最佳化器。
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. *ICLR*. https://arxiv.org/abs/1412.6980 — 提出 Adam，保留梯度一階與二階矩的滑動估計。

### Surveys and textbooks

- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — 提出緊張性正腎上腺素活動支持探索，相位活動支持利用。
- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*, 11(4), 410–416. https://doi.org/10.1038/nn2077 — 回顧神經調節物質與決策的關係。
- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2006.09.002 — 回顧乙醯膽鹼在學習與記憶中角色的證據。
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — 強化學習的標準入門教科書，本頁使用的折扣因子、學習率與 softmax 選擇規則都在此框架下。
