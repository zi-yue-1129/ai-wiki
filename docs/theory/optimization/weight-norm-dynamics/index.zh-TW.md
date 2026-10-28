---
translation_reviewed: 2026-10-28
tags:
  - optimization
  - weight decay
  - normalisation
  - training stability
aliases:
  - Weight-norm dynamics
  - Weight norm growth
  - 權重範數動態
---

# 權重範數動態

當一層之後接著正規化時，把該層權重乘上常數不會改變輸出。此時權重範數的漂移方向由最佳化器與學習率決定，而不是由損失決定。本子主題說明範數如何增長、權重衰減如何形成平衡，以及這對訓練穩定性的意義。衰減的一般說明見[正則化與權重衰減](../regularisation-and-weight-decay.md)，解耦的形式見 [AdamW](../adaptive/adamw.md) 頁面。

## 概述

考慮一層，其輸出經過正規化，因此把權重乘上常數不影響輸出。此時梯度與權重向量正交，每一步梯度更新都會使範數增加。相對於權重範數的步長，也就是有效學習率，因此會隨訓練縮小。權重衰減會抵消這種增長，兩種效應最後在一個平衡範數上達到平衡。

由此衍生兩個問題。平衡要多久才會到來，相對於整個訓練長度？對於不是尺度不變的層，例如注意力輸出或分類頭，同樣的平衡又如何？

## 關鍵方法

每個方法都有自己的頁面。此處的概述與比較只是簡短的整理。

| 方法 | 機制 | 說明的內容 |
|---|---|---|
| [旋轉平衡](rotational-equilibrium.md)（Kosson 等人，2023） | 權重衰減平衡每個神經元權重的旋轉 | 平衡範數與約 \(1/(\eta\lambda)\) 步的時間尺度，不同神經元的旋轉速率不同 |
| [AdamW 的權重衰減縮放](adamw-weight-decay-scaling.md)（Wang 與 Aitchison，2024） | 設定 \(\lambda\)，使平均的時間尺度以 epoch 計固定 | 最佳衰減取決於模型與資料集大小，並隨學習率改變 |
| 球面運動動態（Wan 等人，2020） | 分析以 SGD 與衰減訓練的正規化網路動態 | 有衰減時範數收斂到平衡，沒有衰減時持續增長，有效步長因此縮小 |
| 指數學習率觀點（Li 與 Arora，2019） | 說明衰減與正規化共同作用的效果像指數增長的步長 | 對尺度不變的層，只有乘積 \(\eta\lambda\) 有影響 |

注意力層面的問題見 [QK 正規化](../../models/transformer/qk-norm.md) 與 [σReparam](../../models/transformer/sigma-reparam.md) 頁面。只限制範數並不能保證注意力穩定，因為崩潰可能發生在秩或熵上。

## 相關主題

- [AdamW](../adaptive/adamw.md) 把權重衰減與自適應步驟分開，平衡分析正是在這種設定下適用。
- [學習率排程](../learning-rate-schedules.md) 與衰減互相影響，因為平衡取決於學習率與衰減的乘積。
- [尖銳極小值](../sharp-minima.md) 涵蓋最佳化器與正則化器影響解的另一條途徑。

## 開放問題

- 平衡的圖像對於非尺度不變的層（例如沒有接正規化的頭與投影層）預測得多準確。
- 時間尺度的規則是否適用於所引用研究以外的架構。

## 參考文獻

- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — 旋轉平衡、平衡範數與時間尺度結果的來源。
- Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — 提出分析所用的解耦衰減。
- Wan, R., Zhu, Z., Zhang, X., & Sun, J. (2020). *Spherical Motion Dynamics: Learning Dynamics of Neural Network with Normalization, Weight Decay, and SGD*. arXiv:2006.08419. https://arxiv.org/abs/2006.08419 — 較早分析 SGD 加衰減時的範數動態。
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. ICLR 2020. https://arxiv.org/abs/1910.07454 — 說明衰減與正規化共同作用時，像是一個增長的學習率。
- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — 以同樣的時間尺度觀點，為不同規模選擇衰減。
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — 在小規模下重現注意力與輸出 logit 的不穩定，並測試補救方法。
