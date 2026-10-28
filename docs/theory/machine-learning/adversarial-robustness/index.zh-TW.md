---
translation_reviewed: 2026-10-28
---

# 對抗樣本與穩健性

對抗樣本是指經過一個小到人眼難以察覺的擾動所改變的輸入，但這個擾動足以讓已訓練的模型自信地答錯。對抗穩健性研究如何讓模型抵抗此類輸入、如何誠實地衡量這種抵抗力，以及它在準確率上需要付出什麼代價。

## 概述

Szegedy et al.（2013）指出，深度圖像分類器可以被輸入中難以察覺的改動推向錯誤的答案。後續研究發現，同樣的脆弱性也存在於許多其他情境中，而且錯誤的預測往往伴隨高信心（Goodfellow et al., 2014）。

這個領域的發展呈現出一場軍備競賽。許多防禦被提出，而許多防禦又被針對它們調整過的更強攻擊所擊破。Athalye et al.（2018）檢視了 ICLR 2018 上的防禦，發現九個之中有七個依賴混淆梯度；他們的攻擊完全破解了其中六個，部分破解了一個。Croce 與 Hein（2020）後來回報，在他們測試的五十多個已發表防禦中，除一個以外，其穩健準確率都低於原論文所宣稱的數值。因此，評估與建構防禦同樣困難。

穩健性也有代價。模型可以對小擾動變得穩健，但在乾淨資料上的準確率卻下降；Tsipras et al.（2018）證明，這種張力在簡單的設定中確實可以被證明。本主題與[不確定性與校準](../uncertainty-and-calibration/index.md)相連，因為在對抗輸入上的自信錯誤，正是校準的失敗；也與[泛化](../../paradigms/supervised/generalization-theory/index.md)相連，因為穩健學習有其本身的樣本數需求。

## 關鍵概念

