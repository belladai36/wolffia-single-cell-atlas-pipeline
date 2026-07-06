# Frozen Wolffia Transfer Model v1

## Decision

The provisional model to carry forward into the first real Wolffia analysis is a calibrated,
two-model consensus restricted to 340 strict Arabidopsis-to-Wolffia ortholog features.

The component classifiers are class-balanced logistic regression and class-balanced random forest,
each fitted after scaling and 30-component PCA.

A cell receives a provisional transferred program only when:

1. both models predict the same program
2. each model has calibrated confidence of at least `0.60`
3. at least 80% of the 340 frozen model features are present globally in the input matrix

Otherwise, the result is `ambiguous`. A transferred label does not become a high-confidence
biological annotation until it is also supported by a coherent independent marker module and
cluster-level evidence.

## Why This Model

The unrestricted 2,000-gene model performs better within Arabidopsis, but many of its genes do not
have defensible one-to-one Wolffia mappings. It remains the within-species benchmark and is not
permitted for strict Wolffia prediction.

The 340-feature model is weaker but technically transferable. On the cluster-held-out Arabidopsis
pseudo-label benchmark, the frozen agreement rule accepted 1,438 of 4,727 cells (`30.4%`). Among
accepted cells:

- selective accuracy: `95.3%`
- selective balanced accuracy: `70.7%`
- selective macro F1: `68.1%`

The `0.60` confidence threshold is the selected tradeoff. A threshold of `0.55` accepted more cells
but reduced selective accuracy to `92.5%`; `0.65` increased accuracy to `96.7%` while reducing
acceptance to `22.3%`.

These metrics measure recovery of marker-derived Arabidopsis cluster pseudo-labels. They are not
estimates of true Wolffia cell-type accuracy.

## Programs the Classifier Can Predict

The trained v1 classifier distinguishes only:

- `abiotic_stress_response`
- `proliferative_or_meristematic`
- `transport_interface_or_water_balance`

The broader eight-program ontology remains useful for marker scoring and biological interpretation,
but the remaining five programs are not classifier outputs in v1.

## Marker Policy

- High- and medium-confidence reciprocal mappings may provide independent marker-module support.
- Low-confidence directional mappings are family-review candidates only.
- Family-level candidates are not classifier features and cannot rescue a rejected prediction.
- Unresolved markers remain excluded.
- Absence of a strict marker is not evidence that the corresponding biology is absent.

This is especially important for the vascular program: zero strict markers are currently available,
although six markers have plausible family-level candidates.

## Synthetic Stress Test

The fitted application path was tested with controlled missing-feature and expression-noise
perturbations. As feature dropout increased from 0% to 40%, mean acceptance decreased from 47.3%
to 25.7% while accepted predictions on the training-derived smoke-test subset remained stable.

This demonstrates that the implementation tends to reject deteriorated inputs rather than force
labels. Because the subset contributed to model fitting, this is a software and rejection-path test,
not independent performance validation.

## Applying the Model

The input must be a normalized, `log1p`-transformed Wolffia `.h5ad` compatible with the scale used
by the Arabidopsis references. Raw counts must remain preserved separately.

```bash
python scripts/32_apply_frozen_wolffia_model.py \
  input_wolffia_normalized.h5ad \
  output_wolffia_transferred.h5ad
```

By default, `adata.var_names` must contain NCBI Wolffia gene IDs. Use `--gene-id-column` if those
identifiers are stored in `adata.var` instead.

## Real-Data Re-evaluation Requirements

When `PRJNA1124135` is available:

1. choose cell QC thresholds from observed distributions by capture, not from a fixed template
2. run `scDblFinder` per capture and preserve its score and call
3. quantify ambient RNA when supported by the counting workflow
4. preserve raw counts and provenance in the processed object
5. check predictions by Dawn/Dusk replicate, cluster, and QC state
6. require independent marker and cluster support before naming biological states
7. report label stability under reasonable preprocessing and clustering choices
8. validate the frozen rule on `PRJNA809022` before calling v1 biologically validated

## Reproduction and Artifacts

```bash
python scripts/31_freeze_wolffia_transfer_model.py
```

The machine-readable decision is stored under `results/final_wolffia_transfer_model/`.

## Bottom Line

This is the frozen **provisional transfer model v1**. It is ready for real-data application, but it
must not be described as a validated Wolffia cell-type model until the public Wolffia datasets have
been processed and evaluated.
