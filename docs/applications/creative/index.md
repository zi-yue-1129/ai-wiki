---
related:
- theory/paradigms/unsupervised/density-and-generative-models/generative-models
- theory/models/multimodal
- theory/models/speech
- society/governance
- society/economics
aliases:
  - 藝術
  - 創意
---

# Art, Media & Creativity

## Tools by medium

| Medium | Capabilities | Examples |
|---|---|---|
| Images | Text-to-image, editing, inpainting, style transfer, upscaling | Midjourney, DALL·E / GPT image generation, Stable Diffusion, Flux, Adobe Firefly, Imagen |
| Video | Text/image-to-video, editing, lip-sync, avatars | Sora, Veo, Kling, Runway, Pika |
| Music and audio | Song generation, stem separation, mastering, voice | Suno, Udio, MusicGen, ElevenLabs |
| Writing | Drafting, editing, brainstorming, interactive fiction | LLM assistants |
| 3D and games | Asset generation, texturing, animation | 3D generative models, motion-capture-from-video |
| Design | Layouts, logos, UI mock-ups | Design tools with generative features |
| Film and VFX | Rotoscoping, de-ageing, previsualisation, dubbing | Studio pipelines |

## Creativity research

- **Is AI creative?** Boden distinguishes combinational, exploratory and transformational creativity (Boden, 2009); most generative AI excels at the first two
- **Human–AI co-creation**: studies find AI ideas can raise individual creativity ratings while reducing the **diversity** of outputs across people (Doshi & Hauser, 2024, *Science Advances*)
- **Computational creativity** is a long-standing research field (AARON, EMI/David Cope)

## Copyright and ownership

Training data and the ownership of AI outputs are being contested in courts and legislatures in several countries, and the rules are still unsettled. Check current rulings and official guidance before relying on any specific position.

## Provenance and misinformation

- Deepfakes in politics and non-consensual intimate imagery
- **Content credentials** (C2PA), invisible watermarks (SynthID), and platform labelling
- Detection is an arms race and unreliable on its own

## Economic impact on creative work

Demand for some freelance writing and illustration work fell after generative AI releases (Hui et al., 2024), while other creators use AI to expand output. See [Economics & Work](../../society/economics/index.md).

## Key methods

Three methods underlie most image and video generators. Each links to the page that explains it.

- [Denoising diffusion](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md): a model learns to reverse a gradual noising process (Ho et al., 2020).
- [Latent diffusion](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion.md): runs diffusion in a compressed latent space, which makes high-resolution image generation practical (Rombach et al., 2022).
- [Classifier-free guidance](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/classifier-free-guidance.md): steers samples toward a text prompt without a separate classifier (Ho & Salimans, 2022).

## References

### Seminal papers

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The DDPM paper behind the diffusion method page linked above.
- Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. arXiv. https://arxiv.org/abs/2112.10752 — Latent diffusion, which runs diffusion in a compressed space.
- Ho & Salimans (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — Steers diffusion samples toward a prompt without a separate classifier.
- Doshi & Hauser (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*. https://doi.org/10.1126/sciadv.adn5290 — Finds AI ideas raise individual creativity but reduce diversity across writers.
- Boden (2009). Computer Models of Creativity. *AI Magazine*. https://doi.org/10.1609/aimag.v30i3.2254 — Review of computational creativity, including the three kinds of creativity.
- Epstein et al. (2023). Art and the science of generative AI. *Science*. https://doi.org/10.1126/science.adh4451 — Overview of generative AI in art and what it changes for creators.

### Articles and documentation

- Hui et al. (2024). The Short-Term Effects of Generative Artificial Intelligence on Employment: Evidence from an Online Labor Market. *Organization Science*. https://doi.org/10.1287/orsc.2023.18441 — Online labour market study of how generative AI affected freelance demand.
