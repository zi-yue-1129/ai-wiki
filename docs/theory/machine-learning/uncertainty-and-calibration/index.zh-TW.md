---
translation_reviewed: 2026-10-28
---

# 不確定性量化與校準

不確定性量化是為模型的預測附上一份疑慮程度的衡量。校準則追問這份疑慮是否誠實：在模型標示為有 90% 可能的那些案例中，大約應有 90% 最後確實正確。

## 概述

預測若沒有可靠度的概念，就很難使用。判定為「惡性」的分類器是有用的，但臨床醫師需要知道這個標籤是近乎確定，還是接近擲硬幣。自駕系統也需要知道何時它的感知不可靠。這裡常有兩個問題被混在一起。第一是**校準**：模型的信心數字是否符合它實際答對的頻率。第二是較廣義的**不確定性量化**：區分資料無法告訴我們的事，與模型尚未學到的事，並回傳附有疑慮程度或保證的答案。

Guo 等人（2017）回報，現代神經網路與十年前的網路不同，校準得很差；深度、寬度、權重衰減與批次正規化都會影響其信心偏離正確的程度。網路可以非常準確，卻仍然系統性地過度自信。本主題以[機率與貝氏方法](../../paradigms/probabilistic/index.md)為基礎，後者提供不確定性的原則性語言；同時也仰賴[評估與驗證](../../paradigms/supervised/evaluation-and-validation/index.md)，來判斷模型所宣稱的疑慮是否真的有用。

## 關鍵概念

- **校準。** 若模型在信心為 \(p\) 的所有預測中，有比例 \(p\) 答對，則模型是校準的：對每個 \(p\)，\(P(\hat{Y} = Y \mid \hat{p} = p) = p\)。
- **可靠度圖。** 將預測依信心分成數個區間，並把每個區間內觀察到的準確率，對照該區間的平均信心所畫出的圖。校準良好的模型會落在對角線上。
- **期望校準誤差（ECE）。** 一個單一的摘要數字：信心與準確率之間的平均差距，以區間大小加權。它的數值取決於區間如何劃分。
- **適當評分規則。** 如對數損失或 Brier 分數這類損失函數，只有誠實的機率才能使其最小化，並同時獎勵校準良好與果斷（sharp）的預測（Gneiting 與 Raftery，2007）。
- **偶然不確定性（aleatoric）。** 資料本身不可約的雜訊，例如類別重疊、感測器雜訊，或標籤彼此不一致。增加資料無法消除它。
- **認知不確定性（epistemic）。** 關於模型本身的不確定性，來自資料有限，或來自有許多參數設定同樣能擬合資料。原則上可以隨資料增加而降低，而且在與訓練集不同的輸入上通常最大。Kendall 與 Gal（2017）在電腦視覺中同時對這兩者建模。
- **預測集。** 方法不給出單一標籤，而是給出一組標籤，使真實標籤以所選的機率落在其中。[保形預測](conformal-prediction/index.md)能以形式化的保證產生這種集合。

## 運作方式

多數不確定性工作依循三個階段，如下圖所示。先訓練模型。接著用保留的校準集衡量校準偏差，必要時再擬合修正。最後，在新資料上檢查修正後的輸出，並用於決策，例如棄權或把案例交給人類。

```mermaid
flowchart LR
  T[訓練模型] --> C[保留的校準集]
  C --> R[以可靠度圖與 ECE 衡量]
  R --> F{是否校準不良？}
  F -- 是 --> S[訓練後修正，例如溫度縮放]
  F -- 否 --> D[部署]
  S --> D
  D --> A[棄權、轉交或回報一個集合]
```

上述兩類不確定性可以分開。對迴歸而言，令網路預測平均值 \(\mu_\theta(x)\) 與變異數 \(\sigma^2_\theta(x)\)，兩者都依賴參數 \(\theta\)。全變異數定律給出

\[
\operatorname{Var}[y \mid x] = \underbrace{\mathbb{E}_\theta\big[\sigma^2_\theta(x)\big]}_{\text{aleatoric}} + \underbrace{\operatorname{Var}_\theta\big[\mu_\theta(x)\big]}_{\text{epistemic}}.
\]

