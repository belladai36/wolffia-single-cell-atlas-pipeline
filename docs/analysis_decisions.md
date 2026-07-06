# Analysis Decisions Log

Use this file to record choices that should be visible in the final Wolffia atlas methods section.

## Reference

- Genome FASTA:
- Gene annotation:
- Annotation source/version:
- STAR index parameters:

## QC Thresholds

- Minimum genes per cell: choose from the observed distribution within each capture; do not pre-freeze
- Minimum counts per cell: choose from the observed distribution within each capture; do not pre-freeze
- Maximum mitochondrial percentage: choose from each capture's observed distribution; no universal cutoff
- Plastid percentage: review metric only by default; require an explicit data-based decision before hard filtering
- Doublet detection: `scDblFinder` per capture; preserve score, call, and capture identifier
- Ambient RNA: quantify and use when supported by the count-generation workflow
- Filtering provenance: add a `passes_QC` field and retain counts by flag/removal reason
- Rationale after inspecting distributions: preserve threshold plots and biological justification

## Clustering

- Number of HVGs:
- Number of PCs:
- Number of neighbors:
- Leiden resolution:
- Robustness summary:

## Annotation

- Marker source: strict reciprocal Wolffia mappings plus separately flagged family-review candidates
- Coarse labels used: frozen eight-program interpretation ontology; classifier v1 predicts only three programs
- Transfer classifier: calibrated 340-feature logistic-regression/random-forest consensus
- Transfer acceptance: both models agree and each calibrated confidence is at least `0.60`
- Global feature coverage: at least 80% of frozen features must be present or application stops
- High-confidence biological annotation: also requires coherent independent marker-module and cluster support
- Ambiguous clusters: preserve as `ambiguous`; do not force a nearest label

## Trajectory

- PAGA grouping:
- Root or starting state, if known:
- Biological interpretation limits:
