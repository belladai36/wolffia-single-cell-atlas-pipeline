# Cluster-Based Raw Data Processing

## Purpose

Large public Wolffia sequencing runs should be processed on a compute cluster rather than on a
laptop. Raw SRA conversion can create hundreds of gigabytes of temporary files before any final
FASTQ or count matrix is produced.

The repository should remain the reproducible code and documentation layer. Large raw data,
temporary files, and generated matrices should stay outside GitHub.

## Current Cluster Progress

Use a project or lab scratch workspace with enough storage. For example:

```text
/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell
```

The project folder contains:

```text
wolffia_single_cell/
├── data/
│   ├── raw_sra/
│   ├── raw_fastq/
│   └── reference/
├── results/
├── logs/
├── tmp/
└── tools/
```

SRA Toolkit can be installed locally in the project workspace:

```text
/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/tools/sratoolkit.3.4.1-alma_linux64
```

The first pilot run is:

```text
SRR29417746
```

This run is part of the public Wolffia project `PRJNA1124135`. It is being used as a pilot before
launching the remaining runs, because the first goal is to confirm the read structure.

## Why Only One Run First

The pilot run is intended to answer:

- which split read contains the cell barcode
- which split read contains the UMI
- which split read contains the cDNA/transcript sequence
- whether the dataset can be converted into a gene-by-cell count matrix with the available metadata

The remaining runs should not be processed until this read structure is confirmed.

## Storage Expectation

For one SRA run, temporary storage may reach several hundred gigabytes. A practical planning range
for the pilot run is:

```text
300-700 GB temporary space
```

Large intermediate files should be deleted or compressed after the needed read-structure and count
matrix outputs are confirmed.

## SLURM Submission Pattern

The cluster uses SLURM. The submission pattern is:

```bash
sbatch -A CLUSTER_ACCOUNT -p CPU_PARTITION scripts_run_fasterq_SRR29417746.slurm
```

The job can be monitored with:

```bash
squeue -u USERNAME
```

Log files are written under:

```text
/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/logs
```

## Pilot Job Script

The pilot script should export the project-local SRA Toolkit path, download one SRA run, and split
technical reads:

```bash
#!/bin/bash
#SBATCH --job-name=wolffia_fasterq
#SBATCH --output=/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/logs/%x_%j.out
#SBATCH --error=/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/logs/%x_%j.err
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G

set -euo pipefail

PROJECT=/scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell
RUN=SRR29417746

export PATH="$PROJECT/tools/sratoolkit.3.4.1-alma_linux64/bin:$PATH"

mkdir -p $PROJECT/data/raw_sra/PRJNA1124135
mkdir -p $PROJECT/data/raw_fastq/PRJNA1124135/scRNA_seq_split
mkdir -p $PROJECT/tmp/$RUN

cd $PROJECT/data/raw_sra/PRJNA1124135

prefetch --max-size u $RUN

fasterq-dump $RUN \
  --split-files \
  --include-technical \
  --threads 8 \
  --outdir $PROJECT/data/raw_fastq/PRJNA1124135/scRNA_seq_split \
  --temp $PROJECT/tmp/$RUN

echo "Finished $RUN"
ls -lh $PROJECT/data/raw_fastq/PRJNA1124135/scRNA_seq_split
```

## After the Pilot Finishes

Inspect the split FASTQ files:

```bash
ls -lh /scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/data/raw_fastq/PRJNA1124135/scRNA_seq_split
```

Check read lengths:

```bash
for f in /scratch2/fs1/PROJECT_OR_LAB_ACCOUNT/wolffia_single_cell/data/raw_fastq/PRJNA1124135/scRNA_seq_split/SRR29417746*.fastq; do
  echo "$f"
  awk 'NR%4==2 {print length($0); if (++n==20) exit}' "$f" | sort | uniq -c
done
```

Expected interpretation:

- short technical reads are candidates for barcode and UMI information
- longer reads are candidates for cDNA/transcript sequence
- the final count pipeline depends on this structure

## Relationship to External Storage

The compute cluster is the preferred place for heavy raw-data conversion and temporary files.

External project storage is still useful for:

- backing up final processed matrices
- transferring selected outputs between the cluster and laptop
- storing final `.h5ad`, `matrix.mtx`, `barcodes.tsv`, or `features.tsv` files

The laptop should be used mainly for:

- code development
- notebooks
- figures
- model interpretation
- small validation checks

## Immediate Next Decision

After the pilot split FASTQ files are inspected, choose the count-generation path:

1. 10x-style workflow if the barcode, UMI, and cDNA reads match a known structure
2. custom barcode/UMI extraction if the data use a nonstandard single-cell format
3. processed-matrix workflow if the publication provides a count matrix or Seurat/AnnData object

The desired output for the transfer model remains:

```text
input_wolffia_normalized.h5ad
```
