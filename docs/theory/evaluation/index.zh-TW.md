---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - metrics
---

# 評估

評估要回答的是：模型好不好、好在哪個意義上，以及這個數字能信到什麼程度。本區涵蓋一般理論：哪個指標回答哪個問題、如何進行公平的比較，以及基準分數能說明什麼、又不能說明什麼。

語言模型與應用層級的實務指引見[評估與基準](../../engineering/evaluation/index.md)。具名資料集的清單見[資料集](../../reference/datasets/index.md)。

## 每個結果的三個組成部分

每一次評估都由三個部分組成：

- **指標**：由預測與正確答案計算出的一個數字；
- **資料集**：指標所計算的範例；
- **協定**：資料如何切分、保留哪些資料不用於決策，以及如何報告不確定性。

只有三者都說明清楚，結果才可以解讀。任何一項改變（例如切分方式、決策門檻或提示詞），都可能使兩個方法的排名反轉。

## 各頁

| 頁面 | 核心問題 |
|---|---|
| [指標](metrics/index.md) | 哪個數字符合要做的決定：準確率、排序品質、校準，還是誤差大小？ |
| [評估協定](protocols/index.md) | 如何切分資料、比較方法並報告不確定性，而不自欺？ |
| [基準測試](benchmarks/index.md) | 哪個具名測試衡量什麼，而它的分數能說明什麼？ |

具名基準依任務分組，每個基準一頁，見[基準測試](benchmarks/index.md)。語言模型基準的實務指引，請見[評估與基準](../../engineering/evaluation/index.md)。

## 這個主題已在其他地方出現

- 監督式學習的指標與驗證，已在[評估與驗證](../paradigms/supervised/evaluation-and-validation/index.md)中深入說明。
- 少樣本基準見[基準與基礎模型](../paradigms/meta-learning/benchmarks-and-foundation-models/index.md)。
- 持續學習的評估情境見[評估與情境](../paradigms/continual/evaluation-and-scenarios/index.md)。
- 自監督學習的理論與評估見[理論與評估](../paradigms/self-supervised/theory-and-evaluation/index.md)。

## 核心觀念

- **構念效度。** 分數只能作為它設計來衡量的性質的證據。基準分數高，並不能證明系統在每種情境中都有用（Raji et al., 2021）。
- **保留資料。** 只有在測試集沒有被用來做任何決策時，它才有資訊量。反覆依測試集挑選，會讓它變成開發資料。
- **記憶化。** 大型網路能擬合隨機標籤，因此訓練分數高，並不代表泛化能力好（Zhang et al., 2017）。
- **不確定性。** 小型測試集上相差幾個百分點，可能只是雜訊。應報告測試集大小與區間。
- **可比較性。** 只有指標與協定相同時，兩個數字才可以比較。

## 與其他概念的連結

信度、效度與題目反應理論等心理計量學傳統，是許多這些觀念更早的來源。認知面的內容見[心理學與 AI](../../brain-mind/psychology/index.md)。

## 開放問題

基準會飽和，而預訓練資料中可能包含基準的測試題目。模型評審的分數會繼承評審的偏誤。如何評估會隨時間改變的系統，或需要多步驟行動的系統，目前仍無定論。

## 參考文獻

### 開創性論文

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及根據基準表現做出廣泛主張的限制。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — 跨多個情境與指標評估語言模型，揭露能力缺口與取捨。
- Zhang, C. et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示網路可以記住隨機標籤，因此保留測試集不可或缺。

### 文章與文件

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — 研究以模型為基礎的評審、它與人類的一致性以及其偏誤。
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — 標準分類、迴歸與排序評分器及其定義的參考。
