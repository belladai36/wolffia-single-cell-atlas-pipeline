# External Data Storage Guide

## Purpose

This document explains how to use external project storage for large Wolffia and public-reference data
while keeping the GitHub repository lightweight.

The repository should store:

- scripts
- notebooks
- documentation
- small metadata tables
- reproducible configuration files

External storage should store:

- raw FASTQ files
- downloaded SRA files
- large `.h5ad` files
- genome/reference downloads
- temporary alignment/counting outputs
- large generated results that should not be committed to GitHub

## Check Whether External Storage Is Mounted

In Terminal:

```bash
ls /Volumes
df -h
```

The external volume should appear as something like:

```text
/Volumes/LaCie
```

If it does not appear, unplug/replug it or check Disk Utility.

## Recommended External Storage Folder Layout

The current mounted external volume is `/Volumes/LaCie`. If the drive is renamed later, replace `LaCie` with the actual mounted volume name:

```bash
EXTERNAL_DATA="/Volumes/LaCie"

mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/data/raw_sra"
mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/data/raw_fastq"
mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/data/reference"
mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/data/processed_h5ad"
mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/results"
mkdir -p "$EXTERNAL_DATA/wolffia_single_cell/logs"
```

Suggested layout:

```text
wolffia_single_cell/
├── data/
│   ├── raw_sra/
│   ├── raw_fastq/
│   ├── reference/
│   └── processed_h5ad/
├── results/
└── logs/
```

## Keep GitHub Clean

Do not commit large data files.

The repo already ignores:

```text
results/
figures/
logs/
data/public_references/raw/
data/public_references/processed/
data/reference/
```

Use external storage for those large files and keep the repo focused on code and documentation.

## Optional Symlink Strategy

If you want scripts to keep using familiar repo paths while the actual files live on external storage, use
symlinks.

Example:

```bash
cd "/Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive"

mkdir -p data

ln -s "/Volumes/LaCie/wolffia_single_cell/data/raw_fastq" data/raw_fastq
ln -s "/Volumes/LaCie/wolffia_single_cell/data/reference" data/reference_external
ln -s "/Volumes/LaCie/wolffia_single_cell/data/processed_h5ad" data/wolffia_processed_h5ad
```

Before making symlinks, check whether a folder already exists:

```bash
ls -lh data
```

Do not overwrite existing folders unless you have moved or backed them up.

## First Real Wolffia Data Goal

The first external-storage-backed target should be:

```text
download public Wolffia data
↓
convert or process into a normalized h5ad
↓
run combined leaf-primary + root-benchmark application script
```

Expected application command:

```bash
python scripts/36_apply_leaf_primary_and_root_benchmark.py \
  /Volumes/LaCie/wolffia_single_cell/data/processed_h5ad/input_wolffia_normalized.h5ad \
  --gene-id-column wolffia_gene_id
```

## Practical Next Terminal Check

After connecting the external volume, run:

```bash
ls /Volumes
df -h
```

If the volume name changes, replace `/Volumes/LaCie` in the commands above with the exact mounted volume path.

## Bottom Line

External project storage should become the home for large biological data. The GitHub repository should remain the
clean, reproducible instruction layer that points to local or external data paths.
