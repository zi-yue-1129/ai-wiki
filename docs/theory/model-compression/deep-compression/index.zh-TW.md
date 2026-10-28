---
translation_reviewed: 2026-10-28
---

# 深度壓縮

深度壓縮是一條三階段的流程，結合剪枝、碼本量化與霍夫曼編碼，以縮減已訓練網路的儲存空間。Han、Mao 與 Dally（2016）為嵌入式部署提出此方法，因為單一技術無法把網路縮到硬體能容納的大小。它是[組合式壓縮](../index.zh-TW.md)的一個清楚例子：每個階段移除不同類型的冗餘，且依序套用。各階段本身分別在[剪枝](../pruning/index.zh-TW.md)與[量化](../quantisation/index.zh-TW.md)頁面中說明。

## 問題

已訓練的網路可能太大，無法儲存在嵌入式裝置上；而單獨使用剪枝或單獨使用量化等常用技術，若不接受明顯的準確度損失，又無法達到所需的大小。這裡的限制是儲存空間，因此目標是表示網路所需的位元數，而非執行速度。

## 核心想法

依序套用三個階段。第一，剪除數值較小的連線，接著重新訓練保留下來的權重以恢復準確度。第二，把倖存的權重群聚成少數共享的數值，即碼本，並把每個權重儲存為碼本中的索引。第三，對索引做霍夫曼編碼，讓常見的索引使用較少的位元。每個階段移除不同的冗餘：零值、相異數值的數量，以及剩餘數值出現頻率的不均。

## 公式或演算法

剪枝階段在權重 \(w\) 的絕對值超過門檻 \(|w| > t\) 時保留它，其餘設為零。之後的重新訓練只更新保留下來的連線。

量化階段通常以 k-means 把倖存的權重群聚成 \(k\) 個質心。每個權重被替換為最近質心的索引 \(c_i\)，因此一層 \(n\) 個權重需要 \(n \log_2 k\) 位元存放索引，外加一張小的質心表。接著以共享同一質心的權重所平均的梯度，微調這些質心。

最後階段對索引做霍夫曼編碼。其期望碼長接近索引分布的熵；當某些質心的使用頻率遠高於其他質心時，這個熵低於 \(\log_2 k\)。

## 結果

Han 等人（2016）報告，此流程可把神經網路的儲存需求減少 35 至 49 倍，且不影響準確度。在他們的設定中，減少的是儲存大小而非執行速度，而這些數字只適用於他們所研究的網路與資料集。

## 限制

收益主要在儲存空間。稀疏與基於碼本的模型，需要特殊的硬體或軟體才能跑得更快；密集的加速器可能無法從零值中獲得多少加速。此流程在每次剪枝與量化後還需要重新訓練，對非常大的模型而言成本很高；而當模型已經夠緊湊時，後面的階段就較不實用。

## 開放問題與相關變體

- **速度與大小。** 檔案較小並不代表模型較快。零值與共享數值能否在執行時被利用，取決於模型部署的硬體，見[總覽](../index.zh-TW.md)的說明。
- **訓練後的版本。** 對大型模型而言，重新訓練是成本最高的部分。之後的一次性方法，例如[大型語言模型一次剪枝](../pruning/one-shot-llm-pruning/index.zh-TW.md)系列中的方法，可以避免大部分的重新訓練。
- **相關：** 碼本步驟是向量量化的一種形式，Gong 等人（2014）把它套用在 CNN 的密集層上。

## 相關連結

深度壓縮把[模型壓縮](../index.zh-TW.md)總覽中最大的兩個家族連在一起，即[剪枝](../pruning/index.zh-TW.md)與[量化](../quantisation/index.zh-TW.md)。它的儲存格式與[裝置端與邊緣 AI](../../../engineering/on-device-edge/index.zh-TW.md)最相關，因為模型大小在那裡限制了部署。

## 參考文獻

### 開創性論文

- Han, S., Mao, H., Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR. https://arxiv.org/abs/1510.00149 — 結合剪枝、碼本量化與霍夫曼編碼，報告在不影響準確度下減少 35 至 49 倍的儲存空間。
- Han, S., 等人 (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 剪除連線並重新訓練保留的權重，在不損失準確度的情況下縮小 AlexNet 與 VGG-16。
- Gong, Y., 等人 (2014). *Compressing Deep Convolutional Networks using Vector Quantization*. arXiv:1412.6115. https://arxiv.org/abs/1412.6115 — 顯示對密集層做向量量化，比矩陣分解更有效地壓縮大型 CNN。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 涵蓋訓練與推論的稀疏方法的廣泛綜述。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 顯示在大型任務上，簡單的量值剪枝與較複雜的稀疏方法表現相當或更好。
