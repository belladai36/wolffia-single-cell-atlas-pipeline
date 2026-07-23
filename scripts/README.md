# 01. Scripts Guide

This folder contains the main analysis scripts and lightweight helper/export scripts.

## 01. Best Way to Read This Folder

There are four script groups.

### 1. Legacy raw-data scaffold

These scripts represent the older per-cell FASTQ route:

1. `00_fastq_qc.sh`
2. `01_align_star.sh`
3. `02_featurecounts.sh`
4. `03_build_count_matrix.py`
5. `04_cell_qc.py`
6. `05_normalize_hvg_pca.py`
7. `06_neighbors_leiden_umap.py`
8. `07_markers_annotation.py`
9. `08_paga_trajectory.py`
10. `09_robustness_checks.py`

Use this path only if you need custom raw-read processing.

### 2. Public-reference prediction workflow

These scripts are the main computational core of the current project:

1. `10_public_reference_statistical_prediction.py`
2. `11_prepare_public_references.py`
3. `14_extract_gse121619_from_monocle.R`
4. `15_prepare_gse121619_h5ad.py`
5. `16_prepare_gse123818_h5ad.py`
6. `17_cluster_public_reference.py`
7. `26_prepare_gse161332_leaf_h5ad.py`
8. `27_root_reference_consensus.py`
9. `28_download_orthology_references.sh`
10. `29_build_arabidopsis_wolffia_orthologs.py`
11. `30_transfer_model_benchmark_and_marker_audit.py`
12. `31_freeze_wolffia_transfer_model.py`
13. `32_apply_frozen_wolffia_model.py`
14. `33_apply_root_consensus_to_gse161332_leaf.py`

`27_root_reference_consensus.py` performs a cluster-held-out comparison of logistic regression and random forest, applies a conservative agreement filter to GSE121619, and fits provisional root consensus models.

`28_download_orthology_references.sh` pins and downloads RefSeq Arabidopsis and Wolffia protein/GFF3 resources. `29_build_arabidopsis_wolffia_orthologs.py` performs reciprocal DIAMOND protein searches and writes confidence-graded model and marker mappings.

`30_transfer_model_benchmark_and_marker_audit.py` compares the full Arabidopsis benchmark with the 340-gene transfer-ready model, quantifies performance loss, and separates marker mappings into transfer-ready, family-level candidate, and unresolved categories.

`31_freeze_wolffia_transfer_model.py` audits confidence thresholds, runs controlled rejection-path stress tests, and writes the machine-readable v1 model manifest. `32_apply_frozen_wolffia_model.py` applies that frozen dual-model rule to a normalized Wolffia `.h5ad` while enforcing feature coverage and retaining `ambiguous` calls.

`26_prepare_gse161332_leaf_h5ad.py` converts the selected Arabidopsis leaf reference, `GSE161332`, from GEO's processed 10x-style matrix files into the same `.h5ad` format used by the public-reference workflow.

`33_apply_root_consensus_to_gse161332_leaf.py` applies the frozen 340-feature root-consensus model directly to the processed `GSE161332` matrix files. This bypasses slow full `.h5ad` loading and writes a focused root-to-leaf transfer diagnostic.

`34_train_leaf_primary_ortholog_model.py` trains and retests a leaf-primary Arabidopsis model restricted to the same Arabidopsis-to-Wolffia transfer features. When the PSCB/Kim et al. `leaf.RDS` metadata have been extracted, it uses published cluster labels collapsed to broad project programs. If those metadata are unavailable, it falls back to leaf pseudoclusters and marker-derived broad-program pseudo-labels.

`35_extract_pscb_leaf_metadata.R` extracts barcode-level Seurat metadata from the Plant Single Cell Browser `leaf.RDS` object. This enables `34_train_leaf_primary_ortholog_model.py` to use PSCB/Kim et al. cluster labels collapsed into broad programs instead of relying only on marker-derived pseudoclusters.

`36_apply_leaf_primary_and_root_benchmark.py` applies both the v2 leaf-primary model and the v1 root-benchmark model to a normalized Wolffia `.h5ad`, using the ortholog table to assemble the 340-feature transfer matrix. It writes leaf predictions, root predictions, final interpretation labels, ambiguity/review flags, and a feature-coverage audit. Use `--smoke-test` to test the application path before real Wolffia data arrive.

### 3. Wolffia public-data preparation helpers

These support later Wolffia-native training:

1. `12_prepare_wolffia_public_references.py`
2. `13_wolffia_download_helper.py`

### 4. Figure export scripts

These generate visual exports:

1. `19_generate_public_reference_umaps.py`

## 02. Most Important Scripts Right Now

If you only want the current project core, focus on:

1. `27_root_reference_consensus.py`
2. `28_download_orthology_references.sh`
3. `29_build_arabidopsis_wolffia_orthologs.py`
4. `30_transfer_model_benchmark_and_marker_audit.py`
5. `31_freeze_wolffia_transfer_model.py`
6. `32_apply_frozen_wolffia_model.py`

The older public-reference scripts (`10_public_reference_statistical_prediction.py`,
`17_cluster_public_reference.py`, and `19_generate_public_reference_umaps.py`) remain useful for
background exploration and figure generation, but the current model-freeze path is scripts
`27` through `32`.

Environment note:

- the Scanpy-based scripts must be run inside the Conda environment created from `environment.yml`
- in the current local machine setup, they were validated in the `py311` environment rather than in base Python

## 03. Utility Files

- `pipeline_utils.py`: shared helper functions
- `run_all.sh`: convenience runner for the legacy FASTQ scaffold
- `00_preflight_check.py`: quick input and checkpoint sanity check
