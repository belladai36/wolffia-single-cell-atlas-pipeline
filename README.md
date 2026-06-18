# Wolffia SMART-seq Single-Cell RNA-seq Pipeline

This repository is a beginner-friendly, end-to-end scaffold for a Wolffia single-cell RNA-seq project before the real data arrive. It starts from per-cell SMART-seq FASTQ files, creates a gene-by-cell count matrix, and then runs a standard Scanpy analysis through QC, normalization, clustering, marker discovery, annotation, UMAP, PAGA trajectory inference, and robustness checks.

The paths are placeholders. Replace the example FASTQ, genome, annotation, and metadata paths with your project files when they are available.

## Project Layout

```text
.
├── config/
│   └── config.yaml                  # Edit paths and analysis parameters here
├── data/
│   ├── raw_fastq/                   # Put or symlink FASTQ files here
│   ├── reference/                   # Genome FASTA, GTF/GFF, STAR index
│   └── metadata/                    # Sample/cell metadata and marker tables
├── scripts/
│   ├── 00_fastq_qc.sh               # FastQC + MultiQC
│   ├── 01_align_smartseq_star.sh    # STAR alignment for SMART-seq reads
│   ├── 02_featurecounts.sh          # Gene-level counting from BAM files
│   ├── 03_build_count_matrix.py     # Merge per-cell counts into one matrix
│   ├── 04_cell_qc.py                # Cell QC and filtering flags
│   ├── 05_normalize_hvg_pca.py      # Normalize, log transform, HVGs, PCA
│   ├── 06_neighbors_leiden_umap.py  # KNN graph, Leiden clustering, UMAP
│   ├── 07_markers_annotation.py     # Marker genes and conservative annotation
│   ├── 08_paga_trajectory.py        # PAGA trajectory graph
│   ├── 09_robustness_checks.py      # Optional parameter sensitivity checks
│   ├── 14_extract_gse121619_from_monocle.R  # Export GEO Monocle CellDataSet into matrix/obs/var files
│   ├── 15_prepare_gse121619_h5ad.py         # Convert exported GSE121619 files into h5ad
│   └── run_all.sh                   # Convenience runner
├── results/                         # Count matrices, AnnData files, reports
├── figures/                         # QC, UMAP, marker, and PAGA plots
├── logs/                            # Tool logs
└── notebooks/                       # Optional exploratory notebooks
```

## Install

Install the Python and command-line tools with conda or mamba:

```bash
mamba env create -f environment.yml
conda activate wolffia-scrna
```

The upstream FASTQ steps expect these command-line tools in your `PATH`:

- `fastqc`
- `multiqc`
- `STAR`
- `samtools`
- `featureCounts` from Subread

## Inputs You Need

Edit [config/config.yaml](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/config/config.yaml>) before running.

Minimum inputs:

- Paired-end or single-end SMART-seq FASTQ files, one library per cell.
- A Wolffia genome FASTA file.
- A gene annotation GTF file. Convert GFF3 to GTF first if needed.
- A sample sheet like [data/metadata/samples.csv](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/data/metadata/samples.csv>).
- Optional known marker genes like [data/metadata/marker_genes.csv](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/data/metadata/marker_genes.csv>).

## Run Step by Step

### 1. FASTQ Quality Control

```bash
bash scripts/00_fastq_qc.sh config/config.yaml
```

Outputs:

- FastQC HTML reports in `results/fastqc/`
- MultiQC report in `results/multiqc/`

### 2. Align SMART-seq Reads

SMART-seq data usually do not have 10x-style cell barcodes. This scaffold assumes each FASTQ pair is one cell, aligns each cell independently with STAR, then counts genes per cell.

Build a STAR index first if you do not already have one:

```bash
STAR \
  --runThreadN 8 \
  --runMode genomeGenerate \
  --genomeDir data/reference/star_index \
  --genomeFastaFiles data/reference/Wolffia_genome.fa \
  --sjdbGTFfile data/reference/Wolffia_genes.gtf \
  --sjdbOverhang 99
```

Then align:

```bash
bash scripts/01_align_smartseq_star.sh config/config.yaml
```

### 3. Count Genes

```bash
bash scripts/02_featurecounts.sh config/config.yaml
python scripts/03_build_count_matrix.py --config config/config.yaml
```

Outputs:

- `results/counts/gene_by_cell_counts.csv`
- `results/scanpy/00_raw_counts.h5ad`

### 4. Cell QC

```bash
python scripts/04_cell_qc.py --config config/config.yaml
```

This computes QC metrics, saves threshold plots, and flags cells in `adata.obs["passes_qc"]`. The default config writes a filtered `.h5ad` containing passing cells, while `results/scanpy/qc_summary.json` records the filter decisions so you can audit what happened.

### 5. Normalize, Log Transform, HVGs, PCA

```bash
python scripts/05_normalize_hvg_pca.py --config config/config.yaml
```

This preserves raw counts in `adata.layers["counts"]`, normalizes each cell to the configured library size, log-transforms expression, selects highly variable genes, scales, and runs PCA.

