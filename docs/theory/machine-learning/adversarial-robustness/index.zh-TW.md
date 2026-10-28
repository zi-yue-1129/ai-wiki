---
translation_reviewed: 2026-10-28
---

# 對抗樣本與穩健性

對抗樣本是經過微小（常常難以察覺）擾動後的輸入，會使模型產生錯誤輸出。穩健性研究的是如何使模型抵抗這類擾動，以及如何衡量它們是否真的做到。本頁是[機器學習](../index.md)的一部分。針對大型語言模型的攻擊，見[LLM 安全](../../../engineering/llm-security/index.md)。

## 概述

Szegedy 等人（2014）指出，最先進的影像分類器可能被人眼察覺不到的微小改動所欺騙。Goodfellow 等人（2015）主張，這種現象來自高維模型的線性行為，而非罕見的失誤。此後攻擊越來越強，防禦經過測試，也常被打破，而領域也發展出對某些擾動大小提供保證的認證方法。

## 關鍵概念

- **威脅模型**：擾動的範數與預算 \(\epsilon\)，以及攻擊者掌握的資訊（白箱或黑箱存取）。
- **攻擊**：在預算內搜尋擾動，使損失增加或使標籤改變的程序。
- **對抗訓練**：以對抗樣本進行訓練，使模型學會抵抗所訓練的那一類攻擊。
- **認證穩健性**：對每個輸入都保證，在預算內的任何擾動都不會改變預測。

## 運作方式

多數攻擊會計算損失對輸入的梯度，並在預算內沿著使損失增加的方向移動輸入。最簡單的是單步攻擊（FGSM）（Goodfellow 等人，2015）。更強的攻擊重複較小的步伐，並每步投影回預算之內，這就是投影梯度下降（Madry 等人，2018）。防禦通常以受攻擊的輸入進行訓練，或為平滑後的分類器提供機率性的認證（Cohen 等人，2019）。

## 主要方法

- [快速梯度符號法](fgsm.md)：單步攻擊，是許多對抗訓練研究的基礎。
- [投影梯度下降與對抗訓練](pgd-adversarial-training.md)：強的迭代攻擊，以及以它為基礎的訓練方法。
- [隨機平滑](randomized-smoothing.md)：一種認證方法，為平滑後的分類器給出 \(\ell_2\) 半徑。

## 與其他頁面的連結

- [泛化理論](../../paradigms/supervised/generalization-theory/index.md)說明為何標準訓練無法產生穩健的間隔。
- [LLM 安全](../../../engineering/llm-security/index.md)涵蓋針對語言模型的提示層級攻擊，與此處的像素層級設定不同。
- [分布外偵測](../ood-detection/index.md)處理並非對抗性、但不熟悉的輸入，這些輸入常需要類似的工具。

## 應用

- **安全關鍵的視覺**：檢查交通號誌或醫療分類器在小幅雜訊下不會翻轉判斷。
- **安全性**：偵測或抵抗針對垃圾郵件或惡意程式分類器的逃逸攻擊。
- **基準測試**：與乾淨準確率一併報告穩健準確率，以便公平比較模型。

## 開放問題

- 穩健性與乾淨準確率可能互相取捨。Tsipras 等人（2019）顯示，在某些學習設定中這種取捨是固有的，而不只是現有方法的副產品。
- 經驗性的防禦常被更強的適應性攻擊打破，因此聲稱的穩健性需要以適應性攻擊評估。
- 對多數實用模型而言，認證半徑很小，把認證擴展到大型網路很困難。

## 參考文獻

### 奠基性論文

- Szegedy, C. et al. (2014). Intriguing properties of neural networks. arXiv:1312.6199. https://arxiv.org/abs/1312.6199 — 顯示深度網路的輸入經小擾動後，輸出即可能改變。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — 提出 FGSM 與對抗樣本的線性解釋。
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — 提出更強的攻擊，打破了多種防禦，並設定了評估標準。
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — 提出投影梯度下降攻擊與對抗訓練。
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — 為高斯平滑後的分類器給出認證的 \(\ell_2\) 半徑。

### 綜述與教科書

- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — 在簡單設定中顯示標準準確率與穩健性之間的根本取捨。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋對抗樣本與穩健性，並在對抗方法一章介紹。
