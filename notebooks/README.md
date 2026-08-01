# Notebooks

Use this folder for exploratory review notebooks after the scripted pipeline has produced checkpoint `.h5ad` files.

Start with the consolidated overview:

1. Open [00_wolffia_project_analysis_overview.ipynb](00_wolffia_project_analysis_overview.ipynb).
2. Review the project question, datasets, Arabidopsis transfer results, UMAP examples, classifier validation, confidence calibration, ortholog coverage, and transfer-readiness decision in one place.
3. Use notebooks `01` through `05` for the more detailed analysis layers.

Recommended first notebook:

1. Open [01_public_reference_explorer.ipynb](01_public_reference_explorer.ipynb).
2. Load an existing public-reference result directory such as:
   - `results/public_reference`
   - `results/public_reference_gse121619`
   - `results/public_reference_gse123818`
3. Inspect:
   - train and test UMAPs
   - predicted broad-program counts
   - cluster/program score heatmaps
4. Use the notebook to compare transfer behavior across datasets before moving to Wolffia-native raw-data processing.

Current notebook purpose:

- make visual review easier than command-line script runs
- support side-by-side inspection of the existing Arabidopsis-based public-reference analyses
- keep the underlying scripted workflow as the source of truth while using notebooks for interpretation

Second notebook:

1. Open [02_root_consensus_benchmark.ipynb](02_root_consensus_benchmark.ipynb).
2. Review the cluster-held-out logistic-regression and random-forest comparison.
3. Inspect confidence calibration, confusion matrices, and the conservative GSE121619 consensus set.
4. Treat the reported scores as recovery of marker-derived pseudo-labels, not independent biological annotation accuracy.

Third notebook:

1. Open [03_ortholog_mapping_and_transfer_readiness.ipynb](03_ortholog_mapping_and_transfer_readiness.ipynb).
2. Review reciprocal Arabidopsis-to-Wolffia protein mappings and program-level marker coverage.
3. Compare the 2,000-gene Arabidopsis benchmark with the 340-gene ortholog-restricted model.
4. Use its transfer-readiness decision before applying any model to Wolffia cells.

Fourth notebook:

1. Open [04_transfer_model_benchmark_and_marker_audit.ipynb](04_transfer_model_benchmark_and_marker_audit.ipynb).
2. Compare the full 2,000-gene Arabidopsis model with the 340-gene transfer-ready model.
3. Review performance loss, calibration, independent-root acceptance, and program-level marker coverage.
4. Inspect family-level Wolffia candidates for weak stress, epidermal, and vascular marker panels.

Fifth notebook:

1. Open [05_frozen_wolffia_transfer_model.ipynb](05_frozen_wolffia_transfer_model.ipynb).
2. Review the final 340-feature model decision and its explicit rejection rule.
3. Inspect the confidence-threshold tradeoff, synthetic rejection-path stress test, and marker-evidence coverage.
4. Use the embedded validation checks to reconcile headline metrics directly against paired out-of-fold predictions.
5. Treat the model as provisionally ready for Wolffia application, not as biologically validated before the public Wolffia datasets are processed.

Sixth notebook:

1. Open [06_gse161332_leaf_transfer_test.ipynb](06_gse161332_leaf_transfer_test.ipynb).
2. Review the first Arabidopsis leaf-reference test using `GSE161332`.
3. Inspect frozen-feature coverage, root-derived model agreement, conservative acceptance, and consensus prediction distribution.
4. Use the conclusion to motivate the next project step: keeping the root model as a conservative benchmark while building a dedicated leaf/aerial reference layer for photosynthetic and surface-associated programs.

Seventh notebook:

1. Open [07_leaf_primary_and_combined_transfer_summary.ipynb](07_leaf_primary_and_combined_transfer_summary.ipynb).
2. Review the final ortholog-aware model hierarchy: 340 transfer features, v1 root benchmark, v2 leaf-primary model, and combined application script.
3. Inspect the root-vs-leaf benchmark comparison and combined-script smoke test.
4. Use the takeaways as the current high-level project summary before real Wolffia expression data arrive.

Eighth notebook:

1. Open [08_public_wolffia_srr29417746_qc_umap.ipynb](08_public_wolffia_srr29417746_qc_umap.ipynb).
2. Review the first public Wolffia run processed from STARsolo counts into native Waus8730 QC, UMAP, Leiden clusters, and transfer-label overlays.
3. Inspect whether provisional photosynthetic/assimilation-like and vascular/transport-like labels occupy coherent native Wolffia expression regions.
4. Use this notebook as the starting point for deciding whether to process the remaining public runs in the same way.

Ninth notebook:

1. Open [09_public_wolffia_four_run_comparison.ipynb](09_public_wolffia_four_run_comparison.ipynb).
2. Compare all four public `PRJNA1124135` Wolffia runs after STARsolo counting and transfer-model application.
3. Review cross-run QC, model-feature coverage, leaf-primary/root-benchmark acceptance, final label fractions, and the tentative dawn-versus-dusk pattern.
4. Use this notebook as the current bridge from per-run processing to combined public Wolffia interpretation.

Tenth notebook:

1. Open [10_public_wolffia_combined_umap_marker_review.ipynb](10_public_wolffia_combined_umap_marker_review.ipynb).
2. Combine all four public Wolffia normalized matrices into one cell-level object.
3. Review UMAPs colored by run, dawn/dusk label, native Leiden clusters, final transfer labels, and interpretation status.
4. Inspect the cluster-by-label composition and exported native marker-gene table to decide which transfer labels are supported by coherent Wolffia expression neighborhoods.
