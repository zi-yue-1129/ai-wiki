---
translation_reviewed: 2026-10-28
---

# 記憶與學習的神經機制

## 記憶的種類

```mermaid
flowchart TB
  M[記憶] --> STM[短期／工作記憶]
  M --> LTM[長期記憶]
  LTM --> DEC[陳述性／外顯]
  LTM --> NONDEC[非陳述性／內隱]
  DEC --> EP[情節記憶：事件——海馬迴]
  DEC --> SEM[語意記憶：事實——新皮質]
  NONDEC --> PROC[程序記憶：技能——基底核、小腦]
  NONDEC --> PRIME[促發——皮質]
  NONDEC --> COND[制約——杏仁核、小腦]
```

| 記憶系統 | 大腦基礎 | AI 對應 |
|---|---|---|
| 工作記憶 | 前額葉與頂葉的持續活動；容量有限（約 4 個組塊，Cowan 2001） | 上下文視窗、遞迴狀態 |
| 情節記憶 | 海馬迴，綁定「什麼—哪裡—何時」 | 情節緩衝、檢索增強記憶、對話紀錄 |
| 語意記憶 | 分散的新皮質，前顳葉樞紐 | 模型權重、知識圖譜 |
| 程序記憶 | 基底核、小腦、運動皮質 | 策略、工具／技能庫 |

## 病人 H.M.

1953 年為治療癲癇切除雙側內側顳葉後，Henry Molaison 再也無法形成新的情節記憶，卻能學會新的運動技能（鏡像描圖），即使不記得自己練習過。Brenda Milner 的研究確立了記憶有多個系統，而海馬迴是形成陳述性記憶的關鍵。

## 突觸可塑性

- **長期增益（LTP）**（Bliss & Lømo, 1973）與**長期抑制（LTD）**：突觸持久的增強或減弱
- **NMDA 受體**是巧合偵測器——只有在突觸前釋放麩胺酸*且*突觸後神經元去極化時才打開——分子層級的 Hebb 規則
- **早期 vs 晚期 LTP**：持久改變需要蛋白質合成；**突觸標記與捕獲**解釋強弱事件如何互動
- **結構可塑性**：樹突棘會長出與縮回，有些可維持數月
- **恆定可塑性**（突觸縮放）讓活動維持在範圍內——類似正規化層
- **記憶痕跡細胞（engram）**：用光遺傳學刺激學習時活躍的神經元，可以重新喚起記憶（利根川實驗室；Liu et al., 2012）

## 鞏固與重播

- **系統鞏固**：記憶一開始依賴海馬迴，逐漸轉為依賴皮質
- **尖波漣波（sharp-wave ripples）**：休息與慢波睡眠時，海馬迴位置細胞以壓縮的時間**重播**最近的經驗，有時倒著播、有時產生新的路徑（Wilson & McNaughton, 1994；Foster & Wilson, 2006）
- 干擾漣波會損害學習；增強則可能改善
- **睡眠**：慢振盪、紡錘波與漣波協調海馬迴—皮質對話；突觸恆定假說認為睡眠會縮減突觸強度

### 互補學習系統（CLS）

McClelland、McNaughton 與 O'Reilly（1995）解釋了*為什麼*需要兩個系統：

- **海馬迴**用稀疏、模式分離的編碼快速學習，儲存個別情節而不互相干擾
- **新皮質**用重疊、分散的編碼緩慢學習，萃取統計結構
- 若皮質學得太快，會產生**災難性干擾**；因此由海馬迴**交錯重播**新舊記憶來訓練皮質

這是深度強化學習中**經驗重播**、以及重播式[持續學習](../../theory/paradigms/continual/index.md)的概念根源。Kumaran、Hassabis 與 McClelland（2016）為深度學習時代更新了這個理論。

## 遺忘是一種功能

- Ebbinghaus 遺忘曲線（1885）：一開始快速流失，之後趨緩
- **間隔效應**與**測驗效應**：分散練習與提取練習大幅改善保留——間隔重複軟體（Anki、SuperMemo）就是以記憶衰退模型為基礎
- 遺忘可能幫助泛化，避免過度擬合過時資訊（Richards & Frankland, 2017〈The persistence and transience of memory〉）
- **再鞏固**：被提取的記憶會變得不穩定而可被更新——記憶是重建，不是錄影（Bartlett；Loftus 的錯誤訊息研究）

