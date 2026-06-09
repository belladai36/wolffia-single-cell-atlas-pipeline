# Dataset Inventory

## Purpose

This table is the working inventory for public reference datasets and Wolffia-related resources that will support a prediction-first cell atlas project.

Use it to track:

- reference single-cell datasets
- Wolffia genome and annotation resources
- duckweed comparative transcriptomic resources
- whether each resource is ready for marker transfer, ortholog mapping, or hypothesis generation

## Column Definitions

- `resource_name`: short name of the dataset, paper, or resource
- `species`: organism represented by the resource
- `resource_type`: for example `scRNA-seq`, `genome`, `annotation`, `bulk RNA-seq`, `review`
- `source_database`: GEO, SRA, ENA, journal supplement, project website, and so on
- `accession_or_doi`: accession number or DOI
- `developmental_context`: tissue, stage, treatment, or system
- `annotation_quality`: `high`, `medium`, `low`, or `unknown`
- `planned_use`: how we expect to use the resource
- `status`: `to review`, `in review`, `usable`, or `not prioritized`
- `notes`: any caveats, questions, or next actions

## Working Table

| resource_name | species | resource_type | source_database | accession_or_doi | developmental_context | annotation_quality | planned_use | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| Arabidopsis reference atlas A | Arabidopsis thaliana | scRNA-seq | TBD | TBD | root or whole seedling preferred | TBD | primary marker transfer reference | to review | first target for systematic search |
| Arabidopsis reference atlas B | Arabidopsis thaliana | scRNA-seq | TBD | TBD | developmental atlas preferred | TBD | backup / comparison reference | to review | use if annotations are strong |
| Additional plant single-cell atlas | TBD plant species | scRNA-seq | TBD | TBD | tissue-specific | TBD | cross-species comparison | to review | only if clearly annotated and useful |
| Wolffia genome resource | Wolffia australiana | genome | TBD | TBD | species-wide reference | TBD | ortholog mapping and gene lookup | to review | confirm assembly and annotation source |
| Wolffia annotation resource | Wolffia australiana | annotation | TBD | TBD | species-wide reference | TBD | marker interpretation | to review | confirm GTF/GFF availability |
| Wolffia transcriptome resource | Wolffia australiana | bulk RNA-seq or transcriptome | TBD | TBD | any available tissue / condition | TBD | expression support for predicted programs | to review | useful even without scRNA-seq |
| Duckweed comparative resource 1 | duckweed / Lemnaceae | genome or transcriptome | TBD | TBD | comparative | TBD | evolutionary context | to review | helps separate Wolffia-specific vs duckweed-wide signals |
| Duckweed comparative resource 2 | duckweed / Lemnaceae | review | TBD | TBD | comparative | TBD | biological interpretation | to review | prioritize high-quality reviews |

## Near-Term Goals

### Goal 1

Fill in at least 3 strong public plant single-cell references.

### Goal 2

Identify the exact Wolffia genome and annotation resources we will use in the pipeline.

### Goal 3

Add at least 2 duckweed comparative resources that help interpret reduced or aquatic-specific programs.

## Completion Standard

This file becomes useful once each candidate resource has enough information for a yes/no decision about whether it belongs in the project.