### 6. KNN Graph, Leiden Clustering, UMAP

```bash
python scripts/06_neighbors_leiden_umap.py --config config/config.yaml
```

### 7. Marker Genes and Annotation

```bash
python scripts/07_markers_annotation.py --config config/config.yaml
```

Annotation is intentionally conservative. If marker genes are missing or ambiguous, clusters are labeled `unknown` rather than over-interpreted.

### 8. PAGA Trajectory Inference

```bash
python scripts/08_paga_trajectory.py --config config/config.yaml
```

PAGA is most useful after you have reviewed QC, clustering, and marker biology. Treat it as a hypothesis-generating view of possible transitions, not proof of developmental order.

### 9. Optional Robustness Checks

```bash
python scripts/09_robustness_checks.py --config config/config.yaml
```

This reruns neighbor graph and Leiden clustering across PCA dimensions, Leiden resolutions, and neighbor numbers, then reports how stable cluster assignments are.

## One-Command Demo Runner

After the config points to real files:

```bash
bash scripts/run_all.sh config/config.yaml
```

For a first real dataset, run step by step instead of using `run_all.sh`; it is easier to inspect QC and catch path mistakes.

## Statistical Prediction on Public References

Before Wolffia data arrive, you can run a public-reference statistical workflow that:

1. reads two annotated public plant `.h5ad` datasets
2. collapses detailed labels into broad biological programs
3. computes program scores from marker sets
4. trains a simple classifier on one dataset
5. tests label transfer on a second dataset
6. writes summary figures and metrics

Starter inputs live in:

- [data/metadata/public_reference_program_markers.csv](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/data/metadata/public_reference_program_markers.csv>)
- [data/metadata/public_reference_label_rules.csv](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/data/metadata/public_reference_label_rules.csv>)

Configure the dataset paths under `public_reference_analysis` in [config/config.yaml](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/config/config.yaml>), then run:

```bash
python scripts/10_public_reference_statistical_prediction.py --config config/config.yaml
```

To prepare the next Arabidopsis validation dataset `GSE121619` from its GEO Monocle object:

```bash
Rscript scripts/14_extract_gse121619_from_monocle.R All
python scripts/15_prepare_gse121619_h5ad.py --split All
python scripts/10_public_reference_statistical_prediction.py --config config/public_reference_gse121619.yaml
```

This keeps the main config unchanged while letting you test a second Arabidopsis validation target.

Expected outputs include:

- `results/public_reference/cross_dataset_metrics.json`
- `results/public_reference/cross_dataset_classification_report.csv`
- `results/public_reference/train_reference_scored.h5ad`
- `results/public_reference/test_reference_scored.h5ad`
- `figures/public_reference/train_broad_program_umap.png`
- `figures/public_reference/test_broad_program_umap.png`
- `figures/public_reference/train_program_score_heatmap.png`
- `figures/public_reference/cross_dataset_confusion_matrix.png`
- `figures/public_reference/test_predicted_broad_program_umap.png`

## Notes for Wolffia

- Wolffia organelle gene names may not follow human-style `MT-` prefixes. Edit `mitochondrial_gene_prefixes` and `plastid_gene_prefixes` in `config/config.yaml` after inspecting the annotation.
- SMART-seq has full-length transcript coverage and no UMIs. Counts are read counts, not molecule counts, so doublet detection and QC heuristics differ from droplet scRNA-seq.
- Plant cells can have strong chloroplast/plastid signal. This pipeline computes plastid fractions when prefixes are provided, but does not hard-filter on plastid percentage by default.
- Marker-based annotation is only as good as the marker table. Keep early labels coarse, especially for an under-annotated organism.

## Main Outputs

- `results/scanpy/00_raw_counts.h5ad`
- `results/scanpy/01_qc_flagged.h5ad`
- `results/scanpy/02_pca.h5ad`
- `results/scanpy/03_clustered_umap.h5ad`
- `results/scanpy/04_markers_annotated.h5ad`
- `results/scanpy/05_paga.h5ad`
- `results/scanpy/robustness_summary.csv`
- QC, UMAP, marker, and PAGA figures under `figures/`

## Prediction-First Planning Docs

Before Wolffia SMART-seq data arrive, the project is also organized around a prediction-first comparative biology workflow:

- [Project aims](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/project_aims.md>)
- [Reference datasets](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/reference_datasets.md>)
- [Dataset inventory](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/dataset_inventory.md>)
- [Prediction framework](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/prediction_framework.md>)
- [Statistical prediction strategy](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/statistical_prediction_strategy.md>)
- [Candidate cell programs](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/candidate_cell_programs.md>)
- [First-pass Wolffia mapping notes](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/wolffia_mapping_notes.md>)
- [Phase 1 public-data workplan](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/phase1_public_data_workplan.md>)
- [Validation experiment plan](</Users/bella/Documents/Wolffia Single-Cell Atlas Pipeline Before the Data Arrive/docs/validation_experiment_plan.md>)
# wolffia-single-cell-atlas-pipeline
