---
related:
  - engineering/evaluation
  - theory/models/llm
tags:
  - evaluation
  - benchmarks
  - language
  - scaling
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - BIG-bench
  - Beyond the Imitation Game
  - 超越模仿遊戲基準
  - 大型基準
---

# BIG-bench

BIG-bench（超越模仿遊戲基準）是一組由 204 項任務組成的集合，用來衡量語言模型能做什麼，以及它的表現如何隨規模變化。這些任務由來自 132 個機構的 450 位作者共同撰寫。作者設計它的目的，是探測當時的語言模型可能還做不到的能力（Srivastava et al., 2022）。

## 任務與資料

多數語言基準只來自單一來源，例如一組考題或一組句子對。BIG-bench 則把許多獨立任務匯集成一個套件，每項任務都由一位想測量特定能力的貢獻者撰寫。這些任務涵蓋相當廣的主題。論文摘要指出，任務是為了針對目前模型被認為做不到的能力而選定（Srivastava et al., 2022）。

由於任務彼此差異很大，這個套件不像 GLUE 或 MMLU 那樣用單一分數總結。每項任務各自保留指標，結果則按任務逐項報告，再加以彙總。

## 協定與指標

作者評估了三類模型：OpenAI 的 GPT 模型、Google 內部的稠密 Transformer，以及稀疏的 Switch 式 Transformer。模型規模從數百萬到數千億參數不等。專家人類評分者也完成了所有任務，為每項任務提供人類的參照點（Srivastava et al., 2022）。

每項任務的指標由其作者選定，因此應謹慎看待套件的單一總分。大部分資訊都在逐項結果中。

## 它能說明什麼

主要發現是：表現與校準度會隨規模提升，但絕對分數仍然很低，並且遠低於專家評分者的水準。三類模型的表現相當接近，稀疏性帶來的好處很小（Srivastava et al., 2022）。

論文區分了兩種規模行為：

- **平滑且可預測的任務。** 分數隨模型變大而逐步上升。這類任務通常含有大量知識或記憶成分。
- **突破型任務。** 在某個臨界規模時分數急劇上升。這類任務常涉及多個步驟或組件，或指標不穩定。

作者也報告，在模稜兩可的情境中，偏見通常隨規模增加，而提示詞可以降低偏見（Srivastava et al., 2022）。

之後，突破現象被當作一般現象來研究。Wei et al.（2022）把湧現能力定義為：較大模型具備、較小模型不具備的能力，因此無法從小模型的表現外推而預測（Wei et al., 2022）。

## 限制

- **指標不一致。** 各項任務的分數尺度不同，平均之後會掩蓋任務之間的大差異。
- **不穩定的突破。** 論文指出，突破型行為常伴隨不穩定的指標。因此，一次急遽的跳升可能部分反映了任務的計分方式，而非模型本身的改變。
- **人類基準。** 專家評分者是很強的參照點，但這個基準反映的是實際參與任務的評分者的能力。
- **協定敏感。** 與其他以提示詞為基礎的基準一樣，提示格式與答案擷取方式會改變分數，因此每個結果都必須連同協定一起報告。

## 相關連結

- [GPT-3](../../../models/llm/gpt-3-few-shot/index.md) 是此套件評估的模型家族之一，它的少樣本結果推動了後續大量的基準測試。
- [尺度定律](../../../models/llm/scaling-laws/index.md) 描述損失如何隨計算量下降，而 BIG-bench 探討任務分數如何隨規模變化。損失與任務分數是不同的量，因此兩種觀點回答的是不同的問題。
- [計算最佳化訓練](../../../models/llm/compute-optimal-training/index.md) 說明模型大小與資料預算如何影響同一組基準分數。
- [MMLU](mmlu.md) 是固定的選擇題基準，與 BIG-bench 開放式的任務集合形成對比。
- [HELM](../../../../engineering/evaluation/helm.md) 同時在許多情境與指標上評估語言模型，以另一種方式處理指標不一致的問題。

## 應用

當新的模型家族問世時，BIG-bench 常被用作廣泛的測試平台。它可以顯示模型隨規模成長時在哪些能力上有所進展，又在哪些能力上沒有進展。

## 未解問題

- 突破型行為反映的是模型能力真的改變，還是指標改變。論文以不穩定的指標作為原因之一，但這個問題尚未解決。
- 如何把異質的任務彙總成一個不會掩蓋重要差異的衡量指標。
- 公開的套件有多少內容已進入預訓練資料，因為公開的題目可能被記憶。

## 參考文獻

### 開創性論文

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 提出 204 項任務的套件、專家人類基準，以及本頁摘要的規模結果。
- Wei, J. et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — 將湧現能力定義為較大模型具備、較小模型不具備的能力，並主張它們無法透過外推預測。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 模型家族，是 BIG-bench 評估的三類模型之一。

### 綜述與基準

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 在 16 個核心情境上測量七項指標，是與 BIG-bench 逐項計分相對的多指標設計。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 涵蓋 57 個科目的固定選擇題基準，與開放式任務集合形成對比。
