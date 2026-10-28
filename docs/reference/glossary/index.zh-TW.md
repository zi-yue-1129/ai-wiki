---
references: not-required  # lists and meta pages cite through their entries
---

# 詞彙表

英文術語與繁體中文（台灣）對照。術語連結至說明該概念的頁面。

## A–C

| 術語 | 中文 | 簡短定義 |
|---|---|---|
| Activation function | 啟動函數 | 套用在神經元加權和上的非線性函數（[深度學習](../../theory/deep-learning/index.md)） |
| Active learning | 主動學習 | 由模型選擇要標註哪些範例（[主動學習](../../theory/paradigms/active/index.md)） |
| Adversarial example | 對抗樣本 | 經過微擾、用來騙過模型的輸入 |
| Agent | 代理人／智慧體 | 能感知並朝目標行動的系統（[AI 代理人](../../theory/models/agents/index.md)） |
| Alignment | 對齊 | 讓 AI 追求預期目標（[安全與對齊](../../society/safety-alignment/index.md)） |
| Attention | 注意力機制 | 依相關性對資訊做加權混合（[Transformer](../../theory/models/transformer/index.md)） |
| Autoencoder | 自編碼器 | 壓縮並重建輸入的網路 |
| Backpropagation | 反向傳播 | 以鏈式法則計算梯度 |
| Bandit | 多臂吃角子老虎問題 | 平衡探索與利用的單步決策問題（[線上學習](../../theory/paradigms/online/index.md)） |
| Batch normalisation | 批次正規化 | 在一個小批次內正規化激活值 |
| Bayesian inference | 貝氏推論 | 以貝氏定理更新信念（[機率方法](../../theory/paradigms/probabilistic/index.md)） |
| Benchmark | 基準測試 | 用來比較模型的標準任務（[評估](../../engineering/evaluation/index.md)） |
| Bias–variance trade-off | 偏差—變異權衡 | 欠擬合與過擬合之間的張力 |
| Brain-computer interface (BCI) | 腦機介面 | 解碼腦訊號以控制裝置（[BCI](../../brain-mind/bci/index.md)） |
| Catastrophic forgetting | 災難性遺忘 | 學習新技能時遺失舊技能（[持續學習](../../theory/paradigms/continual/index.md)） |
| Chain-of-thought | 思維鏈 | 以文字逐步推理 |
| Cognitive architecture | 認知架構 | 關於心智結構的整合理論（[認知架構](../../brain-mind/cognitive-architectures/index.md)） |
| Complementary learning systems | 互補學習系統 | 海馬迴快速學習加上皮質慢速學習（[記憶與學習](../../brain-mind/memory-learning/index.md)） |
| Connectome | 連結體 | 神經系統完整的接線圖 |
| Context window | 上下文視窗 | 模型一次能關注的 token 數量 |
| Contrastive learning | 對比學習 | 把相似的配對拉近、其他配對推遠來學習 |
| Convolutional neural network (CNN) | 卷積神經網路 | 具有局部、共享濾波器的網路（[電腦視覺](../../theory/models/computer-vision/index.md)） |
| Cross-entropy | 交叉熵 | 標準的分類損失函數 |

## D–H

| 術語 | 中文 | 簡短定義 |
|---|---|---|
| Data augmentation | 資料增強 | 產生訓練資料的修改版本 |
| Differential privacy | 差分隱私 | 單一個人的資料幾乎不改變輸出的形式化保證（[隱私與資料保護](../../society/privacy/index.md)） |
| Diffusion model | 擴散模型 | 學習去除雜訊的生成模型（[生成模型](../../theory/paradigms/unsupervised/density-and-generative-models/generative-models/index.md)） |
| Distillation | 知識蒸餾 | 訓練小模型模仿大模型 |
| Distribution shift | 分布偏移 | 測試資料與訓練資料不同 |
| Dopamine | 多巴胺 | 傳遞獎勵預測誤差的神經調節物質 |
| DPO | 直接偏好最佳化 | 直接以偏好配對對模型進行對齊 |
| Dropout | 丟棄法 | 訓練時隨機把單元歸零 |
| Embedding | 嵌入（向量） | 稠密的向量表示 |
| Emergent ability | 湧現能力 | 在較大規模時才出現的能力 |
| Encoder / decoder | 編碼器／解碼器 | 網路中負責壓縮與生成的部分 |
| Epoch | 訓練週期 | 遍歷一次訓練資料 |
| Explainable AI (XAI) | 可解釋 AI | 解釋預測的方法（[可解釋性](../../society/interpretability/index.md)） |
| Federated learning | 聯邦學習 | 不集中資料的訓練（[聯邦學習](../../theory/paradigms/federated/index.md)） |
| Few-shot learning | 少樣本學習 | 從極少的範例中學習 |
| Fine-tuning | 微調 | 對預訓練模型進行額外訓練（[訓練](../../engineering/training/index.md)） |
| Foundation model | 基礎模型 | 可適應多種任務的大型預訓練模型 |
| Free-energy principle | 自由能原理 | 認為大腦會最小化預測誤差／驚訝度的理論（[認知科學](../../brain-mind/cognitive-science/index.md)） |
| GAN | 生成對抗網路 | 生成器與判別器互相對抗 |
| Generalisation | 泛化 | 在未見過的資料上表現良好 |
| Gradient descent | 梯度下降 | 反覆沿著梯度的反方向前進 |
| Graph neural network (GNN) | 圖神經網路 | 在圖結構上運作的網路（[GNN](../../theory/models/gnn/index.md)） |
| Grid cell / place cell | 網格細胞／位置細胞 | 編碼空間位置的神經元 |
| Hallucination | 幻覺 | 模型以肯定的語氣輸出錯誤的內容 |
| Hebbian learning | 赫布學習 | 「一起放電的神經元會連在一起」 |
| Hippocampus | 海馬迴 | 負責情節記憶與導航的腦區 |
| Hyperparameter | 超參數 | 訓練前設定的參數（如學習率） |

