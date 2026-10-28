---
translation_reviewed: 2026-10-28
---

# 分布外偵測與分布偏移

分布外（OOD）偵測問的是，某個輸入是否來自與訓練資料不同的分布，使模型能將其標記出來，而不是自信地做出預測。分布偏移是更廣的問題，指測試資料與訓練資料不同。本頁是[機器學習](../index.md)的一部分。

## 概述

在一個分布上訓練的模型，常常會收到來自另一個分布的輸入：夜間拍攝的照片、老化的感測器，或使用不同掃描儀的新醫院。模型仍可能給出自信的預測。Hendrycks 與 Gimpel（2017）顯示，一個簡單的信心分數，就能把許多被誤分類的輸入與分布外的輸入，和正確的輸入區分開來，這使此問題成為可以量測的基準。

## 關鍵概念

- **共變量偏移**：輸入的分布改變，而給定輸入的標籤條件分布不變。
- **標籤偏移**：標籤的分布改變，而給定標籤的輸入條件分布不變。
- **OOD 分數**：由模型算出的數值，對分布內的輸入較高，對分布外的輸入較低，用來設定判斷的門檻。
- **開放集辨識**：對已知類別分類，並拒絕未知類別，與 OOD 偵測密切相關。
- **捷徑學習**：模型依賴訓練中與標籤相關、但一般情況下並不相關的特徵，因此在偏移下會失敗（Geirhos 等人，2020）。

## 運作方式

多數 OOD 偵測器會從網路的輸出或內部特徵計算一個分數，再設定門檻。以輸出為基礎的分數（例如信心）便宜，但對 OOD 輸入可能過度自信。以特徵為基礎的分數則對分布內特徵擬合一個密度或距離。有些方法加入小的擾動或溫度，以拉大分隔（Liang 等人，2018）。WILDS 等基準則衡量模型在跨醫院、跨相機與跨地區的自然偏移下表現如何（Koh 等人，2021）。

## 主要方法

- [ODIN](odin.md)：以溫度縮放與小幅輸入擾動改進的 softmax 分數。
- [馬氏距離偵測器](mahalanobis-distance.md)：到類別條件高斯分布的特徵空間距離，也能涵蓋對抗輸入（Lee 等人，2018）。

## 與其他頁面的連結

- [領域適應](../../paradigms/transfer/domain-adaptation/index.md)嘗試在偏移下讓模型運作，方法是使用未標記的目標資料，與偵測互為補充。
- [對抗樣本與穩健性](../adversarial-robustness/index.md)處理被刻意改動的輸入，而 OOD 輸入通常是自然產生的。

## 應用

- **醫學影像**：標記來自模型未見過的掃描儀或族群的影像。
- **自主系統**：當場景不熟悉時，交由人或安全的備援方案處理。
- **品質管制**：在錯誤累積前，偵測生產線上的新產品類型。

## 開放問題

- 能偵測某一種 OOD 輸入的方法，常常無法偵測另一種，沒有單一分數能在所有偏移上都可靠。
- 深度模型可能對遠離訓練資料的輸入自信地出錯，這會削弱以信心為基礎的偵測。
- 在缺乏捷徑的標記範例時，很難找出並移除捷徑特徵。

## 參考文獻

### 奠基性論文

- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — 顯示最大 softmax 機率即可區分被誤分類與分布外的輸入，並建立基準。
- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — 提出 ODIN，以溫度縮放與輸入擾動改進偵測。
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — 在特徵空間上提出馬氏距離偵測器。
- Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F. & Vaughan, J. W. (2010). A theory of learning from different domains. *Machine Learning* 79(1–2), 151–175. https://doi.org/10.1007/s10994-009-5152-4 — 給出模型在領域改變下誤差的理論界限。

### 綜述與教科書

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — 涵蓋許多真實資料集中自然分布偏移的基準。
- Geirhos, R. et al. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence* 2(11), 665–673. https://doi.org/10.1038/s42256-020-00257-z — 說明模型如何依賴在偏移下會失效的捷徑。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋分布偏移與 OOD 輸入的不確定性。
