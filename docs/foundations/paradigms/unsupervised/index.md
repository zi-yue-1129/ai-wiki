# Unsupervised Learning

## Idea

Find structure in data **without labels**: groups, low-dimensional factors, densities, anomalies. Yann LeCun's cake analogy: if intelligence is a cake, unsupervised (self-supervised) learning is the bulk of the cake, supervised learning the icing, and reinforcement learning the cherry.

## Main families

| Goal | Methods | Uses |
|---|---|---|
| Clustering | k-means, Gaussian mixtures (EM), hierarchical clustering, DBSCAN/HDBSCAN, spectral clustering, Leiden/Louvain on graphs | Customer segments, cell types in single-cell RNA-seq, topic discovery |
| Dimensionality reduction | PCA, ICA, NMF, factor analysis, t-SNE, UMAP, autoencoders | Visualisation, compression, denoising |
| Density estimation | Kernel density, mixture models, normalising flows, autoregressive models, diffusion models | Anomaly detection, generation, likelihoods |
| Anomaly detection | Isolation Forest, one-class SVM, LOF, reconstruction error | Fraud, equipment faults, intrusion detection |
| Association rules | Apriori, FP-growth | Market-basket analysis |
| Representation / manifold learning | Isomap, LLE, autoencoders, [self-supervised](../self-supervised/index.md) methods | Features for downstream tasks |
| Topic modelling | LDA, BERTopic | Document collections |

## Key ideas

- **k-means** minimises within-cluster squared distance; sensitive to initialisation and assumes roughly spherical clusters.
- **PCA** finds orthogonal directions of maximal variance — equivalently the best low-rank linear reconstruction.
- **ICA** finds statistically independent sources — the "cocktail party" problem; widely used to remove eye-blink artefacts from EEG.
- **t-SNE / UMAP** preserve local neighbourhoods for visualisation; distances between far-apart clusters and cluster sizes are *not* meaningful.
- **Autoencoders** compress through a bottleneck and reconstruct; variants (denoising, sparse, variational) shape the representation.

## Evaluating without labels

There is no ground truth, so evaluation is hard:

- Internal indices: silhouette score, Davies–Bouldin, reconstruction error, held-out likelihood
- Stability: do clusters persist across resamples?
- Downstream usefulness: do the features help a task?
- Expert inspection: do the clusters make domain sense?

## Unsupervised learning in the brain

- **Hebbian learning** with normalisation (Oja's rule) performs PCA — a single neuron can learn the first principal component.
- **Sparse coding** of natural images yields V1-like receptive fields (Olshausen & Field, 1996); ICA on natural sounds yields auditory-nerve-like filters (Lewicki, 2002).
- **Competitive learning and self-organising maps** (Kohonen) model topographic maps such as orientation maps and tonotopy.
- **Statistical learning** in infants (Saffran, Aslin & Newport, 1996) shows humans extract structure from unlabelled streams within minutes.
- **Neuroscience uses unsupervised ML constantly**: spike sorting, cell-type clustering, finding neural manifolds with PCA/UMAP, behavioural motif discovery (MoSeq).

## Further reading

- Bishop, *Pattern Recognition and Machine Learning*, chapters 9 and 12 (free PDF)
- [scikit-learn unsupervised learning guide](https://scikit-learn.org/stable/unsupervised_learning.html)
- McInnes et al. (2018), UMAP paper; Wattenberg et al., "How to Use t-SNE Effectively" (Distill, 2016)
