# Public Wolffia Native Program Scoring

This note summarizes the native marker-program scoring layer added after the four public Waus8730 runs were processed.

The main notebook is:

```text
notebooks/11_public_wolffia_native_program_scoring.ipynb
```

## Purpose

The Arabidopsis-transfer model is intentionally conservative. Many Wolffia cells remain `ambiguous` because they do not confidently match the current Arabidopsis-derived reference labels.

This scoring layer asks a complementary question: do those Wolffia cells express reproducible Wolffia-native marker programs?

## Inputs

The notebook uses:

- four normalized public Waus8730 `.h5ad` files stored on external project storage
- the combined transfer-model prediction files for the same four runs
- the repo-level native marker candidate table:

```text
data/metadata/wolffia_native_program_marker_candidates.csv
```

## Outputs

The notebook writes lightweight, repo-safe outputs:

```text
data/metadata/wolffia_native_program_score_gene_coverage.csv
data/metadata/wolffia_native_program_score_summary.csv
figures/wolffia_native_program_scores/
```

The large single-cell matrices remain outside the repository.

## Current results

All candidate marker genes were present in the Waus8730 matrix for the current program table.

The strongest broad signal remains photosynthetic and chloroplast-related biology. Dawn-group runs have higher mean scores for:

- Photosynthesis / light harvesting
- Carbon fixation / assimilation
- Chloroplast gene expression / plastid translation

Dusk-group runs have higher mean scores for:

- Nutrient transport
- RNA-binding / regulatory
- Stress / chaperone response

These dawn/dusk differences are useful exploratory signals, not final biological claims. They should be interpreted as reproducible marker-program patterns in the public data and tested further with controlled experimental metadata.

## Why this matters

This step improves the project because it gives us a Wolffia-native interpretation layer. Instead of relying only on Arabidopsis label transfer, we can now:

1. keep conservative transfer labels,
2. score native Wolffia biological programs,
3. inspect ambiguous cells more productively, and
4. reuse the same score framework for future control versus salt-stress Wolffia data.

## Recommended next step

Manually review the candidate marker genes within each program and create a smaller trusted marker panel. That trusted panel can then be used as the baseline scoring system for new Wolffia experiments.
