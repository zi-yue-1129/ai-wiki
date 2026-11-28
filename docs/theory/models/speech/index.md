---
related:
- brain-mind/bci
- theory/models/multimodal
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

## Frame alignments in speech recognition

Connectionist temporal classification (CTC) assigns probabilities to transcripts without requiring a label for every encoder frame. A path uses the label alphabet plus a special blank symbol (∅); the collapse map first merges consecutive repeated symbols, then removes blanks.[^ctc]

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-collapse-scan-still.svg" data-motion-src="../../../assets/concept-animations/ctc-collapse-scan-motion.svg" data-still-src="../../../assets/concept-animations/ctc-collapse-scan-still.svg" alt="The frame path A, A, blank, A, B is scanned from left to right. Only frames one, four and five emit labels, giving AAB." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-collapse-scan-still.svg)

The moving marker carries emitted labels into the transcript. The second frame repeats A, so it emits nothing; the blank at frame three separates the next A from the previous run. Removing blanks before merging repeats would incorrectly produce AB. The blank is not a word separator or a literal output character.

### Why greedy decoding can disagree with the best transcript

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-path-mass-still.svg" data-motion-src="../../../assets/concept-animations/ctc-path-mass-motion.svg" data-still-src="../../../assets/concept-animations/ctc-path-mass-still.svg" alt="Four two-frame paths route their probability masses to two collapsed transcripts. The greedy blank-blank path has mass 36 percent; the three paths for A sum to 64 percent." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-path-mass-still.svg)

For two frames, let each frame give blank probability 0.6 and label A probability 0.4. Given the input, CTC multiplies frame probabilities along a path and sums over all paths that collapse to the same transcript.[^ctc] The four paths have masses 0.36, 0.24, 0.24 and 0.16. Greedy framewise decoding selects blank-blank, hence an empty transcript. The three paths for A instead sum to 0.64, exceeding the empty transcript's 0.36. The animation accumulates exact path masses upon arrival; its intermediate sums are not a normalized transcript distribution. Practical CTC training uses forward-backward dynamic programming rather than enumerating paths, and decoding may use prefix beam search.

Both are constructed teaching examples, **not recognizer measurements**. On MkDocs, use the existing Play/Pause control and focus the diagram to scroll horizontally on narrow screens. GitHub and reduced-motion users have a static fallback. Original CC BY-SA 4.0 artwork.

### Forward recursion: sum compatible alignments without enumeration

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-forward-lattice-still.svg" data-motion-src="../../../assets/concept-animations/ctc-forward-lattice-motion.svg" data-still-src="../../../assets/concept-animations/ctc-forward-lattice-still.svg" alt="Three forward-lattice columns propagate mass over the leading blank, A and trailing blank states. The terminal A and trailing blank masses sum to 0.688." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-forward-lattice-still.svg)

For target A, expand the state sequence to (blank, A, blank). With each frame assigning probabilities 0.6 to blank and 0.4 to A, initialize the forward masses to (0.6, 0.4, 0). In this example a transition can stay in its state or advance by one. With zero-based state indices, each new mass is[^ctc]

$
\alpha_t(s)=p_t(l'_s)\big(\alpha_{t-1}(s)+\alpha_{t-1}(s-1)\big).
$

Out-of-range states contribute zero. For example, at frame three the A state receives $(0.36+0.4)0.4=0.304$; the trailing blank receives $(0.4+0.24)0.6=0.384$. The leading blank represents an unfinished alignment, so it does not contribute to the final target probability: $P(A\mid x)=0.304+0.384=0.688$. The moving dots indicate predecessor contributions, not equally weighted paths; numerical cells update after the contributions arrive. These unpruned prefix masses need not sum to one because paths incompatible with the target are excluded.

### Repeated labels and the skip transition

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-repeat-skip-still.svg" data-motion-src="../../../assets/concept-animations/ctc-repeat-skip-motion.svg" data-still-src="../../../assets/concept-animations/ctc-repeat-skip-still.svg" alt="The AB target allows a direct transition from A to B across the intervening blank. The AA target blocks that skip, so a third frame is needed to emit the second A." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-repeat-skip-still.svg)

For longer targets, the forward recursion also permits advancing by two states when the destination is nonblank and differs from the label two states earlier. The additional predecessor term is then $\alpha_{t-1}(s-2)$.[^ctc] The diagram isolates this local transition, omitting self-loops and the leading and trailing blanks. AB can be aligned in two frames, but AA needs at least three (A, blank, A); skipping the blank would merge both A labels. For a nonempty target of length $U$, the minimum feasible frame count is $U$ plus the number of adjacent equal label pairs. This is a feasibility condition, not a decoding heuristic.

Both animations use constructed examples rather than model measurements. Use the site's Play/Pause control and focus the diagram to scroll on narrow screens. Static previews preserve the final states. Original CC BY-SA 4.0 artwork.

### Forward-backward alignment posterior

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-alignment-posterior-still.svg" data-motion-src="../../../assets/concept-animations/ctc-alignment-posterior-motion.svg" data-still-src="../../../assets/concept-animations/ctc-alignment-posterior-still.svg" alt="At frame two, three forward masses multiply their suffix probabilities. The two blank state masses combine to 41.86 percent; A has posterior 58.14 percent." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-alignment-posterior-still.svg)

Training needs the distribution over alignments compatible with the target, not merely the framewise prediction. Let $\beta^+_t(s)$ be the suffix probability after frame $t$ given state $s$ (excluding the current emission). Then $\alpha_t(s)\beta^+_t(s)$ is the joint mass of compatible paths passing through that state. This convention excludes the duplicated current emission in the original paper's backward variable.[^ctc]

For the preceding three-frame target A example, frame two has forward masses $(0.36,0.40,0.24)$ and suffix probabilities $(0.4,1,0.6)$. Their products are $(0.144,0.400,0.144)$, summing to $P(A\mid x)=0.688$. Normalize by this total and sum over states emitting the same symbol: the posterior occupancy of A is $0.400/0.688\approx0.5814$ and blank is $0.288/0.688\approx0.4186$. The original frame probabilities were 0.4 and 0.6 respectively. For softmax logits, the gradient of the negative log-likelihood is frame probability minus posterior occupancy, so the A logit gradient here is about −0.1814. This is a soft alignment signal, not a hard frame label.

### Prefix decoding: repeated emissions have two destinations

<div class="concept-motion-scroll" style="overflow-x:auto;max-width:100%" tabindex="0">
<img data-source-asset-urls src="../../../assets/concept-animations/ctc-prefix-repeat-still.svg" data-motion-src="../../../assets/concept-animations/ctc-prefix-repeat-motion.svg" data-still-src="../../../assets/concept-animations/ctc-prefix-repeat-still.svg" alt="The blank-ending mass 0.24 for prefix A sends 0.096 to AA when emitting A; the nonblank-ending mass 0.40 sends 0.160 to the unchanged A." style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub-readable static preview](../../../assets/concept-animations/ctc-prefix-repeat-still.svg)

