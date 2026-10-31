---
translation_reviewed: 2026-10-31
---

# 隨機平滑

隨機平滑透過有雜訊輸入的預測，定義一個分類器。高斯平滑能為這個**平滑分類器**提供局部 $\ell_2$ 穩健性認證，而非自動保證原始分類器。[^cohen] 本頁是[對抗樣本與穩健性](index.md)的一部分。

## 被認證的是哪個分類器

對基礎分類器 $f$ 與雜訊標準差 $\sigma>0$，定義

$$
g(x)=\arg\max_c \Pr_{\eta}[f(x+\eta)=c],
\qquad \eta\sim\mathcal N(0,\sigma^2 I).
$$

這是以機率定義的理想分類器；有限次含雜訊預測只能估計它。在多類別問題中，機率最高的類別不一定超過一半。嚴格過半是簡化認證程序採用的充分條件，而非 $g$ 的定義。

需要保持不變的，是 $g$ 回傳的標籤。單次含雜訊的 $f$ 評估，或未修改的預測 $f(x)$，都不必保持不變。

## 機率界與半徑

令 $c_A$ 為候選類別。定理需要其機率的**下界** $\underline p_A$，以及每個競爭類別機率的**上界** $\overline p_B$：[^cohen]

$$
\Pr[f(x+\eta)=c_A]\geq\underline p_A
>\overline p_B\geq
\max_{c\neq c_A}\Pr[f(x+\eta)=c].
$$

當界限不在退化端點時，正半徑為

$$
R=\frac{\sigma}{2}
\left(\Phi^{-1}(\underline p_A)-\Phi^{-1}(\overline p_B)\right),
\qquad
g(x+\delta)=c_A\quad\text{for all }\|\delta\|_2<R.
$$

其中 $\Phi$ 是標準常態累積分布函數，$\Phi^{-1}$ 是其反函數；SciPy 以常態分布的百分位數函數提供這項反函數。[^normal]

若對次高類別使用下界，就可能不安全：減去過小的值會高估半徑。同樣地，定理對擾動範數使用**嚴格**不等式，並未一般性地保證邊界上會發生什麼事。

## 以樣本估計認證

Cohen 等人的程序先使用先導樣本選出類別，再用一批新的樣本估計其機率下界。若 $\underline p_A>1/2$，令 $\overline p_B=1-\underline p_A$，便得到[^cohen]

$$
R=\sigma\Phi^{-1}(\underline p_A).
$$

否則，此程序棄答。棄答表示程序沒有回傳認證，並非找到了對抗樣本，也不是不穩健的證明。

實作時應區分以下步驟：

1. 抽取 $n_0$ 個獨立高斯擾動，選出候選類別。
2. 抽取 $n$ 個新的擾動，計算候選類別出現的次數 $k$。
3. 計算該二項機率的單側 $(1-\alpha)$ 信賴下界。
4. 只有當下界超過一半時，才回傳候選類別與正半徑。

觀察比例 $k/n$ 是點估計，不是信賴界。SciPy 文件說明了 Clopper–Pearson 精確二項信賴區間；實作必須使用預期的單側涵蓋率，而非未加說明地使用預設雙側區間。[^binomial]

對固定輸入，只要機率界有效，定理就是確定性的。取樣程序在其假設下，回傳無效認證的機率至多為 $\alpha$。[^cohen] 這不表示球內只有 $1-\alpha$ 比例的擾動受到保護；$\alpha$ 也不是類別標籤正確的機率。反覆呼叫認證程序，並不會自動得到涵蓋所有受測輸入的同時保證。

## 半徑計算範例

取 $\sigma=0.25$，並假設下列數值是有效下界，而非原始投票比例：

| $\underline p_A$ | $\Phi^{-1}(\underline p_A)$，約略值 | 半徑 | 簡化程序 |
|---|---|---|---|
| 0.60 | 0.2533 | 0.0633 | 認證 |
| 0.90 | 1.2816 | 0.3204 | 認證 |
| 0.50 | 0 | 無正半徑 | 棄答 |