對分類而言，總預測熵以相同方式分解：一項是期望熵，視為偶然不確定性；另一項是標籤與參數之間的互資訊，視為認知不確定性。兩種分解都需要 \(\theta\) 上的分布。精確的貝氏預測分布為

\[
p(y \mid x, \mathcal{D}) = \int p(y \mid x, \theta)\, p(\theta \mid \mathcal{D})\, d\theta,
\]

而對深度網路來說，這個積分難以計算。貝氏神經網路（BNN）在權重上放置分布，並近似此積分，例如以 Blundell 等人（2015）的變分推論方法實現。兩種較便宜、被廣泛使用的近似是 [MC 丟棄法](mc-dropout/index.md)與[深度集成](deep-ensembles/index.md)。Wilson 與 Izmailov（2020）主張，深度集成提供了貝氏邊緣化的有效近似。

就校準而言，最常見的做法是訓練後修正。在 softmax 之前，以單一純量除以網路的 logit。這就是[溫度縮放](temperature-scaling/index.md)，Guo 等人（2017）發現它在多數受測資料集上出奇地有效。校準以 ECE 衡量，由分箱後的預測計算：

\[
\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n}\,\bigl|\operatorname{acc}(B_m) - \operatorname{conf}(B_m)\bigr|,
\]

其中 \(B_m\) 是第 \(m\) 個區間內的預測集合，\(n\) 是預測總數。

[保形預測](conformal-prediction/index.md)採取不同的路線。它不試圖讓機率變得正確，而是用校準集在非保形分數上選定門檻，並回傳所有通過門檻的標籤。若校準資料與測試資料可交換，這些集合以至少 \(1-\alpha\) 的機率涵蓋真實答案，且與底層模型無關。

## 關鍵方法

這裡比較四種代表性方法，每種都有自己的頁面可以查閱細節。

| 方法 | 不確定性的類型 | 做法 | 頁面 |
|---|---|---|---|
| 溫度縮放 | 校準，訓練後 | 在保留資料上擬合一個溫度，並重新縮放 logit | [溫度縮放](temperature-scaling/index.md) |
| 深度集成 | 認知，近似 | 從不同起點訓練數個網路並平均其預測 | [深度集成](deep-ensembles/index.md) |
| MC 丟棄法 | 認知，近似 | 測試時仍保持丟棄法啟用，並平均多次隨機前向傳播 | [MC 丟棄法](mc-dropout/index.md) |
| 保形預測 | 涵蓋率保證 | 包裹任一模型，使其回傳具有指定涵蓋率的集合 | [保形預測](conformal-prediction/index.md) |

溫度縮放最便宜，且在訓練後套用。集成最昂貴，因為它要訓練數個網路。MC 丟棄法只重用一個已訓練網路，代價是粗糙的近似。保形預測提供其他三者沒有的保證，但只限於邊際意義上。

## 相關連結

[機率方法](../../paradigms/probabilistic/index.md)保有貝氏基礎，其中有關貝氏深度學習的一節與本頁有重疊。[主動學習](../../paradigms/active/index.md)利用不確定性來選擇要標註的範例；[不確定性抽樣](../../paradigms/active/uncertainty-sampling/index.md)的效果取決於它所讀取的不確定性，因此校準不良會直接削弱標籤的選擇。

大腦同樣必須在不確定下行動。Knill 與 Pouget（2004）主張神經編碼與計算會明確地表徵不確定性，而許多知覺可以描述為近似的貝氏推論。Ernst 與 Banks（2002）發現，人們會依可靠度比例地結合視覺與觸覺線索，接近統計上最優的權重。Fleming 與 Lau（2014）回顧了如何測量後設認知，也就是一個人的信心與其自身準確率的吻合程度，這本質上正是對模型提出的校準問題。人類面向請見[認知科學](../../../brain-mind/cognitive-science/index.md)、[預測編碼](../../../brain-mind/predictive-coding/index.md)與[啟發法與偏誤](../../../brain-mind/cognitive-science/heuristics-and-biases/index.md)。

## 應用

