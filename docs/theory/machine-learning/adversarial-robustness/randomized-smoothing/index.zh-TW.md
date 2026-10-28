---
translation_reviewed: 2026-10-28
---

# 隨機平滑

隨機平滑可以把任何分類器轉換為一個平滑分類器，並附帶可證明的保證。對每個輸入，它會認證一個半徑，在此半徑內任何 \(\ell_2\) 擾動都無法改變預測。Cohen et al.（2019）為高斯雜訊給出了緊密的保證，並把它擴展到 ImageNet 規模。它是[對抗樣本與穩健性](../index.md)總覽中的方法之一。

## 概述

早期的可證明防禦只適用於小型網路，或需要特殊的訓練方式。Raghunathan et al.（2018）對只有一個隱藏層的網路，使用半定鬆弛來得到認證。隨機平滑可與任何基礎網路搭配使用，因為其保證來自於對隨機雜訊取平均，而非來自網路的內部結構。Cohen et al.（2019）指出，他們能把任何在高斯雜訊下表現良好的分類器，轉換為在 \(\ell_2\) 範數下可被證明為穩健的分類器；他們也回報，在當時，除了平滑法之外，尚未有任何可證明防禦被證明能在 ImageNet 上可行。

## 關鍵概念

- **平滑分類器。** 其預測是當輸入受到高斯雜訊干擾時，基礎分類器最常輸出的類別。
- **可證明半徑。** 平滑預測保證不會改變的、距離輸入最遠的 \(\ell_2\) 距離。
- **基礎分類器。** 被雜訊取平均的網路。它必須以加入雜訊的方式訓練，才能在含雜訊的輸入上仍然預測良好。
- **棄權。** 當雜訊投票不夠明確、無法認證任何半徑時，方法拒絕做出預測。
- **機率性認證。** 各類別的票數比例是以抽樣估計的，因此保證在所選的信心水準下成立。

## 運作方式

平滑分類器為

\[
g(x) = \arg\max_c \; \mathbb{P}_{\eta \sim \mathcal{N}(0, \sigma^2 I)}\big[f(x+\eta) = c\big].
\]

令 \(p_A\) 為最高類別的機率，\(p_B\) 為次高類別的機率。Cohen et al.（2019）證明，\(g\) 的預測在半徑為下式的 \(\ell_2\) 球內保持不變：

\[
R = \frac{\sigma}{2}\big(\Phi^{-1}(p_A) - \Phi^{-1}(p_B)\big),
\]

其中 \(\Phi^{-1}\) 是標準常態分布函數的反函數。由於 \(p_B \le 1 - p_A\)，較簡單的值 \(\sigma\,\Phi^{-1}(p_A)\) 是有效的、略為保守的半徑。

認證分為四個步驟。

1. 以加入尺度為 \(\sigma\) 的高斯雜訊的輸入，訓練基礎分類器。
2. 抽取輸入的許多含雜訊副本，並統計各類別的票數。
3. 以最高類別比例的下信賴界 \(\underline{p}_A\) 取代所觀察到的比例。
4. 若 \(\underline{p}_A\) 大於二分之一，則認證半徑 \(\sigma\,\Phi^{-1}(\underline{p}_A)\)；否則棄權。

## 結果

Cohen et al.（2019）在摘要中回報，一個 ImageNet 分類器在 \(\ell_2\) 擾動範數小於 0.5 時，其可證明的 top-1 準確率為 49%。在較小的資料集上，其他可證明方法也可行，他們回報平滑法能得到更高的可證明準確率。

## 限制

- **只保證 \(\ell_2\)。** 高斯平滑只對 \(\ell_2\) 擾動給出保證；它不能直接給出多數攻擊基準所用的 \(\ell_\infty\) 保證。
- **乾淨準確率下降。** 以雜訊訓練會降低未受擾動輸入上的準確率，且此權衡隨雜訊尺度增大而加劇。
- **半徑與準確率互相權衡。** 較大的 \(\sigma\) 給出較大的半徑，但基礎分類器也較受雜訊影響，因此 \(\sigma\) 的選擇是一項設計決策。
- **成本。** 認證一個輸入需要大量含雜訊的前向傳播。
- **威脅模型狹窄。** 認證只涵蓋 \(\ell_2\) 球。它不涵蓋語意或實體世界的改變，例如提示注入，相關內容見 [LLM 安全](../../../../engineering/llm-security/index.md)。

## 未解問題

- 能否在不大幅損失乾淨準確率的前提下，把認證延伸到其他範數或更大的擾動？
- 可證明半徑小於經驗攻擊所找到的半徑，剩下的差距有多大？
- 在部署的系統中，應如何處理棄權？拒絕預測本身也可能有代價。

## 連結

平滑是對擾動後輸入取平均，與 [MC dropout](../../uncertainty-and-calibration/mc-dropout/index.md) 所用的平均是近親，也與[不確定性與校準](../../uncertainty-and-calibration/index.md)所研究的棄權相關。機率性認證依賴信賴區間，相關內容見[機率方法](../../../paradigms/probabilistic/index.md)。Lécuyer et al.（2018）把同類以雜訊為基礎的保證與差分隱私連結起來，這也連到[隱私](../../../../society/privacy/index.md)的文獻。

## 應用

- **可證明的影像分類器。** 平滑後的網路能給出 ImageNet 規模的認證，可作為可證明穩健性的參考點。

## 參考文獻

### 開創性論文

- Cohen, J. M., Rosenfeld, E. & Kolter, J. Z. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. arXiv. https://arxiv.org/abs/1902.02918 — 證明高斯平滑的緊密 \(\ell_2\) 保證，並回報在 ImageNet 上的可證明準確率。
- Raghunathan, A., Steinhardt, J. & Liang, P. (2018). *Certified Defenses against Adversarial Examples*. arXiv. https://arxiv.org/abs/1801.09344 — 以半定鬆弛為只有一個隱藏層的網路給出認證，這是可證明訓練可行的模型類別。
- Wong, E. & Kolter, J. Z. (2017). *Provable defenses against adversarial examples via the convex outer adversarial polytope*. arXiv. https://arxiv.org/abs/1711.00851 — 學習具可證明穩健性的 ReLU 分類器，使用可達啟動值的凸外近似。
- Lécuyer, M. et al. (2018). *Certified Robustness to Adversarial Examples with Differential Privacy*. arXiv. https://arxiv.org/abs/1802.03471 — 提出 PixelDP，一種可擴展到 ImageNet 規模網路、且適用於任意模型的可證明防禦。

### 調查與教科書

- Akhtar, N. & Mian, A. (2018). *Threat of Adversarial Attacks on Deep Learning in Computer Vision: A Survey*. arXiv. https://arxiv.org/abs/1801.00553 — 調查電腦視覺中的攻擊與防禦，為可證明方法提供背景。

### 文章與文件

- Carlini, N. et al. (2019). *On Evaluating Adversarial Robustness*. arXiv. https://arxiv.org/abs/1902.06705 — 提供評估防禦的方法論指引，並指出許多防禦會被適應性攻擊擊破。
- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — 說明經驗上的穩健性為何可能產生誤導，也是可證明保證的動機之一。
