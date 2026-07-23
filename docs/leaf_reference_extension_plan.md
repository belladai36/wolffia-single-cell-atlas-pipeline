# Arabidopsis Leaf Reference Extension Plan

## Why This Extension Matters

The current frozen transfer model was built from an Arabidopsis root reference because root single-cell atlases are well annotated and marker genes are well established. That made the root atlas the right first model system for testing whether the pipeline could recover broad, transferable plant cell programs.

However, `Wolffia australiana` is not root-like in the ordinary anatomical sense. Its reduced floating body is much more relevant to photosynthetic, surface, developmental-transition, and aquatic-interface programs. For that reason, the next reference layer should include at least one Arabidopsis leaf or aerial-tissue expression matrix.

## Refined Project Logic

The project should now be framed as a weighted two-reference strategy:

1. **Root-derived reference model**
   - strongest for benchmarking because root cell identities and markers are well characterized
   - useful for testing conservative transfer mechanics
   - especially informative for proliferative, developmental, transport, and stress-response programs
   - should be treated as a proof-of-concept and secondary comparison layer for Wolffia interpretation

2. **Leaf/aerial-tissue reference model**
   - biologically closer to the photosynthetic body plan of Wolffia
   - useful for photosynthetic, epidermal/surface, mesophyll-like, guard-cell-like, and stress/interface programs
   - needed to test whether root-derived ambiguity is caused by reference mismatch rather than true Wolffia simplification
   - should become the primary biological interpretation layer once a leaf-trained, ortholog-restricted model is benchmarked

The two references should not be treated as equal competing answers. Instead, the root model should be used to prove and stress-test the transfer pipeline, while the leaf/aerial model should carry more weight when making Wolffia-facing biological claims.

## Main Question for the Leaf Extension

Does adding an Arabidopsis leaf or aerial-tissue matrix make the Wolffia-facing predictions more biologically specific, especially for photosynthetic and surface-associated programs?

## Proposed Analysis Steps

### Step 1: Selected First Leaf Reference Matrix

The first selected leaf reference is `GSE161332`, **Single cell RNA sequencing of Col-0 leaf cell**.

Why it was selected:

- it is an Arabidopsis leaf single-cell dataset
- processed GEO matrix files are available in 10x-style format
- it includes leaf-relevant populations such as epidermis, guard cells, hydathodes, mesophyll, and vascular cell types
- it directly supports the root-versus-leaf comparison needed for Wolffia-facing photosynthetic, surface, and transport/interface programs

The practical conversion script is:

- [scripts/26_prepare_gse161332_leaf_h5ad.py](../scripts/26_prepare_gse161332_leaf_h5ad.py)

The first comparison config is:

- [config/public_reference_gse123818_wt_train_to_gse161332_leaf.yaml](../config/public_reference_gse123818_wt_train_to_gse161332_leaf.yaml)

### Selection Rule for Additional Leaf or Aerial Matrices

Preference order:

1. `GSE161332` as the first selected Arabidopsis leaf reference
2. an additional published Arabidopsis leaf single-cell or single-nucleus dataset with strong metadata
3. a public Arabidopsis aerial-tissue atlas with processed counts and usable metadata
4. a more targeted leaf dataset, if it has strong cell-type or cluster annotations

Selection criteria:

- processed expression matrix available
- metadata describing cell type, cluster, tissue region, or treatment
- enough cells to train or score broad programs
- clear relationship to photosynthesis, surface identity, or developmental state
- manageable local file size

### Step 2: Convert the Matrix to the Project Format

The selected dataset should be converted into the same `.h5ad` format used for the current public-reference workflow.

Required fields:

- expression matrix
- cell metadata in `adata.obs`
- gene metadata in `adata.var`
- source dataset identifier
- broad program labels where possible

### Step 3: Collapse Leaf Labels into the Existing Broad Ontology

Leaf or aerial cell labels should be mapped into the current eight-program framework:

- `proliferative_or_meristematic`
- `photosynthetic_or_assimilation`
- `vascular_like_or_transport`
- `developmental_transition`
- `epidermal_or_surface_identity`
- `reproductive_or_floral`
- `transport_interface_or_water_balance`
- `abiotic_stress_response`

If a leaf label does not fit cleanly, it should remain `ambiguous` or be kept as a source-specific sublabel rather than forced.

### Step 4: Compare Root-Derived and Leaf-Derived Predictions

The key comparison should ask:

- which programs are recovered by both references?
- which programs improve with the leaf reference?
- which programs remain ambiguous even after adding leaf information?
- does the leaf reference reduce over-assignment to stress-like programs?
- do photosynthetic and surface-associated programs become more separable?

Interpretation rule:

- if the leaf/aerial model is confident and marker-supported, prioritize that result for Wolffia biology
- if the root model is confident but the leaf/aerial model is weak or contradictory, treat the root result as secondary evidence rather than a final label
- if both models agree, consider the result stronger but still require marker-module and cluster support
- if the two models disagree, keep the cell or cluster ambiguous until additional Wolffia-native evidence is available

### Step 5: Prepare for Incoming Wolffia Single-Cell Data

When new Wolffia single-cell expression matrices become available, the first application should run both views:

1. root-derived frozen transfer model
2. leaf/aerial reference scoring or transfer model

Cells supported by both models can be considered higher-confidence. Cells supported mainly by the leaf/aerial model should be treated as more biologically relevant to Wolffia than cells supported only by the root model. Cells supported only by the root model should be interpreted cautiously and checked with marker modules, clustering, and biological context.

## Expected Outcomes

### If the Leaf Reference Improves Prediction

This would suggest that some current ambiguity is caused by using a root-biased reference for a highly reduced, photosynthetic plant body.

### If the Leaf Reference Gives Similar Conservative Results

This would support the idea that Wolffia's reduced body plan genuinely compresses or blurs canonical plant programs, rather than the result being only a reference mismatch.

### If Root and Leaf References Disagree Strongly

This would be biologically useful rather than a failure. It would identify the exact programs where Wolffia interpretation depends most heavily on reference choice.

## Near-Term Deliverable

The immediate deliverable is a leaf-prioritized root-versus-leaf reference comparison notebook that shows:

- label/program composition of the leaf reference
- overlap between root-selected and leaf-selected feature sets
- cross-reference transfer performance
- program-level prediction distributions
- visual comparison plots for photosynthetic, surface, transport, proliferative, and stress/interface programs
- a final interpretation table that separates primary leaf/aerial evidence from secondary root benchmark evidence

The computational first step is:

```bash
python scripts/26_prepare_gse161332_leaf_h5ad.py
python scripts/10_public_reference_statistical_prediction.py --config config/public_reference_gse123818_wt_train_to_gse161332_leaf.yaml
python scripts/34_train_leaf_primary_ortholog_model.py
```

The third command is the new leaf-primary retraining step. It should be interpreted carefully:
because the local `GSE161332` object does not include curated cell-type labels, the script trains
against marker-derived broad-program pseudo-labels from leaf pseudoclusters. This is useful for
testing whether a Wolffia-transferable leaf model is internally stable, but it is not a final
estimate of true biological annotation accuracy.

## Working Summary

The project is no longer only “use Arabidopsis root to predict Wolffia.” The refined version is:

> Use well-annotated Arabidopsis root data as a conservative benchmark, build Arabidopsis leaf/aerial data into the primary Wolffia-relevant photosynthetic reference, and then compare both against incoming Wolffia single-cell data with leaf/aerial evidence weighted more heavily for biological interpretation.
