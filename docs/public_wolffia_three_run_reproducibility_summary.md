# Public Wolffia Three-Run Reproducibility Summary

## Technical Summary

Three public `Wolffia australiana` runs from `PRJNA1124135` have now been processed through the same analysis path: SRA retrieval, technical-read recovery, STARsolo counting against the `Waus8730.v1` reference, AnnData conversion, Waus8730-to-Arabidopsis feature bridging, normalization, and leaf-primary/root-benchmark transfer prediction.

The main result is reproducible across runs. All three runs produced the same Waus8730 gene feature space, the same 309 of 340 mapped transfer-model features, and a conservative prediction profile dominated by ambiguous cells plus a recurring photosynthetic/assimilation-like accepted subset.

This strengthens the current project conclusion: the pipeline can process real public Wolffia single-cell data end-to-end, but the model should still be treated as a broad program detector rather than a final Wolffia cell-type annotation system.

## Scope and Inputs

| Item | Value |
|---|---|
| Public project | `PRJNA1124135` |
| Processed runs | `SRR29417746`, `SRR29417745`, `SRR29417744` |
| Reference | `Waus8730.v1` |
| Count matrix generation | STARsolo |
| Cell barcode/UMI assumption | 16 bp cell barcode + 12 bp UMI from read 2 |
| Transfer model features | 340 Arabidopsis-space features |
| Waus8730 bridge coverage | 309 of 340 model features |

The same Waus8730 orthogroup bridge was used for all three runs. When one Arabidopsis model feature mapped to multiple Waus8730 candidate genes, the Waus8730 expression values were averaged after full-matrix library-size normalization and log transformation.

## QC and Model-Input Comparison

| Metric | `SRR29417746` | `SRR29417745` | `SRR29417744` |
|---|---:|---:|---:|
| Filtered cells | 2,718 | 2,814 | 2,886 |
| Waus8730 genes in matrix | 15,080 | 15,080 | 15,080 |
| Mapped model features | 309 | 309 | 309 |
| Real model-feature coverage | 90.9% | 90.9% | 90.9% |
| Median raw UMIs per cell | 2,595.5 | 3,727.0 | 2,376.0 |
| Median raw genes per cell | 902.5 | 1,134.5 | 1,023.5 |
| Leaf-primary acceptance rate | 13.5% | 12.1% | 8.2% |
| Root-benchmark acceptance rate | 0.04% | 0.11% | 0.10% |

The three runs differ in sequencing depth and accepted-label rate, but they share the same feature-space coverage and the same broad prediction pattern. `SRR29417745` has the strongest median UMI depth, while `SRR29417744` has the lowest leaf-primary acceptance rate.

## Transfer-Label Reproducibility

| Final label | `SRR29417746` cells | `SRR29417745` cells | `SRR29417744` cells |
|---|---:|---:|---:|
| ambiguous | 2,350 | 2,473 | 2,650 |
| photosynthetic_or_assimilation | 347 | 322 | 224 |
| vascular_like_or_transport | 21 | 16 | 11 |
| transport_interface_or_water_balance | 0 | 2 | 0 |
| review_required | 0 | 1 | 1 |

The most reproducible non-ambiguous signal remains `photosynthetic_or_assimilation`:

- `SRR29417746`: 347 of 2,718 cells, or 12.8%
- `SRR29417745`: 322 of 2,814 cells, or 11.4%
- `SRR29417744`: 224 of 2,886 cells, or 7.8%

The smaller vascular/transport-like signal appears in all three runs but remains weak. It should stay provisional until supported by native Wolffia markers, cluster-level expression, and the remaining public run.

## Interpretation

The three-run comparison supports the central project logic:

1. The Waus8730 preprocessing and feature-bridging route is reproducible across multiple public runs.
2. The leaf-primary model consistently accepts only a minority of cells, which matches the intended conservative design.
3. The strongest accepted signal is photosynthetic/assimilation-like, which is biologically plausible for a reduced photosynthetic Wolffia body.
4. The root-benchmark model remains almost entirely ambiguous, supporting its role as a conservative secondary check rather than the main interpretation layer.
5. Most cells remain ambiguous, which is useful at this stage. Ambiguity may reflect Wolffia-native cell states, incomplete cross-species feature coverage, missing reference programs, or uncertain mapping from Arabidopsis-derived labels.

This result is stronger than a single-run proof of concept, but it is still descriptive. It does not establish final Wolffia cell-type identity.

## Limitations and Uncertainty

- Three of four public runs have been processed so far; `SRR29417743` remains to be added.
- Only `SRR29417746` has a completed native UMAP and cluster-marker review in the repository.
- The exact library chemistry/barcode whitelist has not been confirmed, so STARsolo was run with `--soloCBwhitelist None`.
- Waus8730-to-Arabidopsis feature bridging uses orthogroup-level evidence and includes one-to-many mappings.
- The model outputs broad program labels, not final cell-type annotations.

## Recommended Next Steps

1. Process `SRR29417743` through the same STARsolo and transfer-model workflow.
2. Build a combined public-Wolffia notebook comparing all processed runs on QC metrics, feature coverage, model acceptance, label fractions, native clusters, and marker annotations.
3. Add cluster-marker review for `SRR29417745` and `SRR29417744`, parallel to the existing `SRR29417746` review.
4. Treat the reproducible photosynthetic/assimilation-like signal as the main current positive result.
5. Keep vascular/transport-like and root-like signals conservative until they show stronger marker and cross-run support.

## Current Conclusion

The first three public Wolffia runs show early reproducibility. Across all three, the pipeline preserves high model-feature coverage, leaves most cells ambiguous, and repeatedly identifies a small photosynthetic/assimilation-like subset. This supports continuing with the final public run and then building a combined multi-run analysis notebook.
