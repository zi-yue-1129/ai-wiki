---
translation_reviewed: 2026-10-28
---

# AlphaFold 2（Jumper 等人，2021）

AlphaFold 2 是一種神經網路，能從胺基酸序列預測蛋白質的三維結構。在 2020 年的 CASP14 評估中，其預測結果在多數情況下可與實驗測得的結構相比擬，因此成為[生命科學與藥物開發](index.md)中蛋白質結構研究的參照點。

## 概況

蛋白質是一條胺基酸鏈，會摺疊成特定的形狀，而這個形狀大致決定了蛋白質的功能。以實驗測定單一蛋白質的形狀，往往需要數月到數年。2021 年的論文指出，實驗研究已測定約 10 萬個不重複蛋白質的結構，但這只佔已知蛋白質序列（數十億條）的很小一部分。

## 問題

只從序列預測蛋白質結構，也就是蛋白質摺疊問題中的結構預測部分，已是超過 50 年的開放研究問題。在此之前的方法，尤其在找不到同源結構可供參考時，離原子級精確度還有很大差距。

## 核心想法

依論文的說法，AlphaFold 2 是「第一個能穩定地預測出原子級精確度蛋白質結構的計算方法，即使在沒有相似結構可參考的情況下也能做到」。論文描述的神經網路以多序列比對作為輸入，並把蛋白質結構的物理與生物學知識納入設計之中。

## 關鍵概念

- **多序列比對（MSA）**：一組在演化上相關的序列，逐位置對齊排列。論文將 MSA 列為核心輸入。
- **模板（template）**：與目標相關的已知蛋白質結構。釋出的 model_1 設定最多可使用四個模板。
- **配對表示（pair representation）**：一個表格，記錄網路對每一對殘基之間關係的估計。它與 MSA 表示一起被更新。
- **循環（recycling）**：網路的輸出會被回送作為輸入，再次處理。釋出的 model_1 設定執行三次循環迭代。
- **pLDDT**：每個殘基一個、範圍 0 到 100 的信心分數。釋出的程式碼以機率加權的分箱中心平均值乘以 100 計算它，並把分數標示為無序（0–50）、低（50–70）、中（70–90）或高（90–100）。

## 演算法

釋出的實作對 model_1 依序執行以下步驟：

1. **建立輸入。** 從序列資料庫為輸入序列建立 MSA，並可選擇從已知結構中取得模板。將兩者轉換為 MSA 表示與配對表示。
2. **Evoformer 堆疊。** 表示經過 48 個 Evoformer 區塊，每個區塊同時更新兩種表示。MSA 上的逐列注意力會受配對表示偏置，使演化資訊與殘基配對資訊彼此影響。
3. **結構模組。** 八層結構模組把最終表示轉換為每個原子的三維位置。
4. **循環。** 預測的位置與表示被回送到步驟 2 與 3。model_1 設定為三次循環迭代。
5. **評分。** 預測 LDDT 的輸出頭為每個殘基給出 pLDDT 分數。

## 結果

在盲測的結構預測評估 CASP14 中，論文報告其「在多數情況下，準確度可與實驗結構相比擬，並大幅超越其他方法」。各目標的分數見論文的結果章節，本頁不重述。

AlphaFold 蛋白質結構資料庫建立於 AlphaFold v2.0 之上，首次發布時收錄超過 36 萬筆預測結構，涵蓋 21 種模式生物的蛋白質體。作者規劃擴大收錄範圍，涵蓋超過 1 億筆代表性序列中的大部分。

## 限制

- **以單鏈為主。** 主要模型是為單條鏈設計的。釋出的程式碼另外提供 AlphaFold-Multimer 權重處理複合物，而 AlphaFold 3 之後把此方法擴展到包含核酸、小分子與離子的複合物。
- **信心分數是輸出的一部分。** pLDDT 較低的殘基，例如位於無序區間的殘基，不應被解讀為固定的形狀。
- **訓練資料截止日。** 原始訓練資料的截止日為 2018-04-30。v2.3.0 技術說明將新權重的截止日改為 2021-09-30，因此截止日之後新增的結構不在原始訓練資料中。

