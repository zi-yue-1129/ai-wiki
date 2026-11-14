---
related:
  - engineering/evaluation
  - society/ethics
tags:
  - evaluation
  - benchmarks
  - construct validity
  - ethics
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - AI and the Everything in the Whole Wide World Benchmark
  - Benchmark validity
  - 基準的構念效度
  - 基準批判
---

# 基準的構念效度：〈AI and the Everything in the Whole Wide World Benchmark〉（Raji et al., 2021）

Raji、Bender 與 Paullada（2021）主張，少數有影響力的 AI 基準被當成衡量整體進展的尺規，而這種解讀缺乏構念效度。基準可以顯示系統在有限而特定的任務集合上表現良好，但論文認為，這份證據並不足以支持對整體能力的宣稱（Raji et al., 2021）。

## 概觀

幾個子領域都依賴少數基準，把它們當作常見問題的代表，並把它們視為通往靈活、通用 AI 系統的里程碑。在這些基準上的最先進結果，被解讀為朝這些長期目標的進展。論文檢視這種做法的限制，並追問基準究竟能提供什麼樣的證據（Raji et al., 2021）。

標題是刻意誇張的比喻。作者指出，想像中的「通用」基準並不存在，因為每個真實的基準都是有限、特定且有情境的（第 4 節）。

## 關鍵概念

- **構念效度**：測驗是否真的衡量它宣稱要衡量的性質。基準只有在任務能良好代表某項能力時，才對該能力具有構念效度。
- **作為代表的基準**：用來替代廣泛目標（例如一般物件辨識或一般語言理解）的資料集（第 3 節）。
- **彙總指標**：單一數字，可能掩蓋任務之間、使用者群體之間，或錯誤類型之間的差異。

## 論證

作者指出三組效度問題，分別在論文第 4 節討論。

**任務設計受限。** 任務常因方便或經驗法則而被挑選，而非系統性地選擇。語言能力也常與世界知識和常識推理混為一談，而純文字任務無法完整測試後者（第 4.1.1 與 4.1.2 節）。

**脫離情境的資料與報告。** 資料集是封閉的，並受限於特定時間，而且可能偏向特定情境。沒有資料集是中立的，只用英文的基準反映的是其建立者的價值觀與語言（第 4.2.1 與 4.2.2 節）。

**不當的社群使用。** 追逐最先進分數會偏向漸進式的進步，而彙總指標會掩蓋有意義的差異。基準分數也被用來為它們並非為此設計的實際應用辯護，而子群體的失敗可能隱藏在彙總結果之中（第 4.3.1 至 4.3.3 節）。

## 建議

作者並不主張把基準做得更大或更通用。增加任務無法解決構念效度的問題。他們建議：

- 把基準呈現為對具體、範圍明確且有情境的任務的評估（第 5 節）。
- 使用測試套件、稽核與對抗性測試（附錄 A.1）。
- 分析系統輸出，包括錯誤分析、分群分析與反事實分析（附錄 A.2）。
- 進行消融測試，並測量能源使用、記憶體與穩定性等性質（附錄 A.3 與 A.4）。
- 在完整測試集之外，同時報告社會上重要的資料切片上的表現（附錄 A.2）。

作者把基準評測描述為「調查一片地景」，而不是「贏得一場競賽」（第 6 節）。

## 相關連結

- [ImageNet](vision/imagenet.md) 與 [ImageNetV2](vision/imagenet-v2.md) 展示了測試集擬合的問題：原始測試集上的分數，可能部分反映了該測試集的蒐集方式。
- [GLUE](language/glue.md) 是論文討論的基準之一，它是多任務基準，其綜合分數可能掩蓋任務層級的差異（Wang et al., 2018）。
- 模型卡與資料集數據表（datasheets）是記錄模型或資料集用途的提案，回應論文提出的情境問題（Mitchell et al., 2019; Gebru et al., 2018）。

## 應用

當團隊把基準分數當作產品或族群已準備就緒的證據時，論文的建議就適用。作者建議的分群評估，正是揭露商用性別分類器中交叉群體準確率差距的那類分析（Buolamwini & Gebru, 2018）。

## 未解問題

- 基準能以構念效度衡量哪些能力，團隊又如何證明其任務確實代表該能力。
- 如何在不依賴單一代表性基準的情況下，報告廣泛能力的進展。

## 參考文獻

### 開創性論文

- Raji, I. D., Bender, E. M. & Paullada, A. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 關於有影響力 AI 基準的構念效度的立場論文，本頁討論的效度問題與建議皆出自此文。
- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — 多任務基準，其綜合分數是論文檢視的代表之一。
- Russakovsky, O. et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv. https://arxiv.org/abs/1409.0575 — 論文討論到的基準，其測試集與論文的論證相關。
- Buolamwini, J. & Gebru, T. (2018). *Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification*. PMLR 81:77–91. https://proceedings.mlr.press/v81/buolamwini18a.html — 分群評估，發現被彙總分數掩蓋的交叉群體準確率差距。

### 文件化與批判

- Gebru, T. et al. (2018). *Datasheets for Datasets*. arXiv. https://arxiv.org/abs/1803.09010 — 記錄資料集的動機、組成與建議用途的提案。
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting*. FAT* '19, pp. 220–229. https://doi.org/10.1145/3287560.3287596 — 記錄模型預期用途與評估的提案。
- Bender, E. M., Gebru, T., McMillan-Major, A. & Shmitchell, S. (2021). *On the Dangers of Stochastic Parrots*. FAccT '21, pp. 610–623. https://doi.org/10.1145/3442188.3445922 — 對大型語言模型規模與文件化的批判。
