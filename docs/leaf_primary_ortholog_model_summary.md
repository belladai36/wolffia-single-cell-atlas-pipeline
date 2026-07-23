# Leaf-Primary Ortholog Model Summary

## Purpose

This analysis retrains the project around the updated model logic:

- root-derived model = conservative benchmark and proof of concept
- leaf/aerial-derived model = primary Wolffia-relevant biological layer

The new leaf-primary model uses the selected Arabidopsis leaf reference `GSE161332` and restricts
the classifier input to the 340 high- or medium-confidence Arabidopsis-to-Wolffia ortholog features.

## Why This Was Needed

The previous leaf test applied the frozen root-derived model directly to the leaf matrix. That test
showed that the 340-feature space is technically compatible with leaf data, but the root model could
not represent key leaf/aerial programs such as photosynthesis and surface-associated identity.

Because `Wolffia australiana` is a reduced floating photosynthetic plant body rather than a canonical
root system, leaf/aerial references should carry more biological weight for Wolffia interpretation.

## Method

The new script is:

- [scripts/34_train_leaf_primary_ortholog_model.py](../scripts/34_train_leaf_primary_ortholog_model.py)

The script performs the following steps:

1. loads the processed `GSE161332` Arabidopsis leaf matrix
2. normalizes and log-transforms expression
3. scores broad biological programs using the project marker table
4. creates leaf pseudoclusters from PCA space
5. assigns each pseudocluster a marker-derived broad-program pseudo-label
6. keeps only the 340 Arabidopsis genes with high- or medium-confidence Wolffia ortholog mappings
7. trains class-balanced logistic regression and random forest models
8. retests the models with stratified held-out folds
9. applies the same dual-model consensus idea: both models must agree and confidence must be at least `0.60`

## Important Label Caveat

The local `GSE161332` object does not include curated published cell-type labels. Therefore, this
benchmark measures recovery of marker-derived leaf pseudo-labels, not true cell-type annotation
accuracy.

This is still useful because it tests whether a Wolffia-transferable leaf model can recover a
leaf/aerial marker structure more effectively than the root-derived benchmark.

## Main Results

Dataset and feature compatibility:

| Metric | Result |
|---|---:|
| Leaf cells tested | 6,300 |
| Requested transfer features | 340 |
| Transfer features present | 340 |
| Feature coverage | 100.0% |

Marker-derived pseudo-label composition after filtering:

| Pseudo-label | Cells |
|---|---:|
| `photosynthetic_or_assimilation` | 6,117 |
| `abiotic_stress_response` | 95 |
| `transport_interface_or_water_balance` | 88 |

Model retest results:

| Model | Accuracy | Balanced accuracy | Macro F1 | Mean confidence |
|---|---:|---:|---:|---:|
| Logistic regression | 0.959 | 0.905 | 0.720 | 0.977 |
| Random forest | 0.988 | 0.735 | 0.789 | 0.982 |

Dual-model consensus:

| Metric | Result |
|---|---:|
| Held-out cells evaluated | 6,300 |
| Consensus accepted cells | 5,954 |
| Consensus acceptance rate | 94.5% |
| Selective pseudo-label accuracy | 99.7% |

Consensus prediction counts:

| Consensus prediction | Cells |
|---|---:|
| `photosynthetic_or_assimilation` | 5,856 |
| `ambiguous` | 346 |
| `transport_interface_or_water_balance` | 75 |
| `abiotic_stress_response` | 23 |

## Interpretation

The leaf-primary model is much more aligned with the expected biology of a photosynthetic plant body
than the root-derived model. Unlike the root-derived model, the leaf-primary model can represent a
dominant `photosynthetic_or_assimilation` program.

This supports the refined project logic:

> The root-derived model should remain the conservative benchmark, while the leaf/aerial-derived
> model should become the primary biological interpretation layer for Wolffia.

The high consensus acceptance rate should not be overinterpreted as true cell-type accuracy. It is
best described as strong internal recovery of marker-derived leaf programs using the Wolffia-transfer
ortholog feature set.

## Output Files

Main result directory:

- `results/leaf_primary_ortholog_model/`

Key outputs:

- `leaf_primary_model_summary.json`
- `leaf_primary_model_metric_summary.csv`
- `leaf_primary_cv_consensus.csv`
- `leaf_primary_cv_fold_metrics.csv`
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
