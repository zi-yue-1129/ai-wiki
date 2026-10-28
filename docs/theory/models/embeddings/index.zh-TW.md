---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised/index.md
  - brain-mind/neuroai
---

# 嵌入表示與表徵學習（Embeddings and Representation Learning）

嵌入（embedding）把一個物件（例如詞、句子、影像、使用者、圖的節點）映射到一個向量，使向量空間的幾何結構反映任務所關心的相似性。一旦物件位於這樣的空間中，距離、夾角與簡單的線性運算就成為搜尋、分群、分類與推薦的有用工具。由學習得到嵌入，而非手工設計，正是嵌入成為現代 AI 核心的原因。

## 概述

Bengio、Courville 與 Vincent（2012）把問題表述為*表徵學習*：找到一種輸入的轉換，使特徵能用於之後的許多任務。他們的綜述主張，好的表徵通常是分散式的，也就是每個概念分散在許多單元上，並且能解開資料中變動的因素。嵌入是這種表徵最常見的具體形式：一個固定長度的向量，可以直接儲存與比較。

同樣的想法出現在各種模態中。詞嵌入把用法相近的詞放在彼此附近。句子嵌入把整段文字放進同一個空間，使其可以比較。影像—文字嵌入把圖片與說明文字放在同一空間。訓練訊號決定了幾何結構的意義，而這個選擇是主要的設計決定。

## 關鍵概念

- **嵌入表（embedding table）**：從離散項目（例如詞的編號）到學習得到的向量的查找表。
- **相似度**：通常在正規化後使用餘弦相似度或內積來衡量兩個向量。
- **對比目標**：把匹配的配對拉近、把不匹配的配對推遠的損失函數。
- **三元組損失（triplet loss）**：針對一個錨點、一個正例與一個負例的損失，要求錨點與正例的距離比與負例近至少一個邊界值。
- **維度**：向量的長度。維度越高能容納的資訊越多，但儲存與搜尋的成本也越高。

## 運作方式

四種訓練訊號涵蓋了目前使用中的大多數嵌入。

**由上下文預測。** word2vec（Mikolov 等人，2013）透過由鄰近詞預測詞，從大型文字語料中學習詞向量。在相似上下文中出現的詞，會得到相似的向量。論文的目標是讓這樣的訓練有效率到能在極大的語料上執行。

**分解共現計數。** GloVe（Pennington、Socher 與 Manning，2014）從全域的詞與詞共現統計出發，學習內積能反映這些統計的向量。它結合了較早的計數方法所用的全域計數，以及預測方法的向量結構。

**度量學習。** FaceNet（Schroff 等人，2015）訓練一個深度卷積網路，把人臉影像映射到一個距離反映身分的空間。論文以三元組式的目標直接訓練嵌入本身，使同一人的距離比不同人近至少一個邊界值。學到的向量隨後直接用於辨識與分群。

**對齊模態與句子。** Sentence-BERT（Reimers 與 Gurevych，2019）把預先訓練的 Transformer 改造為孿生網路，使句子只需嵌入一次，即可用餘弦相似度比較，而不必兩兩成對地通過模型。CLIP（Radford 等人，2021）從自然語言監督中學習影像與文字編碼器，使配對的影像與說明文字具有相近的嵌入，並可透過把影像與文字提示比較，進行零樣本分類。

## 關鍵方法

簡要比較。上面提到的每個方法都可以有自己的方法頁面；這些頁面尚未撰寫，因此目前在本節提供細節。

- **word2vec（由上下文預測）**：局部上下文預測，在大型文字上很快。產生靜態詞向量，每個詞一個。
- **GloVe（共現分解）**：全域計數，產生靜態詞向量。角色與 word2vec 相近，但得到向量的路徑不同。
- **FaceNet（度量學習）**：為身分學得的嵌入，以三元組式目標訓練。專門用於實例之間的比較。
- **Sentence-BERT（孿生編碼器）**：可快速比較的上下文句子向量。為相似度而訓練，而非為生成而訓練。
- **CLIP（模態對齊）**：由配對資料學得的影像與文字共享空間。

## 關聯

嵌入是一側的 [Transformer](../transformer/index.md) 與[大型語言模型](../llm/index.md)，與另一側的檢索、推薦與多模態系統之間的橋樑。自監督預訓練通常是訓練訊號的來源，見[自監督學習](../../paradigms/self-supervised/index.md)。影像—文字嵌入是[多模態模型](../multimodal/index.md)的核心。

分散式表徵在神經科學中有悠久的歷史。群體編碼（population code）中，刺激由許多神經元的聯合活動來表示，是嵌入向量的自然對應；神經群體活動的相似性結構與模型表徵之間的比較，則在 [NeuroAI](../../../brain-mind/neuroai/index.md) 中討論。這種比較是有待檢驗的假說，而非已確立的等價關係。

## 應用

- **搜尋與檢索。** 在嵌入上做最近鄰搜尋，可找出與查詢相似的文件、影像或商品。
- **推薦。** 使用者與項目被嵌入，使分數就是它們之間的相似度。
- **人臉辨識與分群。** 類 FaceNet 的嵌入以距離比較身分。
- **零樣本分類。** 透過把影像嵌入與各類別的文字描述比較，來進行分類。

## 開放問題

- 靜態嵌入不論詞義為何，都只給一個詞一個向量。情境嵌入能解決這個問題，但每次使用都要重新計算。
- 嵌入空間的幾何結構意味著什麼很難解讀，而相似性可能編碼了訓練資料中的偏見。
- 嵌入的有用程度有多少來自資料的規模，有多少來自訓練目標，目前仍不清楚。

## 參考文獻

### 開創性論文

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — 提出從大型語料高效訓練詞向量的方法，是 word2vec 的基礎。
- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — 從全域共現統計學習詞向量。
- Schroff, F., Kalenichenko, D. & Philbin, J. (2015). *FaceNet: A Unified Embedding for Face Recognition and Clustering*. arXiv. https://arxiv.org/abs/1503.03832 — 以三元組式目標訓練深度網路，直接把人臉影像嵌入向量空間。
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — 產生可用餘弦相似度比較的句子嵌入，不需兩兩成對通過模型。
- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — CLIP：從自然語言監督學得的影像與文字嵌入，具零樣本遷移能力。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 表徵學習的綜述，以及使表徵有用的性質。
