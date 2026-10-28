---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/cognitive-science
- brain-mind/neuroscience
- brain-mind/neuroai
- theory/models/llm
- theory/models/transformer
tags:
- neuroscience
- language
aliases:
  - 大腦中的語言
  - 語言神經科學
  - Language in the Brain
  - Language Neuroscience
---

# Language in the Brain

Language is the human ability that large language models most resemble, so it is the domain where the comparison between brains and AI is most direct. Neuroscience asks where and how the brain processes speech and text, and AI researchers now ask which model features predict the brain's responses to them.

## Overview

Understanding a sentence requires several steps in quick succession: hearing or reading the words, recognising them, combining them into a structure, working out the meaning in context, and then planning a reply. Each step can be disrupted separately after brain injury, which is why aphasia has been a source of evidence about the brain's language system since the 19th century. [Cognitive Science](../cognitive-science/index.md) covers the broader psychology of language; this page focuses on the neural machinery and on the recent work that compares it with language models.

## Key concepts

- **Broca's and Wernicke's areas**: classical regions in the left frontal lobe (speech production and syntax) and left temporal lobe (comprehension). Their roles are now understood as part of a wider network rather than as isolated centres.
- **Dual-stream model**: a view in which speech is processed along a ventral stream that maps sound to meaning, and a dorsal stream that maps sound to articulation (Hickok & Poeppel, 2007).
- **Language network**: a set of left-lateralised frontal and temporal regions that respond to language. Fedorenko et al. (2010) introduced the individual-level localiser used to find it in each person.
- **Predictive processing**: the brain anticipates upcoming words, and the mismatch between prediction and input is the signal that drives comprehension.
- **Contextual embedding**: a representation of a word that depends on the words around it. Transformer language models produce such embeddings, and they are the basis for most brain-model comparisons.

## How it works

Speech is a continuous acoustic signal, and the brain must segment it into words and phonemes before anything else can happen. The dual-stream model describes where this processing happens. Hickok and Poeppel (2007) propose that a bilateral ventral stream supports comprehension, while a left-dominant dorsal stream links acoustic speech to frontal articulatory networks.

```mermaid
flowchart LR
  S[Speech sound] --> STG[Superior temporal cortex<br/>sound to phonemes]
  STG --> V[Ventral stream<br/>sound to meaning]
  STG --> D[Dorsal stream<br/>sound to articulation]
  V --> MTG[Temporal lobe<br/>word and sentence meaning]
  D --> IFG[Left frontal cortex<br/>planning and syntax]
```

Two findings have shaped the modern picture. First, the language network can be identified in each person's fMRI data by contrasting sentences with non-word strings. Fedorenko et al. (2010) developed this individual-level localiser. Second, a person can lose much of their language ability and still reason and solve problems. Fedorenko and Varley (2016) argue from neuroimaging and patient studies that language and thought are separable, so models of thinking should not assume that language is the thing doing the thinking.

## Key methods

### Dual-stream model of speech processing (Hickok & Poeppel, 2007)

- **Problem:** The speech neuroanatomy field had struggled to map speech processing, partly because studies often ignored how the task being performed shapes brain activity.
- **Core idea:** Separate speech processing into two streams. A largely bilateral ventral stream supports comprehension, and a strongly left-dominant dorsal stream links acoustic speech signals to frontal articulatory networks.
- **Equation or algorithm:** Not a computational model. The steps are:
  1. Take the acoustic signal and map it onto phonological representations in the superior temporal cortex.
  2. Route these representations along the ventral stream to lexical and sentence-level meaning.
  3. Route them along the dorsal stream to frontal articulatory networks for repetition and speech production.
  4. Use task demands to predict which stream is active in a given experiment.
- **Results:** The paper is a review and reports no new numbers. Its claim is that the proposed streams organise the existing lesion and imaging evidence.
- **Limitations:** The model is a verbal framework, not a formal one, and the exact division between the streams is still debated. The paper predates much of the work on language networks and language models that follows.

### Language models predict brain responses to sentences (Schrimpf et al., 2021)

- **Problem:** Which computational features of a language model explain human brain responses to sentences, and do these features track the models' ability to predict the next word?
- **Core idea:** Score many transformer language models on how well their internal representations predict human responses to the same sentences, recorded with functional MRI and electrocorticography (ECoG). Then check which model properties, such as accuracy on next-word prediction, correlate with the brain fit.
- **Equation or algorithm:**
  1. Present the same sentences to human participants and to a set of transformer language models.
  2. Record brain responses with fMRI and ECoG, and extract each model's internal activations.
  3. Fit a regression from model activations to the brain responses, and measure how much of the explainable variance it accounts for.
  4. Relate each model's brain fit to its next-word prediction accuracy and to its scores on other language tasks.