- **醫學診斷。** 校準過的機率與保形預測集合，能讓系統回報一組合理的診斷範圍，或在不確定性高時延後決定。Angelopoulos 與 Bates（2021）把醫學診斷列為需要不確定性量化的場景。見[醫療保健](../../../applications/healthcare/index.md)。
- **自動駕駛。** 當感知系統回報其信心時，規劃器可以對可疑的偵測更加謹慎。見[自動駕駛](../../../applications/autonomous-driving/index.md)。
- **金融與風險。** 定價與曝險的決策仰賴校準良好的機率。見[金融](../../../applications/finance/index.md)。
- **人機團隊。** 系統所顯示的信心會影響人們依賴它的程度，因此校準也是[自動化信任](../../../society/human-ai-interaction/trust-in-automation/index.md)的一部分。

## 未解問題

- **分布偏移下的校準。** Ovadia 等人（2019）顯示，在分布內資料上擬合的校準，會在輸入改變時惡化。在沒有新標籤的情況下，要在新分布上維持準確校準，仍然困難。
- **邊際保證與條件保證。** 保形保證是對輸入取平均後成立。Lei 等人（2016）為迴歸證明了有限樣本的邊際涵蓋率。要對特定子群或特定輸入保證涵蓋率，是更困難的目標。
- **語言模型。** 語言模型的符號機率，或模型以文字陳述的信心，是否校準良好，仍是活躍的問題。
- **不確定性的切分。** 在實務中將偶然與認知不確定性分開，取決於模型與資料如何定義。Hüllermeier 與 Waegeman（2021）回顧了這些概念與建立其上的方法。

## 參考文獻

### 開創性論文

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. ICML. https://arxiv.org/abs/1706.04599 — 指出現代網路校準不良，並說明溫度縮放是一種簡單而有效的訓練後修正。
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — 比較不同學習器產生校準機率的能力，以及訓練後校準如何改變它們。
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*. https://doi.org/10.1198/016214506000001437 — 發展獎勵誠實機率預測的評分規則理論，是校準評估的基礎。
- Blundell, C., Cornebise, J., Kavukcuoglu, K. & Wierstra, D. (2015). Weight uncertainty in neural networks. ICML. https://arxiv.org/abs/1505.05424 — Bayes by Backprop，以變分目標學習網路權重上的分布。
- Kendall, A. & Gal, Y. (2017). What uncertainties do we need in Bayesian deep learning for computer vision? NeurIPS. https://arxiv.org/abs/1703.04977 — 在分割與深度迴歸任務中同時對偶然與認知不確定性建模，並以此切分設計損失函數。
- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J. & Wasserman, L. (2016). Distribution-free predictive inference for regression. arXiv. https://arxiv.org/abs/1604.04173 — 發展迴歸的分割與完整保形推論，並具有有限樣本的邊際涵蓋率。
- Knill, D. C. & Pouget, A. (2004). The Bayesian brain: the role of uncertainty in neural coding and computation. *Trends in Neurosciences*. https://doi.org/10.1016/j.tins.2004.10.007 — 回顧文章，主張大腦表徵不確定性，並進行近似的貝氏計算。
- Ernst, M. O. & Banks, M. S. (2002). Humans integrate visual and haptic information in a statistically optimal fashion. *Nature*. https://doi.org/10.1038/415429a — 顯示人們依感官線索的可靠度來結合它們。

### 綜述與教科書

- Hüllermeier, E. & Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://arxiv.org/abs/1910.09457 — 介紹偶然與認知不確定性的區分，以及量化它們的方法。
- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — 綜述深度網路中不確定性的類型、來源與估計方法。
- Angelopoulos, A. N. & Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv. https://arxiv.org/abs/2107.07511 — 關於保形預測的實作導向教學，附有 Python 範例，並延伸至分布偏移與時間序列。
- Fleming, S. M. & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*. https://doi.org/10.3389/fnhum.2014.00443 — 回顧測量後設認知的方法，即一個人的信心與其自身準確率的吻合程度。

### 文章與文件

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — 在分布偏移下對不確定性方法進行的大規模基準測試，發現傳統的訓練後校準表現不足。
- Wilson, A. G. & Izmailov, P. (2020). Bayesian deep learning and a probabilistic perspective of generalization. NeurIPS. https://arxiv.org/abs/2002.08791 — 主張深度集成近似貝氏邊緣化，且邊緣化能改善校準。
