# Combined Wolffia Application Script

## Purpose

This document describes the script that will apply both current transfer models to future Wolffia
single-cell expression matrices.

Script:

- [scripts/36_apply_leaf_primary_and_root_benchmark.py](../scripts/36_apply_leaf_primary_and_root_benchmark.py)

## What the Script Does

The script combines three parts of the project:

1. Arabidopsis-to-Wolffia ortholog mapping
2. v2 leaf-primary model
3. v1 root-benchmark model

It uses the ortholog table to assemble a 340-feature input matrix in the same order used during
model training, then applies both model views to each cell.

## Required Input

The future input should be a normalized, `log1p`-transformed Wolffia `.h5ad` file.

Raw counts should still be preserved separately, but the model input should be on the same expression
scale used by the Arabidopsis reference models.

The `.h5ad` must contain Wolffia gene identifiers in either:

- `adata.var_names`, or
- a specified `adata.var` column passed with `--gene-id-column`

## Output Files

Default output directory:

- `results/combined_wolffia_application/`

Main outputs:

- `combined_leaf_root_predictions.csv`
- `combined_feature_coverage_audit.csv`
- `combined_application_summary.json`

Default figure directory:

- `figures/combined_wolffia_application/`

Main figure:

- `combined_final_label_counts.png`

## Decision Rule

The script applies the project interpretation rule:

| Leaf-primary result | Root-benchmark result | Final status |
|---|---|---|
| confident | agrees | strongest support |
| confident | root ambiguous | leaf-primary support |
| confident | disagrees | review required |
| ambiguous | root confident | secondary root-like signal only |
| ambiguous | ambiguous | ambiguous |

The output preserves both model layers rather than hiding disagreement.

## Smoke Test

Before real Wolffia data arrive, the script can be tested with synthetic Wolffia-like input:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py --smoke-test
```

The smoke test checks that:

- both model artifacts load correctly
- the 340-feature ortholog matrix can be assembled
- leaf and root predictions run
- final interpretation labels are written
- no labels are forced when the input is meaningless

The current smoke-test result returns all cells as `ambiguous`, which is expected for random
synthetic data and supports the conservative rejection behavior of the workflow.

## Future Real-Data Command

Example:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py \
  input_wolffia_normalized.h5ad \
  --gene-id-column wolffia_gene_id
```

If Wolffia gene IDs are already stored in `adata.var_names`, omit `--gene-id-column`.

## Interpretation Caveat

The script produces provisional transferred labels. A final biological annotation still requires:

- adequate feature coverage
- model confidence
- leaf/root agreement or explicit review status
- marker-module support
- cluster-level coherence
- QC checks
- reproducibility across datasets or replicates

## Bottom Line

This script makes the project application-ready: once a Wolffia expression matrix is available, the
pipeline can directly generate leaf-primary predictions, root-benchmark comparisons, confidence
scores, ambiguity calls, and review flags.
