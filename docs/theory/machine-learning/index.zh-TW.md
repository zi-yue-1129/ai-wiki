# 機器學習

## 直覺

傳統程式設計：人類撰寫規則；電腦把輸入轉換為輸出。
機器學習：人類提供輸入與輸出的範例；電腦自己找出規則（模型參數）。

形式化地說，給定資料 \( D = \{(x_i, y_i)\} \)，要在假設空間 \( \mathcal{H} \) 中找到 \( f_\theta \)，使期望損失最小：

\[
\theta^* = \arg\min_\theta \; \mathbb{E}_{(x,y)\sim P}\big[L(f_\theta(x), y)\big] \approx \arg\min_\theta \frac{1}{n}\sum_i L(f_\theta(x_i), y_i) + \lambda R(\theta)
\]

關於不同類型的學習訊號，見[學習範式](../paradigms/index.md)。

## 任務類型

| 任務 | 說明 | 例子 | 常用演算法 |
|---|---|---|---|
| 分類 | 預測類別 | 垃圾郵件、腫瘤良性／惡性 | 邏輯迴歸、樹、SVM、神經網路 |
| 迴歸 | 預測數值 | 房價、藥物劑量 | 線性迴歸、梯度提升 |
| 分群 | 找出群組 | 客戶區隔、細胞類型 | k-means、DBSCAN、階層式分群 |
| 降維 | 壓縮特徵 | 視覺化、去雜訊 | PCA、t-SNE、UMAP |
| 異常偵測 | 找出不尋常的樣本 | 詐欺、機器故障 | Isolation Forest、自編碼器 |
| 排序與推薦 | 依偏好排序 | 搜尋、電子商務 | 矩陣分解、雙塔模型 |
| 預測 | 預測未來 | 需求、負載 | ARIMA、梯度提升、RNN、Transformer |

## 經典演算法

- **線性／邏輯迴歸**：可解釋、快速，是許多領域的基準模型。
- **k 近鄰**：記住所有資料，由鄰居投票。
- **決策樹**：一連串的 if–else；可解釋，但容易過擬合。
- **隨機森林**：對許多棵樹進行 bagging。
- **梯度提升樹（XGBoost、LightGBM、CatBoost）**：表格資料的王者。
- **支援向量機**：最大化間隔；核函數處理非線性。
- **單純貝氏**：假設特徵條件獨立；是快速的文字基準模型。
- **PCA**：變異量最大的方向。
- **高斯混合模型與 EM**：軟分群。

!!! tip "表格資料先試樹模型"
    在中小型的表格資料集上，梯度提升樹往往勝過深度學習（Grinsztajn et al., 2022）。TabPFN 等表格基礎模型近來在小資料上表現很強，也值得一試。

## 泛化：核心問題

### 欠擬合與過擬合

- **欠擬合**：模型太簡單；訓練誤差本來就很高。
- **過擬合**：模型記住了雜訊；訓練誤差低，測試誤差高。

### 偏差—變異權衡

\[
\text{期望誤差} = \text{偏差}^2 + \text{變異} + \text{不可約雜訊}
\]

古典觀點：複雜度會降低偏差、提高變異，因此存在一個最佳點。
現代觀點：**雙下降（double descent）**——當模型大到足以完全擬合訓練資料後，測試誤差會再次下降。這有助於解釋為什麼參數遠多於樣本數的深度網路仍能泛化（Belkin et al., 2019；Nakkiran et al., 2019）。

### 正規化

L1（稀疏性）、L2（權重衰減）、早停、資料增強、dropout、集成。

## 實驗方法

1. **切分資料**：訓練集／驗證集／測試集。測試集只在最後使用一次。
2. **交叉驗證**：資料量少時必不可少。
3. **依時間切分時間序列**，絕不讓未來去預測過去。
4. **避免洩漏**：前處理（縮放、特徵選擇）只在訓練資料上 fit；依病人／使用者切分，而不是依列切分。
5. **選擇符合任務的指標**：

| 指標 | 適用時機 |
|---|---|
| 準確率 | 類別平衡 |
| 精確率／召回率／F1 | 類別不平衡（篩檢偏好召回率，垃圾郵件過濾偏好精確率） |
| ROC-AUC、PR-AUC | 與門檻無關的比較；PR-AUC 適用於嚴重不平衡的情況 |
| MAE、RMSE、R² | 迴歸 |
| 校準（ECE） | 機率必須可信時（醫學、金融） |

關於模型如何表達不確定性，以及如何讓其機率與觀察到的頻率相符，見[不確定性量化與校準](uncertainty-and-calibration/index.md)。

關於刻意設計來騙過模型的輸入，以及讓模型在這些輸入下仍保持正確的方法，見[對抗樣本與穩健性](adversarial-robustness/index.md)。

關於來自與訓練資料不同分布的輸入，以及如何偵測它們，見[分布外偵測與分布偏移](ood-detection/index.md)。

## 學習理論簡述

- **PAC 學習**：要以高機率學到一個近似正確的假說，需要多少樣本。
- **VC 維度**：假說類別的容量度量。
- **沒有免費的午餐**：沒有任何演算法在所有問題上都最好；歸納偏誤是必要的。
- **歸納偏誤**：CNN 的平移等變性、RNN 的時序結構、GNN 的排列不變性，都把領域知識內建到模型中。大腦演化出的架構，可以看作一種強大的歸納偏誤（見 [NeuroAI](../../brain-mind/neuroai/index.md)）。

## 與認知科學的連結

- **概念學習**：人類能從少數範例學會新概念；貝氏程式學習（Lake et al., 2015）對此建模。
- **類別化的原型與範例理論**，分別對應類別中心分類器與 kNN 式的記憶。
- **統計學習**：嬰兒利用音節之間的轉移機率來切分詞語（Saffran et al., 1996）——在某些方面有點像語言模型。

## 學習資源

- Microsoft [ML-For-Beginners](https://github.com/microsoft/ML-For-Beginners)（MIT 授權）
- Andrew Ng，*Machine Learning Specialization*（Coursera）
- *The Elements of Statistical Learning*（免費 PDF）
- [scikit-learn 使用者指南](https://scikit-learn.org/stable/user_guide.html)
- 林軒田，《機器學習基石》與《機器學習技法》（台大，中文）

## 參考文獻

### 開創性論文

- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示大型模型可以記住隨機標籤，這削弱了以容量為基礎的簡單泛化解釋。
- Hastie, T., Tibshirani, R. & Friedman, J. *The Elements of Statistical Learning*，第二版。https://hastie.su.domains/ElemStatLearn/ — 監督與非監督方法的標準研究所參考書，附有背後的統計理論。作者提供免費 PDF。

### 講座與影片

- Abu-Mostafa, Y. S. *Learning From Data*. Caltech. https://work.caltech.edu/telecourse — 免費的入門課程，講授從資料中學習的理論與實務，涵蓋 VC 維度、偏差—變異與正規化。

### 文章與文件

- Domingos, P. (2012). A Few Useful Things to Know About Machine Learning. *Communications of the ACM*, 55(10). https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf — 給實務工作者的十二條實用經驗，涵蓋泛化、特徵與過擬合。
- scikit-learn developers. *User Guide*. https://scikit-learn.org/stable/user_guide.html — 標準演算法、模型評估與常見陷阱的實用參考，附有可執行的範例。
