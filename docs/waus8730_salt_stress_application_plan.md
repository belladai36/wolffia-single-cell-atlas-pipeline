# Waus8730 Salt-Stress Application Plan

## Purpose

This section adapts the existing Arabidopsis-to-Wolffia transfer framework for future
`Wolffia australiana` 8730 salt-stress single-cell data.

The goal is not to create a separate project. Instead, this is the first real-data application
layer for the current model:

```text
Arabidopsis leaf/root references
↓
Arabidopsis-Wolffia ortholog mapping
↓
Waus8730 gene-ID and annotation bridge
↓
Wolffia 8730 control-vs-salt single-cell analysis
```

## Why This Improves the Project

The current model is trained using Arabidopsis references and restricted to transferable
Arabidopsis-to-Wolffia genes. Future salt-stress data will likely use Waus8730 gene IDs from the
reference used during alignment or counting. Those IDs may not match the current NCBI-style
ortholog table directly.

The new Waus8730 layer helps solve that by adding:

- OrthoFinder orthogroups connecting Arabidopsis genes to Waus8730 genes
- eggNOG-mapper functional annotations for Waus8730 genes
- a derived bridge from current model features to Waus8730 IDs
- a salt-stress analysis plan that keeps biological replicates separate

## Current Experimental Design Assumptions

The expected design is:

- organism/reference: `Wolffia australiana` 8730
- control: 3 biological samples
- salt treatment: 3 biological replicates of `100 mM NaCl`
- likely stress duration: approximately 4 hours
- possible extra time point: not expected currently, but possible
- input material: protoplasts from approximately 1-2 g plant tissue
- loading target: approximately 17,000 cells per sample
- expected recovery: more than 10,000 cells per sample
- expected multiplet rate: less than 8%
- expected sequencing scale: approximately 340M reads per sample

These details should be updated once final library, sequencing, and file-format details are known.

## New Bridge Inputs

Two externally provided tables are useful:

```text
Orthogroups.csv
waemap.csv
```

`Orthogroups.csv` is used to connect Arabidopsis genes and Waus8730 genes through shared
orthogroups.

`waemap.csv` is used to add functional annotation to Waus8730 genes, including descriptions, GO
terms, KEGG terms, and protein domains when available.

Raw externally shared tables should not be committed unless permission and provenance are clear.
Instead, keep them in local, external, or cluster storage and generate derived bridge tables with:

```bash
python scripts/37_build_waus8730_annotation_bridge.py \
  --orthogroups /path/to/Orthogroups.csv \
  --waemap /path/to/waemap.csv \
  --output-dir data/metadata/waus8730_bridge
```

The main derived output is:

```text
data/metadata/waus8730_bridge/waus8730_model_feature_annotation_bridge.csv
```

## How the Model Should Be Applied

The current model should remain conservative:

1. apply the leaf-primary model as the main biological interpretation layer
2. apply the root benchmark as a secondary conservative check
3. preserve `ambiguous` and `review_required` categories
4. compare results across biological replicates, not just pooled cells
5. use Waus8730-native clusters and marker genes to review transfer labels

## Main Analysis Questions

The future salt-stress dataset can be used to ask:

- do the broad Arabidopsis-Wolffia ortholog-based programs appear in real Waus8730 data?
- are stress-response or transport/water-balance programs enriched after salt treatment?
- do photosynthesis-related or growth/proliferation programs change after salt treatment?
- are ambiguous or mixed states more common in salt-treated cells?
- do model-supported programs agree with Waus8730-native clusters and marker genes?
- which Waus8730 genes best mark each program or treatment-associated state?

## Planned Outputs

When the count matrix is available, the application should produce:

- QC summary by sample, replicate, and condition
- normalized `.h5ad` object with sample metadata
- UMAP colored by condition, replicate, cluster, and model prediction
- broad-program proportions by biological replicate
- module-score comparisons for stress, transport/water balance, photosynthesis, and growth
- differential expression within major model-supported programs
- marker genes for Waus8730-native clusters
- a summary of confident, ambiguous, and review-required labels

## Files Added for This Layer

- [Waus8730 salt-stress config](../config/waus8730_salt_stress.yaml)
- [Waus8730 bridge builder](../scripts/37_build_waus8730_annotation_bridge.py)

## Bottom Line

This application layer makes the project more useful for real Waus8730 salt-stress data by
connecting the existing transfer model to the gene IDs, functional annotations, and replicate
structure expected in the future experiment.

