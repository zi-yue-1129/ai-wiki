# 非監督式學習

## 概念

在**沒有標籤**的情況下找出資料結構：群組、低維因子、密度、異常。LeCun 的蛋糕比喻：如果智慧是一塊蛋糕，非監督（自監督）學習是蛋糕本體，監督學習是糖霜，強化學習是上面的櫻桃。

## 主要家族

| 目標 | 方法 | 用途 |
|---|---|---|
| 分群 | k-means、高斯混合（EM）、階層式分群、DBSCAN/HDBSCAN、譜分群、圖上的 Leiden/Louvain | 客群區隔、單細胞 RNA 定序的細胞類型、主題探索 |
| 降維 | PCA、ICA、NMF、因素分析、t-SNE、UMAP、自編碼器 | 視覺化、壓縮、去噪 |
| 密度估計 | 核密度、混合模型、正規化流、自迴歸模型、擴散模型 | 異常偵測、生成、概似 |
| 異常偵測 | Isolation Forest、one-class SVM、LOF、重建誤差 | 詐欺、設備故障、入侵偵測 |
| 關聯規則 | Apriori、FP-growth | 購物籃分析 |
| 表徵／流形學習 | Isomap、LLE、自編碼器、[自監督](../self-supervised/index.md)方法 | 下游任務特徵 |
| 主題模型 | LDA、BERTopic | 文件集合 |

## 關鍵概念

- **k-means** 最小化群內平方距離；對初始化敏感，假設群大致呈球形
- **PCA** 找出變異最大的正交方向，等價於最佳的低秩線性重建
- **ICA** 找出統計獨立的來源——「雞尾酒會」問題；常用來去除 EEG 中的眨眼雜訊
- **t-SNE／UMAP** 保留局部鄰近關係供視覺化；群與群之間的距離和群的大小**沒有**意義
- **自編碼器** 透過瓶頸壓縮再重建；各種變體（去噪、稀疏、變分）塑造表徵

## 沒有標籤時如何評估

- 內部指標：輪廓係數、Davies–Bouldin、重建誤差、保留資料的概似
- 穩定性：重抽樣後群是否仍存在？
- 下游有用性：特徵是否幫助任務？
- 專家檢視：分群在領域上是否合理？

## 大腦中的非監督學習

- 加上正規化的 **Hebb 學習**（Oja 規則）等於做 PCA——單一神經元就能學到第一主成分
- 自然影像的**稀疏編碼**得到類似 V1 的感受野（Olshausen & Field, 1996）；自然聲音的 ICA 得到類似聽神經的濾波器（Lewicki, 2002）
- **競爭學習與自組織映射**（Kohonen）模擬方向圖、音調拓撲等地形圖
- **統計學習**：嬰兒在幾分鐘內就能從未標註的語音流中萃取結構（Saffran, Aslin & Newport, 1996）
- **神經科學大量使用非監督 ML**：脈衝分類、細胞類型分群、用 PCA/UMAP 找神經流形、行為片段探索（MoSeq）

## 延伸閱讀

- Bishop，《Pattern Recognition and Machine Learning》第 9、12 章。https://www.microsoft.com/en-us/research/?p=231646
- [scikit-learn 非監督學習指南](https://scikit-learn.org/stable/unsupervised_learning.html)
- McInnes et al. (2018) UMAP 論文。https://arxiv.org/abs/1802.03426
- Wattenberg et al.，〈How to Use t-SNE Effectively〉（Distill, 2016）。https://distill.pub/2016/misread-tsne/
