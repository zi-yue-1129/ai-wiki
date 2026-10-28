---
translation_reviewed: 2026-10-28
---

# 權重初始化與信號傳播

權重初始化決定訓練開始前網路參數的起始數值。由於深度網路會讓訊號在許多層之間逐層相乘，這些起始數值的尺度，決定了激活值與梯度會縮小到接近零、無限制地增長，或是保持在可用的大小。研究訊號在網路起始狀態下如何傳遞的領域，稱為信號傳播。

## 概述

訓練從隨機數值開始。在最初幾步，網路的行為幾乎完全由這些數值決定，而最佳化器所使用的梯度也是由它們算出來的。如果權重太小，激活值會逐層縮小，訊號在到達輸出之前就衰退了。如果權重太大，激活值會不斷增長，單元會飽和。兩種情況下，反向傳播的梯度都會有不良的尺度，學習因此變慢或停滯。Glorot 與 Bengio（2010）針對深層 sigmoid 與 tanh 網路、從樸素的隨機起點開始訓練時展示了這個現象，並指出尺度的選擇會改變收斂的速度。

初始化的重要性不只在最初幾步。起始尺度有助於決定一個普通網路能有多深並仍可被訓練，也決定了在小模型上有效的設定，在大模型上是否依然有效。第二個問題促成了超參數遷移方法的出現，下文會在 muP 的段落中討論。

後來的設計，例如殘差連接與正規化層，降低了對起始尺度的敏感度，但並未完全消除這個問題。

## 關鍵概念

- **扇入與扇出。** 一層的輸入數 \(n_{\text{in}}\) 與輸出數 \(n_{\text{out}}\)。大多數初始化規則會用其中一個數字來設定權重的變異數。
- **變異數傳播。** 激活值的變異數，以及梯度的變異數，在每一層都會乘上一個大致固定的因子。
- **增益。** 一層連同其非線性函數，把訊號的變異數放大的倍數。增益為一時，尺度能夠保持不變。
- **飽和。** 單元的輸入大到使其激活幾乎是平的，因此梯度接近零的狀態。Sigmoid 與 tanh 單元會飽和；整流單元在正輸入時不會飽和。
- **混沌邊緣。** 兩種訊號傳播狀態之間的邊界：一種是有序狀態，不同輸入隨深度而變得更相似；另一種是混沌狀態，相近的輸入會被推開。可訓練性通常在這個邊界附近最好。
- **動力等距。** 網路輸入—輸出雅可比矩陣的所有奇異值都接近一的條件。

## 運作方式

考慮一個有 \(n\) 個輸入的線性層，其激活值的變異數為 \(\mathrm{Var}[x]\)，且權重彼此獨立、平均為零、變異數為 \(\mathrm{Var}[w]\)。則輸出 \(y = \sum_j w_j x_j\) 滿足

\[
\mathrm{Var}[y] = n\,\mathrm{Var}[w]\,\mathrm{Var}[x].
\]

因子 \(n\,\mathrm{Var}[w]\) 就是前向增益。經過 \(L\) 層大致呈線性的運作後，激活值的變異數會乘上這些增益的乘積。梯度的推導相同，但使用輸出數而非輸入數。依每層的增益不同，訊號會隨深度指數式縮小、指數式增長，或大小大致保持不變。

Glorot 與 Bengio（2010）只有在所有層寬度相同時，才能同時滿足前向與反向條件，因此他們採用 \(\mathrm{Var}[w] = 2/(n_{\text{in}} + n_{\text{out}})\)。He 等人（2015）注意到，整流單元會把負的輸入歸零，因此會去掉二階矩的約一半。整流層的前向增益因此是 \(\tfrac{1}{2} n\,\mathrm{Var}[w]\)，對應的選擇是 \(\mathrm{Var}[w] = 2/n_{\text{in}}\)。細節見 [Xavier／Glorot](glorot-xavier/index.md) 與 [He 初始化](he-initialisation/index.md) 兩頁。

### 深度、混沌與混沌邊緣

