# AI 發展史

## 時間軸總覽

| 年份 | 事件 | 意義 |
|---|---|---|
| 1943 | McCulloch & Pitts 提出形式神經元 | 第一個以邏輯描述神經元的數學模型，神經科學與計算的交會點 |
| 1949 | Hebb《行為的組織》 | 「一起放電的神經元會連在一起」，學習規則的生物學起點 |
| 1950 | Turing〈計算機器與智慧〉 | 提出「模仿遊戲」（圖靈測試） |
| 1956 | 達特茅斯會議 | McCarthy 等人命名「人工智慧」，AI 正式成為學科 |
| 1957–58 | Rosenblatt 感知器 | 第一個可學習的神經網路硬體 |
| 1959 | Samuel 西洋跳棋程式 | 「機器學習」一詞普及 |
| 1959 | Hubel & Wiesel 發現貓視覺皮質的簡單／複雜細胞 | 日後啟發 Neocognitron 與 CNN |
| 1966 | ELIZA | 早期聊天機器人，也揭示人類傾向將機器擬人化（ELIZA 效應） |
| 1969 | Minsky & Papert《Perceptrons》 | 指出單層感知器的限制，神經網路研究轉冷 |
| 1970 年代 | 第一次 AI 寒冬 | Lighthill 報告後經費縮減 |
| 1972 | Prolog | 邏輯程式語言 |
| 1970s–80s | 專家系統（MYCIN、XCON） | 知識工程商業化 |
| 1980 | 福島邦彥 Neocognitron | 階層式視覺模型，CNN 前身 |
| 1982 | Hopfield 網路 | 以能量函數描述聯想記憶（2024 年諾貝爾物理獎） |
| 1986 | Rumelhart, Hinton & Williams 推廣反向傳播 | 多層網路可以訓練 |
| 1986 | PDP（平行分散處理）叢書 | 連結主義在認知科學的里程碑 |
| 1987–93 | 第二次 AI 寒冬 | 專家系統市場崩盤 |
| 1988 | Pearl《智慧系統中的機率推理》 | 貝氏網路 |
| 1989 | LeCun 將 CNN 用於手寫數字 | LeNet |
| 1992 | TD-Gammon | 時序差分學習＋神經網路下西洋雙陸棋 |
| 1995 | SVM（Cortes & Vapnik） | 核方法盛行 |
| 1997 | Deep Blue 擊敗 Kasparov；LSTM 發表 | 搜尋式 AI 的高峰；序列學習的關鍵 |
| 1997 | Schultz, Dayan & Montague | 多巴胺神經元編碼獎勵預測誤差，對應 TD 學習 |
| 2006 | Hinton 深度信念網路 | 「深度學習」復興 |
| 2009 | ImageNet 資料集 | 大規模標註資料 |
| 2011 | IBM Watson 贏得 Jeopardy!；Siri | |
| 2012 | AlexNet 贏得 ImageNet | GPU + 大資料 + 深度 CNN，深度學習時代開始 |
| 2013 | word2vec；DQN 玩 Atari | 詞向量；深度強化學習 |
| 2014 | GAN；Seq2Seq；注意力機制（Bahdanau） | 生成模型與機器翻譯突破 |
| 2015 | ResNet；Yamins & DiCarlo 等證明 CNN 可預測靈長類視覺皮質反應 | 超深網路；NeuroAI 興起 |
| 2016 | AlphaGo 擊敗李世乭 | 深度 RL + 蒙地卡羅樹搜尋 |
| 2017 | Transformer〈Attention Is All You Need〉 | 現代 LLM 的架構基礎 |
| 2018 | BERT、GPT；圖靈獎頒給 Hinton、LeCun、Bengio | 預訓練＋微調範式 |
| 2020 | GPT-3；AlphaFold 2（CASP14）；縮放定律 | 上下文學習；蛋白質結構預測 |
| 2021 | CLIP、DALL·E；Codex | 多模態與程式碼生成 |
| 2022 | Stable Diffusion；ChatGPT（11 月） | 生成式 AI 普及 |
| 2023 | GPT-4、Claude、Llama、Gemini | 多家前沿模型與開放權重模型 |
| 2024 | 諾貝爾物理獎（Hopfield、Hinton）、化學獎（Baker、Hassabis、Jumper）；推理模型（o1）；歐盟 AI 法通過 | AI 獲科學界最高肯定；測試時運算 |
| 2025 | 推理模型與開放權重推理模型普及（如 DeepSeek-R1）；AI 代理人與程式代理人大量落地；MCP 等工具協定 | 從聊天到代理 |
| 2026 | 長時程自主代理、多代理系統、AI 輔助科學發現持續推進 | 見各章節最新動態 |

