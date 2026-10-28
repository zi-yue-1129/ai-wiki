---
translation_reviewed: 2026-10-28
---

# 無分類器引導

無分類器引導是一種讓條件式擴散模型更忠實地遵循條件（例如類別標籤或文字提示）的方法，代價是多樣性下降。它不需要另外的分類器：同一個網路同時以有條件與無條件的方式訓練，取樣時再把兩種預測結合起來。家族層級的概觀請見[擴散模型](index.md)頁面。

## 概述

Dhariwal 與 Nichol（2021）指出，以另外訓練的分類器的梯度來引導擴散模型，能提升樣本品質。這稱為分類器引導。它需要一個在雜訊影像上訓練的額外分類器，是一個麻煩的額外元件。Ho 與 Salimans（2022）則讓擴散模型本身同時做有條件與無條件的預測，從而去掉了分類器。

## 問題

分類器引導以多樣性換取保真度，這本身有用，但它需要第二個模型，而且必須在每一個雜訊層級上以雜訊影像訓練。這樣成本高，也很難套用到自由形式的文字等新條件。問題在於：能否只靠擴散模型本身取得引導的效果？

## 核心想法

訓練時，以機率 \(p_{\text{uncond}}\) 把條件 \(c\) 換成空白標記。同一個網路因此同時學會有條件與無條件的雜訊預測。取樣時，再以引導權重 \(w\) 結合兩種預測，\(w\) 決定條件被強調的程度。\(w = 0\) 即為單純的條件模型，\(w\) 越大則越貼近條件，多樣性也越低。

## 演算法

每個取樣步驟中，網路要執行兩次，預測結合為

\[
\tilde\epsilon = (1+w)\,\epsilon_\theta(x_t, t, c) - w\,\epsilon_\theta(x_t, t)
\]

等價地寫成 \(\tilde\epsilon = \epsilon_\theta(x_t,t) + (1+w)\big(\epsilon_\theta(x_t,t,c) - \epsilon_\theta(x_t,t)\big)\)，可見每一步是從無條件預測朝條件預測移動。\(w = 0\) 時即為單純的條件模型。每一步的成本加倍，因為需要兩次網路評估。

![無分類器引導動態向量外插：引導權重增加時，雜訊預測點沿有條件與無條件預測的差向量往外移動，再隨權重降低返回。](../../../../../assets/concept-animations/cfg-extrapolation-motion.svg)

*原創循環向量空間教學動畫，CC BY-SA 4.0。* 圖中固定的有條件與無條件雜訊預測，是將高維預測張量**示意投影至二維**。隨著示意引導權重從 \(w=0\) 增至 \(w=1.5\)，引導後的預測依 \(\epsilon_{\text{cond}}+w(\epsilon_{\text{cond}}-\epsilon_{\text{uncond}})\) 從有條件預測向外延伸；權重降低時再返回。**這不是實際去噪軌跡，也不是模型實測輸出**。參見 [Ho 與 Salimans（2022）](https://arxiv.org/abs/2207.12598)。Wiki 網站提供「暫停動畫」按鈕及偏好減少動態效果時的靜態畫面。

## 結果

論文只在 ImageNet 的 64×64 與 128×128 上評估。表中同時報告 FID 與 Inception score。

- **ImageNet 64×64，表 1**（\(p_{\text{uncond}} = 0.1\)）。未引導的模型 FID 為 1.80、IS 為 53.71。\(w = 0.1\) 時 FID 為 1.55、IS 為 66.11。\(w = 1.0\) 時 FID 升至 12.6，IS 達 170.1。\(w = 4.0\) 時 FID 為 26.22，IS 為 260.2。
- **ImageNet 128×128，表 2**（256 個取樣步）。未引導的模型 FID 為 7.27。\(w = 0.3\) 時 FID 為 2.43。論文指出，這優於 ADM-G（Dhariwal 與 Nichol 的分類器引導模型），後者的 FID 為 2.97。

## 限制

- **成本。**每一步兩次網路評估，大約使取樣成本加倍。
- **多樣性。**\(w\) 變大時，IS 上升，FID 只在一定範圍內下降。在 \(w = 4.0\) 時，64×64 的 FID 為 26.22，這反映了論文所描述的多樣性損失。
- **訓練時的選擇。**論文調整了丟棄條件的機率：在整個 IS/FID 範圍內，\(p_{\text{uncond}} = 0.5\) 的表現持續比 0.1 或 0.2 差，而 0.1 與 0.2 表現大致相當。
- **評估範圍有限。**論文的實驗只用了 ImageNet，因此報告的增益並未在其他資料集上量測。

## 關聯

- 條件通常透過[潛在擴散](latent-diffusion.md)所描述的交叉注意力路徑編碼，而論文的文字生成影像模型即使用此引導。
- 去噪器可以是 [DiT](../../../../models/transformer/dit/index.md) 或 U-Net；引導與骨幹架構無關。
- [DDIM](ddim.md) 的加速取樣器可以與引導結合。潛在擴散的論文同時使用 DDIM 步驟與無分類器引導取樣。

## 未解問題

- 引導權重應如何在取樣過程中變化？
- 能否讓引導比每一步兩次網路評估更便宜？

## 參考文獻

### 開創性論文

- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — 以結合有條件與無條件預測的方式引入不需要外部分類器的引導。短版本曾發表於 NeurIPS 2021 深度生成模型與下游應用研討會。
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — 提出分類器引導，無分類器引導即是取代它的方法。
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — 引導所套用的基礎擴散模型。
- Rombach, R. 等人（2022）。High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — 其文字生成影像模型使用無分類器引導。

### 綜述與教科書

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — 描述可控生成：以條件來引導無條件的分數模型，並附有類別條件的範例。
