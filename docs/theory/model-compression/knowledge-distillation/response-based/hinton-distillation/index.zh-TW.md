---
translation_reviewed: 2026-10-28
---

# Hinton 蒸餾

Hinton、Vinyals 與 Dean 在 2015 年的論文是現代知識蒸餾的起點。它以大型教師經軟化的輸出訓練小模型，使學生學到錯誤答案的相對機率，而不只是正確標籤。他們的配方是其他[以回應為基礎](../index.zh-TW.md)方法所依據的標準目標。

## 問題

網路集成是最準確的模型，但部署成本太高。需要一個能捕捉集成知識的單一模型。

## 核心想法

以教師的軟化輸出訓練小模型。溫度會攤平教師的機率，使近似的錯誤類別（它們承載類別如何相關的資訊）對學生變得可見。學生同時以真實標籤訓練。

## 公式或演算法

組合損失為

\[
\mathcal{L} = (1-\alpha)\, \mathrm{CE}(y, \sigma(z_s)) + \alpha\, T^2\, \mathrm{KL}\!\left(\sigma(z_t/T)\,\Vert\,\sigma(z_s/T)\right)
\]

其中 \(z_s\) 與 \(z_t\) 分別是學生與教師的 logits，\(\sigma\) 是 softmax，\(T\) 是溫度，\(\alpha\) 為兩項的權重。因子 \(T^2\) 使不同溫度下的梯度大小保持相近。論文也提議訓練針對類別子集的專家模型，這些模型可以平行訓練。

## 結果

摘要報告在 MNIST 上有出人意料的結果，並顯著改善商業語音系統的聲學模型。摘要沒有給出數字，需要的讀者應查閱全文。

## 限制

此方法需要教師在訓練輸入上的輸出，對大型教師而言成本高。論文的實驗以今日標準來看規模很小。

## 開放問題與相關變體

- **溫度的選擇。** 最佳溫度取決於任務，通常靠搜尋找到。
- **相關：** [DistilBERT](../distilbert/index.zh-TW.md) 把同一目標應用到語言模型預訓練上，而[以特徵為基礎](../../feature-based/index.zh-TW.md)的方法則加入中間目標。

## 相關連結

此目標是各種[訓練](../../../../../engineering/training/index.zh-TW.md)與部署蒸餾做法的基礎。學生從教師的分級信念中學習，與學習者吸收老師答案細微之處的方式有類比，見[認知科學](../../../../../brain-mind/cognitive-science/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 以溫度軟化的蒸餾目標，搭配組合的任務損失。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 在輸出蒸餾之外加入中間提示目標。
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 把同樣的軟目標應用於語言模型預訓練。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 把以輸出為基礎的蒸餾視為此領域的起點。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 顯示當教師比學生大很多時，學生的表現會下降。
