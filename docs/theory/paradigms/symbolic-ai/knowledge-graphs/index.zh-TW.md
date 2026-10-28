---
translation_reviewed: 2026-10-28
---

# 知識圖譜與知識表示

知識圖譜以圖的形式儲存事實：實體之間以帶標籤的關係相連，通常寫成 (主體, 關係, 客體) 形式的三元組。知識表示則研究如何寫下這些事實及其意義，使機器能夠使用。本頁是[符號 AI、搜尋與規劃](../index.md)的一部分。

## 概述

符號 AI 以規則與邏輯表示知識，這些表示精確，但在大規模下難以建立與維護。知識圖譜走的是較偏向資料的路線：儲存大量簡單的事實，這些事實常由文字與資料庫擷取，並附上一個本體（ontology），說明允許哪些類型的實體與關係。搜尋引擎的答案面板背後，就是以這種方式建立的大型公開圖譜。

## 關鍵概念

- **三元組**：例如 (巴黎, 首都是, 法國) 這樣的事實。圖即是在共同詞彙上的三元組集合。
- **本體或綱要**：實體的類別與它們之間的關係，並附上定義域與值域等約束。
- **描述邏輯**：一階邏輯中可判定的片段，是網路本體語言的基礎。它在表達力與推理成本之間取得平衡（Hogan 等人，2021）。
- **知識圖譜補全**：從既有圖預測缺少的三元組，通常稱為連結預測（link prediction）。

## 運作方式

知識圖譜有兩種用法。符號式用法是對明確的事實與本體進行查詢與推理，例如推論子類別會繼承父類別的屬性。統計式用法則把實體與關係轉為向量，並為候選三元組打分。第二種做法是[知識圖譜嵌入](transe.md)的基礎，這類方法從學得的表示來預測缺少的連結（Nickel 等人，2016）。

## 主要方法

- [TransE](transe.md)：把關係表示為實體嵌入之間的平移，使真實的三元組滿足「主體加關係接近客體」（Bordes 等人，2013）。

其他嵌入模型使用不同的評分函數，例如複數值評分（Trouillon 等人，2016），並在綜述文獻中有摘要（Wang 等人，2017；Nickel 等人，2016）。

## 與其他頁面的連結

- [符號 AI、搜尋與規劃](../index.md)把知識表示與搜尋、規劃、定理證明放在一起說明。
- [神經符號 AI](../neuro-symbolic/index.md)把知識圖譜或邏輯規則與神經學習結合。
- [機率與統計](../../../math/probability-statistics/index.md)提供某些知識圖譜所用的不確定事實之機率觀點。

## 應用

- **搜尋與問答**：答案面板直接從圖中給出某實體的事實。
- **推薦**：把使用者、項目與屬性連結起來的圖，用來解釋並排序推薦結果。
- **生物醫學**：由基因、藥物與疾病組成的圖，用來提出值得研究的新假說。

## 開放問題

- 知識圖譜本來就不完整，封閉世界與開放世界假設對缺失事實的解讀不同。
- 嵌入方法主要以少數基準上的連結預測來評估，還需要更好的方式來評估它們所預測的事實。
- 讓學得的表示同時遵守本體的邏輯約束，仍然困難。

## 參考文獻

### 奠基性論文

- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — 提出用於知識圖譜嵌入的 TransE。
- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — 以複數值嵌入建模非對稱關係。

### 綜述與教科書

- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — 知識圖譜模型、本體與推理的廣泛綜述。
- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — 回顧用於預測知識圖譜中連結的統計方法。
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — 綜述嵌入方法及其應用。
