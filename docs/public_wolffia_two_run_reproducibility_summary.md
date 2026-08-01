# Public Wolffia Two-Run Reproducibility Summary

## Technical Summary

Two public Wolffia runs from `PRJNA1124135`, `SRR29417746` and `SRR29417745`, have now been processed through the same analysis path: SRA retrieval, technical-read recovery, STARsolo counting against `Waus8730.v1`, AnnData conversion, Waus8730-to-Arabidopsis feature bridging, normalization, and leaf-primary/root-benchmark transfer prediction.

The second run reproduces the first run's main pattern. Both runs produced similar filtered cell counts, the same Waus8730 gene feature space, the same 309 of 340 mapped transfer-model features, and a conservative model output dominated by ambiguous cells plus a reproducible photosynthetic/assimilation-like accepted subset.

This is an important milestone because the project is no longer supported by one public Wolffia run alone. The model now shows early run-to-run reproducibility in the public Waus8730 data, although the result remains provisional and needs marker/cluster review for the second run and additional public runs.

## Scope and Inputs

| Item | Value |
|---|---|
| Public project | `PRJNA1124135` |
| Processed runs | `SRR29417746`, `SRR29417745` |
| Reference | `Waus8730.v1` |
| Count matrix generation | STARsolo |
| Cell barcode/UMI assumption | 16 bp cell barcode + 12 bp UMI from read 2 |
| Transfer model features | 340 Arabidopsis-space features |
| Waus8730 bridge coverage | 309 of 340 model features |

The same Waus8730 orthogroup bridge was used for both runs. One-to-many Waus8730 candidates for a model feature were averaged after full-matrix library-size normalization and log transformation.

## QC and Model-Input Comparison

| Metric | `SRR29417746` | `SRR29417745` |
|---|---:|---:|
| Filtered cells | 2,718 | 2,814 |
| Waus8730 genes in matrix | 15,080 | 15,080 |
| Mapped model features | 309 | 309 |
| Real model-feature coverage | 90.9% | 90.9% |
| Median raw UMIs per cell | 2,595.5 | 3,727.0 |
| Median raw genes per cell | 902.5 | 1,134.5 |
| Leaf-primary acceptance rate | 13.5% | 12.1% |
| Root-benchmark acceptance rate | 0.04% | 0.11% |

`SRR29417745` has stronger cell-level depth than `SRR29417746`, with higher median UMIs and genes per cell. Despite that difference, the transfer model remains similarly conservative across both runs.

## Transfer-Label Reproducibility

| Final label | `SRR29417746` cells | `SRR29417745` cells |
|---|---:|---:|
| ambiguous | 2,350 | 2,473 |
| photosynthetic_or_assimilation | 347 | 322 |
| vascular_like_or_transport | 21 | 16 |
| transport_interface_or_water_balance | 0 | 2 |
| review_required | 0 | 1 |

The most reproducible non-ambiguous signal is `photosynthetic_or_assimilation`. It appears in both runs at a similar scale:

- `SRR29417746`: 347 of 2,718 cells, or 12.8%
- `SRR29417745`: 322 of 2,814 cells, or 11.4%

The vascular/transport-like signal is much smaller in both runs and should remain a weak provisional signal until it is supported by cluster markers and additional runs.

## Interpretation

The two-run comparison supports the central project logic:

1. The Waus8730 preprocessing and feature-bridging route is reproducible across public runs.
2. The leaf-primary model consistently identifies a small photosynthetic/assimilation-like subset.
3. The root-benchmark model remains mostly ambiguous, which is expected for Wolffia and supports treating it as a conservative secondary check rather than the main biological interpretation layer.
4. Most cells remain ambiguous, which is a useful conservative behavior rather than a failure. Ambiguous clusters may represent Wolffia-native states, poor annotation coverage, or programs not represented well by the current Arabidopsis-derived references.

The result strengthens the argument that the model is not simply producing one-run artifacts. However, the current evidence is still descriptive and provisional; it does not establish final Wolffia cell-type identity.

## Limitations

- Only two public runs have been processed so far.
- `SRR29417745` has not yet received the same native UMAP and annotated marker review completed for `SRR29417746`.
- The exact library chemistry/barcode whitelist has not been confirmed, so STARsolo was run with `--soloCBwhitelist None`.
- Waus8730-to-Arabidopsis feature bridging uses orthogroup-level evidence and includes one-to-many mappings.
- The model outputs broad program labels, not final cell-type annotations.

## Recommended Next Steps

1. Create a QC/UMAP/marker-review notebook for `SRR29417745`, parallel to the existing `SRR29417746` notebook.
2. Process `SRR29417744` and `SRR29417743` through the same STARsolo and transfer-model workflow.
3. Build a combined multi-run notebook that compares all processed runs on QC, feature coverage, model acceptance, label fractions, native clusters, and marker annotations.
4. Treat the reproducible photosynthetic/assimilation-like signal as the main current positive result.
5. Keep vascular/transport-like and root-like signals conservative until they show stronger marker and cross-run support.

## Current Conclusion

The first two public Wolffia runs show early reproducibility. Both support a conservative leaf-primary transfer model that reliably leaves most cells ambiguous while identifying a consistent photosynthetic/assimilation-like subset. This makes the next public-run processing step worthwhile and gives the future Waus8730 salt-stress application a stronger computational foundation.
