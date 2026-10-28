---
translation_reviewed: 2026-10-28
---

# 隨機平滑

隨機平滑把任何基礎分類器轉換為平滑後的分類器：對輸入的多個加了雜訊的副本進行多數決。Cohen 等人（2019）顯示，在高斯雜訊下，這種投票能給出認證的 \(\ell_2\) 半徑，在此半徑內預測不會改變。本頁是[對抗樣本與穩健性](index.md)的一部分。

## 概述

多數防禦只提供經驗性的穩健性，可能被更好的攻擊打破。認證方法則對每個輸入都給出保證。隨機平滑是大型網路最具擴展性的認證方法，因為它只需要取樣與一個基礎分類器，不需要特殊的網路架構。

## 關鍵概念

- **平滑分類器**：\(g(x)=\arg\max_c \mathbb{P}_{\eta}[f(x+\eta)=c]\)，其中 \(\eta\) 為高斯雜訊。
- **認證半徑**：一個距離 \(R\)，使得對所有 \(\|\delta\|_2\le R\)，都有 \(g(x+\delta)=g(x)\)。
- **雜訊水準 \(\sigma\)**：高斯雜訊的尺度，它在乾淨準確率與半徑之間取捨。
- **信賴界**：由於投票是由取樣估計，認證以高機率成立。

## 運作方式

令 \(p_A\) 為基礎分類器在雜訊下輸出最可能類別 \(c_A\) 的機率，\(p_B\) 為次高類別機率的下界。Cohen 等人（2019）證明，平滑預測在下式給出的半徑內被認證：

\[
R=\frac{\sigma}{2}\big(\Phi^{-1}(p_A)-\Phi^{-1}(p_B)\big),
\]

其中 \(\Phi^{-1}\) 為標準常態累積分布函數的反函數。機率由取樣估計，並使用考慮取樣誤差的信賴界。基礎分類器通常以高斯雜訊增強來訓練，使其在有雜訊的輸入上也準確。

## 變體

- **不同的雜訊分布**會改變認證所涵蓋的範數，這是活躍的研究方向。
- **自適應取樣**把更多樣本花在接近決策邊界的輸入上，在同樣的計算預算下收緊界限。
- **去噪平滑**在標準分類器前加上去噪器，以提高有雜訊輸入上的準確率。

## 結果與限制

- 此方法可擴展到大型影像網路，並在 ImageNet 規模的基準上，在非平凡的半徑下給出認證準確率（Cohen 等人，2019）。
- 半徑受雜訊水準限制。要得到大半徑需要大雜訊，這會降低乾淨準確率。
- 認證只對所選雜訊下的 \(\ell_2\) 擾動成立，不直接涵蓋其他威脅模型。
- 推論時的認證成本高，因為每次預測都需要大量的雜訊樣本。

## 應用

- **認證的影像分類器**：對小的 \(\ell_2\) 擾動提供保證。
- **認證方法的基準**：認證半徑與認證準確率是標準的評估指標。
- **安全關鍵的視覺**：在需要保證而非經驗性聲稱的情境中使用。

## 開放問題

- 在實用的準確率水準下，認證半徑仍然很小，改善此取捨是活躍的領域。
- 把保證擴展到 \(\ell_2\) 以外，以及擴展到文字或圖等結構化輸入，更加困難。

## 參考文獻

### 奠基性論文

- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — 為高斯平滑後的分類器給出認證的 \(\ell_2\) 半徑。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — 提出認證方法所要排除的對抗樣本。
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — 經驗性穩健性，是認證方法比較的基準。

### 綜述與教科書

- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — 說明經驗性防禦可能被打破，因此需要認證保證。
- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — 討論雜訊式認證同樣需付出的準確率代價。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；提供穩健性與認證的背景。
