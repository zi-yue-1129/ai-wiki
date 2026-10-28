---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/visual-perception
tags:
- neuroscience
- methods
aliases:
  - Logothetis 2001
  - Simultaneous fMRI and electrophysiology
  - Basis of the fMRI signal
---

# Simultaneous fMRI and Electrophysiology (Logothetis et al. 2001)

Logothetis et al. (2001) recorded electrical activity in monkey cortex while measuring fMRI in the same animal, so that the BOLD signal and the neural signal could be compared directly. The paper asked which neural measure the BOLD response follows, spiking output or the synaptic input that drives it. Its central finding, from the summary used here, is that the BOLD signal relates more closely to local field potentials, which mainly reflect synaptic activity, than to the spiking of individual neurons.

This page is part of [Neuroimaging and Recording Methods](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

fMRI is widely used, but its interpretation depends on which neural signal it reflects. If the BOLD response followed spiking, an fMRI map would show where the output of neurons changed. If it followed synaptic input, the map would show where incoming signals and local processing changed, which is a different quantity. The question was which one it is.

## The approach

The authors combined fMRI with electrode recordings in the same monkeys, during visual stimulation. They recorded the BOLD response alongside local field potentials and the spiking of neurons near each electrode, and then compared how well each neural measure predicted the BOLD signal.

The steps were:

1. Present visual stimuli to anaesthetised monkeys while recording fMRI.
2. Record local field potentials and single-unit spiking at the same sites.
3. Relate the BOLD response to each neural measure, and compare which predicts it better.
4. Test the relation across stimulus strengths, to check that it holds beyond one condition.

Step 3 is the key comparison. The answer depends on the fact that local field potentials and spiking can diverge, so the two measures give different predictions.

## Results

The summary reports that the BOLD signal tracks local field potentials more closely than spiking, which suggests the fMRI response reflects the input and local processing around a site. These results are qualitative in the summary used for this page. Check the full paper before quoting specific values.

## Limitations

- The recordings come from anaesthetised monkeys, so the generality to awake humans needs separate evidence.
- The local field potential and spiking are measured near each electrode, which is a small sample of the region fMRI covers.
- The relation may differ across brain areas, tasks and levels of activity.

## Connections

- **The BOLD method**: the underlying measurement of blood oxygenation is on [BOLD fMRI](../bold-fmri/index.md), which relies on the link this paper tests.
- **Visual cortex**: the single-neuron recording tradition behind the spiking measure is summarised on [Perception and the Visual System](../../visual-perception/index.md).
- **Language**: the same question about what fMRI reflects arises in sentence studies, where ECoG offers a faster comparison, on [Language in the Brain](../../language-in-brain/index.md).
- **Neuroscience background**: the difference between spikes and synaptic activity is covered on [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **Does the coupling hold in humans and in awake animals?** The result comes from anaesthetised monkeys, and the coupling may change with state.
- **How does the coupling vary across regions?** Different areas may have different ratios of synaptic input to output, which would change how fMRI maps should be read.

## References

### Seminal papers

- Logothetis, N. K., Pauls, J., Augath, M., Trinath, T. & Oeltermann, A. (2001). Neurophysiological investigation of the basis of the fMRI signal. *Nature*. https://doi.org/10.1038/35084005 — Relates the BOLD signal to local field potentials and spiking recorded in the same animals.
- Ogawa, S., Lee, T.-M., Kay, A. R. & Tank, D. W. (1990). Brain magnetic resonance imaging with contrast dependent on blood oxygenation. *Proceedings of the National Academy of Sciences*. https://pmc.ncbi.nlm.nih.gov/articles/PMC55275 — The blood-oxygenation contrast that the BOLD signal measures.
- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — The single-neuron recording tradition on which the spiking measure rests. (Reference reused from the Neuroscience Basics page; not re-checked for this page.)

### Articles and primary research

- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — A fMRI method whose interpretation depends on the coupling this paper tests.
- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — Uses electrocorticography, a direct electrical measure, to compare with the slower blood-based signal.
