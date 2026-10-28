---
translation_reviewed: 2026-10-28
---

# T5：以編碼器—解碼器進行文字到文字的遷移（Raffel et al., 2019）

T5 是一個編碼器—解碼器 Transformer，把每個語言任務都轉換成「文字進、文字出」的格式，並透過填補被移除的文字片段進行預訓練。它是 [Transformer 架構家族](../index.md)中具代表性的編碼器—解碼器模型。

## 概觀

到了 2019 年，NLP 的遷移學習對每個任務使用不同的輸出頭、格式與目標。Raffel et al.（2019）為所有任務提出單一的介面：分類標籤、翻譯與摘要都寫成文字字串，並由同一個模型與損失函數處理。論文以這個框架，對目標、架構與語料做了系統性的研究。

他們建立了 Colossal Clean Crawled Corpus（C4），約 750 GB 經過清理的英文網路文字，並訓練了最多 110 億參數的模型。

T5 位於[架構家族](../index.md)中，介於僅編碼器的 [BERT](../bert/index.md) 與僅解碼器的 [GPT-3](../../../llm/gpt-3-few-shot/index.md) 之間。BART（Lewis et al., 2019）是近親，以文字重建方式訓練。編碼器—解碼器設計也用於語音，如 Whisper（Radford et al., 2022）；見[語音模型](../../../speech/index.md)。更大的脈絡見 [Transformers & Attention](../../index.md)。

## 關鍵概念

- **文字到文字格式。** 輸入以任務前綴開頭，例如「translate English to German:」，目標則是以文字寫出的答案。分類標籤也寫成文字，因此輸出格式不會改變。
- **編碼器—解碼器。** 依照 Vaswani et al.（2017）的標準 Transformer：對輸入進行雙向編碼，解碼器則是因果式的，並對編碼器輸出做交叉注意力。
- **片段破壞。** 一種去噪目標，把輸入中的連續 token 片段替換為哨兵 token，目標則是被移除的片段序列。
- **哨兵 token。** 標示某段文字被移除位置的特殊詞彙項目。

## 運作方式

最終模型使用的預訓練流程如下：

1. 從 C4 取出一段未標註的文字，並選出約 15% 的 token 進行破壞。
2. 把被選中的 token 分組為平均長度為三的連續片段。在輸入中，每個片段替換為一個哨兵 token。
3. 把目標建構為被移除的片段，每段前面接上其哨兵，最後再加上一個標示結束的哨兵。
4. 以教師強制（teacher forcing）方式訓練，對目標 token 計算交叉熵損失。
5. 下游任務時，把輸入與目標寫成帶有任務前綴的文字，並以相同格式微調。

論文中的一個例子：文字「Thank you for inviting me to your party last week」可被破壞成輸入「Thank you <X> me to your party <Y> week」，目標「<X> for inviting <Y> last <Z>」。其中哨兵標示被移除的片段，最後一個哨兵標示目標的結束。

連續片段的選擇，部分原因是為了降低運算成本，論文中也如此說明。

## 結果

論文的受控比較使用運算成本相同的模型。在架構與目標的表格中，採用去噪目標的編碼器—解碼器取得最高的 GLUE 平均分數（83.28）。使用相同去噪目標的僅解碼器語言模型得分為 74.70，而使用標準因果目標的僅解碼器語言模型得分為 73.78，是表中最低的 GLUE 數值。前綴語言模型是一種對前綴雙向、其餘部分因果式的僅解碼器模型，使用去噪目標時得分為 81.82。

在片段長度的掃描中，平均長度 2 到 5 在 GLUE 上的表現相近（83.40 至 83.54，對照獨立 token 的 83.28），長度 10 則為 82.85。最終模型使用的平均長度為三。

110 億參數的模型在所研究的各種尺寸中表現最好，摘要也報告在許多基準上達到最先進結果。

## 限制

- **兩個堆疊的成本。** 每個堆疊 *L* 層的編碼器—解碼器，參數量約為 *L* 層僅解碼器模型的兩倍，而運算量大致相當。
- **比較受規模影響。** 後續研究報告，在純無監督預訓練之後，採自迴歸預訓練的僅解碼器模型，對新任務的泛化最好（Wang et al., 2022）。T5 的比較是在特定的規模與預算下進行的。
- **固定的目標。** 片段破壞只是眾多去噪選擇之一，其優勢取決於設定。

## 未解問題

- 編碼器—解碼器在理解類任務上的優勢，在更大的規模下是否仍然存在？
- 能否以混合目標訓練單一模型，並在不同模式下使用？UL2（Tay et al., 2022）提出混合去噪器，並報告在多種設定下勝過 T5 與 GPT 式模型。

## 參考文獻

### 開創性論文

- Raffel, C., et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv；JMLR 2020. https://arxiv.org/abs/1910.10683 — 原始論文：文字到文字框架、C4 語料與受控比較。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — T5 以其為基礎架構的編碼器—解碼器 Transformer。
- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv；NAACL 2019. https://arxiv.org/abs/1810.04805 — 片段破壞所改編的遮罩目標。
- Lewis, M., et al. (2019). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*. arXiv；ACL 2020. https://arxiv.org/abs/1910.13461 — 透過破壞文字再重建來預訓練的編碼器—解碼器。
- Wang, T., et al. (2022). *What Language Model Architecture and Pretraining Objective Work Best for Zero-Shot Generalization?* arXiv. https://arxiv.org/abs/2204.05832 — 發現採自迴歸預訓練的僅解碼器模型，在零樣本上泛化最好。

### 綜述與教科書

- Tay, Y., et al. (2022). *UL2: Unifying Language Learning Paradigms*. arXiv；ICLR 2023. https://arxiv.org/abs/2205.05131 — 提出混合去噪器，報告在多種設定下勝過 T5 與 GPT 式模型。

### 文章與文件

- Radford, A., et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv；ICML 2023. https://arxiv.org/abs/2212.04356 — 介紹 Whisper，一個以編碼器—解碼器 Transformer 建構、以大規模網路音訊轉錄訓練的語音辨識系統。
