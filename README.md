# Wolffia PIP-seq Single-Cell Atlas Framework

This repository is a beginner-friendly, prediction-first scaffold for a `Wolffia australiana` single-cell project before the real data arrive. The current planned experimental platform is `PIP-seq`. The repo therefore combines:

- a comparative public-reference workflow for biological prediction and label transfer
- Wolffia-facing planning and validation documents
- a legacy FASTQ-level alignment-and-counting scaffold that can still be useful for full-length or custom raw-data workflows

The paths are placeholders. Replace the example FASTQ, genome, annotation, and metadata paths with your project files when they are available.

## 1. Start Here

If you are opening this repository for the first time, these are the most useful entry points:

1. [Project progress summary](docs/project_progress_summary.md)
2. [Project aims](docs/project_aims.md)
3. [Docs guide](docs/README.md)
4. [Wolffia first transfer note](docs/wolffia_first_transfer_note.md)

## 2. Recommended Reading Order

For most viewers, the easiest way through the repository is:

1. [Project progress summary](docs/project_progress_summary.md) for the current state
2. [Project aims](docs/project_aims.md) for the biological motivation
3. [Prediction framework](docs/prediction_framework.md) for the main hypothesis logic
4. [Root-derived reference update](docs/root_derived_reference_update.md) for the most important computational lesson so far
5. [Arabidopsis leaf reference extension plan](docs/leaf_reference_extension_plan.md) for the next root-versus-leaf reference comparison
6. [Wolffia first transfer note](docs/wolffia_first_transfer_note.md) for how the model will be applied to Wolffia
7. [Frozen Wolffia transfer model v1](docs/final_wolffia_transfer_model.md) for the exact model and rejection rule
8. [Wolffia data-generation protocol](docs/wolffia_data_generation_protocol.md) for the planned experimental route

## 3. Current Status

The project is currently in the **Wolffia-facing transfer preparation stage**.

What that means:

- the Arabidopsis reference-and-transfer framework has been built and tested
- the broad program set has been refined into a more interpretable working ontology
- the current reference layer is ready for a first Wolffia-facing pass
- the provisional 340-feature Wolffia transfer model and conservative decision rule are frozen
- the next reference refinement is an Arabidopsis root-versus-leaf comparison
- actual Wolffia training is waiting on download, preprocessing, or arrival of new Wolffia `PIP-seq` matrices

Current public Wolffia plan:

- `PRJNA1124135` as the first training dataset
- `PRJNA809022` as the validation dataset

Current lab-data plan:

- new Wolffia single-cell libraries are being generated using `PIP-seq`
- when those matrices become available, they should be analyzed with both the frozen root-derived view and the new leaf/aerial reference view

Current model snapshot:

- the within-Arabidopsis benchmark starts from the top 2,000 variable/shared genes selected from
  the GSE123818 wild-type root reference
- reciprocal Arabidopsis-to-Wolffia protein mapping reduces that benchmark feature space to
  340 high- or medium-confidence transferable ortholog features
- the restricted 340-feature model is the only model intended for Wolffia application
- the frozen rule emits a provisional program only when calibrated logistic regression and random
  forest agree at confidence `>= 0.60`; otherwise the cell remains `ambiguous`
- on held-out Arabidopsis pseudo-labels, the restricted consensus accepted `30.4%` of cells with
  `95.3%` selective accuracy

The clearest current progress summary is here:

- [Project progress summary](docs/project_progress_summary.md)
- [Arabidopsis leaf reference extension plan](docs/leaf_reference_extension_plan.md)
- [Frozen Wolffia transfer model v1](docs/final_wolffia_transfer_model.md)

Selected first leaf reference:

- `GSE161332`, an Arabidopsis leaf scRNA-seq matrix used for the first root-versus-leaf comparison
- [GSE161332 leaf reference test summary](docs/gse161332_leaf_reference_test_summary.md)

## 4. Project Layout