## 模式分離與模式完成

- **齒狀回**做模式分離（讓相似的輸入變得不同）
- **CA3** 的遞迴側枝做模式完成（從線索取回完整記憶）——類 Hopfield 的**自聯想記憶**
- 現代 Hopfield 網路把這點和 Transformer 的注意力連在一起（見 [Transformer](../../theory/models/transformer/index.md)）

## 給 AI 系統的記憶設計啟示

| 大腦的啟示 | AI 設計 |
|---|---|
| 分離快速的情節儲存與緩慢的語意儲存 | RAG／外部記憶＋模型權重 |
| 重播防止干擾 | 重播緩衝區、持續學習中的複習 |
| 鞏固重要的東西 | 摘要與蒸餾代理人的記憶；優先重播 |
| 提取依賴線索且是重建的 | 檢索品質取決於查詢寫法；生成的「記憶」可能是錯的 |
| 遺忘有用 | 記憶衰減、近期加權、修剪過時知識 |
| 工作記憶有限且需主動維持 | 上下文管理、草稿區、任務拆解 |

## 關鍵方法

每個方法各有專頁，此處的概述與比較從簡。

### 病人 H.M. 與內側顳葉損傷（Scoville & Milner, 1957）

- **概述：** 雙側切除內側顳葉的病人，顯示記憶依賴哪些結構。
- **比較：** 這是損傷研究：能證明必要性，但無法說明機制；機制由突觸與回放相關的方法處理。
- **完整內容：** [內側顳葉損傷](medial-temporal-lesions/index.md)

### 長期增益（Bliss & Lømo, 1973）

- **概述：** 短暫的高頻刺激能讓突觸長時間增強，是記憶的一個候選細胞機制。
- **比較：** 這是細胞層級的機制，而非系統層級的解釋。下方的互補學習系統說明這種可塑性如何放進記憶系統。
- **完整內容：** [長期增益](long-term-potentiation/index.md)

### 互補學習系統（McClelland, McNaughton & O'Reilly, 1995）

- **概述：** 快速的海馬迴儲存與緩慢的新皮質學習者，透過回放連結。
- **比較：** 系統層級的解釋，結合上述的損傷與可塑性證據。
- **完整內容：** [互補學習系統](complementary-learning-systems/index.md)

## 學習資源

- Squire & Kandel,《Memory: From Mind to Molecules》
- Eichenbaum,《The Cognitive Neuroscience of Memory》
- McClelland, McNaughton & O'Reilly (1995), *Psychological Review*
- Kumaran, Hassabis & McClelland (2016), *Trends in Cognitive Sciences*
- Buzsáki,《The Brain from Inside Out》

## 參考文獻

### 開創性論文

- Scoville, W. B. & Milner, B. (1957). Loss of recent memory after bilateral hippocampal lesions. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp.20.1.11 — 報告包括 H.M. 在內、雙側內側顳葉損傷的病人，確立這些結構對新記憶的作用。
- Bliss, T. V. P. & Lømo, T. (1973). Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1973.sp010273 — 長期增益的首次報告，許多記憶模型的突觸基礎。
- McClelland, J. L., McNaughton, B. L. & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review*. https://doi.org/10.1037/0033-295X.102.3.419 — 互補學習系統理論的原始版本，包含干擾與交錯學習的模擬。

### 綜述與教科書

- Kumaran, D., Hassabis, D. & McClelland, J. L. (2016). What learning systems do intelligent agents need? Complementary learning systems theory updated. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2016.05.004 — 在深度學習、重播與兩個系統角色的脈絡下重新檢視此理論。
- Richards, B. A. & Frankland, P. W. (2017). The persistence and transience of memory. *Neuron*. https://doi.org/10.1016/j.neuron.2017.04.037 — 主張遺忘有助於泛化，記憶應被理解為持久與短暫之間的平衡。