## I–P

| 術語 | 中文 | 簡短定義 |
|---|---|---|
| Imitation learning | 模仿學習 | 從示範中學習（[模仿學習](../../theory/paradigms/imitation/index.md)） |
| In-context learning | 上下文學習 | 從提示中的範例學習 |
| Inductive bias | 歸納偏誤 | 引導學習的內建假設 |
| Inference | 推論 | 執行已訓練的模型；也指統計推論 |
| Interpretability | 可解釋性 | 理解模型內部的運作 |
| KL divergence | KL 散度 | 衡量兩個分布之間差異的指標 |
| Knowledge graph | 知識圖譜 | 由實體與關係組成的圖 |
| Large language model (LLM) | 大型語言模型 | 以文字訓練的大型 Transformer（[LLM](../../theory/models/llm/index.md)） |
| Latent space | 潛在空間 | 學到的壓縮表徵空間 |
| Learning rate | 學習率 | 梯度下降中的步長 |
| LoRA | 低秩適應 | 以低秩更新進行參數高效的微調 |
| Loss function | 損失函數 | 訓練時要最小化的量 |
| Membership inference | 成員推論 | 判斷某筆紀錄是否在模型的訓練集中（[隱私與資料保護](../../society/privacy/index.md)） |
| Memorisation | 記憶化 | 模型重現特定的訓練樣本（[隱私與資料保護](../../society/privacy/index.md)） |
| Meta-learning | 元學習 | 學習如何學習（[元學習](../../theory/paradigms/meta-learning/index.md)） |
| Mixture of experts (MoE) | 混合專家 | 把每個 token 路由到一部分專家子網路 |
| Model card | 模型卡 | 記錄模型預期用途與限制的文件 |
| Multimodal | 多模態 | 同時使用多種資料類型（[多模態模型](../../theory/models/multimodal/index.md)） |
| Neuromorphic computing | 神經形態運算 | 受大腦啟發、事件驅動的硬體（[SNN](../../brain-mind/snn-neuromorphic/index.md)） |
| Neuron (artificial / biological) | 神經元 | 網路或神經系統的基本單元 |
| Overfitting | 過擬合 | 記住訓練資料，卻無法泛化 |
| Parameter | 參數 | 模型學到的權重 |
| Perplexity | 困惑度 | 平均負對數似然的指數 |
| Policy | 策略 | 強化學習中從狀態映射到動作的函數 |
| Predictive coding | 預測編碼 | 認為皮質傳遞預測誤差的理論 |
| Pre-training | 預訓練 | 大規模的初始自監督訓練 |
| Prompt | 提示 | 輸入給模型的指令（[提示工程](../../engineering/prompting/index.md)） |
| Prompt injection | 提示注入 | 隱藏在模型輸入中的惡意指令 |

## Q–Z

| 術語 | 中文 | 簡短定義 |
|---|---|---|
| Quantisation | 量化 | 以較低精度的數字表示權重或激活值 |
| RAG | 檢索增強生成 | 檢索文件以使生成有所依據（[RAG](../../engineering/rag/index.md)） |
| Recurrent neural network (RNN) | 循環神經網路 | 具有循環狀態的網路 |
| Regularisation | 正規化（正則化） | 減少過擬合的技術 |
| Reinforcement learning (RL) | 強化學習 | 從獎勵中學習（[強化學習](../../theory/paradigms/reinforcement-learning/index.md)） |
| Representation learning | 表徵學習 | 自動學習有用的特徵 |
| Reward hacking | 獎勵駭客 | 利用獎勵函數中的缺陷 |
| RLHF | 基於人類回饋的強化學習 | 以人類偏好資料對模型進行對齊 |
| Scaling laws | 縮放定律 | 規模與效能之間的冪次關係 |
| Self-attention | 自注意力 | 序列對自身的注意力 |
| Self-supervised learning | 自監督學習 | 從資料本身推導出標籤（[自監督學習](../../theory/paradigms/self-supervised/index.md)） |
| Semi-supervised learning | 半監督學習 | 少量標籤加上大量未標註的範例 |
| Spiking neural network (SNN) | 脈衝神經網路 | 以脈衝進行通訊的網路 |
| STDP | 脈衝時序依賴可塑性 | 以時間為基礎的突觸學習規則 |
| Supervised learning | 監督式學習 | 從有標籤的範例中學習（[監督式學習](../../theory/paradigms/supervised/index.md)） |
| Synapse | 突觸 | 神經元之間的連接 |
| TD error | 時序差分誤差 | 強化學習中的獎勵預測誤差 |
| Theory of mind | 心智理論 | 把心理狀態歸因給他人 |
| Token / tokenisation | 詞元／分詞 | 語言模型使用的文字單位 |
| Transfer learning | 遷移學習 | 在不同任務之間重用知識（[遷移學習](../../theory/paradigms/transfer/index.md)） |
| Transformer | Transformer | 以注意力為基礎的架構 |
| Underfitting | 欠擬合 | 模型太簡單，無法捕捉規律 |
| Unsupervised learning | 非監督式學習 | 在沒有標籤的情況下學習結構（[非監督式學習](../../theory/paradigms/unsupervised/index.md)） |
| Vision Transformer (ViT) | 視覺 Transformer | 作用在影像區塊上的 Transformer |
| World model | 世界模型 | 預測環境的內部模型（[世界模型](../../theory/models/world-models/index.md)） |
| Zero-shot | 零樣本 | 不提供任何任務範例即可執行任務 |
