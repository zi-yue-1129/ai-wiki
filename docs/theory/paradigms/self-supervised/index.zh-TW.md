# 自監督學習

## 概念

**從未標註資料本身**製造出看似監督的任務：把輸入的一部分遮起來再預測，或讓同一事物的兩個視角一致。模型必須學到有用的表徵才能解決這個前置任務。自監督是基礎模型得以存在的原因：資料自己標註自己時，「標註資料」的數量沒有上限。

## 家族

| 家族 | 前置任務 | 例子 |
|---|---|---|
| 自迴歸預測 | 預測下一個 token／像素／音訊樣本 | GPT、PixelCNN、WaveNet、音訊語言模型 |
| 遮罩建模 | 重建被遮住的部分 | BERT（文字）、MAE 與 BEiT（影像）、wav2vec 2.0／HuBERT（語音）、遮罩蛋白質模型（ESM） |
| 對比學習 | 拉近同一物件的不同視角、推開其他（InfoNCE 損失） | SimCLR、MoCo、CPC、CLIP（圖文） |
| 非對比聯合嵌入 | 不用負樣本也讓視角一致，以不對稱或正規化避免崩塌 | BYOL、SimSiam、Barlow Twins、VICReg、DINO |
| 聯合嵌入預測架構 | 預測被遮住部分的**表徵**而非像素 | I-JEPA、V-JEPA |
| 去噪 | 去除加入的雜訊 | 去噪自編碼器、擴散模型 |
| 早期拼圖任務 | 旋轉預測、拼圖、上色 | 2016–2018 年的視覺論文 |

### InfoNCE（對比）損失

對於錨點 \(z_i\)、正樣本 \(z_i^+\)、負樣本 \(z_j\)，相似度 \(s\)、溫度 \(\tau\)：

\[
L = -\log \frac{\exp(s(z_i, z_i^+)/\tau)}{\sum_j \exp(s(z_i, z_j)/\tau)}
\]

最小化它等於最大化兩個視角之間互資訊的下界。

## 為什麼有效

- 前置任務迫使模型捕捉規律（語法、語意、物體形狀、物理），這些對下游任務也有用
- 規模：數十億個免費樣本
- 資料增強編碼了我們想要的**不變性**（裁切、顏色擾動 → 物體身份重要，精確像素不重要）

## 風險

- 聯合嵌入方法的**表徵崩塌**（全部映射到同一點），以負樣本、stop-gradient、變異數／共變異數正規化避免
- 從增強方式或資料瑕疵學到**捷徑**
- **資料品質與偏見**會從網路規模語料中全盤繼承

## 大腦是自監督學習者

- **預測編碼／預測處理**（Rao & Ballard, 1999；Friston）：皮質不斷預測感官輸入並從預測誤差中學習——本質上就是自監督學習。見 [認知科學](../../../brain-mind/cognitive-science/index.md)
- **時間對比**：緩慢性／時間一致性原則（slow feature analysis）會產生類似複雜細胞與位置細胞的表徵
- **自監督模型和監督模型一樣能吻合腹側視覺流**（Zhuang et al., 2021, *PNAS*）——這很重要，因為靈長類並沒有收到數百萬個標籤
- **語言**：下一個字預測模型能預測人類語言區的活動（Schrimpf et al., 2021）；大腦可能在多個時間尺度上預測即將到來的字（Caucheteux et al., 2023）

## 延伸閱讀

- Balestriero et al. (2023), "A Cookbook of Self-Supervised Learning"
- LeCun & Misra〈Self-supervised learning: the dark matter of intelligence〉（Meta AI 部落格, 2021）
- Chen et al. (2020) SimCLR；He et al. (2022) MAE；Radford et al. (2021) CLIP