Prefix search groups paths by collapsed prefix but must distinguish their blank-ending and nonblank-ending masses. For the two-frame prefix A, these are 0.24 (A, blank) and 0.40 (blank, A or A, A). Appending A with probability 0.4 adds 0.096 to prefix AA from the blank-ending paths, but 0.160 to unchanged prefix A from the nonblank-ending paths. The same emitted label therefore has two distinct destinations. The diagram isolates these contributions, not the complete beam update: appending blank and extending the empty prefix also contribute to the next frame. Without pruning, the full third-frame masses are empty 0.216, A 0.688 and AA 0.096. Beam search merges contributions before ranking and pruning; the finite beam need not preserve all probability mass.[^ctc-prefix]

These are constructed examples, not recognizer measurements. On MkDocs use Play/Pause; focus the diagram to scroll on narrow screens. Static fallbacks show the final states. Original CC BY-SA 4.0 artwork.

[^ctc-prefix]: Hannun, A. Y., Maas, A. L., Jurafsky, D. & Ng, A. Y. (2014). First-pass large vocabulary continuous speech recognition using bi-directional recurrent DNNs. https://arxiv.org/abs/1408.2873

[^ctc]: Graves, A., Fernández, S., Gomez, F. & Schmidhuber, J. (2006). Connectionist temporal classification. ICML, section 3.1 and 4.1. https://doi.org/10.1145/1143844.1143891

## Low-resource and code-switched speech

Most languages and dialects lack large transcribed corpora. Code-switching (mixing languages within a sentence) and regional languages (e.g. Taiwanese Hokkien, Hakka and Indigenous languages in Taiwan) are active research areas; Whisper-style models often need fine-tuning and post-processing for them.

## Auditory neuroscience

- The cochlea decomposes sound into frequencies (like a short-time Fourier transform); auditory cortex is **tonotopically** organised
- Deep networks trained on speech and music tasks predict human auditory-cortex responses and show a cortex-like hierarchy (Kell et al., 2018; Tuckute et al., 2023)
- Self-supervised speech models (wav2vec 2.0) align with the brain's speech-processing hierarchy (Millet et al., 2022)
- The **cocktail-party effect** — attending to one voice in a crowd — inspired source separation and attention research
- **Speech neuroprostheses** decode intended speech from motor cortex — see [Brain-Computer Interfaces](../../../brain-mind/bci/index.md)

## Ethical risks

Deepfake voice scams, cloning without consent, voice actors' rights. Countermeasures: audio watermarking, liveness detection, regulation (see [Law, Policy & Governance](../../../society/governance/index.md)).

## References

- Hannun, A. Y. et al. (2014). *First-Pass Large Vocabulary Continuous Speech Recognition using Bi-Directional Recurrent DNNs*. https://arxiv.org/abs/1408.2873 — Modified prefix-search decoding with separate blank and nonblank scores.
- Graves, A. et al. (2006). Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks. *Proceedings of ICML 2006*. https://doi.org/10.1145/1143844.1143891 — Trains a recurrent network to align unsegmented audio with label sequences, the basis of many end-to-end recognisers.
- Hinton, G. et al. (2012). Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2012.2205597 — Reviews how deep networks replaced Gaussian mixture models in acoustic modelling, with large error reductions.
- Chan, W. et al. (2015). *Listen, Attend and Spell*. arXiv:1508.01211. https://arxiv.org/abs/1508.01211 — End-to-end attention model that transcribes speech directly into characters.
- Baevski, A. et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations. *NeurIPS 2020*. https://arxiv.org/abs/2006.11477 — Learns speech representations from unlabelled audio and then fine-tunes them with little labelled data, which matters for low-resource languages.
- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv:2212.04356. https://arxiv.org/abs/2212.04356 — Whisper: trains on large amounts of weakly labelled multilingual audio for robust transcription and translation.

## Further learning

- [SpeechBrain](https://speechbrain.github.io/), [ESPnet](https://github.com/espnet/espnet) and [NeMo](https://github.com/NVIDIA/NeMo) — open-source speech toolkits.
- [Hugging Face Audio Course](https://huggingface.co/learn/audio-course) — hands-on course on audio models.
