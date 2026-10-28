# 機率圖模型與貝氏方法

## 為什麼需要機率？

真實世界充滿不確定：感測器有雜訊、資訊不完整、未來無法確知。機率提供了一套**一致地表達與更新信念**的語言。

## 貝氏推論

\[
\underbrace{p(\theta\mid D)}_{\text{後驗}} = \frac{\overbrace{p(D\mid\theta)}^{\text{概似}}\;\overbrace{p(\theta)}^{\text{先驗}}}{p(D)}
\]

- **先驗**：看到資料前的信念
- **概似**：在某個假設下觀察到這些資料的機率
- **後驗**：更新後的信念

貝氏方法的好處：自然地量化不確定性、能融入先驗知識、在小資料下比較穩健。

## 機率圖模型

用圖表示變數之間的條件依賴關係，讓高維聯合分布變得可處理。

| 類型 | 圖 | 例子 |
|---|---|---|
| 貝氏網路 | 有向無環圖 | 醫療診斷、因果模型 |
| 馬可夫隨機場 | 無向圖 | 影像分割、Ising 模型 |
| 隱馬可夫模型 HMM | 鏈狀有向 | 早期語音辨識、基因序列 |
| 條件隨機場 CRF | 無向，條件於輸入 | 命名實體辨識 |
| 卡爾曼濾波 | 線性高斯狀態空間 | 追蹤、導航 |
| 主題模型 LDA | 階層式 | 文件主題分析 |

關於推論演算法與歷史上的序列模型，詳見[機率圖模型](graphical-models/index.md)。

## 推論方法

- **精確推論**：變數消去、信念傳播（樹狀圖）
- **近似推論**：
    - **抽樣**：[馬可夫鏈蒙地卡羅](mcmc/index.md)（Metropolis-Hastings、Gibbs、HMC/NUTS、朗之萬動力學）
    - **變分推論**：用簡單分布 \(q\) 近似後驗，最大化證據下界（ELBO）——VAE 就是攤銷式變分推論。方法細節見 [變分推論](variational-inference/index.md)

## 因果推論

相關不等於因果。Pearl 的因果階梯：

1. **關聯**（看到）：\(p(y\mid x)\)
2. **介入**（做）：\(p(y\mid do(x))\)
3. **反事實**（想像）：如果當初沒做 x，y 會怎樣？

工具：結構因果模型、do-calculus、潛在結果框架（Rubin）、工具變數、差異中的差異、雙重機器學習。這對醫療、經濟、政策評估中使用 AI 至關重要。

## 貝氏深度學習與不確定性

- 貝氏神經網路、MC Dropout、深度整體（deep ensembles）
- **偶然不確定性**（資料雜訊）vs **認知不確定性**（模型不知道）
- 共形預測（conformal prediction）：提供分布無關的預測區間保證，近年在醫療 AI 流行
- 高斯過程：小資料迴歸、貝氏最佳化（超參數調整、實驗設計）

## 貝氏大腦假說

認知科學與神經科學的重要觀點：**大腦是一台貝氏推論機器**。

- **知覺**：大腦結合感官證據（概似）與過去經驗（先驗）推論外界狀態。著名例子是「光從上方來」的先驗讓我們把凹凸陰影看成特定形狀。
- **多感官整合**：人類整合視覺與觸覺時，會依各自的可靠度加權，接近統計最佳（Ernst & Banks, 2002）。
- **運動控制**：Körding & Wolpert（2004）顯示人類在運動中以貝氏方式整合先驗與感覺回饋。
- **認知發展**：兒童如何從少量資料學習因果關係與詞彙（Gopnik、Tenenbaum 的研究）。
- **預測編碼與自由能原理**：見 [認知科學](../../../brain-mind/cognitive-science/index.md)。
- **精神疾病的計算觀點**：思覺失調、自閉症可能與先驗和感覺證據的權重失衡有關（計算精神醫學，見 [心理健康](../../../applications/mental-health/index.md)）。

批評：「貝氏」可能過於有彈性，幾乎能解釋任何行為；人類也有大量系統性偏離最佳推論的偏誤（見 [心理學與 AI](../../../brain-mind/psychology/index.md)）。

## 機率程式設計

用程式描述生成模型，由系統自動推論：[PyMC](https://www.pymc.io/)、[Stan](https://mc-stan.org/)、[NumPyro](https://num.pyro.ai/)、[Pyro](https://pyro.ai/)。

## 學習資源

- Koller & Friedman《Probabilistic Graphical Models》與 Coursera 課程
- Kevin Murphy《Probabilistic Machine Learning》
- Bishop《Pattern Recognition and Machine Learning》（作者提供免費 PDF）
- McElreath《Statistical Rethinking》（影片免費）
- Pearl & Mackenzie《The Book of Why》
- Griffiths, Chater & Tenenbaum《Bayesian Models of Cognition》（2024）

## 參考文獻

### 開創性論文

- Hoffman, M. D., et al. (2013). *Stochastic Variational Inference*. arXiv. https://arxiv.org/abs/1206.7051 — 以隨機梯度最佳化變分目標，讓變分推論能擴展到大型資料集。
- Neal, R. M. (2012). *MCMC using Hamiltonian dynamics*. arXiv. https://arxiv.org/abs/1206.1901 — 哈密頓蒙地卡羅法的教學文章，是現代機率程式設計系統背後的取樣器。
- Blei, D. M., et al. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — 為統計學家寫的清楚入門，以最佳化近似難解的後驗分布，並附有實例。

### 綜述與教科書

- Deisenroth, M. P., Faisal, A. A. & Ong, C. S. *Mathematics for Machine Learning*. https://mml-book.github.io/ — 涵蓋機器學習背後的機率與統計，作者提供免費 PDF。

### 文章與文件

- Bingham, E., et al. (2018). *Pyro: Deep Universal Probabilistic Programming*. arXiv. https://arxiv.org/abs/1810.09538 — 介紹建立在 PyTorch 上的機率程式語言，結合深度網路與貝氏模型。
- Carpenter, B., et al. (2015). *The Stan Math Library: Reverse-Mode Automatic Differentiation in C++*. arXiv. https://arxiv.org/abs/1509.07164 — Stan 所用的自動微分引擎，Stan 是廣泛使用的貝氏推論系統。