- **對抗樣本。** 一個輸入 \(x' = x + \delta\)，其擾動 \(\delta\) 位於一個小集合內，例如 \(\|\delta\|_\infty \le \varepsilon\)，並且模型對它的分類結果與對 \(x\) 的不同。
- **威脅模型。** 攻擊的完整規格：擾動集合、攻擊者的目標（任何錯誤答案，或指定的錯誤答案），以及攻擊者所掌握的資訊。在白箱攻擊中，攻擊者可以看到模型的梯度；在黑箱攻擊中，攻擊者只能查詢模型。
- **可遷移性。** 針對某一模型所製作的對抗樣本，常常也能騙過另一個模型。Papernot et al.（2016）利用這一點建立黑箱攻擊，做法是訓練一個替代模型，並針對它製作樣本。
- **穩健準確率與標準準確率。** 穩健準確率是在威脅模型內、經擾動輸入上的準確率；標準準確率是在乾淨輸入上的準確率。
- **梯度遮罩。** 使梯度失去資訊的防禦，可能看似能抵抗基於梯度的攻擊，實際上並不穩健。Athalye et al.（2018）說明了這種效應，以及如何繞過它。
- **可證明穩健性。** 證明在威脅模型內的任何擾動都無法改變預測，並在一個指定的半徑內成立。

## 運作方式

攻擊與防禦是一場雙人博弈。攻擊者在擾動預算內選擇擾動，以最大化損失；防禦者選擇參數，以最小化這些最壞情況輸入上的損失。這可由穩健目標表達：

\[
\min_\theta \; \mathbb{E}_{(x,y)\sim\mathcal{D}} \Big[ \max_{\|\delta\|\le\varepsilon} L(f_\theta(x+\delta), y) \Big].
\]

內層的最大化即為攻擊。其標準近似包括單步的 [FGSM](fgsm/index.md)，以及迭代的投影梯度法，後者也是對抗訓練的核心。防禦最好以設計者未曾預料的攻擊來評判，因此評估步驟本身也是方法的一部分。

```mermaid
flowchart LR
  A[威脅模型：範數、預算、掌握的資訊] --> B[攻擊：在預算內最大化損失]
  B --> C[防禦：對抗訓練或平滑]
  C --> D[以適應性攻擊評估]
  D -->|發現更強的攻擊| B
  C --> E[認證：證明一個半徑]
```

從這個圖景可以得出三類防禦。對抗訓練在學習過程中使用內層攻擊。可證明方法為一個指定的半徑給出保證，通常需要付出準確率或計算量的代價。偵測方法試圖標記對抗輸入，但多數已被證明在適應性攻擊下失效（Carlini et al., 2019），這也是圖中評估迴圈之所以重要的原因。

## 主要方法

這裡比較三個里程碑式的方法，每個方法都有專屬頁面說明細節。

| 方法 | 類型 | 作法 | 頁面 |
|---|---|---|---|
| 快速梯度符號法（Goodfellow et al., 2014） | 攻擊 | 在 \(\ell_\infty\) 球內走一步固定大小的梯度符號步 | [FGSM](fgsm/index.md) |
| PGD 與對抗訓練（Madry et al., 2017） | 攻擊與防禦 | 以多個投影步作為內層攻擊，並以極小極大目標進行訓練 | [PGD 與對抗訓練](pgd-adversarial-training/index.md) |
| 隨機平滑（Cohen et al., 2019） | 可證明的防禦 | 對高斯雜訊下的預測取平均，以認證一個 \(\ell_2\) 半徑 | [隨機平滑](randomized-smoothing/index.md) |

FGSM 成本低，也是線性性解釋的基礎，但面對預先考慮到它的防禦者時較為薄弱。PGD 是強得多的攻擊，也是對抗訓練常用的基礎，但訓練成本可能高出數倍。隨機平滑是三者中唯一提供保證的方法，而且僅限於 \(\ell_2\) 擾動。

## 連結

大腦為這個主題提供了有用的比較對象。對抗脆弱性是深度視覺模型與人類感知之間值得注意的差異之一，相關討論見[視覺感知](../../../brain-mind/visual-perception/index.md)。Geirhos et al.（2018）顯示，以 ImageNet 訓練的 CNN 嚴重依賴紋理，而以形狀偏好訓練可提升對部分圖像失真的穩健性。Elsayed et al.（2018）發現，從視覺模型遷移而來的樣本，也能改變受時間限制之人類觀察者的判斷，因此人類並非完全免疫。Bowers et al.（2022）主張，這類失效正是深度網路並非良好人類視覺模型的原因之一。另見 [NeuroAI](../../../brain-mind/neuroai/index.md)。

語言模型帶來不同類型的攻擊。輸入是離散的 token，而非像素，因此梯度步驟必須加以調整。Zou et al.（2023）找到了能跨模型遷移的對抗後綴，[LLM 安全](../../../engineering/llm-security/index.md)則詳細涵蓋這類攻擊，以及提示注入與越獄。

評估方法，包括測試任何防禦所需的適應性攻擊，見[評估](../../../engineering/evaluation/index.md)。

## 應用

- **基準測試。** 如以 AutoAttack 為基礎的 RobustBench 排行榜（Croce et al., 2020）等標準評估套件，使影像分類器能在固定的威脅模型下相互比較。
- **實體世界的感知。** Kurakin et al.（2016）顯示，對抗圖像經相機擷取後仍會被誤分類，這對[自動駕駛](../../../applications/autonomous-driving/index.md)等系統十分重要。
- **可證明的分類器。** Cohen et al.（2019）產生了一個具可證明保證的 ImageNet 分類器，可作為可證明方法在大規模上能達到何種程度的參考點。
- **安全系統。** 任何可被對手探測的分類器，包括[網路安全](../../../applications/cybersecurity/index.md)中所用的分類器，都面臨相同的威脅模型。

## 未解問題

- **為何對抗樣本會存在？** Goodfellow et al.（2014）歸因於網路的線性行為。Ilyas et al.（2019）則主張，模型所用的特徵具有預測力卻不穩健，這是一種不依賴線性性的不同解釋。
- **準確率的權衡是否固有？** Zhang et al.（2019）把穩健誤差拆成自然分類誤差與邊界誤差，並設計了一個在兩者之間權衡的訓練目標。這種權衡能否被消除，目前尚未解決。
- **需要多少資料？** Schmidt et al.（2018）顯示，穩健學習所需的樣本數可能遠多於標準學習，這或許可以解釋部分的困難。
- **如何信任評估結果？** Carlini et al.（2019）提供了評估防禦的指引，而聲稱的穩健性與實測穩健性之間的落差顯示，此問題仍然開放。

## 參考文獻

### 開創性論文

- Szegedy, C. et al. (2013). *Intriguing properties of neural networks*. arXiv. https://arxiv.org/abs/1312.6199 — 首次顯示，難以察覺的輸入擾動可以改變深度圖像分類器的輸出。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples*. arXiv. https://arxiv.org/abs/1412.6572 — 提出 FGSM，並主張網路的線性性解釋了對抗脆弱性。
- Papernot, N. et al. (2016). *Transferability in Machine Learning: from Phenomena to Black-Box Attacks using Adversarial Samples*. arXiv. https://arxiv.org/abs/1605.07277 — 研究可遷移性，並透過替代模型建立黑箱攻擊。
- Carlini, N. & Wagner, D. (2016). *Towards Evaluating the Robustness of Neural Networks*. arXiv. https://arxiv.org/abs/1608.04644 — 提出更強的、以最佳化為基礎的攻擊，能擊敗防禦性蒸餾。
- Madry, A. et al. (2017). *Towards Deep Learning Models Resistant to Adversarial Attacks*. arXiv. https://arxiv.org/abs/1706.06083 — 把穩健性表述為極小極大最佳化，並以 PGD 作為訓練攻擊。
- Zhang, H. et al. (2019). *Theoretically Principled Trade-off between Robustness and Accuracy*. arXiv. https://arxiv.org/abs/1901.08573 — 把穩健誤差拆為自然誤差與邊界誤差，並提出 TRADES 訓練目標。
- Tsipras, D. et al. (2018). *Robustness May Be at Odds with Accuracy*. arXiv. https://arxiv.org/abs/1805.12152 — 在簡單的設定中，證明標準準確率與對抗穩健性之間存在可證明的張力。
- Kurakin, A., Goodfellow, I. J. & Bengio, S. (2016). *Adversarial examples in the physical world*. arXiv. https://arxiv.org/abs/1607.02533 — 顯示由手機相機擷取的對抗圖像，仍會被大量誤分類。
- Cohen, J. M., Rosenfeld, E. & Kolter, J. Z. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. arXiv. https://arxiv.org/abs/1902.02918 — 證明高斯平滑的緊密 \(\ell_2\) 保證，並回報在 ImageNet 上的可證明準確率。

### 調查與教科書

- Akhtar, N. & Mian, A. (2018). *Threat of Adversarial Attacks on Deep Learning in Computer Vision: A Survey*. arXiv. https://arxiv.org/abs/1801.00553 — 調查電腦視覺中的攻擊方法、其所構成的威脅，以及所提出的防禦。
- Bai, T. et al. (2021). *Recent Advances in Adversarial Training for Adversarial Robustness*. arXiv. https://arxiv.org/abs/2102.01356 — 調查對抗訓練，以及它所引發的泛化問題。

### 文章與文件

- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — 指出梯度遮罩是虛假安全感的來源，並擊破了數個 ICLR 2018 的防禦。
- Croce, F. & Hein, M. (2020). *Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks*. arXiv. https://arxiv.org/abs/2003.01690 — 提出 AutoAttack，所得的穩健準確率常低於許多已發表防禦的報告。
- Croce, F. et al. (2020). *RobustBench: a standardized adversarial robustness benchmark*. arXiv. https://arxiv.org/abs/2010.09670 — 介紹標準化穩健性評估的排行榜與函式庫。
- Schmidt, L. et al. (2018). *Adversarially Robust Generalization Requires More Data*. arXiv. https://arxiv.org/abs/1804.11285 — 證明穩健學習與標準學習之間的樣本複雜度差距，並以圖像實驗加以驗證。
- Carlini, N. et al. (2019). *On Evaluating Adversarial Robustness*. arXiv. https://arxiv.org/abs/1902.06705 — 提供評估防禦的方法論指引，以及常見的陷阱。
- Geirhos, R. et al. (2018). *ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness*. arXiv. https://arxiv.org/abs/1811.12231 — 顯示 CNN 比人類更依賴紋理，而形狀偏好能提升對失真的穩健性。
- Bowers, J. S. et al. (2022). Deep problems with neural network models of human vision. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X22002813 — 主張深度網路作為人類視覺模型的能力不足，並以對抗脆弱性等失效為例。
- Elsayed, G. F. et al. (2018). *Adversarial Examples that Fool both Computer Vision and Time-Limited Humans*. arXiv. https://arxiv.org/abs/1802.08195 — 顯示從視覺模型遷移而來的對抗樣本，也會改變受時間限制之人類觀察者的判斷。
- Ilyas, A. et al. (2019). *Adversarial Examples Are Not Bugs, They Are Features*. arXiv. https://arxiv.org/abs/1905.02175 — 把對抗脆弱性歸因於資料中具預測力卻不穩健的特徵。
- Zou, A. et al. (2023). *Universal and Transferable Adversarial Attacks on Aligned Language Models*. arXiv. https://arxiv.org/abs/2307.15043 — 以梯度搜尋找出可跨提示與閉源模型遷移的對抗後綴。