## 三大思潮

### 符號主義（Symbolism）
智慧＝符號操作。代表：邏輯推理、專家系統、知識圖譜、規劃。強項是可解釋、可驗證；弱項是知識獲取瓶頸、處理不確定性與感知困難。詳見 [符號 AI](../../theory/paradigms/symbolic-ai/index.md)。

### 連結主義（Connectionism）
智慧從大量簡單單元的連結中湧現。代表：神經網路、深度學習。直接受神經科學啟發，詳見 [NeuroAI](../../brain-mind/neuroai/index.md)。

### 行為主義／演化與控制論（Behaviorism / Cybernetics）
智慧在與環境互動中產生。代表：強化學習、控制論、具身智慧、演化計算。與心理學的行為主義（Skinner）及動物學習研究關係密切。

近年的趨勢是**融合**：神經網路負責感知與直覺，搜尋、工具與程式負責精確推理（神經符號 AI、LLM＋工具、AlphaGo 的網路＋樹搜尋）。

## AI 寒冬的教訓

1. **過度承諾**：1960 年代宣稱「20 年內機器能做人類能做的任何事」。
2. **組合爆炸**：符號方法在真實世界問題規模下失效。
3. **資料與算力不足**：神經網路的想法早在 1980 年代就有，等到 2010 年代 GPU 與網路資料才起飛。
4. **啟示**：評估方法與實際能力要分清楚；基準分數不等於真實世界可靠度（見 [評估與基準](../../engineering/evaluation/index.md)）。

## 參考文獻

- McCulloch & Pitts（1943）。A logical calculus of the ideas immanent in nervous activity。*Bulletin of Mathematical Biophysics* 5。https://doi.org/10.1007/bf02478259 — 第一個把神經元當作邏輯單元的數學模型。
- Turing（1950）。Computing Machinery and Intelligence。*Mind* 59。https://doi.org/10.1093/mind/lix.236.433 — 提出模仿遊戲，後來稱為圖靈測試。
- Rumelhart, Hinton & Williams（1986）。Learning representations by back-propagating errors。*Nature* 323。https://doi.org/10.1038/323533a0 — 推廣用於訓練多層網路的倒傳遞法。
- LeCun, Bengio & Hinton（2015）。Deep learning。*Nature* 521。https://doi.org/10.1038/nature14539 — 深度學習的綜述：透過多個處理層學習表徵。
- Nilsson, N. J.（2009）。*The Quest for Artificial Intelligence*。Cambridge University Press。https://doi.org/10.1017/cbo9780511819346 — 由史丹佛 AI 研究者撰寫的 AI 思想與成就史。
- Mitchell, M.（2019）。*Artificial Intelligence: A Guide for Thinking Humans*。Farrar, Straus and Giroux。https://melaniemitchell.me/aibook/ — 淺顯介紹當前 AI 能做什麼、不能做什麼，並附歷史脈絡。
- Sejnowski, T. J.（2018）。*The Deep Learning Revolution*。MIT Press。https://doi.org/10.7551/mitpress/11474.001.0001 — 從神經科學家角度寫的深度學習史，以及它與大腦的關聯。

## 延伸學習

- [Wikipedia: History of artificial intelligence](https://en.wikipedia.org/wiki/History_of_artificial_intelligence) — 與上述書籍一併閱讀的百科全書概述。
