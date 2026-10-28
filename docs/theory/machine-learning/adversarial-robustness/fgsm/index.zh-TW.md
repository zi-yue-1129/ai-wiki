---
translation_reviewed: 2026-10-28
---

# 快速梯度符號法（FGSM）

快速梯度符號法是對神經網路最簡單的梯度攻擊。它沿著使損失增加最多的方向，走一步固定大小的步長。Goodfellow et al.（2014）提出它，目的是快速產生[對抗樣本](../index.md)，並解釋對抗樣本為何存在。

## 概述

Szegedy et al.（2013）指出，對圖像做微小、肉眼難以察覺的改動，就能讓深度網路的輸出翻轉，但他們的攻擊需要反覆搜尋。Goodfellow et al.（2014）主張，這種脆弱性的主要成因是網路在高維輸入空間中近乎線性的行為，而不是早期解釋所歸咎的非線性或過擬合。若損失對輸入大致呈線性變化，最好的小幅改動就會與梯度的符號對齊，而這只需一次反向傳播即可算出。

## 關鍵概念

- **擾動預算 \(\varepsilon\)。** 每個輸入座標允許的最大改動量，以 \(\ell_\infty\) 範數衡量。
- **梯度符號。** 只保留梯度每個分量的方向，不保留其大小，因此每個輸入座標都移動相同的量。
- **單步攻擊。** 只需一次梯度計算即可產生對抗樣本，這使 FGSM 相較於 [PGD 頁](../pgd-adversarial-training/index.md)所述的迭代攻擊更為便宜。
- **線性假說。** 此解釋認為，許多各自與權重對齊的小幅改動，會沿著模型最敏感的方向累加。

## 運作方式

令 \(J(\theta, x, y)\) 為參數為 \(\theta\)、輸入為 \(x\)、標籤為 \(y\) 的模型損失。對抗樣本為

\[
x^{\text{adv}} = x + \varepsilon \,\operatorname{sign}\big(\nabla_x J(\theta, x, y)\big).
\]

1. 計算乾淨輸入 \(x\) 相對於其真實標籤 \(y\) 的損失。
2. 反向傳播至輸入，使梯度對 \(x\) 求導，並保持權重不變。
3. 只保留每個梯度分量的符號。
4. 將 \(\varepsilon\) 乘以該符號加到 \(x\) 上，再裁剪到有效的輸入範圍，例如正規化像素的 \([0, 1]\)。

同一篇論文也提出以這些樣本進行訓練。目標函數將乾淨樣本的損失與擾動後輸入的損失混合，混合權重 \(\alpha\) 由使用者設定。這是[對抗訓練](../pgd-adversarial-training/index.md)最早的形式。

## 結果

Goodfellow et al.（2014）以定量結果支持線性解釋，並顯示針對某一模型所產生的樣本，能跨越不同架構與訓練資料集遷移。他們也回報，以對抗樣本訓練可降低 MNIST 上 maxout 網路的測試誤差。摘要未給出數字，若需要數值，請參閱原文。

後續研究提供了更多脈絡。Kurakin et al.（2016）發現，由手機相機拍攝的對抗圖像，仍常被誤分類。Tramèr et al.（2017）則發現，以單步樣本進行對抗訓練，可能收斂到退化解：模型能抵抗 FGSM，卻無法抵抗更強的攻擊。

## 限制

- **線性模型只是近似。** 在損失曲面高度彎曲之處，一步可能無法使損失明顯增加，因此 FGSM 可能遠弱於經過最佳化的攻擊。
- **攻擊失敗不代表穩健。** 會遮蔽梯度的防禦可以擊敗 FGSM，但更強的攻擊仍會成功（Athalye et al., 2018）。防禦必須接受[適應性評估](../../../../engineering/evaluation/index.md)。
- **單步訓練很脆弱。** 只以 FGSM 型樣本訓練的模型，可能帶來虛假的安全感（Tramèr et al., 2017）。

## 未解問題

- 線性是否就是完整的解釋？Ilyas et al.（2019）把對抗樣本歸因於具預測力卻脆弱的特徵，這是另一種說法。
- 單步對抗訓練能否穩定進行，而不退化為弱擾動？
- 小幅的 \(\ell_\infty\) 改動是否等同於人們所感知的微小改變，目前尚無定論。Elsayed et al.（2018）發現，遷移而來的樣本也會影響受時間限制的人類觀察者。

## 連結

FGSM 是投影梯度法的單步情形，[梯度下降](../../../math/calculus/gradient-descent/index.md)頁說明了它與訓練所共用的更新規則。它通常用於圖像的[卷積網路](../../../models/cnn/index.md)。語言模型的文字輸入是離散的，因此梯度步驟無法直接套用；該情形見 [LLM 安全](../../../../engineering/llm-security/index.md)。至於大腦的一側，見[視覺感知](../../../../brain-mind/visual-perception/index.md)。

## 應用

- **穩健性測試。** FGSM 是快速的基準，可用來檢查模型對微小擾動是否敏感。
- **資料擴增。** 以擾動後的訓練資料副本來提升電腦視覺的穩健性，此用途源自 2014 年的論文。
- **實體世界風險。** Kurakin et al.（2016）顯示，對抗圖像經相機擷取後仍可能有效，這對[自動駕駛](../../../../applications/autonomous-driving/index.md)的感知等系統十分相關。

## 參考文獻

### 開創性論文

- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples*. arXiv. https://arxiv.org/abs/1412.6572 — 提出 FGSM，主張線性性解釋了對抗脆弱性，並提出以此類樣本進行訓練。
- Szegedy, C. et al. (2013). *Intriguing properties of neural networks*. arXiv. https://arxiv.org/abs/1312.6199 — 首次顯示，難以察覺的輸入擾動可以改變深度圖像分類器的輸出。
- Kurakin, A., Goodfellow, I. J. & Bengio, S. (2016). *Adversarial examples in the physical world*. arXiv. https://arxiv.org/abs/1607.02533 — 顯示由手機相機擷取的對抗圖像，仍常被誤分類。
- Tramèr, F. et al. (2017). *Ensemble Adversarial Training: Attacks and Defenses*. arXiv. https://arxiv.org/abs/1705.07204 — 顯示單步對抗訓練可能收斂到退化的極小值，能抵抗 FGSM 卻無法抵抗更強的攻擊。

### 文章與文件

- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — 說明為何基於梯度的攻擊可能在未真正提升穩健性的防禦面前失效。
- Ilyas, A. et al. (2019). *Adversarial Examples Are Not Bugs, They Are Features*. arXiv. https://arxiv.org/abs/1905.02175 — 將對抗脆弱性歸因於非穩健但具預測力的特徵，是與線性性解釋相競爭的說法。
- Elsayed, G. F. et al. (2018). *Adversarial Examples that Fool both Computer Vision and Time-Limited Humans*. arXiv. https://arxiv.org/abs/1802.08195 — 顯示從視覺模型遷移而來的樣本，也會改變受時間限制之人類觀察者的判斷。