這些是直接計算，而非基準測量。較大的下界，會讓所有競爭類別合計可占用的機率更少。

即使有限次取樣全數同意，也不應視為機率等於一。當 $n$ 次試驗全數成功，精確單側下界滿足

$$
\underline p_A=\alpha^{1/n}.
$$

例如 $n=100$、$\alpha=0.001$ 時，$\underline p_A\approx0.9333$；在 $\sigma=0.25$ 下，$R\approx0.3751$。此下界來自解 $p^n=\alpha$：即使真實機率小於一，仍可能全數同意。直接代入點估計一，會錯誤地暗示無限大的半徑。

## 論文結果與相關發展

Cohen 等人的表 1 報告：在半徑 0.5、$\sigma=0.25$ 下，ImageNet 的**近似認證準確率為 49%**。[^cohen] 認證準確率計入預測正確、且回傳半徑足夠的樣本，而非只在已接受樣本中計算獲認證比例。這是限定於該評估設定的歷史結果。

Salman 等人（2019）研究了針對平滑分類器設計的對抗訓練。[^adversarial] Salman 等人（2020）則在預訓練分類器前加上已訓練的去噪器，再進行平滑。[^denoised] 去噪器成為基礎映射的一部分；分類器權重固定，並不代表整套程序不需要訓練。

## 適用範圍與評估

認證確立的是局部標籤穩定性，而非正確性、語意相似性，或對所有攻擊類型的穩健性。$\ell_2$ 球並不直接認證旋轉、貼片、任意分布偏移或文字的離散編輯。

應記錄輸入座標系統、正規化方式、完整的基礎映射、雜訊分布與 $\sigma$。前處理可以納入 $f$，但改變雜訊分布時，需要相應的定理。正規化座標中的半徑，不應未加說明地當作原始像素座標中的半徑。

也應報告 $n_0$、$n$、$\alpha$、信賴界方法、棄答率、準確率與執行時間。必須清楚交代雜訊樣本的獨立性與類別選擇方式。比較訓練方法時，應使用相同取樣預算，並說明執行時間包含認證，還是只有預測。

提高 $\sigma$ 會改變 $f$ 收到的資料分布，因此半徑公式中的乘數變大，不代表一定能得到更大且有用的認證；機率界與分類表現都必須重新評估。

[^cohen]: Cohen、Rosenfeld 與 Kolter（2019），定理 1、第 3.2.2 節、命題 2 與表 1；詳見參考文獻。
[^normal]: SciPy 的常態分布累積分布函數與百分位數函數；詳見參考文獻。
[^binomial]: SciPy 的精確二項比例信賴區間；詳見參考文獻。
[^adversarial]: Salman et al.（2019），摘要；詳見參考文獻。
[^denoised]: Salman et al.（2020），摘要；詳見參考文獻。

## 參考文獻

- Cohen, J., Rosenfeld, E. & Kolter, J. Z. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. ICML, PMLR 97:1310–1320. https://proceedings.mlr.press/v97/cohen19c.html — 建立高斯平滑認證，以及可控制失敗機率的取樣程序。
- Salman, H. et al. (2019). *Provably Robust Deep Learning via Adversarially Trained Smoothed Classifiers*. NeurIPS. https://arxiv.org/abs/1906.04584 — 研究用於提高平滑分類器認證穩健性的對抗訓練。
- Salman, H., Sun, M., Yang, G., Kapoor, A. & Kolter, J. Z. (2020). *Denoised Smoothing: A Provable Defense for Pretrained Classifiers*. https://arxiv.org/abs/2003.01908 — 在預訓練分類器前使用已訓練的去噪器，形成平滑所用的基礎映射。
- SciPy contributors. *BinomTestResult.proportion_ci*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html — 說明二項比例的 Clopper–Pearson 精確信賴區間及其他區間方法。
- SciPy contributors. *scipy.stats.norm*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html — 指定標準常態分布函數，包括計算半徑所用的反累積分布函數。
