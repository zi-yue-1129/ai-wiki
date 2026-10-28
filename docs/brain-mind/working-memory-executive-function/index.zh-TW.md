---
translation_reviewed: 2026-10-28
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/memory-learning
- brain-mind/cognitive-architectures
- theory/models/rnn/gated-cells
tags:
- working memory
- executive function
- prefrontal cortex
- gating
aliases:
  - 工作記憶與執行功能
  - 工作記憶
  - 執行功能
  - Working Memory
  - Executive Function
  - Executive Control
  - Prefrontal Cortex
  - PFC
---

# 工作記憶與執行功能

工作記憶是在短時間內把少量資訊保留在心中並加以使用的能力，例如撥打電話時記住的號碼，或讀句子時記住句首的內容。執行功能則是一組控制過程，決定什麼資訊可以進入這個儲存區、保留什麼、何時更新，以及行為如何依此進行。兩者都高度依賴前額葉皮質（prefrontal cortex, PFC）。在 AI 中，上下文視窗與門控循環網路扮演的角色與之相近。


## 概述

工作記憶是一個有限、暫時的儲存區。Baddeley 與 Hitch（1974）把工作記憶界定為一個獨立的暫時儲存區。執行功能是更廣的一族控制能力：選擇目標、在任務之間切換、過濾干擾，以及在心中保持規則。兩者在實際中難以分開，因為保持資訊是為了控制，而控制又決定了保持什麼。

Miller 與 Cohen（2001）提出，前額葉皮質透過主動維持代表目標及達成目標之手段的活動模式來執行控制功能。這些模式會偏置其他腦區的處理，使活動沿著任務所需的輸入、內部狀態與輸出之間的對應路徑流動。

## 核心概念

- **工作記憶（working memory）**：為了正在進行的工作，在短時間內保持可用的資訊。
- **執行功能（executive function）**：對於注意、儲存、更新、切換與抑制哪些內容的控制。
- **持續活動（persistent activity）**：延遲期間神經元持續放電。Funahashi、Bruce 與 Goldman-Rakic（1989）在猴子的空間記憶任務中，記錄到前額葉神經元在這段時間內的活動。
- **活動靜默記憶（activity-silent memory）**：資訊保存於短暫的變化之中，不需要持續放電。
- **閘控（gating）**：開啟或關閉對記憶儲存區的存取的機制，使只有相關的輸入能更新它。
- **容量限制（capacity limit）**：同時能保持的量。Cowan（2001）回顧證據，認為限制約為三到五個組塊，中心值約為四個。

## 核心理念

**保持與決定是兩個不同的問題。** 一個什麼都保留的系統並不具選擇性，而一個不斷更新的系統則會忘記它所需要的內容。被提出的常見解法是閘控：系統學習何時寫入記憶，何時保護已經存在的內容。

**保持資訊的兩種機制。** 早期的網路模型把持續活動解釋為由遞迴連結維持的穩定放電模式（Compte 等人，2000）。較新的研究發現，延遲期間的活動並不總是伴隨著保持（Wolff 等人，2017；Stokes，2015），這暗示記憶也可能由突觸或其他隱藏狀態承載。兩種觀點目前尚未定論。

**學習而得的控制閘。** 一個有影響力的模型中，基底核學習何時前額葉皮質應該更新其內容，所用的是類多巴胺的學習訊號。如此一來，控制本身是系統學到的，而不是一個無法解釋的內在控制者。

**容量是槽位還是資源。** 以槽位為基礎的說法認為，工作記憶是少數幾個離散的項目。以資源為基礎的說法則認為，它是一個可分配給各項目的共享精確度資源。Bays 與 Husain（2008）指出，視覺記憶並不由物件數目固定，而是會依注意力動態分配，這支持資源觀。

## 主要方法

- [前額葉—基底核工作記憶（PBWM）](pbwm/index.md)：基底核學習前額葉皮質何時更新其內容的模型，使執行控制成為學習而得的能力。
- [活動靜默工作記憶](activity-silent-working-memory/index.md)：記憶以短暫的突觸狀態保存的理論，因此在延遲期間放電可以停止。

## 連結

- **記憶。** 海馬迴與皮質中的長期儲存，見[大腦中的記憶與學習](../memory-learning/index.md)及[互補學習系統](../memory-learning/complementary-learning-systems/index.md)。
- **基底核與獎勵。** PBWM 依賴的學習訊號，與[多巴胺的獎勵預測誤差](../neuroscience/dopamine-reward-prediction-error/index.md)屬於同一類。多巴胺在選擇中的更廣角色，見[決策、多巴胺與獎勵](../decision-reward/index.md)。
- **注意力。** 選擇相關資訊的功能，與[大腦與機器中的注意力](../attention-brain-machine/index.md)相通。
- **認知架構。** 有些架構把工作記憶與控制當作獨立模組處理，見[認知架構](../cognitive-architectures/index.md)。
- **AI：上下文視窗。** Transformer 的上下文視窗是它能同時注意的詞元集合（[Transformer](../../theory/models/transformer/index.md)）。與工作記憶儲存區不同，視窗本身不會自行決定保留什麼；超出視窗之外的內容能否留存，取決於周圍的系統，這也是許多系統要加上外部記憶的原因。
- **AI：門控循環網路。** LSTM 的輸入閘、遺忘閘與輸出閘，學習何時寫入、保留與讀出記憶單元（[LSTM](../../theory/models/rnn/gated-cells/lstm/index.md)）。它在功能上類似 PBWM 的閘控，但這種相似只在功能上成立，兩者的實作並不相同。
- **AI：執行控制。** 人工代理人的規劃與控制，見 [AI 代理人](../../theory/models/agents/index.md)與[推理](../../theory/models/reasoning/index.md)。