```text
.
├── config/
│   ├── config.yaml                  # Main project config
│   └── README.md                    # Which config file is for which workflow
├── data/
│   ├── raw_fastq/                   # Put or symlink FASTQ files here
│   ├── reference/                   # Genome FASTA, GTF/GFF, STAR index
│   └── metadata/                    # Sample/cell metadata and marker tables
├── docs/                            # Project narrative, plans, results, and protocols
├── scripts/
│   ├── README.md                    # Script order and what each group does
│   ├── 00_fastq_qc.sh               # FastQC + MultiQC
│   ├── 01_align_pipseq_star.sh      # Legacy STAR alignment route for per-cell FASTQ workflows
│   ├── 02_featurecounts.sh          # Legacy gene-level counting from BAM files
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
├── notebooks/                       # Optional exploratory notebooks
└── output/                          # Shareable PDF and DOCX exports
```

## 5. Folder Guide

- [docs/README.md](docs/README.md): best entry point for understanding the project
- [scripts/README.md](scripts/README.md): best entry point for running code in the right order
- [config/README.md](config/README.md): best entry point for choosing config files
- [notebooks/README.md](notebooks/README.md): optional exploratory analysis notes
- [output/README.md](output/README.md): generated summary and protocol exports

## 6. Install

Install the Python and command-line tools with conda or mamba:

```bash
mamba env create -f environment.yml
conda activate wolffia-scrna
```

The legacy FASTQ steps expect these command-line tools in your `PATH`:

- `fastqc`
- `multiqc`
- `STAR`
- `samtools`
- `featureCounts` from Subread

Important environment note:

- the analysis scripts assume the Conda environment created from `environment.yml`
- if you run them from a plain base Python without `scanpy` installed, the public-reference and Scanpy-based workflows will fail immediately

## 7. Inputs You Need

Edit [config/config.yaml](config/config.yaml) before running.

For the current prediction-first and transfer workflow, the key inputs are:

- processed public reference `.h5ad` files
- marker tables and label-collapse rules under `data/metadata/`
- later, a processed Wolffia matrix or `.h5ad` derived from the lab's `PIP-seq` output

If you want to run the legacy FASTQ scaffold, the minimum inputs are:

- Paired-end or single-end per-cell FASTQ files, one library per cell.
- A Wolffia genome FASTA file.
- A gene annotation GTF file. Convert GFF3 to GTF first if needed.
- A sample sheet like [data/metadata/samples.csv](data/metadata/samples.csv).
- Optional known marker genes like [data/metadata/marker_genes.csv](data/metadata/marker_genes.csv).

## 8. Run Step by Step

The commands below describe the **legacy FASTQ-to-count-matrix route**. They remain useful if the lab or core provides raw per-cell FASTQs or if we need a custom alignment workflow.

### 1. FASTQ Quality Control

```bash
bash scripts/00_fastq_qc.sh config/config.yaml
```

Outputs:

- FastQC HTML reports in `results/fastqc/`
- MultiQC report in `results/multiqc/`

### 2. Align Per-Cell Reads

This scaffold assumes each FASTQ pair is one cell, aligns each cell independently with STAR, then counts genes per cell.

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
bash scripts/01_align_pipseq_star.sh config/config.yaml
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

## 9. One-Command Demo Runner

After the config points to real files:

```bash
bash scripts/run_all.sh config/config.yaml
```

For a first real dataset, run step by step instead of using `run_all.sh`; it is easier to inspect QC and catch path mistakes.

## 10. Statistical Prediction on Public References

Before Wolffia data arrive, you can run a public-reference statistical workflow that:

1. reads two annotated public plant `.h5ad` datasets
2. collapses detailed labels into broad biological programs
3. computes program scores from marker sets
4. trains a simple classifier on one dataset
5. tests label transfer on a second dataset
6. writes summary figures and metrics

Starter inputs live in:

- [data/metadata/public_reference_program_markers.csv](data/metadata/public_reference_program_markers.csv)
- [data/metadata/public_reference_label_rules.csv](data/metadata/public_reference_label_rules.csv)

Configure the dataset paths under `public_reference_analysis` in [config/config.yaml](config/config.yaml), then run:

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

To prepare the broader Arabidopsis root atlas `GSE123818` from GEO CSV matrices:

```bash
python scripts/16_prepare_gse123818_h5ad.py --split both
python scripts/10_public_reference_statistical_prediction.py --config config/public_reference_gse123818.yaml
```

This gives us a larger unlabeled developmental target to test whether the stress-like program still dominates during cross-dataset transfer.

To promote the `GSE123818 WT` atlas into a root-derived training reference:

