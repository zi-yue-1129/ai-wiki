---
translation_reviewed: 2026-10-28
---

# 人職適配（Zhu et al. 2018）

人職適配是判斷候選人的資格與某份工作契合程度的任務，而 Zhu 等人（2018）提出的人職適配神經網路（Person-Job Fit Neural Network，PJFNN），是對此任務的早期深度學習解法。模型從歷史應徵資料中學習候選人與職缺要求的聯合表示，並能指出候選人符合哪些要求項目。它是上層頁面[人力資源與招募](../index.md)列出的兩個代表性方法之一。

## 概述

履歷篩選是一個比對問題。招募人員閱讀職缺說明，列出各項要求，再逐項核對每位候選人的背景。早期的自動化系統比對關鍵字，因此會遺漏同義詞，以及以不同說法描述的技能。Zhu 等人主張從資料中學習這種比對：過去的應徵紀錄顯示哪些候選人適合哪些工作，神經網路便能從這些例子中學到兩段文字之間的連結。

論文把契合視為人與職缺共同的性質，而不只是候選人本身的分數。這使輸出更有用：模型能指出候選人滿足哪些要求，而不是只回傳一個沒有解釋的數字。

## 關鍵概念

- **二部網路（bipartite network）**：有兩個輸入端的網路，一端是候選人，一端是職缺，兩者在共享的表示中相遇。
- **聯合表示（joint representation）**：候選人與職缺可以直接比較的向量空間，彼此的接近程度即代表契合程度。
- **要求項目（requirement items）**：職缺說明中各自獨立的敘述，例如某項技能、某項資格或某年的工作經驗要求，各自被單獨表示。
- **階層式表示（hierarchical representation）**：分層的設計，先表示較小的文字單位，再組合成整份履歷或職缺的表示。

## 運作方式

摘要描述的模型，其各部分可以概括如下。以下步驟是對設計的白話解讀；確切的層大小與數學式，請以論文為準。

1. **編碼職缺。** 以卷積神經網路將職缺中的每個要求項目轉成向量。卷積網路以學習到的濾波器掃過文字中的詞，再加以彙整。
2. **編碼候選人。** 從履歷取出的資格，以相同的階層方式編碼，使兩側可以逐項比較。
3. **學習聯合空間。** 二部網路在歷史應徵資料上訓練，每筆範例配對一位候選人與一份職缺，並記錄結果。網路由此學到兩側的聯合表示。
4. **評估契合與要求。** 整體契合度由聯合表示估計。對每個要求項目，其向量與對應的候選人表示之間的距離，顯示該要求是否被滿足。

此設計是端到端的：文字編碼器與比對網路一起訓練，而不是分開工程設計。

## 關鍵結果

作者報告，他們在一個大型真實應徵資料集上做了大量實驗，並認為這些實驗驗證了模型在預測契合度上的表現。他們也展示了模型學到的職缺與人才基準的視覺化。摘要沒有給出數字，因此本頁不引用任何數字。需要與基準模型比較的讀者，應參閱論文的實驗章節。

## 限制

- **目標偏誤。** 標籤是過去的決策。以此訓練的模型會學到這些決策，包括其中的歧視，亞馬遜案例正是如此（見[演算法偏見案例研究](../../../society/ethics/bias-case-studies.md)）。
- **只看文字。** 模型只讀取履歷與職缺中寫下的內容。它無法看見候選人具備但未寫出的技能，而且可能獎勵那些履歷寫法與過去錄用者相似的人。
- **已過時的架構。** 卷積編碼器之後已被 Transformer 語言模型（例如 BERT，Devlin 等人 2019）超越，後者是較新的文字比對工作的常見起點（見[Transformer](../../../theory/models/transformer/index.md)）。
- **要求層級的解釋。** 解釋的品質受限於職缺說明本身。模糊或誇大的要求，只會產生模糊的解釋。

## 開放問題

- 若以經過公平性審查修正的結果（例如績效而非錄用）來訓練，模型能否學到更好的契合概念？
- 要求層級的分數在不同語言與職業之間，以及面對為了符合職缺而寫的對抗性履歷時，表現如何？
- 應如何向招募人員呈現契合分數，使其支援而非取代決策（見[人機互動](../../../society/human-ai-interaction/index.md)）？

## 參考文獻

### 開創性論文

- Zhu, C. et al. (2018). *Person-Job Fit: Adapting the Right Talent for the Right Job with Joint Representation Learning*. arXiv 預印本. https://arxiv.org/abs/1810.04040 — 原始論文，提出用於候選人與要求比對的二部、階層式 PJFNN。
- Kim, Y. (2014). *Convolutional Neural Networks for Sentence Classification*. arXiv 預印本. https://arxiv.org/abs/1408.5882 — 顯示以詞嵌入為輸入的簡單卷積網路，在句子分類上表現良好，是用於職缺與履歷的文字編碼器的一類。
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv 預印本（2018）；NAACL 2019. https://arxiv.org/abs/1810.04805 — 預訓練的雙向 Transformer 編碼器，在許多文字比對系統中取代了針對任務設計的卷積編碼器。

### 綜述與教科書

- Mehrabi, N. et al. (2019). *A Survey on Bias and Fairness in Machine Learning*. arXiv 預印本. https://arxiv.org/abs/1908.09635 — 綜述偏見的來源與公平性定義，與任何以歷史招募決策訓練的模型都相關。

### 文章與文件

- Decorte, J.-J. et al. (2021). *JobBERT: Understanding Job Titles through Skills*. arXiv 預印本. https://arxiv.org/abs/2109.09605 — 以職缺中的技能來表示職稱，是比對要求與候選人的相關做法。
- Wilson, K. & Caliskan, A. (2024). *Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval*. arXiv 預印本. https://arxiv.org/abs/2407.20371 — 稽核顯示，學習而來的履歷與職缺比對，可能系統性地偏好某些姓名。
- Raghavan, M. et al. (2020). *Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices*. FAT* 2020. https://arxiv.org/abs/1906.09208 — 檢視演算法評估廠商所揭露的效度與偏見測試資訊。
