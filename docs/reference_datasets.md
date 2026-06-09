# Reference Datasets and Resource Plan

## Goal

This document defines the public datasets and background resources needed for a prediction-first Wolffia project.

## Resource Categories

### 1. Public Plant Single-Cell RNA-seq References

Primary purpose:

- define known plant cell states
- collect robust marker genes
- study how developmental trajectories are analyzed in plants

Priority reference systems:

- `Arabidopsis thaliana`
- other plant single-cell atlases if they are well-annotated and publicly accessible

Desired properties of a good reference dataset:

- clear cell-type annotations
- accessible expression matrix and metadata
- published marker genes
- developmental context if possible

## Candidate Reference Cell Programs

These are initial categories to look for in public plant references:

- meristematic / proliferative cells
- epidermal cells
- photosynthetic / mesophyll-like cells
- vascular-associated cells
- reproductive or floral precursor states
- stress-responsive or transitional states

## 2. Wolffia-Specific Background Resources

Primary purpose:

- establish what is already known about Wolffia morphology and development
- define available genome / annotation resources
- support ortholog mapping and marker interpretation

Needed resource types:

- genome assembly
- gene annotation
- published developmental or morphology studies
- public transcriptome or bulk RNA-seq datasets if available

## 3. Duckweed / Lemnaceae Comparative Resources

Primary purpose:

- provide evolutionary context for Wolffia
- identify gene programs that may be shared across duckweeds
- distinguish Wolffia-specific features from general duckweed traits

Useful targets:

- other duckweed genomes
- duckweed transcriptomic studies
- reviews of duckweed development, physiology, and aquatic adaptation

## Planned Data Table

For each dataset or resource, record:

- resource name
- species
- data type
- source database
- accession or DOI
- developmental context
- annotation quality
- likely usefulness for Wolffia prediction

## Current Best Assumption

At the moment, we should assume that:

- public `Wolffia australiana` single-cell RNA-seq data may not yet be available
- the project will rely on reference transfer and comparative reasoning rather than direct Wolffia single-cell reanalysis

That assumption should be revisited after a more systematic search of:

- GEO
- SRA
- ENA
- ArrayExpress / BioStudies
- plant single-cell atlas papers and supplementary repositories

## Immediate Next Steps

1. build a spreadsheet of candidate reference datasets
2. identify 1 to 3 primary reference atlases to use first
3. collect published marker genes from those atlases
4. locate Wolffia genome and annotation files for downstream ortholog mapping