```bash
python scripts/17_cluster_public_reference.py \
  --input data/public_references/processed/GSE123818_wt_root.h5ad \
  --output data/public_references/processed/GSE123818_wt_root_clustered.h5ad

python scripts/10_public_reference_statistical_prediction.py \
  --config config/public_reference_gse123818_wt_train_to_shr.yaml

python scripts/10_public_reference_statistical_prediction.py \
  --config config/public_reference_gse123818_wt_train_to_gse121619.yaml
```

This tests whether a root-derived reference reduces the strong stress-like collapse we saw when training on callus.

To benchmark two classifiers with entire GSE123818 clusters held out and build a conservative two-dataset root consensus model:

```bash
python scripts/27_root_reference_consensus.py
```

This comparison uses logistic regression and random forest. GSE121619 cells enter the provisional consensus set only when both models agree with each other and with the strongest marker module at the configured confidence thresholds. Review the executed notebook at `notebooks/02_root_consensus_benchmark.ipynb` and the interpretation in `docs/root_consensus_benchmark_summary.md`.

To prepare cross-species-compatible features:

```bash
bash scripts/28_download_orthology_references.sh
python scripts/29_build_arabidopsis_wolffia_orthologs.py
python scripts/30_transfer_model_benchmark_and_marker_audit.py
```

This uses pinned RefSeq protein annotations and reciprocal DIAMOND searches. The generated `data/metadata/wolffia_transfer_feature_set.csv` contains only high- and medium-confidence reciprocal mappings. See `docs/ortholog_mapping_summary.md` for confidence rules and limitations.

The final comparison and biological-program coverage audit are summarized in [docs/transfer_model_and_marker_audit.md](docs/transfer_model_and_marker_audit.md).

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

## 11. Notes for Wolffia

- Wolffia organelle gene names may not follow human-style `MT-` prefixes. Edit `mitochondrial_gene_prefixes` and `plastid_gene_prefixes` in `config/config.yaml` after inspecting the annotation.
- If the lab's `PIP-seq` workflow returns a processed matrix or `.h5ad` rather than per-cell FASTQs, start from the downstream Scanpy and transfer-analysis stages instead of forcing the legacy STAR and featureCounts route.
- Because the planned experimental platform is `PIP-seq`, future wet-lab success will depend heavily on low-debris, low-clump sample preparation and on matching the core facility's loading requirements.
- Plant cells can have strong chloroplast/plastid signal. This pipeline computes plastid fractions when prefixes are provided, but does not hard-filter on plastid percentage by default.
- Marker-based annotation is only as good as the marker table. Keep early labels coarse, especially for an under-annotated organism.

## 12. Main Outputs

- `results/scanpy/00_raw_counts.h5ad`
- `results/scanpy/01_qc_flagged.h5ad`
- `results/scanpy/02_pca.h5ad`
- `results/scanpy/03_clustered_umap.h5ad`
- `results/scanpy/04_markers_annotated.h5ad`
- `results/scanpy/05_paga.h5ad`
- `results/scanpy/robustness_summary.csv`
- QC, UMAP, marker, and PAGA figures under `figures/`

## 13. Prediction-First Planning Docs

Before Wolffia `PIP-seq` data arrive, the project is organized around a prediction-first comparative biology workflow:

- [Project aims](docs/project_aims.md)
- [Reference datasets](docs/reference_datasets.md)
- [Dataset inventory](docs/dataset_inventory.md)
- [Prediction framework](docs/prediction_framework.md)
- [Statistical prediction strategy](docs/statistical_prediction_strategy.md)
- [Candidate cell programs](docs/candidate_cell_programs.md)
- [First-pass Wolffia mapping notes](docs/wolffia_mapping_notes.md)
- [Phase 1 public-data workplan](docs/phase1_public_data_workplan.md)
- [Validation experiment plan](docs/validation_experiment_plan.md)

## 14. License

This repository is **not open source**. All rights are reserved by Jinglan Dai.
Use, modification, redistribution, sublicensing, commercialization, or derivative work requires
prior written permission. See [LICENSE](LICENSE).

## 15. Citations

Please cite this repository with [CITATION.cff](CITATION.cff). Upstream datasets, genome
resources, software, and method papers are listed in [docs/references.md](docs/references.md) and
provided as BibTeX in [references.bib](references.bib).
