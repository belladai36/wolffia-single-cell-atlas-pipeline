# Scripts Guide

This folder contains both the main analysis scripts and the helper/export scripts.

## Best Way to Read This Folder

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

## Most Important Scripts Right Now

If you only want the current project core, focus on:

1. `10_public_reference_statistical_prediction.py`
2. `17_cluster_public_reference.py`
3. `19_generate_public_reference_umaps.py`

## Utility Files

- `pipeline_utils.py`: shared helper functions
- `run_all.sh`: convenience runner for the legacy FASTQ scaffold
- `00_preflight_check.py`: quick input and checkpoint sanity check
