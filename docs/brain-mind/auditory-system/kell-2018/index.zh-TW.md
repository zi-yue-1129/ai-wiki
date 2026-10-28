---
translation_reviewed: 2026-10-28
---

# 面向聽覺的任務最佳化深度網路（Kell 等人 2018）

Kell 等人（2018）以日常音訊任務訓練一個深度神經網路，然後把它與人類聽者及人類聽覺皮質相比較。他們報告，這個網路在任務上的表現與人類相似，它的反應能預測聽覺皮質的活動，而且它的各個階段形成了類似皮質的階層。這篇論文是[Yamins 等人 2014](../../visual-perception/yamins-2014/index.md)在聽覺上的對應研究，也是 [NeuroAI](../../neuroai/index.md) 的里程碑。

本頁是[聽覺與聽覺系統](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 概述

關於聽覺皮質的許多認識，來自純音與噪音短脈衝等簡單聲音。這些刺激能揭示調諧特性，但無法說明系統如何處理語音與音樂。Kell 等人提出的問題，與 Yamins 等人（2014）在視覺上提出的問題相呼應：如果讓深度網路學會人們用聲音進行的任務，它的內部組織是否會逐漸像聽覺系統？

## 核心概念

- **任務最佳化**：透過在某項任務上訓練來選擇模型參數，而不是直接擬合神經紀錄。
- **耳蝸圖（cochleagram）**：模仿耳蝸頻率分析的時間—頻率表示法。它是網路的輸入。
- **編碼模型**：從模型的內部單元到單一記錄位置反應的線性映射，在部分聲音上擬合，並在其他聲音上檢驗。
- **階段階層**：網路的各層，從輸入到輸出依序排列。比較的目的是看哪一階段最符合哪一個皮質區域。

## 運作方式

1. **輸入。** 每段聲音被轉換為耳蝸圖。
2. **訓練。** 一個具有多個階段的卷積網路，同時在數項音訊任務上訓練，例如辨識字詞與說話者，以及對環境聲音分類。
3. **行為測試。** 把訓練後的網路交給人類聽者會做的任務，包括在背景噪音中的任務。比較其錯誤型態與人類表現。
4. **神經測試。** 對每個記錄位置，用一組聲音，從各階段擬合一個編碼模型來預測該位置的反應，並在未用於擬合的聲音上檢驗。預測最好的階段，被視為最符合該位置的階段。

編碼步驟是線性迴歸。若 $h_\ell(x)$ 是階段 $\ell$ 對聲音 $x$ 的活動，則位置 $v$ 的預測為 $\hat{r}_v(x) = \mathbf{w}_v^\top h_\ell(x)$，每個位置各有一組權重向量 $\mathbf{w}_v$。

## 結果

論文標題概括了三項主要發現。第一，訓練後的網路重現了人類聽覺行為的部分特徵，包括其錯誤型態。第二，它的內部階段能預測人類聽覺皮質對未用於擬合之聲音的反應。第三，這些階段與皮質階層相符：論文報告，階段由前往後呈現一種推進關係，較早的階段對應初級聽覺皮質，較後的階段則對應其之外的區域。

定量結果見於論文原文。本頁以文字描述這些結果，不引用數字。

## 限制

- **對任務的依賴。** 網路的組織取決於它所被訓練的任務，因此這種吻合既反映架構，也反映所選的任務。
- **粗糙的神經資料。** 人類的紀錄是在空間與時間上對許多神經元的平均，因此這項比較描述的是群體反應，而非個別神經元的運算。
- **相似不等於機制。** 能預測皮質反應，並不能證明大腦使用相同的運算。
- **刺激有限。** 比較所用的聲音是有限的，對其他聲音、說話者與聽覺條件的推廣，有待後續研究。

## 開放問題

- **哪些任務會產生類似皮質的階層？** Kell 與 McDermott（2019）回顧了任務限制如何塑造學得的表徵。人類聽覺系統究竟最佳化於哪些任務，仍有爭議。
- **這種吻合能否延伸到更細的尺度？** 以單一神經元紀錄檢驗相同的模型，可以判斷這種對應是否也成立於迴路層級。
- **它能推廣到有噪音的語音嗎？** Mattys 等人（2012）顯示，聽者能應付的不利條件範圍，比大多數模型所測試的條件更廣。

## 參考文獻

### 開創性論文

- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H.（2018）。A Task-Optimized Neural Network Replicates Human Auditory Behavior, Predicts Brain Responses, and Reveals a Cortical Processing Hierarchy。*Neuron*。https://doi.org/10.1016/j.neuron.2018.03.044 — 以音訊任務訓練深度網路，並顯示其符合人類聽覺行為、能預測皮質反應，且具有類似皮質的階層。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J.（2014）。Performance-optimized hierarchical models predict neural responses in higher visual cortex。*Proceedings of the National Academy of Sciences*。https://doi.org/10.1073/pnas.1403112111 — 顯示為物體辨識選出的網路，能預測 V4 與顳下皮質的反應。

### 綜述與教科書

- Kell, A. J. E. & McDermott, J. H.（2019）。Deep neural network models of sensory systems: windows onto the role of task constraints。*Current Opinion in Neurobiology*。https://doi.org/10.1016/j.conb.2019.02.003 — 回顧所訓練的任務如何塑造網路的感覺表徵，以及這對大腦模型意味著什麼。
- Yamins, D. L. K. & DiCarlo, J. J.（2016）。Using goal-driven deep learning models to understand sensory cortex。*Nature Neuroscience*。https://doi.org/10.1038/nn.4244 — 主張以目標最佳化的網路可作為感覺皮質的模型，並說明如何檢驗它們。
- Mattys, S. L., Davis, M. H., Bradlow, A. R. & Scott, S. K.（2012）。Speech recognition in adverse conditions: A review。*Language and Cognitive Processes*。https://doi.org/10.1080/01690965.2012.705006 — 回顧聽者如何在噪音中辨識語音，以及哪些過程能加以補償。

### 文章與文件

- Wang, D. & Chen, J.（2018）。Supervised Speech Separation Based on Deep Learning: An Overview。arXiv。https://arxiv.org/abs/1708.07524 — 綜述從背景噪音中分離目標語音的深度學習方法。
