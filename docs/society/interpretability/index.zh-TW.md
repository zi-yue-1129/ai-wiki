# 可解釋性

理解模型**為什麼**產生某個輸出——用於除錯、建立信任、科學研究、法規與安全。

## 兩個傳統

| | 可解釋 AI（XAI） | 機械式可解釋性 |
|---|---|---|
| 目標 | 向使用者與稽核人員解釋個別預測 | 對網路內部學到的演算法進行逆向工程 |
| 方法 | 特徵歸因、替代模型、反事實 | 電路、特徵、因果介入 |
| 典型模型 | 表格模型、影像分類器 | Transformer、LLM |

## 可解釋 AI 的方法

| 方法 | 想法 |
|---|---|
| 本質上可解釋的模型 | 線性模型、小型決策樹、規則清單、GAM（EBM）——Rudin（2019）主張在高風險決策中優先採用 |
| 排列重要性 | 打亂某個特徵後，效能的下降程度 |
| LIME | 在單一預測附近擬合局部的線性替代模型 |
| SHAP | 具有賽局理論性質的 Shapley 值歸因 |
| 顯著性圖／Grad-CAM／積分梯度 | 哪些像素或 token 驅動了輸出 |
| 反事實解釋 | 能使決策翻轉的最小改變 |
| 基於概念（TCAV） | 對人類定義的概念之敏感度 |

提醒：歸因圖可能不忠實，或無法通過合理性檢查（Adebayo et al., 2018）；而解釋本身也可能增加過度信任。

歸因方法的完整內容，包括合理性檢查與 Transformer 的歸因，見[特徵歸因：SHAP、LIME 與顯著性](feature-attribution.md)。

## 機械式可解釋性

完整內容（包括各方法的比較與開放問題）見[機械式可解釋性與電路](mechanistic-interpretability.md)。

- **電路**：實現可辨識演算法的小型子網路——視覺模型中的曲線偵測器、Transformer 中的歸納頭（induction heads）、間接賓語辨識電路
- **疊加（superposition）**：網路透過重疊的方向，表示比神經元數量更多的特徵（Elhage et al., 2022），使單一神經元呈現多義性（polysemantic）
- **稀疏自編碼器（SAE）與字典學習**能從 LLM 的激活中抽出數百萬個較易解讀的特徵（Anthropic 的 "Scaling Monosemanticity"，2024；OpenAI 與 Google DeepMind 的類似工作，以及 Gemma Scope）。完整內容見[稀疏自編碼器與特徵字典](sparse-autoencoders.md)
- **歸因圖／電路追蹤**：追蹤特徵如何交互作用以產生輸出，例如揭示押韻時的多步驟推理與提前規劃（Anthropic, 2025）
- **因果介入**：激活修補（activation patching）、因果追蹤（定位事實記憶，Meng et al., 2022）、引導向量（steering vectors）
- **探測（probing）**：從激活中讀取資訊的線性分類器——例如真實性方向，或 Othello-GPT 中的棋盤狀態。控制任務與表徵分析見[探測分類器與表徵分析](probing.md)
- **思維鏈的忠實性**：模型陳述的推理是否反映其實際運算——通常只是部分如此

## 與神經科學的平行

可解釋性研究者面對的，正是神經科學家數十年來面對的問題——只不過他們能完全存取每一個「神經元」：

| 神經科學 | 可解釋性 |
|---|---|
| 單一神經元的調諧曲線 | 神經元與特徵的視覺化 |
| 「祖母細胞」與概念細胞 | 單義性特徵 |
| 前額葉皮質的混合選擇性 | 多義性神經元、疊加 |
| 損傷與光遺傳學 | 消融、激活修補 |
| 群體編碼與神經流形 | 線性表徵、低維結構 |
| 連結體學 | 權重與歸因圖 |

「神經科學家能理解一顆微處理器嗎？」（Jonas & Kording, 2017）顯示，即使在一顆已知的晶片上，標準的神經科學方法也力有未逮——這對兩個領域都是警示。方法如今是雙向流動的：表徵相似性分析與降維來自神經科學；SAE 與因果修補則反過來用於神經資料分析。

## 用途

- 除錯虛假相關與捷徑
- 偏見稽核，以及法規要求的解釋（GDPR、信用法規、歐盟 AI 法）
- 偵測欺騙或隱藏目標（稽核遊戲）
- 不重新訓練即可引導行為
- 科學發現：從超人類的模型中學習新概念（例如 AlphaZero 的西洋棋概念，Schut et al., 2023）

## 學習資源

- Molnar，*Interpretable Machine Learning*（可免費線上閱讀）
- [Transformer Circuits Thread](https://transformer-circuits.pub/)
- Neel Nanda 的機械式可解釋性指南；[TransformerLens](https://github.com/TransformerLensOrg/TransformerLens)
- Bereska & Gavves (2024), "Mechanistic Interpretability for AI Safety — A Review"
- [Captum](https://captum.ai/)、[SHAP](https://github.com/shap/shap)
