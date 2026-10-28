---
tags:
  - supervised learning
  - learning theory
  - generalization
---

# 泛化與統計學習理論

為什麼在有限樣本上擬合的模型，能在未見過的資料上表現良好？統計學習理論給出了條件與界限，而深度學習則揭示了古典理論的不足之處。

## 設定

資料 $(x,y)$ 獨立同分布地取自未知分布 $P$。**真實風險**為 $R(f)=\mathbb{E}[L(f(x),y)]$；學習器只能看到**經驗風險** $\hat R(f)$。**泛化差距**則是 $R(f)-\hat R(f)$。

## 偏差—變異權衡

對平方誤差而言，期望的測試誤差可以分解為偏差平方＋變異＋不可約雜訊。簡單的模型偏差高；彈性大的模型變異高。古典的智慧是選擇兩者之間的最佳點。

## 容量度量與界限

| 概念 | 想法 |
|---|---|
| PAC 學習（Valiant, 1984） | 以至少 $1-\delta$ 的機率，使用多項式數量的樣本，使誤差 $\le\epsilon$ |
| VC 維度 | 假說類別能打散的最大集合；樣本複雜度隨之成長 |
| Rademacher 複雜度 | 假說類別擬合隨機雜訊的能力；依賴資料 |
| 一致穩定性 | 改變一個訓練點，輸出只會有很小的改變 |
| PAC-Bayes | 透過與先驗的 KL 散度，約束後驗分布於模型上的平均風險 |
| 間隔界限 | 間隔越大，界限越緊，且與維度無關 |

典型的界限形式為 $R(f)\le\hat R(f)+O\big(\sqrt{(\text{複雜度}+\log(1/\delta))/n}\big)$。

## 深度學習改變了什麼

- 網路可以擬合隨機標籤（Zhang et al., 2017），因此天真的容量界限變得毫無意義。
- **雙下降**（Belkin et al., 2019）：隨著模型變大，測試誤差先下降、在內插門檻附近上升，然後再次下降。
- 過參數化模型依靠最佳化器的隱式偏置、平坦的極小值與資料結構來泛化。縮放定律（Kaplan et al., 2020）描述了這種經驗規律。

## 沒有免費的午餐

沒有任何學習器能在所有可能的問題上勝過其他學習器；學習之所以有效，是因為真實資料具有結構（平滑性、組合性、低維性）。這正是卷積等架構所編碼的**歸納偏誤**。

## 與其他概念的連結

分布偏移會打破獨立同分布的假設；若要在沒有此假設下的保證，請見[遷移理論](../../transfer/index.md)與[線上學習](../../online/index.md)。

## 參考文獻

### 開創性論文

- Valiant (1984), "A theory of the learnable", *Communications of the ACM* 27(11). https://mlanthology.org/misc/1984/valiant1984misc-theory — 提出 PAC 學習，即從樣本中能學到什麼的形式化模型。
- Zhang et al. (2017), "Understanding deep learning requires rethinking generalization", ICLR, arXiv:1611.03530. https://mlanthology.org/iclr/2017/zhang2017iclr-understanding — 顯示大型網路可以擬合隨機標籤，這打破了古典的容量界限。
- Jacot, Gabriel & Hongler (2018), "Neural tangent kernel", NeurIPS, arXiv:1806.07572 — 把極寬網路的泛化與核迴歸連結起來。

### 綜述與教科書

- Vapnik，*Statistical Learning Theory*，Wiley（1998）。https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/statistical-learning-theory-978-0-471-03003-4 — VC 理論與結構風險最小化的奠基之作。
- Shalev-Shwartz & Ben-David，*Understanding Machine Learning: From Theory to Algorithms*，Cambridge University Press（2014）。https://doi.org/10.1017/CBO9781107298019 — 易讀的教科書，涵蓋 PAC 學習、VC 維度與演算法。

### 講座與影片

- Yaser Abu-Mostafa，*Learning From Data*，Caltech 線上課程（2012），關於 VC 維度與泛化的講座。https://work.caltech.edu/telecourse — 免費的課程講座，逐步建立泛化界限。

### 文章與文件

- Belkin, Hsu, Ma & Mandal (2019), "Reconciling modern machine-learning practice and the bias–variance trade-off", *PNAS*, arXiv:1812.11118 — 說明雙下降：模型能擬合訓練集之後，測試誤差會再次下降。
- Kaplan et al. (2020), "Scaling laws for neural language models", arXiv:2001.08361 — 以經驗上的冪次定律，把語言模型的損失與模型大小、資料與運算量連結起來。
