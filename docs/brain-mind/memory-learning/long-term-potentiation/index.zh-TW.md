---
status: complete
last_reviewed: 2026-10-28
---

# 長期增益（Bliss 與 Lømo，1973）

短暫的高頻刺激爆發能使一個突觸增強數小時，這使長期增益（long-term potentiation，LTP）成為記憶細胞機制的主要候選。

## 概觀

學習必然會改變大腦中的某些東西，而最可能的地方是突觸，也就是一個神經元把訊號傳給另一個神經元的接合處。Hebb 式的想法認為，同時活動的神經元之間的連結會被加強，此類想法需要生理學上的檢驗。Bliss 與 Lømo（1973）清楚示範了：突觸可以發生一種改變，其持續時間遠超過引起它的刺激。這種改變如今稱為長期增益（LTP）。

LTP 是神經科學中研究最透徹的機制之一。它本身並不是完整的記憶理論，但許多記憶模型都以它為基礎，並把神經元的行為與經驗的儲存連結起來。它介於[記憶系統的患者證據](../medial-temporal-lesions/index.md)與[記憶如何隨時間組織的系統層級理論](../complementary-learning-systems/index.md)之間。

## 關鍵概念

- **突觸**：一個神經元影響另一個神經元的接合處。其強度決定了突觸前訊號能改變突觸後細胞多少。
- **穿通路徑（perforant path）**：把訊號從內嗅皮質傳到海馬迴齒狀回的纖維束。
- **齒狀回（dentate gyrus）**：海馬迴的一個區域，其顆粒細胞接收穿通路徑的輸入。
- **群體反應（population response）**：以電極記錄到的許多神經元的合併反應。在這些實驗中它有兩個部分：反映細胞去極化的興奮性突觸後電位（EPSP），以及反映細胞放電的群體峰電位（population spike）。
- **增強（potentiation）**：對同一輸入的反應出現持久增加。與之相反的是長期抑制（LTD），即持久減弱。

## 問題

突觸是否存在可以儲存記憶的持久實體變化？有兩個問題尚未解決。第一，突觸能否以持續數小時、而非數毫秒或數秒的方式改變？第二，這種改變是否取決於突觸如何被使用，因而能儲存特定的資訊？Bliss 與 Lømo 直接處理了第一個問題。

## 核心想法

Bliss 與 Lømo 刺激麻醉兔子的穿通路徑，並在齒狀回記錄反應。他們先施以短暫的高頻刺激串，再以低頻單一脈衝測試反應。刺激串之後，對測試脈衝的反應在很長時間內維持增強。刺激本身很短，但突觸的改變遠遠持續得更久。這是首次報告這類持久的突觸改變。

## 方程式或演算法

實驗程序可以依 1973 年論文的條件寫成編號步驟：

1. 麻醉兔子，並在齒狀區放置細胞外電極。記錄對穿通路徑施加單一脈衝的群體反應，作為基線測試反應。
2. 施加高頻的條件刺激串：每秒 10 至 20 次，持續 10 至 15 秒，或每秒 100 次，持續 3 至 4 秒。
3. 以低頻單一脈衝繼續測試，並追蹤 EPSP 振幅、群體峰電位振幅與峰電位潛時隨時間的變化。
4. 把反應與基線比較。增強即是相對於該基線的持久增加。

描述基本結果不需要方程式，但後來的研究把 LTP 表述為突觸權重 $w$ 的改變，其大小取決於突觸前與突觸後活動的時序與頻率。1973 年的論文屬於描述性研究：它測量反應及其改變，而非建立形式化模型。

## 結果

在 18 隻兔子中，有 15 隻的群體反應在一次或多次條件刺激串之後，對單一穿通路徑脈衝的反應被增強，持續時間從 30 分鐘到 10 小時不等。兩種刺激串都產生了長期增益。每秒 10 至 20 次的刺激串使群體峰電位大幅增強，而每秒 100 次的刺激串則在刺激期間抑制了峰電位。論文分析了三個參數：EPSP 振幅、峰電位振幅與峰電位潛時。在所有實驗中，潛時縮短是最常見的增強徵象，出現在 57% 的實驗中。作者的結論是，兩種獨立機制促成了持久的增強：突觸傳遞效率的提高，以及顆粒細胞群體興奮性的提高。

後續研究顯示，最透徹研究的 LTP 形式依賴 NMDA 受體。Bliss 與 Collingridge（1993）指出，這些受體使突觸具有 Hebb 式的性質，因為它們把突觸後膜的電活動轉換為化學訊號，而這些訊號會引發突觸兩側的持久改變。Morris 等人（1986）報告，NMDA 受體拮抗劑 AP5 阻斷了 LTP，並選擇性地損害了學習，這把突觸機制與行為連結了起來。

## 限制

