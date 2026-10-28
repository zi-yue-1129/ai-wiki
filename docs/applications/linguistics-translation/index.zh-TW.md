---
translation_reviewed: 2026-10-28
related:
  - theory/models/nlp
  - theory/models/transformer
  - brain-mind/attention-brain-machine
aliases:
  - 語言學與機器翻譯
  - Machine translation
  - Linguistics
---

# 語言學與機器翻譯

現在大部分的跨語言文字翻譯都由 AI 完成，AI 也越來越多地被用來研究語言本身。本頁說明 AI 在翻譯與語言學研究中的應用。底層的語言模型見[自然語言處理](../../theory/models/nlp/index.md)。

## 概況

| 領域 | 例子 |
|---|---|
| 文字翻譯 | 用於文件、網站與聊天的商用與開放神經機器翻譯 |
| 語音翻譯 | 把口語翻成文字或語音，用於旅遊與會議 |
| 語料庫語言學 | 大型標註語料庫，以及語法與語意的自動標記 |
| 低資源語言 | 書面資料很少的語言之翻譯與記錄 |
| 文學與專業翻譯 | 供譯者使用、需要人工審校的起草工具 |
| 語言學習 | 自動回饋語法、發音與詞彙 |

## 從規則到神經模型

機器翻譯最初依靠人工撰寫的規則，後來改用統計模型，從平行語料中學習片語之間的對應。這段時期的標準參考書是 Koehn 的教科書（見參考文獻）。大約從 2014 年起，神經模型已取代大部分的統計流程。

## 關鍵方法

有三個里程碑式的想法塑造了神經翻譯。每個都連結到解釋它的頁面。

- [用於對齊的注意力（Bahdanau 等人，2014）](../../theory/models/transformer/bahdanau-attention/index.md)：解碼器學會回頭查看與每個輸出詞最相關的來源詞。
- [Transformer（Vaswani 等人，2017）](../../theory/models/transformer/attention-is-all-you-need/index.md)：只用注意力取代遞迴，訓練更快，也是當前系統的基礎。
- 子詞單位：把罕見詞切成較小的片段，使詞彙表不必列出每一個詞（Sennrich 等人，2015，見參考文獻）。

## 低資源語言

世界上大多數語言的平行文本很少，用網路資料訓練的系統對它們的表現通常很差。NLLB 計畫（2022）建立了涵蓋 200 種語言的系統，其新資料集由訪談母語者而來。作者報告相較於先前系統有大幅進步，但高資源與低資源語言之間的品質差距仍在，而且單一基準無法說明系統對每個語言社群的實際表現。

## 評估

- BLEU 等自動分數比較系統輸出與參考譯文。它們與人類判斷只是粗略相關，參考譯文不足時可能產生誤導。
- 人工評估是發表的標準，但速度慢、成本高。
- 毒性基準等安全檢查，現已成為主要多語評估的一部分。

## 風險

- **高風險文本的錯誤。**醫療指示或法律條款被誤譯可能造成實際傷害，因此仍需專業人員審閱。
- **偏見與刻板印象**，來自訓練資料，例如職業相關的性別代名詞。
- **語言瀕危。**自動工具可能擴散優勢語言的規範，並減少記錄少數語言的誘因。

## 連結

- 翻譯中的注意力，是以大腦中的選擇性注意力為類比命名的。這個類比相當鬆散，見[大腦與機器中的注意力](../../brain-mind/attention-brain-machine/index.md)。
- 用於翻譯的語言模型，見[自然語言處理](../../theory/models/nlp/index.md)。

## 未解問題

- 翻譯系統如何處理沒有標準書寫系統的語言、方言與語碼轉換？
- 沒有單一正確答案時，如何衡量翻譯品質？
- 機器輔助翻譯能否改善人類譯者的工作，而不降低報酬或品質？

## 參考文獻

### 開創性論文

- Bahdanau, D., Cho, K. & Bengio, Y. (2014). Neural Machine Translation by Jointly Learning to Align and Translate. arXiv. https://arxiv.org/abs/1409.0473 — 提出來源詞與目標詞之間的可學習軟對齊，使模型不必把整個句子壓縮成一個固定向量。
- Vaswani, A. et al. (2017). Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，只用注意力，在訓練更快的同時提升翻譯品質。
- Sennrich, R., Haddow, B. & Birch, A. (2015). Neural Machine Translation of Rare Words with Subword Units. arXiv. https://arxiv.org/abs/1508.07909 — 把罕見詞切成子詞單位，使神經系統能翻譯未見過的詞。
- NLLB Team (2022). No Language Left Behind: Scaling Human-Centered Machine Translation. arXiv. https://arxiv.org/abs/2207.04672 — 涵蓋 200 種語言的翻譯系統，以新資料集建置，並在超過 40,000 種語言配對上進行公開評估。

### 教科書與綜述

- Koehn, P. (2009). *Statistical Machine Translation*. Cambridge University Press. https://www.cambridge.org/core/books/statistical-machine-translation/94EADF9F680558E13BE759997553CDE5 — 統計機器翻譯的教科書，涵蓋詞基、片語基與樹基模型，以及評估方法。
