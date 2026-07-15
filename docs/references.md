# References and Citation Guide

This file centralizes the project-level citations for the repository. Use it alongside
[`references.bib`](../references.bib), which contains BibTeX entries for manuscripts, posters, and
reports.

## How to Cite This Repository

Dai B. *Wolffia PIP-seq Single-Cell Atlas Framework*. 2026.
<https://github.com/belladai36/wolffia-single-cell-atlas-pipeline>

GitHub should also expose this citation through [`CITATION.cff`](../CITATION.cff).

## Arabidopsis Single-Cell Reference Datasets

- Denyer T, Ma X, Klesen S, Scacchi E, Nieselt K, Timmermans MCP. 2019.
  Spatiotemporal Developmental Trajectories in the Arabidopsis Root Revealed Using
  High-Throughput Single-Cell RNA Sequencing. *Developmental Cell* 48(6):840-852.e5.
  doi: [10.1016/j.devcel.2019.02.022](https://doi.org/10.1016/j.devcel.2019.02.022).
  Dataset: [GSE123818](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123818).

- Jean-Baptiste K, McFaline-Figueroa JL, Alexandre CM, Dorrity MW, Saunders L, Bubb KL,
  Trapnell C, Fields S, Queitsch C, Cuperus JT. 2019. Dynamics of Gene Expression in
  Single Root Cells of *Arabidopsis thaliana*. *The Plant Cell* 31(5):993-1011.
  doi: [10.1105/tpc.18.00785](https://doi.org/10.1105/tpc.18.00785).
  Dataset: [GSE121619](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121619).

- Wendrich JR, Yang B, Vandamme N, Verstaen K, Smet W, Van de Velde C, et al. 2020.
  Vascular transcription factors guide plant epidermal responses to limiting phosphate
  conditions. *Science* 370(6518). doi:
  [10.1126/science.aay4970](https://doi.org/10.1126/science.aay4970).
  Dataset: [GSE141730](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141730).

- Ogura N, Sasagawa Y, Ito T, Tameshige T, Kawai S, Sano M, et al. 2023.
  WUSCHEL-RELATED HOMEOBOX 13 suppresses de novo shoot regeneration via cell fate control
  of pluripotent callus. *Science Advances* 9(27):eadg6983.
  doi: [10.1126/sciadv.adg6983](https://doi.org/10.1126/sciadv.adg6983).
  Dataset: [GSE227564](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227564).

Additional candidate Arabidopsis datasets currently recorded in
[`data/metadata/arabidopsis_public_dataset_manifest.csv`](../data/metadata/arabidopsis_public_dataset_manifest.csv)
include:

- [GSE181999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE181999):
  *An Arabidopsis root phloem pole cell atlas reveals PINEAPPLE genes as transitioners to
  autotrophy*.
- [GSE308672](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308672):
  *Discrete and cell specific hypoxic responses in Arabidopsis roots resolved by single nuclei
  transcriptomics*.

Before using either in a submission, add its primary publication details if they are available.

## Wolffia Genome and Public Data Resources

- Park H, Park JH, Lee Y, Woo DU, Jeon HH, et al. 2021. Genome of the world's smallest
  flowering plant, *Wolffia australiana*, helps explain its specialized physiology and unique
  morphology. *Communications Biology* 4. doi:
  [10.1038/s42003-021-02422-5](https://doi.org/10.1038/s42003-021-02422-5).

- Hoang PTN, et al. 2022. The genome of *Wolffia australiana* facilitates discovery of
  genetic basis for aquatic adaptation in duckweeds. *The Plant Cell* 34(5):1536-1553.
  doi: [10.1093/plcell/koac068](https://doi.org/10.1093/plcell/koac068).

- NCBI Datasets. *Arabidopsis thaliana* genome assembly TAIR10.1, RefSeq
  [GCF_000001735.4](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001735.4/).

- NCBI Datasets. *Wolffia australiana* genome assembly, RefSeq
  [GCF_029677425.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_029677425.1/).

- NCBI BioProject [PRJNA1124135](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1124135):
  planned first Wolffia time-of-day single-cell training/application dataset.

- NCBI BioProject [PRJNA809022](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA809022):
  planned Wolffia single-nucleus validation dataset.

## Cross-Species Mapping and Analysis Software

- Buchfink B, Reuter K, Drost HG. 2021. Sensitive protein alignments at tree-of-life scale
  using DIAMOND. *Nature Methods* 18:366-368. doi:
  [10.1038/s41592-021-01101-x](https://doi.org/10.1038/s41592-021-01101-x).

- Tarashansky AJ, Musser JM, Khariton M, Li P, Arendt D, Quake SR, Wang B. 2021.
  Mapping single-cell atlases throughout Metazoa unravels cell type evolution.
  *eLife* 10:e66747. doi: [10.7554/eLife.66747](https://doi.org/10.7554/eLife.66747).
  Software: [atarashansky/SAMap](https://github.com/atarashansky/SAMap).

- Wolf FA, Angerer P, Theis FJ. 2018. SCANPY: large-scale single-cell gene expression data
  analysis. *Genome Biology* 19:15. doi:
  [10.1186/s13059-017-1382-0](https://doi.org/10.1186/s13059-017-1382-0).

- Wolf FA, Hamey FK, Plass M, Solana J, Dahlin JS, Göttgens B, Rajewsky N, Simon L,
  Theis FJ. 2019. PAGA: graph abstraction reconciles clustering with trajectory inference
  through a topology preserving map of single cells. *Genome Biology*. doi:
  [10.1186/s13059-019-1663-x](https://doi.org/10.1186/s13059-019-1663-x).

- Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, Blondel M,
  Prettenhofer P, Weiss R, Dubourg V, VanderPlas J, Passos A, Cournapeau D, Brucher M,
  Perrot M, Duchesnay E. 2011. Scikit-learn: Machine Learning in Python.
  *Journal of Machine Learning Research* 12:2825-2830.

- Virshup I, Rybakov S, Theis FJ, Angerer P, Wolf FA. 2024. anndata: Annotated data.
  *Journal of Open Source Software*. doi:
  [10.21105/joss.04371](https://doi.org/10.21105/joss.04371).

## Citation Maintenance Notes

- Before submitting a manuscript, verify every dataset actually used in the final analysis and
  remove citations for datasets that remained only candidates.
- Add DOI/publication details for PRJNA1124135 and PRJNA809022 if associated papers become
  available or if the repository moves from planning to real-data analysis.
- Keep `references.bib`, this file, and manuscript references synchronized.
