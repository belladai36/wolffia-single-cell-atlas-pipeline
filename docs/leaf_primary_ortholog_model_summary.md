# Leaf-Primary Ortholog Model Summary

## Purpose

This analysis retrains the project around the updated model logic:

- root-derived model = conservative benchmark and proof of concept
- leaf/aerial-derived model = primary Wolffia-relevant biological layer

The new leaf-primary model uses the selected Arabidopsis leaf reference `GSE161332`, the Plant
Single Cell Browser/Kim et al. cluster assignments, and the 340 high- or medium-confidence
Arabidopsis-to-Wolffia ortholog features.

## Why This Was Needed

The previous leaf test applied the frozen root-derived model directly to the leaf matrix. That test
showed that the 340-feature space is technically compatible with leaf data, but the root model could
not represent key leaf/aerial programs such as photosynthesis and surface-associated identity.

Because `Wolffia australiana` is a reduced floating photosynthetic plant body rather than a canonical
root system, leaf/aerial references should carry more biological weight for Wolffia interpretation.

## Method

The main training script is:

- [scripts/34_train_leaf_primary_ortholog_model.py](../scripts/34_train_leaf_primary_ortholog_model.py)

The metadata extraction helper is:

- [scripts/35_extract_pscb_leaf_metadata.R](../scripts/35_extract_pscb_leaf_metadata.R)

The script performs the following steps:

1. loads the processed `GSE161332` Arabidopsis leaf matrix
2. normalizes and log-transforms expression
3. scores broad biological programs using the project marker table
4. attaches PSCB/Kim et al. Seurat cluster IDs where barcode-level metadata are available
5. collapses the published cluster IDs into broad project programs
6. creates marker-derived pseudocluster labels as a fallback/checking layer
7. keeps only the 340 Arabidopsis genes with high- or medium-confidence Wolffia ortholog mappings
8. trains class-balanced logistic regression and random forest models
9. retests the models with stratified held-out folds
10. applies the same dual-model consensus idea: both models must agree and confidence must be at least `0.60`

## Important Label Caveat

The GEO `GSE161332` matrix does not include barcode-level cell-type labels. We therefore downloaded
the Plant Single Cell Browser `leaf.RDS` object and extracted its Seurat cluster metadata. The
training labels are published cluster identities collapsed into broad project programs, not manually
curated per-cell Wolffia labels.

This is still not true Wolffia accuracy. It measures recovery of broad Arabidopsis leaf programs
within the published leaf reference.

## Main Results

Dataset and feature compatibility:

| Metric | Result |
|---|---:|
| Leaf matrix cells | 6,300 |
| PSCB/Kim-labeled cells used after filtering | 4,587 |
| Requested transfer features | 340 |
| Transfer features present | 340 |
| Feature coverage | 100.0% |

Published-label composition after filtering:

| Broad program label | Cells |
|---|---:|
| `photosynthetic_or_assimilation` | 3,527 |
| `vascular_like_or_transport` | 820 |
| `epidermal_or_surface_identity` | 177 |
| `transport_interface_or_water_balance` | 63 |

Model retest results:

| Model | Accuracy | Balanced accuracy | Macro F1 | Mean confidence |
|---|---:|---:|---:|---:|
| Logistic regression | 0.699 | 0.763 | 0.623 | 0.703 |
| Random forest | 0.830 | 0.589 | 0.653 | 0.787 |

Dual-model consensus:

| Metric | Result |
|---|---:|
| Held-out labeled cells evaluated | 4,587 |
| Consensus accepted cells | 1,988 |
| Consensus acceptance rate | 43.3% |
| Selective label recovery | 93.6% |

Consensus prediction counts:

| Consensus prediction | Cells |
|---|---:|
| `ambiguous` | 2,599 |
| `photosynthetic_or_assimilation` | 1,711 |
| `vascular_like_or_transport` | 153 |
| `epidermal_or_surface_identity` | 100 |
| `transport_interface_or_water_balance` | 24 |

## Interpretation

The leaf-primary model is much more aligned with the expected biology of a photosynthetic plant body
than the root-derived model. Unlike the root-derived model, the leaf-primary model can represent a
dominant `photosynthetic_or_assimilation` program.

This supports the refined project logic:

> The root-derived model should remain the conservative benchmark, while the leaf/aerial-derived
> model should become the primary biological interpretation layer for Wolffia.

The consensus acceptance rate is lower than the marker-only pseudo-label run because the benchmark is
now harder and more realistic. This is a good refinement: the model accepts fewer cells, but accepted
labels have high broad-program recovery.

## Output Files

Main result directory:

- `results/leaf_primary_ortholog_model/`

Key outputs:

- `leaf_primary_model_summary.json`
- `leaf_primary_model_metric_summary.csv`
- `leaf_primary_cv_consensus.csv`
- `leaf_primary_cv_fold_metrics.csv`
- `published_leaf_cluster_label_summary.csv`
- `leaf_cluster_program_assignments.csv`
- `leaf_transfer_feature_coverage.csv`
- `leaf_primary_selected_transfer_features.csv`
- `logistic_regression_leaf_primary.joblib`
- `random_forest_leaf_primary.joblib`

Figures:

- `figures/leaf_primary_ortholog_model/leaf_pseudo_label_counts.png`
- `figures/leaf_primary_ortholog_model/leaf_primary_consensus_confusion_matrix.png`

## Bottom Line

The project should now be described as a leaf-prioritized, ortholog-aware Wolffia program-prediction
framework. The current root-derived model is still useful, but mainly as a baseline and stress test.
The new leaf-primary model is the better biological direction for future Wolffia application.
