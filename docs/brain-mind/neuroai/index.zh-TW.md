# NeuroAI：大腦與 AI 的雙向啟發

**NeuroAI** 是神經科學與 AI 之間的雙向交流：用大腦啟發更好的 AI，也用 AI 模型理解大腦。Zador et al.（2023, *Nature Communications*）〈Catalyzing next-generation AI through NeuroAI〉提出「具身圖靈測試」——讓 AI 達到動物的感覺運動能力——作為這個領域的大挑戰。

## 方向一：深度網路作為大腦模型

### 任務最佳化建模範式

1. 訓練網路完成動物也會做的任務（物體辨識、預測下一個字、導航）
2. 記錄大腦對相同刺激的神經反應
3. 從模型特徵到神經反應擬合線性映射，測量對保留資料的預測能力
4. 比較不同架構、目標與訓練資料

| 系統 | 關鍵發現 |
|---|---|
| 腹側視覺流 | 以表現最佳化的 CNN 比過去的模型更能預測 V4 與 IT 反應；層的深度對應皮質階層（Yamins et al., 2014；Khaligh-Razavi & Kriegeskorte, 2014） |
| 聽覺皮質 | 以語音／音樂訓練的網路能預測聽覺皮質，且呈現類似皮質的階層（Kell et al., 2018） |
| 語言網路 | 下一字預測的 LLM 能預測語言網路的 fMRI/ECoG 反應；下一字預測越好，大腦預測越好（Schrimpf et al., 2021） |
| 運動皮質 | 訓練產生伸手動作的 RNN 出現與猴子運動皮質類似的旋轉動態（Sussillo et al., 2015） |
| 海馬迴—內嗅系統 | 以路徑整合訓練的網路出現類網格單元（Banino et al., 2018；Cueva & Wei, 2018）——但結果有多依賴設計選擇仍有爭議（Schaeffer et al., 2022） |
| 多巴胺 | TD 學習與分布式 RL 解釋多巴胺反應 |

**基準**：[Brain-Score](https://www.brain-score.org/) 依模型與靈長類視覺、人類語言資料的相似度排名；Algonauts 挑戰與 Natural Scenes Dataset（NSD）提供大規模 fMRI 基準。

**比較表徵的方法**：線性編碼模型、表徵相似度分析（RSA）、中心化核對齊（CKA）、Procrustes／形狀度量。

### 注意事項

- **可預測不等於機制**：許多不同模型對神經資料的預測一樣好；高分可能來自通用特徵
- **行為差異**：網路易受對抗樣本影響、比人類更依賴紋理（Bowers et al., 2023〈Deep problems with neural network models of human vision〉）
- **生物不合理性**：反向傳播、權重共享、海量標註資料都沒有明顯的生物對應——[自監督](../../foundations/paradigms/self-supervised/index.md)模型能和監督模型一樣吻合腹側視覺流（Zhuang et al., 2021），部分回應了這點

## 方向二：大腦啟發 AI

| 大腦原理 | AI 想法 |
|---|---|
| 階層式感受野 | CNN |
| 多巴胺預測誤差、動物學習 | 強化學習 |
| 海馬迴重播 | 經驗重播（DQN）、生成式重播 |
| 互補學習系統 | 持續學習方法；檢索增強模型 |
| 突觸鞏固 | 彈性權重鞏固 |
| 注意力與閘控 | 注意力機制、混合專家路由（鬆散的類比） |
| 脈衝與事件驅動處理 | 脈衝神經網路、神經形態晶片 |
| 樹突運算 | 樹突神經元模型、用於多任務學習的主動樹突網路 |
| 神經調節 | 學習率的元學習、依情境閘控 |
| 預測編碼 | 自監督預測目標、JEPA |
| 網格細胞與認知地圖 | 用於導航與抽象推理的結構化表徵 |
| 稀疏、節能的編碼 | 稀疏性、啟動稀疏、MoE |
| 演化帶來的先天結構 | 歸納偏誤、元學習、「基因組瓶頸」模型 |

經典綜述：Hassabis et al.（2017, *Neuron*）〈Neuroscience-inspired artificial intelligence〉。

## 信用分配問題：大腦如何學習？

深度學習依賴**反向傳播**，它需要：

1. 對稱的回饋權重（「權重傳輸」問題）
2. 分離的前向與反向階段
3. 把精確的誤差訊號送到每個突觸

這些在大腦中都不明顯存在。提出的生物合理替代方案：

| 提案 | 想法 |
|---|---|
| 回饋對齊（Lillicrap et al., 2016） | 隨機固定的回饋權重仍然能學習 |
| 預測編碼網路 | 局部預測誤差近似反向傳播梯度（Whittington & Bogacz, 2017） |
| 平衡傳播（Scellier & Bengio, 2017） | 比較能量網路的兩個平衡狀態 |
| 樹突誤差運算 | 誤差編碼在錐狀細胞的頂端樹突（Sacramento et al., 2018） |
| 爆發依賴可塑性 | 爆發與單一脈衝多工傳遞訊號與誤差（Payeur et al., 2021） |
| Forward-forward（Hinton, 2022） | 兩次前向傳播、正負資料、局部目標 |
| 三因子規則／節點擾動 | 獎勵調節的局部可塑性 |

Lillicrap et al.（2020, *Nature Reviews Neuroscience*）〈Backpropagation and the brain〉主張大腦可能透過回饋驅動的活動差異，近似類反向傳播的梯度。

## 仍然存在的巨大差異

| 大腦 | 目前的 AI |
|---|---|
| 約 20 瓦 | 千瓦到百萬瓦 |
| 持續學習且不災難性遺忘 | 訓練後大多靜態 |
| 從少量資料少樣本學習 | 需要龐大資料 |
| 出生起就具身、多感官、社會化 | 大多無身體 |
| 遞迴，且有大量回饋連結 | 每個 token 大多是前饋 |
| 對雜訊與對抗擾動穩健 | 在特定方面很脆弱 |
| 內在動機、恆定、情緒 | 外部指定的目標 |

## 延伸

- [脈衝神經網路與神經形態運算](../snn-neuromorphic/index.md)
- [記憶與學習的神經機制](../memory-learning/index.md)
- [腦機介面](../bci/index.md)

## 學習資源

- [Neuromatch NeuroAI 課程](https://neuroai.neuromatch.io/)（CC BY 4.0）
- Hassabis et al. (2017), *Neuron*
- Richards et al. (2019), *Nature Neuroscience*
- Yamins & DiCarlo (2016), *Nature Neuroscience*
- Lindsay,《Models of the Mind》（科普好書）
- Doerig et al. (2023), "The neuroconnectionist research programme", *Nature Reviews Neuroscience*
