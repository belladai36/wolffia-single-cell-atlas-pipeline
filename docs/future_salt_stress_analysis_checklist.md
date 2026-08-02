# Future Wolffia Salt-Stress Analysis Checklist

This checklist summarizes what should be collected before applying the current Wolffia analysis framework to future control-versus-salt datasets.

## 1. Minimum dataset information

Please record:

- species and accession
- control condition
- salt concentration
- treatment duration
- number of biological replicates per condition
- sample names
- library names
- sequencing run names
- expected recovered cells per sample, if known
- any known batch information

If some details are not decided yet, that is fine. The analysis can be planned first and finalized once the sequencing output is available.

## 2. Preferred data formats

The project can work from several input levels.

Best input:

- normalized `.h5ad` file with Waus8730 gene IDs and sample metadata

Also useful:

- raw 10x-style matrix folder with `barcodes.tsv`, `features.tsv`, and `matrix.mtx`
- filtered 10x-style matrix folder
- Seurat object
- raw FASTQ files

If FASTQ files are provided, also confirm:

- which sequencing or single-cell chemistry was used
- which read contains the RNA sequence
- which read contains the cell barcode and UMI
- whether the output is single-end, paired-end, or multi-read single-cell format

## 3. Reference and annotation information

The most important reference question is whether the gene IDs match the current Waus8730 reference.

Please record:

- genome/reference name
- genome/reference version
- annotation version
- gene ID format
- whether the data were aligned to Waus8730 v1 or a different Wolffia reference

If a different reference is used, the marker panel and ortholog bridge may need to be remapped before scoring.

## 4. Minimum metadata table

A simple sample-level metadata table is enough at the beginning. A cell-level table can be added after count matrices are generated.

Recommended columns:

```text
sample_id
condition
replicate
treatment_concentration
treatment_duration
batch
library_id
sequencing_run
reference_version
notes
```

If cell-level metadata are available, also include:

```text
cell_id
sample_id
cluster
leiden
qc_status
```

## 5. Pre-analysis QC checks

Before biological interpretation, check:

- file integrity
- read structure and read lengths
- total reads per sample
- estimated cells per sample
- median reads per cell
- median UMIs per cell
- median genes per cell
- total detected genes
- fraction of reads mapped to genes
- replicate consistency

These checks help separate real biological patterns from sequencing, alignment, or sample-quality artifacts.

## 6. Main analysis plan

The recommended analysis order is:

1. create or receive a gene-by-cell count matrix
2. run QC filtering
3. normalize and log-transform expression
4. cluster cells and build UMAP visualization
5. score the reviewed Wolffia native marker panel v1
6. compare marker-program scores by condition and replicate
7. apply the Arabidopsis-to-Wolffia transfer model as a secondary conservative view
8. manually inspect top marker genes before naming clusters or states

## 7. Example scoring command

After a normalized `.h5ad` file and metadata table are ready:

```bash
python scripts/40_score_future_wolffia_dataset.py \
  /path/to/future_wolffia_normalized_log1p.h5ad \
  --panel data/metadata/wolffia_reviewed_native_marker_panel_v1.csv \
  --metadata /path/to/future_metadata.csv \
  --metadata-cell-id-column cell_id \
  --group-columns condition,sample_id,replicate,cluster,leiden \
  --output-dir /path/to/output/reviewed_v1_scores
```

## 8. Main biological questions

The first-pass biological questions should stay broad:

- Are stress or protein-protection programs higher after salt treatment?
- Are transport, water-balance, or ion-related programs shifted after salt treatment?
- Are photosynthesis or carbon-fixation programs reduced or reorganized?
- Are growth or biosynthesis programs reduced after treatment?
- Are unknown Wolffia marker states enriched in treatment samples?
- Are changes consistent across biological replicates?

## 9. Expected outputs

Useful shareable outputs include:

- QC summary by sample
- UMAP colored by sample, condition, replicate, and cluster
- marker-program score summaries by condition
- marker-program score summaries by replicate
- cluster-level marker review table
- gene-coverage audit for the reviewed marker panel
- list of ambiguous or unknown marker states needing manual review

## 10. Current interpretation rule

The current safest conclusion should be program-level:

- high native marker score means a cell or cluster expresses a Wolffia marker program
- a treatment shift means the program is more or less active under that condition
- Arabidopsis transfer labels are conservative supporting evidence
- unknown-watchlist markers should be kept as reproducible Wolffia states until their biology is clearer

