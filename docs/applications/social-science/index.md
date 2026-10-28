---
related:
- brain-mind/psychology
- society/economics
- society/ethics
- theory/models/agents
aliases:
  - 社會科學
  - 人文學
---

# Social Sciences & Humanities

## Computational social science

- **Text as data**: topic models, embeddings and LLMs to measure ideology, sentiment, framing and policy positions in speeches, news and social media
- **Network analysis** of social ties, diffusion of information and misinformation
- **Digital trace data**: mobility, online behaviour, administrative records
- **Prediction vs explanation**: the Fragile Families Challenge showed that even with rich data and ML, life outcomes were barely predictable (Salganik et al., 2020, *PNAS*) — a sobering lesson for predictive policy tools
- **LLMs as annotators**: zero-shot LLM coding can match or exceed crowdworkers for many tasks (Gilardi et al., 2023), but must be validated per task and can encode biases

## Simulating people and societies

- **Silicon samples**: conditioning LLMs on demographic backstories to approximate survey responses (Argyle et al., 2023); results vary by population and question, and under-represent variance and minority views
- **Agent-based models with LLM agents**: Generative Agents (Park et al., 2023) and later simulations of 1,000 real people's attitudes from interviews (Park et al., 2024)
- **Uses**: piloting surveys and experiments, exploring hypotheses; **not** a substitute for real participants

## Economics

- Causal ML for treatment effects (double/debiased ML, causal forests)
- Nowcasting with satellite imagery and alternative data (e.g. poverty mapping from night lights and daytime imagery, Jean et al., 2016)
- Economics *of* AI: see [Economics & Work](../../society/economics/index.md)

## Political science and public policy

- Measuring polarisation, propaganda and censorship
- Persuasion research: personalised AI dialogue reduced belief in conspiracy theories in a large study (Costello, Pennycook & Rand, 2024)
- Algorithmic decision making in government can cause serious harm when errors go unchecked

## Digital humanities

- OCR and handwritten text recognition for archives (Transkribus)
- Deciphering and restoring ancient texts: Ithaca for Greek inscriptions (Assael et al., 2022)
- Stylometry and authorship attribution
- Cultural analytics over millions of books, images and films
- Translation and revitalisation of endangered languages

## Methodological cautions

- Validate measurement against human-coded gold standards
- Beware of training-data contamination when using LLMs on well-known texts
- Report prompts and model versions for reproducibility; closed models change silently
- Consider ethics of scraping and consent

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture behind the text-as-data and annotation tools described above (Vaswani et al., 2017).
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): instruction-following models used as zero-shot annotators (Gilardi et al., 2023).
- [Agents](../../theory/models/agents/index.md): LLM agents used to simulate people and societies (Park et al., 2023; Park et al., 2024).

## References

### Seminal papers

- Salganik et al. (2020). Measuring the predictability of life outcomes with a scientific mass collaboration. *PNAS*. https://doi.org/10.1073/pnas.1915006117 — The Fragile Families Challenge, showing the limits of predicting life outcomes.
- Gilardi et al. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *PNAS*. https://doi.org/10.1073/pnas.2305016120 — Compares zero-shot ChatGPT annotations with crowd workers.
- Argyle et al. (2023). Out of One, Many: Using Language Models to Simulate Human Samples. *Political Analysis*. https://doi.org/10.1017/pan.2023.2 — Conditions language models on demographic backstories to simulate survey samples.
- Park et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — LLM agents in a simulated town that plan and remember.
- Park et al. (2024). LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals. arXiv. https://arxiv.org/abs/2411.10109 — Simulates individuals from interview transcripts and checks them against their survey responses.
- Jean et al. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*. https://doi.org/10.1126/science.aaf7894 — Predicts poverty from satellite imagery with machine learning.
- Costello, Pennycook & Rand (2024). Durably reducing conspiracy beliefs through dialogues with AI. *Science*. https://doi.org/10.1126/science.adq1814 — Dialogues with an AI durably reduced conspiracy beliefs in a large experiment.
- Assael et al. (2022). Restoring and attributing ancient texts using deep neural networks. *Nature*. https://doi.org/10.1038/s41586-022-04448-z — Ithaca, a neural network for restoring and dating Greek inscriptions.

### Surveys and textbooks

- Ziems et al. (2024). Can Large Language Models Transform Computational Social Science? *Computational Linguistics*. https://doi.org/10.1162/coli_a_00502 — Review of how large language models can be used in computational social science.
