# Public Wolffia Four-Run Reproducibility Summary

## Technical Summary

All four public `Wolffia australiana` runs from `PRJNA1124135` have now been processed through the same analysis path: SRA retrieval, technical-read recovery, STARsolo counting against the `Waus8730.v1` reference, AnnData conversion, Waus8730-to-Arabidopsis feature bridging, normalization, and leaf-primary/root-benchmark transfer prediction.

The main result is reproducible across the full public run set. Each run produced the same Waus8730 gene feature space, the same 309 of 340 mapped transfer-model features, and a conservative prediction profile dominated by ambiguous cells plus a recurring photosynthetic/assimilation-like accepted subset.

This is the strongest current computational checkpoint for the project. The pipeline can now process real public Wolffia single-cell data end-to-end, but the model should still be interpreted as a broad program detector rather than a final Wolffia cell-type annotation system.

## Scope and Inputs

| Item | Value |
|---|---|
| Public project | `PRJNA1124135` |
| Processed runs | `SRR29417746`, `SRR29417745`, `SRR29417744`, `SRR29417743` |
| Reference | `Waus8730.v1` |
| Count matrix generation | STARsolo |
| Cell barcode/UMI assumption | 16 bp cell barcode + 12 bp UMI from read 2 |
| Transfer model features | 340 Arabidopsis-space features |
| Waus8730 bridge coverage | 309 of 340 model features |

The same Waus8730 orthogroup bridge was used for all four runs. When one Arabidopsis model feature mapped to multiple Waus8730 candidate genes, the Waus8730 expression values were averaged after full-matrix library-size normalization and log transformation.

## QC and Model-Input Comparison

| Metric | `SRR29417746` | `SRR29417745` | `SRR29417744` | `SRR29417743` |
|---|---:|---:|---:|---:|
| Filtered cells | 2,718 | 2,814 | 2,886 | 2,666 |
| Waus8730 genes in matrix | 15,080 | 15,080 | 15,080 | 15,080 |
| Mapped model features | 309 | 309 | 309 | 309 |
| Real model-feature coverage | 90.9% | 90.9% | 90.9% | 90.9% |
| Median raw UMIs per cell | 2,595.5 | 3,727.0 | 2,376.0 | 2,231.0 |
| Median raw genes per cell | 902.5 | 1,134.5 | 1,023.5 | 992.5 |
| Leaf-primary acceptance rate | 13.5% | 12.1% | 8.2% | 7.3% |
| Root-benchmark acceptance rate | 0.04% | 0.11% | 0.10% | 0.08% |

The four runs differ in sequencing depth and accepted-label rate, but they share the same feature-space coverage and the same broad prediction pattern. The dawn-labeled runs have higher leaf-primary acceptance than the dusk-labeled runs, which is worth checking in a combined notebook before treating it as biological.

## Transfer-Label Reproducibility

| Final label | `SRR29417746` cells | `SRR29417745` cells | `SRR29417744` cells | `SRR29417743` cells |
|---|---:|---:|---:|---:|
| ambiguous | 2,350 | 2,473 | 2,650 | 2,471 |
| photosynthetic_or_assimilation | 347 | 322 | 224 | 183 |
| vascular_like_or_transport | 21 | 16 | 11 | 10 |
| transport_interface_or_water_balance | 0 | 2 | 0 | 2 |
| review_required | 0 | 1 | 1 | 0 |

The most reproducible non-ambiguous signal remains `photosynthetic_or_assimilation`:

- `SRR29417746`: 347 of 2,718 cells, or 12.8%
- `SRR29417745`: 322 of 2,814 cells, or 11.4%
- `SRR29417744`: 224 of 2,886 cells, or 7.8%
- `SRR29417743`: 183 of 2,666 cells, or 6.9%

The smaller vascular/transport-like signal appears in all four runs but remains weak. It should stay provisional until supported by native Wolffia markers, cluster-level expression, and cross-run consistency.

## Interpretation

The four-run comparison supports the central project logic:

1. The Waus8730 preprocessing and feature-bridging route is reproducible across the complete public run set.
2. The leaf-primary model consistently accepts only a minority of cells, matching the intended conservative design.
3. The strongest accepted signal is photosynthetic/assimilation-like, which is biologically plausible for a reduced photosynthetic Wolffia body.
4. The root-benchmark model remains almost entirely ambiguous, supporting its role as a conservative secondary check rather than the main interpretation layer.
5. Most cells remain ambiguous, which is useful at this stage. Ambiguity may reflect Wolffia-native cell states, incomplete cross-species feature coverage, missing reference programs, or uncertain mapping from Arabidopsis-derived labels.

This result is stronger than the earlier one-run, two-run, and three-run checkpoints because the same broad pattern now appears across all four public runs. It is still descriptive and does not establish final Wolffia cell-type identity.

## Limitations and Uncertainty

- Only `SRR29417746` has a completed native UMAP and cluster-marker review in the repository.
- The exact library chemistry/barcode whitelist has not been confirmed, so STARsolo was run with `--soloCBwhitelist None`.
- Waus8730-to-Arabidopsis feature bridging uses orthogroup-level evidence and includes one-to-many mappings.
- The model outputs broad program labels, not final cell-type annotations.
- Any apparent dawn-versus-dusk difference in acceptance rate needs a combined run-level analysis before interpretation.

## Recommended Next Steps

1. Build a combined public-Wolffia notebook comparing all four runs on QC metrics, feature coverage, model acceptance, label fractions, native clusters, and marker annotations.
2. Add cluster-marker review for `SRR29417745`, `SRR29417744`, and `SRR29417743`, parallel to the existing `SRR29417746` review.
3. Treat the reproducible photosynthetic/assimilation-like signal as the main current positive result.
4. Keep vascular/transport-like and root-like signals conservative until they show stronger marker and cross-run support.
5. Use the four-run public result as the baseline expectation before applying the model to new Waus8730 salt-stress data.

## Current Conclusion

All four public Wolffia runs show early reproducibility. Across the full run set, the pipeline preserves high model-feature coverage, leaves most cells ambiguous, and repeatedly identifies a small photosynthetic/assimilation-like subset. This supports moving from per-run processing into a combined multi-run analysis notebook.
