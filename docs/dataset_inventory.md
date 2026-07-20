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
| Jean-Baptiste Arabidopsis root single-cell reference | Arabidopsis thaliana | scRNA-seq | journal supplement / public repository | paper-level reference locked; exact accession to verify later | root cell-state atlas | high | primary marker transfer reference | usable | locked into Phase 1 reference panel because it supports conservative marker collection |
| Shulse Arabidopsis root single-cell reference | Arabidopsis thaliana | scRNA-seq | journal supplement / public repository | paper-level reference locked; exact accession to verify later | root cell-type profiling | high | cross-reference for marker stability | usable | reduces dependence on a single annotation scheme |
| Denyer Arabidopsis developmental root trajectory reference | Arabidopsis thaliana | scRNA-seq | journal supplement / public repository | paper-level reference locked; exact accession to verify later | developmental root trajectories | high | developmental transition and pseudotime reference | usable | especially important for testing the idea of compressed or continuous Wolffia states |
| GSE161332 Arabidopsis leaf single-cell reference | Arabidopsis thaliana | scRNA-seq | GEO | GSE161332 | leaf, enriched leaf vasculature, mesophyll, epidermis, guard cells, hydathodes | medium to high | first root-versus-leaf comparison; photosynthetic, surface, mesophyll-like, vascular/transport, and stress/interface programs | selected | selected because processed 10x-style matrix files are available and the biology is more Wolffia-relevant than root alone |
| Genome of the world's smallest flowering plant, Wolffia australiana, helps explain its specialized physiology and unique morphology | Wolffia australiana | genome | Communications Biology | 10.1038/s42003-021-02389-w | species-wide genome and morphology resource | medium | foundational Wolffia background; candidate genome source | usable | anchors morphology, reduction, and genome context |
| The genome of Wolffia australiana facilitates discovery of genetic basis for aquatic adaptation in duckweeds | Wolffia australiana | genome / annotation | The Plant Cell | 10.1093/plcell/koac068 | species-wide genome and comparative duckweed resource | high | ortholog reasoning, annotation context, aquatic adaptation interpretation | usable | strongest currently locked Wolffia genome-context paper for Phase 1 |
| Wolffia public transcriptome resource | Wolffia australiana | bulk RNA-seq or transcriptome | SRA / GEO / journal supplement | accession still to verify | any available tissue or condition | medium | expression support for predicted programs | in review | valuable but not required to finish first-pass marker mapping |
| Small but mighty: The genomics of the world's smallest flowering plants | duckweed / Wolffia | review | Current Opinion in Plant Biology | 10.1016/j.pbi.2021.102153 | comparative genomics and evolutionary reduction | high | novelty framing and comparative interpretation | usable | strong review for the biological logic of reduced morphology versus retained programs |
| Duckweeds: Omnipresent tiny plants with profound applications in agriculture and food | duckweed / Lemnaceae | review | Plants | 10.3390/plants11121641 | comparative duckweed biology and applied context | medium | broad duckweed background | usable | secondary context for Lemnaceae biology |
| Nutritional value of duckweeds (Lemnaceae) as human food | duckweed / Lemnaceae | review | Frontiers in Chemistry | 10.3389/fchem.2023.1134924 | comparative duckweed physiology and composition | low | optional context only | not prioritized | not directly useful for cell-state prediction |

## Near-Term Goals

### Goal 1

Lock and document 3 strong public plant single-cell references.

### Goal 2

Identify the exact Wolffia genome and annotation resources we will use in the pipeline.

### Goal 3

Add at least 2 duckweed comparative resources that help interpret reduced or aquatic-specific programs.

### Goal 4

Convert `GSE161332` into `.h5ad` and compare its broad-program behavior against the existing root-derived reference model.

## Completion Standard

This file becomes useful once each candidate resource has enough information for a yes/no decision about whether it belongs in the project.

## First-Pass Search Notes

- As of `2026-06-09`, a quick current search did **not** reveal an obvious public `Wolffia australiana` single-cell RNA-seq atlas.
- This project should therefore continue with a prediction-first design unless a dedicated Wolffia single-cell dataset is identified later.
- For Phase 1, the Arabidopsis reference panel is considered locked at the paper level even though some exact repository accessions still need later verification.
