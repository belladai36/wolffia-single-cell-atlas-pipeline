# Wolffia Public Download Layout

## What we verified

The two public `Wolffia australiana` reference projects currently look like **raw sequencing-run
projects**, not downloadable processed matrices.

### Training candidate

- dataset id in this repo: `PRJNA1124135_scRNA`
- study accession: `SRP514015`
- local target folder:
  `data/public_references/raw/PRJNA1124135/scRNA_seq/`
- core scRNA-seq runs:
  - `SRR29417746` `Dawn1`
  - `SRR29417745` `Dawn2`
  - `SRR29417744` `Dusk1`
  - `SRR29417743` `Dusk2`

Approximate compressed download sizes from ENA:

- `SRR29417746`: `19.2 GB`
- `SRR29417745`: `23.6 GB`
- `SRR29417744`: `19.8 GB`
- `SRR29417743`: `20.1 GB`

Total compressed size is about **82.7 GB**, which is larger than the current free disk space in the
workspace machine.

Important note:

- The same BioProject also contains additional **bulk RNA-seq** runs for whole frond, top, bottom,
  mother, and daughter frond samples.
- For the first Wolffia-native reference, we should focus on the **four single-cell runs** above,
  not the bulk runs.

### Validation candidate

- dataset id in this repo: `PRJNA809022_snRNA`
- study accession: `SRP360930`
- local target folder:
  `data/public_references/raw/PRJNA809022/snRNA_seq/`
- runs:
  - `SRR18098970` through `SRR18098953`
  - corresponding to `Waus_snRNA-Seq_1` through `Waus_snRNA-Seq_18`

## Repo files updated for this

- manifest:
  [data/metadata/wolffia_public_dataset_manifest.csv](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/data/metadata/wolffia_public_dataset_manifest.csv)
- run table:
  [data/metadata/wolffia_public_run_accessions.csv](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/data/metadata/wolffia_public_run_accessions.csv)

## Recommended local directory structure

```text
data/public_references/raw/
  PRJNA1124135/
    scRNA_seq/
      SRR29417743.fastq.gz
      SRR29417744.fastq.gz
      SRR29417745.fastq.gz
      SRR29417746.fastq.gz
  PRJNA809022/
    snRNA_seq/
      SRR18098953_1.fastq.gz
      SRR18098953_2.fastq.gz
      ...
      SRR18098970_1.fastq.gz
      SRR18098970_2.fastq.gz
```

## What this means for the workflow

Because these are raw sequencing runs:

- `scripts/12_prepare_wolffia_public_references.py` cannot convert them directly into `.h5ad`
- we first need a **count-generation step**
- after counts or matrices exist, the manifest can be switched from:
  - `input_format=raw_fastq_dir`
  to one of:
  - `h5ad`
  - `10x_h5`
  - `10x_mtx_dir`

## Best immediate next move

1. free additional storage or use a larger external location before download
2. download the four `PRJNA1124135` scRNA-seq runs only
3. keep `PRJNA809022` as the secondary download after the first Wolffia workflow is proven
4. generate a matrix or count object for `PRJNA1124135`
5. update the manifest to point to that matrix
6. run [scripts/12_prepare_wolffia_public_references.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/12_prepare_wolffia_public_references.py)
