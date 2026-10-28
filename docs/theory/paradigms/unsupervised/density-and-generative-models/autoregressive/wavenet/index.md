---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/speech
tags:
  - generative models
  - sequence modelling
  - convolutional networks
aliases:
  - WaveNet
  - Dilated causal convolution
  - 波網
---

# WaveNet

WaveNet is an autoregressive model of raw audio. It predicts every sample of a waveform from all the samples before it, using stacks of dilated causal convolutions. Introduced by van den Oord and colleagues (2016), it was rated as more natural than the best parametric and concatenative speech systems of its time, and it is one of the landmark methods of the [Autoregressive generative models](../index.md) overview.

## Overview

Earlier statistical speech synthesis predicted acoustic features and passed them to a separate vocoder. WaveNet models the waveform itself, one sample at a time, at 16,000 or more samples per second, so it needs a receptive field of thousands of samples while remaining affordable to run.

The design is a one-dimensional relative of the [PixelCNN](../pixelcnn/index.md). Dilated convolutions enlarge the receptive field without pooling, so the output keeps the input's time resolution.

## Key concepts

- **Causal dilated convolution**: a convolution that sees only the present and past samples, and skips inputs with a fixed step (the dilation). Doubling the dilation at each layer makes the receptive field grow exponentially with depth.
- **Receptive field**: the span of past samples that can affect one prediction. It is about 240 ms in the text-to-speech model and about 300 ms in the multi-speaker model.
- **µ-law companding**: a logarithmic transform that lets 256 quantisation levels cover the waveform more usefully than linear levels would.
- **Global and local conditioning**: a speaker identity affects every time step, while linguistic features vary over time and are upsampled to the audio rate.

## How it works

The joint distribution of a waveform \(x = (x_1, \dots, x_T)\) is

\[
p(x) = \prod_{t=1}^{T} p\big(x_t \mid x_1, \dots, x_{t-1}\big)
\]

Each sample is companded and quantised to 256 values with

\[
f(x_t) = \operatorname{sign}(x_t)\,\frac{\ln(1 + \mu\lvert x_t\rvert)}{\ln(1 + \mu)}, \qquad \mu = 255
\]

and the network outputs a softmax over those values. Each residual block applies a gated activation, \(z = \tanh(W_f * x) \odot \sigma(W_g * x)\), where \(*\) is a dilated causal convolution. Residual and skip connections carry the signal through the stack.

The dilation schedule is the key choice. The dilation doubles at each layer, 1, 2, 4, up to 512, and then the cycle repeats. One such cycle covers 1,024 samples, about 64 ms at 16 kHz. Training maximises the likelihood of the quantised samples with all time steps computed in parallel. Generation draws one sample, feeds it back, and repeats for each output sample.

## Results

- **Text-to-speech.** On a five-point naturalness scale, WaveNet conditioned on linguistic features and pitch scored above 4.0 for both English and Mandarin, above the LSTM-based parametric and concatenative baselines. The gap to natural speech shrank by 51% in English and 69% in Mandarin.
- **Multiple speakers.** One model conditioned on a speaker code produced 109 voices from about 44 hours of VCTK data. Adding speakers improved validation performance.

## Limitations

- **Sampling cost.** Generating one second of 16 kHz audio takes 16,000 sequential steps. [Parallel WaveNet](https://arxiv.org/abs/1711.10433) distils the model into a much faster feed-forward flow.
- **Limited context.** The receptive field spans a few hundred milliseconds. Unconditional speech lacks long-range coherence, because the model can only remember the last two or three phonemes it produced.
- **Dependence on inputs.** Linguistic features alone sometimes gave wrong stress. Adding a lower-rate fundamental-frequency input removed the problem in the paper's tests.

## Open questions

- **Long-range structure.** Music and long speech need coherence over seconds or minutes. Models that first generate discrete semantic tokens and then fill in acoustic detail, such as [AudioLM](https://arxiv.org/abs/2209.03143), are one response.
- **Speed and quality.** Parallel WaveNet trains a fast model from a slow one. Whether a fast model can match the original without a teacher is less clear.

## Connections

- **Image counterpart.** [PixelCNN](../pixelcnn/index.md) introduced the gated, masked design that WaveNet adapts to one dimension.
- **Speech.** Later systems are surveyed in [Speech and audio](../../../../../models/speech/index.md).
- **Discrete codes.** A WaveNet prior over the codes of a [VQ-VAE](../../vae/vq-vae/index.md) is the audio version of the image setup described there.

## Applications

- **Speech synthesis.** Parallel WaveNet is deployed in Google Assistant, serving several English and Japanese voices (van den Oord et al., 2017).
- **Music.** Jukebox compresses audio with a multi-scale VQ-VAE and models the codes autoregressively, producing songs that stay coherent for minutes (Dhariwal et al., 2020).
- **Speech codecs.** VALL-E treats speech synthesis as language modelling over codec tokens and can clone a voice from a three-second prompt (Wang et al., 2023).

## References

### Seminal papers

- van den Oord, A. et al. (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv. https://arxiv.org/abs/1609.03499 — The paper itself: dilated causal convolutions over raw waveforms, with speech and music experiments.
- van den Oord, A. et al. (2017). *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*. arXiv. https://arxiv.org/abs/1711.10433 — Distils WaveNet into a feed-forward flow, more than 20 times faster than real time.
- Yu, F. & Koltun, V. (2016). *Multi-Scale Context Aggregation by Dilated Convolutions*. arXiv. https://arxiv.org/abs/1511.07122 — Uses dilated convolutions to aggregate wide context without losing resolution.
- Dhariwal, P. et al. (2020). *Jukebox: A Generative Model for Music*. arXiv. https://arxiv.org/abs/2005.00341 — Models music codes from a multi-scale VQ-VAE with autoregressive Transformers.
- Borsos, Z. et al. (2022). *AudioLM: a Language Modeling Approach to Audio Generation*. arXiv. https://arxiv.org/abs/2209.03143 — Casts audio generation as language modelling over discrete tokens.
- Wang, C. et al. (2023). *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers*. arXiv. https://arxiv.org/abs/2301.02111 — Treats text-to-speech as language modelling over codec tokens.

### Surveys and textbooks

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — Places autoregressive audio models among other deep generative families.
