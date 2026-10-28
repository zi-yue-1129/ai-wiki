---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
aliases:
  - Few-shot benchmarks
  - 少樣本基準
---

# 少樣本基準

少樣本基準測試學習者能否從少量有標籤的範例中辨識新類別。分數只有連同產生它的協定一起看才有意義：類別如何切分、每個類別給多少範例，以及平均了多少個隨機情節。

## 概述

大多數少樣本基準以一連串**情節**（episode）建構。在每個情節中，學習者先看到一組包含 N 個類別、每類 K 個範例的有標籤**支撐集**（support set），然後預測來自同樣 N 個類別的無標籤**查詢**（query）影像的標籤。這就是 N-way K-shot 設定。單一情節的結果變異很大，因此報告的數字通常是許多情節的平均，並常附上信賴區間。

Matching Networks 在 ImageNet 與 Omniglot 上引入了這種單樣本評估風格，也說明了設計為何重要。該論文報告，其單樣本準確率在 ImageNet 上從 87.6% 提升到 93.2%，在 Omniglot 上從 88.0% 提升到 93.8%，優於相互競爭的方法（Vinyals et al., 2016）。這類比較只有在所有方法都使用相同的情節抽樣器時才公平。

## 比較的基準

| 基準 | 影像來源 | 著重的能力 |
|---|---|---|
| [miniImageNet](mini-imagenet.md) | ImageNet 的子集，測試類別保留不用於訓練 | 細粒度視覺差異的自然照片 |
| [Omniglot](omniglot.md) | 多種書寫系統的手寫字元 | 從一個或少數幾個筆跡學會新字元 |

兩個基準來自不同的影像領域。在手寫字元上表現好的方法，不一定在自然照片上也好，因此不應把其中一個的結果直接當成另一個的結果。

## 關鍵概念

- **支撐集與查詢集**：情節提供的有標籤範例，以及學習者必須分類的無標籤範例。
- **情節**：一個抽樣出來的任務，包含 N 個類別與每類 K 個範例。準確率是許多情節的平均。
- **基礎類別與新類別**：訓練使用基礎類別，測試使用學習者從未見過的類別。

## 運作方式

少樣本學習者通常先把每個範例轉成特徵向量，再把查詢與支撐集比較。例如原型網路（Prototypical Networks）以每個類別支撐嵌入的平均值代表該類別，並把查詢分配給最近的原型。該論文主張，這種較簡單的歸納偏置適合資料有限的情況，而簡單的設計選擇能優於較複雜的近期方法（Snell et al., 2017）。模型無關元學習（MAML）則走另一條路線：它訓練一組初始參數，使其在少數幾步梯度更新後即可適應新任務，並在兩個少樣本影像分類基準上報告結果（Finn et al., 2017）。

## 常見問題

- **協定漂移。** 各論文的類別切分、骨幹網路、影像解析度與情節數都不同，同一方法可能報告不同的數字。
- **飽和。** 強勁的方法在標準切分上已留下很小的空間，因此細微差異需要信賴區間才有意義。
- **領域落差。** Omniglot 的影像是簡單的筆畫，自然影像則嘈雜得多。在其中一個基準上的進步不會自動轉移到另一個。

## 相關連結

- [元學習](../../../paradigms/meta-learning/index.md) 是大多數在這些基準上評估的方法所屬的學習範式。
- [像人一樣學習與思考的機器](../../../../brain-mind/cognitive-science/building-machines-like-people/index.md) 討論人如何從少數範例學習新概念，這正是 Omniglot 所要支持的比較。

## 開放問題

- 情節式基準衡量的是學習新概念的能力，還是主要反映預訓練特徵的品質。
- 少樣本分數與大型預訓練模型的少樣本表現之間有什麼關係；後者透過提示而非梯度更新來學習（Brown et al., 2020）。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [ImageNet](../vision/imagenet.md) 是 miniImageNet 影像的來源。
- [視覺](../vision/index.md) 涵蓋少樣本切分所取自的影像基準。

## 參考文獻

### 開創性論文

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — 定義以支撐集與查詢進行的 ImageNet 與 Omniglot 單樣本評估，並報告上文引用的準確率提升。
- Lake, B. M., Salakhutdinov, R. & Tenenbaum, J. B. (2015). *Human-level concept learning through probabilistic program induction*. Science, 350(6266), 1332–1338. https://doi.org/10.1126/science.aab3050 — 提出 Omniglot 所依據的手寫字元學習情境。
- Snell, J., Swersky, K. & Zemel, R. S. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — 以查詢到類別原型的距離進行分類，是 N-way K-shot 任務的簡單基線。
- Finn, C., Abbeel, P. & Levine, S. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — 訓練一組能在少數幾步梯度更新內適應的初始參數，並在少樣本影像分類上評估。

### 文章與文件

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision, 115, 211–252. https://doi.org/10.1007/s11263-015-0816-y — 描述 ImageNet 基準，即 miniImageNet 所用影像的來源。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 將 few-shot 一詞用於以示範進行提示、且不做梯度更新的做法，與情節式學習的協定不同。
