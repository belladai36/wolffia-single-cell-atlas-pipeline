#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_utils import load_config, project_path


def check_paths(label: str, paths: list[tuple[str, Path]]) -> int:
    print(f"\n[{label}]")
    missing = 0
    for name, path in paths:
        exists = path.exists()
        status = "OK" if exists else "MISSING"
        print(f"{status:8} {name}: {path}")
        if not exists:
            missing += 1
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether required project inputs exist before running the pipeline.")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    paths = config["paths"]
    public_ref = config.get("public_reference_analysis", {})

    missing = 0

    missing += check_paths(
        "Core metadata and references",
        [
            ("sample_sheet", project_path(paths["sample_sheet"])),
            ("marker_genes", project_path(paths["marker_genes"])),
            ("genome_fasta", project_path(paths["genome_fasta"])),
            ("annotation_gtf", project_path(paths["annotation_gtf"])),
            ("raw_fastq_dir", project_path(paths["raw_fastq_dir"])),
        ],
    )

    missing += check_paths(
        "Intermediate outputs required for downstream Scanpy steps",
        [
            ("00_raw_counts.h5ad", project_path(paths["scanpy_dir"]) / "00_raw_counts.h5ad"),
            ("01_qc_filtered.h5ad", project_path(paths["scanpy_dir"]) / "01_qc_filtered.h5ad"),
            ("02_pca.h5ad", project_path(paths["scanpy_dir"]) / "02_pca.h5ad"),
            ("03_clustered_umap.h5ad", project_path(paths["scanpy_dir"]) / "03_clustered_umap.h5ad"),
        ],
    )

    if public_ref:
        missing += check_paths(
            "Public reference transfer workflow",
            [
                ("train_h5ad", project_path(public_ref["train_h5ad"])),
                ("test_h5ad", project_path(public_ref["test_h5ad"])),
                ("label_rules_csv", project_path(public_ref["label_rules_csv"])),
                ("program_markers_csv", project_path(public_ref["program_markers_csv"])),
            ],
        )

    print("\nSummary")
    if missing:
        print(f"Missing {missing} required input(s) or intermediate file(s).")
        print("Fix those missing files before running downstream steps.")
    else:
        print("Everything required by the configured workflow is present.")


if __name__ == "__main__":
    main()
