---
related:
- brain-mind/psychology
- society/economics
- society/ethics
- theory/models/agents
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
- Persuasion research: AI-generated messages can shift attitudes comparably to human-written ones; personalised AI dialogue reduced belief in conspiracy theories in a large study (Costello, Pennycook & Rand, 2024, *Science*)
- Algorithmic decision making in government: welfare fraud detection scandals (e.g. the Dutch childcare-benefits affair) illustrate harms

## Digital humanities

- OCR and handwritten text recognition for archives (Transkribus)
- Deciphering and restoring ancient texts: Ithaca for Greek inscriptions (Assael et al., 2022, *Nature*); the Vesuvius Challenge read carbonised Herculaneum scrolls with ML (2023–2024)
- Stylometry and authorship attribution
- Cultural analytics over millions of books, images and films
- Translation and revitalisation of endangered languages

## Methodological cautions

- Validate measurement against human-coded gold standards
- Beware of training-data contamination when using LLMs on well-known texts
- Report prompts and model versions for reproducibility; closed models change silently
- Consider ethics of scraping and consent

## Resources

- Grimmer, Roberts & Stewart, *Text as Data*
- Salganik, *Bit by Bit: Social Research in the Digital Age* (free online)
- Ziems et al. (2024), "Can Large Language Models Transform Computational Social Science?", *Computational Linguistics*
- Summer Institutes in Computational Social Science (SICSS) materials
