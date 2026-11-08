---
related:
  - engineering/frameworks
  - engineering/frameworks/compilers-and-kernels
  - engineering/training
tags:
  - deep learning frameworks
  - automatic differentiation
  - eager execution
  - PyTorch
aliases:
  - PyTorch paper
  - PyTorch: An Imperative Style, High-Performance Deep Learning Library
  - PyTorch 論文
last_reviewed: 2026-11-01
---

# PyTorch: An Imperative Style, High-Performance Deep Learning Library

The PyTorch paper (Paszke et al., 2019) describes a deep learning library whose programs run eagerly, as ordinary Python, and whose automatic differentiation is built at run time. It was published at NeurIPS 2019. The paper argues that giving up graph metaprogramming, in exchange for an imperative model, is worth a modest loss of speed, and it reports benchmarks against other frameworks of its time. The landscape of frameworks is on the [Frameworks](index.md) page.

## Overview

Before PyTorch, many frameworks required the user to build a static graph and then run it. The paper's design keeps the Python model: layers, models and training loops are plain Python code, and the user controls every part of the process. This makes programs easy to write and to debug with standard tools, at the cost of some compile-time optimisation that the paper leaves to later work.

## Design principles

Section 3 names four principles.

- **Be Pythonic.** PyTorch should be a first-class member of the Python ecosystem, with simple and consistent interfaces.
- **Put researchers first.** Models, data loaders and optimisers should be easy to write, and complexity should be hidden behind intuitive APIs without surprising performance cliffs.
- **Provide pragmatic performance.** Speed matters, but not at the cost of simplicity. The authors accept a modest loss of speed for a simpler model, but not a large one.
- **Worse is better.** A simple, slightly incomplete implementation is preferred to a complete but hard-to-maintain one, because the saved effort goes into features and keeping pace with the field.

## Autograd and eager execution

Section 4.3 explains the automatic differentiation. Rather than transforming source code, PyTorch uses operator overloading, so the computation is recorded as it runs. The current implementation is reverse mode, which suits a scalar output with many inputs. Forward mode is described as possible but is not part of the implementation.

Mutation of tensors is supported. A versioning system tracks modifications so that the correct values are used in the backward pass. The authors decided against copy-on-write. The complicated in-place cases raise a user error rather than copying silently, to avoid hidden performance costs. Most gradient formulas are implemented in C++ and evaluated by a multithreaded engine that does not hold the Python global interpreter lock.

Because programs run eagerly, print statements, standard debuggers and visualisation tools work without a compilation step.

## Performance

Section 6 compares training speed on two Intel Xeon CPUs and one NVIDIA Quadro GP100 GPU, using 32-bit floats. The table below gives the values as reported. Units are images per second for the image models, tokens per second for GNMTv2 and samples per second for NCF.

| Framework | AlexNet | VGG-19 | ResNet-50 | MobileNet | GNMTv2 | NCF |
|---|---|---|---|---|---|---|
| Chainer | 778 ± 15 | N/A | 219 ± 1 | N/A | N/A | N/A |
| CNTK | 845 ± 8 | 84 ± 3 | 210 ± 1 | N/A | N/A | N/A |
| MXNet | 1554 ± 22 | 113 ± 1 | 218 ± 2 | 444 ± 2 | N/A | N/A |
| PaddlePaddle | 933 ± 123 | 112 ± 2 | 192 ± 4 | 557 ± 24 | N/A | N/A |
| TensorFlow | 1422 ± 27 | 66 ± 2 | 200 ± 1 | 216 ± 15 | 9631 ± 1.3% | 4.8e6 ± 2.9% |
| **PyTorch** | 1547 ± 316 | 119 ± 1 | 212 ± 2 | 463 ± 17 | 15512 ± 4.8% | 5.4e6 ± 3.4% |

On these numbers, PyTorch is fastest on VGG-19, GNMTv2 and NCF. MXNet is fastest on AlexNet, Chainer on ResNet-50 and PaddlePaddle on MobileNet. The AlexNet figure for PyTorch has a very wide spread. The authors attribute the close results on common models to the shared use of the same vendor kernel libraries, and they report that GPU work overlaps with CPU scheduling, which keeps the device busy.

## Limitations

The paper has no dedicated limitations section, but the body states several.

- The most complicated in-place mutations raise a user error rather than being handled automatically.
- Forward-mode differentiation is not implemented.
- The memory guarantees rely on reference counting, which excludes some language runtimes.
- The per-stream memory allocator can fail in corner cases, although the authors say this is rare in practice.
- Python's global interpreter lock limits threads, which the design works around with multiprocessing.

The stated future work includes a JIT that runs programs outside the Python interpreter, efficient primitives for data parallelism, and a Pythonic library for model parallelism based on remote procedure calls.

## Connections

- The paper's future-work idea of a JIT that runs programs outside the Python interpreter points toward the [Compilers and Kernels](compilers-and-kernels/index.md) chapter.
- The training practices that depend on the framework are on the [Training](../training/index.md) page.
- The graph-based frameworks that PyTorch's eager model was designed to contrast with are covered in the [Frameworks](index.md) overview.

## Open questions

- How much of the eager model's speed can a compiler recover without changing the Python program?
- Can data and model parallelism be expressed with the same simple interfaces the paper describes?
- How should memory allocation behave under heavy multi-stream workloads?

## References

### Seminal papers

- Paszke, A. et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS. [arXiv:1912.01703](https://arxiv.org/abs/1912.01703) — The design, autograd and benchmark results discussed on this page.
- Abadi, M. et al. (2016). TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems. [arXiv:1603.04467](https://arxiv.org/abs/1603.04467) — The static-graph framework that the paper contrasts with its eager design.
- Kingma, D. P. & Ba, J. (2014). Adam: A Method for Stochastic Optimization. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980) — The optimiser that PyTorch's training loops commonly use.
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). Deep Residual Learning for Image Recognition. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — ResNet-50, one of the benchmark models.
- Howard, A. G. et al. (2017). MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. [arXiv:1704.04861](https://arxiv.org/abs/1704.04861) — MobileNet, one of the benchmark models.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