## 相關連結

- **注意力**：Evoformer 使用注意力機制，與語言模型中 [Transformer](../../theory/models/transformer/index.md) 所用的機制相同。它的注意力作用於殘基與序列位置，而非單字。
- **腦與心智**：沒有直接關聯。此方法以演化序列資料為基礎，並未模擬神經活動。
- **藥物發現**：關於結構預測在藥物發現中的應用，見[生命科學](index.md)頁面。

## 應用

- **結構生物學**：公開的 AlphaFold 蛋白質結構資料庫，讓研究者能取得整個蛋白質體的預測結構，並附有每個殘基與成對的信心估計。
- **法規脈絡**：美國 FDA 於 2025 年 1 月發布的草案指引，針對 AI 支持藥物與生物製劑監管決策的使用，涵蓋為藥物安全性、有效性或品質相關決策而產生資訊或資料的 AI。草案提出一套以風險為基礎的框架，用來判斷某個模型在特定使用情境下是否可信。FDA 頁面將指引的範圍限定於監管決策，並未提及藥物發現研究中使用的 AI。因此，僅用於早期研究的結構預測不在其所述範圍內；若預測結果用來支持監管決策，則屬於範圍之內。

## 開放問題

- **複合物與配體**：AlphaFold 3 將此方法擴展到包含核酸、小分子、離子與修飾殘基的複合物。準確度在這些情況下能延續到什麼程度，仍是活躍的研究問題。
- **不只一種形狀**：預測的結構是單一的構象。如何表示蛋白質所能採取的一系列形狀，仍未解決。

## 參考文獻

### 開創性論文

- Jumper, J. et al.（2021）. *Highly accurate protein structure prediction with AlphaFold*. *Nature* 596, 583–589. https://doi.org/10.1038/s41586-021-03819-2 — AlphaFold 2 論文：問題設定、CASP14 驗證與方法本身。
- Senior, A. W. et al.（2020）. *Improved protein structure prediction using potentials from deep learning*. *Nature* 577, 706–710. https://doi.org/10.1038/s41586-019-1923-7 — 較早的 AlphaFold 系統，以深度學習得到的勢能預測結構。

### 綜述與教科書

- Abramson, J. et al.（2024）. *Accurate structure prediction of biomolecular interactions with AlphaFold 3*. *Nature* 630, 493–500. https://doi.org/10.1038/s41586-024-07487-w — 後續模型，把此方法擴展到包含核酸、小分子與離子的複合物。

### 文章與技術文件

- Varadi, M. et al.（2022）. *AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models*. *Nucleic Acids Research* 50, D439–D444. https://doi.org/10.1093/nar/gkab1061 — 建立於 AlphaFold v2.0 之上的公開資料庫，包括首次發布與規劃中的擴充。
- Google DeepMind，*AlphaFold* 原始碼，`alphafold/model/config.py`、`alphafold/model/modules.py` 與 `alphafold/common/confidence.py`。https://github.com/google-deepmind/alphafold — 釋出的實作。model_1 設定定義了 Evoformer 深度、結構模組深度與循環次數，信心模組則定義 pLDDT。
- Google DeepMind，*AlphaFold v2.3.0 技術說明*。https://github.com/google-deepmind/alphafold/blob/main/docs/technical_note_v2.3.0.md — 新權重的發布說明，包括訓練截止日與 AlphaFold-Multimer 模型。
- 美國食品藥物管理局（FDA），*Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products*，草案指引（2025 年 1 月）。https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological — 草案指引的適用範圍與其以風險為基礎的可信度框架。

## 延伸學習

- [AlphaFold 蛋白質結構資料庫](https://alphafold.ebi.ac.uk/) — 搜尋與下載預測結構，並可查看每個殘基的信心分數。
