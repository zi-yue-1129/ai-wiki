# 語音與音訊

## 任務

| 任務 | 說明 | 代表模型／工具 |
|---|---|---|
| 自動語音辨識 ASR | 語音 → 文字 | Whisper、wav2vec 2.0、Conformer、Paraformer |
| 語音合成 TTS | 文字 → 語音 | Tacotron、FastSpeech、VITS、神經編解碼器語言模型（VALL-E 類） |
| 語音轉換 / 聲音複製 | 改變說話者音色 | RVC、零樣本 TTS |
| 說話者辨識與分離 | 誰在說話、何時說 | pyannote |
| 語音增強 | 降噪、去迴響 | Demucs 等 |
| 音樂生成 | 文字或旋律 → 音樂 | MusicLM、MusicGen、Suno、Udio 等 |
| 音源分離 | 分離人聲、樂器 | Demucs |
| 聲音事件偵測 | 槍聲、玻璃破裂、鳥鳴 | PANNs、BirdNET |
| 語音對話模型 | 端到端即時語音對話 | GPT-4o 類全模態模型、Moshi |

## 技術要點

- **特徵**：梅爾頻譜、MFCC；或直接從波形學（wav2vec）
- **神經音訊編解碼器**：EnCodec、SoundStream 把音訊壓縮成離散 token，讓語言模型能「說話」與「作曲」
- **端到端語音 LLM**：不經過文字轉換，直接處理語音 token，保留語調與情緒，延遲更低
- **聲碼器**：WaveNet → HiFi-GAN → 編解碼器解碼

## 語音辨識中的影格對齊

連結式時間分類（Connectionist Temporal Classification，CTC）不需要逐一標註每個編碼器影格，就能計算轉錄序列的機率。路徑的符號集合包含標籤與特殊空白符號（∅）；折疊映射先合併連續重複的符號，再移除空白符號。[^ctc]

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-collapse-scan-still.svg" data-motion-src="../../../assets/concept-animations/ctc-collapse-scan-motion.svg" data-still-src="../../../assets/concept-animations/ctc-collapse-scan-still.svg" alt="依序掃描影格路徑 A、A、空白、A、B，僅第一、第四與第五個影格輸出標籤，得到 AAB。" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 可讀靜態預覽](../../../assets/concept-animations/ctc-collapse-scan-still.svg)

移動的訊號代表輸出標籤送至轉錄序列。第二個影格重複 A，因此不輸出；第三個影格的空白隔開前後兩段 A。若先移除空白再合併重複標籤，會錯誤得到 AB。空白不是分詞符號，也不是實際輸出的字元。

### 為什麼貪婪解碼不一定得到最可能的轉錄序列

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-path-mass-still.svg" data-motion-src="../../../assets/concept-animations/ctc-path-mass-motion.svg" data-still-src="../../../assets/concept-animations/ctc-path-mass-still.svg" alt="四條雙影格路徑將機率質量匯入兩個折疊後的轉錄序列；貪婪選擇的雙空白路徑為 36%，三條對應 A 的路徑總和為 64%。" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 可讀靜態預覽](../../../assets/concept-animations/ctc-path-mass-still.svg)

設定兩個影格各自對空白給予 0.6 的機率、對 A 給予 0.4 的機率。給定輸入，CTC 將路徑上的影格機率相乘，並加總所有折疊成相同轉錄序列的路徑機率。[^ctc] 四條路徑的機率分別為 0.36、0.24、0.24、0.16。逐影格貪婪解碼選擇雙空白，產生空轉錄序列；然而三條對應 A 的路徑機率相加為 0.64，高於空轉錄序列的 0.36。動畫在訊號抵達時累加精確的路徑機率；中途的累積值尚不是正規化的轉錄機率分布。實際 CTC 訓練採前向－後向動態規劃，而非列舉路徑；解碼則可採用前綴束搜尋（prefix beam search）。

兩圖皆為人工教學算例，**不是語音辨識模型實測值**。在 MkDocs 網站可使用既有播放／暫停控制；窄螢幕可聚焦圖示後水平捲動。GitHub 與減少動態效果的使用者可閱讀靜態回退圖。原創圖示，CC BY-SA 4.0。

[^ctc]: Graves, A., Fernández, S., Gomez, F. & Schmidhuber, J. (2006). Connectionist temporal classification. ICML，第 3.1 與 4.1 節。https://doi.org/10.1145/1143844.1143891

## 台灣與華語語音

- 台語、客語、原住民族語辨識與合成：教育部、中研院、台大等計畫，以及「台灣媠聲」、意傳科技等
- 中英夾雜（code-switching）是在地語音辨識的難題
- Whisper 對繁中輸出常混入簡體，常需後處理或微調

## 與聽覺神經科學

- 耳蝸將聲音分解成頻率成分（類似短時傅立葉轉換），聽覺皮質具有音調拓撲（tonotopy）
- 以語音任務訓練的深度網路能預測人類聽覺皮質的反應，且呈現與皮質相似的階層（Kell et al., 2018；Li et al., 2023）
- 自監督語音模型（wav2vec 2.0）的表徵與人腦語音處理階層對齊（Millet et al., 2022）
- **雞尾酒會效應**：人類能在吵雜環境中專注於一個說話者，啟發了音源分離與注意力研究
- **語音神經義肢**：從運動皮質解碼想說的話，見 [腦機介面](../../../brain-mind/bci/index.md)

## 倫理風險

深偽語音詐騙、未經同意的聲音複製、配音員權益。對策：語音浮水印、活體偵測、法規（見 [法規與治理](../../../society/governance/index.md)）。

## 學習資源

- Hugging Face Audio Course
- [SpeechBrain](https://speechbrain.github.io/)、[ESPnet](https://github.com/espnet/espnet)、[NeMo](https://github.com/NVIDIA/NeMo)
- 李宏毅《Deep Learning for Human Language Processing》