每層增益的推論是線性的。對於權重隨機的非線性網路，平均場理論追蹤兩個輸入之間的相似度如何隨深度改變。在有序相，不同輸入會變得更相似；在混沌相，相近的輸入會被推開。Poole 等人（2016）把這描述為有序—混沌的表達能力轉變，在混沌網路中，所計算函數的曲率會隨深度呈指數成長。Schoenholz 等人（2017）定義了會限制訊號傳遞距離的深度尺度，並主張只有當資訊能在網路中傳遞時，網路才能被訓練。在混沌邊緣附近，其中一個深度尺度會發散，因此只要設定在這個邊界附近，非常深的網路也可以被訓練。

Pennington 等人（2017）發現，整流網路無法達到動力等距，而 sigmoid 網路可以，但前提是權重為正交的。

### 為何殘差連接與正規化有所幫助

殘差區塊計算 \(x + F(x)\)。它的恆等路徑在傳遞訊號時不做乘法，因此即使 \(F\) 的貢獻很小，區塊的增益仍接近一。He 等人（2016）證明，有了恆等跳接，前向與反向訊號可以從任一區塊直接傳遞到任何其他區塊。

正規化的作用方式不同。De 與 Smith（2020）指出，在初始化時，批次正規化會把殘差分支相對於跳接路徑縮小，縮小的倍數大約是深度的平方根，因此訓練初期每個區塊都接近恆等映射。Zhang 等人（2019）以重新縮放初始化的方式（Fixup），在不使用正規化的情況下達到類似的效果，並以一萬層的殘差網路訓練得與有正規化的網路一樣穩定。Brock 等人（2021）結合訊號傳播工具與權重標準化，設計出不含正規化的殘差網路，在 ImageNet 上可與 EfficientNet 相比。正規化器本身的介紹見[正規化層](../normalisation/index.md)頁面。

## 關鍵方法

每個方法各有專頁。此處的比較從簡。

| 方法 | 年份 | 核心想法 | 專頁 |
|---|---|---|---|
| Xavier（Glorot）初始化 | 2010 | 變異數為 \(2/(n_{\text{in}}+n_{\text{out}})\)，使近似線性的層中前向與反向訊號保持相近的尺度 | [Xavier／Glorot](glorot-xavier/index.md) |
| He 初始化 | 2015 | 變異數為 \(2/n_{\text{in}}\)，補償整流單元所移除的一半訊號 | [He 初始化](he-initialisation/index.md) |
| 最大更新參數化（muP） | 2021 | 隨寬度縮放初始化與學習率，使特徵以相近的速度學習，並讓設定可以遷移 | [muP](mup/index.md) |

Xavier 與 He 是針對單一網路在起始狀態的規則。muP 則規定網路變寬時，起始尺度與學習率應如何改變。

## 與其他主題的關聯

初始化與訓練的其他部分密切相關。[漸進式預熱](../../optimization/gradual-warm-up.md)頁面所述的學習率預熱，常被解釋為對抗不良起點所產生的不可靠早期梯度。[殘差網路](../../models/cnn/backbones-and-scaling/resnet/index.md)與 [Transformer](../../models/transformer/index.md)頁面說明了恆等路徑與正規化位置在實務中如何使用。

大腦與心智的角度位於動力學層面，而非訓練層面。Van Vreeswijk 與 Sompolinsky（1996）指出，由興奮性與抑制性神經元組成的網路，若其輸入大致互相抵消，即使在恆定輸入下也會產生強烈的混沌活動。這與 Sompolinsky、Crisanti 與 Sommers（1988）早期對隨機網路的分析屬於同一類研究。這顯示神經迴路可以處於混沌狀態而不致失控，但並不表示大腦皮質經過調校而位於混沌邊緣。生物迴路也並非由彼此獨立的隨機數抽取而成：其初始連接受發育過程塑造，見[發展認知](../../../brain-mind/developmental-cognition/index.md)頁面的描述。

## 應用

- **訓練深層網路。** Glorot 與 He 方案是標準的選項，而整流網路通常選用 He 初始化。
- **不含正規化的網路。** Fixup 與 Brock 等人（2021）的設計顯示，謹慎的初始化可以取代殘差網路中的正規化層。
- **調校超大型模型。** muP 讓人可以在小模型上進行搜尋，再把最佳設定用於大得多的模型。證據見 [muP](mup/index.md) 頁面。

