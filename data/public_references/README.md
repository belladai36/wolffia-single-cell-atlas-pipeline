Public reference datasets for the transfer-learning workflow go here.

Expected files
- `arabidopsis_reference_train.h5ad`
- `arabidopsis_reference_test.h5ad`

These paths are defined in:
- `/Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/config/config.yaml`

Current status
- The Python environment is working in PyCharm.
- `scripts/10_public_reference_statistical_prediction.py` fails only because these `.h5ad` files are not present yet.

Suggested next move
1. Download or build one Arabidopsis training reference `.h5ad`.
2. Download or build one second Arabidopsis test `.h5ad`.
3. Place both files in this folder with the names above, or update `config/config.yaml` to match the filenames you use.

Downloaded starter datasets
- `raw/GSE227564_counts.csv.gz`
- `raw/GSE227564_metadata.csv.gz`
- `raw/GSE141730_aggregated_filtered_gene_bc_matrices.h5`

Current prepared outputs
- `processed/GSE227564_callus.h5ad`
- `processed/GSE141730_root_phosphate.h5ad`

Preparation script
- `/Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/scripts/11_prepare_public_references.py`

Notes
- `GSE227564` includes metadata and Seurat cluster assignments.
- `GSE141730` is a 10x HDF5 matrix and does not come with cell-type labels in the downloaded file.
