---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
aliases:
  - ESM-2
  - ESM2
  - 蛋白質語言模型
---

# ESM-2（Lin 等人，2023）

ESM-2 是一個只在蛋白質序列上訓練的 Transformer 語言模型。它的內部表徵帶有蛋白質結構的資訊，因此同一個模型可以延伸用來預測結構。它是 [ESMFold](esmfold.md) 背後的序列模型，家族總覽見 [ESM-2 與 ESMFold](index.md) 頁面。

## 概況

蛋白質是一條胺基酸鏈，它的序列遠比三維結構容易取得。ESM-2 把語言模型的方法應用在這些序列上：它從許多蛋白質的序列中學習統計模式，就像語言模型從文字中學習一樣。

## 問題

定序已揭示的蛋白質序列數量遠多於已知結構的數量。若能只從序列中擷取結構資訊，速度會比實驗方法快得多，而且不需要依賴比對的預測器所搜尋的序列資料庫。

## 關鍵概念

- **蛋白質語言模型**：在胺基酸序列上訓練的模型，每個殘基扮演類似單字的角色。
- **遮罩式語言模型**：序列的部分位置被遮住，模型根據其餘部分預測被遮住的內容。較早的 ESM 模型即以此方式訓練（Rives et al., 2021）。
- **嵌入（embedding）**：模型為每個殘基產生的向量，下游模型會讀取這些向量。
- **規模**：預印本訓練的模型參數從 800 萬到 150 億不等。

## 核心想法

在許多序列上訓練的語言模型會學到演化模式。預印本報告指出，當模型規模擴大時，其表徵所含的資訊足以預測原子解析度的結構。建立在它之上的結構預測器就是 [ESMFold](esmfold.md)。

## 演算法

訓練遵循遮罩詞元目標：

1. 從訓練資料中取樣一條蛋白質序列。
2. 遮住其中一部分殘基。
3. 根據周圍的序列，用 Transformer 編碼器預測被遮住的殘基；其自注意力機制讓每個殘基都能與其他所有殘基互動。
4. 更新參數，以降低被遮住殘基的預測誤差。

訓練損失是被遮住位置 \(M\) 上的交叉熵：

```latex
\mathcal{L} = -\sum_{i \in M} \log p_\theta(x_i \mid x_{\setminus M})
```

## 結果

預印本報告指出，擴大模型規模後，其表徵足以預測原子解析度的結構。各模型大小的具體數字在論文中，這裡不再重述。最終數字應以正式發表於 *Science* 的版本為準。

## 限制

- 這裡描述的結果來自預印本，*Science* 版本取代其數字。
- 模型從序列資料庫中的模式學習。已知近親很少的蛋白質，可能提供較少的資訊可供學習（這是推論，並非論文的結論）。
- 良好的嵌入本身並不能保證得到可靠的三維形狀。結構是由其上的摺疊頭產生的，該頭部也有其限制（見 [ESMFold](esmfold.md)）。

## 相關連結

- [ESMFold](esmfold.md)：建立在此模型之上的結構預測器。
- [Transformer](../../../theory/models/transformer/attention-is-all-you-need/index.md)：ESM-2 使用的架構，以殘基而非單字之間的自注意力運作。
- [AlphaFold 2](../alphafold-2.md)：依賴比對的結構預測器，這個家族通常拿來與之比較。
- 腦與心智：沒有直接關聯。此模型從序列統計中學習，並不模擬神經活動。

## 應用

- **結構預測**：ESM Metagenomic Atlas 是以 ESMFold 建立在 ESM-2 之上所得，是最主要的大規模應用（見 [ESMFold](esmfold.md)）。
- **蛋白質表徵**：較早的 ESM 工作報告指出，在這些表徵之上訓練的簡單模型，可以預測結構接觸與其他蛋白質性質（Rives et al., 2021）。

## 開放問題

- 學到的結構知識中，有多少是通用的，又有多少來自訓練資料中的近親。
- 進一步擴大規模是否仍會持續改善結果，以及代價多少運算量。

## 參考文獻

### 開創性論文

- Lin et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. https://doi.org/10.1126/science.ade2574 — 正式發表版本，介紹 ESM-2 與 ESMFold。
- Lin et al. (2022). Evolutionary-scale prediction of atomic level protein structure with a language model. *bioRxiv*. https://doi.org/10.1101/2022.07.20.500902 — 本頁數字所依據的預印本。
- Rives et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*. https://doi.org/10.1073/pnas.2016239118 — 較早的 ESM 工作，顯示以序列進行語言模型訓練會浮現與結構相關的資訊。
- Jumper et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2，參照用的結構預測器。
- Vaswani et al. (2017). Attention Is All You Need. arXiv. https://arxiv.org/abs/1706.03762 — 提出 ESM-2 所建立於其上的 Transformer 架構。
