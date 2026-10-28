---
references: not-required  # lists and meta pages cite through their entries
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
aliases:
  - 模型與發表時間軸
  - Model timeline
  - AI timeline
---

# 模型與發表時間軸

AI 的重要里程碑依時間排列，從感知器到大型語言模型。這是讓你把某個模型放回其時代脈絡的起點，而不是完整的歷史。每一列都連結到能夠說明其日期的來源。

## 日期的計算方式

論文往往在期刊正式發表之前就已公開，因此每個日期都是該列所列來源的第一個公開版本：

- **預印本**使用第 1 版的 arXiv 投稿日期。
- **期刊論文**使用線上發表日期。正式的期刊卷期日期可能更晚。
- **會議論文**使用會議年份。
- **公司發表**使用公告日期。

## 重要里程碑

| 日期 | 里程碑 | 為何重要 | 來源 |
|---|---|---|---|
| 1958 | 感知器 | Rosenblatt 將感知器提出為大腦中資訊儲存與組織的機率模型 | [Rosenblatt, *Psychological Review* 65(6)](https://doi.org/10.1037/h0042519) |
| 1986 | 反向傳播 | Rumelhart、Hinton 與 Williams 描述如何透過多層網路，以反向傳播誤差來學習表徵 | [Rumelhart et al., *Nature* 323](https://doi.org/10.1038/323533a0) |
| 1998 | 用於文件的卷積網路 | LeCun 等人提出以梯度為基礎的學習方法來辨識文件，屬於卷積式的做法 | [LeCun et al., *Proc. IEEE* 86(11)](https://doi.org/10.1109/5.726791) |
| 2012 | AlexNet | 在 ImageNet 分類任務上訓練的深層卷積網路 | [Krizhevsky, Sutskever & Hinton, NIPS 2012](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) |
| 2013 | 詞向量 | 從大型文字語料中學習有效率的詞表示 | [Mikolov et al., arXiv:1301.3781](https://arxiv.org/abs/1301.3781) |
| 2014 | 序列到序列 | 編碼器—解碼器網路在序列之間進行翻譯，見[序列到序列](../../theory/models/rnn/sequence-modes/sequence-to-sequence/index.zh-TW.md) | [Sutskever et al., arXiv:1409.3215](https://arxiv.org/abs/1409.3215) |
| 2015 | 深度 Q 網路 | 透過深度強化學習，從原始畫面在 Atari 遊戲中達到人類水準的控制 | [Mnih et al., *Nature* 518](https://doi.org/10.1038/nature14236) |
| 2015 | 殘差網路 | 跳接連線讓極深的網路得以訓練 | [He et al., arXiv:1512.03385](https://arxiv.org/abs/1512.03385) |
| 2016 | AlphaGo | 深度神經網路結合樹搜尋，下圍棋 | [Silver et al., *Nature* 529](https://doi.org/10.1038/nature16961) |
| 2017 | Transformer | 自注意力取代遞迴，見 [Attention Is All You Need](../../theory/models/transformer/attention-is-all-you-need/index.zh-TW.md) | [Vaswani et al., arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| 2018 | BERT | 以雙向預訓練的 Transformer 編碼器來理解語言 | [Devlin et al., arXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| 2020 | GPT-3 | 大型語言模型，能在提示中以少量範例完成任務，見 [GPT-3 少樣本](../../theory/models/llm/gpt-3-few-shot/index.zh-TW.md) | [Brown et al., arXiv:2005.14165](https://arxiv.org/abs/2005.14165) |
| 2020 | 去噪擴散 | 訓練一個生成模型來逆轉逐步加噪的過程 | [Ho et al., arXiv:2006.11239](https://arxiv.org/abs/2006.11239) |
| 2021 | AlphaFold 2 | 從序列高精度預測蛋白質結構 | [Jumper et al., *Nature* 596](https://doi.org/10.1038/s41586-021-03819-2) |
| 2021 | 潛在擴散 | 在壓縮的潛在空間中進行擴散，合成高解析度影像 | [Rombach et al., arXiv:2112.10752](https://arxiv.org/abs/2112.10752) |
| 2022 | 運算最佳化訓練 | Chinchilla 主張模型大小與訓練權杖數應一同放大，見[運算最佳化訓練](../../theory/models/llm/compute-optimal-training/index.zh-TW.md) | [Hoffmann et al., arXiv:2203.15556](https://arxiv.org/abs/2203.15556) |
| 2022 | ChatGPT | 與 InstructGPT 相關的對話模型，開放免費的公開測試 | [OpenAI, "Introducing ChatGPT"](https://openai.com/index/chatgpt/) |
| 2023 | GPT-4 | 大型模型，其技術報告說明能力與評估 | [OpenAI, arXiv:2303.08774](https://arxiv.org/abs/2303.08774) |
| 2023 | Llama 2 | 開放的基礎模型與微調後的對話模型，見其技術報告 | [Touvron et al., arXiv:2307.09288](https://arxiv.org/abs/2307.09288) |

## 與其他主題的連結

- 這些里程碑背後的模型家族，見[模型](../../theory/models/index.zh-TW.md)，包括 [Transformer](../../theory/models/transformer/index.zh-TW.md)、[CNN](../../theory/models/cnn/index.zh-TW.md)、[RNN](../../theory/models/rnn/index.zh-TW.md) 與 [LLM](../../theory/models/llm/index.zh-TW.md)。
- 許多發表背後的人物與團體，見[人物與研究室](../people-and-labs/index.zh-TW.md)。

## 開放問題

- 接下來應該補上哪些里程碑？如何讓時間軸保持更新，又不致變成所有發表的清單？
