#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config/config.yaml}"

python - <<'PY' "$CONFIG"
import shlex
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

config_path = sys.argv[1]
with open(config_path, "r", encoding="utf-8") as handle:
    config = yaml.safe_load(handle)

samples = pd.read_csv(config["paths"]["sample_sheet"])
out_root = Path(config["paths"]["alignment_dir"])
log_dir = Path(config["paths"]["log_dir"])
out_root.mkdir(parents=True, exist_ok=True)
log_dir.mkdir(parents=True, exist_ok=True)

star_index = Path(config["paths"]["star_index"])
if not star_index.exists():
    raise SystemExit(f"STAR index not found: {star_index}")

paired = config["fastq"].get("paired_end", True)
threads = str(config["alignment"].get("threads", 8))
read_cmd = config["alignment"].get("read_files_command", "zcat")
extra = [str(x) for x in config["alignment"].get("star_extra_args", [])]

for _, row in samples.iterrows():
    cell_id = str(row["cell_id"])
    r1 = Path(row["fastq_r1"])
    r2 = Path(row["fastq_r2"]) if paired else None
    if not r1.exists() or (paired and not r2.exists()):
        raise SystemExit(f"Missing FASTQ for {cell_id}")

    cell_dir = out_root / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)
    prefix = str(cell_dir / f"{cell_id}.")
    reads = [str(r1), str(r2)] if paired else [str(r1)]
    cmd = [
        "STAR",
        "--runThreadN", threads,
        "--genomeDir", str(star_index),
        "--readFilesIn", *reads,
        "--readFilesCommand", read_cmd,
        "--outFileNamePrefix", prefix,
        *extra,
    ]
    print("Running:", " ".join(shlex.quote(x) for x in cmd))
    subprocess.run(cmd, check=True)

    bam = cell_dir / f"{cell_id}.Aligned.sortedByCoord.out.bam"
    if bam.exists():
        subprocess.run(["samtools", "index", str(bam)], check=True)
PY

