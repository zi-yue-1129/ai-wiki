---
translation_reviewed: 2026-10-28
---

# ODIN

ODIN 是一種分布外偵測器，以兩種方式改進 softmax 分數：先把 logits 除以一個大於一的溫度，再沿著使最大 softmax 分數增加的方向，對輸入做小幅擾動。本頁是[分布外偵測與分布偏移](index.md)的一部分。

## 概述

單純的 softmax 信心是較弱的 OOD 分數，因為網路可能對遠離訓練資料的輸入也很有信心。Liang 等人（2018）發現，兩個小改動可以在不重新訓練網路的情況下，拉大分布內與分布外輸入之間的分隔。此方法只需一次前向傳播與一次額外的梯度步伐，調整參數則需要一小組驗證用的 OOD 輸入。

## 關鍵概念

- **softmax 的溫度縮放**：\(S_i(x;T)=\frac{\exp(f_i(x)/T)}{\sum_j\exp(f_j(x)/T)}\)，其中 \(T>1\)。提高溫度可把分數拉開，有利於偵測。
- **輸入擾動**：一步 \(\tilde{x}=x-\varepsilon\,\mathrm{sign}(-\nabla_x \log S_{\hat y}(x;T))\)，使預測類別的分數上升。
- **偵測規則**：當分數低於門檻時，輸入被標記為 OOD。

## 運作方式

對輸入 \(x\)，ODIN 先算出預測類別 \(\hat y\)，再構造出能提高 \(\hat y\) 之溫度縮放 softmax 分數的擾動輸入 \(\tilde{x}\)。它以 \(S_{\hat y}(\tilde{x};T)\) 為 \(\tilde{x}\) 打分。分布內的輸入對擾動的反應與分布外的輸入不同，因此分隔比單純的 softmax 更大。溫度 \(T\) 與擾動大小 \(\varepsilon\) 在驗證資料上選定。Liang 等人（2018）報告，在標準網路與影像基準上，ODIN 相較基準有明顯的提升。

## 變體

- **僅溫度**：只做縮放而不擾動，成本較低，但分隔較小。
- **僅擾動**：對未經縮放的 softmax 做一步，可能有幫助，但較不穩定。
- **以特徵為基礎的分數**以特徵空間的距離取代輸出分數，即[馬氏距離偵測器](mahalanobis-distance.md)所採用的方法。

## 結果與限制

- ODIN 在不改變網路權重的情況下，改進了相較 softmax 基準的 OOD 偵測（Liang 等人，2018）。
- 它使用小型 OOD 驗證集來選擇 \(T\) 與 \(\varepsilon\)，而這些輸入未必與部署時遇到的 OOD 輸入相符。
- 梯度步伐在推論時增加成本，而且此方法依賴於具 softmax 輸出的分類器。
- 效益取決於分布內與分布外資料集的組合，因此在一個基準上的結果不保證在另一個基準上也成立。

## 應用

- **部署中的影像分類器**：需要便宜的 OOD 旗標時。
- **基準測試**：把 OOD 偵測器與 softmax 基準比較。
- **分流**：把被標記的輸入送交人工檢視。

## 開放問題

- 在某一種 OOD 資料上調整的參數，未必能遷移到之後出現的偏移。
- 當網路以不同目標或不同模態訓練時，溫度與擾動是否仍有幫助，尚無定論。

## 參考文獻

### 奠基性論文

- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — 提出 ODIN，以溫度縮放與輸入擾動改進偵測。
- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — ODIN 所改進的 softmax 基準。
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — 以特徵為基礎、取代輸出分數的替代方法。

### 綜述與教科書

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — 用來衡量偵測器與偏移穩健性的基準。
- Geirhos, R. et al. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence* 2(11), 665–673. https://doi.org/10.1038/s42256-020-00257-z — 說明為何在一種偏移上訓練的偵測器，可能漏掉另一種偏移。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 softmax 校準與偵測的背景。
