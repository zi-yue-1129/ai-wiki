---
translation_reviewed: 2026-10-28
---

# Hinton 蒸餾

Hinton、Vinyals 與 Dean 在 2015 年的論文是現代知識蒸餾的起點。它以大型教師經軟化的輸出訓練小模型，使學生學到錯誤答案的相對機率，而不只是正確標籤。他們的配方是其他[以回應為基礎](../index.zh-TW.md)方法所依據的標準目標。

## 問題

網路集成是最準確的模型，但部署成本太高。需要一個能捕捉集成知識、同時足夠便宜、可以在生產環境中執行的單一模型。

## 核心想法

以教師的軟化輸出訓練小模型。溫度 \(T\) 會攤平教師的機率，使近似的錯誤類別變得可見。這些近似類別承載了類別如何相關的資訊，例如手寫數字 7 的圖片比 0 更接近 1。學生同時以真實標籤訓練，因此軟目標是額外的訊號，而不是取代標籤。

## 公式或演算法

組合損失為

\[
\mathcal{L} = (1-\alpha)\, \mathrm{CE}(y, \sigma(z_s)) + \alpha\, T^2\, \mathrm{KL}\!\left(\sigma(z_t/T)\,\Vert\,\sigma(z_s/T)\right)
\]

其中 \(z_s\) 與 \(z_t\) 分別是學生與教師的 logits，\(\sigma\) 是 softmax，\(T\) 是溫度，\(\alpha\) 為兩項的權重。因子 \(T^2\) 使不同溫度下的梯度大小保持相近。

論文還給出一項分析。當溫度相對於 logits 的大小很高時，軟目標項對每個學生 logit \(z_i\) 的梯度近似為

\[
\frac{\partial \mathcal{L}}{\partial z_i} \approx \frac{1}{N T^2}\,(z_i - v_i)
\]

其中 \(v_i\) 是教師的 logits，\(N\) 是類別數。在論文對 logits 零均值的假設下，高溫的蒸餾等同於讓學生的 logits 匹配教師的 logits。論文也提出專家集成：一個通才模型加上許多專家模型，每個專家只針對一組容易混淆的類別訓練。與混合專家不同，這些專家可以快速且平行地訓練。

## 結果

在 MNIST 上，論文報告的測試錯誤數如下：

- 未正則化的 800 單元基線：146 個錯誤。
- 同樣的 800 單元架構，以大型教師的軟目標在溫度 20 下訓練：74 個錯誤。
- 大型且重度正則化的教師網路本身：67 個錯誤。

摘要也指出，把集成的知識蒸餾到單一網路後，可以明顯改善一個被大量使用的商業聲學模型。該實驗的數字見全文。

## 限制

此方法需要教師在訓練輸入上的輸出，對大型教師而言成本很高。溫度是需要搜尋的超參數，而且實驗以今日的標準來看規模很小：以上結果都在 MNIST 上，另一個應用是一個商業語音系統。

## 未解問題與相關變體

- **溫度選擇。** 最佳溫度取決於任務，通常靠搜尋找到。論文的梯度分析只在高溫極限下成立。
- **特徵目標。** Hinton 的方法只匹配輸出。[FitNets](../../feature-based/fitnets/index.zh-TW.md) 加入中間層提示，而[注意力轉移](../../feature-based/attention-transfer/index.zh-TW.md)透過中間的注意力圖傳遞知識。
- **語言模型。** [DistilBERT](../distilbert/index.zh-TW.md) 在語言模型預訓練時套用同樣的目標。

## 與其他主題的連結

此目標是[訓練](../../../../../engineering/training/index.zh-TW.md)與部署中所用蒸餾的基礎。學生從教師分級的信念中學習，這個想法類似於學習者如何吸收老師回答中的細微差別；見[認知科學](../../../../../brain-mind/cognitive-science/index.zh-TW.md)。

## 參考文獻

### 奠基性論文

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 溫度軟化的蒸餾目標、高溫下 logit 匹配的分析、MNIST 結果與專家集成。
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 在輸出蒸餾之外加入中間層提示；較深的學生以約十分之一的參數量在 CIFAR-10 上超越較大的教師。
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — 在 BERT 預訓練時套用軟目標；體積約小 40%、速度約快 60%，同時保留約 97% 的語言理解能力。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J., Tao, D. (2021). *Knowledge Distillation: A Survey*. arXiv:2006.05525. https://arxiv.org/abs/2006.05525 — 蒸餾方法綜述；arXiv 頁面列出已發表版本為 https://doi.org/10.1007/s11263-021-01453-z。將基於輸出的蒸餾視為該領域的起點。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 發現教師比學生大很多時，學生的表現會下降；提出中間大小的教師助理。
