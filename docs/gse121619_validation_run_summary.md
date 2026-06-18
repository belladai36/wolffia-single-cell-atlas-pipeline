# GSE121619 Validation Run Summary

## What was done

We added `GSE121619` as a second Arabidopsis validation target using the processed GEO Monocle object.

Files and scripts used:

- [scripts/14_extract_gse121619_from_monocle.R](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/14_extract_gse121619_from_monocle.R)
- [scripts/15_prepare_gse121619_h5ad.py](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/scripts/15_prepare_gse121619_h5ad.py)
- [config/public_reference_gse121619.yaml](/Users/bella/Documents/Wolffia%20Single-Cell%20Atlas%20Pipeline%20Before%20the%20Data%20Arrive/config/public_reference_gse121619.yaml)
- source dataset: [GSE121619](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121619)

## Intake result

The `All` split of the GEO Monocle object converted successfully into a local `.h5ad`.

Recovered object dimensions:

- genes: `37,336`
- cells: `2,085`

Recovered metadata columns include:

- `treatment_id`
- `louvain_component`
- `State`
- `UMAP1`, `UMAP2`
- `TSNE.1`, `TSNE.2`

This means `GSE121619` is now a practical validation dataset in our workflow, not just a candidate accession.

## Transfer result

Training reference:

- `GSE227564_callus`

Validation target:

- `GSE121619_all_root`

Predicted broad programs on the target dataset:

- `aquatic_adaptation_or_stress`: `1900`
- `proliferative_or_meristematic`: `47`
- `developmental_transition`: `46`
- `photosynthetic_or_assimilation`: `5`
- `reproductive_or_floral`: `2`

## Treatment-level pattern

Predictions by treatment:

- `Control`
  - stress-like: `945`
  - developmental: `45`
  - proliferative: `42`
  - photosynthetic: `4`
- `HeatShock`
  - stress-like: `955`
  - developmental: `1`
  - proliferative: `5`
  - photosynthetic: `1`
  - reproductive: `2`

## Interpretation

This validation run strengthens our current working interpretation in three ways.

### 1. The dominant transfer pattern is reproducible

Our first Arabidopsis validation target (`GSE141730`) was already dominated by `aquatic_adaptation_or_stress`.

Now `GSE121619` shows the same broad outcome.

That suggests the stress-like or adaptive program is not a one-dataset accident.

### 2. Developmental and proliferative predictions shrink under heat shock

The `developmental_transition` and `proliferative_or_meristematic` predictions are mostly found in control cells and become rare in heat-shocked cells.

That is biologically plausible and encouraging:

- it suggests the transferred broad programs are responding to condition changes in a sensible direction
- it makes the classifier look more meaningful than a random label propagator

### 3. Broad programs are transferable, but not evenly represented

We do not see balanced representation across all programs.

Instead, a few programs dominate strongly.

That supports the idea that later Wolffia analyses should focus on:

- which programs are strongly preserved
- which are weak but detectable
- which fail to separate clearly

rather than expecting every canonical plant program to appear as a crisp, equally sized cluster.

## What this means for Wolffia predictions

This is now a stronger basis for our Wolffia-first hypotheses.

If Wolffia later shows:

- a dominant adaptive or stress-like program
- small proliferative subpopulations
- weakly separable developmental states

then those outcomes should not automatically be dismissed as technical failure, because similar asymmetry already appears in Arabidopsis transfer settings.

Instead, we will need to ask:

- is the program genuinely preserved but compressed
- is the program condition-sensitive
- or is it lost as a distinct identity

## Practical next step

The most useful next dataset remains:

- `GSE123818` for a broader developmental root atlas comparison

That will help us decide whether the current dominance of the stress-like program is a general feature of cross-dataset transfer or whether it is specific to the currently sampled validation sets.
