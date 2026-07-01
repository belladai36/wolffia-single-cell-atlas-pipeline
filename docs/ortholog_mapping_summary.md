# Arabidopsis-to-Wolffia Ortholog Mapping

## Reference Resources

The mapping uses pinned NCBI RefSeq resources:

- *Arabidopsis thaliana*: [GCF_000001735.4](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001735.4/)
- *Wolffia australiana*: [GCF_029677425.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_029677425.1/)
- Wolffia annotation release: `GCF_029677425.1-RS_2025_12`

The Wolffia assembly is chromosome-level and is designated the RefSeq reference genome. The local workflow downloads protein FASTA and GFF3 files through NCBI Datasets.

## Method

1. Parse RefSeq GFF3 files to connect protein accessions to gene identifiers and annotations.
2. Select the longest annotated protein isoform for each gene.
3. Search requested Arabidopsis proteins against all Wolffia proteins with DIAMOND 2.2.2.
4. Search Wolffia proteins back against the full Arabidopsis protein set.
5. Collapse protein hits to genes and identify reciprocal best hits.
6. Grade mappings using sequence identity, query coverage, subject coverage, reciprocal status, and separation from the second-best gene hit.

DIAMOND is described by Buchfink et al., *Nature Methods* 18, 366–368 (2021), [doi:10.1038/s41592-021-01101-x](https://doi.org/10.1038/s41592-021-01101-x).

## Confidence Rules

- `high`: reciprocal best hit, at least 35% identity, at least 70% query coverage, at least 50% subject coverage, and a top/second bitscore ratio of at least 1.10
- `medium`: reciprocal best hit meeting the baseline thresholds
- `low`: directional best hit meeting the baseline thresholds but not reciprocal
- `unmapped`: no hit or a hit below 25% identity, 50% query coverage, or 40% subject coverage

Low-confidence mappings can support gene-family reasoning but are excluded from the first cross-species classifier feature set.

## Model Feature Coverage

Of the 2,000 Arabidopsis model features:

- high confidence: 217
- medium confidence: 123
- low confidence: 874
- unmapped or below threshold: 786

The initial Wolffia-transfer feature set therefore contains 340 genes, or 17.0% of the original model features.

## Marker Coverage

High- or medium-confidence marker coverage varies by program:

| Program | Coverage |
|---|---:|
| Reproductive/floral | 100.0% |
| Transport/interface or water balance | 60.0% |
| Photosynthetic/assimilation | 50.0% |
| Proliferative/meristematic | 40.0% |
| Developmental transition | 33.3% |
| Epidermal/surface identity | 20.0% |
| Abiotic stress response | 16.7% |
| Vascular-like/transport | 0.0% |

The vascular result does not prove vascular biology is absent from Wolffia. Most vascular markers have plausible family-level directional hits, but none meet the strict reciprocal criteria. The panel therefore needs family-aware refinement before absence claims are possible.

## Interpretation

Reciprocal protein similarity supports putative orthology, not conserved expression or function. Gene duplication, loss, annotation differences, and lineage-specific family expansion can break one-to-one reciprocity. Cross-species predictions should require adequate mapped-feature coverage and preserve an `ambiguous` result whenever evidence is weak.

## Reproduction

```bash
bash scripts/28_download_orthology_references.sh
python scripts/29_build_arabidopsis_wolffia_orthologs.py
python scripts/27_root_reference_consensus.py \
  --feature-list data/metadata/wolffia_transfer_feature_set.csv \
  --output-dir results/root_reference_consensus_ortholog_restricted \
  --figure-dir figures/root_reference_consensus_ortholog_restricted
```
