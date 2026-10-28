---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision
  - theory/models/multimodal
  - society/ethics
aliases:
  - 無障礙與輔助科技
  - Accessibility
  - Assistive technology
---

# Accessibility and Assistive Technology

Many AI tools are, at heart, assistive: they describe images to blind users, caption speech for deaf users, and simplify text for people with cognitive or language difficulties. The same techniques can also make products less accessible when they are not designed and tested with disabled people. This page covers how AI is used to help, and the design standards that keep it accountable.

## Landscape

| Area | Examples |
|---|---|
| Image description | Describing photos and objects for screen reader users |
| Visual question answering | Answering questions about what a camera sees |
| Captions and transcription | Live captions for speech, and transcripts of recorded audio |
| Social media and content | Automatic alternative text on images in feeds |
| Animated content | Describing GIFs and video for users who cannot see them |
| Language and reading | Simplified text, and speech synthesis for people with reading difficulties |

## Image description and visual questions

VizWiz (Bigham et al., 2010) let blind users take a photo, ask a spoken question, and receive answers from remote workers, usually within minutes. A field deployment with 11 blind participants reported answers in about two minutes on average. Automatic alternative text takes the next step: Wu et al. (2017) describe a system that generates image descriptions for screen reader users on a social network, and a field test with about 9,000 VoiceOver users. Ga11y (Zhang et al., 2022) describes animated GIFs with a combination of automation and human annotation.

## Standards

Web Content Accessibility Guidelines 2.2 (W3C, 2024) set testable criteria for making web content usable by people with a wide range of disabilities. AI features are judged against the same criteria as other interface features, so an automatic description that is wrong or missing still counts as a failure. The World Health Organization (2019) reports how many people live with vision loss and how eye care can be strengthened, which sets the scale of the need.

## Key methods

Two methods underlie most assistive vision tools. Each links to the page that explains it.

- [Computer vision](../../theory/models/computer-vision/index.md): recognising objects, text and scenes in images, which image-description tools rely on.
- [Multimodal models](../../theory/models/multimodal/index.md): combining images and language to answer questions about a scene, as in visual question answering.

## Risks

- **Wrong descriptions** can mislead a user who cannot check the image, so errors need clear signals and an easy way to correct them.
- **Lack of testing with disabled people** can produce tools that meet a benchmark but fail in practice.
- **Privacy.** Cameras that describe surroundings may capture bystanders.

Fairness and inclusion issues are covered in [Ethics & Fairness](../../society/ethics/index.md).

## Open questions

- How should assistive tools report their own uncertainty to a user who cannot see the image?
- Can automated descriptions match the quality of human-written alternative text across different kinds of content?
- How should design standards be extended to cover AI-generated content?

## References

### Seminal papers

- Bigham, J. P. et al. (2010). VizWiz: nearly real-time answers to visual questions. *UIST '10*. https://doi.org/10.1145/1866029.1866080 — Blind users photograph a scene, ask a question and receive answers from remote workers, with a field deployment of 11 participants.
- Wu, S. et al. (2017). Automatic Alt-text: Computer-generated Image Descriptions for Blind Users on a Social Network Service. *CSCW '17*. https://doi.org/10.1145/2998181.2998364 — Facebook's automatic image descriptions for screen reader users, with a two-week field test of about 9,000 VoiceOver users.
- Zhang, M. R., Zhong, M. & Wobbrock, J. O. (2022). Ga11y: An Automated GIF Annotation System for Visually Impaired Users. *CHI '22*. https://doi.org/10.1145/3491102.3502092 — Annotates animated GIFs for blind and low-vision users, comparing three annotation interface styles.

### Surveys and textbooks

- World Health Organization (2019). *World report on vision*. WHO. https://www.who.int/publications/i/item/9789241516570 — Reports how many people live with vision loss and how eye-care services can be strengthened.

### Articles and documentation

- W3C (2024). *Web Content Accessibility Guidelines (WCAG) 2.2*. W3C Recommendation. https://www.w3.org/TR/WCAG22/ — Testable standard for making web content usable by people with a wide range of disabilities.
