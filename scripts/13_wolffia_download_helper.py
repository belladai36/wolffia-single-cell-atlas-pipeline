#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

from pipeline_utils import load_config, project_path


DEFAULT_RUN_TABLE = project_path("data/metadata/wolffia_public_run_accessions.csv")


def load_runs(run_table: Path, dataset_id: str) -> list[dict[str, str]]:
    with open(run_table, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    filtered = [row for row in rows if row["dataset_id"] == dataset_id]
    if not filtered:
        raise ValueError(f"No runs found for dataset_id={dataset_id}")
    return filtered


def external_raw_root_from_env_or_config(config_path: str | Path = "config/config.yaml") -> Path | None:
    env_value = os.environ.get("WOLFFIA_PUBLIC_RAW_ROOT")
    if env_value:
        return Path(env_value).expanduser().resolve()
    config = load_config(config_path)
    cfg_value = config.get("wolffia_public_reference_analysis", {}).get("external_raw_root")
    if cfg_value:
        return Path(str(cfg_value)).expanduser().resolve()
    return None


def target_dir_for(dataset_id: str, external_root: Path | None = None) -> Path:
    if dataset_id == "PRJNA1124135_scRNA":
        internal = Path("PRJNA1124135/scRNA_seq")
        return (external_root / internal).resolve() if external_root else project_path(
            "data/public_references/raw/PRJNA1124135/scRNA_seq"
        )
    if dataset_id == "PRJNA809022_snRNA":
        internal = Path("PRJNA809022/snRNA_seq")
        return (external_root / internal).resolve() if external_root else project_path(
            "data/public_references/raw/PRJNA809022/snRNA_seq"
        )
    raise ValueError(f"No target directory rule defined for dataset_id={dataset_id}")


def print_prefetch_commands(runs: list[dict[str, str]], target_dir: Path) -> None:
    print("# Option 1: SRA Toolkit style download")
    print(f"mkdir -p '{target_dir}'")
    print("")
    for row in runs:
        run = row["run_accession"]
        print(f"prefetch {run}")
        print(f"fasterq-dump {run} -O '{target_dir}' --split-files")
        print(f"gzip '{target_dir}/{run}_1.fastq'")
        print(f"gzip '{target_dir}/{run}_2.fastq'")
        print("")


def print_ena_commands(runs: list[dict[str, str]], target_dir: Path) -> None:
    print("# Option 2: ENA direct FASTQ download")
    print(f"mkdir -p '{target_dir}'")
    print("")
    for row in runs:
        run = row["run_accession"]
        url = row.get("ena_fastq_url", "").strip()
        if not url:
            print(f"# {run}: ENA FASTQ URL not filled in yet")
            print("")
            continue
        print(f"# {run}")
        print(f"curl -L '{url}' -o '{target_dir}/{run}.fastq.gz'")
        print("")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print download commands for public Wolffia reference runs.")
    parser.add_argument(
        "--dataset-id",
        default="PRJNA1124135_scRNA",
        choices=["PRJNA1124135_scRNA", "PRJNA809022_snRNA"],
        help="Which dataset to prepare download commands for.",
    )
    parser.add_argument(
        "--mode",
        default="prefetch",
        choices=["prefetch", "ena"],
        help="Command style to print.",
    )
    parser.add_argument(
        "--make-dirs",
        action="store_true",
        help="Create the target raw-data directory locally.",
    )
    parser.add_argument(
        "--target-root",
        default=None,
        help="Optional external raw-data root, for example /Volumes/MyDrive/wolffia_public_raw",
    )
    args = parser.parse_args()

    runs = load_runs(DEFAULT_RUN_TABLE, args.dataset_id)
    external_root = (
        Path(args.target_root).expanduser().resolve()
        if args.target_root
        else external_raw_root_from_env_or_config()
    )
    target_dir = target_dir_for(args.dataset_id, external_root=external_root)

    if args.make_dirs:
        target_dir.mkdir(parents=True, exist_ok=True)

    print(f"# Dataset: {args.dataset_id}")
    print(f"# Target directory: {target_dir}")
    print(f"# Runs: {', '.join(row['run_accession'] for row in runs)}")
    print("")

    if args.mode == "prefetch":
        print_prefetch_commands(runs, target_dir)
    else:
        print_ena_commands(runs, target_dir)


if __name__ == "__main__":
    main()
