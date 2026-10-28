---
translation_reviewed: 2026-10-28
---

# 投影梯度下降與對抗訓練

投影梯度下降（PGD）是 FGSM 的迭代式、帶約束版本，後來成為神經網路上標準的強力攻擊。Madry et al.（2017）把 PGD 放進極小極大（min–max）的訓練目標中，這種組合通常稱為對抗訓練，並成為[對抗穩健性](../index.md)的常見基準。

## 概述

[FGSM](../fgsm/index.md) 只走一個線性步，是對最壞擾動的粗略猜測。PGD 則改為走許多小步，每一步之後都投影回輸入周圍允許的範圍內。Madry et al.（2017）把整個問題表述為穩健最佳化：若一個模型在對手所能選擇的最壞擾動下損失仍保持低，它就是穩健的。他們的摘要把這描述為對任何一階對手（即使用梯度資訊的對手）的安全保證。

## 關鍵概念

- **投影。** 每一步之後，把擾動後的輸入映回允許輸入的集合，通常是以原輸入為中心、半徑為 \(\varepsilon\) 的 \(\ell_\infty\) 球，並限制在有效的像素範圍內。
- **隨機起點。** 攻擊可以從球內的隨機點開始，而非從乾淨輸入開始，這有助於探索該區域。
- **極小極大目標。** 訓練時最小化最壞擾動下的損失，使模型在每一步都從最困難的樣本中學習。
- **一階對手。** 使用模型梯度的攻擊者，涵蓋大多數實際的白箱攻擊。

## 運作方式

穩健目標為

\[
\min_\theta \; \mathbb{E}_{(x,y)\sim\mathcal{D}} \Big[ \max_{\|\delta\|_\infty \le \varepsilon} L(\theta, x+\delta, y) \Big].
\]

內層的最大化由 PGD 近似，步長為 \(\alpha\)，迭代 \(K\) 次：

\[
x^{t+1} = \Pi_{\mathcal{B}_\varepsilon(x)}\Big(x^{t} + \alpha\, \operatorname{sign}\big(\nabla_x L(\theta, x^{t}, y)\big)\Big),
\]

其中 \(\Pi\) 是到球 \(\mathcal{B}_\varepsilon(x)\) 的投影。

1. 在每個訓練輸入周圍的球內選擇一個隨機點。
2. 重複 \(K\) 次：走一步帶符號的梯度步，再投影回去。
3. 以產生的對抗樣本取代乾淨樣本，或與之並用。
4. 對模型參數 \(\theta\) 進行一次標準的梯度步。

因此，每個訓練步大約需要額外的 \(K\) 次前向與反向傳播，這是此方法主要的實際代價。

## 結果

Madry et al.（2017）回報，以此目標訓練的網路對多種攻擊的抵抗力有顯著提升。摘要未給出準確率數字，因此此處不引用任何數字。

獨立評估的意見相當批判。Croce 與 Hein（2020）把改良的 PGD 變體與其他攻擊結合為 AutoAttack。他們的摘要指出，在他們測試的五十多個已發表防禦中，除一個以外，其所測得的穩健準確率都低於原論文所報告的數值，且常常低於 10%。Croce et al.（2020）隨後建立了 RobustBench，這是一個以 AutoAttack 為標準評估的排行榜。

## 限制

- **成本。** 訓練成本隨 PGD 步數增加，因此穩健訓練遠比標準訓練昂貴。
- **乾淨準確率較低。** 穩健模型往往會在未受擾動的輸入上犧牲一些準確率，Tsipras et al.（2018）在簡單的設定中證明了這種權衡確實存在。見[主題總覽](../index.md)。
- **針對特定攻擊的穩健性。** 針對某一攻擊調整的模型，可能在另一攻擊面前較弱。因此需要適應性評估，這正是 AutoAttack 的重點。
- **資料需求大。** Schmidt et al.（2018）顯示，穩健學習所需的樣本數可能遠多於標準學習。

## 未解問題

- 準確率的代價是穩健性本身固有的，還是可以透過更好的訓練消除？
- 能否在不損失強度的前提下，讓內層攻擊更便宜？
- 對 \(\ell_\infty\) 球的穩健性，能否遷移到其他類型的擾動？

## 連結

PGD 可視為加上投影後反覆進行的 FGSM，建立在[梯度下降](../../../math/calculus/gradient-descent/index.md)之上。它所引發的泛化問題，與[泛化理論](../../../paradigms/supervised/generalization-theory/index.md)相關。當語言模型透過紅隊演練被攻擊與強化時，極小極大的想法會再次出現，相關內容見[越獄與紅隊演練](../../../../engineering/llm-security/jailbreaks-and-red-teaming.md)。若需要可證明的替代方法，見[隨機平滑](../randomized-smoothing/index.md)。

## 應用

- **基準測試。** 如 RobustBench 所採用的 PGD 型與 AutoAttack 標準化評估，使影像分類器能在固定的威脅模型下相互比較。
- **安全關鍵的視覺。** 對微小擾動的穩健性是感知系統的要求之一，但單靠對抗訓練無法證明這一點。見[自動駕駛](../../../../applications/autonomous-driving/index.md)。

## 參考文獻

### 開創性論文

- Madry, A. et al. (2017). *Towards Deep Learning Models Resistant to Adversarial Attacks*. arXiv. https://arxiv.org/abs/1706.06083 — 把穩健性表述為極小極大最佳化，以 PGD 作為訓練攻擊，並公開 MNIST 與 CIFAR-10 的挑戰賽程式。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples*. arXiv. https://arxiv.org/abs/1412.6572 — PGD 所延伸的單步 FGSM 攻擊，也是第一個對抗訓練的目標函數。
- Carlini, N. & Wagner, D. (2016). *Towards Evaluating the Robustness of Neural Networks*. arXiv. https://arxiv.org/abs/1608.04644 — 以最佳化為基礎的攻擊，能擊敗防禦性蒸餾。
- Tsipras, D. et al. (2018). *Robustness May Be at Odds with Accuracy*. arXiv. https://arxiv.org/abs/1805.12152 — 在簡單的設定中，證明標準準確率與對抗穩健性之間存在可證明的張力。
- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — 顯示數個以混淆梯度為基礎的防禦，都被適應性攻擊擊破。

### 調查與教科書

- Bai, T. et al. (2021). *Recent Advances in Adversarial Training for Adversarial Robustness*. arXiv. https://arxiv.org/abs/2102.01356 — 調查對抗訓練的各種變體，以及它們所引發的泛化問題。

### 文章與文件

- Croce, F. & Hein, M. (2020). *Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks*. arXiv. https://arxiv.org/abs/2003.01690 — 提出 AutoAttack，一個免參數的攻擊集成，所得的穩健準確率常低於許多已發表防禦的報告。
- Croce, F. et al. (2020). *RobustBench: a standardized adversarial robustness benchmark*. arXiv. https://arxiv.org/abs/2010.09670 — 介紹標準化穩健性評估的排行榜與函式庫。
- Schmidt, L. et al. (2018). *Adversarially Robust Generalization Requires More Data*. arXiv. https://arxiv.org/abs/1804.11285 — 證明穩健學習與標準學習之間的樣本複雜度差距，並以圖像實驗加以驗證。
