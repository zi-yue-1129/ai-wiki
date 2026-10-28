---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - neuroscience
---

# Brain-Score

Brain-Score 是以人工神經網路的內部反應，預測靈長類視覺皮層神經記錄與物體辨識行為資料的能力來評分的基準（Schrimpf et al., 2018）。它問的是模型表徵與量測反應有多接近，而不只是它能否正確分類影像。

## 任務與資料

模型看到的影像與動物看過的相同。模型的內部反應被映射到記錄到的神經反應，分數衡量這個映射在留出影像上預測反應的能力（Schrimpf et al., 2018）。

## 協定與指標

可預測性是留出影像上預測反應與量測反應之間的相關係數，並跨記錄位點彙總。所選的層、迴歸方法與神經資料集都會影響分數，因此每一項都必須報告。

## 它能說明什麼

它顯示模型表徵與量測到的神經與行為反應，在物體辨識上有多相符。可預測性高是相似性的證據，不是共享機制的證明。早先的研究發現，為辨識而最佳化的模型能預測高階視覺皮層的反應（Yamins et al., 2014）。

## 限制

- **彈性映射。** 彈性的迴歸可能擬合雜訊，因此映射必須受約束並經過驗證。
- **資料有限。** 記錄只涵蓋少數位點與影像，因此分數的不確定性很大。
- **單一任務。** 靜態影像上的物體辨識無法涵蓋大腦功能的完整範圍。

## 相關

- [神經科學概述](index.md) 說明神經科學基準。
- [ImageNet](../vision/imagenet.md) 是許多被評分模型所訓練的分類基準。

## 參考文獻

### 開創性論文

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — 介紹基準及其神經與行為分數。
- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — 顯示物體辨識模型能預測高階視覺皮層的反應。

### 文章與文件

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。

### 補充來源

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，揭露其取捨。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
