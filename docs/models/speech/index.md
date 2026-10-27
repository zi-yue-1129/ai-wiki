---
related:
- brain-mind/bci
- models/multimodal
---

# Speech & Audio

## Tasks

| Task | Description | Models / tools |
|---|---|---|
| Automatic speech recognition (ASR) | Speech → text | Whisper, wav2vec 2.0, Conformer, Paraformer |
| Text-to-speech (TTS) | Text → speech | Tacotron, FastSpeech, VITS, neural-codec language models (VALL-E style) |
| Voice conversion / cloning | Change speaker identity | RVC, zero-shot TTS |
| Speaker recognition and diarisation | Who spoke when | pyannote |
| Speech enhancement | Denoising, dereverberation | Demucs and others |
| Music generation | Text or melody → music | MusicLM, MusicGen, Suno, Udio, etc. |
| Source separation | Isolate vocals, instruments | Demucs |
| Sound event detection | Gunshots, glass breaking, birdsong | PANNs, BirdNET |
| Spoken dialogue models | Real-time end-to-end voice conversation | GPT-4o-style omni models, Moshi |

## Key techniques

- **Features**: mel spectrograms, MFCCs — or learn directly from waveforms (wav2vec)
- **Neural audio codecs**: EnCodec and SoundStream compress audio into discrete tokens so language models can "speak" and "compose"
- **End-to-end speech LLMs**: process speech tokens directly, preserving prosody and emotion with lower latency
- **Vocoders**: WaveNet → HiFi-GAN → codec decoders

## Low-resource and code-switched speech

Most languages and dialects lack large transcribed corpora. Code-switching (mixing languages within a sentence) and regional languages (e.g. Taiwanese Hokkien, Hakka and Indigenous languages in Taiwan) are active research areas; Whisper-style models often need fine-tuning and post-processing for them.

## Auditory neuroscience

- The cochlea decomposes sound into frequencies (like a short-time Fourier transform); auditory cortex is **tonotopically** organised
- Deep networks trained on speech and music tasks predict human auditory-cortex responses and show a cortex-like hierarchy (Kell et al., 2018; Tuckute et al., 2023)
- Self-supervised speech models (wav2vec 2.0) align with the brain's speech-processing hierarchy (Millet et al., 2022)
- The **cocktail-party effect** — attending to one voice in a crowd — inspired source separation and attention research
- **Speech neuroprostheses** decode intended speech from motor cortex — see [Brain-Computer Interfaces](../../brain-mind/bci/index.md)

## Ethical risks

Deepfake voice scams, cloning without consent, voice actors' rights. Countermeasures: audio watermarking, liveness detection, regulation (see [Law, Policy & Governance](../../society/governance/index.md)).

## Resources

- Hugging Face Audio Course
- [SpeechBrain](https://speechbrain.github.io/), [ESPnet](https://github.com/espnet/espnet), [NeMo](https://github.com/NVIDIA/NeMo)
- Hung-yi Lee, *Deep Learning for Human Language Processing* (NTU)
