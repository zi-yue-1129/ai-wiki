---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/cognitive-science
- brain-mind/neuroscience
tags:
- neuroscience
- language
aliases:
  - Hickok & Poeppel 2007
  - Dual-stream model
  - Dual Stream Model of Speech
---

# Dual-Stream Model of Speech Processing (Hickok & Poeppel 2007)

Hickok and Poeppel (2007) proposed that speech processing in the cortex runs along two streams. A largely bilateral ventral stream maps sound to meaning and supports comprehension, while a left-dominant dorsal stream maps sound to articulation. The framework organised a large body of lesion and imaging evidence, and it is still the reference point for later work on where language is processed.

This page is part of [Language in the Brain](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

By the mid-2000s, the neuroanatomy of speech had proved hard to map. Studies often reported different regions for the same task, and many ignored how the task demands shaped the activity that was recorded. A model was needed that could tell which regions should respond to which aspects of speech, and when.

## The approach

The paper is a theoretical review rather than an experiment. It takes the existing lesion, imaging and clinical evidence and proposes a division of labour between two routes.

The steps of the proposed model are:

1. Map the acoustic signal onto phonological representations in the superior temporal cortex.
2. Route these representations along the ventral stream to lexical and sentence-level meaning.
3. Route them along the dorsal stream to frontal articulatory networks, used for repetition and speech production.
4. Use task demands to predict which stream is active in a given experiment.

Step 4 is what makes the model testable. Changing the task should change which stream responds.

## Results

The paper reports no new numbers. Its claim is that the two streams organise the existing evidence, including lesion and imaging findings, into one framework.

## Limitations

- The model is a verbal framework, not a formal or computational one. It predicts which regions should respond, but it does not specify the transformations that happen within them.
- The exact boundary between the streams is still debated, and later work has refined the account.
- The paper predates much of the work on individual-level language networks and on language models that follows.

## Connections

- **Language network**: the individual-level method that later work uses to find language regions is in [Fedorenko et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923). The broader case for separating language from thought is in [Fedorenko and Varley 2016](https://discovery.ucl.ac.uk/id/eprint/1489434/).
- **Language models**: the comparison of brain responses with transformer models that followed is on [Schrimpf et al. 2021](../schrimpf-2021/index.md) and [Goldstein et al. 2022](../goldstein-2022/index.md).
- **Cognitive science**: the psychology of language that this model sits beside is in [Cognitive Science](../../cognitive-science/index.md).
- **Neuroscience background**: the cortical regions and recording methods are in [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **Where exactly is the boundary?** The ventral and dorsal streams are defined by function, and the anatomical split between them is less clear than the diagram suggests.
- **How do the streams interact?** The model describes two routes, but the feedback and timing between them is open.

## References

### Seminal papers

- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — Proposes the dual-stream model of speech processing, with a ventral stream for comprehension and a dorsal stream for articulation.
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — The individual-level localiser that identifies each person's language network.

### Surveys and reviews

- Fedorenko, E. & Varley, R. (2016). Language and thought are not the same thing: evidence from neuroimaging and neurological patients. *Annals of the New York Academy of Sciences*. https://discovery.ucl.ac.uk/id/eprint/1489434/ — Reviews neuroimaging and patient evidence that language and thought are separable.

### Articles and primary research

- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that the best transformer models predict nearly all explainable variance in neural responses to sentences.