## 開放問題

- **起始分析能否預測訓練後的網路？** 大部分理論描述的是初始化時的網路，而訓練會使權重遠離那個起點。混沌邊緣與等距條件在訓練後能保留多少，尚無定論。
- **無限寬極限能否描述真實網路？** muP 規則與非常寬的網路的核極限，都是在寬度趨於無限時推導的。Yang 與 Hu（2021）指出，標準參數化與 NTK 參數化不存在能讓特徵學習的極限。這些極限對實際網路的描述有多好，仍是活躍的研究問題。
- **正規化為何有所幫助？** De 與 Smith（2020）提出的初始時恆等觀點，能解釋殘差網路中批次正規化的部分益處。它是否也能解釋其餘部分，仍有爭論。
- **生物學。** 神經系統是否以類似的機制，把增益調整到臨界狀態，目前尚不清楚。

## 參考文獻

### 開創性論文

- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — 提出變異數為 \(2/(n_i+n_{i+1})\) 的標準化初始化，依據是讓激活值與梯度的變異數保持恆定。
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — 針對整流單元修正 Xavier 的推導，並顯示 30 層網路在 Xavier 停滯的情況下，可用新方案訓練。
- Sompolinsky, H., Crisanti, A. & Sommers, H. J. (1988). *Chaos in Random Neural Networks*. Physical Review Letters. https://doi.org/10.1103/PhysRevLett.61.259 — 針對隨機循環網路的早期分析，確定了有序動力學與混沌動力學之間的轉變。
- Poole, B., Lahiri, S., Raghu, M., Sohl-Dickstein, J. & Ganguli, S. (2016). *Exponential expressivity in deep neural networks through transient chaos*. arXiv. https://arxiv.org/abs/1606.05340 — 對隨機深度網路的平均場分析，確定了有序到混沌的表達能力轉變。
- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — 定義限制隨機網路可訓練性的深度尺度，並主張可訓練性在混沌邊緣附近最好。
- van Vreeswijk, C. & Sompolinsky, H. (1996). *Chaos in Neuronal Networks with Balanced Excitatory and Inhibitory Activity*. Science. https://doi.org/10.1126/science.274.5293.1724 — 顯示神經元網路模型中，興奮與抑制達到平衡時會產生強烈的混沌活動。
- Yang, G. & Hu, E. J. (2021). *Feature Learning in Infinite-Width Neural Networks*. arXiv. https://arxiv.org/abs/2011.14522 — 顯示標準與 NTK 參數化沒有能讓特徵學習的無限寬極限，並提出最大更新參數化。
- Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Liu, X., Farhi, D. et al. (2022). *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*. arXiv. https://arxiv.org/abs/2203.03466 — 提出 muTransfer，在小模型上調整超參數，再將其遷移到大型 Transformer 與 ResNet。

### 文章與文件

- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — 計算雅可比奇異值的分布，並顯示哪些激活函數與初始化能達到動力等距。
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Identity Mappings in Deep Residual Networks*. arXiv. https://arxiv.org/abs/1603.05027 — 分析恆等跳接如何讓前向與反向訊號抵達任一區塊，並提出讓訓練更容易的殘差單元。
- De, S. & Smith, S. L. (2020). *Batch Normalization Biases Residual Blocks Towards the Identity Function in Deep Networks*. arXiv. https://arxiv.org/abs/2002.10444 — 顯示批次正規化在初始化時會縮小殘差分支，使深層殘差區塊接近恆等映射。
- Zhang, H., Dauphin, Y. N. & Ma, T. (2019). *Fixup Initialization: Residual Learning Without Normalization*. arXiv. https://arxiv.org/abs/1901.09321 — 重新縮放標準初始化，使殘差網路在不使用正規化層的情況下也能訓練，包括一萬層的網路。
- Brock, A., De, S. & Smith, S. L. (2021). *Characterizing signal propagation to close the performance gap in unnormalized ResNets*. arXiv. https://arxiv.org/abs/2101.08692 — 以訊號傳播工具搭配權重標準化，設計出不含正規化的 ResNet，其表現可與 EfficientNet 相比。
