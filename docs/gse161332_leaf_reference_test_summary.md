# GSE161332 Leaf Reference Test Summary

## Purpose

This test applies the frozen 340-feature root-consensus transfer model to the selected Arabidopsis leaf reference `GSE161332`.

The goal is not to claim that a root-derived model can fully annotate leaf biology. Instead, the test asks whether the frozen transfer feature space can technically operate on a leaf single-cell matrix, and whether its behavior supports the need for a dedicated leaf/aerial reference layer.

## Dataset

- Dataset: `GSE161332`
- Organism: `Arabidopsis thaliana`
- Tissue/context: leaf single-cell RNA-seq
- Matrix size used locally: 6,300 cells by 32,833 genes
- Input files:
  - `GSE161332_matrix.mtx.gz`
  - `GSE161332_features.tsv.gz`
  - `GSE161332_barcodes.tsv.gz`

## Model Tested

- Model: frozen root-consensus 340-feature model
- Feature source: high- or medium-confidence Arabidopsis-to-Wolffia transferable genes
- Classifiers:
  - calibrated logistic regression
  - random forest
- Acceptance rule:
  - both models must agree
  - both model confidences must be at least `0.60`
  - global feature coverage must be at least `80%`
  - otherwise the cell is labeled `ambiguous`

## Main Results

| Metric | Result |
|---|---:|
| Total cells tested | 6,300 |
| Total genes in GSE161332 matrix | 32,833 |
| Frozen model features requested | 340 |
| Frozen model features present | 340 |
| Feature coverage | 100.0% |
| Model agreement rate | 88.8% |
| Consensus accepted cells | 1,987 |
| Consensus acceptance rate | 31.5% |

Consensus prediction counts:

| Consensus prediction | Cells | Fraction |
|---|---:|---:|
| `ambiguous` | 4,313 | 68.5% |
| `abiotic_stress_response` | 1,825 | 29.0% |
| `transport_interface_or_water_balance` | 155 | 2.5% |
| `proliferative_or_meristematic` | 7 | 0.1% |

## Interpretation

The leaf dataset is technically compatible with the frozen model because all 340 required features are present. This means the Arabidopsis gene-ID space is not the limiting issue for applying the model to `GSE161332`.

However, the biological result is conservative and root-biased. Most cells remain `ambiguous`, and accepted cells are dominated by `abiotic_stress_response`. This is consistent with the model's design: the frozen v1 model was trained from a root-derived benchmark and currently predicts only three broad programs:

- `abiotic_stress_response`
- `proliferative_or_meristematic`
- `transport_interface_or_water_balance`

It does not yet predict leaf-relevant programs such as:

- `photosynthetic_or_assimilation`
- `epidermal_or_surface_identity`
- mesophyll-like identity
- guard-cell-like identity
- leaf vascular subtypes

## Conclusion

`GSE161332` passes the technical feature-coverage test and can be used in the project. But the frozen root-derived model is not sufficient as the final biological model for leaf-like or Wolffia-like interpretation.

The result strengthens the current reference-strategy refinement:

> Keep the root-derived model as a conservative benchmark, but build a dedicated Arabidopsis leaf/aerial reference layer as the primary biological model before interpreting Wolffia single-cell data.

In practical terms, the next model-development step should be to use `GSE161332` to add or score leaf-relevant programs, especially photosynthetic, surface/epidermal, mesophyll-like, and vascular/transport programs.

This is now implemented as a separate retraining step:

- [scripts/34_train_leaf_primary_ortholog_model.py](../scripts/34_train_leaf_primary_ortholog_model.py)

That script now trains a leaf-primary model using PSCB/Kim et al. cluster labels when the
`leaf.RDS` metadata have been extracted, then collapses those labels into the project broad-program
ontology. If the PSCB metadata are unavailable, it falls back to marker-derived pseudocluster labels.
The resulting benchmark should still be described as Arabidopsis broad-label recovery rather than
true Wolffia accuracy.

## Reproducible Command

```bash
python scripts/33_apply_root_consensus_to_gse161332_leaf.py
```
