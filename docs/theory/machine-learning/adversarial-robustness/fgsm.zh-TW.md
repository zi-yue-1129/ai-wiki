---
translation_reviewed: 2026-10-28
---

# 快速梯度符號法

快速梯度符號法（FGSM）是一種單步攻擊：沿著損失對輸入之梯度的符號方向，以固定大小 \(\epsilon\) 擾動輸入。本頁是[對抗樣本與穩健性](index.md)的一部分。

## 概述

對可微分的分類器而言，FGSM 是最簡單且有效的攻擊。它只需計算一次梯度，不需搜尋，因此快到可以放在訓練過程中使用。Goodfellow 等人（2015）提出此方法，並藉由它主張對抗樣本來自高維模型的線性行為。

## 關鍵概念

- **擾動預算 \(\epsilon\)**：每個輸入分量允許的最大改變，以 \(\ell_\infty\) 範數衡量。
- **損失梯度**：訓練損失對輸入的導數，而非對參數的導數。
- **符號運算**：在輸入值域裁剪之前，每個非零梯度分量產生大小為 \(\epsilon\) 的擾動；梯度為零的分量不變。若碰到輸入合法值域邊界，實際變化量可能小於 \(\epsilon\)。

## 運作方式

給定輸入 \(x\)、標籤 \(y\)、損失 \(J(\theta,x,y)\) 與參數 \(\theta\)，對抗輸入為

\[
\tilde{x} = x + \epsilon\,\mathrm{sign}\big(\nabla_x J(\theta, x, y)\big).
\]

將 \(\tilde{x}\) 裁剪到有效的輸入範圍內（例如影像的 \([0,1]\)），可使樣本維持為有效輸入。Goodfellow 等人（2015）顯示，線性模型特別脆弱，因為擾動會在許多輸入維度上累加，使輸出改變 \(\epsilon\|w\|_1\)。

### FGSM 與迭代式 PGD 的路徑比較

![雙欄示意圖：FGSM 從起點單步移至可行終點；PGD 先進行多個可行更新，再將越界候選點投影回擾動範圍邊界](../../../assets/concept-animations/fgsm-pgd-trajectory.svg)

*原創示意動畫。* 左側呈現一次梯度符號更新；右側呈現受 \(\ell_\infty\) 擾動預算限制的多次小步更新。橘色虛線表示從最後一個青綠色可行迭代點出發、尚未投影的候選更新；紫色線段才表示將該候選點逐座標裁剪回右側擾動預算邊界。青綠色路徑終點是候選更新之前的迭代點，**不是投影結果**。位置、方向與時間皆為**教學示意，並非模型實測結果**。GitHub 停用 SVG 動畫時，完整路徑仍可直接閱讀。

**依時間閱讀動畫的三個階段：**0–2.5 秒，藍色 FGSM 標記完成唯一一次更新，青綠色 PGD 迭代點則在擾動預算內前進；2.5–3.5 秒，橘色候選點沿著**尚未施加限制**的梯度更新方向移動，可能越過可行域；3.5–5 秒，紫色標記將候選點投影回可行域邊界，這個返回動作**不是另一次梯度更新**。淡色完整路徑僅供靜態預覽，不表示所有更新同時發生。此 SVG 動畫播放五秒後停止，沒有播放／暫停或進度控制；需要逐階段檢視時，可對照靜態路徑與上述時間說明。

**正確解讀 FGSM 終點。** 藍色終點僅示意一次更新，並非數值精確的 \(\ell_\infty\) 符號梯度步伐。對兩個梯度分量皆非零、且不受輸入值域邊界限制的情況，FGSM 會讓每個座標恰好改變 \(\pm\epsilon\)，因此終點應位於 \(\ell_\infty\) 正方形的**角落**。若終點如圖落在內部，則須有輸入值域裁剪、零梯度分量或不同步長等額外條件。不可從藍色與青綠色箭頭的座標或相對長度推算實際梯度值。\n\n**紫色投影實際施加的限制。** 對有效輸入範圍為 \([0,1]\) 的影像，採用 \(\ell_\infty\) 擾動預算的 PGD，必須將橘色候選點 \(z\) 投影至輸入值域與擾動預算的**交集**：\(\mathcal{S}=[0,1]^d\cap\{u:\|u-x\|_\infty\le\epsilon\}\)，而非僅裁剪到影像值域。第 \(i\) 個座標須限制於 \([\max(0,x_i-\epsilon),\min(1,x_i+\epsilon)]\)。圖中僅呈現二維切面，且右側擾動預算邊界正在發揮限制作用；紫色水平返回是**特定示意情況**，不代表所有 PGD 投影都沿水平方向進行。投影只負責恢復可行性，不會重新計算損失梯度。

## 變體

- **目標式 FGSM** 把輸入推向選定的錯誤標籤，而非遠離真實標籤。
- **迭代式 FGSM** 重複較小的步伐，攻擊較強，也是 PGD 的基礎（見[投影梯度下降與對抗訓練](pgd-adversarial-training.md)）。
- **單步對抗訓練** 以 FGSM 樣本進行訓練。它成本低，但可能因單步攻擊而出現災難性過擬合。

## 結果與限制

- 在小預算下，FGSM 使未防禦的影像分類器準確率大幅下降，這個結果引起了人們對此問題的注意（Goodfellow 等人，2015）。
- 對於有防禦的模型，它是較弱的攻擊，因為單一線性步伐可能錯過對抗區域。Carlini 與 Wagner（2017）顯示，能抵抗 FGSM 的許多防禦會被更強的攻擊打破。
- 符號運算是 \(\ell_\infty\) 攻擊的啟發式作法，並不直接給出能改變標籤的最小擾動。

## 應用

- **穩健性評估**：用來回報攻擊下準確率的快速基準。
- **對抗訓練**：在訓練迴圈中低成本地產生訓練樣本。
- **教學**：基於梯度的攻擊中的標準入門範例。

## 開放問題

- 為什麼單步攻擊有時在對抗訓練後的模型上失去效果，以及如何避免災難性過擬合，仍在研究中。
- 線性解釋能否很好地描述非常深的網路，仍有爭議。

## 參考文獻

### 奠基性論文

- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — 提出 FGSM 與線性解釋。
- Szegedy, C. et al. (2014). Intriguing properties of neural networks. arXiv:1312.6199. https://arxiv.org/abs/1312.6199 — 較早展示小擾動會改變網路輸出。
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — 顯示較強的攻擊能打破能抵抗 FGSM 的防禦。

### 綜述與教科書

- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — 以迭代的 FGSM 式攻擊訓練穩健模型。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；介紹基於梯度的對抗攻擊。
