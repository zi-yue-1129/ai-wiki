# Graph Neural Networks

## Why graphs?

Much data is naturally a graph: molecules (atoms and bonds), social networks, knowledge graphs, road networks, citation networks, protein interaction networks — and **brain connectomes**. CNNs and RNNs assume grids or sequences; GNNs handle arbitrary graphs.

## Message passing

At each layer, every node gathers messages from its neighbours, aggregates them, and updates itself:

\[
h_v^{(k+1)} = \text{UPDATE}\Big(h_v^{(k)},\; \text{AGG}_{u\in\mathcal{N}(v)}\, \text{MSG}(h_u^{(k)}, h_v^{(k)}, e_{uv})\Big)
\]

The aggregation must be **permutation-invariant** (sum, mean, max, attention).

## Representative models

| Model | Character |
|---|---|
| GCN (Kipf & Welling, 2017) | First-order approximation of spectral graph convolution |
| GraphSAGE | Neighbour sampling; scales to large graphs; inductive |
| GAT | Attention over neighbours |
| GIN | As expressive as the 1-WL graph isomorphism test |
| MPNN | Unified message-passing framework (quantum chemistry) |
| Equivariant GNNs (EGNN, NequIP, MACE) | Equivariant to 3D rotations and translations; molecular simulation |
| Graph Transformers | Global attention plus structural encodings |

## Tasks

- Node classification (paper topics, fraudulent accounts)
- Link prediction (recommendation, drug–drug interactions, knowledge-graph completion)
- Graph classification / regression (molecular properties, toxicity)
- Graph generation (molecule design)

## Known issues

- **Over-smoothing**: node representations converge as depth grows
- **Over-squashing**: long-range information is compressed into fixed-size vectors
- **Expressivity limits**: standard message passing cannot distinguish some non-isomorphic graphs

## Major applications

- **GNoME** (2023) used GNNs to predict a very large number of new stable crystal structures
- **GraphCast** (2023): global medium-range weather forecasting with a GNN, outperforming the leading operational numerical model on most targets
- Recommendation (Pinterest's PinSage), Google Maps arrival-time prediction
- Drug discovery and materials science — see [Life Sciences](../../applications/life-science/index.md), [Scientific Discovery](../../applications/science/index.md)

## Neuroscience: connectomics

- A **connectome** is the complete wiring diagram of neurons and synapses. The nematode *C. elegans* (302 neurons) was mapped in 1986; the **whole adult fruit-fly brain** connectome (FlyWire, ~140,000 neurons) was published in *Nature* in 2024
- Connectome-constrained network models can predict neural activity in the fly visual system (Lappalainen et al., 2024)
- **Network neuroscience** uses graph theory to study small-worldness, modularity and hubs in brain networks
- The MICrONS project (2025) released structural and functional data for a cubic millimetre of mouse visual cortex
- Deep learning is what made dense connectome reconstruction from electron microscopy feasible

## Resources

- Stanford CS224W, *Machine Learning with Graphs*
- [PyTorch Geometric](https://pyg.org/), [DGL](https://www.dgl.ai/)
- Hamilton, *Graph Representation Learning* (free PDF)
- Bronstein et al., *Geometric Deep Learning* (free online)
