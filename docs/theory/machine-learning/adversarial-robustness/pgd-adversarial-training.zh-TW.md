---
translation_reviewed: 2026-10-28
---

# 投影梯度下降與對抗訓練

投影梯度下降（PGD）是一種迭代攻擊：重複小幅的梯度步伐，並在每步之後把擾動投影回允許的預算之內。對抗訓練則以 PGD 樣本作為訓練資料，Madry 等人（2018）證明這是一種強的防禦。本頁是[對抗樣本與穩健性](index.md)的一部分。

## 概述

單步 FGSM 可能錯過損失最高的區域。PGD 採取多步，並從預算內的隨機點重新開始，因此能找到更強的對抗樣本。Madry 等人（2018）把穩健訓練表述為極小極大問題：對參數取極小，同時對預算內的擾動取最壞情況的損失。

## 關鍵概念

- **投影**：每一步之後，把擾動裁回以乾淨輸入為中心的 \(\epsilon\) 球內。
- **隨機起點**：攻擊從球內的隨機點開始，有助於跳出損失函數的平坦區域。
- **極小極大目標**：\(\min_\theta \mathbb{E}\big[\max_{\|\delta\|\le\epsilon} J(\theta,x+\delta,y)\big]\)。

## 運作方式

從球內隨機的 \(\eta\) 出發，令 \(x^{(0)}=x+\eta\)，PGD 更新為

\[
x^{(t+1)}=\Pi_{\mathcal{B}_\epsilon(x)}\!\Big(x^{(t)}+\alpha\,\mathrm{sign}\big(\nabla_x J(\theta,x^{(t)},y)\big)\Big),
\]

其中 \(\Pi\) 為投影到球上，\(\alpha\) 為步長。對抗訓練在每個小批次上計算這個內層最大化，並以得到的樣本更新參數。此方法成本高，因為每個訓練步需要多次計算梯度。

## 變體

- **TRADES** 以兼顧乾淨準確率與攻擊下輸出變化的損失進行訓練，得到不同的準確率與穩健性取捨。
- **免費對抗訓練**重用一次傳遞的梯度，以降低攻擊的成本。
- **快速對抗訓練**使用帶隨機初始化的單步 FGSM 以節省計算，但有[FGSM](fgsm.md)頁中提到的災難性過擬合風險。

## 結果與限制

- PGD 對抗訓練在影像基準上產生的模型，其穩健準確率遠高於標準訓練（Madry 等人，2018）。
- 穩健性提高時，乾淨準確率通常會下降，Tsipras 等人（2019）將其解釋為某些設定中固有的取捨。
- 穩健準確率取決於評估所用的攻擊。Carlini 與 Wagner（2017）顯示，只針對較弱攻擊訓練的防禦，可能被更強的攻擊打破。
- 訓練成本是標準訓練的數倍，收益需與這個成本權衡。

## 應用

- **穩健的影像分類器**：用於小幅雜訊就可能改變判斷的情境。
- **基準測試**：使用多步與多次隨機重啟的 PGD，是標準的評估攻擊。
- **遷移到其他領域**：對抗訓練的想法已應用於語音、文字嵌入與圖資料，成本問題也相同。

## 開放問題

- 各領域訓練時應採用的預算與攻擊尚無定論，而穩健性也未必能遷移到新的攻擊類型。
- 在不損失穩健性的前提下降低對抗訓練的成本，仍是研究目標。

## 參考文獻

### 奠基性論文

- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — 提出 PGD 攻擊與極小極大的對抗訓練。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — 提出基於梯度的攻擊與最早的對抗訓練實驗。
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — 顯示更強的攻擊會打破僅以較弱攻擊評估的防禦。

### 綜述與教科書

- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — 說明對抗訓練所呈現的準確率與穩健性取捨。
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — 比較經驗性的對抗訓練與認證保證。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；把對抗訓練視為極小極大問題。
