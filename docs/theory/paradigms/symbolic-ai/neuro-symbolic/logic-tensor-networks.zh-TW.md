---
translation_reviewed: 2026-11-04
---

# 邏輯張量網路

邏輯張量網路（LTN）是一種神經符號框架，其中一階公式獲得 [0, 1] 中的實數真值，使知識庫能與神經網路一起訓練。本頁是[神經符號 AI](index.md)的一部分。

## 概述

邏輯能精確地陳述規則，神經網路則從資料中學習模式。LTN 要問的是：學習者能否被訓練成既滿足邏輯公理，又能擬合有標籤的範例。Serafini 與 d'Avila Garcez（2016）提出了這個方法，其一階語言的符號以向量與神經網路來落地（ground）。Badreddine 等人（2022）給出完整的框架與語意。

## 關鍵概念

- **落地（grounding）**：每個常數映射為一個向量，每個述詞映射為一個神經網路，對其論元回傳 [0, 1] 中的真值。
- **模糊連接詞**：合取、析取、否定與蘊涵以模糊運算子計算。運算子的選擇會影響模型學到的內容。
- **量詞**：全稱與存在量詞以有限組落地上的真值聚合來近似，例如使用廣義平均。
- **滿足度**：在目前的落地下，公式成立的程度。訓練的目標是最大化知識庫的滿足度。

## 運作方式

訓練結合兩個項。資料損失是有標籤落地上的一般監督式損失。滿足損失則懲罰真值偏低的公理。最小化兩者之和會同時調整述詞網路與向量落地。

假設知識庫包含述詞 Smokes(x) 與 Friends(x, y)，以及公理「對所有 x 與 y，若 x 與 y 是朋友且 x 抽菸，則 y 抽菸」。每個物件是一個向量，公理在每一對物件上求值，真值再對所有配對聚合。梯度回傳到述詞網路，使模型朝向符合公理的數值調整。此例為示意；確切的運算子與聚合方式請見原論文。

## 主要方法

- [馬可夫邏輯網路](markov-logic-networks.md)：為給定公式附上權重，定義可能世界上的機率分布。MLN 保留機率語意，而 LTN 使用實數真值。
- [可微分歸納邏輯程式設計](differentiable-ilp.md)：從範例學習規則，而非滿足事先給定的公理。

## 與其他頁面的連結

- [知識圖譜](../knowledge-graphs/index.md)提供 LTN 可以訓練的關係與公理。
- [神經符號 AI](index.md)把 LTN 放在把邏輯當作訓練約束的方法之中。
- Lake 等人（2017）主張學習系統需要這類結構化知識，這也是以公理為基礎的方法的動機。

## 應用

- **帶背景知識的學習**：在標籤稀少、但已知類別之間公理的情況下訓練分類器。
- **關係資料**：把學得的述詞與關係公理結合，例如用於知識補全。
- **檢查模型**：找出訓練後的模型違反了哪些公理，提供可解釋的行為測試。

## 開放問題

- 模糊語意與量詞聚合的選擇會改變結果，而哪些選擇是合理的，理論上尚不完整。
- 為所有物件配對落地的成本隨物件數平方增長，因此擴展到大型領域很困難。
- 滿足度是否真正反映邏輯蘊涵，而非僅是有用的近似，仍有爭議。

## 參考文獻

### 奠基性論文

- Serafini, L. & d'Avila Garcez, A. (2016). Logic tensor networks: deep learning and logical reasoning from data and knowledge. arXiv:1606.04422. https://arxiv.org/abs/1606.04422 — 提出 Real Logic，並在資料之外訓練神經落地以滿足一階公理。
- Badreddine, S., d'Avila Garcez, A., Serafini, L. & Spranger, M. (2022). Logic tensor networks. *Artificial Intelligence* 303, 103649. https://doi.org/10.1016/j.artint.2021.103649 — 完整的框架、語意與訓練方法。
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2017). *Building machines that learn and think like people*. *Behavioral and Brain Sciences* 40, e253. https://doi.org/10.1017/S0140525X16001837 — 主張類人學習需要結構化知識，例如因果與組合式模型。

### 綜述與教科書

- Garcez, A. d'A. & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave. *Artificial Intelligence Review* 56(11), 12387–12406. https://doi.org/10.1007/s10462-023-10448-w — 神經符號領域的綜述，包括實數值邏輯。
- Besold, T. R., d'Avila Garcez, A. S. & Bader, S. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv:1711.03902. https://arxiv.org/abs/1711.03902 — 綜述神經與符號方法如何結合於學習與推理。