- **Results:** The most powerful models predicted "nearly 100% of explainable variance" in neural responses to sentences, across datasets and both imaging modalities. Brain fit and behavioural fit correlated strongly with next-word prediction accuracy, but not with other language tasks.
- **Limitations:** Explainable variance depends on the noise ceiling of each dataset, so the figure is relative to that ceiling. The result shows a correlation between prediction and brain fit, not a mechanism. Model architecture also affected the fit, which the authors note as a separate factor.

### Contextual embeddings and the next-word prediction loop (Goldstein et al., 2022)

- **Problem:** Do autoregressive language models and the human brain share computational principles during real listening, or are the similarities only at the level of final predictions?
- **Core idea:** Record electrocorticography from people listening to a 30-minute podcast, and compare the neural signals with GPT-2 on three properties: continuous next-word prediction before a word is heard, a surprise signal after it is heard, and contextual embeddings for each word.
- **Equation or algorithm:**
  1. Collect word-level predictions from human participants, and compare them with GPT-2's predictions for the same words.
  2. Measure how well each electrode's signal encodes GPT-2 embeddings and GloVe embeddings.
  3. Test whether neural activity before word onset predicts the upcoming word, and whether post-onset activity tracks surprise.
  4. Decode word identity from neural signals and compare the decoding performance across embedding types.
- **Results:** Human predictability and GPT-2 predictions correlated at r = 0.79, and the match improved as the context grew, from r = 0.46 at two words to about 0.79 at roughly 100 words. Contextual GPT-2 embeddings were encoded at 208 left-hemisphere electrodes and 34 right-hemisphere electrodes, with 71 of the left-hemisphere sites not found with GloVe. Decoding with GPT-2 embeddings gave a mean ROC-AUC of 0.74, against 0.68 for GloVe. Post-onset activity peaked around 400 ms after onset for unpredicted words.
- **Limitations:** The study has nine participants, so the individual-level generality is limited. Electrocorticography is recorded only where clinical needs place electrodes, which constrains which regions can be studied. The authors argue for a biologically feasible framework, not a proof that the brain implements a transformer.

## Connections

- **Cognitive science**: the psychology of language acquisition, parsing and pragmatics is in [Cognitive Science](../cognitive-science/index.md), which this page builds on.
- **Neuroscience**: cortical regions, recording methods and the auditory pathway are summarised in [Neuroscience Basics](../neuroscience/index.md).
- **NeuroAI**: using language models as models of the language cortex is discussed on [NeuroAI](../neuroai/index.md).
- **Language models**: the model families compared with the brain are on [Large Language Models](../../theory/models/llm/index.md) and [Transformer](../../theory/models/transformer/index.md).
- **Brain-computer interfaces**: decoding language from neural activity is covered in [Brain-Computer Interfaces](../bci/index.md).

## Applications

- **Presurgical language mapping**: fMRI and ECoG are used to locate language regions before neurosurgery, to lower the risk of losing speech.
- **Aphasia assessment**: language tests and imaging help clinicians classify the type of language impairment after stroke, and guide rehabilitation.
- **Speech decoding**: brain signals decoded into text or speech for people who cannot speak. See [Brain-Computer Interfaces](../bci/index.md).

## Open questions

- **Are the similarities mechanistic?** Models and brains predict the same words, but whether the internal computations match is unresolved. Correlation of representations does not establish mechanism.
- **Does language ability imply thinking?** Patient evidence suggests the two can come apart, but the results depend on how each is measured.
- **How far does brain fit depend on the benchmark?** Scores are relative to noise ceilings and datasets, so comparisons across studies need care.
- **Do models without language training show the same fit?** The role of training data versus architecture is still being tested.

## References

### Seminal papers

- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — Proposes the dual-stream model of speech processing, with a ventral stream for comprehension and a dorsal stream for articulation.
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — The individual-level localiser that identifies each person's language network.

### Surveys and reviews

- Fedorenko, E. & Varley, R. (2016). Language and thought are not the same thing: evidence from neuroimaging and neurological patients. *Annals of the New York Academy of Sciences*. https://discovery.ucl.ac.uk/id/eprint/1489434/ — Reviews neuroimaging and patient evidence that language and thought are separable.

### Articles and primary research

- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that the best transformer models predict nearly all explainable variance in neural responses to sentences.
- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — Compares human ECoG responses with GPT-2 on prediction, surprise and contextual embeddings during a podcast.
- Caucheteux, C. & King, J.-R. (2022). Brains and algorithms partially converge in natural language processing. *Communications Biology*. https://doi.org/10.1038/s42003-022-03036-1 — Compares language-model representations with brain recordings, and reports partial convergence between the two.