1973 年的實驗是在麻醉動物身上進行，以細胞外記錄測量群體反應，而非單一突觸。與學習的連結是推論。論文顯示增強可以持續數小時，但並未顯示被增強的突觸儲存了任何特定記憶。Lynch（2004）明確指出這一點：目前尚不清楚維持 LTP 的變化是否也是記憶鞏固的基礎。

論文也沒有檢驗分子基礎。Bliss 與 Collingridge（1993）總結了後來的研究，把最透徹研究的 LTP 形式與 NMDA 受體連結起來。Malenka 與 Bear（2004）的標題即提到「豐富得令人困擾」（embarrassment of riches），他們討論了增強與抑制有多少種形式，這使得判斷哪一種形式對記憶最重要變得更為困難。

## 關鍵方法

以下三種具代表性的替代方法，解釋突觸如何改變，或這些改變與記憶的關係：

- [內側顳葉損傷的患者（Scoville 與 Milner，1957）](../medial-temporal-lesions/index.md)：顯示新記憶需要海馬迴系統的行為證據。它並未顯示突觸機制，這由 LTP 研究提供。
- [互補學習系統（McClelland 等人，1995）](../complementary-learning-systems/index.md)：關於快速與緩慢學習如何互動的系統層級理論，其快速儲存器需要像 LTP 這樣的可塑性機制來實作。
- 脈衝時序依賴可塑性（Dan 與 Poo，2004）：一種規則，突觸前與突觸後脈衝的相對時序決定突觸是增強還是減弱。它是 LTP 所檢驗之 Hebb 式想法的細化。

## 連結

- 母頁：[記憶與學習的神經機制](../index.md)
- 同一主題的另一方法：[內側顳葉損傷](../medial-temporal-lesions/index.md)
- 同一主題的另一方法：[互補學習系統](../complementary-learning-systems/index.md)
- 脈衝模型：類似 LTP 的規則用於脈衝神經網路。見[SNN 與神經形態運算](../../snn-neuromorphic/index.md)。

## 應用

- **模型中的赫布學習。** 許多人工學習模型使用類似 LTP 的規則：當連結兩端的細胞同時活動時，連結便加強。赫布學習的術語見[母頁](../index.md)。
- **神經形態硬體。** 脈衝硬體實作基於時序的可塑性規則，這些規則比 Bliss 與 Lømo 之後研究的突觸機制更接近生理。見[SNN 與神經形態運算](../../snn-neuromorphic/index.md)。
- **藥物與疾病研究。** 由於 LTP 依賴 NMDA 受體，會改變這些受體的藥物與疾病狀態，會被研究其對學習的影響。Morris 等人（1986）是這種研究取向的經典例子。

## 未解問題

- LTP 是否造成記憶，還是伴隨儲存記憶的歷程？Lynch（2004）指出，目前尚不清楚維持 LTP 的變化是否也是記憶鞏固的基礎。
- 哪些分子變化能在數天到數月間維持 LTP，它們又如何與記憶鞏固相關？Lynch（2004）將此列為未解問題。
- 在切片與麻醉動物中觀察到的 LTP，有多少會在自然行為中發生？
- 哪一種可塑性形式（LTP、LTD，還是時序規則）最能解釋特定記憶如何被儲存？

## 參考文獻

### 開創性論文

- Bliss, T. V. P. & Lømo, T. (1973). Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1973.sp010273 — 麻醉兔子齒狀區首次報告的長期增益，持續時間從 30 分鐘到 10 小時。
- Morris, R. G. et al. (1986). Selective impairment of learning and blockade of long-term potentiation by an N-methyl-D-aspartate receptor antagonist, AP5. *Nature*. https://doi.org/10.1038/319774a0 — 把 NMDA 受體與 LTP 連結起來，報告拮抗劑 AP5 阻斷了 LTP 並損害了學習。
- Bliss, T. V. P. & Collingridge, G. L. (1993). A synaptic model of memory: long-term potentiation in the hippocampus. *Nature*. https://doi.org/10.1038/361031a0 — 將 LTP 呈現為記憶儲存模型的綜述，涵蓋其對 NMDA 受體的依賴與 Hebb 式性質。

### 綜述與教科書

- Lynch, M. A. (2004). Long-term potentiation and memory. *Physiological Reviews*. https://doi.org/10.1152/physrev.00014.2003 — 綜述 LTP 與學習、記憶的關係，尤其是空間學習，並討論 LTP 的維持與記憶鞏固是否共享機制這個未解問題。
- Malenka, R. C. & Bear, M. F. (2004). LTP and LTD: an embarrassment of riches. *Neuron*. https://doi.org/10.1016/j.neuron.2004.09.012 — 綜述突觸增強與抑制的多種形式與機制，以及這種多樣性為何對記憶重要。
- Dan, Y. & Poo, M.-M. (2004). Spike timing-dependent plasticity of neural circuits. *Neuron*. https://doi.org/10.1016/j.neuron.2004.09.007 — 綜述脈衝時序依賴可塑性，這是細化 LTP 背後 Hebb 式想法的時序規則。
