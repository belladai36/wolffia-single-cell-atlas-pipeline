# Public Wolffia SRR29417746 Model Application

## Purpose

This note records the first end-to-end application of the current ortholog-aware transfer framework to a public Wolffia single-cell RNA-seq run.

The goal of this step was not to make final biological cell-type claims. Instead, it tested whether the project can move from raw public Wolffia sequencing data to:

1. a Waus8730-aligned gene-by-cell count matrix,
2. a normalized AnnData object,
3. a Waus8730-to-Arabidopsis model-feature bridge, and
4. provisional leaf-primary/root-benchmark transfer predictions.

## Input dataset

- Public run: `SRR29417746`
- Project: `PRJNA1124135`
- Reference used for alignment/counting: `Waus8730.v1`
- Counting route: STARsolo
- Cell barcode and UMI structure used for this run:
  - read 1: sample index, 8 bp
  - read 2: cell barcode and UMI, 28 bp
  - read 3: transcript/cDNA read, 91 bp
  - model used for counting: 16 bp cell barcode + 12 bp UMI from read 2

## STARsolo count matrix result

STARsolo produced a filtered matrix with:

- 2,718 cells
- 15,080 Waus8730 genes/features
- 4,268,225 nonzero gene-by-cell entries

Important STARsolo summary metrics:

| Metric | Value |
|---|---:|
| Reads processed | 446,999,681 |
| Estimated cells | 2,718 |
| Reads mapped to genome, unique + multiple | 94.5% |
| Reads mapped uniquely to genome | 48.0% |
| Reads mapped uniquely to genes | 38.3% |
| Median raw UMIs per cell | 2,595.5 |
| Median genes per cell | 902.5 |
| Total genes detected | 13,462 |

The field `Reads With Valid Barcodes` was not interpreted as a strict quality metric here because STARsolo was run without a barcode whitelist. This was intentional for the first public-data test because the exact chemistry/whitelist was not yet confirmed.

## Waus8730 ortholog bridge

The current transfer model uses 340 Arabidopsis model features. The Waus8730 bridge connected those features to Waus8730 gene IDs using externally provided OrthoFinder and eggNOG-mapper tables.

Bridge summary:

| Metric | Value |
|---|---:|
| Arabidopsis model features | 340 |
| Model features mapped to Waus8730 orthogroups | 309 |
| Waus8730 genes in bridge | 557 |
| Bridge rows | 582 |
| Real model-feature coverage | 90.9% |

For one-to-many Arabidopsis-to-Waus8730 mappings, the Waus8730 candidate genes were averaged after full-matrix library-size normalization and log transformation. This avoids artificially inflating a model feature just because one Arabidopsis gene has multiple Waus8730 candidates.

## Normalization and model input

The STARsolo filtered matrix was converted into AnnData and normalized by:

1. preserving raw counts,
2. normalizing each cell to 10,000 total counts,
3. applying `log1p`,
4. projecting Waus8730 expression into the 340-feature Arabidopsis model space through the Waus8730 orthogroup bridge.

The resulting model-input object contained:

- 2,718 cells
- 340 Arabidopsis-space model features
- 309 mapped features
- 31 zero-filled missing features

## Transfer model result

The leaf-primary and root-benchmark transfer script was applied to the model-input AnnData object.

Model application summary:

| Output label | Cells |
|---|---:|
| ambiguous | 2,350 |
| photosynthetic_or_assimilation | 347 |
| vascular_like_or_transport | 21 |

Status summary:

| Status | Cells |
|---|---:|
| both models ambiguous | 2,349 |
| primary leaf supported, root ambiguous | 368 |
| secondary root-like signal only | 1 |

Acceptance rates:

- leaf-primary acceptance rate: 13.5%
- root-benchmark acceptance rate: 0.04%

## Interpretation

This result is consistent with the intended conservative behavior of the framework.

Most cells remained ambiguous, which means the model did not force labels where the current Arabidopsis-derived transfer evidence was weak. A smaller subset of cells showed leaf-primary support, especially for photosynthetic or assimilation-like programs. The root-benchmark layer was almost entirely ambiguous, which is expected because this Wolffia dataset is not expected to resemble a canonical Arabidopsis root reference.

The main conclusion is that the pipeline can now process a real public Wolffia single-cell run into a usable matrix and produce provisional ortholog-aware program predictions. The next analysis step is to evaluate whether these predictions align with native Wolffia clustering, marker genes, and sample-level structure.

## Caveats

- The result is provisional and should not be treated as final Wolffia cell-type annotation.
- The Waus8730 feature bridge is based on orthogroups, not experimentally validated one-to-one functional equivalence.
- Some Arabidopsis model features map to multiple Waus8730 candidates, so candidate expression was averaged.
- Barcode handling can be improved if the exact library chemistry and barcode whitelist become available.
- Cluster-level marker analysis is still needed before assigning stronger biological interpretations.

## Pushable summary file

A compact machine-readable summary of this run is stored in:

- `data/metadata/public_wolffia_srr29417746_model_application_summary.csv`

Large raw outputs, `.h5ad` files, FASTQ files, STAR indexes, and matrix files should remain in external storage rather than GitHub.
