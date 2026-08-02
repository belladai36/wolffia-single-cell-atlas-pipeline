# Current Wolffia Analysis Workflow v1

This note is the current start-here workflow for the project. It connects the public Wolffia raw-data processing, the Arabidopsis-to-Wolffia transfer model, the Wolffia-native marker panel, and the future salt-stress analysis path.

## 1. Current project status

The project now has two complementary interpretation layers:

1. A conservative Arabidopsis-to-Wolffia transfer layer.
2. A Wolffia-native marker-program layer built from public Waus8730 single-cell data.

The transfer layer is useful for testing whether broad Arabidopsis-derived biological programs are recognizable in Wolffia. The native marker layer is more directly useful for future Wolffia datasets because it uses Waus8730 gene IDs and programs observed in public Wolffia data.

## 2. Main inputs

The large expression data are kept outside the repository. The repository tracks scripts, small metadata tables, notebooks, and documentation.

Key external inputs:

- public Waus8730 SRA or FASTQ files from `PRJNA1124135`
- Waus8730 genome FASTA and annotation GFF3/GTF files
- STARsolo count matrices generated from the public FASTQs
- normalized `.h5ad` files generated from the count matrices

Key repository inputs:

- `data/metadata/wolffia_reviewed_native_marker_panel_v1.csv`
- `data/metadata/wolffia_reviewed_native_marker_panel_v1_gene_coverage.csv`
- `data/metadata/wolffia_reviewed_native_marker_panel_v1_score_summary.csv`
- `scripts/36_apply_leaf_primary_and_root_benchmark.py`
- `scripts/40_score_future_wolffia_dataset.py`
- `scripts/41_freeze_reviewed_native_marker_panel_v1.py`
- `notebooks/14_public_wolffia_reviewed_marker_panel_v1_scoring.ipynb`

## 3. Workflow stages

### Stage 1. Public raw-data processing

The public Waus8730 runs are downloaded from SRA and converted into split FASTQ files. Each run has three FASTQ components:

- read 1: short sample/index read
- read 2: cell barcode plus UMI read
- read 3: RNA expression read

The useful structure for STARsolo is:

- cell barcode: first 16 bases of read 2
- UMI: next 12 bases of read 2
- RNA read: read 3

The large FASTQ conversion and STARsolo steps should be run on the compute cluster or external storage, not inside the GitHub repository.

### Stage 2. Waus8730 reference preparation

The Waus8730 genome FASTA and annotation are used to build a STAR index. The exon-level GTF version is preferred because it correctly records gene-level information for gene counting.

The current successful reference path uses:

- Waus8730 genome FASTA
- Waus8730 annotation converted to exon-level GTF
- STAR genome index with `genomeSAindexNbases 13`

### Stage 3. STARsolo count generation

STARsolo maps RNA reads to the Waus8730 reference and produces a 10x-style gene-by-cell matrix.

The main output files are:

- `barcodes.tsv`
- `features.tsv`
- `matrix.mtx`
- `Summary.csv`

The public Waus8730 runs processed so far give a total of 11,084 filtered cells across four runs. These matrices are used for QC, clustering, marker review, and native program scoring.

### Stage 4. Count-matrix normalization and clustering

The STARsolo matrices are loaded into AnnData, filtered, normalized, log-transformed, and clustered. This creates the working single-cell object used for:

- UMAP visualization
- cluster marker detection
- manual marker interpretation
- native program scoring
- future comparison with treatment datasets

The normalized data are large and should stay outside GitHub.

### Stage 5. Arabidopsis-to-Wolffia transfer model

The transfer model uses Arabidopsis references as a biological guide, but it only applies genes that can be mapped to Wolffia through orthology.

The root-derived benchmark starts from 2,000 Arabidopsis model features and narrows to 340 transferable genes after high- or medium-confidence ortholog filtering. A label is accepted only when the model has enough feature coverage and the model confidence passes the threshold. Otherwise, the cell is labeled ambiguous.

The current transfer interpretation is:

- leaf/aerial evidence is biologically more relevant to Wolffia than root evidence
- root evidence remains useful as a conservative benchmark
- ambiguous labels are expected and should not be treated as failure
- transfer labels are broad program hints, not final Wolffia cell-type names

### Stage 6. Wolffia-native marker-program discovery

Because Wolffia does not map cleanly onto Arabidopsis organs, the project also builds a Wolffia-native marker layer from public Waus8730 data.

This layer starts from public Wolffia cluster markers and groups genes into broad programs such as:

- photosynthesis and light harvesting
- carbon fixation and chloroplast metabolism
- stress and protein protection
- growth and biosynthesis
- cell wall or structural programs
- unknown but reproducible Wolffia marker states

This gives the project a more Wolffia-centered analysis route.

### Stage 7. Reviewed marker panel v1

The reviewed marker panel freezes a small, interpretable set of marker genes for future scoring.

Current reviewed panel:

- 60 marker-program rows
- 47 reviewed core markers
- 9 reviewed supporting markers
- 4 reviewed unknown-watchlist markers
- 100% coverage in the current public Waus8730 data

Main files:

- `data/metadata/wolffia_reviewed_native_marker_panel_v1.csv`
- `docs/wolffia_reviewed_native_marker_panel_v1.md`
- `notebooks/14_public_wolffia_reviewed_marker_panel_v1_scoring.ipynb`

### Stage 8. Future dataset scoring

Future Wolffia datasets can be scored against the reviewed native marker panel using:

```bash
python scripts/40_score_future_wolffia_dataset.py \
  /path/to/future_wolffia_normalized_log1p.h5ad \
  --panel data/metadata/wolffia_reviewed_native_marker_panel_v1.csv \
  --metadata /path/to/future_metadata.csv \
  --metadata-cell-id-column cell_id \
  --group-columns condition,sample_id,replicate,cluster,leiden \
  --output-dir /path/to/output/reviewed_v1_scores
```

The script writes cell-level program scores, group summaries, and a gene-coverage audit. The output filenames use generic marker-score naming, so they can be applied to public data, future control data, or future salt-stress data.

## 4. How to interpret the outputs

Use the Arabidopsis transfer model to ask:

- Which broad Arabidopsis-like programs are detectable in Wolffia?
- Which cells are confidently similar enough to transfer?
- Which cells remain ambiguous because Wolffia is biologically different or the ortholog feature space is limited?

Use the native marker panel to ask:

- Which Wolffia marker programs are active in each cell or cluster?
- Are photosynthesis, stress, growth, or unknown marker programs enriched in certain groups?
- Do future treatment samples shift program scores compared with controls?

The safest current interpretation is program-level, not cell-type-level. A program score says that a cell expresses a set of genes associated with a biological process. It does not by itself prove a final cell identity.

## 5. Best current next use

For future Wolffia control-versus-treatment data, the main analysis should:

1. process or receive a gene-by-cell matrix with Waus8730-compatible gene IDs
2. run QC, normalization, clustering, and UMAP
3. score the reviewed native marker panel v1
4. apply the Arabidopsis transfer model as a conservative secondary view
5. compare program scores by condition, sample, replicate, and cluster
6. manually inspect top marker genes before assigning biological names

