---
translation_reviewed: 2026-10-28
---

# AI 所需的機率與統計

機率是 AI 處理不確定性的語言，統計則是在這種不確定性下從資料學習的方法。本頁說明兩個領域中 AI 最常用的部分：隨機變數、常見分布、貝氏定理、估計量，以及損失函數的統計觀點。它是[數學基礎概述](../index.md)所涵蓋的領域之一。

## 概述

隨機變數 \(X\) 依機率分布 \(p(x)\) 取值。分類器輸出標籤上的分布，語言模型輸出下一個詞元上的分布，回歸模型則可以輸出平均值與變異數。統計問的則是反向的問題：給定觀測資料 \(D\)，哪一組分布或參數最能解釋它，我們又能有多確定？

這門學科有兩種觀點貫穿其中。頻率學派把參數視為固定但未知的數字，並探討估計量在重複抽樣下的表現。貝氏學派把參數視為具有先驗分布的隨機變數，並以資料更新先驗。現代 AI 兩者都用：最大概似是訓練的主要工具，貝氏推理則支配不確定性與正規化。

## 關鍵概念

- **期望值與變異數**：\(\mathbb{E}[X] = \sum_x x\,p(x)\) 與 \(\operatorname{Var}[X] = \mathbb{E}[(X-\mathbb{E}X)^2]\)。訓練所要最小化的，正是期望損失。
- **常見分布**：二元結果用白努利分布，\(K\) 類之一用類別分布，實值雜訊用高斯分布，計數用卜瓦松分布。
- **條件機率與獨立性**：\(p(x\mid y) = p(x,y)/p(y)\)。條件獨立使圖模型變得可以處理。
- **貝氏定理**：\(p(\theta\mid D) = \dfrac{p(D\mid\theta)\,p(\theta)}{p(D)}\)，結合先驗與概似得到後驗。
- **估計量**：把資料轉換為參數估計值的規則。其偏差與變異數描述典型誤差。
- **大數法則與中央極限定理**：樣本平均收斂到期望值，樣本夠大時其波動近似高斯分布。這些結果支撐蒙地卡羅估計與信賴區間。

## 運作方式

統計觀點能解釋實務中大多數的損失函數。最大化模型的概似，等同於最小化負對數概似，常見的損失函數都是其特例：

- 分類用的交叉熵損失，是類別分布的負對數概似。
- 均方誤差在變異數固定時，相當於高斯分布的負對數概似（相差常數）。
- 計算 MAP 估計時，L2 權重正規化相當於對權重取高斯先驗。

估計有兩條標準途徑。[最大概似估計](maximum-likelihood.md)選出使觀測資料機率最大的參數。[最大後驗估計](maximum-a-posteriori.md)在概似上加上對數先驗，使先驗扮演正規化的角色。完整的貝氏推理保留整個後驗分布，但通常無法精確計算，因此以[變分推論](../../paradigms/probabilistic/variational-inference/index.md)或[馬可夫鏈蒙地卡羅](../../paradigms/probabilistic/mcmc/index.md)近似。

## 主要方法

這個領域的兩種估計量是代表性的方法，各自有獨立的頁面。

- [最大概似估計](maximum-likelihood.md)：選出使資料機率最大的參數，幾乎用於訓練所有參數模型。
- [最大後驗估計](maximum-a-posteriori.md)：在概似上加上先驗。先驗為平坦時等於最大概似；高斯先驗等常見先驗則會轉化為正規化項。

## 與其他頁面的連結

- [機率與貝氏方法](../../paradigms/probabilistic/index.md)在本頁基礎上延伸到圖模型、推論與貝氏深度學習。
- [資訊理論](../../information-theory/index.md)定義熵與 KL 散度，它們正是交叉熵損失背後的期望值。
- [線性代數](../linear-algebra/index.md)提供多元高斯分布的共變異數矩陣及其特徵值分解。
- 腦與認知：貝氏大腦假說主張神經系統表示不確定性，並把先前期望與感官證據結合。此假說仍有爭議，詳見[機率與貝氏方法頁面](../../paradigms/probabilistic/index.md)。

## 應用

- **訓練**：分類器與語言模型以最大概似訓練，交叉熵即負對數概似（Bishop, 2006）。
- **不確定性**：貝氏模型給出可信區間與後驗預測分布（Gelman et al., 2013）。
- **評估**：比較模型在基準測試上的準確率時，使用信賴區間與顯著性檢定。這些工具已是標準做法，本頁參考文獻中的教科書有完整說明。
- **科學實驗設計**：同樣的估計與檢定方法，也是神經科學與心理學實證研究的基礎。

## 開放問題

- 校準問題：模型宣稱的機率常與觀察到的頻率不一致，大型神經網路尤其明顯。參見[不確定性量化與校準](../../paradigms/probabilistic/index.md)。
- 先驗選擇：對某個問題合理的先驗，可能扭曲另一個問題的結果。大型模型該如何選擇先驗尚無定論。
- 基準測試的統計檢定：許多模型之間報告的差異，小於不同訓練執行之間的變異，目前也缺乏可靠的報告方式。

## 參考文獻

### 奠基性論文

- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A* 222, 309–368. https://doi.org/10.1098/rsta.1922.0009 — 提出最大概似估計，並定義一致性、效率與充分性等概念。論文副本取自阿德雷德大學的典藏庫。
- 對 Fisher (1922) 的評論：*From evidence to understanding*，PubMed Central。https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — 同儕審查的評論，說明該論文的內容與影響，包括其對概似的處理。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 免費 PDF。說明最大概似如何在高斯雜訊下得到最小平方法，在分類中得到交叉熵。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費線上教科書，機率、估計與貝氏推理以機器學習讀者為對象撰寫。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 應用貝氏統計的標準教科書；作者網站提供本書與相關資料。
