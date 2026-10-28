# 社會科學與人文學

## 計算社會科學

- **文本即資料**：以主題模型、嵌入向量與 LLM，衡量演說、新聞與社群媒體中的意識形態、情緒、框架與政策立場
- **網路分析**：社會關係、資訊與錯誤資訊的擴散
- **數位足跡資料**：移動軌跡、網路行為、行政紀錄
- **預測與解釋**：Fragile Families Challenge 顯示，即使有豐富資料與機器學習，人生結果仍然幾乎無法預測（Salganik et al., 2020, *PNAS*）——這對預測性的政策工具是發人深省的教訓
- **LLM 作為標註者**：零樣本的 LLM 編碼在許多任務上能與群眾外包工作者相當或更好（Gilardi et al., 2023），但必須針對每項任務加以驗證，而且可能編碼了偏見

## 模擬人與社會

- **矽樣本**：以人口統計背景設定 LLM，以近似調查回應（Argyle et al., 2023）；結果因族群與問題而異，並且低估了變異與少數意見
- **以 LLM 代理人為基礎的代理人模型**：Generative Agents（Park et al., 2023），以及後來根據訪談模擬 1,000 位真人態度的研究（Park et al., 2024）
- **用途**：試辦調查與實驗、探索假說；**不能**取代真實的受試者

## 經濟學

- 用於處理效應的因果機器學習（雙重／去偏機器學習、因果森林）
- 以衛星影像與替代資料進行即時估計（例如以夜間燈光與日間影像繪製貧窮地圖，Jean et al., 2016）
- AI 對經濟的影響：見[經濟與就業](../../society/economics/index.md)

## 政治學與公共政策

- 衡量極化、宣傳與審查
- 說服研究：AI 生成的訊息改變態度的效果，與人類撰寫的相當；在一項大型研究中，個人化的 AI 對話降低了人們對陰謀論的相信程度（Costello, Pennycook & Rand, 2024, *Science*）
- 政府中的演算法決策：福利詐欺偵測的醜聞（例如荷蘭的兒童津貼事件）說明了其危害

## 數位人文

- 檔案的 OCR 與手寫文字辨識（Transkribus）
- 古代文本的解讀與修復：用於希臘銘文的 Ithaca（Assael et al., 2022, *Nature*）；Vesuvius Challenge 以機器學習讀取了碳化的赫庫蘭尼姆古卷（2023–2024）
- 文體計量與作者歸屬
- 對數百萬本書、圖像與電影的文化分析
- 瀕危語言的翻譯與復振

## 方法上的提醒

- 以人工編碼的黃金標準驗證測量結果
- 在著名文本上使用 LLM 時，留意訓練資料的污染
- 為了可重現性，記錄提示與模型版本；封閉模型會無聲地改變
- 考量網路爬取與同意的倫理問題

## 學習資源

- Grimmer、Roberts 與 Stewart，*Text as Data*
- Salganik，*Bit by Bit: Social Research in the Digital Age*（可免費線上閱讀）
- Ziems et al. (2024), "Can Large Language Models Transform Computational Social Science?", *Computational Linguistics*
- 計算社會科學夏季學院（SICSS）的教材
