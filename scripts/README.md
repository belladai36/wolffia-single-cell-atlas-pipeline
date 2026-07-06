# 01. Scripts Guide

This folder contains both the main analysis scripts and the helper/export scripts.

## 01. Best Way to Read This Folder

There are four script groups.

### 1. Legacy raw-data scaffold

These scripts represent the older per-cell FASTQ route:

1. `00_fastq_qc.sh`
2. `01_align_pipseq_star.sh`
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
7. `27_root_reference_consensus.py`
8. `28_download_orthology_references.sh`
9. `29_build_arabidopsis_wolffia_orthologs.py`
10. `30_transfer_model_benchmark_and_marker_audit.py`
11. `31_freeze_wolffia_transfer_model.py`
12. `32_apply_frozen_wolffia_model.py`

`27_root_reference_consensus.py` performs a cluster-held-out comparison of logistic regression and random forest, applies a conservative agreement filter to GSE121619, and fits provisional root consensus models.

`28_download_orthology_references.sh` pins and downloads RefSeq Arabidopsis and Wolffia protein/GFF3 resources. `29_build_arabidopsis_wolffia_orthologs.py` performs reciprocal DIAMOND protein searches and writes confidence-graded model and marker mappings.

`30_transfer_model_benchmark_and_marker_audit.py` compares the full Arabidopsis benchmark with the 340-gene transfer-ready model, quantifies performance loss, and separates marker mappings into transfer-ready, family-level candidate, and unresolved categories.

`31_freeze_wolffia_transfer_model.py` audits confidence thresholds, runs controlled rejection-path stress tests, and writes the machine-readable v1 model manifest. `32_apply_frozen_wolffia_model.py` applies that frozen dual-model rule to a normalized Wolffia `.h5ad` while enforcing feature coverage and retaining `ambiguous` calls.

### 3. Wolffia public-data preparation helpers

These support later Wolffia-native training:

1. `12_prepare_wolffia_public_references.py`
2. `13_wolffia_download_helper.py`

### 4. Report and protocol export scripts

These generate the polished project documents:

1. `18_generate_project_progress_pdf.py`
2. `19_generate_public_reference_umaps.py`
3. `20_generate_wolffia_protocol_pdf.py`
4. `21_generate_stepwise_protocol_pdf.py`
5. `22_generate_plain_protocol_pdf.py`
6. `23_generate_protocol_docx.py`
7. `24_generate_detailed_protocol_pdf.py`
8. `25_build_pipseq_protocol_docx.py`

## 02. Most Important Scripts Right Now

If you only want the current project core, focus on:

1. `10_public_reference_statistical_prediction.py`
2. `17_cluster_public_reference.py`
3. `19_generate_public_reference_umaps.py`
4. `27_root_reference_consensus.py`

Environment note:

- the Scanpy-based scripts must be run inside the Conda environment created from `environment.yml`
- in the current local machine setup, they were validated in the `py311` environment rather than in base Python

## 03. Utility Files

- `pipeline_utils.py`: shared helper functions
- `run_all.sh`: convenience runner for the legacy FASTQ scaffold
- `00_preflight_check.py`: quick input and checkpoint sanity check
