---
translation_reviewed: 2026-10-28
---

# 零樣本知識蒸餾

零樣本知識蒸餾（ZSKD）在完全沒有訓練資料的情況下蒸餾網路。Nayak 等人只從教師合成替代樣本：最佳化輸入，使教師有信心且樣本多樣，然後在這些樣本上訓練學生。它是一種[無資料](../index.zh-TW.md)方法，作者報告其表現與在真實訓練資料上的蒸餾相當。

## 問題

蒸餾需要訓練資料，但已釋出的模型可能拿不到這些資料，或資料本身是私密的。

## 核心想法

從教師生成替代樣本。從隨機雜訊開始，最佳化輸入，使教師以高信心把它歸為某個選定的類別，並加入鼓勵各類別之間多樣性的項。學生接著以一般的蒸餾損失從這些樣本學習。

## 公式或演算法

輸入從雜訊開始最佳化，以提高教師對所抽樣類別的信心，並加入一個保持樣本多樣性的項。學生在合成樣本上，以[Hinton 蒸餾](../../response-based/hinton-distillation/index.zh-TW.md)的軟目標訓練。

## 結果

作者表示，在多個基準上，此框架的泛化表現與使用真實訓練資料的蒸餾具有競爭力。

## 限制

合成過程成本高，品質取決於教師的輸出能否刻畫資料。論文的基準是影像分類。

## 開放問題與相關變體

- **語言模型。** 離散的 token 比連續的影像更難最佳化，因此為語言合成樣本仍是開放問題。
- **相關：** [序列層級蒸餾](../../llm-distillation/sequence-level/index.zh-TW.md)是語言序列模型的部分無資料方法，仍使用來源句子。

## 相關連結

無資料蒸餾涉及隱私，這在[倫理](../../../../../society/ethics/index.zh-TW.md)與[治理](../../../../../society/governance/index.zh-TW.md)頁討論。

## 參考文獻

### 開創性論文

- Nayak, G. K., Mopuri, K. R., Shaj, V., Babu, R. V., Chakraborty, A. (2019). *Zero-Shot Knowledge Distillation in Deep Networks*. arXiv:1905.08114. https://arxiv.org/abs/1905.08114 — 從教師單獨生成的合成樣本蒸餾網路，表現與真實資料相當。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 標準的蒸餾目標，零樣本方法在合成樣本上使用它。
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — 部分無資料的序列蒸餾方法，對翻譯模型有效。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾設定，包括沒有資料的情況。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 使用真實資料的語言模型蒸餾，是與合成資料方法對照的例子。
