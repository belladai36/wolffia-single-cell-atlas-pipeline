# Wolffia Native Marker-Program Candidate Table

This note documents the first repo-friendly marker-program table derived directly from the public `Wolffia australiana` Waus8730 single-cell data.

The goal is to complement the Arabidopsis-to-Wolffia transfer model. The transfer model tells us which cells look similar to broad Arabidopsis-derived programs. The native marker-program table asks a different question: among Wolffia clusters that are often left ambiguous by the transfer model, which Wolffia genes and annotations repeatedly suggest interpretable biological programs?

## Input

The table was generated from the combined four-run public Wolffia marker review:

- `SRR29417743`
- `SRR29417744`
- `SRR29417745`
- `SRR29417746`

The upstream marker table was produced by `notebooks/10_public_wolffia_combined_umap_marker_review.ipynb` and stored outside the repository on external project storage:

```text
/Volumes/LaCie/wolffia_single_cell/results/combined_public_wolffia/four_run_leiden_marker_genes.csv
```

The repo stores the lightweight candidate summary here:

```text
data/metadata/wolffia_native_program_marker_candidates.csv
```

## Output table columns

- `native_program_id`: machine-readable candidate program name
- `native_program_name`: readable candidate program name
- `waus8730_gene_id`: Waus8730 gene identifier
- `preferred_name`: preferred annotation name when available
- `source_leiden_clusters`: Leiden clusters where the gene appeared as a marker
- `best_marker_rank`: best marker rank across clusters
- `max_marker_score`: strongest marker score observed
- `evidence_level`: simple priority level based on marker rank
- `annotation_summary`: eggNOG or gene-description text used for interpretation
- `candidate_rationale`: why the gene was assigned to the candidate program
- `review_status`: current status; all rows are candidates for manual review

## Candidate program groups

The current table contains candidate markers for these broad Wolffia-native programs:

- Photosynthesis / light harvesting
- Carbon fixation / assimilation
- Chloroplast gene expression / plastid translation
- Nutrient transport
- Ion / water balance
- Lipid / surface / cell-wall biology
- Stress / chaperone response
- RNA-binding / regulatory
- Unknown high-ranking marker

These are not final cell-type annotations. They are a structured starting point for deciding which Wolffia-native marker programs should be inspected more carefully.

## How this improves the project

The Arabidopsis transfer model is intentionally conservative. Many Wolffia cells are labeled `ambiguous` because the model should not force a plant with a reduced body plan into root or leaf labels that may not biologically fit.

This native marker-program layer helps interpret those ambiguous cells without overclaiming. It lets us:

1. keep the conservative Arabidopsis-transfer labels,
2. identify Wolffia-native marker patterns in the ambiguous clusters,
3. build focused marker panels for future Wolffia experiments, and
4. prepare a better baseline for future salt-stress or developmental datasets.

## Current interpretation

The strongest recurring signal across the public Waus8730 runs remains photosynthetic and chloroplast-related biology. Several clusters contain markers related to light harvesting, RuBisCO/carbon fixation, plastid gene expression, and electron-transfer processes.

Other candidate programs are present but should be treated more cautiously. These include nutrient transport, ion/water balance, lipid or surface-associated biology, and stress/chaperone-related markers. These categories are useful for hypothesis generation, especially for future salt-stress analysis, but they require manual review and comparison across biological replicates before being treated as stable Wolffia cell-state programs.

## Caveats

- The table is annotation-dependent, so incomplete or noisy Waus8730 gene descriptions can affect grouping.
- Candidate assignment is keyword-guided and should be manually reviewed.
- A gene appearing in this table does not prove a final cell type or state.
- The table should be used as a marker-prior list for interpretation, not as a validated annotation reference.

## Recommended next step

Use this table to define a small, manually reviewed Wolffia-native marker panel. Then compare those marker programs across the four public runs and, later, across control versus salt-stress Wolffia samples.
