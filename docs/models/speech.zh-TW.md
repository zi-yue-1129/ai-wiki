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

## 台灣與華語語音

- 台語、客語、原住民族語辨識與合成：教育部、中研院、台大等計畫，以及「台灣媠聲」、意傳科技等
- 中英夾雜（code-switching）是在地語音辨識的難題
- Whisper 對繁中輸出常混入簡體，常需後處理或微調

## 與聽覺神經科學

- 耳蝸將聲音分解成頻率成分（類似短時傅立葉轉換），聽覺皮質具有音調拓撲（tonotopy）
- 以語音任務訓練的深度網路能預測人類聽覺皮質的反應，且呈現與皮質相似的階層（Kell et al., 2018；Li et al., 2023）
- 自監督語音模型（wav2vec 2.0）的表徵與人腦語音處理階層對齊（Millet et al., 2022）
- **雞尾酒會效應**：人類能在吵雜環境中專注於一個說話者，啟發了音源分離與注意力研究
- **語音神經義肢**：從運動皮質解碼想說的話，見 [腦機介面](../brain-mind/bci.md)

## 倫理風險

深偽語音詐騙、未經同意的聲音複製、配音員權益。對策：語音浮水印、活體偵測、法規（見 [法規與治理](../society/governance.md)）。

## 學習資源

- Hugging Face Audio Course
- [SpeechBrain](https://speechbrain.github.io/)、[ESPnet](https://github.com/espnet/espnet)、[NeMo](https://github.com/NVIDIA/NeMo)
- 李宏毅《Deep Learning for Human Language Processing》
