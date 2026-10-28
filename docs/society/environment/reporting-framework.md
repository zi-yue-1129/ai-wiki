---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Reporting energy and carbon
  - Experiment Impact Tracker
  - Systematic reporting of ML footprints
---

# Reporting Energy and Carbon (Henderson et al., 2020)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one framework in detail; the parent page compares it with others.

Henderson, Hu, Romoff, Brunskill, Jurafsky and Pineau (2020) present a framework for tracking the energy use and carbon emissions of machine-learning experiments while they run, and for publishing the results in a standard form. The tool is called the Experiment Impact Tracker. They use the collected results to build a leaderboard for energy-efficient reinforcement learning.

## Problem

Accurate reporting of energy and carbon use is needed to understand the climate impact of machine learning, but it is rarely done. Estimates made after the fact depend on details that are easy to lose, and figures reported in different ways cannot be compared. Without a common format, a researcher who wants to report energy use has to build the measurement from scratch.

## Core idea

Measure energy and estimate emissions during the experiment, not afterwards, and publish the figures in a standard form. The same format for every experiment makes results comparable, and collecting them in one place makes it possible to rank methods on energy as well as performance.

## How the framework works

1. **Track while running.** The tracker needs only a short code change. It logs the hardware, the process start and end times, the power drawn by CPU and GPU, and the grid region of the machine.
2. **Estimate carbon.** Each region's average carbon intensity is used to convert energy into emissions. Real-time intensity is supported only for California.
3. **Standardise the output.** Publish the figures in a standard online appendix and a Carbon Impact Statement, expressed in CO2 equivalent.
4. **Collect and rank.** The Deep RL Energy Leaderboard ranks reinforcement-learning methods by average return per kWh, on Pong and Breakout, with PPO, A2C, A2C with V-trace and DQN.

The paper's headline example is a class of 235 students who each run Pong five times. Using PPO instead of DQN would save 888 kWh. The authors also recommend that cloud jobs use low-carbon regions where possible.

## Results

The framework itself is the result. The paper reports the tracking tool, the leaderboard and the case studies that suggest ways to reduce energy and emissions. Its leaderboard shows that no single algorithm wins on both games: A2C with V-trace ranks first on Pong, and PPO ranks first on Breakout.

## Limitations

- **Depends on drivers.** Power readings need hardware and driver support. Not every chipset supports the Intel RAPL interface, and per-process GPU readings inside Docker containers are not supported. Only Intel RAPL or PowerGadget systems on macOS and Linux are covered.
- **Regional averages.** Carbon figures are regional supply averages. Clean-energy purchases by cloud providers may not appear in them, and the authors found no real-time energy-mix data for such cases.
- **Closed data source.** The regional intensity fallback comes from a closed-source system, which limits how far the figures can be verified.
- **Narrow first case.** The leaderboard covers reinforcement learning on two Atari games. Other fields may need different measures and formats.
- **Adoption.** A standard appendix is useful only if researchers fill it in.

## Connections

- The earlier calculator that estimates from three inputs, without tracking the run, is on the [Emissions Calculator](emissions-calculator.md) page.
- The argument for reporting cost alongside accuracy is on the [Green AI](green-ai.md) page.
- Ways of reducing the energy use that such reports reveal are covered in [Energy-Efficient Training](energy-efficient-training.md).

## Open questions

- How should energy and carbon be measured consistently across different hardware and cloud providers?
- Who should check the figures that researchers report?
- How can a reporting format be extended to fields beyond reinforcement learning?

## References

### Seminal papers

- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248), 1–43. https://www.jmlr.org/papers/v21/20-312.html — The framework, the Experiment Impact Tracker and the leaderboard described on this page. Preprint: https://arxiv.org/abs/2002.05651
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54–63. doi:[10.1145/3381831](https://doi.org/10.1145/3381831) — Argues that the cost of research should be reported and treated as a criterion, which this framework makes practical.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv preprint. https://arxiv.org/abs/1910.09700 — Estimates emissions from three inputs, without tracking the run during training.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — An earlier cost estimate made after the fact, which shows why in-run measurement matters.
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv preprint. https://arxiv.org/abs/2104.10350 — Shows how much the factors that such reports record can change the footprint.
