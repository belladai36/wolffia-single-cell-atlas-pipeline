#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config/config.yaml}"

bash scripts/00_fastq_qc.sh "$CONFIG"
bash scripts/01_align_star.sh "$CONFIG"
bash scripts/02_featurecounts.sh "$CONFIG"
python scripts/03_build_count_matrix.py --config "$CONFIG"
python scripts/04_cell_qc.py --config "$CONFIG"
python scripts/05_normalize_hvg_pca.py --config "$CONFIG"
python scripts/06_neighbors_leiden_umap.py --config "$CONFIG"
python scripts/07_markers_annotation.py --config "$CONFIG"
python scripts/08_paga_trajectory.py --config "$CONFIG"
python scripts/09_robustness_checks.py --config "$CONFIG"

echo "Pipeline complete. Review results/scanpy and figures/."
