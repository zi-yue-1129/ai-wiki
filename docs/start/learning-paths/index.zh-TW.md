# 學習路線

依你的背景挑一條路線。每一站都連到本站頁面，頁面底部再連到外部課程與書籍。

## 路線 A：零基礎、想全面理解 AI

1. [什麼是 AI](../index.md) → [AI 發展史](../history/index.md)
2. [機器學習](../../theory/machine-learning/index.md)（先讀直覺部分，跳過公式）
3. [深度學習](../../theory/deep-learning/index.md)
4. [大型語言模型](../../theory/models/llm/index.md) → [提示工程](../../engineering/prompting/index.md)
5. 挑兩個你有興趣的 [領域應用](../../applications/index.md)
6. [AI 安全與對齊](../../society/safety-alignment/index.md)、[倫理與公平](../../society/ethics/index.md)

**推薦外部資源**：Microsoft AI-For-Beginners（繁中）、李宏毅「生成式 AI 導論」。

## 路線 B：軟體工程師 → AI 工程師

1. [數學基礎](../../theory/math/index.md)（線性代數、機率、最佳化即可）
2. [機器學習](../../theory/machine-learning/index.md) → [深度學習](../../theory/deep-learning/index.md)
3. [Transformer](../../theory/models/transformer/index.md) → [大型語言模型](../../theory/models/llm/index.md)
4. [框架與工具](../../engineering/frameworks/index.md) → [訓練與微調](../../engineering/training/index.md)
5. [RAG](../../engineering/rag/index.md) → [AI 代理人](../../theory/models/agents/index.md)
6. [評估與基準](../../engineering/evaluation/index.md) → [MLOps 與部署](../../engineering/mlops/index.md)

**實作里程碑**：用 PyTorch 從零訓練 MNIST → 用 nanoGPT 訓練小型語言模型 → 用 LoRA 微調開源 LLM → 做一個有工具呼叫的 RAG 代理人並建立評估集。

## 路線 C：研究者（ML 理論與前沿）

1. [數學基礎](../../theory/math/index.md)（含資訊理論、凸最佳化）
2. [機率圖模型與貝氏方法](../../theory/probabilistic/index.md)
3. [深度學習](../../theory/deep-learning/index.md) 的理論段落（泛化、雙下降、縮放定律）
4. [生成模型](../../theory/generative/index.md)（擴散、流匹配）
5. [強化學習](../../theory/paradigms/reinforcement-learning/index.md) → [世界模型](../../theory/models/world-models/index.md)
6. [可解釋性](../../society/interpretability/index.md) → [AI 安全與對齊](../../society/safety-alignment/index.md)
7. [經典論文](../../reference/papers/index.md)

## 路線 D：腦科學、神經科學、心理學背景 → AI

1. [機器學習](../../theory/machine-learning/index.md) 與 [深度學習](../../theory/deep-learning/index.md)：把神經網路當作「極度簡化的神經元模型」理解
2. [計算神經科學](../../brain-mind/computational-neuroscience/index.md)：你熟悉的領域如何形式化
3. [NeuroAI](../../brain-mind/neuroai/index.md)：深度網路作為大腦模型、大腦作為 AI 靈感
4. [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：多巴胺與時序差分學習
5. [脈衝神經網路與神經形態運算](../../brain-mind/snn-neuromorphic/index.md)
6. [認知架構](../../brain-mind/cognitive-architectures/index.md)、[心理學與 AI](../../brain-mind/psychology/index.md)
7. [腦機介面與神經解碼](../../brain-mind/bci/index.md)

**推薦外部資源**：Neuromatch Academy（Computational Neuroscience、NeuroAI 兩門課，全部開源）。

## 路線 E：AI → 腦科學與認知科學

1. [神經科學基礎](../../brain-mind/neuroscience/index.md)
2. [記憶與學習的神經機制](../../brain-mind/memory-learning/index.md)
3. [認知科學](../../brain-mind/cognitive-science/index.md) → [心理學與 AI](../../brain-mind/psychology/index.md)
4. [NeuroAI](../../brain-mind/neuroai/index.md) → [意識與心靈哲學](../../brain-mind/consciousness/index.md)

## 路線 F：各產業從業者

1. [什麼是 AI](../index.md) → [大型語言模型](../../theory/models/llm/index.md) → [提示工程](../../engineering/prompting/index.md)
2. 你所在的 [領域應用](../../applications/index.md) 頁面
3. [RAG](../../engineering/rag/index.md)（把企業知識接上 LLM）
4. [法規與治理](../../society/governance/index.md)、[倫理與公平](../../society/ethics/index.md)

## 自我檢核清單

- [ ] 能解釋過擬合、偏差—變異權衡、交叉驗證
- [ ] 能手推一層神經網路的反向傳播
- [ ] 能說明注意力機制的 Q、K、V 各是什麼
- [ ] 能說明預訓練、指令微調、RLHF/DPO 的差異
- [ ] 能說出至少三個大腦與深度網路的相似處與三個差異
- [ ] 能說明 TD 誤差與多巴胺神經元的關係
- [ ] 能設計一個任務的評估集並說明資料汙染風險
- [ ] 能列出你所在領域導入 AI 的三個主要風險