## 應用

- **神經網路中的閘控記憶。** LSTM（Hochreiter 與 Schmidhuber，1997）以乘法閘保護記憶單元，跨越長時間間隔，至今仍廣泛用於序列建模。
- **解讀執行控制實驗。** Miller 與 Cohen（2001）回顧支持前額葉作為控制來源的神經生理、神經影像與計算研究。
- **檢驗記憶維持。** Wolff 等人（2017）在延遲期間施以短暫的 EEG 擾動脈衝，以偵測項目特定的記憶。

## 未解問題

- **資訊如何被保持？** 持續放電、突觸狀態以及兩者的混合，都有一些支持證據。在特定任務中各自的比重仍有爭議（Stokes，2015；Wolff 等人，2017）。
- **是什麼決定容量？** 槽位與資源兩種解釋仍然並存，答案可能隨任務而異（Cowan，2001；Bays 與 Husain，2008）。
- **閘控如何學習？** PBWM 提出一個基於多巴胺、可學習的閘，但它與已確認的神經迴路之間的對應仍在檢驗中。
- **AI 與大腦的閘控是否共享原理？** 功能上的類比很清楚。它是否反映共通的計算原理，仍是開放問題。

## 參考文獻

### 開創性論文

- Baddeley, A. D. & Hitch, G. (1974). Working memory. In *Psychology of Learning and Motivation*, pp. 47–89. Academic Press. https://doi.org/10.1016/S0079-7421(08)60452-1 — 提出工作記憶作為一個獨立的暫時儲存區，是本概述的出發概念。
- Funahashi, S., Bruce, C. J. & Goldman-Rakic, P. S. (1989). Mnemonic coding of visual space in the monkey's dorsolateral prefrontal cortex. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.1989.61.2.331 — 記錄空間記憶任務延遲期間活躍的前額葉神經元。
- Compte, A. et al. (2000). Synaptic mechanisms and network dynamics underlying spatial working memory in a cortical network model. *Cerebral Cortex*. https://doi.org/10.1093/cercor/10.9.910 — 以持續活動為基礎的空間工作記憶網路模型。
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X01003922 — 回顧容量限制約為三到五個組塊的證據。
- Bays, P. M. & Husain, M. (2008). Dynamic shifts of limited working memory resources in human vision. *Science*. https://doi.org/10.1126/science.1158023 — 顯示視覺記憶是有限資源，會在各項目之間動態分配。
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — 提出 LSTM，其乘法閘控制對記憶單元的存取。
- Miller, E. K. & Cohen, J. D. (2001). An integrative theory of prefrontal cortex function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — 提出前額葉維持目標表徵，並偏置其他腦區的理論。
- O'Reilly, R. C. & Frank, M. J. (2006). Making working memory work: a computational model of learning in the prefrontal cortex and basal ganglia. *Neural Computation*. https://doi.org/10.1162/089976606775093909 — 提出 PBWM，即基底核對前額葉更新進行閘控的模型。
- Mongillo, G., Barak, O. & Tsodyks, M. (2008). Synaptic theory of working memory. *Science*. https://doi.org/10.1126/science.1150769 — 提出工作記憶由鈣介導的突觸易化維持，並由放電加以刷新。

### 綜述與教科書

- Stokes, M. G. (2015). 'Activity-silent' working memory in prefrontal cortex: a dynamic coding framework. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2015.05.004 — 回顧延遲活動並不總是伴隨保持的證據，並提出動態編碼框架。
- Curtis, C. E. & D'Esposito, M. (2003). Persistent activity in the prefrontal cortex during working memory. *Trends in Cognitive Sciences*. https://doi.org/10.1016/S1364-6613(03)00197-9 — 回顧工作記憶期間前額葉持續延遲活動的證據。
- Ma, W. J., Husain, M. & Bays, P. M. (2014). Changing concepts of working memory. *Nature Neuroscience*. https://doi.org/10.1038/nn.3655 — 回顧工作記憶從固定項目數轉向有限資源、在各項目間分配的觀點，並納入行為與神經證據。
- Miller, E. K., Lundqvist, M. & Bastos, A. M. (2018). Working memory 2.0. *Neuron*. https://doi.org/10.1016/j.neuron.2018.09.023 — 回顧近期提議：工作記憶的維持依賴於放電爆發之間的突觸權重變化，而執行控制則源於不同皮質層中振盪節律的交互作用。
- Jonides, J., Lewis, R. L., Nee, D. E., Lustig, C. A., Berman, M. G. & Moore, K. S. (2008). The mind and brain of short-term memory. *Annual Review of Psychology*. https://doi.org/10.1146/annurev.psych.59.103006.093615 — 回顧短期記憶的心理學理論，包括容量與遺忘，以及這些理論與大腦機制證據的關係。
- Wolff, M. J., Jochim, J., Akyürek, E. G. & Stokes, M. G. (2017). Dynamic hidden states underlying working-memory-guided behavior. *Nature Neuroscience*. https://doi.org/10.1038/nn.4546 — 以 EEG 與擾動脈衝偵測延遲期間的項目特定記憶；此訊號的強度可預測記憶引導的行為。
